import os
import re
import json
import requests
from urllib.parse import urljoin

def search_trending_ai_repos(limit=5):
    """
    Finds high-growth, trending AI developer repositories using GitHub Search API.
    """
    print("[*] Searching GitHub for trending AI developer repositories...")
    url = "https://api.github.com/search/repositories"
    params = {
        "q": "topic:ai stars:>1000",
        "sort": "updated",
        "order": "desc",
        "per_page": 15
    }
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Autonomous-Video-Engine"
    }
    
    res = requests.get(url, params=params, headers=headers)
    if res.status_code != 200:
        print(f"[!] GitHub search fallback triggered (status {res.status_code})")
        # Fallback to curated premier AI repositories if rate-limited
        return get_curated_ai_repos()[:limit]
        
    items = res.json().get("items", [])
    curated = []
    
    for item in items:
        # Filter for actual developer tools/repos with substantial stars
        if item.get("stargazers_count", 0) > 1500 and item.get("description"):
            curated.append({
                "owner": item["owner"]["login"],
                "name": item["name"],
                "full_name": item["full_name"],
                "stars": item["stargazers_count"],
                "description": item["description"],
                "url": item["html_url"],
                "language": item.get("language") or "Python"
            })
            if len(curated) >= limit:
                break
                
    if len(curated) < limit:
        return get_curated_ai_repos()[:limit]
        
    return curated

def get_curated_ai_repos():
    """Curated fallback catalog of breakthrough AI developer repos."""
    return [
        {
            "owner": "browser-use",
            "name": "browser-use",
            "full_name": "browser-use/browser-use",
            "stars": 38500,
            "description": "Make websites accessible for AI agents to browse, click, and automate workflows.",
            "url": "https://github.com/browser-use/browser-use",
            "language": "Python"
        },
        {
            "owner": "ollama",
            "name": "ollama",
            "full_name": "ollama/ollama",
            "stars": 118000,
            "description": "Get up and running with Llama 3, DeepSeek, and Mistral locally in 1 command.",
            "url": "https://github.com/ollama/ollama",
            "language": "Go"
        },
        {
            "owner": "mendableai",
            "name": "firecrawl",
            "full_name": "mendableai/firecrawl",
            "stars": 24200,
            "description": "Turn entire websites into clean, LLM-ready markdown with zero hallucinations.",
            "url": "https://github.com/mendableai/firecrawl",
            "language": "TypeScript"
        },
        {
            "owner": "cline",
            "name": "cline",
            "full_name": "cline/cline",
            "stars": 42100,
            "description": "Autonomous coding agent right inside VS Code that reads errors, runs bash, and builds features.",
            "url": "https://github.com/cline/cline",
            "language": "TypeScript"
        },
        {
            "owner": "heygen-com",
            "name": "hyperframes",
            "full_name": "heygen-com/hyperframes",
            "stars": 15400,
            "description": "Deterministic code-to-video rendering engine using HTML, CSS, and GSAP.",
            "url": "https://github.com/heygen-com/hyperframes",
            "language": "TypeScript"
        }
    ]

def fetch_repo_media_assets(repo: dict, base_dir: str = "assets/repos") -> dict:
    """
    Downloads the official GitHub OpenGraph card and extracts embedded demo GIFs/images from README.
    """
    repo_slug = repo["full_name"].replace("/", "_")
    target_dir = os.path.join(base_dir, repo_slug)
    os.makedirs(target_dir, exist_ok=True)
    
    # 1. Download OpenGraph social banner
    og_url = f"https://opengraph.githubassets.com/1/{repo['full_name']}"
    og_path = os.path.join(target_dir, "og_banner.png")
    
    if not os.path.exists(og_path):
        try:
            r = requests.get(og_url, timeout=10)
            if r.status_code == 200:
                with open(og_path, "wb") as f:
                    f.write(r.content)
                repo["og_image"] = og_path
                print(f"[✓] Downloaded OG banner for {repo['full_name']}")
        except Exception as e:
            print(f"[!] Could not download OG image for {repo['full_name']}: {e}")
            
    # 2. Extract demo media from README
    readme_url = f"https://raw.githubusercontent.com/{repo['full_name']}/main/README.md"
    try:
        r = requests.get(readme_url, timeout=10)
        if r.status_code == 200:
            content = r.text
            # Look for image and gif URLs (markdown or HTML tags)
            media_urls = re.findall(r'(?:!\[.*?\]\((https?://[^\s\)]+\.(?:png|jpg|jpeg|gif|webp))\)|<img[^>]+src=["\'](https?://[^"\']+\.(?:png|jpg|jpeg|gif|webp))["\'])', content, re.IGNORECASE)
            
            flat_urls = [u[0] or u[1] for u in media_urls if (u[0] or u[1])]
            # Filter out badges / shields
            content_media = [u for u in flat_urls if not any(x in u.lower() for x in ["shield.io", "badge", "travis", "sonar"])]
            
            if content_media:
                demo_url = content_media[0]
                ext = demo_url.split(".")[-1].split("?")[0]
                demo_path = os.path.join(target_dir, f"demo.{ext}")
                
                if not os.path.exists(demo_path):
                    dm_res = requests.get(demo_url, timeout=10)
                    if dm_res.status_code == 200:
                        with open(demo_path, "wb") as f:
                            f.write(dm_res.content)
                        repo["demo_media"] = demo_path
                        print(f"[✓] Downloaded real README demo asset for {repo['full_name']} -> {demo_path}")
    except Exception as e:
        print(f"[!] README media parsing skipped for {repo['full_name']}: {e}")
        
    return repo

def scrape_and_cache_all(limit=5):
    repos = search_trending_ai_repos(limit=limit)
    enriched = []
    for r in repos:
        enriched.append(fetch_repo_media_assets(r))
        
    out_file = "assets/curated_repos.json"
    with open(out_file, "w") as f:
        json.dump(enriched, f, indent=2)
        
    print(f"[✓] Enriched {len(enriched)} repositories with real media assets in {out_file}")
    return enriched

if __name__ == "__main__":
    scrape_and_cache_all(5)
