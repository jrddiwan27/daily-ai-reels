import os
import json
import requests

BUFFER_ACCESS_TOKEN = os.environ.get("BUFFER_ACCESS_TOKEN", "gCUwoZC7cOjHobBSz5a9S3a4nrBh1PF8mydBp6_Rku2")
DEFAULT_CHANNEL_ID = os.environ.get("BUFFER_CHANNEL_ID", "6ac7f82a6a5c39ccb6564f06") # jayant.digitalstudio

def dispatch_to_buffer(video_url: str, caption: str, channel_id: str = None):
    """
    Schedules and publishes video to Buffer using official GraphQL API.
    """
    token = BUFFER_ACCESS_TOKEN
    target_channel = channel_id or DEFAULT_CHANNEL_ID
    
    if not token or not target_channel:
        print("[!] Missing BUFFER_ACCESS_TOKEN or channel ID.")
        return False
        
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
            state
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
                        "url": video_url
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
