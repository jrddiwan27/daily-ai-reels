import os
import subprocess

def produce_master_audio(
    voice_path="assets/voice.mp3",
    output_audio="assets/master_audio.mp3",
    duration=28.76,
    scene_transitions=None
):
    """
    Mixes voiceover with ducked background beat (at -18dB) + punchy studio sound effects
    (sub-bass boom, crisp whoosh, pop, ding, click).
    """
    whoosh_path = "assets/sfx/sfx_whoosh.mp3"
    pop_path = "assets/sfx/sfx_pop.mp3"
    ding_path = "assets/sfx/sfx_ding.mp3"
    click_path = "assets/sfx/sfx_click.mp3"
    boom_path = "assets/sfx/sfx_bass_boom.wav"
    bgm_path = "assets/bg_music.wav"

    # Default cues timed to scene changes & kinetic events
    if scene_transitions is None:
        t_hook_end = min(4.2, duration * 0.14)
        t_trans_end = min(8.5, duration * 0.28)
        t_tool1_end = duration * 0.52
        t_tool2_end = duration * 0.74
        t_tool3_end = duration * 0.88
        scene_transitions = [
            ("boom", 0.0),
            ("whoosh", 0.05),
            ("pop", 0.45),
            ("ding", 1.25),
            ("whoosh", t_hook_end),
            ("pop", t_hook_end + 0.35),
            ("ding", t_hook_end + 0.85),
            ("whoosh", t_trans_end),
            ("click", t_trans_end + 0.35),
            ("click", t_trans_end + 0.70),
            ("pop", t_trans_end + 1.2),
            ("whoosh", t_tool1_end),
            ("ding", t_tool1_end + 0.4),
            ("pop", t_tool1_end + 1.0),
            ("whoosh", t_tool2_end),
            ("pop", t_tool2_end + 0.35),
            ("ding", t_tool2_end + 0.9),
            ("whoosh", t_tool3_end),
            ("boom", t_tool3_end + 0.1),
            ("pop", t_tool3_end + 0.35),
            ("pop", t_tool3_end + 0.65),
            ("pop", t_tool3_end + 0.95),
            ("ding", t_tool3_end + 1.3)
        ]

    # Build filter complex for ffmpeg
    inputs = [
        "-i", voice_path,     # 0: voice
        "-i", whoosh_path,    # 1: whoosh
        "-i", pop_path,       # 2: pop
        "-i", ding_path,      # 3: ding
        "-i", click_path,     # 4: click
        "-i", boom_path       # 5: boom
    ]

    filter_chains = [
        "[0:a]volume=1.25[voice]"
    ]
    mix_labels = ["[voice]"]

    # Background music ducked underneath voice
    if os.path.exists(bgm_path):
        inputs.extend(["-i", bgm_path]) # 6: bgm
        filter_chains.append("[6:a]volume=0.12[bgm]")
        mix_labels.append("[bgm]")

    idx = 0
    for sfx_type, t_sec in scene_transitions:
        delay_ms = int(t_sec * 1000)
        if sfx_type == "whoosh":
            filter_chains.append(f"[1:a]adelay={delay_ms}|{delay_ms},volume=0.95[sfx{idx}]")
        elif sfx_type == "pop":
            filter_chains.append(f"[2:a]adelay={delay_ms}|{delay_ms},volume=1.05[sfx{idx}]")
        elif sfx_type == "ding":
            filter_chains.append(f"[3:a]adelay={delay_ms}|{delay_ms},volume=0.85[sfx{idx}]")
        elif sfx_type == "click":
            filter_chains.append(f"[4:a]adelay={delay_ms}|{delay_ms},volume=0.95[sfx{idx}]")
        elif sfx_type == "boom":
            filter_chains.append(f"[5:a]adelay={delay_ms}|{delay_ms},volume=1.20[sfx{idx}]")
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
        "-ar", "44100",
        "-ac", "2",
        output_audio
    ]

    subprocess.check_call(cmd)
    print(f"[✓] Broadcast master audio produced with ducked beat & punchy SFX: {output_audio}")
    return output_audio

if __name__ == "__main__":
    produce_master_audio()
