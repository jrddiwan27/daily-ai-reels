import os
import json
import time
import requests

import subprocess

BUFFER_ACCESS_TOKEN = os.environ.get("BUFFER_ACCESS_TOKEN") or "gCUwoZC7cOjHobBSz5a9S3a4nrBh1PF8mydBp6_Rku2"
DEFAULT_CHANNEL_ID = os.environ.get("BUFFER_CHANNEL_ID") or "6ac7f82a6a5c39ccb6564f06" # jayant.digitalstudio
GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY") or "jrddiwan27/daily-ai-reels"

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
    
    # 1. Create release
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
    
    # 2. Upload video asset
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

def dispatch_to_buffer(video_target: str, caption: str, channel_id: str = None):
    """
    Schedules and publishes video to Buffer Instagram Reels using official GraphQL API.
    """
    token = BUFFER_ACCESS_TOKEN
    target_channel = channel_id or DEFAULT_CHANNEL_ID
    
    if not token or not target_channel:
        print("[!] Missing BUFFER_ACCESS_TOKEN or channel ID.")
        return False
        
    # If video_target is a local file, upload it to GitHub Release CDN
    if os.path.exists(video_target):
        public_video_url = upload_video_to_github_release(video_target)
    else:
        public_video_url = video_target

    url = "https://api.buffer.com"
    headers = {
        "Authorization": f"Bearer {token}",
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
            "channelId": target_channel,
            "text": caption,
            "schedulingType": "automatic",
            "mode": "addToQueue",
            "needsApproval": False,
            "assets": [
                {
                    "video": {
                        "url": public_video_url
                    }
                }
            ],
            "metadata": {
                "instagram": {
                    "type": "reel",
                    "shouldShareToFeed": True
                }
            }
        }
    }
    
    print(f"[*] Dispatching Instagram Reel to Buffer channel ({target_channel})...")
    res = requests.post(url, headers=headers, json={"query": mutation, "variables": variables}, timeout=60)
    
    if res.status_code == 200:
        data = res.json()
        if "errors" in data:
            print(f"[!] GraphQL Error: {json.dumps(data['errors'])}")
            return None
            
        post_res = data.get("data", {}).get("createPost", {})
        if "message" in post_res and "post" not in post_res:
            print(f"[!] Buffer error message: {post_res['message']}")
            return None
            
        post_id = post_res.get("post", {}).get("id") or "scheduled"
        print(f"[✓] Successfully queued Instagram Reel in Buffer for @jayant.digitalstudio! (Post ID: {post_id})")
        print(json.dumps(post_res, indent=2))
        return post_id
    else:
        print(f"[✗] Failed to communicate with Buffer: {res.status_code} - {res.text}")
        return None

if __name__ == "__main__":
    print("Buffer GraphQL Dispatcher initialized for @jayant.digitalstudio.")
