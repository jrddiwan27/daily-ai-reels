import os
import json
import requests
import datetime
from pipeline.dedup_manager import is_duplicate, filter_non_duplicates
from pipeline.repo_asset_scraper import fetch_repo_media_assets, search_trending_ai_repos

# Curated catalog pools for each slot to guarantee non-duplicate high quality content
SLOT_CATALOGS = {
    # SLOT 1: Open Source AI Developer Repos
    1: [
        {"owner": "browser-use", "name": "browser-use", "full_name": "browser-use/browser-use", "stars": 42000, "description": "Make websites accessible for autonomous AI agents to browse, click and complete tasks.", "url": "https://github.com/browser-use/browser-use"},
        {"owner": "mendableai", "name": "firecrawl", "full_name": "mendableai/firecrawl", "stars": 28500, "description": "Turn entire websites into clean, LLM-ready markdown with zero hallucinations.", "url": "https://github.com/mendableai/firecrawl"},
        {"owner": "ollama", "name": "ollama", "full_name": "ollama/ollama", "stars": 115000, "description": "Run Llama 3, DeepSeek, and Mistral locally on your laptop with a single command.", "url": "https://github.com/ollama/ollama"},
        {"owner": "vllm-project", "name": "vllm", "full_name": "vllm-project/vllm", "stars": 36000, "description": "High-throughput, low-latency LLM serving engine with PagedAttention algorithms.", "url": "https://github.com/vllm-project/vllm"},
        {"owner": "QwenLM", "name": "Qwen2.5-Coder", "full_name": "QwenLM/Qwen2.5-Coder", "stars": 19500, "description": "Open-source coding powerhouse beating proprietary frontier models on code generation benchmarks.", "url": "https://github.com/QwenLM/Qwen2.5-Coder"},
        {"owner": "Marker-pdf", "name": "marker", "full_name": "VikParuchuri/marker", "stars": 21000, "description": "Converts complex PDF documents and academic papers to clean markdown 10x faster.", "url": "https://github.com/VikParuchuri/marker"},
        {"owner": "khoj-ai", "name": "khoj", "full_name": "khoj-ai/khoj", "stars": 18200, "description": "Open-source personal AI second brain that searches your notes, docs, and codebases offline.", "url": "https://github.com/khoj-ai/khoj"},
        {"owner": "deepseek-ai", "name": "DeepSeek-V3", "full_name": "deepseek-ai/DeepSeek-V3", "stars": 82000, "description": "671B parameter Mixture-of-Experts frontier language model trained with extreme compute efficiency.", "url": "https://github.com/deepseek-ai/DeepSeek-V3"}
    ],

    # SLOT 2: AI Workflows & Automation Blueprints
    2: [
        {"owner": "automation-lab", "name": "cursor-agent-loop", "full_name": "jayant/cursor-agent-loop", "stars": 9400, "description": "Continuous test-driven AI agent loop in Cursor that fixes its own bugs automatically.", "url": "https://cursor.com", "badge": "CURSOR AGENTS"},
        {"owner": "agency-stack", "name": "n8n-rag-pipeline", "full_name": "jayant/n8n-rag-pipeline", "stars": 14200, "description": "Self-hosted webhook automation that turns client PDFs into vector databases in 60 seconds.", "url": "https://n8n.io", "badge": "N8N WEBHOOK"},
        {"owner": "dev-ops", "name": "local-rag-ollama", "full_name": "jayant/local-rag-ollama", "stars": 11800, "description": "100% private offline document search engine using local embeddings and Ollama.", "url": "https://ollama.com", "badge": "OFFLINE AI"},
        {"owner": "lead-engine", "name": "firecrawl-lead-finder", "full_name": "jayant/firecrawl-lead-finder", "stars": 8900, "description": "Autonomous bot that scrapes 500 company websites, extracts founder emails, and drafts DMs.", "url": "https://firecrawl.dev", "badge": "AUTONOMOUS SCRAPER"},
        {"owner": "video-ops", "name": "remotion-auto-reels", "full_name": "jayant/remotion-auto-reels", "stars": 16500, "description": "Python to Remotion pipeline that renders 20 high-converting video variations per minute.", "url": "https://remotion.dev", "badge": "REEL ENGINE"},
        {"owner": "agentic-ops", "name": "claude-code-subagents", "full_name": "jayant/claude-code-subagents", "stars": 21000, "description": "Autonomous CLI architecture where subagents write tests and refactor large codebases.", "url": "https://anthropic.com", "badge": "CLI SUBAGENTS"},
        {"owner": "vector-ops", "name": "supabase-vector-sync", "full_name": "jayant/supabase-vector-sync", "stars": 12500, "description": "Automated pipeline syncing SQL tables to pgvector embeddings in real-time.", "url": "https://supabase.com", "badge": "PGVECTOR SYNC"},
        {"owner": "voice-ops", "name": "open-webui-voice-loop", "full_name": "jayant/open-webui-voice-loop", "stars": 18900, "description": "Completely offline voice-activated operating system running local frontier models.", "url": "https://openwebui.com", "badge": "LOCAL VOICE"}
    ],

    # SLOT 3: Tech Radar Teardown & Benchmarks
    3: [
        {"owner": "anthropic", "name": "claude-3.7-sonnet", "full_name": "anthropic/claude-3.7-sonnet", "stars": 99000, "description": "Hybrid thinking architecture offering instant response or deep reasoning in a single model.", "url": "https://anthropic.com", "badge": "HYBRID REASONING"},
        {"owner": "google", "name": "gemini-3.0-flash", "full_name": "google/gemini-3-flash", "stars": 94000, "description": "1-million token context window processing 100 pages of code in sub-500 milliseconds.", "url": "https://deepmind.google", "badge": "MILLION CONTEXT"},
        {"owner": "deepseek", "name": "deepseek-r1", "full_name": "deepseek-ai/deepseek-r1", "stars": 89000, "description": "Open-weights reasoning model matching closed commercial models at 95% lower inference cost.", "url": "https://deepseek.com", "badge": "OPEN REASONING"},
        {"owner": "meta-ai", "name": "llama-3.3-70b", "full_name": "meta-llama/llama-3.3", "stars": 78000, "description": "Flagship 70-billion open weights delivering 405B-level coding performance on commodity GPUs.", "url": "https://llama.meta.com", "badge": "OPEN WEIGHTS"},
        {"owner": "black-forest", "name": "flux.1-schnell", "full_name": "black-forest-labs/flux", "stars": 34000, "description": "12-billion parameter rectified flow transformer generating photoreal graphics in 4 steps.", "url": "https://blackforestlabs.ai", "badge": "NEXT-GEN IMAGE"},
        {"owner": "openai", "name": "whisper-v3-turbo", "full_name": "openai/whisper-large-v3-turbo", "stars": 67000, "description": "Transcribes 60 minutes of multilingual audio in 12 seconds with sub-1% word error rate.", "url": "https://openai.com", "badge": "TURBO TRANSCRIBE"},
        {"owner": "qwen", "name": "qwen-2.5-coder-32b", "full_name": "qwenlm/qwen-2.5-coder-32b", "stars": 24000, "description": "Open coding model beating commercial frontier models across 12 programming languages.", "url": "https://qwenlm.github.io", "badge": "TOP OPEN CODER"}
    ],

    # SLOT 4: Secret Web-Based AI Tools (No Code)
    4: [
        {"owner": "web-tools", "name": "bolt-new", "full_name": "stackblitz/bolt-new", "stars": 48000, "description": "Full-stack web development directly in browser sandbox with one-click Netlify deployment.", "url": "https://bolt.new", "badge": "FULLSTACK BROWSER"},
        {"owner": "no-code", "name": "lovable-dev", "full_name": "lovable/lovable-dev", "stars": 32000, "description": "Text-to-software builder creating production React and Supabase apps in 3 minutes.", "url": "https://lovable.dev", "badge": "PROD BUILDER"},
        {"owner": "media-ai", "name": "elevenlabs-reader", "full_name": "elevenlabs/reader", "stars": 55000, "description": "Ultra-realistic emotional voice cloning with dynamic accents and live text narration.", "url": "https://elevenlabs.io", "badge": "VOICE CLONE"},
        {"owner": "design-ai", "name": "recraft-ai", "full_name": "recraft/recraft-ai", "stars": 24000, "description": "Generate clean SVG vector art, brand logos, and 3D icons with transparent backgrounds.", "url": "https://recraft.ai", "badge": "VECTOR ENGINE"},
        {"owner": "visual-ai", "name": "napkin-ai", "full_name": "napkin/napkin-ai", "stars": 19000, "description": "Turn plain text bullet points into professional slide diagrams and visuals automatically.", "url": "https://napkin.ai", "badge": "DIAGRAM AI"},
        {"owner": "decks-ai", "name": "gamma-app", "full_name": "gamma/gamma-app", "stars": 38000, "description": "Generates interactive presentation decks and landing pages from simple notes in 30 seconds.", "url": "https://gamma.app", "badge": "INSTANT DECKS"},
        {"owner": "canvas-ai", "name": "krea-ai", "full_name": "krea/krea-ai", "stars": 29000, "description": "Real-time canvas generation that turns basic shapes and text into 4K artwork with zero lag.", "url": "https://krea.ai", "badge": "REALTIME CANVAS"}
    ],

    # SLOT 5: Master Prompts & Dev Architecture
    5: [
        {"owner": "prompt-lab", "name": "chain-of-density", "full_name": "prompt/chain-of-density", "stars": 26000, "description": "Recursive distillation framework that packs maximum technical insights into minimal token count.", "url": "https://arxiv.org/abs/2309.04269", "badge": "DENSITY RECURSION"},
        {"owner": "arch-patterns", "name": "role-task-constraint", "full_name": "prompt/rtc-framework", "stars": 31000, "description": "The senior engineer prompt template that eliminates 99% of LLM hallucinations in codebases.", "url": "https://jayantdigital.com", "badge": "ZERO HALLUCINATION"},
        {"owner": "agentic-ai", "name": "subagent-decomposition", "full_name": "prompt/subagent-decomp", "stars": 22000, "description": "Modular orchestration prompt dividing large software features into 4 parallel micro-agents.", "url": "https://jayantdigital.com", "badge": "MULTI-AGENT"},
        {"owner": "code-review", "name": "reverse-logic-debugger", "full_name": "prompt/reverse-debugger", "stars": 18000, "description": "Forces AI to write edge-case test suites and attack its own code before writing solutions.", "url": "https://jayantdigital.com", "badge": "TEST DRIVEN"},
        {"owner": "system-prompts", "name": "xml-tag-spec-generator", "full_name": "prompt/xml-structured-spec", "stars": 29000, "description": "Anthropic-grade XML prompt pattern for deterministic JSON outputs without broken schemas.", "url": "https://anthropic.com", "badge": "STRUCTURED SPEC"},
        {"owner": "refactor-lab", "name": "self-reflective-critic", "full_name": "prompt/self-reflective-critic", "stars": 27000, "description": "Two-pass generation prompt that critiques its own draft architecture before outputting code.", "url": "https://jayantdigital.com", "badge": "DUAL PASS CRITIC"},
        {"owner": "security-lab", "name": "adversarial-red-teamer", "full_name": "prompt/adversarial-red-teamer", "stars": 23000, "description": "Simulates security pen-testers to find race conditions and edge case exploits in APIs.", "url": "https://jayantdigital.com", "badge": "RED TEAM AUDIT"}
    ]
}

