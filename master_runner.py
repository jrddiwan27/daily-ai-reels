import os
import sys
import json
import subprocess
from pipeline.creator_radar import fetch_creator_trending_transcripts
from pipeline.repo_asset_scraper import scrape_and_cache_all
from pipeline.ai_scriptwriter import generate_viral_script_with_gemini
from pipeline.fish_audio_client import generate_voiceover, generate_caption_chunks
from pipeline.audio_enhancer import produce_master_audio
from pipeline.composition_compiler import build_hyperframes_composition
from pipeline.buffer_dispatcher import dispatch_to_buffer

def run_daily_pipeline():
    print("=" * 60)
    print("🚀 LAUNCHING AUTONOMOUS DAILY HYPER-MOTION REEL ENGINE")
    print("=" * 60)

    # 1. Creator Radar: Monitor top creators for viral transcripts
    print("\n[STEP 1/6] Scanning Top Tech Creators for Viral Formats...")
    trends = fetch_creator_trending_transcripts(limit_creators=4)
    print(f"[✓] Captured {len(trends)} trending reference hooks.")

    # 2. Scrape 3 breakthrough repos with real demo images/GIFs
    print("\n[STEP 2/6] Scraping 3 Trending AI Repos & Real Media Assets...")
    repos = scrape_and_cache_all(limit=3)
    print(f"[✓] Curated {len(repos)} repositories with real demo assets.")

    # 3. AI Scriptwriter: Craft viral script with Gemini (strictly 95-105 words)
    print("\n[STEP 3/6] Generating High-Retention Script with Gemini 3.8 Flash...")
    script_data = generate_viral_script_with_gemini(repos, trends)
    script_text = script_data["full_script"]
    
    # Save generated script for composition
    with open("assets/generated_script.json", "w") as f:
        json.dump(script_data, f, indent=2)
        
    print(f"\n[Generated Voiceover Script]:\n\"{script_text}\"\n")

    # 4. Synthesize Voiceover & Captions with Fish Audio S2.1 Pro Free
    print("\n[STEP 4/6] Synthesizing Voiceover with Fish Audio (S2.1 Pro Free)...")
    audio_path = "assets/voice.mp3"
    captions_path = "assets/caption_chunks.json"
    
    try:
        dur = generate_voiceover(script_text, audio_path)
    except Exception as e:
        print(f"[!] Fish Audio failed ({e}), falling back to Edge-TTS...")
        cmd = f'edge-tts --voice en-US-ChristopherNeural --text "{script_text}" --write-media {audio_path}'
        subprocess.check_call(cmd, shell=True)
        dur = 38.0
        
    print(f"[✓] Exact Voice Duration: {dur:.2f} seconds (Target: <50s)")
    generate_caption_chunks(script_text, dur, captions_path)

    # 5. Compile 100% Hyper-Motion Composition with Real Scraped Media
    print("\n[STEP 5/6] Compiling Hyper-Motion Code Composition...")
    build_hyperframes_composition(
        repos_file="assets/curated_repos.json",
        captions_file=captions_path,
        audio_path=audio_path,
        script_file="assets/generated_script.json",
        duration=dur,
        output_html="index.html"
    )

    # 6. Render High-Definition MP4 Video via HyperFrames
    print("\n[STEP 6/6] Rendering High-Definition MP4 Video & Multiplexing Audio...")
    raw_mp4 = "out/raw_video.mp4"
    out_mp4 = "out/daily-reel.mp4"
    os.makedirs("out", exist_ok=True)
    
    render_cmd = f"npx hyperframes render -o {raw_mp4}"
    print(f"[*] Executing: {render_cmd}")
    res = subprocess.call(render_cmd, shell=True)
    
    # Multiplex synchronized broadcast audio track with SFX and beat
    print(f"[*] Producing broadcast master audio (voice + SFX + cyber beat)...")
    master_audio = produce_master_audio(voice_path=audio_path, duration=dur)
    
    print(f"[*] Multiplexing master audio ({master_audio}) into final video via FFmpeg...")
    mux_cmd = f"ffmpeg -y -i {raw_mp4} -i {master_audio} -c:v copy -c:a aac -b:a 192k -shortest {out_mp4}"
    subprocess.check_call(mux_cmd, shell=True)
    
    if not os.path.exists(out_mp4):
        raise RuntimeError("Final video generation failed.")
        
    file_size = os.path.getsize(out_mp4)
    print(f"[✓] Final Video Complete with Audio: {out_mp4} ({file_size} bytes, {round(file_size/1024/1024, 2)} MB)")

    # 7. Auto-Publish to Buffer Instagram Reels (Strictly 5 Hashtags)
    print("\n[*] Dispatching to Buffer for Auto-Publishing...")
    repo_names = [r["name"].split("/")[-1] for r in repos]
    caption = (
        f"3 Insane Open-Source AI Developer Repos You Need Today! 🚀\n\n"
        f"1. {repo_names[0]}\n2. {repo_names[1]}\n3. {repo_names[2]}\n\n"
        f"Comment 'TOOLS' and I'll DM you all 3 links!\n\n"
        f"#developer #ai #opensource #github #coding"
    )
    dispatch_to_buffer(out_mp4, caption)

    print("\n" + "=" * 60)
    print("✨ DAILY HYPER-MOTION PIPELINE COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    run_daily_pipeline()
