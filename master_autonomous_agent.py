import os
import sys
import time
import json
import datetime
import argparse
from dotenv import load_dotenv

load_dotenv()

from master_runner import run_pipeline
from pipeline.omni_intelligence_radar import scan_breaking_ai_radar_omni
from pipeline.video_recreator import process_inbox
from pipeline.dedup_manager import is_duplicate, record_published
from pipeline.quality_evaluator import evaluate_video_quality

TRACKER_FILE = "history/slot_schedule_tracker.json"

SLOT_SCHEDULE_IST = {
    1: 9,   # 09:00 AM IST
    2: 12,  # 12:00 PM IST
    3: 15,  # 03:00 PM IST
    4: 18,  # 06:00 PM IST
    5: 21   # 09:00 PM IST
}

def get_ist_now():
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    return utc_now + datetime.timedelta(hours=5, minutes=30)

def load_tracker():
    os.makedirs("history", exist_ok=True)
    if os.path.exists(TRACKER_FILE):
        try:
            with open(TRACKER_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_tracker(tracker):
    os.makedirs("history", exist_ok=True)
    with open(TRACKER_FILE, "w") as f:
        json.dump(tracker, f, indent=2)

def check_scheduled_slots(dry_run: bool = False):
    """
    Checks if current IST time falls into one of the 5 daily posting windows
    and triggers the pipeline if not yet executed today.
    """
    ist = get_ist_now()
    today_str = ist.strftime("%Y-%m-%d")
    hour = ist.hour

    tracker = load_tracker()
    today_runs = tracker.get(today_str, [])

    # Check which slot matches the current hour
    current_slot = None
    for slot_id, scheduled_hour in SLOT_SCHEDULE_IST.items():
        # Trigger window: within the scheduled hour or subsequent hour before next slot
        if hour >= scheduled_hour:
            # Check if this slot was already run today
            if slot_id not in today_runs:
                current_slot = slot_id

    if current_slot:
        print(f"\n[⏰ 24/7 SENTINEL] Scheduled Drop Triggered: Slot {current_slot}/5 ({today_str} @ {ist.strftime('%H:%M')} IST)")
        try:
            run_pipeline(slot_id=current_slot, dry_run=dry_run)
            today_runs.append(current_slot)
            tracker[today_str] = today_runs
            save_tracker(tracker)
            print(f"[✓] Slot {current_slot} completed and recorded in tracker.")
        except Exception as e:
            print(f"[❌] Error executing Slot {current_slot}: {e}")
    else:
        print(f"[*] Schedule Check: All due slots up to hour {hour}:00 IST are already published for {today_str}.")

def check_breaking_news(dry_run: bool = False):
    """
    Scans for breaking viral AI spikes (score >= 85).
    If a major drop (like Qwen open-sourcing image model, DeepSeek release, etc.) occurs,
    triggers an immediate Breaking Edition!
    """
    print("\n[*] 24/7 AI Radar: Scanning for breaking AI spikes...")
    try:
        breaking_items = scan_breaking_ai_radar_omni()
    except Exception as e:
        print(f"[!] Breaking radar scan warning: {e}")
        return

    for item in breaking_items:
        score = item.get("score", 0)
        title = item.get("title", "")
        if score >= 85 and not is_duplicate(title, max_days=30):
            print(f"\n🔥 [BREAKING AI SPIKE DETECTED] Score {score}/100: '{title}'")
            print("[*] Launching immediate Breaking Edition production...")
            try:
                # Use Slot 1 or Slot 3 template for breaking model releases
                slot_id = 1 if "model" in title.lower() or "weight" in title.lower() or "open" in title.lower() else 3
                meta = {
                    "slot_id": slot_id,
                    "slot_name": f"BREAKING: {title[:40]}",
                    "badge_title": "BREAKING AI",
                    "badge_sub": "HIGH IMPACT RELEASE",
                    "hook_theme": "breaking",
                    "cta_keyword": "BREAKING",
                    "hashtags": ["#breakingnews", "#ai", "#tech", "#innovation", "#future"],
                    "post_title": f"🚨 BREAKING AI DROP: {title}!"
                }
                # Run pipeline with the breaking item as primary
                from pipeline.ai_scriptwriter import generate_viral_script_with_gemini
                from pipeline.fish_audio_client import generate_voiceover, generate_caption_chunks
                from pipeline.audio_enhancer import produce_master_audio
                from pipeline.composition_compiler import build_hyperframes_composition
                from pipeline.buffer_dispatcher import dispatch_to_all_platforms
                import glob, subprocess

                single_item = [{
                    "name": item.get("title", "")[:25],
                    "full_name": item.get("title", ""),
                    "description": item.get("description", "") or "Breaking AI release open-sourced to the world.",
                    "url": item.get("url", ""),
                    "badge": "BREAKING"
                }]

                script_data = generate_viral_script_with_gemini(single_item, [], slot_meta=meta)
                script_text = script_data["full_script"]
                audio_path = "assets/voice.mp3"
                captions_path = "assets/caption_chunks.json"

                dur = generate_voiceover(script_text, audio_path)
                generate_caption_chunks(script_text, dur, captions_path)

                curated_file = "assets/breaking_curated.json"
                with open(curated_file, "w") as cf:
                    json.dump(single_item * 3, cf)

                build_hyperframes_composition(
                    repos_file=curated_file,
                    captions_file=captions_path,
                    audio_path=audio_path,
                    script_file="assets/generated_script.json",
                    duration=dur,
                    slot_meta=meta
                )

                raw_mp4 = "out/raw_video.mp4"
                out_mp4 = "out/daily-reel.mp4"
                subprocess.check_call(f"npx --yes hyperframes render -o {raw_mp4}", shell=True)
                master_audio = produce_master_audio(voice_path=audio_path, duration=dur)
                temp_main = "out/temp_main.mp4"
                subprocess.check_call(f"ffmpeg -y -i {raw_mp4} -i {master_audio} -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -ar 44100 -ac 2 -shortest {temp_main}", shell=True)

                # Attach rotating CTA
                cta_files = sorted(glob.glob("assets/cta/cta_*.mp4"))
                if cta_files:
                    chosen_cta = cta_files[0]
                    concat_list = "out/concat_list.txt"
                    with open(concat_list, "w") as f:
                        f.write(f"file '{os.path.abspath(temp_main)}'\nfile '{os.path.abspath(chosen_cta)}'\n")
                    subprocess.check_call(f"ffmpeg -y -f concat -safe 0 -i {concat_list} -c:v copy -c:a aac -b:a 192k -ar 44100 -ac 2 {out_mp4}", shell=True)
                else:
                    os.rename(temp_main, out_mp4)

                # Quality audit
                q_res = evaluate_video_quality(out_mp4, expected_duration=dur)
                print(f"[✓] Breaking Video Quality Score: {q_res['score']}/100")

                # Dispatch
                if not dry_run:
                    dispatch_to_all_platforms(out_mp4, meta, single_item)
                record_published(slot_id, meta["slot_name"], single_item, post_id="breaking_published")
                print(f"[✓] Published breaking news edition on: {title}")
                break
            except Exception as e:
                print(f"[❌] Error creating breaking news edition: {e}")

def run_agent_cycle(dry_run: bool = False):
    """Runs a single 360-degree autonomous audit cycle."""
    ist = get_ist_now()
    print("=" * 70)
    print(f"🤖 JDS 24/7 AUTONOMOUS AGENT CYCLE · {ist.strftime('%Y-%m-%d %H:%M:%S')} IST")
    print("=" * 70)

    # 1. Check User Inbox for dropped videos or URLs
    print("\n[1/3] Checking Video Inbox...")
    try:
        process_inbox()
    except Exception as e:
        print(f"[!] Inbox check warning: {e}")

    # 2. Check 5x Daily Schedule Slots
    print("\n[2/3] Checking 5x Daily Slot Schedule...")
    check_scheduled_slots(dry_run=dry_run)

    # 3. Check Breaking AI News Radar
    print("\n[3/3] Checking 24/7 Breaking AI Radar...")
    check_breaking_news(dry_run=dry_run)

    print("\n[✓] Agent cycle complete. System standing by.")

def run_continuous_daemon(poll_interval_seconds: int = 900, dry_run: bool = False):
    """
    Runs continuously 24/7 as a background daemon, polling every 15 minutes.
    """
    print("=" * 70)
    print("🚀 STARTING JDS 24/7 AUTONOMOUS PRODUCTION DAEMON")
    print(f"⏱️ Polling interval: {poll_interval_seconds} seconds ({round(poll_interval_seconds/60)} minutes)")
    print("=" * 70)

    while True:
        try:
            run_agent_cycle(dry_run=dry_run)
        except Exception as e:
            print(f"[!] Cycle exception caught: {e}")
        time.sleep(poll_interval_seconds)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jayant Digital Studio 24/7 Autonomous Agent")
    parser.add_argument("--daemon", action="store_true", help="Run continuously in background (default poll 15m)")
    parser.add_argument("--interval", type=int, default=900, help="Daemon polling interval in seconds (default: 900)")
    parser.add_argument("--dry-run", action="store_true", help="Run without posting to Buffer")
    args = parser.parse_args()

    if args.daemon:
        run_continuous_daemon(poll_interval_seconds=args.interval, dry_run=args.dry_run)
    else:
        run_agent_cycle(dry_run=args.dry_run)
