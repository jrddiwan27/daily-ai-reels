import os
import re
import json
import requests
import subprocess

FISH_API_KEY = os.environ.get("FISH_API_KEY") or "sk-fish-e_CiO1ZoKFL64y_iv6_dEHz6EZ15WoNv0fRZx5Mq-mk"
VOICE_ID = os.environ.get("FISH_VOICE_ID") or "c85fb11f91f84312a4bd16756f298ae2"

def parse_vtt_to_word_chunks(vtt_path: str, output_chunks_path: str = "assets/caption_chunks.json"):
    """
    Parses a WebVTT file and extracts word-by-word kinetic subtitle chunks.
    """
    if not os.path.exists(vtt_path):
        return []

    with open(vtt_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern for timestamp cues: 00:00:00.100 --> 00:00:02.400 or 00:00:00,100 --> 00:00:02,400
    cue_pattern = re.compile(
        r'(\d{2}:\d{2}:\d{2}[.,]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[.,]\d{3})\s*\n(.*?)(?=\n\s*\n|\Z)',
        re.DOTALL
    )

    def parse_sec(ts_str):
        ts_str = ts_str.replace(',', '.')
        parts = ts_str.split(':')
        return round(float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2]), 3)

    chunks = []
    matches = cue_pattern.findall(content)

    for start_raw, end_raw, cue_text in matches:
        st = parse_sec(start_raw)
        et = parse_sec(end_raw)
        clean_text = re.sub(r'<[^>]+>', '', cue_text).strip()
        words = clean_text.split()
        if not words:
            continue

        cue_dur = max(0.1, et - st)
        word_dur = cue_dur / len(words)

        # Emit 1-2 words per kinetic chunk
        idx = 0
        while idx < len(words):
            grp = words[idx:idx + 2]
            c_st = round(st + idx * word_dur, 2)
            c_et = round(st + (idx + len(grp)) * word_dur, 2)
            chunks.append({
                "words": grp,
                "text": " ".join(grp),
                "start": c_st,
                "end": c_et
            })
            idx += 2

    with open(output_chunks_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    return chunks

def generate_voiceover(text: str, output_audio_path: str = "assets/voice.mp3") -> float:
    """
    Generates high-fidelity voiceover with exact subtitle sync.
    Attempts Fish Audio first; falls back smoothly to Edge-TTS (Andrew Multilingual Neural +10%).
    Returns exact duration in seconds.
    """
    os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)
    vtt_path = output_audio_path.rsplit(".", 1)[0] + ".vtt"

    # Try Fish Audio
    fish_ok = False
    try:
        url = "https://api.fish.audio/v1/tts"
        headers = {
            "Authorization": f"Bearer {FISH_API_KEY}",
            "Content-Type": "application/json",
            "model": "s2.1-pro-free"
        }
        payload = {"text": text, "reference_id": VOICE_ID, "format": "mp3"}
        res = requests.post(url, headers=headers, json=payload, stream=True, timeout=8)
        if res.status_code == 200:
            with open(output_audio_path, "wb") as f:
                for chunk in res.iter_content(chunk_size=2048):
                    if chunk:
                        f.write(chunk)
            fish_ok = True
    except Exception as e:
        print(f"[*] Fish Audio note: {e}")

    # Fallback to Edge-TTS with Andrew Multilingual Neural (+10% rate for high retention)
    if not fish_ok:
        print("[*] Synthesizing via Edge-TTS (en-US-AndrewMultilingualNeural @ +10%)...")
        cmd = [
            "edge-tts",
            "--voice", "en-US-AndrewMultilingualNeural",
            "--rate=+10%",
            "--text", text,
            "--write-media", output_audio_path,
            "--write-subtitles", vtt_path
        ]
        subprocess.check_call(cmd)

    # Get exact duration via ffprobe
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", output_audio_path
    ]
    duration_str = subprocess.check_output(cmd).decode().strip()
    duration = round(float(duration_str), 2)
    print(f"[✓] Voiceover successfully generated: {output_audio_path} ({duration:.2f}s)")

    # Generate or parse subtitle chunks
    captions_path = "assets/caption_chunks.json"
    if os.path.exists(vtt_path):
        parse_vtt_to_word_chunks(vtt_path, captions_path)
    else:
        generate_caption_chunks(text, duration, captions_path)

    return duration

def generate_caption_chunks(text: str, total_duration: float, output_chunks_path: str = "assets/caption_chunks.json"):
    """
    Splits text into 1-2 word kinetic caption chunks synchronized proportionally to audio length.
    """
    raw_words = re.findall(r'\S+', text)
    chunks = []
    i = 0
    total_words = len(raw_words)
    time_per_word = total_duration / max(total_words, 1)

    while i < total_words:
        group = raw_words[i:i + 2]
        start_time = round(i * time_per_word, 2)
        end_time = round((i + len(group)) * time_per_word, 2)
        chunks.append({
            "words": group,
            "text": " ".join(group),
            "start": start_time,
            "end": end_time
        })
        i += len(group)

    with open(output_chunks_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    return chunks

if __name__ == "__main__":
    dur = generate_voiceover("Stop doing manual testing. Meet iPhone Use, the open source AI agent controlling physical iPhones over USB.")
    print("Test run duration:", dur)
