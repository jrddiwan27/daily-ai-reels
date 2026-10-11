import os
import sys
import json
import time
import datetime
from pipeline.buffer_dispatcher import (
    upload_video_to_github_release,
    dispatch_post_payload,
    CHANNELS
)

def main():
    video_path = "out/daily-reel.mp4"
    if not os.path.exists(video_path):
        print(f"[!] Error: {video_path} not found.")
        sys.exit(1)

    print(f"[*] Step 1: Uploading {video_path} to GitHub Releases CDN...")
    cdn_url = upload_video_to_github_release(video_path)
    print(f"[✓] CDN URL: {cdn_url}")

    # Instagram Caption
    ig_caption = (
        "Comment “QWEN” and I’ll DM you the direct download link + local setup guide 📩\n\n"
        "Midjourney costs $30/month.\n"
        "Qwen just open-sourced Image 2.1 — and it is 100% free.\n\n"
        "Why this changes everything:\n"
        "• 20 Billion parameters beating Flux & Midjourney\n"
        "• Photorealistic textures & anatomically accurate hands\n"
        "• Flawless in-image typography and signage\n"
        "• 100% offline local inference on Apple Silicon Mac & PC GPUs\n\n"
        "💾 Save this for your local AI stack\n"
        "➡️ Follow @jayant.digitalstudio for daily breakthrough open-source AI tools\n\n"
        "#qwen #midjourney #opensource #aiart #machinelearning #generativeai #localllm"
    )
    ig_meta = {"instagram": {"type": "reel", "shouldShareToFeed": True}}

    # YouTube Caption
    yt_title = "Midjourney is Dead? Qwen Just Open Sourced Image 2.1! 🚀 #Shorts"
    yt_description = (
        "Qwen just open-sourced Image 2.1 with 20B parameters, beating Midjourney and Flux — completely free and offline!\n\n"
        "Features:\n"
        "1. 20B parameter vision transformer architecture\n"
        "2. Photorealistic anatomy & perfect text rendering\n"
        "3. 100% local inference on Mac & RTX GPUs\n\n"
        "👉 Setup guides & code: https://jrddiwan27.github.io/daily-ai-reels/\n\n"
        "#Shorts #AI #Qwen #OpenSource #GenerativeAI #MachineLearning"
    )
    yt_meta = {
        "youtube": {
            "title": yt_title,
            "privacy": "public",
            "categoryId": "28",
            "madeForKids": False
        }
    }

    # Twitter Caption
    tw_text = (
        "⚡ Qwen just open-sourced Image 2.1!\n\n"
        "• 20B parameters beating Midjourney & Flux\n"
        "• Photorealistic textures & perfect text\n"
        "• 100% offline on Mac & PC (Zero cloud queues)\n\n"
        "Drop a comment below to get the download links & setup guide! 👇\n\n"
        "#AI #Tech #OpenSource"
    )

    print("\n[*] Step 2: Dispatching to Connected Buffer Channels...")
    results = {}

    print(f"[*] Posting to Instagram (@jayant.digitalstudio)...")
    ig_id = dispatch_post_payload(CHANNELS["instagram"], ig_caption, cdn_url, ig_meta)
    results["instagram"] = ig_id
    print(f"[✓ INSTAGRAM] Scheduled: Post ID {ig_id}")

    print(f"[*] Posting to YouTube (Jayant Digital Studio)...")
    yt_id = dispatch_post_payload(CHANNELS["youtube"], yt_description, cdn_url, yt_meta)
    results["youtube"] = yt_id
    print(f"[✓ YOUTUBE] Scheduled: Post ID {yt_id}")

    print(f"[*] Posting to Twitter / X (@jayantdiwanAI)...")
    tw_id = dispatch_post_payload(CHANNELS["twitter"], tw_text, cdn_url)
    results["twitter"] = tw_id
    print(f"[✓ X/TWITTER] Scheduled: Post ID {tw_id}")

    # Step 3: Record to published history
    history_file = "history/published_history.json"
    history = []
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                history = json.load(f)
        except Exception:
            history = []

    now_utc = datetime.datetime.now(datetime.timezone.utc)
    ist = now_utc + datetime.timedelta(hours=5, minutes=30)

    entry = {
        "title": "Qwen Image 2.1 Open-Source Breakdown",
        "timestamp_utc": now_utc.isoformat(),
        "date_ist": ist.strftime("%Y-%m-%d %H:%M:%S IST"),
        "buffer_post_id": results.get("instagram") or results.get("youtube") or "scheduled",
        "channel_results": results,
        "cdn_url": cdn_url,
        "items": [
            {
                "id": "Qwen/Qwen-Image-2.1",
                "name": "Qwen-Image-2.1",
                "url": "https://huggingface.co/Qwen/Qwen-Image-2.1",
                "title": "20B Parameter Open-Source Photorealistic Text-to-Image Foundation Model"
            }
        ]
    }
    history.append(entry)
    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)

    # Step 4: Update docs/posts_data.json for github pages showcase
    docs_posts = "docs/posts_data.json"
    os.makedirs("docs", exist_ok=True)
    posts = []
    if os.path.exists(docs_posts):
        try:
            with open(docs_posts, "r") as f:
                posts = json.load(f)
        except Exception:
            posts = []

    posts.insert(0, {
        "title": "Qwen Image 2.1: The Free Midjourney Killer",
        "description": "20B parameter open-source image model running 100% offline on consumer hardware with photorealistic detail.",
        "date": ist.strftime("%b %d, %Y"),
        "cdn_url": cdn_url,
        "repo_url": "https://huggingface.co/Qwen/Qwen-Image-2.1",
        "tags": ["Qwen", "OpenSource", "Text2Image", "GGUF"]
    })
    with open(docs_posts, "w") as f:
        json.dump(posts[:20], f, indent=2)

    print("\n[✓ COMPLETE] Qwen Image 2.1 Reel successfully uploaded, dispatched, and recorded!")

if __name__ == "__main__":
    main()