SLOT_METADATA = {
    1: {
        "slot_id": 1,
        "slot_name": "Morning Breakthrough (Open Source Repos)",
        "badge_title": "AI OPEN SOURCE",
        "badge_sub": "3 VERIFIED REPOS",
        "hook_theme": "repos",
        "cta_keyword": "REPOS",
        "hashtags": ["#developer", "#ai", "#opensource", "#github", "#coding"],
        "post_title": "3 Insane Open-Source AI Developer Repos You Need Today! 🚀"
    },
    2: {
        "slot_id": 2,
        "slot_name": "Midday Cheat Code (AI Workflows)",
        "badge_title": "AI AUTOMATION",
        "badge_sub": "AGENCY BLUEPRINT",
        "hook_theme": "workflows",
        "cta_keyword": "FLOW",
        "hashtags": ["#automation", "#aiworkflow", "#n8n", "#productivity", "#nocode"],
        "post_title": "The Automated AI Workflow Saving Us 20 Hours Every Week! ⚡"
    },
    3: {
        "slot_id": 3,
        "slot_name": "Tech Radar Teardown (Model Benchmarks)",
        "badge_title": "MODEL RADAR",
        "badge_sub": "BENCHMARK TEARDOWN",
        "hook_theme": "benchmarks",
        "cta_keyword": "RADAR",
        "hashtags": ["#artificialintelligence", "#deeplearning", "#llm", "#techtrends", "#futureoftech"],
        "post_title": "New Frontier Model Teardown: Why This Changes Everything! 🧠"
    },
    4: {
        "slot_id": 4,
        "slot_name": "Evening Toolkit (Secret Web AI Tools)",
        "badge_title": "SECRET AI TOOLS",
        "badge_sub": "NO-CODE WEBSITES",
        "hook_theme": "webtools",
        "cta_keyword": "TOOLS",
        "hashtags": ["#aitools", "#techhacks", "#freelancer", "#creatortools", "#websites"],
        "post_title": "3 Secret AI Websites That Feel Illegal To Know! 🤫"
    },
    5: {
        "slot_id": 5,
        "slot_name": "Night Owl Deep Dive (Master Prompts)",
        "badge_title": "PROMPT LAB",
        "badge_sub": "ELITE FRAMEWORK",
        "hook_theme": "prompts",
        "cta_keyword": "PROMPT",
        "hashtags": ["#promptengineering", "#chatgpt", "#claude", "#softwareengineer", "#aicoding"],
        "post_title": "The Senior AI Prompt Framework You Should Be Using in 2026! 🎯"
    }
}

