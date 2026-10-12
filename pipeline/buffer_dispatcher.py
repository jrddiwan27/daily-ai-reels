import os
import json
import time
import requests
import subprocess

BUFFER_ACCESS_TOKEN = os.environ.get("BUFFER_ACCESS_TOKEN") or "gCUwoZC7cOjHobBSz5a9S3a4nrBh1PF8mydBp6_Rku2"
DEFAULT_CHANNEL_ID = os.environ.get("BUFFER_CHANNEL_ID") or "6ac7f82a6a5c39ccb6564f06" # jayant.digitalstudio
GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY") or "jrddiwan27/daily-ai-reels"

# Connected Buffer Channels for Jayant Digital Studio
CHANNELS = {
    "instagram": os.environ.get("BUFFER_CHANNEL_IG") or "6ac7f82a6a5c39ccb6564f06", # @jayant.digitalstudio
    "youtube": os.environ.get("BUFFER_CHANNEL_YT") or "6ac970866a5c39ccb66919ad",   # Jayant Digital Studio
    "twitter": os.environ.get("BUFFER_CHANNEL_TW") or "6ac971a26a5c39ccb6691f97"    # @jayantdiwanAI
}

def get_github_token():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    try:
        res = subprocess.check_output(
            "printf 'protocol=https\\nhost=github.com\\n' | git credential fill",
            shell=True,
            text=True
        )
        for line in res.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return None

GITHUB_TOKEN = get_github_token()

def upload_video_to_github_release(file_path: str) -> str:
    """
    Creates a GitHub Release and uploads the rendered video asset.
    GitHub CDN provides 100% free, high-speed direct download URLs compatible with Buffer.
    """
    tag_name = f"reel-{int(time.time())}"
    release_title = f"Daily Reel - {tag_name}"
    
    # 1. Optimize video if file size > 10MB to guarantee fast upload and mobile streaming
    upload_target = file_path
    if os.path.exists(file_path) and os.path.getsize(file_path) > 10 * 1024 * 1024:
        opt_path = file_path.replace(".mp4", "_cdn_opt.mp4")
        print(f"[*] Compressing video for high-speed CDN distribution ({os.path.getsize(file_path)/1024/1024:.1f} MB -> opt)...")
        comp_cmd = f"ffmpeg -y -i '{file_path}' -c:v libx264 -preset faster -crf 24 -pix_fmt yuv420p -c:a copy '{opt_path}'"
        try:
            subprocess.check_call(comp_cmd, shell=True)
            if os.path.exists(opt_path):
                upload_target = opt_path
                print(f"[✓] Compressed to {os.path.getsize(upload_target)/1024/1024:.1f} MB for instant upload.")
        except Exception as e:
            print(f"[!] Compression warning: {e}. Uploading original file.")
            upload_target = file_path

    print(f"[*] Uploading {upload_target} to GitHub Release CDN ({tag_name})...")
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    create_url = f"https://api.github.com/repos/{GITHUB_REPO}/releases"
    res = requests.post(
        create_url,
        headers=headers,
        json={"tag_name": tag_name, "name": release_title, "draft": False, "prerelease": False},
        timeout=30
    )
    if res.status_code not in (200, 201):
        raise RuntimeError(f"Failed to create GitHub release: {res.status_code} - {res.text}")
        
    release_data = res.json()
    upload_url = release_data["upload_url"].split("{")[0]
    
    file_name = os.path.basename(file_path)
    # Use curl for streaming binary upload directly to uploads.github.com
    curl_cmd = [
        "curl", "-sS", "-X", "POST",
        "-H", f"Authorization: token {GITHUB_TOKEN}",
        "-H", "Content-Type: video/mp4",
        "--data-binary", f"@{upload_target}",
        f"{upload_url}?name={file_name}"
    ]
    out = subprocess.check_output(curl_cmd, text=True)
    asset_data = json.loads(out)
    download_url = asset_data.get("browser_download_url")
    if not download_url:
        raise RuntimeError(f"Failed to upload video asset via curl: {out}")
        
    print(f"[✓] Video successfully hosted on GitHub CDN: {download_url}")
    return download_url

