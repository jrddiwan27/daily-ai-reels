import os
import requests
import json

FISH_API_KEY = "sk-fish-e_CiO1ZoKFL64y_iv6_dEHz6EZ15WoNv0fRZx5Mq-mk"
VOICE_ID = "c85fb11f91f84312a4bd16756f298ae2"

def test_fish_audio():
    url = "https://api.fish.audio/v1/tts"
    headers = {
        "Authorization": f"Bearer {FISH_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": "Stop paying for expensive AI subscriptions. Here are five insane open-source GitHub repos every developer needs right now.",
        "reference_id": VOICE_ID,
        "format": "mp3",
        "latency": "normal"
    }
    
    print("[*] Sending TTS request to Fish Audio API...")
    response = requests.post(url, headers=headers, json=payload, stream=True)
    
    print(f"[*] Response status code: {response.status_code}")
    if response.status_code == 200:
        out_path = "assets/test_fish_audio.mp3"
        with open(out_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"[✓] Audio successfully generated and saved to {out_path} ({os.path.getsize(out_path)} bytes)")
        return True
    else:
        print(f"[✗] Error: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    test_fish_audio()