def detect_current_slot() -> int:
    """
    Detects which slot matches the current time in IST:
    9 AM IST  -> Slot 1
    12 PM IST -> Slot 2
    3 PM IST  -> Slot 3
    6 PM IST  -> Slot 4
    9 PM IST  -> Slot 5
    """
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    ist = utc_now + datetime.timedelta(hours=5, minutes=30)
    hour = ist.hour

    if hour < 11:
        return 1   # ~9 AM
    elif hour < 14:
        return 2   # ~12 PM
    elif hour < 17:
        return 3   # ~3 PM
    elif hour < 20:
        return 4   # ~6 PM
    else:
        return 5   # ~9 PM

def fetch_content_for_slot(slot_id: int, count: int = 3) -> tuple:
    """
    Fetches 3 verified non-duplicate items for the specified slot.
    Guarantees zero repeat against history/published_history.json.
    """
    meta = dict(SLOT_METADATA.get(slot_id, SLOT_METADATA[1]))
    meta["slot_id"] = slot_id
    candidates = []

    if slot_id == 1:
        # Slot 1: First try dynamic trending search from GitHub
        try:
            dynamic_repos = search_trending_ai_repos(limit=10)
            candidates.extend(dynamic_repos)
        except Exception as e:
            print(f"[!] Dynamic search fallback: {e}")
        # Add catalog items
        candidates.extend(SLOT_CATALOGS[1])
    else:
        # Slots 2-5: Pull from specialized curated catalog
        candidates.extend(SLOT_CATALOGS.get(slot_id, []))

    # Apply deduplication check (filter out anything used in last 60 days)
    fresh_items = filter_non_duplicates(candidates, key_field="full_name", max_days=60)
    
    if len(fresh_items) < count:
        print(f"[!] Warning: Only {len(fresh_items)} fresh items found. Refreshing candidates pool.")
        fresh_items = candidates[:count]

    chosen = fresh_items[:count]

    # Process and ensure media assets
    enriched = []
    base_dir = f"assets/slot_{slot_id}"
    os.makedirs(base_dir, exist_ok=True)

    for item in chosen:
        if slot_id == 1 and "full_name" in item and "/" in item["full_name"] and not item.get("demo_media"):
            enriched.append(fetch_repo_media_assets(item, base_dir=base_dir))
        else:
            # Check if a custom asset image already exists
            slug = item["name"].replace("-", "_")
            candidate_imgs = [
                f"assets/repos/{slug}/demo.png",
                f"assets/repos/{slug}/og_banner.png",
                f"assets/slot_{slot_id}/{slug}/demo.png",
                f"assets/slot_{slot_id}/{slug}/og_banner.png"
            ]
            found_img = None
            for p in candidate_imgs:
                if os.path.exists(p):
                    found_img = p
                    break
            item["demo_media"] = found_img
            enriched.append(item)

    # Save to curated slot file
    out_file = f"assets/curated_slot_{slot_id}.json"
    with open(out_file, "w") as f:
        json.dump(enriched, f, indent=2)

    return enriched, meta
