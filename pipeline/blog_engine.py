import os
import json
import datetime
import re
import requests
from pipeline.ai_scriptwriter import get_gemini_key

DOCS_DIR = "docs"
POSTS_DATA_FILE = os.path.join(DOCS_DIR, "posts_data.json")

def load_posts_data() -> list:
    if os.path.exists(POSTS_DATA_FILE):
        try:
            with open(POSTS_DATA_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] Error reading {POSTS_DATA_FILE}: {e}")
    return []

def save_posts_data(posts: list):
    os.makedirs(DOCS_DIR, exist_ok=True)
    with open(POSTS_DATA_FILE, "w") as f:
        json.dump(posts, f, indent=2)

def generate_blog_article(slot_id: int, meta: dict, items: list, script_data: dict, video_url: str = None) -> dict:
    """
    Synthesizes an SEO-optimized blog article and blueprint from the reel items.
    """
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    ist_offset = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    now_ist = now_utc.astimezone(ist_offset)
    date_str = now_ist.strftime("%B %d, %Y")
    date_slug = now_ist.strftime("%Y-%m-%d")
    slot_slug = meta.get("hook_theme", f"slot-{slot_id}")

    post_title = meta.get("post_title", "Daily AI Systems & Automation Blueprint").rstrip("! 🚀⚡🧠🤫🎯")

    # Item breakdowns
    item_sections = []
    for idx, itm in enumerate(items, 1):
        name = itm.get("name", f"Tool {idx}").replace("-", " ").title()
        url = itm.get("url") or f"https://github.com/{itm.get('full_name', '')}"
        desc = itm.get("description", "")
        stars = itm.get("stars", 10000)
        badge = itm.get("badge", meta.get("badge_title", "AI TOOL"))
        
        # Suggested install / quickstart command
        slug_raw = itm.get("name", "").lower()
        if "pip" in desc.lower() or "python" in desc.lower():
            cmd = f"pip install {slug_raw}"
        elif "npm" in desc.lower() or "typescript" in desc.lower():
            cmd = f"npx {slug_raw} --latest"
        elif "docker" in desc.lower():
            cmd = f"docker run -d -p 8080:8080 {slug_raw}"
        else:
            cmd = f"git clone {url}.git\ncd {slug_raw}\n./setup.sh"

        item_sections.append({
            "number": idx,
            "name": name,
            "url": url,
            "stars": f"★ {stars:,}" if isinstance(stars, int) else str(stars),
            "badge": badge,
            "description": desc,
            "command": cmd,
            "image": itm.get("demo_media") or itm.get("og_image") or "assets/repos/heygen-com_hyperframes/og_banner.png"
        })

    post_data = {
        "id": f"{date_slug}-slot-{slot_id}",
        "title": post_title,
        "date": date_str,
        "date_slug": date_slug,
        "slot_id": slot_id,
        "slot_name": meta.get("slot_name", "AI Insights"),
        "badge": meta.get("badge_title", "AI RADAR"),
        "cta_keyword": meta.get("cta_keyword", "TOOLS"),
        "video_url": video_url or "",
        "summary": script_data.get("hook", f"Here are 3 breakthrough tools featured in today's {meta.get('slot_name')} edition."),
        "voiceover_script": script_data.get("full_script", ""),
        "items": item_sections,
        "cta_text": f"Want our studio to build custom autonomous AI employees for your workflow? Follow @jayant.digitalstudio and DM '{meta.get('cta_keyword', 'AUTOMATE')}'.",
        "tags": meta.get("hashtags", ["#ai", "#developer", "#automation"])
    }

    # Prepend to posts list (newest first)
    posts = load_posts_data()
    # Deduplicate by ID
    posts = [p for p in posts if p.get("id") != post_data["id"]]
    posts.insert(0, post_data)
    save_posts_data(posts)

    print(f"[✓ BLOG] Published blog post: '{post_title}' -> {POSTS_DATA_FILE}")
    return post_data
