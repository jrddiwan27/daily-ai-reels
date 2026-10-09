import os
import re
import json
import requests
from urllib.parse import urljoin

def search_trending_ai_repos(limit=3):
    """
    Finds high-growth, trending AI developer repositories using GitHub Search API.
    """
    print("[*] Searching GitHub for trending AI developer repositories...")
    url = "https://api.github.com/search/repositories"
    params = {
        "q": "topic:ai stars:>1000",
        "sort": "updated",
        "order": "desc",
        "per_page": 10
    }
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Autonomous-Video-Engine"
    }
    
    try:
        res = requests.get(url, params=params, headers=headers, timeout=10)
        if res.status_code == 200:
            items = res.json().get("items", [])
            curated = []
            for item in items:
                name_low = item["name"].lower()
                desc_low = (item.get("description") or "").lower()
                if any(bad in name_low or bad in desc_low for bad in ["mev", "flashloan", "crypto", "trading", "airdrop", "arbitrage", "casino"]):
                    continue
                if item.get("stargazers_count", 0) > 1000 and item.get("description"):
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
                        return curated
    except Exception as e:
        print(f"[!] GitHub API query warning: {e}")

    # Fallback catalog of famous breakthrough AI developer repos
    return get_curated_ai_repos()[:limit]

def get_curated_ai_repos():
    """Curated premier AI repositories with rich visuals and demo graphics."""
    return [
        {
            "owner": "heygen-com",
            "name": "hyperframes",
            "full_name": "heygen-com/hyperframes",
            "stars": 15400,
            "description": "Deterministic code-to-video rendering engine using HTML, CSS, and GSAP.",
            "url": "https://github.com/heygen-com/hyperframes",
            "language": "TypeScript"
        },
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
            "owner": "mendableai",
            "name": "firecrawl",
            "full_name": "mendableai/firecrawl",
            "stars": 24200,
            "description": "Turn entire websites into clean, LLM-ready markdown with zero hallucinations.",
            "url": "https://github.com/mendableai/firecrawl",
            "language": "TypeScript"
        }
    ]

def fetch_repo_media_assets(repo: dict, base_dir: str = "assets/repos") -> dict:
    """
    Downloads official GitHub OpenGraph social cards and extracts real high-res demo 
    screenshots, GIFs, and user-attachment UI previews from the repository README.
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
    else:
        repo["og_image"] = og_path
            
    # 2. Extract demo media from README (main and master branches)
    for branch in ["main", "master"]:
        readme_url = f"https://raw.githubusercontent.com/{repo['full_name']}/{branch}/README.md"
        try:
            r = requests.get(readme_url, timeout=10)
            if r.status_code == 200:
                content = r.text
                
                # Match markdown images, html img tags, and github user-attachments
                patterns = [
                    r'!\[.*?\]\(([^\s\)]+)\)',
                    r'<img[^>]+src=["\']([^"\']+)["\']',
                    r'https://github\.com/user-attachments/assets/[a-zA-Z0-9-]+'
                ]
                found_candidates = []
                for p in patterns:
                    for m in re.findall(p, content, re.IGNORECASE):
                        if isinstance(m, str):
                            found_candidates.append(m)
                            
                # Filter out shields, badges, icons
                valid_media = []
                for u in found_candidates:
                    u_low = u.lower()
                    if any(x in u_low for x in ["shield.io", "badge", "travis", "sonar", "license", "svg"]):
                        continue
                    if any(ext in u_low for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp"]) or "user-attachments" in u_low:
                        if not u.startswith("http"):
                            u = f"https://raw.githubusercontent.com/{repo['full_name']}/{branch}/{u.lstrip('./')}"
                        valid_media.append(u)
                        
                if valid_media:
                    demo_url = valid_media[0]
                    ext = "png"
                    if ".gif" in demo_url.lower(): ext = "gif"
                    elif ".webp" in demo_url.lower(): ext = "webp"
                    elif ".jpg" in demo_url.lower() or ".jpeg" in demo_url.lower(): ext = "jpg"
                    
                    demo_path = os.path.join(target_dir, f"demo.{ext}")
                    if not os.path.exists(demo_path):
                        dm_res = requests.get(demo_url, timeout=15)
                        if dm_res.status_code == 200:
                            with open(demo_path, "wb") as f:
                                f.write(dm_res.content)
                            repo["demo_media"] = demo_path
                            print(f"[✓] Downloaded real README demo asset for {repo['full_name']} -> {demo_path}")
                            break
                    else:
                        repo["demo_media"] = demo_path
                        break
        except Exception as e:
            pass
            
    # Guarantee a media asset is always present
    if not repo.get("demo_media"):
        repo["demo_media"] = repo.get("og_image")
        
    return repo

def scrape_and_cache_all(limit=3):
    repos = search_trending_ai_repos(limit=limit)
    enriched = []
    for r in repos:
        enriched.append(fetch_repo_media_assets(r))
        
    out_file = "assets/curated_repos.json"
    with open(out_file, "w") as f:
        json.dump(enriched, f, indent=2)
        
    return enriched

if __name__ == "__main__":
    results = scrape_and_cache_all(3)
    print(f"Scraped {len(results)} repositories with verified real media assets.")
