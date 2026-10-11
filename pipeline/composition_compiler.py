import os
import json
import re
import math
import subprocess
from pipeline.lipsync_engine import generate_lipsync_data

SLOT_VISUAL_THEMES = {
    1: {
        "accent": "#d9694a",       # Brand Clay Orange
        "accent_light": "#ff8c69",
        "bg_blob1": "#f6c6b0",
        "bg_blob2": "#cfd2f3",
        "bg_blob3": "#f9d9c4",
        "badge_bg": "#1a1714",
        "badge_fg": "#ffffff",
        "hoodie_color": "#1f2937",
        "hoodie_trim": "#d9694a",
        "desk_color": "#855132",
        "mug_color": "#d9694a",
        "tagline": "Open Source Superpowers"
    },
    2: {
        "accent": "#2563eb",       # Electric Blue
        "accent_light": "#60a5fa",
        "bg_blob1": "#bfdbfe",
        "bg_blob2": "#ddd6fe",
        "bg_blob3": "#c7d2fe",
        "badge_bg": "#1e3a8a",
        "badge_fg": "#ffffff",
        "hoodie_color": "#1e293b",
        "hoodie_trim": "#3b82f6",
        "desk_color": "#633c1d",
        "mug_color": "#2563eb",
        "tagline": "Automated AI Workflows"
    },
    3: {
        "accent": "#7c3aed",       # Deep Purple
        "accent_light": "#a78bfa",
        "bg_blob1": "#e9d5ff",
        "bg_blob2": "#fbcfe8",
        "bg_blob3": "#ddd6fe",
        "badge_bg": "#4c1d95",
        "badge_fg": "#ffffff",
        "hoodie_color": "#0f172a",
        "hoodie_trim": "#8b5cf6",
        "desk_color": "#78431e",
        "mug_color": "#7c3aed",
        "tagline": "Model Benchmark Teardown"
    },
    4: {
        "accent": "#059669",       # Emerald Green
        "accent_light": "#34d399",
        "bg_blob1": "#a7f3d0",
        "bg_blob2": "#bae6fd",
        "bg_blob3": "#d1fae5",
        "badge_bg": "#064e3b",
        "badge_fg": "#ffffff",
        "hoodie_color": "#1e293b",
        "hoodie_trim": "#10b981",
        "desk_color": "#855132",
        "mug_color": "#059669",
        "tagline": "Secret Web AI Websites"
    },
    5: {
        "accent": "#ef4444",       # Crimson Red
        "accent_light": "#f87171",
        "bg_blob1": "#fecaca",
        "bg_blob2": "#fed7aa",
        "bg_blob3": "#fee2e2",
        "badge_bg": "#7f1d1d",
        "badge_fg": "#ffffff",
        "hoodie_color": "#111827",
        "hoodie_trim": "#f87171",
        "desk_color": "#603418",
        "mug_color": "#ef4444",
        "tagline": "Senior Prompt Architecture"
    }
}

