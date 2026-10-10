import os
import json
import wave
import subprocess
import numpy as np

def generate_lipsync_data(
    audio_path: str = "assets/voice.mp3",
    caption_chunks_path: str = "assets/caption_chunks.json",
    output_mouth_path: str = "assets/mouth.json",
    fps: int = 30
) -> list:
    """
    Deterministically computes lip-sync mouth states and blinks:
    1. Decodes audio to mono 16kHz WAV
    2. Computes RMS per frame (window 33.33ms, hop 33.33ms)
    3. Normalizes by 95th percentile and applies 3-frame moving average
    4. Quantizes to 4 states with hysteresis:
       closed < 0.12 < small < 0.35 < open < 0.60 < wide
       - State changes at most once per 2 frames unless jumping >= 2 levels (plosive onset)
    5. Forces 'closed' during inter-word gaps > 120ms
    6. Blinks eyelids automatically every 90 frames (frame % 90 < 4)
    7. Outputs mouth.json = [{"f": int, "mouth": str, "blink": bool}]
    """
    # 1. Decode to 16kHz Mono WAV
    wav_path = "assets/voice_mono.wav"
    os.makedirs("assets", exist_ok=True)
    cmd = f'ffmpeg -y -i "{audio_path}" -ac 1 -ar 16000 "{wav_path}"'
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.exists(wav_path):
        raise FileNotFoundError(f"Failed to decode audio to WAV: {wav_path}")

    with wave.open(wav_path, "rb") as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        raw_bytes = wf.readframes(n_frames)

    samples = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0
    total_duration = n_frames / framerate
    total_video_frames = int(np.ceil(total_duration * fps))

    # Frame window & hop in audio samples
    samples_per_frame = int(round(framerate / fps)) # ~533 samples for 16kHz @ 30fps

    # 2. Compute RMS per frame
    raw_rms = []
    for f in range(total_video_frames):
        start_idx = f * samples_per_frame
        end_idx = min(start_idx + samples_per_frame, len(samples))
        if start_idx >= len(samples):
            chunk = np.zeros(samples_per_frame)
        else:
            chunk = samples[start_idx:end_idx]
            if len(chunk) < samples_per_frame:
                chunk = np.pad(chunk, (0, samples_per_frame - len(chunk)))
        rms = np.sqrt(np.mean(chunk ** 2))
        raw_rms.append(rms)

    raw_rms = np.array(raw_rms)

    # 3. Normalize by 95th percentile
    p95 = np.percentile(raw_rms[raw_rms > 0], 95) if np.any(raw_rms > 0) else 1e-4
    if p95 < 1e-6:
        p95 = 1e-4
    norm_rms = np.clip(raw_rms / p95, 0.0, 1.5)

    # 3-frame moving average smoothing
    kernel = np.ones(3) / 3.0
    smooth_rms = np.convolve(norm_rms, kernel, mode="same")

    # 4. Extract word timing intervals from captions for silence clamping
    word_intervals = []
    if os.path.exists(caption_chunks_path):
        try:
            with open(caption_chunks_path, "r") as cf:
                chunks = json.load(cf)
            for c in chunks:
                word_intervals.append((c.get("start", 0.0), c.get("end", 0.0)))
        except Exception:
            pass

    # 5. Quantize with hysteresis
    # 0 = closed (< 0.12), 1 = small (0.12 - 0.35), 2 = open (0.35 - 0.60), 3 = wide (>= 0.60)
    def val_to_level(v: float) -> int:
        if v < 0.12:
            return 0
        elif v < 0.35:
            return 1
        elif v < 0.60:
            return 2
        else:
            return 3

    state_names = ["closed", "small", "open", "wide"]
    mouth_data = []

    current_level = 0
    last_change_frame = -99

    for f in range(total_video_frames):
        t_sec = f / fps
        raw_target_level = val_to_level(smooth_rms[f])

        # Check silence gap between words (> 120ms gap)
        in_speech = False
        for (w_start, w_end) in word_intervals:
            if (w_start - 0.06) <= t_sec <= (w_end + 0.06):
                in_speech = True
                break

        if not in_speech and word_intervals:
            target_level = 0
        else:
            target_level = raw_target_level

        # Hysteresis: change at most once per 2 frames, except when jumping >= 2 levels on plosive onset
        jump = abs(target_level - current_level)
        if target_level != current_level:
            if jump >= 2:
                # Plosive onset - fast jump allowed
                current_level = target_level
                last_change_frame = f
            elif (f - last_change_frame) >= 2:
                # Normal 2-frame hysteresis
                current_level = target_level
                last_change_frame = f

        # Blinking: eyelids blink automatically every 90 frames (frame % 90 < 4)
        blink = bool((f % 90) < 4)

        mouth_data.append({
            "f": f,
            "mouth": state_names[current_level],
            "blink": blink
        })

    with open(output_mouth_path, "w") as out_f:
        json.dump(mouth_data, out_f, indent=2)

    # Clean up wav temp
    if os.path.exists(wav_path):
        os.remove(wav_path)

    print(f"[✓] Lip-sync generated: {output_mouth_path} ({len(mouth_data)} frames @ {fps}fps)")
    return mouth_data

if __name__ == "__main__":
    if os.path.exists("assets/voice.mp3"):
        generate_lipsync_data()
    else:
        print("Usage: python -m pipeline.lipsync_engine")
