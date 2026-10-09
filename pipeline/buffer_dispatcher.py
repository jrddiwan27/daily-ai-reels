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
    
    print(f"[*] Uploading {file_path} to GitHub Release CDN ({tag_name})...")
    
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
    with open(file_path, "rb") as f:
        up_headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Content-Type": "video/mp4"
        }
        up_res = requests.post(f"{upload_url}?name={file_name}", headers=up_headers, data=f, timeout=120)
        
    if up_res.status_code not in (200, 201):
        raise RuntimeError(f"Failed to upload video asset to release: {up_res.status_code} - {up_res.text}")
        
    asset_data = up_res.json()
    download_url = asset_data["browser_download_url"]
    print(f"[✓] Video successfully hosted on GitHub CDN: {download_url}")
    return download_url

def dispatch_post_payload(channel_id: str, text: str, public_video_url: str, metadata: dict = None) -> str:
    url = "https://api.buffer.com"
    headers = {
        "Authorization": f"Bearer {BUFFER_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    mutation = """
    mutation CreatePost($input: CreatePostInput!) {
      createPost(input: $input) {
        ... on PostActionSuccess {
          post {
            id
            text
            status
          }
        }
        ... on MutationError {
          message
        }
      }
    }
    """
    
    variables = {
        "input": {
            "channelId": channel_id,
            "text": text,
            "schedulingType": "automatic",
            "mode": "addToQueue",
            "needsApproval": False,
            "assets": [
                {
                    "video": {
                        "url": public_video_url
                    }
                }
            ]
        }
    }
    if metadata:
        variables["input"]["metadata"] = metadata
        
    res = requests.post(url, headers=headers, json={"query": mutation, "variables": variables}, timeout=60)
    if res.status_code == 200:
        data = res.json()
        if "errors" in data:
            print(f"[!] GraphQL Error ({channel_id}): {json.dumps(data['errors'])}")
            return None
        post_res = data.get("data", {}).get("createPost", {})
        post_id = post_res.get("post", {}).get("id") or "scheduled"
        return post_id
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

def dispatch_to_all_platforms(video_target: str, meta: dict, items: list) -> dict:
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

    # 1. Instagram Reels
    ig_caption = (
        f"{meta['post_title']}\n\n"
        f"1. {item_titles[0]}\n2. {item_titles[1]}\n3. {item_titles[2]}\n\n"
        f"Comment '{meta['cta_keyword']}' and I'll DM you the blueprint & direct links!\n"
        f"All code & links in bio hub: {bio_hub_url}\n\n"
        f"{' '.join(meta.get('hashtags', []))}"
    )
    ig_meta = {"instagram": {"type": "reel", "shouldShareToFeed": True}}
    ig_id = dispatch_post_payload(CHANNELS["instagram"], ig_caption, public_video_url, ig_meta)
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
            "privacy": "PUBLIC",
            "madeForKids": False
        }
    }
    yt_id = dispatch_post_payload(CHANNELS["youtube"], yt_description, public_video_url, yt_meta)
    results["youtube"] = yt_id
    print(f"[✓ YOUTUBE] Scheduled Shorts: Post ID {yt_id}")

    # 3. Twitter / X
    tw_text = (
        f"🔥 {meta['post_title']}\n\n"
        f"1. {item_titles[0]}\n2. {item_titles[1]}\n3. {item_titles[2]}\n\n"
        f"All direct links & setup guides in our bio hub 👇\n{bio_hub_url}\n\n"
        f"#AI #Developer"
    )
    tw_id = dispatch_post_payload(CHANNELS["twitter"], tw_text, public_video_url)
    results["twitter"] = tw_id
    print(f"[✓ X/TWITTER] Scheduled Post: Post ID {tw_id}")

    return results

if __name__ == "__main__":
    print("Multi-channel Buffer Dispatcher initialized for Instagram, YouTube, and X.")
