"""
Editor Agent:
Responsible for frame-accurate rendering, studio audio mastering, SFX synchronization,
and creator outro stitching.
"""

import os
import glob
import json
import random
import subprocess
import time
from pipeline.audio_enhancer import produce_master_audio

def run_editor_agent(
    raw_video_path="out/raw_video.mp4",
    voice_path="assets/voice.mp3",
    output_final_path="out/daily-reel.mp4",
    cta_dir="assets/cta",
    duration=None
):
    print("================================================================================")
    print("🎬 [EDITOR AGENT] Commencing Broadcast Assembly & SFX Synchronization...")
    print("================================================================================")
    start_time = time.time()
    os.makedirs("out", exist_ok=True)
    os.makedirs("assets/cta_normalized", exist_ok=True)

    # 1. Determine duration from voiceover or hyperframes.json
    if duration is None:
        if os.path.exists("hyperframes.json"):
            try:
                with open("hyperframes.json") as f:
                    hf_data = json.load(f)
                    duration = float(hf_data.get("duration", 30.0))
            except Exception:
                duration = 30.0
        elif os.path.exists(voice_path):
            probe_cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{voice_path}"'
            try:
                duration = float(subprocess.check_output(probe_cmd, shell=True).decode().strip())
            except Exception:
                duration = 30.0
        else:
            duration = 30.0

    print(f"[✓] Target visual duration locked: {duration:.2f} seconds")

    # 2. Render HyperFrames HTML composition to MP4
    print("[1/4] Rendering kinetic Neo-Brutalist HTML composition with HyperFrames...")
    render_cmd = f"echo '' | npx --yes hyperframes render -o {raw_video_path}"
    res = subprocess.run(render_cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[!] HyperFrames render warning/error:\n{res.stderr}")
        if not os.path.exists(raw_video_path):
            raise RuntimeError(f"HyperFrames render failed: {res.stderr}")

    if not os.path.exists(raw_video_path):
        raise FileNotFoundError(f"Render output missing: {raw_video_path}")
    print(f"[✓] Raw video rendered successfully: {raw_video_path}")

    # 3. Master broadcast audio with ducked music and frame-accurate SFX
    print("[2/4] Mixing broadcast audio with dynamic sound design (sub-bass boom, swooshes, pops, dings)...")
    master_audio_path = "assets/master_audio.mp3"
    produce_master_audio(
        voice_path=voice_path,
        output_audio=master_audio_path,
        duration=duration
    )
    print(f"[✓] Audio mastered and enhanced: {master_audio_path}")

    # 4. Multiplex video and audio
    print("[3/4] Muxing video and studio master audio...")
    temp_main = "out/temp_main.mp4"
    mux_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video_path,
        "-i", master_audio_path,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        "-shortest",
        temp_main
    ]
    subprocess.check_call(mux_cmd)
    print(f"[✓] Multiplexed core reel: {temp_main}")

    # 5. Seamlessly append rotating creator CTA
    print("[4/4] Normalizing and appending creator face CTA outro...")
    cta_files = sorted(glob.glob(os.path.join(cta_dir, "*.mp4")))
    if cta_files:
        chosen_cta = random.choice(cta_files)
        normalized_cta = os.path.join("assets/cta_normalized", os.path.basename(chosen_cta))
        
        # Normalize CTA to 1080x1920 @ 30fps and 44100Hz stereo AAC
        norm_cmd = [
            "ffmpeg", "-y",
            "-i", chosen_cta,
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-ar", "44100",
            "-ac", "2",
            "-b:a", "192k",
            normalized_cta
        ]
        subprocess.check_call(norm_cmd)

        concat_list = "out/concat_list.txt"
        with open(concat_list, "w") as f:
            f.write(f"file '{os.path.abspath(temp_main)}'\n")
            f.write(f"file '{os.path.abspath(normalized_cta)}'\n")

        concat_cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_list,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "44100",
            "-ac", "2",
            output_final_path
        ]
        subprocess.check_call(concat_cmd)
        print(f"[✓] Creator outro appended smoothly: {output_final_path}")
    else:
        print("[!] No creator CTA found in assets/cta, keeping temp_main as final output.")
        import shutil
        shutil.copyfile(temp_main, output_final_path)

    elapsed = time.time() - start_time

    # Collect final probe metrics
    probe_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration,r_frame_rate -of json "{output_final_path}"'
    probe_json = json.loads(subprocess.check_output(probe_cmd, shell=True).decode())
    stream_info = probe_json.get("streams", [{}])[0]

    manifest = {
        "status": "COMPLETED",
        "final_video_path": output_final_path,
        "width": int(stream_info.get("width", 1080)),
        "height": int(stream_info.get("height", 1920)),
        "duration": float(stream_info.get("duration", duration)),
        "render_time_seconds": round(elapsed, 2)
    }

    with open("assets/editor_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"🎬 [EDITOR AGENT] Finished assembly in {elapsed:.1f}s -> {output_final_path}")
    return manifest

if __name__ == "__main__":
    run_editor_agent()