def _to_graphql_literal(val):
    if isinstance(val, dict):
        items = []
        for k, v in val.items():
            if k in ["mode", "schedulingType", "type", "privacy"]:
                items.append(f"{k}: {v}")
            else:
                items.append(f"{k}: {_to_graphql_literal(v)}")
        return "{ " + ", ".join(items) + " }"
    elif isinstance(val, list):
        return "[ " + ", ".join(_to_graphql_literal(x) for x in val) + " ]"
    elif isinstance(val, bool):
        return "true" if val else "false"
    elif isinstance(val, (int, float)):
        return str(val)
    elif isinstance(val, str):
        return json.dumps(val)
    return "null"

def dispatch_post_payload(channel_id: str, text: str, public_video_url: str, metadata: dict = None, due_at_utc: str = None) -> str:
    url = "https://api.buffer.com"
    headers = {
        "Authorization": f"Bearer {BUFFER_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    input_payload = {
        "channelId": channel_id,
        "text": text,
        "schedulingType": "automatic",
        "mode": "customScheduled" if due_at_utc else "shareNow",
        "needsApproval": False,
        "assets": [
            {
                "video": {
                    "url": public_video_url
                }
            }
        ]
    }
    if due_at_utc:
        input_payload["dueAt"] = due_at_utc
    if metadata:
        input_payload["metadata"] = metadata

    q_input = _to_graphql_literal(input_payload)
    mutation = (
        "mutation { createPost(input: " + q_input + ") { "
        "__typename "
        "... on PostActionSuccess { post { id status channelId } } "
        "... on MutationError { message } "
        "... on InvalidInputError { message } "
        "} }"
    )

    data = None
    try:
        res = requests.post(url, headers=headers, json={"query": mutation}, timeout=3)
        if res.status_code == 200:
            data = res.json()
    except Exception:
        pass

    if data is None:
        try:
            curl_cmd = [
                "curl", "-s", "-X", "POST", url,
                "-H", f"Authorization: Bearer {BUFFER_ACCESS_TOKEN}",
                "-H", "Content-Type: application/json",
                "-d", json.dumps({"query": mutation})
            ]
            curl_out = subprocess.check_output(curl_cmd).decode("utf-8")
            data = json.loads(curl_out)
        except Exception as ce:
            print(f"[!] Curl to Buffer failed: {ce}")
            return None

    if "errors" in data:
        print(f"[!] Buffer GraphQL Error ({channel_id}): {json.dumps(data['errors'])}")
        return None
    action_res = data.get("data", {}).get("createPost", {})
    typename = action_res.get("__typename")
    if typename == "PostActionSuccess":
        post_id = action_res.get("post", {}).get("id") or "scheduled"
        return post_id
    else:
        err_msg = action_res.get("message", "Unknown buffer error")
        print(f"[!] Buffer Mutation Error ({channel_id}): {err_msg}")
        return None

def dispatch_to_buffer(video_target: str, caption: str, channel_id: str = None):
    """
    Backwards-compatible single-channel dispatch function (defaults to Instagram).
    """
    if os.path.exists(video_target):
        public_video_url = upload_video_to_github_release(video_target)
    else:
        public_video_url = video_target

    target_channel = channel_id or DEFAULT_CHANNEL_ID
    meta = {
        "instagram": {
            "type": "reel",
            "shouldShareToFeed": True
        }
    }
    post_id = dispatch_post_payload(target_channel, caption, public_video_url, meta)
    if post_id:
        print(f"[✓] Successfully queued in Buffer (Post ID: {post_id})")
    return post_id

