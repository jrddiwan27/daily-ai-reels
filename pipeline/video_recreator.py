import os
import sys
import json
import base64
import subprocess
import requests
from pipeline.ai_scriptwriter import get_gemini_key, sanitize_voice_script

def download_video_from_url(url: str, output_dir: str = "inbox/videos") -> str:
    """
    Downloads a video from any social platform (YouTube Shorts, X, Instagram, TikTok)
    using yt-dlp into the inbox/videos directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    out_template = os.path.join(output_dir, "%(title).30s_%(id)s.%(ext)s")
    print(f"[*] Downloading reference video from URL: {url}...")
    cmd = f'yt-dlp -f "mp4/best" --no-playlist -o "{out_template}" "{url}"'
    subprocess.check_call(cmd, shell=True)

    # Find the newest downloaded video in output_dir
    files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith((".mp4", ".mov", ".mkv", ".webm"))]
    if not files:
        raise FileNotFoundError(f"Failed to locate downloaded video for {url}")
    newest = max(files, key=os.path.getctime)
    print(f"[✓] Successfully downloaded reference video to: {newest}")
    return newest

def analyze_reference_video(video_path: str, output_dir: str = "inbox/analysis") -> dict:
    """
    Deconstructs a reference video frame-by-frame and audio using Gemini:
    - Extracts keyframes at scene transitions
    - Analyzes visual hierarchy, motion graphics, and typography
    - Extracts the psychological retention blueprint
    """
    os.makedirs(output_dir, exist_ok=True)
    frames_dir = os.path.join(output_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    print(f"[*] Extracting keyframes from: {video_path}...")
    # Extract 8 evenly spaced frames across the video duration
    cmd = f'ffmpeg -y -i "{video_path}" -vf "fps=1/4,scale=360:640" -q:v 3 "{frames_dir}/frame_%02d.jpg"'
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    extracted = sorted([os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.endswith(".jpg")])
    if not extracted:
        raise ValueError(f"No frames could be extracted from {video_path}")

    print(f"[✓] Extracted {len(extracted)} keyframes. Sending to Gemini for visual deconstruction...")

    api_key = get_gemini_key()
    if not api_key:
        raise ValueError("GEMINI_API_KEY is required for video reverse-engineering.")

    parts = []
    # Send up to 6 keyframes
    for fpath in extracted[:6]:
        with open(fpath, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        parts.append({
            "inlineData": {
                "mimeType": "image/jpeg",
                "data": b64
            }
        })

    prompt = """
You are an elite motion designer and viral reel strategist. Analyze these sequential keyframes from a top-tier viral tech reel.
Deconstruct this video into a structured JSON blueprint:
{
  "layout_style": "string (e.g. 60/40 split with top motion graphics and bottom presenter)",
  "hook_technique": "string (how the first 3 seconds grab curiosity)",
  "visual_elements": [
    "element 1 description",
    "element 2 description",
    "element 3 description"
  ],
  "caption_style": "string (font, size, bounding box style, highlight colors)",
  "color_palette": {
    "background": "hex code",
    "accent": "hex code",
    "card_dark": "hex code"
  },
  "narrative_structure": [
    {"timestamp": "0-3s", "stage": "Hook", "role": "Pattern interrupt"},
    {"timestamp": "3-15s", "stage": "Mechanism", "role": "Introduce the technology"},
    {"timestamp": "15-25s", "stage": "Proof/Feature", "role": "Visual proof & benchmark"},
    {"timestamp": "25-33s", "stage": "CTA", "role": "Keyword trigger"}
  ],
  "core_retention_takeaway": "string explaining why this video retains viewers"
}
Output valid JSON only.
"""
    parts.append({"text": prompt})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
    res = requests.post(
        url,
        json={
            "contents": [{"parts": parts}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.3}
        },
        timeout=60
    )

    if res.status_code != 200:
        raise RuntimeError(f"Gemini API error ({res.status_code}): {res.text[:200]}")

    raw_json = res.json()["candidates"][0]["content"]["parts"][0]["text"]
    blueprint = json.loads(raw_json)

    blueprint_path = os.path.join(output_dir, "blueprint.json")
    with open(blueprint_path, "w") as f:
        json.dump(blueprint, f, indent=2)

    print(f"[✓] Reverse-engineering blueprint saved to {blueprint_path}")
    return blueprint

def recreate_video_with_topic(
    reference_video_path: str,
    target_topic: str,
    target_items: list = None,
    output_dir: str = "inbox/recreated"
) -> dict:
    """
    Analyzes the reference video and generates an original, high-converting video
    in the exact same viral visual and narrative style, applied to the target topic.
    """
    blueprint = analyze_reference_video(reference_video_path)

    api_key = get_gemini_key()
    prompt = f"""
