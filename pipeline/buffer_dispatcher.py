import os
import json
import requests

BUFFER_ACCESS_TOKEN = os.environ.get("BUFFER_ACCESS_TOKEN") or "gCUwoZC7cOjHobBSz5a9S3a4nrBh1PF8mydBp6_Rku2"
DEFAULT_CHANNEL_ID = os.environ.get("BUFFER_CHANNEL_ID") or "6ac7f82a6a5c39ccb6564f06" # jayant.digitalstudio

def upload_to_public_cdn(file_path: str) -> str:
    """
    Uploads video to free permanent public CDN so Buffer can ingest it.
    Zero configuration, zero API key, zero cost.
    """
    print(f"[*] Uploading {file_path} to public CDN for Buffer ingestion...")
    try:
        with open(file_path, "rb") as f:
            res = requests.post(
                "https://catbox.moe/user/api.php",
                data={"reqtype": "fileupload"},
                files={"fileToUpload": f},
                timeout=120
            )
        if res.status_code == 200 and res.text.startswith("https://"):
            public_url = res.text.strip()
            print(f"[✓] Video hosted publicly at: {public_url}")
            return public_url
    except Exception as e:
        print(f"[!] Primary upload error: {e}, trying fallback...")

    # Fallback to tmpfiles
    try:
        with open(file_path, "rb") as f:
            res = requests.post(
                "https://tmpfiles.org/api/v1/upload",
                files={"file": f},
                timeout=120
            )
        if res.status_code == 200:
            data = res.json()
            raw_url = data["data"]["url"]
            # Convert https://tmpfiles.org/ID/name to https://tmpfiles.org/dl/ID/name
            direct_url = raw_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
            print(f"[✓] Video hosted publicly at fallback: {direct_url}")
            return direct_url
    except Exception as e:
        print(f"[!] Fallback upload error: {e}")

    raise RuntimeError("Failed to obtain public video URL for Buffer ingestion.")

def dispatch_to_buffer(video_target: str, caption: str, channel_id: str = None):
    """
    Schedules and publishes video to Buffer using official GraphQL API.
    """
    token = BUFFER_ACCESS_TOKEN
    target_channel = channel_id or DEFAULT_CHANNEL_ID
    
    if not token or not target_channel:
        print("[!] Missing BUFFER_ACCESS_TOKEN or channel ID.")
        return False
        
    # If video_target is a local file, upload it to get public URL
    if os.path.exists(video_target):
        public_video_url = upload_to_public_cdn(video_target)
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
            "schedulingType": "addToQueue",
            "mode": "buffer",
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
    
    print(f"[*] Dispatching video to Buffer channel ({target_channel})...")
    res = requests.post(url, headers=headers, json={"query": mutation, "variables": variables})
    
    if res.status_code == 200:
        data = res.json()
        if "errors" in data:
            print(f"[!] GraphQL Error: {json.dumps(data['errors'])}")
            return False
        print(f"[✓] Successfully queued post in Buffer for @jayant.digitalstudio!")
        print(json.dumps(data.get("data", {}), indent=2))
        return True
    else:
        print(f"[✗] Failed to communicate with Buffer: {res.status_code} - {res.text}")
        return False

if __name__ == "__main__":
    print("Buffer GraphQL Dispatcher initialized for @jayant.digitalstudio.")
