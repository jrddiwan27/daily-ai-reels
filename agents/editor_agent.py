import os
import json
import subprocess
import time
from pipeline.audio_enhancer import produce_master_audio

def run_editor_agent(
    raw_video_path="out/raw_video.mp4",
    voice_path="assets/voice.mp3",
    output_final_path="out/daily-reel.mp4",
    duration=None,
    slot_id=1
):
    """
    EDITOR AGENT:
    Renders kinetic HyperFrames composition to MP4,
    masters broadcast audio with looping music & dynamic SFX,
    and multiplexes final broadcast 1080x1920 video with rotating creator face CTA.
    """
    print("=" * 65)
    print("🎬 [AGENT 5: EDITOR AGENT] Commencing Broadcast Assembly & SFX Synchronization...")
    print("=" * 65)
    start_time = time.time()
    os.makedirs("out", exist_ok=True)
    os.makedirs(os.path.dirname(output_final_path) or ".", exist_ok=True)

    # 1. Determine duration
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

    print(f"[✓] Target duration locked: {duration:.2f}s")

    # 2. Render HyperFrames HTML composition
    print("[1/3] Rendering kinetic Neo-Brutalist HTML composition with HyperFrames...")
    render_cmd = f"echo '' | npx --yes hyperframes render -o '{raw_video_path}'"
    res = subprocess.run(render_cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[!] HyperFrames render warning:\n{res.stderr}")
        if not os.path.exists(raw_video_path):
            raise RuntimeError(f"HyperFrames render failed: {res.stderr}")

    if not os.path.exists(raw_video_path):
        raise FileNotFoundError(f"Render output missing: {raw_video_path}")
    print(f"[✓] Raw kinetic video rendered successfully: {raw_video_path}")

    # 3. Master broadcast audio with ducked looping beat and frame-accurate SFX
    print("[2/3] Mastering broadcast audio with looping beat and frame-accurate SFX...")
    master_audio_path = "assets/master_audio.mp3"
    produce_master_audio(
        voice_path=voice_path,
        output_audio=master_audio_path,
        duration=duration
    )
    print(f"[✓] Audio mastered: {master_audio_path}")

    # 4. Multiplex video and audio into intermediate main reel
    temp_main = f"out/temp_main_reel_{slot_id}.mp4"
    print("[3/4] Muxing video and studio master audio into main reel...")
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
    subprocess.check_call(mux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 5. Concatenate with Creator Face CTA Outro
    cta_idx = ((slot_id - 1) % 7) + 1
    norm_cta_path = f"assets/cta/norm_cta_{cta_idx}.mp4"
    print(f"[4/4] Stitching creator face CTA outro (Rotation #{cta_idx}: {norm_cta_path})...")

    if os.path.exists(norm_cta_path):
        concat_cmd = [
            "ffmpeg", "-y",
            "-i", temp_main,
            "-i", norm_cta_path,
            "-filter_complex", "[0:v:0][0:a:0][1:v:0][1:a:0]concat=n=2:v=1:a=1[v][a]",
            "-map", "[v]",
            "-map", "[a]",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "44100",
            "-ac", "2",
            output_final_path
        ]
        subprocess.check_call(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(temp_main):
            try:
                os.remove(temp_main)
            except Exception:
                pass
        print(f"[✓] Assembled master reel with creator face CTA: {output_final_path}")
    else:
        print(f"[!] Warning: {norm_cta_path} not found. Keeping main animated reel.")
        if os.path.exists(temp_main):
            os.replace(temp_main, output_final_path)

    elapsed = time.time() - start_time

    # Collect final probe metrics
    probe_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration,r_frame_rate -of json "{output_final_path}"'
    probe_json = json.loads(subprocess.check_output(probe_cmd, shell=True).decode())
    stream_info = probe_json.get("streams", [{}])[0]

    manifest = {
        "status": "COMPLETED",
        "video_path": output_final_path,
        "width": stream_info.get("width"),
        "height": stream_info.get("height"),
        "duration": float(stream_info.get("duration", duration)),
        "fps": stream_info.get("r_frame_rate"),
        "master_audio": master_audio_path,
        "cta_appended": os.path.exists(norm_cta_path),
        "cta_file": norm_cta_path if os.path.exists(norm_cta_path) else None,
        "render_elapsed_seconds": round(elapsed, 2)
    }

    with open("assets/editor_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    return manifest

if __name__ == "__main__":
    run_editor_agent()