Using the exact viral blueprint below, write a high-retention 30-35s Instagram Reel script on this new topic:
TOPIC: {target_topic}
FEATURED ITEMS: {json.dumps(target_items or [])}

VIRAL BLUEPRINT TO EMULATE:
{json.dumps(blueprint, indent=2)}

RULES:
1. Pacing: 75 to 90 words total (Fireship / high-energy punchy style).
2. Follow the blueprint's narrative structure exactly.
3. End with a 1-word CTA keyword.
4. Output valid JSON with keys: 'hook', 'body_1', 'body_2', 'cta_keyword', 'full_script', 'motion_scenes'
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
    res = requests.post(
        url,
        json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.7}
        },
        timeout=40
    )

    if res.status_code != 200:
        raise RuntimeError(f"Gemini API error: {res.text[:200]}")

    script_data = json.loads(res.json()["candidates"][0]["content"]["parts"][0]["text"])
    script_data["full_script"] = sanitize_voice_script(script_data["full_script"])

    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, "recreated_script.json")
    with open(out_file, "w") as f:
        json.dump(script_data, f, indent=2)

    print(f"[✓] Generated matching script for '{target_topic}':")
    print(f"\"{script_data['full_script']}\"")
    return script_data

def process_inbox():
    """
    Scans inbox/videos for uploaded video files and inbox/urls.txt for shared links.
    Deconstructs and recreates them into high-converting studio productions.
    """
    os.makedirs("inbox/videos", exist_ok=True)
    url_file = "inbox/urls.txt"
    if os.path.exists(url_file):
        with open(url_file, "r") as uf:
            urls = [line.strip() for line in uf.readlines() if line.strip() and not line.startswith("#")]
        if urls:
            print(f"[*] Found {len(urls)} URLs in {url_file}. Processing first URL...")
            target_url = urls[0]
            downloaded_video = download_video_from_url(target_url)
            recreate_video_with_topic(downloaded_video, "Qwen Open-Source Vision & Image Model (Qwen-Image)")
            # Remove processed URL from file
            with open(url_file, "w") as uf:
                uf.write("\n".join(urls[1:]) + "\n")
            return

    # Check for direct video files
    video_files = [os.path.join("inbox/videos", f) for f in os.listdir("inbox/videos") if f.endswith((".mp4", ".mov", ".mkv", ".webm"))]
    if video_files:
        print(f"[*] Found video in inbox/videos: {video_files[0]}")
        recreate_video_with_topic(video_files[0], "Qwen Open-Source Vision & Image Model (Qwen-Image)")
    else:
        print("[*] Inbox is currently empty. Drop videos into inbox/videos/ or add links to inbox/urls.txt")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.startswith("http://") or arg.startswith("https://"):
            vid = download_video_from_url(arg)
            topic = sys.argv[2] if len(sys.argv) > 2 else "Qwen Open-Source Image Model (Qwen-Image)"
            recreate_video_with_topic(vid, topic)
        elif os.path.exists(arg):
            topic = sys.argv[2] if len(sys.argv) > 2 else "Qwen Open-Source Image Model (Qwen-Image)"
            recreate_video_with_topic(arg, topic)
        elif arg == "--inbox":
            process_inbox()
    else:
        process_inbox()