def build_hyperframes_composition(
    repos_file="assets/curated_repos.json",
    captions_file="assets/caption_chunks.json",
    audio_path="assets/voice.mp3",
    script_file="assets/generated_script.json",
    duration=40.0,
    output_html="index.html",
    slot_meta=None
):
    """
    Next-Gen Hyper-Paced Motion Composition Engine:
    - UPPER THEATER (Y: 40px to 1120px): 10 Hyper-Motion Micro-Scenes (every 3.2s - 4.5s)
      with spinning rays, strike-through wipes, dynamic counting numbers, 3D fanning stack cards,
      activity heatmaps, code terminals, device phone & browser frames, and kinetic typography.
    - LOWER STAGE (Y: 1120px to 1920px): Rock-solid Animated Vector Host Rig behind tech desk,
      4-state RMS lip-sync, automatic 90-frame eye blinking, idle breathing oscillation, boom mic & coffee mug.
    - WORD-BY-WORD KINETIC SUBTITLES: Upper third word-by-word tracking with orange highlight pill.
    - FRAME-ACCURATE SOUND CUES: Outputs assets/sfx_cues.json for sub-frame audio synchronization.
    """
    if slot_meta is None:
        slot_meta = {
            "slot_id": 1,
            "badge_title": "AI OPEN SOURCE",
            "badge_sub": "3 VERIFIED REPOS",
            "cta_keyword": "REPOS",
            "post_title": "Stop Paying Monthly Fees! 3 Open Source Superpowers"
        }

    sid = slot_meta.get("slot_id", 1)
    theme = SLOT_VISUAL_THEMES.get(sid, SLOT_VISUAL_THEMES[1])
    cta_word = slot_meta.get("cta_keyword", "TOOLS").upper()

    # Load curated items
    repos = []
    if os.path.exists(repos_file):
        try:
            with open(repos_file) as f:
                repos = json.load(f)[:3]
        except Exception:
            repos = []

    # Fallback items if needed
    if len(repos) < 3:
        repos = [
            {"name": "Qwen-Image-2.1", "description": "SOTA text-to-image generator", "badge": "LOCAL IMAGE", "stars": "24,500"},
            {"name": "Llama-3.3-70B", "description": "Flagship open weights model", "badge": "OPEN WEIGHTS", "stars": "78,000"},
            {"name": "LobeHub", "description": "Autonomous AI agent fleets", "badge": "AGENT FLEETS", "stars": "83,000"}
        ]

    # Clean & format item data
    items_data = []
    for r in repos:
        name_clean = r["name"].split("/")[-1].replace("-", " ").title()
        stars_val = r.get("stars", 18500)
        star_str = f"{stars_val:,}" if isinstance(stars_val, int) else str(stars_val)

        # Locate preview image
        img_candidate = r.get("demo_media") or r.get("og_image") or ""
        if not os.path.exists(img_candidate):
            safe_name = r.get("full_name", r["name"]).replace("/", "_")
            possible = [
                f"assets/slot_{sid}/{safe_name}/demo.png",
                f"assets/slot_{sid}/{safe_name}/og_banner.png",
                f"assets/slot_{sid}/{safe_name}/demo.webp"
            ]
            for p in possible:
                if os.path.exists(p):
                    img_candidate = p
                    break

        items_data.append({
            "name": name_clean,
            "full_name": r.get("full_name", r["name"]),
            "stars": star_str,
            "desc": r.get("description", "")[:95],
            "badge": r.get("badge", "SOTA AI"),
            "img": img_candidate if os.path.exists(img_candidate) else ""
        })

    while len(items_data) < 3:
        items_data.append({"name": "AI Tool", "full_name": "developer/tool", "stars": "25,000", "desc": "High performance developer tool", "badge": "AI", "img": ""})

    # Load captions
    caption_chunks = []
    if os.path.exists(captions_file):
        with open(captions_file) as f:
            caption_chunks = json.load(f)

    # Deterministic Lip-Sync Data
    mouth_json_path = "assets/mouth.json"
    mouth_data = generate_lipsync_data(
        audio_path=audio_path,
        caption_chunks_path=captions_file,
        output_mouth_path=mouth_json_path,
        fps=30
    )

    # Compute GSAP Lip-Sync mouth states
    mouth_tl_lines = []
    last_m = None
    for item in mouth_data:
        m_state = item["mouth"]
        if m_state != last_m:
            frame_num = item.get("f", item.get("frame", 0))
            t_sec = round(frame_num / 30.0, 3)
            mouth_tl_lines.append(f'tl.call(() => setMouth("{m_state}"), null, {t_sec});')
            last_m = m_state
    mouth_code_str = "\n    ".join(mouth_tl_lines)

    # 10 Micro-Scene Boundary Timestamps (Speech-Locked)
    t_tool1 = duration * 0.22
    t_tool2 = duration * 0.48
    t_tool3 = duration * 0.72
    t_cta = duration * 0.86

    for c in caption_chunks:
        txt = " ".join(c.get("words", [])).lower()
        st = c.get("start", 0)
        if any(k in txt for k in ["first up", "first is", "first,"]):
            t_tool1 = st
        elif any(k in txt for k in ["second", "next is", "next up"]):
            t_tool2 = st
        elif any(k in txt for k in ["finally", "third", "lastly"]):
            t_tool3 = st
        elif any(k in txt for k in ["comment", "drop a comment", "dm me"]):
            t_cta = st

    s1 = 0.0
    s2 = round(t_tool1 * 0.50, 2)
    s3 = round(t_tool1, 2)
    s4 = round(t_tool1 + (t_tool2 - t_tool1) * 0.52, 2)
    s5 = round(t_tool2, 2)
    s6 = round(t_tool2 + (t_tool3 - t_tool2) * 0.52, 2)
    s7 = round(t_tool3, 2)
    s8 = round(t_tool3 + (t_cta - t_tool3) * 0.52, 2)
    s9 = round(max(s8 + 1.5, t_cta - 3.2), 2)
    s10 = round(t_cta, 2)
    s_end = round(duration, 2)

    # Export Frame-Accurate SFX Cues
    sfx_cues = [
        {"type": "boom", "time": s1},
        {"type": "whoosh", "time": round(s1 + 0.05, 2)},
        {"type": "ding", "time": round(s1 + 0.95, 2)},      # Price strike wipe
        {"type": "whoosh", "time": round(s2, 2)},
        {"type": "pop", "time": round(s2 + 0.35, 2)},
        {"type": "ding", "time": round(s2 + 0.85, 2)},     # Counter roll
        {"type": "whoosh", "time": round(s3, 2)},
        {"type": "pop", "time": round(s3 + 0.25, 2)},
        {"type": "ding", "time": round(s3 + 0.80, 2)},
        {"type": "whoosh", "time": round(s4, 2)},
        {"type": "click", "time": round(s4 + 0.35, 2)},
        {"type": "click", "time": round(s4 + 0.70, 2)},
        {"type": "ding", "time": round(s4 + 1.20, 2)},
        {"type": "whoosh", "time": round(s5, 2)},          # Dark mode shift
        {"type": "pop", "time": round(s5 + 0.30, 2)},
        {"type": "ding", "time": round(s5 + 0.85, 2)},
        {"type": "whoosh", "time": round(s6, 2)},
        {"type": "click", "time": round(s6 + 0.40, 2)},
        {"type": "ding", "time": round(s6 + 0.90, 2)},
        {"type": "whoosh", "time": round(s7, 2)},
        {"type": "pop", "time": round(s7 + 0.25, 2)},
        {"type": "click", "time": round(s7 + 0.80, 2)},    # Deploy click
        {"type": "whoosh", "time": round(s8, 2)},
        {"type": "pop", "time": round(s8 + 0.35, 2)},
        {"type": "ding", "time": round(s8 + 0.75, 2)},
        {"type": "whoosh", "time": round(s9, 2)},
        {"type": "pop", "time": round(s9 + 0.30, 2)},
        {"type": "ding", "time": round(s9 + 0.90, 2)},     # Radial ring complete
        {"type": "boom", "time": round(s10, 2)},           # CTA Clay drop
        {"type": "whoosh", "time": round(s10 + 0.05, 2)},
        {"type": "pop", "time": round(s10 + 0.40, 2)},     # Bubble 1
        {"type": "pop", "time": round(s10 + 0.75, 2)},     # Bubble 2
        {"type": "pop", "time": round(s10 + 1.10, 2)},     # Bubble 3
        {"type": "ding", "time": round(s10 + 1.60, 2)}      # DM sent
    ]
    with open("assets/sfx_cues.json", "w") as f:
        json.dump(sfx_cues, f, indent=2)

    # HyperFrames configuration (1080x1920 Full HD @ 30fps)
    hf_config = {
        "name": "daily-automation-engine",
        "version": "3.0.0",
        "fps": 30,
        "width": 1080,
        "height": 1920,
        "duration": s_end
    }
    with open("hyperframes.json", "w") as f:
        json.dump(hf_config, f, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=1080, height=1920, initial-scale=1">
  <title>Jayant Digital Studio - Hyper-Motion Engine</title>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800;900&family=Instrument+Serif:ital@1&family=JetBrains+Mono:wght@600;800&display=swap" rel="stylesheet">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>

  <style>
    :root {{
      --page: #f4f1ea;
      --bar: #1a1714;
      --clay: {theme['accent']};
      --ink: #1a1714;
      --mut: #8c857b;
      --card-bg: #ffffff;
      --border: rgba(26, 23, 20, 0.09);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: var(--page);
      font-family: 'Bricolage Grotesque', system-ui, sans-serif;
      color: var(--ink);
      position: relative;
    }}

    /* Engineering Paper Grid Background */
    #stage {{
      position: absolute;
      inset: 0;
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #f4f1ea;
    }}

    #stage:not(.dark):not(.or)::before {{
      content: "";
      position: absolute;
      inset: 0;
      background-image: 
        linear-gradient(rgba(120, 100, 70, 0.08) 2px, transparent 2px),
        linear-gradient(90deg, rgba(120, 100, 70, 0.08) 2px, transparent 2px);
      background-size: 48px 48px;
      z-index: 1;
      pointer-events: none;
    }}

    /* Ambient Drifting Blur Blobs (Always in motion) */
    .blob {{
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.65;
      animation: drift 9s ease-in-out infinite alternate;
      z-index: 1;
    }}
    .b1 {{ width: 540px; height: 540px; background: {theme['bg_blob1']}; left: -140px; top: 120px; }}
    .b2 {{ width: 480px; height: 480px; background: {theme['bg_blob2']}; right: -160px; top: 60px; animation-delay: -4s; }}
    .b3 {{ width: 560px; height: 420px; background: {theme['bg_blob3']}; left: 80px; top: 580px; animation-delay: -2s; }}

    @keyframes drift {{
      to {{ transform: translate(50px, -45px) scale(1.18); }}
    }}

    /* Dark Mode Stage Shift */
    #stage.dark {{
      background: #0b0809;
      color: #ffffff;
    }}
    #stage.dark::before {{
      background-image: 
        linear-gradient(rgba(255, 255, 255, 0.05) 2px, transparent 2px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.05) 2px, transparent 2px);
    }}
    #stage.dark .b1 {{ background: #5a1d2c; }}
    #stage.dark .b2 {{ background: #2a1f55; }}
    #stage.dark .b3 {{ background: #7a3a22; }}

    /* Clay Mode Stage Shift (Viral CTA) */
    #stage.or {{
      background: {theme['accent']};
      color: #ffffff;
    }}
    #stage.or .b1, #stage.or .b2, #stage.or .b3 {{ background: rgba(255, 255, 255, 0.25); }}

    /* Spinning Rays Conic Mask */
    .rays {{
      position: absolute;
      left: 50%;
      top: 480px;
      width: 820px;
      height: 820px;
      margin: -410px;
      background: repeating-conic-gradient(rgba(217, 105, 74, 0.28) 0 3deg, transparent 3deg 12deg);
      -webkit-mask: radial-gradient(circle, transparent 20%, #000 35%, transparent 72%);
      mask: radial-gradient(circle, transparent 20%, #000 35%, transparent 72%);
      animation: spin 20s linear infinite;
      z-index: 1;
      pointer-events: none;
    }}
    @keyframes spin {{ to {{ rotate: 360deg; }} }}

    /* ================= UPPER THEATER (Y: 40px to 1120px) ================= */
    #upper-theater {{
      position: absolute;
      left: 0;
      top: 0;
      width: 1080px;
      height: 1120px;
      z-index: 10;
      overflow: hidden;
      padding: 60px 54px;
    }}

    .scene-view {{
      position: absolute;
      inset: 60px 54px;
      display: flex;
      flex-direction: column;
      align-items: center;
      opacity: 0;
      pointer-events: none;
      transform-origin: center center;
    }}
    .scene-view.active {{
      opacity: 1;
      pointer-events: auto;
    }}

    /* Reusable Motion Atoms */
    .pill {{
      font: 800 24px 'Bricolage Grotesque';
      padding: 10px 26px;
      border-radius: 99px;
      background: #1a1714;
      color: #fff;
      display: inline-flex;
      align-items: center;
      gap: 12px;
      box-shadow: 0 10px 26px rgba(0,0,0,0.12);
    }}
    .pill.clay {{ background: var(--clay); color: #fff; }}
    .pill.red {{ background: #ef4444; color: #fff; }}
    .pill.green {{ background: #10b981; color: #fff; }}

    .step-pill {{
      font-size: 24px;
      font-weight: 800;
      letter-spacing: 2px;
      background: #1a1714;
      color: #ffffff;
      padding: 12px 28px;
      border-radius: 99px;
      display: inline-flex;
      align-items: center;
      gap: 16px;
      box-shadow: 0 10px 28px rgba(0,0,0,0.15);
      margin-bottom: 24px;
    }}
    .step-dashes {{
      display: flex;
      gap: 6px;
    }}
    .step-dash {{
      width: 20px;
      height: 6px;
      border-radius: 99px;
      background: rgba(255,255,255,0.3);
    }}
    .step-dash.active {{
      background: var(--clay);
      width: 32px;
    }}

    .hero-title {{
      font-size: 68px;
      font-weight: 900;
      line-height: 1.05;
      letter-spacing: -2px;
      text-align: center;
      margin: 10px 0 24px;
    }}
    .serif-accent {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-style: italic;
      font-weight: 400;
      color: var(--clay);
      font-size: 1.14em;
    }}

    .card {{
      background: var(--card-bg);
      border-radius: 28px;
      box-shadow: 0 20px 48px rgba(70, 45, 20, 0.14);
      border: 1px solid var(--border);
      position: relative;
    }}

    /* Strike-Through Animation */
    .strike-wrap {{
      position: relative;
      display: inline-block;
    }}
    .strike {{
      position: absolute;
      left: -12px;
      top: 50%;
      height: 14px;
      background: #ef4444;
      border-radius: 8px;
      width: 0;
      rotate: -8deg;
      animation: wipe 0.6s 0.6s ease-out forwards;
    }}
    @keyframes wipe {{
      to {{ width: calc(100% + 24px); }}
    }}

    /* Animated Counter */
    @property --n {{
      syntax: '<integer>';
      inherits: false;
      initial-value: 0;
    }}
    .cnt {{
      font-size: 130px;
      font-weight: 900;
      color: var(--clay);
      --n: 0;
      animation: cn 1.4s 0.3s ease-out forwards;
      counter-reset: n var(--n);
      line-height: 1;
    }}
    .cnt::after {{
      content: counter(n);
    }}
    @keyframes cn {{
      to {{ --n: 3; }}
    }}

    /* 3D Fanning Cards Stack */
    .stack {{
      position: relative;
      width: 440px;
      height: 240px;
      margin-top: 24px;
    }}
    .stack .fan-card {{
      position: absolute;
      inset: 0;
      background: #ffffff;
      border-radius: 22px;
      box-shadow: 0 16px 36px rgba(70, 45, 20, 0.16);
      padding: 24px 30px;
      border: 1px solid rgba(26,23,20,0.08);
      opacity: 0;
      animation: fan 0.65s var(--d) cubic-bezier(0.3, 1.4, 0.5, 1) forwards;
    }}
    @keyframes fan {{
      from {{ opacity: 0; transform: translateY(80px) rotate(0deg); }}
      to {{ opacity: 1; transform: translate(var(--x), 0) rotate(var(--r)); }}
    }}

    /* Realistic Phone Device Mockup */
    .phone-mockup {{
      width: 620px;
      height: 480px;
      background: #1a1714;
      border-radius: 36px;
      padding: 14px;
      box-shadow: 0 24px 60px rgba(0,0,0,0.22);
      border: 4px solid #332d29;
      position: relative;
      margin-top: 10px;
    }}
    .phone-screen {{
      width: 100%;
      height: 100%;
      border-radius: 26px;
      overflow: hidden;
      background: #231f20;
      position: relative;
      display: flex;
      flex-direction: column;
    }}
    .phone-screen img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}
    .phone-floating-pill {{
      position: absolute;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(255,255,255,0.95);
      color: #1a1714;
      font-size: 24px;
      font-weight: 900;
      padding: 10px 28px;
      border-radius: 99px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
      white-space: nowrap;
    }}

    /* Browser Window Mockup */
    .browser-mockup {{
      width: 820px;
      height: 480px;
      background: #ffffff;
      border-radius: 24px;
      box-shadow: 0 24px 60px rgba(70,45,20,0.18);
      border: 1px solid rgba(26,23,20,0.1);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      margin-top: 10px;
    }}
    .browser-header {{
      background: #ede8df;
      padding: 16px 24px;
      display: flex;
      align-items: center;
      gap: 14px;
      border-bottom: 1px solid rgba(26,23,20,0.08);
    }}
    .browser-dots {{
      display: flex;
      gap: 8px;
    }}
    .browser-dots span {{
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: #d4cec3;
    }}
    .browser-bar {{
      flex: 1;
      background: #ffffff;
      border-radius: 99px;
      padding: 6px 18px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 18px;
      font-weight: 700;
      color: #666;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .browser-body {{
      flex: 1;
      position: relative;
      background: #181516;
      overflow: hidden;
    }}
    .browser-body img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}

    /* Progress Bar Filling */
    .progress-bar-wrap {{
      width: 100%;
      height: 16px;
      border-radius: 99px;
      background: #e5e0d5;
      overflow: hidden;
      margin-top: 16px;
    }}
    .progress-bar-fill {{
      height: 100%;
      background: var(--clay);
      width: 0;
      animation: fillProgress 1.6s 0.4s ease-out forwards;
    }}
    @keyframes fillProgress {{
      to {{ width: 100%; }}
    }}

    /* 28-Cell Activity Calendar Heatmap */
    .cal-grid {{
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 12px;
      width: 680px;
      margin-top: 18px;
    }}
    .cal-cell {{
      height: 60px;
      border-radius: 12px;
      background: #e9e4da;
    }}
    .cal-cell.active {{
      animation: popCell 0.4s var(--d) cubic-bezier(0.3, 1.4, 0.5, 1) forwards;
    }}
    @keyframes popCell {{
      to {{ background: var(--clay); box-shadow: 0 0 0 4px #fff inset, 0 6px 16px rgba(217,105,74,0.4); }}
    }}

    /* Radial Progress Ring SVG */
    .radial-ring {{
      width: 220px;
      height: 220px;
      position: relative;
      margin: 10px auto;
    }}
    .radial-ring svg {{
      width: 220px;
      height: 220px;
      transform: rotate(-90deg);
    }}
    .radial-ring circle {{
      fill: none;
      stroke-width: 16;
      stroke-linecap: round;
    }}
    .radial-ring .ring-track {{ stroke: #ede7dc; }}
    .radial-ring .ring-fill {{
      stroke: var(--clay);
      stroke-dasharray: 565;
      stroke-dashoffset: 565;
      animation: ringFill 2.0s 0.4s ease-out forwards;
    }}
    @keyframes ringFill {{
      to {{ stroke-dashoffset: 20; }}
    }}
    .radial-ring span {{
      position: absolute;
      inset: 0;
      display: grid;
      place-items: center;
      font-size: 56px;
      font-weight: 900;
    }}

    /* Radar Viewport */
    .radar-box {{
      width: 440px;
      height: 340px;
      border-radius: 24px;
      background: #110d10;
      border: 2px solid #2d262a;
      position: relative;
      overflow: hidden;
      margin-top: 10px;
    }}
    .radar-sweep-beam {{
      position: absolute;
      left: 50%;
      top: 50%;
      width: 240px;
      height: 240px;
      margin: -120px;
      border-radius: 50%;
      background: conic-gradient(from 0deg, rgba(124,58,237,0.7) 0deg, transparent 90deg);
      animation: spin 3s linear infinite;
    }}

    /* Glowing Pulse */
    .glow-pulse {{
      box-shadow: 0 0 0 0 rgba(217,105,74,0.8);
      animation: pulseGlow 1.4s 1.2s infinite;
    }}
    @keyframes pulseGlow {{
      to {{ box-shadow: 0 0 0 30px rgba(217,105,74,0); }}
    }}

    /* Bouncing Bold Letters */
    .bounce-word {{
      display: flex;
      font-size: 140px;
      font-weight: 900;
      letter-spacing: -4px;
      line-height: 1;
    }}
    .bounce-word span {{
      display: inline-block;
      opacity: 0;
      animation: letterPop 0.5s var(--d) cubic-bezier(0.2, 1.4, 0.4, 1) forwards;
    }}
    @keyframes letterPop {{
      from {{ opacity: 0; transform: translateY(70px) rotate(16deg); }}
      to {{ opacity: 1; transform: none; }}
    }}

    /* Comment Bubbles (CTA) */
    .cta-bubble {{
      background: #ffffff;
      color: #1a1714;
      font-size: 26px;
      font-weight: 800;
      padding: 16px 32px;
      border-radius: 99px;
      box-shadow: 0 14px 34px rgba(0,0,0,0.18);
      display: flex;
      align-items: center;
      gap: 16px;
      margin-top: 14px;
      opacity: 0;
      animation: bubbleDrop 0.5s var(--d) cubic-bezier(0.3, 1.5, 0.5, 1) forwards;
    }}
    @keyframes bubbleDrop {{
      from {{ opacity: 0; transform: translateY(-40px) scale(0.85); }}
      to {{ opacity: 1; transform: none; }}
    }}
    .cb-avatar {{
      width: 38px;
      height: 38px;
      border-radius: 50%;
      background: var(--clay);
    }}

    /* ================= KINETIC SUBTITLE BAR (Y: 1040px to 1120px) ================= */
    #caption-bar {{
      position: absolute;
      left: 60px;
      right: 60px;
      top: 1040px;
      height: 90px;
      z-index: 100;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
      text-align: center;
    }}
    #caption-bar .w {{
      font-size: 38px;
      font-weight: 800;
      color: var(--mut);
      padding: 6px 14px;
      border-radius: 12px;
      display: inline-block;
    }}
    #caption-bar .w.done {{
      color: var(--ink);
    }}
    #stage.dark #caption-bar .w.done,
    #stage.or #caption-bar .w.done {{
      color: #ffffff;
    }}
    #caption-bar .w.on {{
      background: var(--clay);
      color: #ffffff !important;
      transform: scale(1.12);
      box-shadow: 0 8px 24px rgba(0,0,0,0.22);
    }}
    #stage.or #caption-bar .w.on {{
      background: #1a1714;
    }}

    /* ================= LOWER STAGE: HOST AVATAR & TECH DESK (Y: 1120px to 1920px) ================= */
    #lower-stage {{
      position: absolute;
      left: 0;
      bottom: 0;
      width: 1080px;
      height: 800px;
      z-index: 50;
      pointer-events: none;
    }}

    #host-avatar {{
      position: absolute;
      left: 50%;
      bottom: 220px;
      transform: translateX(-50%);
      width: 640px;
      height: 640px;
      z-index: 51;
    }}

    .desk-surface {{
      position: absolute;
      left: 0;
      bottom: 0;
      width: 1080px;
      height: 240px;
      background: linear-gradient(180deg, #96603a 0%, #683e20 40%, #3e2210 100%);
      border-top: 12px solid #b3784c;
      box-shadow: 0 -16px 40px rgba(0,0,0,0.35);
      z-index: 55;
    }}

    .desk-props {{
      position: absolute;
      left: 0;
      bottom: 140px;
      width: 1080px;
      height: 280px;
      z-index: 60;
      pointer-events: none;
    }}

    .studio-mic {{
      position: absolute;
      right: 140px;
      bottom: 20px;
      width: 220px;
      height: 260px;
    }}

    .desk-mug-wrap {{
      position: absolute;
      left: 170px;
      bottom: 30px;
      width: 100px;
      height: 120px;
    }}
    .mug-cup {{
      width: 80px;
      height: 94px;
      background: {theme['mug_color']};
      border-radius: 6px 6px 18px 18px;
      border: 6px solid #1a1714;
      position: absolute;
      bottom: 0;
      box-shadow: 6px 12px 24px rgba(0,0,0,0.3);
    }}
    .mug-cup::after {{
      content: "";
      position: absolute;
      right: -24px;
      top: 18px;
      width: 28px;
      height: 48px;
      border: 6px solid #1a1714;
      border-radius: 0 16px 16px 0;
    }}
    .steam-curl {{
      position: absolute;
      font-size: 38px;
      color: rgba(255,255,255,0.7);
      animation: steamRise 2.2s infinite ease-out;
      font-family: monospace;
    }}
    .s1 {{ left: 16px; bottom: 95px; animation-delay: 0s; }}
    .s2 {{ left: 42px; bottom: 95px; animation-delay: 1.1s; }}
    @keyframes steamRise {{
      0% {{ opacity: 0; transform: translateY(0) scaleX(1); }}
      50% {{ opacity: 0.8; transform: translateY(-28px) scaleX(1.3); }}
      100% {{ opacity: 0; transform: translateY(-56px) scaleX(0.9); }}
    }}

    /* Subtitle Bounding Box highlight style matching Video-56015.mp4 */
    .word-box {{
      border: 3px solid var(--clay);
      border-radius: 8px;
      padding: 0 8px;
      background: rgba(217, 105, 74, 0.12);
      font-weight: 900;
      color: #1a1714;
    }}
  </style>
</head>

<body>
  <div id="stage" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{round(duration, 2)}" data-fps="30">
    <!-- Ambient Blur Blobs -->
    <div class="blob b1"></div>
    <div class="blob b2"></div>
    <div class="blob b3"></div>

    <!-- HyperFrames Synchronized Voice Audio -->
    <audio id="voice" src="{audio_path}" data-start="0" data-duration="{round(duration, 2)}" data-volume="1"></audio>

    <!-- ================= UPPER THEATER (10 HYPER-MOTION SCENES) ================= -->
    <div id="upper-theater">

      <!-- SCENE 1: HOOK (Pain Point / $200 Subscriptions Crossed Out) -->
      <div id="sc-1" class="scene-view active">
        <div class="rays"></div>
        <div class="pill red" style="margin-top: 10px;">✕ TIRED OF PAYING SUBSCRIPTIONS</div>

        <h1 class="hero-title" style="margin-top: 24px;">
          Stop Paying <span class="serif-accent">Monthly Fees!</span><br>
          3 Open Source Superpowers
        </h1>

        <div class="card" style="width: 820px; padding: 36px 48px; margin-top: 24px; display: flex; align-items: center; justify-content: space-between;">
          <div>
            <div style="font-size: 26px; font-weight: 800; color: #ef4444; margin-bottom: 6px;">✕ CLOSED PLATFORMS</div>
            <div class="strike-wrap">
              <span style="font-size: 88px; font-weight: 900; color: #1a1714;">$200/mo</span>
              <div class="strike"></div>
            </div>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 26px; font-weight: 800; color: #10b981; margin-bottom: 6px;">✓ 3 VERIFIED REPOS</div>
            <div style="font-size: 88px; font-weight: 900; color: #10b981;">$0 FREE</div>
          </div>
        </div>
      </div>

      <!-- SCENE 2: HOOK REVEAL (Fanning Stack Cards + Rolling 0->3 Counter) -->
      <div id="sc-2" class="scene-view">
        <div class="pill clay">3 PROVEN FORMULAS</div>
        <div class="bounce-word" style="margin-top: 10px;">
          <span style="--d: 0.1s; color: var(--clay);">F</span>
          <span style="--d: 0.2s; color: var(--clay);">R</span>
          <span style="--d: 0.3s; color: var(--clay);">E</span>
          <span style="--d: 0.4s; color: var(--clay);">E</span>
        </div>

        <div class="stack">
          <div class="fan-card" style="--d: 0.1s; --x: -60px; --r: -12deg;">
            <div style="font-size: 28px; font-weight: 900; color: var(--clay);">#1 {items_data[0]['name']}</div>
            <div style="font-size: 20px; font-weight: 700; color: #666; margin-top: 6px;">{items_data[0]['badge']}</div>
          </div>
          <div class="fan-card" style="--d: 0.25s; --x: 0px; --r: 0deg;">
            <div style="font-size: 28px; font-weight: 900; color: #2563eb;">#2 {items_data[1]['name']}</div>
            <div style="font-size: 20px; font-weight: 700; color: #666; margin-top: 6px;">{items_data[1]['badge']}</div>
          </div>
          <div class="fan-card" style="--d: 0.4s; --x: 60px; --r: 12deg;">
            <div style="font-size: 28px; font-weight: 900; color: #10b981;">#3 {items_data[2]['name']}</div>
            <div style="font-size: 20px; font-weight: 700; color: #666; margin-top: 6px;">{items_data[2]['badge']}</div>
          </div>
        </div>
      </div>

      <!-- SCENE 3: TOOL 1 HERO (Device Phone Mockup + Rating + Badge) -->
      <div id="sc-3" class="scene-view">
        <div class="step-pill">
          TOOL 1/3 · {items_data[0]['badge'].upper()}
          <div class="step-dashes">
            <div class="step-dash active"></div>
            <div class="step-dash"></div>
            <div class="step-dash"></div>
          </div>
        </div>

        <h1 class="hero-title">
          {items_data[0]['name']} <span class="serif-accent">breakthrough</span>
        </h1>

        <div class="phone-mockup">
          <div class="phone-screen">
            {"<img src='" + items_data[0]['img'] + "' alt='preview'>" if items_data[0]['img'] else "<div style='display: grid; place-items: center; height: 100%; font-size: 48px; font-weight: 900; color: #fff;'>🎨 " + items_data[0]['name'].upper() + "</div>"}
            <div class="phone-floating-pill">★ {items_data[0]['stars']} · 100% Offline GGUF</div>
          </div>
        </div>
      </div>

      <!-- SCENE 4: TOOL 1 FEATURE (Code Terminal + Speed Progress Bar) -->
      <div id="sc-4" class="scene-view">
        <div class="step-pill">
          TOOL 1/3 · EXECUTION SPEED
          <div class="step-dashes">
            <div class="step-dash active"></div>
            <div class="step-dash"></div>
            <div class="step-dash"></div>
          </div>
        </div>

        <div class="card" style="width: 820px; padding: 36px 44px; margin-top: 10px;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 26px; font-weight: 800; color: var(--clay);">LOCAL INFERENCE SPEED</span>
            <span style="background: #dcfce7; color: #15803d; font-size: 22px; font-weight: 800; padding: 6px 18px; border-radius: 99px;">10x FASTER</span>
          </div>
          <div class="progress-bar-wrap">
            <div class="progress-bar-fill"></div>
          </div>
          <div style="font-size: 32px; font-weight: 800; color: #1a1714; margin-top: 24px;">
            {items_data[0]['desc']}
          </div>
        </div>
      </div>

      <!-- SCENE 5: TOOL 2 HERO (Contrasting Dark Mode Shift + Radar Sweep) -->
      <div id="sc-5" class="scene-view">
        <div class="step-pill" style="background: #2e1065; border: 1px solid #7c3aed;">
          TOOL 2/3 · {items_data[1]['badge'].upper()}
          <div class="step-dashes">
            <div class="step-dash active"></div>
            <div class="step-dash active"></div>
            <div class="step-dash"></div>
          </div>
        </div>

        <h1 class="hero-title" style="color: #ffffff;">
          {items_data[1]['name']} <span class="serif-accent" style="color: #a78bfa;">private intelligence</span>
        </h1>

        <div class="radar-box">
          <div class="radar-sweep-beam"></div>
          <div style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 5;">
            <div style="font-size: 64px; font-weight: 900; color: #a78bfa;">28ms</div>
            <div style="font-size: 24px; font-weight: 800; color: #e9d5ff; letter-spacing: 2px;">ULTRA-LOW LATENCY</div>
          </div>
        </div>
      </div>

      <!-- SCENE 6: TOOL 2 FEATURE (Connected Flow Nodes + Benchmark Metric) -->
      <div id="sc-6" class="scene-view">
        <div class="step-pill" style="background: #2e1065; border: 1px solid #7c3aed;">
          TOOL 2/3 · BENCHMARK DUEL
          <div class="step-dashes">
            <div class="step-dash active"></div>
            <div class="step-dash active"></div>
            <div class="step-dash"></div>
          </div>
        </div>

        <div class="card" style="width: 820px; background: #17131a; border: 2px solid #3b2d42; padding: 36px 44px; color: #fff; margin-top: 10px;">
          <div style="font-size: 32px; font-weight: 900; color: #a78bfa; margin-bottom: 16px;">
            BEATS PROPRIETARY MODELS
          </div>
          <div style="font-size: 28px; font-weight: 700; color: #ddd; line-height: 1.3;">
            {items_data[1]['desc']}
          </div>
          <div style="display: flex; gap: 16px; margin-top: 24px;">
            <span style="background: #4c1d95; color: #fff; padding: 8px 22px; border-radius: 99px; font-size: 22px; font-weight: 800;">★ {items_data[1]['stars']} Stars</span>
            <span style="background: #065f46; color: #6ee7b7; padding: 8px 22px; border-radius: 99px; font-size: 22px; font-weight: 800;">Zero GPU Subscriptions</span>
          </div>
        </div>
      </div>

      <!-- SCENE 7: TOOL 3 HERO (Browser Window Mockup + Cursor Click) -->
      <div id="sc-7" class="scene-view">
        <div class="step-pill">
          TOOL 3/3 · {items_data[2]['badge'].upper()}
          <div class="step-dashes">
            <div class="step-dash active"></div>
            <div class="step-dash active"></div>
            <div class="step-dash active"></div>
          </div>
        </div>

        <h1 class="hero-title">
          {items_data[2]['name']} <span class="serif-accent">agent operator</span>
        </h1>

        <div class="browser-mockup">
          <div class="browser-header">
            <div class="browser-dots">
              <span></span><span></span><span></span>
            </div>
            <div class="browser-bar">
              🔒 github.com/{items_data[2]['full_name']}
            </div>
            <div style="background: var(--clay); color: #fff; font-size: 16px; font-weight: 800; padding: 6px 16px; border-radius: 99px;">
              DEPLOY ➔
            </div>
          </div>
          <div class="browser-body">
            {"<img src='" + items_data[2]['img'] + "' alt='preview'>" if items_data[2]['img'] else "<div style='display: grid; place-items: center; height: 100%; font-size: 48px; font-weight: 900; color: #fff;'>⚡ " + items_data[2]['name'].upper() + "</div>"}
          </div>
        </div>
      </div>

      <!-- SCENE 8: TOOL 3 FEATURE (24/7 Fleet Activity Heatmap Grid) -->
      <div id="sc-8" class="scene-view">
        <div class="step-pill">
          TOOL 3/3 · 24/7 AUTONOMOUS FLEET
          <div class="step-dashes">
            <div class="step-dash active"></div>
            <div class="step-dash active"></div>
            <div class="step-dash active"></div>
          </div>
        </div>

        <div class="card" style="width: 820px; padding: 32px 40px; margin-top: 10px; display: flex; flex-direction: column; align-items: center;">
          <div style="display: flex; justify-content: space-between; width: 100%; font-size: 26px; font-weight: 800;">
            <span>ACTIVE WORKER AGENTS</span>
            <span style="color: #10b981;">● 24/7 RUNNING</span>
          </div>

          <div class="cal-grid">
            {''.join([f'<div class="cal-cell active" style="--d: {0.1 + i*0.06}s;"></div>' if i % 2 == 0 or i % 3 == 0 else '<div class="cal-cell"></div>' for i in range(28)])}
          </div>

          <div style="font-size: 28px; font-weight: 800; color: #1a1714; margin-top: 24px; text-align: center;">
            {items_data[2]['desc']}
          </div>
        </div>
      </div>

      <!-- SCENE 9: PROVEN SYSTEM (Radial Progress Ring + 3-Step Checklist) -->
      <div id="sc-9" class="scene-view">
        <div class="step-pill">
          BONUS · INSTANT SETUP
          <div class="step-dashes">
            <div class="step-dash active"></div>
            <div class="step-dash active"></div>
            <div class="step-dash active"></div>
          </div>
        </div>

        <div class="radial-ring">
          <svg viewBox="0 0 220 220">
            <circle class="ring-track" cx="110" cy="110" r="90"/>
            <circle class="ring-fill" cx="110" cy="110" r="90"/>
          </svg>
          <span>10s</span>
        </div>

        <div class="card" style="width: 820px; padding: 24px 36px; margin-top: 14px; display: flex; flex-direction: column; gap: 14px;">
          <div style="display: flex; align-items: center; gap: 16px; font-size: 26px; font-weight: 800;">
            <span style="background: var(--clay); color: #fff; width: 36px; height: 36px; border-radius: 50%; display: grid; place-items: center;">1</span>
            Open terminal & clone repository
          </div>
          <div style="display: flex; align-items: center; gap: 16px; font-size: 26px; font-weight: 800;">
            <span style="background: var(--clay); color: #fff; width: 36px; height: 36px; border-radius: 50%; display: grid; place-items: center;">2</span>
            Run single-command installer
          </div>
          <div style="display: flex; align-items: center; gap: 16px; font-size: 26px; font-weight: 800; color: #10b981;">
            <span style="background: #10b981; color: #fff; width: 36px; height: 36px; border-radius: 50%; display: grid; place-items: center;">✔</span>
            Ready to use 100% free offline
          </div>
        </div>
      </div>

      <!-- SCENE 10: VIRAL CTA (Clay Mode Shift + Comment Bubbles + DM Notification) -->
      <div id="sc-10" class="scene-view">
        <div class="step-pill" style="background: #1a1714; color: #fff;">
          🎁 FREE BLUEPRINT + REPO LINKS
        </div>

        <div style="display: flex; gap: 20px; margin-top: 10px;">
          <div class="pill" style="font-size: 38px; padding: 14px 36px; transform: rotate(-3deg);">💬 COMMENT</div>
          <div class="pill clay" style="font-size: 38px; padding: 14px 36px; transform: rotate(3deg);">{cta_word}</div>
        </div>

        <!-- Flying Comment Bubbles -->
        <div class="cta-bubble" style="--d: 0.1s;">
          <div class="cb-avatar" style="background: #f59e0b;"></div>
          <span>@alex.ai {cta_word.lower()} 🔥</span>
        </div>
        <div class="cta-bubble" style="--d: 0.25s;">
          <div class="cb-avatar" style="background: #3b82f6;"></div>
          <span>@dev_kevin {cta_word.capitalize()} please!</span>
        </div>
        <div class="cta-bubble" style="--d: 0.4s;">
          <div class="cb-avatar" style="background: #10b981;"></div>
          <span>@sara.tech {cta_word}!</span>
        </div>

        <!-- DM Notification Card -->
        <div class="card" style="width: 820px; padding: 22px 34px; margin-top: 20px; display: flex; align-items: center; gap: 20px;">
          <div style="font-size: 44px;">📩</div>
          <div>
            <div style="font-size: 28px; font-weight: 900; color: #1a1714;">jayant.digitalstudio · now</div>
            <div style="font-size: 24px; font-weight: 700; color: var(--mut);">All 3 tool repos + setup guide sent to your DMs</div>
          </div>
          <div style="margin-left: auto; background: #dcfce7; color: #15803d; padding: 8px 20px; border-radius: 99px; font-size: 20px; font-weight: 900;">SENT ✓</div>
        </div>
      </div>

    </div> <!-- end upper-theater -->

    <!-- ================= WORD-BY-WORD KINETIC SUBTITLE BAR ================= -->
    <div id="caption-bar"></div>

    <!-- ================= LOWER STAGE: ANIMATED HOST AVATAR & TECH DESK ================= -->
    <div id="lower-stage">

      <!-- Host Avatar Rig (Anchored - Zero Detached Limbs) -->
      <div id="host-avatar">
        <svg viewBox="0 0 440 440" width="100%" height="100%">
          <defs>
            <linearGradient id="skin" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#fcd5b8"/>
              <stop offset="100%" stop-color="#f5b890"/>
            </linearGradient>
            <linearGradient id="hoodie" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="{theme['hoodie_color']}"/>
              <stop offset="100%" stop-color="#141312"/>
            </linearGradient>
          </defs>

          <!-- Avatar Character (Idle Breathing Oscillation) -->
          <g id="avatar-character">
            
            <!-- Torso & Broad Shoulders -->
            <path d="M80 340 C80 270, 160 255, 220 255 C280 255, 360 270, 360 340 L380 440 L60 440 Z" 
                  fill="url(#hoodie)" stroke="#1a1714" stroke-width="8"/>
            <path d="M190 255 C190 295, 250 295, 250 255 Z" fill="#ffffff" stroke="#1a1714" stroke-width="6"/>
            <!-- Drawstrings -->
            <path d="M165 260 L195 355" stroke="{theme['hoodie_trim']}" stroke-width="6" stroke-linecap="round" fill="none"/>
            <path d="M275 260 L245 355" stroke="{theme['hoodie_trim']}" stroke-width="6" stroke-linecap="round" fill="none"/>

            <!-- Arms Contiguously Attached Resting on Desk (ZERO detachment) -->
            <path d="M90 320 C80 365, 100 410, 165 424" fill="none" stroke="#1a1714" stroke-width="36" stroke-linecap="round"/>
            <path d="M90 320 C80 365, 100 410, 165 424" fill="none" stroke="{theme['hoodie_color']}" stroke-width="28" stroke-linecap="round"/>
            <circle cx="170" cy="424" r="14" fill="url(#skin)" stroke="#1a1714" stroke-width="5"/>

            <path d="M350 320 C360 365, 340 410, 275 424" fill="none" stroke="#1a1714" stroke-width="36" stroke-linecap="round"/>
            <path d="M350 320 C360 365, 340 410, 275 424" fill="none" stroke="{theme['hoodie_color']}" stroke-width="28" stroke-linecap="round"/>
            <circle cx="270" cy="424" r="14" fill="url(#skin)" stroke="#1a1714" stroke-width="5"/>

            <!-- Neck -->
            <path d="M195 240 L195 275 C195 285, 245 285, 245 275 L245 240 Z" 
                  fill="url(#skin)" stroke="#1a1714" stroke-width="6"/>

            <!-- Head / Jaw -->
            <path d="M150 155 C150 90, 290 90, 290 155 C290 230, 255 258, 220 258 C185 258, 150 230, 150 155 Z" 
                  fill="url(#skin)" stroke="#1a1714" stroke-width="7"/>

            <!-- Stylish Modern Hair -->
            <path d="M142 145 C138 95, 175 60, 220 58 C265 60, 302 95, 298 145 C294 110, 260 78, 220 78 C180 78, 146 110, 142 145 Z" 
                  fill="#1a1714"/>
            <path d="M146 130 C155 105, 185 85, 220 84 C255 85, 285 105, 294 130 C280 115, 250 102, 220 102 C190 102, 160 115, 146 130 Z" 
                  fill="#2d2a26"/>

            <!-- Ears -->
            <ellipse cx="148" cy="170" rx="10" ry="16" fill="url(#skin)" stroke="#1a1714" stroke-width="5"/>
            <ellipse cx="292" cy="170" rx="10" ry="16" fill="url(#skin)" stroke="#1a1714" stroke-width="5"/>

            <!-- Eyebrows -->
            <path d="M172 145 Q190 138 204 146" stroke="#1a1714" stroke-width="6" stroke-linecap="round" fill="none"/>
            <path d="M236 146 Q250 138 268 145" stroke="#1a1714" stroke-width="6" stroke-linecap="round" fill="none"/>

            <!-- Eyes (Blinking Group) -->
            <g id="eyes-open">
              <ellipse cx="188" cy="162" rx="11" ry="13" fill="#ffffff" stroke="#1a1714" stroke-width="4.5"/>
              <ellipse cx="252" cy="162" rx="11" ry="13" fill="#ffffff" stroke="#1a1714" stroke-width="4.5"/>
              <circle cx="189" cy="162" r="6" fill="#1a1714"/>
              <circle cx="253" cy="162" r="6" fill="#1a1714"/>
              <circle cx="191" cy="159" r="2.5" fill="#ffffff"/>
              <circle cx="255" cy="159" r="2.5" fill="#ffffff"/>
            </g>
            <g id="eyes-blink" style="display:none;">
              <path d="M177 163 Q188 171 199 163" stroke="#1a1714" stroke-width="6" stroke-linecap="round" fill="none"/>
              <path d="M241 163 Q252 171 263 163" stroke="#1a1714" stroke-width="6" stroke-linecap="round" fill="none"/>
            </g>

            <!-- Nose -->
            <path d="M220 162 L216 186 L224 186" stroke="#1a1714" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>

            <!-- Well-Groomed Stubble / Beard -->
            <path d="M168 190 C172 238, 268 238, 272 190 C265 248, 175 248, 168 190 Z" fill="#2d2a26" opacity="0.35"/>

            <!-- Synchronized Lip-Sync Mouth Rig (4-State RMS) -->
            <g id="mouth-closed">
              <path d="M205 210 Q220 215 235 210" stroke="#1a1714" stroke-width="5" stroke-linecap="round" fill="none"/>
            </g>
            <g id="mouth-small" style="display:none;">
              <ellipse cx="220" cy="211" rx="8" ry="6" fill="#7a2e22" stroke="#1a1714" stroke-width="4"/>
            </g>
            <g id="mouth-open" style="display:none;">
              <path d="M204 207 Q220 203 236 207 Q220 226 204 207 Z" fill="#7a2e22" stroke="#1a1714" stroke-width="4.5"/>
              <path d="M208 208 Q220 211 232 208" stroke="#ffffff" stroke-width="3" fill="none"/>
            </g>
            <g id="mouth-wide" style="display:none;">
              <path d="M200 206 Q220 200 240 206 Q220 235 200 206 Z" fill="#7a2e22" stroke="#1a1714" stroke-width="5"/>
              <path d="M205 208 Q220 213 235 208" stroke="#ffffff" stroke-width="4" fill="none"/>
              <path d="M210 224 Q220 220 230 224" stroke="#d97768" stroke-width="5" stroke-linecap="round" fill="none"/>
            </g>

          </g> <!-- end avatar-character -->
        </svg>
      </div> <!-- end host-avatar -->

      <!-- Wooden Tech Desk Surface -->
      <div class="desk-surface"></div>

      <!-- Desk Props: Studio Boom Microphone & Steaming Mug -->
      <div class="desk-props">
        <div class="studio-mic">
          <svg viewBox="0 0 120 140" width="100%" height="100%">
            <rect x="15" y="115" width="24" height="22" rx="4" fill="#1a1714"/>
            <path d="M26 115 L50 55 L82 78" stroke="#1a1714" stroke-width="8" stroke-linecap="round" fill="none"/>
            <path d="M30 115 L54 55 L86 78" stroke="#6b7280" stroke-width="3.5" stroke-linecap="round" fill="none"/>
            <circle cx="26" cy="115" r="8" fill="#1a1714"/>
            <circle cx="50" cy="55" r="8" fill="#1a1714"/>
            <circle cx="86" cy="82" r="18" fill="none" stroke="#1a1714" stroke-width="4.5"/>
            <rect x="76" y="66" width="22" height="34" rx="11" fill="#2d3748" stroke="#1a1714" stroke-width="4"/>
            <path d="M79 78 L95 78 M79 84 L95 84" stroke="#4a5568" stroke-width="2.5"/>
          </svg>
        </div>

        <div class="desk-mug-wrap">
          <div class="steam-curl s1">~</div>
          <div class="steam-curl s2">~</div>
          <div class="mug-cup"></div>
        </div>
      </div>

    </div> <!-- end lower-stage -->

  </div> <!-- end stage -->

  <script>
    const captionChunks = {json.dumps(caption_chunks)};
    const duration = {round(duration, 2)};
    const stage = document.getElementById("stage");

    const tl = gsap.timeline();
    window.__timelines = window.__timelines || {{}};
    window.__timelines["main"] = tl;

    // Helper functions
    function setMouth(state) {{
      const states = ["closed", "small", "open", "wide"];
      states.forEach(s => {{
        const el = document.getElementById("mouth-" + s);
        if (el) el.style.display = (s === state ? "block" : "none");
      }});
    }}

    function switchScene(fromId, toId, time, mode = "") {{
      tl.to(fromId, {{ opacity: 0, duration: 0.2 }}, time);
      tl.set(fromId, {{ display: "none", pointerEvents: "none" }}, time + 0.2);
      tl.call(() => {{
        if (mode === "dark") {{
          stage.className = "dark";
        }} else if (mode === "or") {{
          stage.className = "or";
        }} else {{
          stage.className = "";
        }}
      }}, null, time + 0.2);
      tl.set(toId, {{ display: "flex", pointerEvents: "auto" }}, time + 0.2);
      tl.fromTo(toId, {{ opacity: 0, y: 35, scale: 0.95 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(1.4)" }}, time + 0.2);
    }}

    // 1. Initial State
    gsap.set("#sc-1", {{ display: "flex", opacity: 1, pointerEvents: "auto" }});
    gsap.set(["#sc-2", "#sc-3", "#sc-4", "#sc-5", "#sc-6", "#sc-7", "#sc-8", "#sc-9", "#sc-10"], {{ display: "none", opacity: 0, pointerEvents: "none" }});
    gsap.set("#eyes-open", {{ display: "block" }});
    gsap.set("#eyes-blink", {{ display: "none" }});

    // 2. 10 Micro-Scene Transitions
    switchScene("#sc-1", "#sc-2", {s2});
    switchScene("#sc-2", "#sc-3", {s3});
    switchScene("#sc-3", "#sc-4", {s4});
    switchScene("#sc-4", "#sc-5", {s5}, "dark");   // Dark mode for Tool 2
    switchScene("#sc-5", "#sc-6", {s6}, "dark");
    switchScene("#sc-6", "#sc-7", {s7}, "");       // Back to tech paper
    switchScene("#sc-7", "#sc-8", {s8});
    switchScene("#sc-8", "#sc-9", {s9});
    switchScene("#sc-9", "#sc-10", {s10}, "or");    // Clay brand mode for Viral CTA

    // 3. Continuous Idle Breathing Oscillation
    tl.to("#avatar-character", {{ y: -6, duration: 1.4, repeat: {int(duration / 1.4)}, yoyo: true, ease: "sine.inOut" }}, 0);

    // 4. Automatic Eye Blinks (Every 3 seconds)
    for (let t = 1.2; t < duration; t += 3.0) {{
      tl.set("#eyes-open", {{ display: "none" }}, t);
      tl.set("#eyes-blink", {{ display: "block" }}, t);
      tl.set("#eyes-open", {{ display: "block" }}, t + 0.133);
      tl.set("#eyes-blink", {{ display: "none" }}, t + 0.133);
    }}

    // 5. Frame-Accurate Lip-Sync
    {mouth_code_str}

    // 6. Word-by-Word Kinetic Subtitle Schedule
    captionChunks.forEach(chunk => {{
      tl.call(() => {{
        const bar = document.getElementById("caption-bar");
        if (!bar) return;
        bar.innerHTML = "";
        chunk.words.forEach((w, wIdx) => {{
          const span = document.createElement("span");
          span.className = "w" + (wIdx === chunk.active ? " on" : (wIdx < chunk.active ? " done" : ""));
          span.innerText = w;
          bar.appendChild(span);
        }});
      }}, null, chunk.start);
    }});
  </script>
</body>
</html>
"""

    with open(output_html, "w") as f:
        f.write(html)

    print(f"[✓] Compiled 10-Scene Hyper-Motion Studio Composition to {output_html} ({round(duration, 2)}s, {len(sfx_cues)} SFX cues)")
    return output_html

if __name__ == "__main__":
    build_hyperframes_composition()
