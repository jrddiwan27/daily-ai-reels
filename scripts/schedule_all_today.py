"""
Multi-Slot Production & Scheduling Coordinator:
Executes the 7-Agent Engine for each pending/upcoming slot:
- Slot 2 (12:00 PM IST): Post Now
- Slot 3 (3:00 PM IST): Schedule for 09:30 UTC
- Slot 4 (6:00 PM IST): Schedule for 12:30 UTC
- Slot 5 (9:00 PM IST): Schedule for 15:30 UTC
"""

import os
import sys
import json
import time
import datetime

# Ensure project root is in python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from agents.pipeline_orchestrator import run_production_pipeline, SLOT_CONFIGS
from pipeline.buffer_dispatcher import dispatch_to_all_platforms

SCHEDULE_PLAN = [
    {
        "slot_id": 2,
        "name": "Midday Cheat Code",
        "theme": "autonomous AI automation workflows 2026",
        "cta": "WORKFLOW",
        "due_at_utc": None, # Post immediately (Makeup for 12 PM)
        "time_ist": "12:00 PM (Instant Makeup Post)"
    },
    {
        "slot_id": 3,
        "name": "Tech Radar Teardown",
        "theme": "new open weights multimodal reasoning AI models",
        "cta": "MODELS",
        "due_at_utc": "2026-10-12T09:30:00.000Z", # 3:00 PM IST
        "time_ist": "3:00 PM IST"
    },
    {
        "slot_id": 4,
        "name": "Evening Toolkit",
        "theme": "secret web AI developer productivity tools 2026",
        "cta": "TOOLS",
        "due_at_utc": "2026-10-12T12:30:00.000Z", # 6:00 PM IST
        "time_ist": "6:00 PM IST"
    },
    {
        "slot_id": 5,
        "name": "Night Owl Deep Dive",
        "theme": "advanced prompt engineering frameworks architectures 2026",
        "cta": "PROMPT",
        "due_at_utc": "2026-10-12T15:30:00.000Z", # 9:00 PM IST
        "time_ist": "9:00 PM IST"
    }
]

def produce_and_dispatch_slot(plan_item):
    slot_id = plan_item["slot_id"]
    theme = plan_item["theme"]
    cta = plan_item["cta"]
    due_at = plan_item["due_at_utc"]
    time_ist = plan_item["time_ist"]

    print("================================================================================")
    print(f"🎬 PROCESSING SLOT {slot_id}: {plan_item['name']} ({time_ist})")
    print("================================================================================")

    # 1. Run full 7-agent pipeline
    verdict = run_production_pipeline(slot_id=slot_id, theme_focus=theme, cta_keyword=cta)
    video_path = verdict["video_path"]

    # 2. Load generated dossier & script
    with open("assets/research_dossier.json") as f:
        dossier = json.load(f)
    items = dossier.get("items", [])
    for it in items:
        if "name" not in it:
            it["name"] = it["title"].split("·")[0].split("–")[0].split(":")[0].strip()

    with open("assets/viral_script.json") as f:
        script = json.load(f)

    meta = {
        "slot_id": slot_id,
        "slot_name": f"{plan_item['name']} (Slot {slot_id})",
        "cta_keyword": cta,
        "post_title": script.get("hook", f"Top 3 AI Breakthroughs for {plan_item['name']}!"),
        "hashtags": ["#ai", "#automation", "#tech", "#softwareengineer", "#workflow"]
    }

    # 3. Dispatch to Buffer across all platforms
    print(f"\n[*] Dispatching to all platforms (Scheduled: {due_at or 'SHARE NOW'})...")
    results = dispatch_to_all_platforms(video_path, meta, items, due_at_utc=due_at)

    # 4. Record in published history
    hist_entry = {
        "slot_id": slot_id,
        "slot_name": meta["slot_name"],
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "date_ist": f"2026-10-12 {time_ist}",
        "buffer_post_id": results.get("instagram", "scheduled"),
        "channel_results": results,
        "video_path": video_path,
        "items": items
    }

    os.makedirs("history", exist_ok=True)
    history = []
    if os.path.exists("history/published_history.json"):
        try:
            with open("history/published_history.json") as f:
                history = json.load(f)
        except Exception:
            history = []

    history.append(hist_entry)
    with open("history/published_history.json", "w") as f:
        json.dump(history, f, indent=2)

    print(f"\n[✓] Slot {slot_id} ({time_ist}) Complete and Dispatched/Scheduled: {results}")
    return hist_entry

if __name__ == "__main__":
    for item in SCHEDULE_PLAN:
        produce_and_dispatch_slot(item)
