import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from youtube_transcript_api import YouTubeTranscriptApi

TOP_CREATORS = [
    {"name": "Fireship", "channel_id": "UCsBjURrPoezykLs9EqgamOA"},
    {"name": "Matthew Berman", "channel_id": "UCawZsQWqfGSbCI5yjkdVkTA"},
    {"name": "AI Jason", "channel_id": "UCrXSVX9a1mj8l0CMLwKgMVw"},
    {"name": "Wes Roth", "channel_id": "UCqcbQf6yw5KzRoDDcZ_wBSw"},
    {"name": "Liam Ottley", "channel_id": "UCui4jxDaMb53Gdh-AZUTPAg"}
]

def fetch_creator_trending_transcripts(limit_creators=4) -> list:
    """
    Scrapes the latest videos from top AI creators via public RSS feeds (zero API keys),
    and downloads the first 45 seconds of their transcripts to serve as viral few-shot samples.
    """
    print("[*] Creator Radar: Scanning top creators for latest viral topics & scripts...")
    samples = []
    
    for creator in TOP_CREATORS[:limit_creators]:
        feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={creator['channel_id']}"
        try:
            req = urllib.request.Request(feed_url, headers={"User-Agent": "Mozilla/5.0"})
            content = urllib.request.urlopen(req, timeout=10).read()
            root = ET.fromstring(content)
            ns = {"atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
            
            entry = root.find("atom:entry", ns)
            if entry is None:
                continue
                
            video_id = entry.find("yt:videoId", ns).text
            title = entry.find("atom:title", ns).text
            
            transcript_text = ""
            try:
                transcript_snippets = YouTubeTranscriptApi().fetch(video_id)
                # Keep text up to first 45 seconds
                hook_snippets = [s.text for s in transcript_snippets if getattr(s, "start", 0) < 45.0]
                transcript_text = " ".join(hook_snippets[:25]).replace("\n", " ").strip()
            except Exception as te:
                pass
                
            samples.append({
                "creator": creator["name"],
                "video_title": title,
                "video_id": video_id,
                "transcript_sample": transcript_text or f"Topic hook from {creator['name']}: {title}"
            })
            print(f"[✓] Captured trend from {creator['name']}: '{title[:45]}...'")
        except Exception as e:
            print(f"[!] Error fetching feed for {creator['name']}: {e}")
            
    os.makedirs("assets", exist_ok=True)
    with open("assets/creator_trends.json", "w") as f:
        json.dump(samples, f, indent=2)
        
    return samples

if __name__ == "__main__":
    results = fetch_creator_trending_transcripts()
    print(f"Collected {len(results)} viral reference trends.")
