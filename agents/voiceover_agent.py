import os
import re
import json
import subprocess
from dotenv import load_dotenv

load_dotenv()

def parse_vtt_timeline(vtt_path: str, output_path: str = "assets/word_timeline.json"):
    """
    Parses WebVTT subtitle stream into exact per-word timestamps.
    """
    if not os.path.exists(vtt_path):
        return []

    with open(vtt_path, "r", encoding="utf-8") as f:
        content = f.read()

    cue_pattern = re.compile(
        r'(\d{2}:\d{2}:\d{2}[.,]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[.,]\d{3})\s*\n(.*?)(?=\n\s*\n|\Z)',
        re.DOTALL
    )

    def parse_sec(ts_str):
        ts_str = ts_str.replace(',', '.')
        parts = ts_str.split(':')
        return round(float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2]), 3)

    matches = cue_pattern.findall(content)
    timeline = []

    for start_raw, end_raw, cue_text in matches:
        st = parse_sec(start_raw)
        et = parse_sec(end_raw)
        clean = re.sub(r'<[^>]+>', '', cue_text).strip()
        words = clean.split()
        if not words:
            continue

        cue_dur = max(0.1, et - st)
        word_dur = cue_dur / len(words)

        for idx, w in enumerate(words):
            w_st = round(st + idx * word_dur, 2)
            w_et = round(st + (idx + 1) * word_dur, 2)
            timeline.append({
                "word": w,
                "start": w_st,
                "end": w_et,
                "second": int(w_st)
            })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(timeline, f, indent=2)

    return timeline

def generate_mouth_visemes(audio_path: str, timeline: list, fps: int = 30) -> list:
    """
    Generates 4-state RMS lip-sync mouth animation frames ('closed', 'slight', 'half', 'wide').
    """
    import numpy as np

    # Decode audio to raw PCM via ffmpeg
    cmd = [
        "ffmpeg", "-y", "-i", audio_path,
        "-ac", "1", "-ar", "16000", "-f", "s16le", "-"
    ]
    raw_pcm = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
    samples = np.frombuffer(raw_pcm, dtype=np.int16).astype(np.float32)

    # Frame parameters
    samples_per_frame = int(16000 / fps)
    total_frames = int(len(samples) / samples_per_frame)

    mouth_frames = []
    # Compute RMS amplitude per frame
    rms_values = []
    for f in range(total_frames):
        chunk = samples[f * samples_per_frame:(f + 1) * samples_per_frame]
        rms = np.sqrt(np.mean(chunk**2)) if len(chunk) > 0 else 0
        rms_values.append(rms)

    max_rms = max(rms_values) if rms_values and max(rms_values) > 0 else 1.0

    for f, rms in enumerate(rms_values):
        norm = rms / max_rms
        if norm < 0.08:
            m = "closed"
        elif norm < 0.28:
            m = "slight"
        elif norm < 0.60:
            m = "half"
        else:
            m = "wide"
        mouth_frames.append({"f": f, "t": round(f / fps, 3), "mouth": m})

    with open("assets/mouth_sync.json", "w") as f:
        json.dump(mouth_frames, f, indent=2)

    return mouth_frames

def run_voiceover_agent(script_path: str = "assets/viral_script.json", script_data: dict = None) -> dict:
    """
    VOICEOVER AGENT:
    Generates studio broadcast narration, extracts second-by-second word timestamps,
    and produces frame-accurate RMS lip-sync visemes.
    """
    print("=" * 65)
    print(f"🎙️ [AGENT 3: VOICEOVER AGENT] Synthesizing Studio Voiceover & Word Timeline...")
    print("=" * 65)

    if script_data:
        os.makedirs("assets", exist_ok=True)
        with open(script_path, "w") as f:
            json.dump(script_data, f, indent=2)
    elif os.path.exists(script_path):
        with open(script_path, "r") as f:
            script_data = json.load(f)
    else:
        raise FileNotFoundError(f"Script file {script_path} not found.")

    full_text = script_data.get("full_script", "")
    clean_text = re.sub(r'[*_#`]', '', full_text).strip()
    os.makedirs("assets", exist_ok=True)
    audio_path = "assets/voice.mp3"
    vtt_path = "assets/voice.vtt"
    script_txt = "assets/voice_text.txt"
    with open(script_txt, "w", encoding="utf-8") as f:
        f.write(clean_text)

    # Edge-TTS Studio Guy +12% rate for high retention
    voice_name = "en-US-GuyNeural"
    print(f"[*] Generating speech via edge-tts ({voice_name} @ +12%)...")
    cmd = [
        "edge-tts",
        "--voice", voice_name,
        "--rate=+12%",
        "--file", script_txt,
        "--write-media", audio_path,
        "--write-subtitles", vtt_path
    ]
    try:
        subprocess.check_call(cmd, timeout=25)
    except Exception as e:
        print(f"[!] Primary voice failed ({e}), trying fallback en-US-ChristopherNeural...")
        cmd[2] = "en-US-ChristopherNeural"
        subprocess.check_call(cmd, timeout=25)

    # Get exact audio duration via ffprobe
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    dur = float(subprocess.check_output(probe_cmd).decode().strip())
    print(f"[✓] Voiceover audio generated: {audio_path} ({dur:.2f}s)")

    # Extract word-by-word timeline
    timeline = parse_vtt_timeline(vtt_path, "assets/word_timeline.json")
    print(f"[✓] Extracted {len(timeline)} word timestamps across {int(dur)} seconds.")

    # Generate lip-sync mouth data
    mouth_data = generate_mouth_visemes(audio_path, timeline, fps=30)
    print(f"[✓] Generated {len(mouth_data)} mouth viseme frames for character rig.")

    return {
        "audio_path": audio_path,
        "vtt_path": vtt_path,
        "duration": round(dur, 2),
        "total_words": len(timeline),
        "total_visemes": len(mouth_data)
    }

if __name__ == "__main__":
    run_voiceover_agent()
