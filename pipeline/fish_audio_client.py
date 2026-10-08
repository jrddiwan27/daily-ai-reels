import os
import re
import json
import requests
import subprocess

FISH_API_KEY = os.environ.get("FISH_API_KEY") or "sk-fish-e_CiO1ZoKFL64y_iv6_dEHz6EZ15WoNv0fRZx5Mq-mk"
VOICE_ID = os.environ.get("FISH_VOICE_ID") or "c85fb11f91f84312a4bd16756f298ae2"

def generate_voiceover(text: str, output_audio_path: str = "assets/voice.mp3") -> float:
    """
    Generates high-fidelity voiceover using Fish Audio S2.1 Pro Free API.
    Returns total audio duration in seconds.
    """
    url = "https://api.fish.audio/v1/tts"
    headers = {
        "Authorization": f"Bearer {FISH_API_KEY}",
        "Content-Type": "application/json",
        "model": "s2.1-pro-free"
    }
    
    payload = {
        "text": text,
        "reference_id": VOICE_ID,
        "format": "mp3"
    }
    
    print(f"[*] Requesting Fish Audio voiceover for {len(text)} characters...")
    res = requests.post(url, headers=headers, json=payload, stream=True)
    
    if res.status_code != 200:
        raise RuntimeError(f"Fish Audio failed with code {res.status_code}: {res.text}")
        
    os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)
    with open(output_audio_path, "wb") as f:
        for chunk in res.iter_content(chunk_size=2048):
            if chunk:
                f.write(chunk)
                
    # Get exact duration via ffprobe
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", output_audio_path
    ]
    duration_str = subprocess.check_output(cmd).decode().strip()
    duration = float(duration_str)
    print(f"[✓] Voiceover successfully generated: {output_audio_path} ({duration:.2f}s)")
    return duration

def generate_caption_chunks(text: str, total_duration: float, output_chunks_path: str = "assets/caption_chunks.json"):
    """
    Splits text into 1-3 word kinetic caption chunks synchronized proportionally to audio length.
    """
    raw_words = re.findall(r'\S+', text)
    chunks = []
    
    # Target ~2 words per chunk for fast-paced visual rhythm
    i = 0
    total_words = len(raw_words)
    time_per_word = total_duration / max(total_words, 1)
    
    while i < total_words:
        chunk_size = 2 if (i + 1 < total_words) else 1
        group = raw_words[i:i + chunk_size]
        start_time = round(i * time_per_word, 2)
        end_time = round((i + len(group)) * time_per_word, 2)
        
        chunks.append({
            "words": group,
            "active": min(1, len(group) - 1),
            "start": start_time,
            "end": end_time
        })
        i += chunk_size
        
    with open(output_chunks_path, "w") as f:
        json.dump(chunks, f, indent=2)
        
    print(f"[✓] Generated {len(chunks)} synchronized caption chunks at {output_chunks_path}")
    return chunks

if __name__ == "__main__":
    sample_text = "Stop paying for expensive AI subscriptions. Here are five insane open-source GitHub repos every developer needs right now."
    dur = generate_voiceover(sample_text, "assets/sample_voice.mp3")
    generate_caption_chunks(sample_text, dur, "assets/sample_chunks.json")
