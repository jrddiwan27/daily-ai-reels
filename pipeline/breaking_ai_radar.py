import os
import json
import requests
import datetime
from pipeline.dedup_manager import is_duplicate, record_published

def fetch_huggingface_trending(limit: int = 10) -> list:
    """
    Fetches hot trending open-weight models from Hugging Face.
    Catches major model drops like Qwen-Image, DeepSeek, Flux, Llama in real-time.
    """
    url = "https://huggingface.co/api/models?sort=trendingScore&direction=-1&limit=25"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            models = res.json()
            results = []
            for m in models:
                mid = m.get("id", "")
                # Focus on significant releases (vision, image, reasoning, code, llm)
                tags = m.get("tags", [])
                pipeline_tag = m.get("pipeline_tag", "")
                likes = m.get("likes", 0)
                downloads = m.get("downloads", 0)
                
                results.append({
                    "source": "huggingface",
                    "title": mid,
                    "name": mid.split("/")[-1],
                    "full_name": mid,
                    "url": f"https://huggingface.co/{mid}",
                    "score": m.get("trendingScore", 0) + (likes * 2),
                    "pipeline_tag": pipeline_tag,
                    "description": f"Trending open-weights model on Hugging Face ({pipeline_tag or 'AI model'}) with {likes} likes."
                })
            return results[:limit]
    except Exception as e:
        print(f"[!] Hugging Face API warning: {e}")
    return []

def fetch_hackernews_ai_stories(limit: int = 10) -> list:
    """
    Scrapes breaking AI news and model announcements from Hacker News (Algolia API).
    """
    url = "https://hn.algolia.com/api/v1/search_by_date?tags=story&query=AI&hitsPerPage=30"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            hits = res.json().get("hits", [])
            results = []
            keywords = ["open source", "weights", "qwen", "deepseek", "claude", "gemini", "llama", "release", "benchmark", "model", "agent"]
            for h in hits:
                title = h.get("title", "")
                points = h.get("points") or 0
                title_lower = title.lower()
                if any(kw in title_lower for kw in keywords) and points >= 15:
                    results.append({
                        "source": "hackernews",
                        "title": title,
                        "name": title[:30],
                        "full_name": title,
                        "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                        "score": points * 3,
                        "description": title
                    })
            return results[:limit]
    except Exception as e:
        print(f"[!] Hacker News API warning: {e}")
    return []

def scan_breaking_ai_events() -> list:
    """
    24/7 Sentinel: Aggregates real-time signals from Hugging Face, Hacker News, and GitHub.
    Filters out duplicates and ranks breaking candidates by viral impact score.
    """
    print("[*] 24/7 AI Radar: Scanning internet for breaking AI model & tool releases...")
    candidates = []

    hf = fetch_huggingface_trending(limit=12)
    candidates.extend(hf)

    hn = fetch_hackernews_ai_stories(limit=10)
    candidates.extend(hn)

    # Filter out anything already covered in the past 60 days
    fresh = []
    for c in candidates:
        key = c.get("full_name") or c.get("title")
        if not is_duplicate(key, max_days=60):
            fresh.append(c)

    # Sort by impact score descending
    fresh.sort(key=lambda x: x.get("score", 0), reverse=True)
    print(f"[✓] 24/7 AI Radar: Found {len(fresh)} fresh breaking AI events.")
    for f in fresh[:5]:
        print(f"    • [{f['source'].upper()}] {f['title']} (Score: {f.get('score', 0)})")

    return fresh

if __name__ == "__main__":
    scan_breaking_ai_events()
