import os
import subprocess

def produce_master_audio(
    voice_path="assets/voice.mp3",
    output_audio="assets/master_audio.mp3",
    duration=28.76,
    scene_transitions=None
):
    """
    Mixes voiceover with ducked background beat (at -18dB) + pristine studio sound effects (whoosh, pop, ding, click).
    """
    whoosh_path = "assets/sfx/sfx_whoosh.mp3"
    pop_path = "assets/sfx/sfx_pop.mp3"
    ding_path = "assets/sfx/sfx_ding.mp3"
    click_path = "assets/sfx/sfx_click.mp3"
    bgm_path = "assets/bg_music.wav"

    # Default cues timed to scene changes
    if scene_transitions is None:
        t_hook_end = min(3.8, duration * 0.13)
        t_tool1_end = duration * 0.40
        t_tool2_end = duration * 0.68
        t_tool3_end = duration * 0.88
        scene_transitions = [
            ("whoosh", 0.0),
            ("pop", 0.5),
            ("whoosh", t_hook_end),
            ("pop", t_hook_end + 0.35),
            ("ding", t_hook_end + 0.85),
            ("click", t_hook_end + 1.4),
            ("whoosh", t_tool1_end),
            ("pop", t_tool1_end + 0.35),
            ("ding", t_tool1_end + 0.85),
            ("click", t_tool1_end + 1.4),
            ("whoosh", t_tool2_end),
            ("pop", t_tool2_end + 0.35),
            ("ding", t_tool2_end + 0.85),
            ("click", t_tool2_end + 1.4),
            ("whoosh", t_tool3_end),
            ("pop", t_tool3_end + 0.25),
            ("ding", t_tool3_end + 0.7),
            ("click", t_tool3_end + 1.2)
        ]

    # Build filter complex for ffmpeg
    inputs = [
        "-i", voice_path,     # 0: voice
        "-i", whoosh_path,    # 1: whoosh
        "-i", pop_path,       # 2: pop
        "-i", ding_path,      # 3: ding
        "-i", click_path      # 4: click
    ]

    filter_chains = [
        "[0:a]volume=1.30[voice]"
    ]
    mix_labels = ["[voice]"]

    # Background music ducked underneath voice
    if os.path.exists(bgm_path):
        inputs.extend(["-i", bgm_path]) # 5: bgm
        filter_chains.append("[5:a]volume=0.15[bgm]")
        mix_labels.append("[bgm]")

    idx = 0
    for sfx_type, t_sec in scene_transitions:
        delay_ms = int(t_sec * 1000)
        if sfx_type == "whoosh":
            filter_chains.append(f"[1:a]adelay={delay_ms}|{delay_ms},volume=0.55[sfx{idx}]")
        elif sfx_type == "pop":
            filter_chains.append(f"[2:a]adelay={delay_ms}|{delay_ms},volume=0.60[sfx{idx}]")
        elif sfx_type == "ding":
            filter_chains.append(f"[3:a]adelay={delay_ms}|{delay_ms},volume=0.50[sfx{idx}]")
        elif sfx_type == "click":
            filter_chains.append(f"[4:a]adelay={delay_ms}|{delay_ms},volume=0.60[sfx{idx}]")
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
        "-t", str(round(duration + 0.2, 2)),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        output_audio
    ]

    subprocess.check_call(cmd)
    print(f"[✓] Broadcast master audio produced with ducked beat & studio SFX: {output_audio}")
    return output_audio

if __name__ == "__main__":
    produce_master_audio()
