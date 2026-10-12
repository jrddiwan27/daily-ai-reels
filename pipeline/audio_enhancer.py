import os
import json
import subprocess

def produce_master_audio(
    voice_path="assets/voice.mp3",
    output_audio="assets/master_audio.mp3",
    duration=30.0,
    scene_transitions=None
):
    """
    Mixes studio voiceover with a looping, punchy background beat
    and frame-accurate sound effects (bass boom, crisp whoosh, pop, ding).
    """
    whoosh_path = "assets/sfx/sfx_whoosh.mp3"
    pop_path = "assets/sfx/sfx_pop.mp3"
    ding_path = "assets/sfx/sfx_ding.mp3"
    click_path = "assets/sfx/sfx_click.mp3"
    boom_path = "assets/sfx/sfx_bass_boom.wav"
    bgm_path = "assets/bg_music.wav"

    # Load frame-accurate cues if available from visual agent
    if scene_transitions is None:
        cues_file = "assets/sfx_cues.json"
        if os.path.exists(cues_file):
            try:
                with open(cues_file) as f:
                    raw_cues = json.load(f)
                    scene_transitions = [(c["type"], float(c["time"])) for c in raw_cues]
                    print(f"[✓] Loaded {len(scene_transitions)} frame-accurate SFX cues from {cues_file}")
            except Exception as e:
                print(f"[!] Warning reading {cues_file}: {e}")
                scene_transitions = None

    if scene_transitions is None:
        scene_transitions = [
            ("boom", 0.0),
            ("whoosh", 0.1),
            ("pop", 0.6),
            ("whoosh", 4.0),
            ("pop", 4.5),
            ("ding", 6.0),
            ("whoosh", 8.0),
            ("pop", 8.5),
            ("ding", 10.0),
            ("whoosh", 14.0),
            ("pop", 14.5),
            ("ding", 16.0),
            ("whoosh", 20.0),
            ("pop", 20.5),
            ("ding", 22.0),
            ("boom", 25.0),
            ("ding", 25.5),
            ("pop", 26.5)
        ]

    # Filter complex inputs
    inputs = [
        "-i", voice_path,     # 0: voice
        "-i", whoosh_path,    # 1: whoosh
        "-i", pop_path,       # 2: pop
        "-i", ding_path,      # 3: ding
        "-i", click_path,     # 4: click
        "-i", boom_path       # 5: boom
    ]

    filter_chains = [
        "[0:a]volume=1.35[voice]"
    ]
    mix_labels = ["[voice]"]

    # Background music with infinite loop flag so it NEVER cuts out
    if os.path.exists(bgm_path):
        inputs.extend(["-stream_loop", "-1", "-i", bgm_path]) # 6: looped bgm
        filter_chains.append("[6:a]volume=0.30[bgm]")
        mix_labels.append("[bgm]")

    idx = 0
    for sfx_type, t_sec in scene_transitions:
        delay_ms = max(0, int(t_sec * 1000))
        if sfx_type == "whoosh":
            filter_chains.append(f"[1:a]adelay={delay_ms}|{delay_ms},volume=0.90[sfx{idx}]")
        elif sfx_type == "pop":
            filter_chains.append(f"[2:a]adelay={delay_ms}|{delay_ms},volume=0.95[sfx{idx}]")
        elif sfx_type == "ding":
            filter_chains.append(f"[3:a]adelay={delay_ms}|{delay_ms},volume=0.85[sfx{idx}]")
        elif sfx_type == "click":
            filter_chains.append(f"[4:a]adelay={delay_ms}|{delay_ms},volume=0.90[sfx{idx}]")
        elif sfx_type == "boom":
            filter_chains.append(f"[5:a]adelay={delay_ms}|{delay_ms},volume=1.15[sfx{idx}]")
        mix_labels.append(f"[sfx{idx}]")
        idx += 1

    total_inputs = len(mix_labels)
    filter_chains.append(f"{''.join(mix_labels)}amix=inputs={total_inputs}:normalize=0:dropout_transition=0[outa]")
    filter_complex = ";".join(filter_chains)

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[outa]",
        "-t", str(round(duration + 0.1, 2)),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        output_audio
    ]

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[✓] Broadcast master audio produced with looping beat & punchy SFX: {output_audio}")
    return output_audio

if __name__ == "__main__":
    produce_master_audio()
