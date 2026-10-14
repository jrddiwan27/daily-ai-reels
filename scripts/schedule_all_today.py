"""
Multi-Slot Production & Scheduling Coordinator:
Executes the upgraded 7-Agent Production Engine for each pending slot:
- Slot 2 (12:00 PM IST): Post Now (Instant Makeup Post)
- Slot 3 (3:00 PM IST): Schedule for 5:30 PM IST (12:00 UTC)
- Slot 4 (6:00 PM IST): Schedule for 6:00 PM IST (12:30 UTC)
- Slot 5 (9:00 PM IST): Schedule for 9:00 PM IST (15:30 UTC)
"""

import os
import sys
import json
import time
import datetime
import subprocess

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from agents.pipeline_orchestrator import run_production_pipeline
from pipeline.buffer_dispatcher import dispatch_to_all_platforms

def get_daily_schedule_plan():
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    ist_offset = datetime.timedelta(hours=5, minutes=30)
    now_ist = now_utc + ist_offset
    today_ist_str = now_ist.strftime("%Y-%m-%d")

    slots_def = [
        {
            "slot_id": 1,
            "name": "Morning Breakthrough",
            "theme": "open source AI developer tools GitHub 2026",
            "cta": "REPOS",
            "hour_ist": 9,
            "minute_ist": 0,
            "time_ist": "9:00 AM IST"
        },
        {
            "slot_id": 2,
            "name": "Midday Cheat Code",
            "theme": "autonomous AI automation workflows 2026",
            "cta": "WORKFLOW",
            "hour_ist": 12,
            "minute_ist": 0,
            "time_ist": "12:00 PM IST"
        },
        {
            "slot_id": 3,
            "name": "Tech Radar Teardown",
            "theme": "new open weights multimodal reasoning AI models",
            "cta": "MODELS",
            "hour_ist": 15,
            "minute_ist": 0,
            "time_ist": "3:00 PM IST"
        },
        {
            "slot_id": 4,
            "name": "Evening Toolkit",
            "theme": "secret web AI developer productivity tools 2026",
            "cta": "TOOLS",
            "hour_ist": 18,
            "minute_ist": 0,
            "time_ist": "6:00 PM IST"
        },
        {
            "slot_id": 5,
            "name": "Night Owl Deep Dive",
            "theme": "advanced prompt engineering frameworks architectures 2026",
            "cta": "PROMPT",
            "hour_ist": 21,
            "minute_ist": 0,
            "time_ist": "9:00 PM IST"
        }
    ]

    plan = []
    for s in slots_def:
        target_ist = datetime.datetime(
            now_ist.year, now_ist.month, now_ist.day,
            s["hour_ist"], s["minute_ist"], 0,
            tzinfo=datetime.timezone(ist_offset)
        )
        target_utc = target_ist.astimezone(datetime.timezone.utc)

        # Allow a 15-minute grace window for scheduling
        if now_utc >= (target_utc - datetime.timedelta(minutes=10)):
            due_at_utc = None
            status_desc = f"{s['time_ist']} (Immediate / Makeup)"
        else:
            due_at_utc = target_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            status_desc = f"{s['time_ist']} (Scheduled for {target_utc.strftime('%H:%M')} UTC)"

        plan.append({
            "slot_id": s["slot_id"],
            "name": s["name"],
            "theme": s["theme"],
            "cta": s["cta"],
            "due_at_utc": due_at_utc,
            "time_ist": status_desc,
            "today_date": today_ist_str
        })
    return plan

def is_slot_already_published_today(slot_id, today_date_str):
    hist_path = "history/published_history.json"
    if not os.path.exists(hist_path):
        return False
    try:
        with open(hist_path) as f:
            hist = json.load(f)
        for h in hist:
            h_date = str(h.get("date_ist", ""))
            h_time = str(h.get("timestamp_utc", ""))
            if h.get("slot_id") == slot_id and (today_date_str in h_date or today_date_str in h_time):
                # Verify that it was successfully dispatched
                if h.get("buffer_post_id") or h.get("channel_results"):
                    return True
    except Exception:
        pass
    return False

def produce_and_dispatch_slot(plan_item):
    slot_id = plan_item["slot_id"]
    theme = plan_item["theme"]
    cta = plan_item["cta"]
    due_at = plan_item["due_at_utc"]
    time_ist = plan_item["time_ist"]

    print("================================================================================")
    print(f"🎬 PROCESSING SLOT {slot_id}: {plan_item['name']} ({time_ist})")
    print("================================================================================")

    # 1. Run full 7-agent pipeline (or reuse recent render if fresh)
    final_reel = f"out/slot_{slot_id}_daily_reel.mp4"
    if os.path.exists(final_reel) and (time.time() - os.path.getmtime(final_reel) < 1800):
        print(f"[*] Found fresh existing reel for Slot {slot_id} ({final_reel}), reusing verified render...")
        raw_video = final_reel
    else:
        verdict = run_production_pipeline(slot_id=slot_id, theme_focus=theme, cta_keyword=cta)
        raw_video = verdict["video_path"]

    # Optimize video for high-speed CDN and mobile streaming
    opt_video = raw_video.replace(".mp4", "_opt.mp4")
    print(f"[*] Optimizing video for mobile delivery: {opt_video}...")
    opt_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        opt_video
    ]
    subprocess.run(opt_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    video_to_dispatch = opt_video if os.path.exists(opt_video) else raw_video

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
    results = dispatch_to_all_platforms(video_to_dispatch, meta, items, due_at_utc=due_at)

    # 4. Record in published history
    today_str = plan_item.get("today_date", datetime.date.today().isoformat())
    hist_entry = {
        "slot_id": slot_id,
        "slot_name": meta["slot_name"],
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "date_ist": f"{today_str} {time_ist}",
        "buffer_post_id": results.get("instagram", "scheduled"),
        "channel_results": results,
        "video_path": video_to_dispatch,
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
    force = "--force" in sys.argv or os.environ.get("FORCE_RESCHEDULE") == "1"
    target_slot = None
    for arg in sys.argv:
        if arg.startswith("--slot="):
            try:
                target_slot = int(arg.split("=")[1])
            except ValueError:
                pass

    plan = get_daily_schedule_plan()
    print("=" * 80)
    print(f"🚀 EXECUTING DAILY AUTOMATION ENGINE — {plan[0]['today_date']} (Force: {force})")
    print("=" * 80)
    for item in plan:
        slot_id = item["slot_id"]
        if target_slot is not None and slot_id != target_slot:
            continue
        today_date = item["today_date"]
        if not force and is_slot_already_published_today(slot_id, today_date):
            print(f"[*] Slot {slot_id} ({item['name']}) has already been dispatched today ({today_date}). Skipping.")
            continue
        produce_and_dispatch_slot(item)
