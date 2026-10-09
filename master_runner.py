import os
import sys
import json
import argparse
import subprocess
from pipeline.slot_content_engine import detect_current_slot, fetch_content_for_slot
from pipeline.creator_radar import fetch_creator_trending_transcripts
from pipeline.ai_scriptwriter import generate_viral_script_with_gemini
from pipeline.fish_audio_client import generate_voiceover, generate_caption_chunks
from pipeline.audio_enhancer import produce_master_audio
from pipeline.composition_compiler import build_hyperframes_composition
from pipeline.buffer_dispatcher import dispatch_to_buffer, dispatch_to_all_platforms
from pipeline.dedup_manager import record_published
from pipeline.blog_engine import generate_blog_article

def run_pipeline(slot_id: int = None, dry_run: bool = False):
    if slot_id is None:
        slot_id = detect_current_slot()

    print("=" * 65)
    print(f"🚀 LAUNCHING 5X DAILY REEL ENGINE — SLOT {slot_id}/5")
    print("=" * 65)

    # 1. Fetch 3 fresh, guaranteed non-duplicate items for this slot
    print(f"\n[STEP 1/7] Curating 3 Non-Duplicate Items for Slot {slot_id}...")
    items, meta = fetch_content_for_slot(slot_id, count=3)
    curated_file = f"assets/curated_slot_{slot_id}.json"
    print(f"[✓] Curated {len(items)} items for: {meta['slot_name']}")
    for it in items:
        print(f"    • {it.get('full_name') or it.get('name')}: {it.get('description', '')[:70]}...")

    # 2. Creator Radar: Monitor top tech creator formats
    print("\n[STEP 2/7] Scanning Reference Creator Formats...")
    try:
        trends = fetch_creator_trending_transcripts(limit_creators=3)
    except Exception as e:
        print(f"[!] Creator radar warning: {e}")
        trends = []

    # 3. AI Scriptwriter: Craft viral script with Gemini tailored to slot & CTA
    print(f"\n[STEP 3/7] Generating High-Retention Script (Target: 95-105 words, CTA: '{meta['cta_keyword']}')...")
    script_data = generate_viral_script_with_gemini(items, trends, slot_meta=meta)
    script_text = script_data["full_script"]

    with open("assets/generated_script.json", "w") as f:
        json.dump(script_data, f, indent=2)

    print(f"\n[Voiceover Script]:\n\"{script_text}\"\n")

    # 4. Synthesize Voiceover & Captions with Fish Audio (or Edge-TTS fallback)
    print("\n[STEP 4/7] Synthesizing Voiceover with Fish Audio (S2.1 Pro)...")
    audio_path = "assets/voice.mp3"
    captions_path = "assets/caption_chunks.json"

    try:
        dur = generate_voiceover(script_text, audio_path)
    except Exception as e:
        print(f"[!] Fish Audio fallback to Edge-TTS: {e}")
        cmd = f'edge-tts --voice en-US-ChristopherNeural --text "{script_text}" --write-media {audio_path}'
        subprocess.check_call(cmd, shell=True)
        dur = 38.0

    print(f"[✓] Exact Voice Duration: {dur:.2f}s (Pacing: <50s broadcast target)")
    generate_caption_chunks(script_text, dur, captions_path)

    # 5. Compile Hyper-Motion Code Composition
    print("\n[STEP 5/7] Compiling Hyper-Motion Code Composition (720x1280 @ 60fps)...")
    build_hyperframes_composition(
        repos_file=curated_file,
        captions_file=captions_path,
        audio_path=audio_path,
        script_file="assets/generated_script.json",
        duration=dur,
        output_html="index.html",
        slot_meta=meta
    )

    # 6. Render MP4 Video via HyperFrames & Multiplex Ducked Audio
    print("\n[STEP 6/7] Rendering High-Definition MP4 Video...")
    raw_mp4 = "out/raw_video.mp4"
    out_mp4 = "out/daily-reel.mp4"
    os.makedirs("out", exist_ok=True)

    render_cmd = f"npx hyperframes render -o {raw_mp4}"
    print(f"[*] Executing: {render_cmd}")
    subprocess.check_call(render_cmd, shell=True)

    print(f"[*] Multiplexing broadcast master audio (voice + SFX + ducked BGM)...")
    master_audio = produce_master_audio(voice_path=audio_path, duration=dur)

    mux_cmd = f"ffmpeg -y -i {raw_mp4} -i {master_audio} -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -shortest {out_mp4}"
    subprocess.check_call(mux_cmd, shell=True)

    if not os.path.exists(out_mp4):
        raise RuntimeError("Final video generation failed.")

    file_size = os.path.getsize(out_mp4)
    print(f"[✓] Final Video Generated: {out_mp4} ({round(file_size/1024/1024, 2)} MB)")

    # 7. Auto-Publish to Buffer across Instagram, YouTube Shorts & X
    post_ids = {}
    if not dry_run:
        print("\n[STEP 7/8] Dispatching across Instagram Reels, YouTube Shorts & X...")
        post_ids = dispatch_to_all_platforms(out_mp4, meta, items)
    else:
        print("\n[STEP 7/8] Dry-run mode enabled. Skipping multi-platform dispatch.")

    # 8. Update Autonomous AI Blog & Hub
    print("\n[STEP 8/8] Updating Autonomous AI Blog & Hub (docs/)...")
    generate_blog_article(slot_id, meta, items, script_data)

    # Record in deduplication ledger to guarantee no repeats
    primary_id = post_ids.get("instagram") or "scheduled"
    record_published(slot_id, meta["slot_name"], items, post_id=primary_id)

    print("\n" + "=" * 65)
    print(f"✨ COMPLETED 5X PIPELINE FOR SLOT {slot_id} ({meta['slot_name']})")
    print("=" * 65)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous 5x Daily AI Reel Engine")
    parser.add_argument("--slot", type=int, choices=[1, 2, 3, 4, 5], help="Slot number (1-5). Auto-detected if omitted.")
    parser.add_argument("--dry-run", action="store_true", help="Render video and update ledger without pushing to Buffer.")
    args = parser.parse_args()

    run_pipeline(slot_id=args.slot, dry_run=args.dry_run)
