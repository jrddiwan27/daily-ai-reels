import os
import sys
import json
import subprocess
from pipeline.repo_asset_scraper import scrape_and_cache_all
from pipeline.fish_audio_client import generate_voiceover, generate_caption_chunks
from pipeline.composition_compiler import build_hyperframes_composition
from pipeline.buffer_dispatcher import dispatch_to_buffer

def run_daily_pipeline():
    print("=" * 60)
    print("🚀 LAUNCHING AUTONOMOUS DAILY VIDEO ENGINE")
    print("=" * 60)

    # 1. Scrape trending repos & download real media assets
    print("\n[STEP 1/5] Scraping Trending Repos & Real Media Assets...")
    repos = scrape_and_cache_all(limit=5)
    print(f"[✓] Curated {len(repos)} repositories with real images & demos.")

    # 2. Build voiceover script
    script_text = (
        f"Stop paying for expensive AI subscriptions. "
        f"Here are five insane open-source GitHub repos every developer needs right now. "
        f"First is {repos[0]['name']}, {repos[0]['description']} "
        f"Second is {repos[1]['name']}, {repos[1]['description']} "
        f"Third is {repos[2]['name']}, {repos[2]['description']} "
        f"Fourth is {repos[3]['name']}, {repos[3]['description']} "
        f"And fifth is {repos[4]['name']}, {repos[4]['description']} "
        f"Comment REPOS below and I'll send you the direct links right away."
    )

    # 3. Generate Fish Audio Voiceover & Captions
    print("\n[STEP 2/5] Synthesizing Voiceover with Fish Audio (S2.1 Pro Free)...")
    audio_path = "assets/voice.mp3"
    captions_path = "assets/caption_chunks.json"
    
    try:
        dur = generate_voiceover(script_text, audio_path)
    except Exception as e:
        print(f"[!] Fish Audio failed ({e}), falling back to Edge-TTS...")
        cmd = f'edge-tts --voice en-US-ChristopherNeural --text "{script_text}" --write-media {audio_path}'
        subprocess.check_call(cmd, shell=True)
        dur = 60.9
        
    generate_caption_chunks(script_text, dur, captions_path)

    # 4. Compile Composition
    print("\n[STEP 3/5] Compiling HyperFrames Code Composition...")
    build_hyperframes_composition(
        repos_file="assets/curated_repos.json",
        captions_file=captions_path,
        audio_path=audio_path,
        output_html="index.html"
    )

    # 5. Render Video via HyperFrames
    print("\n[STEP 4/5] Rendering High-Definition MP4 Video...")
    out_mp4 = "out/daily-reel.mp4"
    os.makedirs("out", exist_ok=True)
    
    render_cmd = f"npx hyperframes render -o {out_mp4}"
    print(f"[*] Executing: {render_cmd}")
    res = subprocess.call(render_cmd, shell=True)
    
    if res != 0 or not os.path.exists(out_mp4):
        print("[!] Video render had warnings or exited. Checking output...")
    else:
        print(f"[✓] Render Complete: {out_mp4} ({os.path.getsize(out_mp4)} bytes)")

    # 6. Dispatch to Buffer
    print("\n[STEP 5/5] Dispatching to Buffer for Auto-Publishing...")
    caption = (
        f"5 Insane Open-Source AI Developer Repos You Need Today! 🚀\n\n"
        f"1. {repos[0]['name']}\n2. {repos[1]['name']}\n3. {repos[2]['name']}\n"
        f"4. {repos[3]['name']}\n5. {repos[4]['name']}\n\n"
        f"Comment 'REPOS' and I'll DM you all 5 links!\n"
        f"#developer #ai #opensource #github #coding #programming #webdev"
    )
    dispatch_to_buffer(out_mp4, caption)

    print("\n" + "=" * 60)
    print("✨ DAILY PIPELINE EXECUTION COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    run_daily_pipeline()
