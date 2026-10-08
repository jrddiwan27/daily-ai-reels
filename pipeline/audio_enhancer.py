import os
import wave
import math
import struct
import random
import subprocess

def ensure_sfx_assets(assets_dir="assets"):
    """
    Synthesizes crisp, professional procedural sound effects and background beat.
    """
    os.makedirs(assets_dir, exist_ok=True)
    sample_rate = 44100

    whoosh_path = os.path.join(assets_dir, "sfx_whoosh.wav")
    pop_path = os.path.join(assets_dir, "sfx_pop.wav")
    impact_path = os.path.join(assets_dir, "sfx_impact.wav")
    bg_music_path = os.path.join(assets_dir, "bg_music.wav")

    # 1. Whoosh / Swoosh (air rush sweep with pitch bend)
    if not os.path.exists(whoosh_path):
        with wave.open(whoosh_path, "w") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(sample_rate)
            n = int(sample_rate * 0.30)
            for i in range(n):
                t = i / n
                env = (math.sin(t * math.pi) ** 2) * (1.0 - 0.2 * t)
                freq = 240 + 1400 * math.sin(t * math.pi)
                noise = random.uniform(-0.7, 0.7) * 0.5
                tone = math.sin(2 * math.pi * freq * (i / sample_rate)) * 0.5
                val = (noise + tone) * env
                f.writeframes(struct.pack('<h', int(val * 28000)))

    # 2. Pop / Click (punchy UI pop with exponential decay)
    if not os.path.exists(pop_path):
        with wave.open(pop_path, "w") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(sample_rate)
            n = int(sample_rate * 0.09)
            for i in range(n):
                t = i / n
                env = math.exp(-t * 22)
                freq = 900 - 450 * t
                val = math.sin(2 * math.pi * freq * (i / sample_rate)) * env
                f.writeframes(struct.pack('<h', int(val * 27000)))

    # 3. Sub Impact / Boom (808 sub-bass drop)
    if not os.path.exists(impact_path):
        with wave.open(impact_path, "w") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(sample_rate)
            n = int(sample_rate * 0.48)
            for i in range(n):
                t = i / n
                env = math.exp(-t * 5.5)
                freq = 150 * math.exp(-t * 7.5) + 42
                val = math.sin(2 * math.pi * freq * (i / sample_rate)) * env
                f.writeframes(struct.pack('<h', int(val * 30000)))

    # 4. Upbeat Cyber Synthwave Beat (126 BPM)
    if not os.path.exists(bg_music_path):
        duration = 32.0
        bpm = 126
        beat_dur = 60.0 / bpm
        total_samples = int(duration * sample_rate)

        kick_samples = int(0.22 * sample_rate)
        kick = []
        for i in range(kick_samples):
            t = i / sample_rate
            f_k = 135 * math.exp(-t * 24) + 42
            env_k = math.exp(-t * 11)
            kick.append(math.sin(2 * math.pi * f_k * t) * env_k)

        snare_samples = int(0.19 * sample_rate)
        snare = []
        for i in range(snare_samples):
            t = i / sample_rate
            env_s = math.exp(-t * 13)
            noise_s = random.uniform(-1, 1) * 0.75 + math.sin(2 * math.pi * 220 * t) * 0.25
            snare.append(noise_s * env_s)

        hihat_samples = int(0.06 * sample_rate)
        hihat = []
        for i in range(hihat_samples):
            t = i / sample_rate
            env_h = math.exp(-t * 40)
            hihat.append(random.uniform(-1, 1) * env_h)

        buffer = [0.0] * total_samples
        bass_notes = [55.0, 55.0, 65.4, 73.4, 55.0, 55.0, 82.4, 73.4]

        beat_idx = 0
        cur_t = 0.0
        while cur_t < duration:
            cur_sample = int(cur_t * sample_rate)
            beat_in_bar = beat_idx % 4

            for s in range(len(kick)):
                if cur_sample + s < total_samples:
                    buffer[cur_sample + s] += kick[s] * 0.75

            if beat_in_bar in (1, 3):
                for s in range(len(snare)):
                    if cur_sample + s < total_samples:
                        buffer[cur_sample + s] += snare[s] * 0.45

            for s in range(len(hihat)):
                if cur_sample + s < total_samples:
                    buffer[cur_sample + s] += hihat[s] * 0.20
            off_beat_sample = cur_sample + int(beat_dur * 0.5 * sample_rate)
            for s in range(len(hihat)):
                if off_beat_sample + s < total_samples:
                    buffer[off_beat_sample + s] += hihat[s] * 0.25

            note_freq = bass_notes[(beat_idx // 2) % len(bass_notes)]
            bass_len = int(beat_dur * 0.45 * sample_rate)
            for s in range(bass_len):
                if cur_sample + s < total_samples:
                    t_b = s / sample_rate
                    env_b = math.exp(-t_b * 5.8)
                    wave_val = (
                        math.sin(2 * math.pi * note_freq * t_b) +
                        0.45 * math.sin(4 * math.pi * note_freq * t_b) +
                        0.25 * math.sin(6 * math.pi * note_freq * t_b)
                    ) * 0.35 * env_b
                    buffer[cur_sample + s] += wave_val

            beat_idx += 1
            cur_t += beat_dur

        max_val = max(max(abs(x) for x in buffer), 0.001)
        scale = 22000.0 / max_val
        with wave.open(bg_music_path, "w") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(sample_rate)
            frames = bytearray()
            for x in buffer:
                val = max(min(int(x * scale), 32767), -32768)
                frames.extend(struct.pack('<h', val))
            f.writeframes(frames)

    return whoosh_path, pop_path, impact_path, bg_music_path

def produce_master_audio(
    voice_path="assets/voice.mp3",
    output_audio="assets/master_audio.mp3",
    duration=28.76,
    scene_transitions=None
):
    """
    Mixes voiceover, rhythmic cyber beat, and precision sound effects into a broadcast master track.
    """
    whoosh_path, pop_path, impact_path, bg_path = ensure_sfx_assets()

    if scene_transitions is None:
        t_hook_end = min(3.8, duration * 0.12)
        t_tool1_end = duration * 0.40
        t_tool2_end = duration * 0.68
        t_tool3_end = duration * 0.88
        scene_transitions = [
            ("impact", 0.0),
            ("whoosh", t_hook_end),
            ("pop", t_hook_end + 0.45),
            ("whoosh", t_tool1_end),
            ("pop", t_tool1_end + 0.45),
            ("whoosh", t_tool2_end),
            ("pop", t_tool2_end + 0.45),
            ("impact", t_tool3_end),
            ("whoosh", t_tool3_end + 0.20),
            ("pop", t_tool3_end + 0.60)
        ]

    # Build filter complex for ffmpeg
    inputs = [
        "-i", voice_path,     # 0: voice
        "-i", bg_path,        # 1: background music
        "-i", impact_path,    # 2: impact
        "-i", whoosh_path,    # 3: whoosh
        "-i", pop_path        # 4: pop
    ]

    filter_chains = [
        "[1:a]volume=0.15[bg]",
        "[0:a]volume=1.20[voice]"
    ]
    mix_labels = ["[voice]", "[bg]"]

    idx = 0
    for sfx_type, t_sec in scene_transitions:
        delay_ms = int(t_sec * 1000)
        if sfx_type == "impact":
            filter_chains.append(f"[2:a]adelay={delay_ms}|{delay_ms},volume=0.65[sfx{idx}]")
        elif sfx_type == "whoosh":
            filter_chains.append(f"[3:a]adelay={delay_ms}|{delay_ms},volume=0.55[sfx{idx}]")
        elif sfx_type == "pop":
            filter_chains.append(f"[4:a]adelay={delay_ms}|{delay_ms},volume=0.65[sfx{idx}]")
        mix_labels.append(f"[sfx{idx}]")
        idx += 1

    total_inputs = len(mix_labels)
    filter_chains.append(f"{''.join(mix_labels)}amix=inputs={total_inputs}:normalize=0:dropout_transition=2[outa]")
    filter_complex = ";".join(filter_chains)

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[outa]",
        "-t", str(round(duration + 0.5, 2)),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        output_audio
    ]

    subprocess.check_call(cmd)
    print(f"[✓] Master audio mixed with SFX & cyber beat: {output_audio}")
    return output_audio

if __name__ == "__main__":
    produce_master_audio()