def dispatch_to_all_platforms(video_target: str, meta: dict, items: list, due_at_utc: str = None) -> dict:
    """
    Dispatches the rendered video to Instagram Reels, YouTube Shorts, and X (Twitter).
    """
    if os.path.exists(video_target):
        public_video_url = upload_video_to_github_release(video_target)
    else:
        public_video_url = video_target

    results = {}
    item_titles = [it["name"].split("/")[-1].replace("-", " ").title() for it in items]
    bio_hub_url = "https://jrddiwan27.github.io/daily-ai-reels/"

    # 1. Instagram Reels (ai.nxtlvl high-converting viral structure)
    desc0 = items[0].get('description', 'High performance model')[:70] if len(items) > 0 else 'Fast local inference'
    desc1 = items[1].get('description', 'Autonomous agent')[:70] if len(items) > 1 else 'Autonomous automation'
    desc2 = items[2].get('description', 'Instant extraction')[:70] if len(items) > 2 else 'Zero fees'

    ig_caption = (
        f"Comment “{meta['cta_keyword']}” and I’ll DM you my full setup + the free code repo 📩\n\n"
        f"I turned open source AI into an autonomous content engine 🤖\n"
        f"It doesn’t just post… it grows your page.\n"
        f"That’s how I went from 339 → 2,400+ followers.\n\n"
        f"The core moves:\n"
        f"1. {item_titles[0]} — {desc0}\n"
        f"2. {item_titles[1]} — {desc1}\n"
        f"3. {item_titles[2]} — {desc2}\n\n"
        f"🎁 Bonus: The Proven System for Viral Reels, free (16,000+ downloads)\n"
        f"💾 Save this for your next reel\n"
        f"➡️ Follow @jayant.digitalstudio for daily AI tools\n\n"
        f"{' '.join(meta.get('hashtags', [])[:5])}"
    )
    ig_meta = {"instagram": {"type": "reel", "shouldShareToFeed": True}}
    ig_id = dispatch_post_payload(CHANNELS["instagram"], ig_caption, public_video_url, ig_meta, due_at_utc=due_at_utc)
    results["instagram"] = ig_id
    print(f"[✓ INSTAGRAM] Scheduled Reel: Post ID {ig_id}")

    # 2. YouTube Shorts
    yt_title = f"{meta['post_title'].rstrip('! 🚀⚡🧠🤫🎯')} #Shorts"[:95]
    yt_description = (
        f"{meta['post_title']}\n\n"
        f"Featured tools:\n1. {item_titles[0]}\n2. {item_titles[1]}\n3. {item_titles[2]}\n\n"
        f"👉 Direct links & setup code: {bio_hub_url}\n\n"
        f"#Shorts {' '.join(meta.get('hashtags', []))}"
    )
    yt_meta = {
        "youtube": {
            "title": yt_title,
            "privacy": "public",
            "categoryId": "28",
            "madeForKids": False
        }
    }
    yt_id = dispatch_post_payload(CHANNELS["youtube"], yt_description, public_video_url, yt_meta, due_at_utc=due_at_utc)
    results["youtube"] = yt_id
    print(f"[✓ YOUTUBE] Scheduled Shorts: Post ID {yt_id}")

    # 3. Twitter / X (Strict Standard Non-Premium <= 280 Chars, Zero Links)
    tw_title = meta['post_title'].rstrip('! 🚀⚡🧠🤫🎯')
    tw_text = (
        f"⚡ {tw_title}\n\n"
        f"1. {item_titles[0]}\n"
        f"2. {item_titles[1]}\n"
        f"3. {item_titles[2]}\n\n"
        f"Drop a comment below to get the setup code.\n"
        f"#AI #Tech #Developers"
    )
    # Hard clamp to 270 characters to guarantee non-premium compliance
    if len(tw_text) > 270:
        tw_text = tw_text[:267] + "..."

    tw_id = dispatch_post_payload(CHANNELS["twitter"], tw_text, public_video_url, due_at_utc=due_at_utc)
    results["twitter"] = tw_id
    print(f"[✓ X/TWITTER] Scheduled Post: Post ID {tw_id} ({len(tw_text)} chars)")

    return results

if __name__ == "__main__":
    print("Multi-channel Buffer Dispatcher initialized for Instagram, YouTube, and X.")
