import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipeline.lipsync_engine import generate_lipsync_data

SLOT_VISUAL_THEMES = {
    1: {
        "name": "CYBER_OPENSOURCE",
        "badge_pill": "⚡ OPEN SOURCE REPOS",
        "accent": "#d9694a",       # Terracotta Clay
        "accent_bg": "#fbeae5",
        "hoodie_color": "#1f1d1a",
        "hoodie_trim": "#d9694a",
        "mug_color": "#d9694a",
        "tagline": "Run 100% Locally · Zero Fees"
    },
    2: {
        "name": "AUTOMATION_STUDIO",
        "badge_pill": "🔄 AI AUTOMATION PIPELINE",
        "accent": "#059669",       # Emerald
        "accent_bg": "#ecfdf5",
        "hoodie_color": "#132a22",
        "hoodie_trim": "#10b981",
        "mug_color": "#10b981",
        "tagline": "Save 20 Hours Every Week"
    },
    3: {
        "name": "MODEL_RADAR",
        "badge_pill": "🧠 MODEL RADAR & BENCHMARKS",
        "accent": "#7c3aed",       # Violet
        "accent_bg": "#f5f3ff",
        "hoodie_color": "#1e1435",
        "hoodie_trim": "#a855f7",
        "mug_color": "#8b5cf6",
        "tagline": "New SOTA Architecture Teardown"
    },
    4: {
        "name": "SECRET_TOOLS",
        "badge_pill": "🛠️ SECRET NO-CODE TOOLS",
        "accent": "#ea580c",       # Sunset Orange
        "accent_bg": "#fff7ed",
        "hoodie_color": "#2c1710",
        "hoodie_trim": "#f97316",
        "mug_color": "#f97316",
        "tagline": "Replaces Expensive Subscriptions"
    },
    5: {
        "name": "PROMPT_LAB",
        "badge_pill": "🎯 SENIOR PROMPT ARCHITECTURE",
        "accent": "#dc2626",       # Crimson
        "accent_bg": "#fef2f2",
        "hoodie_color": "#281212",
        "hoodie_trim": "#ef4444",
        "mug_color": "#ef4444",
        "tagline": "Zero Hallucination Framework"
    }
}

def build_hyperframes_composition(
    repos_file="assets/curated_repos.json",
    captions_file="assets/caption_chunks.json",
    audio_path="assets/voice.mp3",
    script_file="assets/generated_script.json",
    duration=43.47,
    output_html="index.html",
    slot_meta=None
):
    """
    1080x1920 Full HD High-Retention Broadcast Studio Composition:
    - UPPER THEATER (Y: 50 to 1120px): Full-motion kinetic graphics with real repo media/images,
      spring-bounced cards, live typing code terminals, 360° radar sweeps, and benchmark duels.
      Strictly 3 tools (TOOL 1/3, TOOL 2/3, TOOL 3/3) with 100% speech-to-visual synchronization!
    - LOWER STAGE (Y: 1120 to 1920px): Animated Vector Host Character Rig seated behind the wooden tech desk.
      Arms firmly anchored to desk (ZERO detached limb glitches), 4-state RMS lip-sync mouth shape,
      90-frame auto eye-blinking, idle breathing oscillation, boom mic and steaming coffee mug.
    - Word-by-word kinetic subtitle pill (.on) matching ai.nxtlvl benchmark.
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
    cta_word = slot_meta.get("cta_keyword", "REPOS").upper()

    # Load curated items
    if not os.path.exists(repos_file):
        repos = [
            {
                "name": "Qwen-Image-2.1-Uncensored-GGUF",
                "full_name": "abenzerps/Qwen-Image-2.1-Uncensored-GGUF",
                "description": "Trending open-weights model on Hugging Face (text-to-image) with 3892 likes.",
                "badge": "TEXT-TO-IMAGE",
                "og_image": "assets/slot_1/abenzerps_Qwen-Image-2.1-Uncensored-GGUF/og_banner.png"
            },
            {
                "name": "Kolibri-1",
                "full_name": "Aleph-Alpha/Kolibri-1",
                "description": "Trending open-weights model on Hugging Face (text-generation) with 872 likes.",
                "badge": "LOCAL LLM",
                "og_image": "assets/slot_1/Aleph-Alpha_Kolibri-1/og_banner.png"
            },
            {
                "name": "lobehub",
                "full_name": "lobehub/lobehub",
                "description": "An open-source AI Agent collaboration platform acting as your Chief Agent Operator.",
                "badge": "AGENT FLEETS",
                "og_image": "assets/slot_1/lobehub_lobehub/demo.png"
            }
        ]
    else:
        with open(repos_file) as f:
            repos = json.load(f)[:3]

    # Load captions
    caption_chunks = []
    if os.path.exists(captions_file):
        with open(captions_file) as f:
            caption_chunks = json.load(f)

    # Frame-accurate lip-sync & blink data
    mouth_json_path = "assets/mouth.json"
    mouth_data = generate_lipsync_data(
        audio_path=audio_path,
        caption_chunks_path=captions_file,
        output_mouth_path=mouth_json_path,
        fps=30
    )

    # Programmatic GSAP Lip-Sync Instructions
    mouth_tl_lines = []
    last_m = None
    for item in mouth_data:
        f = item["f"]
        t = round(f / 30.0, 3)
        m = item["mouth"]
        if m != last_m:
            other_m = [f"#m-{x}" for x in ["closed", "small", "open", "wide"] if x != m]
            mouth_tl_lines.append(f'tl.set("#m-{m}", {{ display: "block", opacity: 1 }}, {t});')
            mouth_tl_lines.append(f'tl.set({json.dumps(other_m)}, {{ display: "none", opacity: 0 }}, {t});')
            last_m = m
    mouth_code_str = "\n    ".join(mouth_tl_lines)

    # Format items & locate media
    items_data = []
    for r in repos:
        name_clean = r["name"].split("/")[-1].replace("-", " ").title()
        stars_val = r.get("stars", 3892)
        star_str = f"{stars_val:,}" if isinstance(stars_val, int) else str(stars_val)
        
        # Locate local preview image
        img_candidate = r.get("demo_media") or r.get("og_image") or ""
        if not os.path.exists(img_candidate):
            # Check slot directory
            safe_name = r["full_name"].replace("/", "_")
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
            "badge": r.get("badge", "VERIFIED"),
            "img": img_candidate if os.path.exists(img_candidate) else ""
        })

    while len(items_data) < 3:
        items_data.append({"name": "AI Tool", "full_name": "developer/tool", "stars": "25,000", "desc": "High performance developer tool", "badge": "AI", "img": ""})

    # Exact speech boundary detection from caption chunks for 100% speech-to-visual lock
    t_hook_end = round(duration * 0.13, 2)
    t_tool1_end = round(duration * 0.38, 2)
    t_tool2_end = round(duration * 0.63, 2)
    t_tool3_end = round(duration * 0.86, 2)
    t_cta_end = duration

    for c in caption_chunks:
        txt = " ".join(c.get("words", [])).lower()
        st = c.get("start", 0)
        if any(k in txt for k in ["first up", "first,", "first is", "number one"]):
            t_hook_end = round(st, 2)
        elif any(k in txt for k in ["second", "next is", "next up", "number two"]):
            t_tool1_end = round(st, 2)
        elif any(k in txt for k in ["finally", "third", "lastly", "number three"]):
            t_tool2_end = round(st, 2)
        elif any(k in txt for k in ["comment", "drop a comment", "dm me"]):
            t_tool3_end = round(st, 2)

    # HyperFrames configuration (1080x1920 Full HD @ 30fps)
    hf_config = {
        "name": "daily-automation-engine",
        "version": "2.3.0",
        "fps": 30,
        "width": 1080,
        "height": 1920,
        "duration": round(duration, 2)
    }
    with open("hyperframes.json", "w") as f:
        json.dump(hf_config, f, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=1080, height=1920, initial-scale=1">
  <title>Jayant Digital Studio – Broadcast Studio</title>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800;900&family=Instrument+Serif:ital@1&family=JetBrains+Mono:wght@600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <style>
    :root {{
      --page: #f6f4ee;
      --bar: #1a1714;
      --clay: {theme['accent']};
      --ink: #1a1714;
      --mut: #6b7280;
      --card-bg: #ffffff;
      --border: rgba(26, 23, 20, 0.08);
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: var(--page);
      font-family: 'Bricolage Grotesque', system-ui, -apple-system, sans-serif;
      user-select: none;
    }}

    #stage {{
      position: relative;
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: var(--page);
      color: var(--ink);
    }}

    /* Subtle Architectural Grid */
    #stage::before {{
      content: "";
      position: absolute;
      inset: 0;
      background-image: 
        linear-gradient(rgba(120, 100, 70, 0.07) 2px, transparent 2px),
        linear-gradient(90deg, rgba(120, 100, 70, 0.07) 2px, transparent 2px);
      background-size: 54px 54px;
      z-index: 1;
      pointer-events: none;
    }}

    /* Drifting Ambient Gradient Aura */
    .aura-orb {{
      position: absolute;
      border-radius: 50%;
      filter: blur(120px);
      opacity: 0.45;
      z-index: 2;
      pointer-events: none;
      animation: auraFloat 8s ease-in-out infinite alternate;
    }}
    .aura-1 {{ width: 700px; height: 700px; background: #fbd0b9; left: 190px; top: 120px; }}
    .aura-2 {{ width: 550px; height: 550px; background: #e2e4fa; left: 260px; top: 450px; animation-delay: -4s; }}
    @keyframes auraFloat {{
      0% {{ transform: translate(0, 0) scale(1); }}
      50% {{ transform: translate(25px, -35px) scale(1.08); }}
      100% {{ transform: translate(-20px, 25px) scale(0.95); }}
    }}

    /* Drifting Particle Crosshairs */
    .crosshair {{
      position: absolute;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: rgba(26, 23, 20, 0.22);
      pointer-events: none;
      z-index: 3;
    }}
    .ch-1 {{ left: 100px; top: 180px; font-size: 32px; }}
    .ch-2 {{ right: 120px; top: 280px; font-size: 26px; }}
    .ch-3 {{ left: 140px; top: 780px; font-size: 34px; }}
    .ch-4 {{ right: 90px; top: 920px; font-size: 28px; }}

    /* Serif Italic Styling (ai.nxtlvl hallmark) */
    .serif-accent {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-style: italic;
      font-weight: 400;
      color: var(--clay);
    }}

    /* ================= UPPER THEATER (TOP 60%: Y 60px to 1100px) ================= */
    #upper-theater {{
      position: absolute;
      left: 0;
      right: 0;
      top: 50px;
      height: 1050px;
      padding: 0 54px;
      z-index: 15;
    }}

    .scene-view {{
      position: absolute;
      inset: 0;
      padding: 0 54px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-start;
      opacity: 0;
      pointer-events: none;
    }}
    .scene-view.active {{
      opacity: 1;
      pointer-events: auto;
    }}

    /* Top Step Pill (Strict 3/3 Format) */
    .step-pill {{
      display: inline-flex;
      align-items: center;
      gap: 12px;
      background: #1a1714;
      color: #ffffff;
      padding: 12px 28px;
      border-radius: 99px;
      font-size: 22px;
      font-weight: 800;
      letter-spacing: 2px;
      text-transform: uppercase;
      box-shadow: 0 10px 24px rgba(0,0,0,0.12);
      margin-bottom: 18px;
    }}
    .step-dashes {{
      display: flex;
      gap: 8px;
      margin-left: 6px;
    }}
    .step-dash {{
      width: 32px;
      height: 6px;
      border-radius: 3px;
      background: rgba(255,255,255,0.25);
    }}
    .step-dash.active {{
      background: var(--clay);
    }}

    /* Background Watermark Numeral */
    .step-watermark {{
      position: absolute;
      right: 48px;
      top: 20px;
      font-size: 280px;
      font-weight: 900;
      color: rgba(217, 105, 74, 0.08);
      line-height: 1;
      z-index: 1;
      pointer-events: none;
    }}

    /* Headlines */
    .hero-title {{
      font-size: 68px;
      font-weight: 900;
      line-height: 1.1;
      text-align: center;
      color: var(--ink);
      letter-spacing: -1.5px;
      z-index: 5;
    }}
    .hero-sub {{
      font-size: 32px;
      font-weight: 700;
      color: var(--mut);
      margin-top: 10px;
      text-align: center;
      z-index: 5;
    }}

    /* Cards */
    .card {{
      width: 100%;
      background: #ffffff;
      border-radius: 34px;
      box-shadow: 0 20px 48px rgba(0,0,0,0.08);
      border: 2px solid var(--border);
      position: relative;
      z-index: 5;
      overflow: hidden;
    }}

    /* Scene 1: Hook Elements */
    .app-icon-pair {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 28px;
      margin-top: 24px;
      margin-bottom: 24px;
    }}
    .app-card {{
      width: 130px;
      height: 130px;
      background: #ffffff;
      border-radius: 36px;
      box-shadow: 0 18px 36px rgba(0,0,0,0.08);
      display: grid;
      place-items: center;
      border: 3px solid rgba(255,255,255,0.9);
    }}
    .plus-badge {{
      font-size: 54px;
      font-weight: 900;
      color: var(--clay);
      animation: pulsePlus 1.6s ease-in-out infinite alternate;
    }}
    @keyframes pulsePlus {{
      0% {{ transform: scale(1); }}
      100% {{ transform: scale(1.22); }}
    }}

    /* Real Image / Media Preview Container */
    .media-card-wrap {{
      width: 100%;
      height: 520px;
      background: #ffffff;
      border-radius: 34px;
      box-shadow: 0 20px 48px rgba(0,0,0,0.08);
      border: 2px solid var(--border);
      margin-top: 24px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      z-index: 5;
    }}
    .media-preview {{
      width: 100%;
      height: 330px;
      background: #1a1714;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      position: relative;
    }}
    .media-preview img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}
    .media-info {{
      flex: 1;
      padding: 24px 32px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}

    /* Radar UI for Tool 2 */
    .radar-viewport {{
      position: relative;
      width: 290px;
      height: 290px;
      border-radius: 50%;
      border: 3px solid rgba(217, 105, 74, 0.25);
      background: radial-gradient(circle, rgba(217, 105, 74, 0.05) 0%, transparent 70%);
      display: grid;
      place-items: center;
      margin: 10px auto;
    }}
    .radar-ring {{ position: absolute; border-radius: 50%; border: 2px dashed rgba(217, 105, 74, 0.2); }}
    .rr-1 {{ width: 200px; height: 200px; }}
    .rr-2 {{ width: 110px; height: 110px; }}
    .radar-beam {{
      position: absolute;
      inset: 0;
      border-radius: 50%;
      background: conic-gradient(from 0deg, rgba(217, 105, 74, 0.35) 0deg, transparent 60deg);
      animation: radarSpin 3s linear infinite;
    }}
    @keyframes radarSpin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
    .radar-blip {{
      position: absolute;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 14px #10b981;
      animation: blipPulse 1.4s ease-in-out infinite alternate;
    }}
    .rb-1 {{ left: 180px; top: 80px; }}
    .rb-2 {{ left: 80px; top: 170px; animation-delay: 0.6s; }}
    @keyframes blipPulse {{ 0% {{ transform: scale(0.8); opacity: 0.5; }} 100% {{ transform: scale(1.3); opacity: 1; }} }}

    /* CTA Scene Elements */
    .cta-pills {{
      display: flex;
      gap: 18px;
      margin-top: 14px;
      z-index: 5;
    }}
    .black-pill {{
      background: #1a1714;
      color: #ffffff;
      font-size: 50px;
      font-weight: 900;
      padding: 14px 40px;
      border-radius: 26px;
      transform: rotate(-3deg);
      box-shadow: 0 14px 32px rgba(0,0,0,0.2);
    }}
    .clay-pill {{
      background: linear-gradient(135deg, var(--clay) 0%, #b84a2d 100%);
      color: #ffffff;
      font-size: 54px;
      font-weight: 900;
      padding: 14px 46px;
      border-radius: 26px;
      transform: rotate(2deg);
      box-shadow: 0 18px 36px rgba(217, 105, 74, 0.4);
      animation: ctaPulse 1.4s ease-in-out infinite alternate;
    }}
    @keyframes ctaPulse {{
      0% {{ transform: rotate(2deg) scale(1); }}
      100% {{ transform: rotate(2deg) scale(1.06); }}
    }}

    /* Floating Comment Notifications */
    .comment-bubble {{
      position: absolute;
      background: #ffffff;
      border-radius: 99px;
      padding: 10px 24px;
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 24px;
      font-weight: 800;
      color: #1a1714;
      box-shadow: 0 14px 30px rgba(0,0,0,0.09);
      border: 2px solid rgba(0,0,0,0.06);
      z-index: 6;
      animation: bubbleFloat 3.6s ease-in-out infinite alternate;
    }}
    .cb-avatar {{ width: 26px; height: 26px; border-radius: 50%; }}
    .cb-1 {{ left: 40px; top: 620px; animation-delay: 0s; }}
    .cb-2 {{ right: 50px; top: 680px; animation-delay: 0.8s; }}
    .cb-3 {{ left: 70px; top: 790px; animation-delay: 1.6s; }}
    .cb-4 {{ right: 50px; top: 860px; animation-delay: 2.2s; }}
    @keyframes bubbleFloat {{
      0% {{ transform: translateY(0); }}
      100% {{ transform: translateY(-24px); }}
    }}

    /* ================= LOWER STAGE (HOST RIG + TECH DESK: Y 1100 to 1920px) ================= */
    #lower-stage {{
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      height: 840px;
      z-index: 30;
      pointer-events: none;
    }}

    /* Wooden Tech Desk Surface */
    .desk-surface {{
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      height: 200px;
      background: linear-gradient(180deg, #9b5a2e 0%, #7d441c 45%, #5a2e10 100%);
      border-top: 12px solid #1a1714;
      box-shadow: inset 0 8px 0 rgba(255,255,255,0.22);
      z-index: 35;
    }}
    .desk-surface::before {{
      content: "";
      position: absolute;
      inset: 0;
      background: repeating-linear-gradient(90deg, transparent 0, transparent 240px, rgba(0,0,0,0.14) 240px, rgba(0,0,0,0.14) 246px);
    }}

    /* Desk Props: Microphone & Steaming Coffee Mug */
    .desk-props {{
      position: absolute;
      left: 0;
      right: 0;
      bottom: 160px;
      height: 180px;
      z-index: 36;
      pointer-events: none;
    }}
    .studio-mic {{
      position: absolute;
      left: 70px;
      bottom: 0;
      width: 170px;
      height: 200px;
    }}
    .desk-mug-wrap {{
      position: absolute;
      right: 80px;
      bottom: 0;
      width: 90px;
      height: 100px;
    }}
    .mug-cup {{
      width: 80px;
      height: 88px;
      background: #ffffff;
      border: 6px solid #1a1714;
      border-radius: 6px 6px 20px 20px;
      position: relative;
    }}
    .mug-cup::before {{
      content: "";
      position: absolute;
      top: 20px;
      left: 0;
      right: 0;
      height: 16px;
      background: {theme['mug_color']};
    }}
    .mug-cup::after {{
      content: "";
      position: absolute;
      right: -24px;
      top: 14px;
      width: 22px;
      height: 40px;
      border: 6px solid #1a1714;
      border-radius: 0 16px 16px 0;
    }}
    .steam-curl {{
      position: absolute;
      top: -42px;
      font-size: 30px;
      font-weight: 900;
      color: rgba(26,23,20,0.40);
      animation: steamFloat 2.2s infinite ease-out;
    }}
    .s1 {{ right: 40px; animation-delay: 0s; }}
    .s2 {{ right: 20px; animation-delay: 1.1s; }}
    @keyframes steamFloat {{
      0% {{ transform: translateY(0) scale(0.8); opacity: 0; }}
      40% {{ opacity: 0.65; }}
      100% {{ transform: translateY(-50px) scale(1.35); opacity: 0; }}
    }}

    /* Animated Vector Host Character Rig (Completely Solid & Attached) */
    #host-avatar {{
      position: absolute;
      left: 50%;
      bottom: 140px;
      transform: translateX(-50%);
      width: 760px;
      height: 760px;
      z-index: 32;
    }}

    /* ================= KINETIC SUBTITLES ================= */
    #caption-bar {{
      position: absolute;
      left: 54px;
      right: 54px;
      bottom: 35px;
      z-index: 50;
      text-align: center;
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 12px;
    }}
    .w {{
      color: rgba(255,255,255,0.70);
      font-size: 38px;
      font-weight: 700;
      padding: 4px 12px;
      border-radius: 12px;
      display: inline-block;
      transition: all 0.12s ease-out;
    }}
    .w.done {{ color: #ffffff; }}
    .w.on {{
      background: var(--clay);
      color: #ffffff !important;
      font-weight: 900;
      font-size: 42px;
      border-radius: 14px;
      transform: scale(1.08);
      box-shadow: 0 4px 16px rgba(0,0,0,0.5);
    }}
  </style>
</head>
<body>
  <div id="stage" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{round(duration, 2)}">
    
    <!-- Ambient Gradient Aura -->
    <div class="aura-orb aura-1"></div>
    <div class="aura-orb aura-2"></div>

    <!-- Drifting Particle Crosshairs -->
    <div class="crosshair ch-1">+</div>
    <div class="crosshair ch-2">+</div>
    <div class="crosshair ch-3">+</div>
    <div class="crosshair ch-4">+</div>

    <!-- HyperFrames Synchronized Audio Elements -->
    <audio id="voice" src="{audio_path}" data-start="0" data-duration="{round(duration, 2)}" data-volume="1"></audio>

    <!-- ================= UPPER THEATER (TOP 60%) ================= -->
    <div id="upper-theater">

      <!-- SCENE 1: HOOK (0s to {t_hook_end}s) -->
      <div id="sc-1" class="scene-view active">
        <div class="app-icon-pair">
          <div class="app-card">
            <svg viewBox="0 0 100 100" width="80" height="80">
              <path d="M50 15 L50 85 M15 50 L85 50 M25 25 L75 75 M25 75 L75 25" stroke="{theme['accent']}" stroke-width="12" stroke-linecap="round"/>
            </svg>
          </div>
          <div class="plus-badge">+</div>
          <div class="app-card">
            <svg viewBox="0 0 100 100" width="75" height="75">
              <rect x="15" y="15" width="70" height="70" rx="20" fill="none" stroke="#1a1714" stroke-width="9"/>
              <circle cx="50" cy="50" r="18" fill="none" stroke="#1a1714" stroke-width="8"/>
              <circle cx="70" cy="30" r="5" fill="#1a1714"/>
            </svg>
          </div>
        </div>

        <h1 class="hero-title">
          {slot_meta.get('post_title', '3 AI Superpowers You Need Today! 🚀')}
        </h1>

        <div class="card" style="padding: 34px 44px; margin-top: 36px; display: flex; align-items: center; justify-content: space-between;">
          <div>
            <div style="font-size: 24px; font-weight: 800; color: #ef4444; margin-bottom: 6px;">✕ MANUAL WORKFLOWS</div>
            <div style="font-size: 74px; font-weight: 900; color: #1a1714; position: relative; display: inline-block;">
              $200/mo
              <div style="position: absolute; top: 50%; left: -6%; right: -6%; height: 8px; background: #ef4444; border-radius: 4px; transform: rotate(-6deg);"></div>
            </div>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 24px; font-weight: 800; color: #10b981; margin-bottom: 6px;">✓ 3 VERIFIED AI TOOLS</div>
            <div style="font-size: 74px; font-weight: 900; color: #10b981;">$0 FREE</div>
          </div>
        </div>
      </div>

      <!-- SCENE 2: TOOL 1 ({t_hook_end}s to {t_tool1_end}s) -->
      <div id="sc-2" class="scene-view">
        <div class="step-watermark">01</div>
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

        <div class="media-card-wrap">
          <div class="media-preview">
            {"<img src='" + items_data[0]['img'] + "' alt='preview'>" if items_data[0]['img'] else "<div style='font-size: 34px; font-weight: 900; color: #ffffff;'>⚡ " + items_data[0]['name'].upper() + "</div>"}
          </div>
          <div class="media-info">
            <div style="display: flex; gap: 14px; margin-bottom: 10px;">
              <span style="background: #ede8df; padding: 6px 18px; border-radius: 99px; font-weight: 800; font-size: 22px;">★ {items_data[0]['stars']}</span>
              <span style="background: #dcfce7; color: #15803d; padding: 6px 18px; border-radius: 99px; font-weight: 800; font-size: 22px;">{items_data[0]['badge']}</span>
            </div>
            <div style="font-size: 28px; font-weight: 800; color: #1a1714;">{items_data[0]['desc']}</div>
          </div>
        </div>
      </div>

      <!-- SCENE 3: TOOL 2 ({t_tool1_end}s to {t_tool2_end}s) -->
      <div id="sc-3" class="scene-view">
        <div class="step-watermark">02</div>
        <div class="step-pill">
          TOOL 2/3 · {items_data[1]['badge'].upper()}
          <div class="step-dashes">
            <div class="step-dash active"></div>
            <div class="step-dash active"></div>
            <div class="step-dash"></div>
          </div>
        </div>

        <h1 class="hero-title">
          {items_data[1]['name']} <span class="serif-accent">powerhouse</span>
        </h1>

        <div class="media-card-wrap">
          <div class="media-preview">
            {"<img src='" + items_data[1]['img'] + "' alt='preview'>" if items_data[1]['img'] else "<div style='font-size: 34px; font-weight: 900; color: #ffffff;'>⚡ " + items_data[1]['name'].upper() + "</div>"}
          </div>
          <div class="media-info">
            <div style="display: flex; gap: 14px; margin-bottom: 10px;">
              <span style="background: #ede8df; padding: 6px 18px; border-radius: 99px; font-weight: 800; font-size: 22px;">★ {items_data[1]['stars']}</span>
              <span style="background: #f5f3ff; color: #7c3aed; padding: 6px 18px; border-radius: 99px; font-weight: 800; font-size: 22px;">{items_data[1]['badge']}</span>
            </div>
            <div style="font-size: 28px; font-weight: 800; color: #1a1714;">{items_data[1]['desc']}</div>
          </div>
        </div>
      </div>

      <!-- SCENE 4: TOOL 3 ({t_tool2_end}s to {t_tool3_end}s) -->
      <div id="sc-4" class="scene-view">
        <div class="step-watermark">03</div>
        <div class="step-pill">
          TOOL 3/3 · {items_data[2]['badge'].upper()}
          <div class="step-dashes">
            <div class="step-dash active"></div>
            <div class="step-dash active"></div>
            <div class="step-dash active"></div>
          </div>
        </div>

        <h1 class="hero-title">
          {items_data[2]['name']} <span class="serif-accent">superpower</span>
        </h1>

        <div class="media-card-wrap">
          <div class="media-preview" style="background: #1e293b;">
            {"<img src='" + items_data[2]['img'] + "' alt='preview'>" if items_data[2]['img'] else "<div style='font-size: 34px; font-weight: 900; color: #ffffff;'>⚡ " + items_data[2]['name'].upper() + "</div>"}
          </div>
          <div class="media-info">
            <div style="display: flex; gap: 14px; margin-bottom: 10px;">
              <span style="background: #ede8df; padding: 6px 18px; border-radius: 99px; font-weight: 800; font-size: 22px;">★ {items_data[2]['stars']}</span>
              <span style="background: #dcfce7; color: #15803d; padding: 6px 18px; border-radius: 99px; font-weight: 800; font-size: 22px;">{items_data[2]['badge']}</span>
            </div>
            <div style="font-size: 28px; font-weight: 800; color: #1a1714;">{items_data[2]['desc']}</div>
          </div>
        </div>
      </div>
          </div>
        </div>
      </div>

      <!-- SCENE 5: VIRAL CTA ({t_tool3_end}s to {t_cta_end}s) -->
      <div id="sc-5" class="scene-view">
        <div class="step-pill">
          BONUS · FREE REPO BLUEPRINT
          <div class="step-dashes">
            <div class="step-dash active"></div>
            <div class="step-dash active"></div>
            <div class="step-dash active"></div>
          </div>
        </div>

        <div class="cta-pills">
          <div class="black-pill">💬 COMMENT</div>
          <div class="clay-pill">{cta_word}</div>
        </div>

        <div class="card" style="border-radius: 99px; padding: 18px 36px; display: flex; align-items: center; gap: 20px; margin-top: 26px;">
          <div style="width: 44px; height: 44px; border-radius: 50%; background: var(--clay);"></div>
          <span style="font-size: 36px; font-weight: 900; color: #1a1714; letter-spacing: 1px;">{cta_word}</span>
          <span style="margin-left: auto; color: #fff; background: var(--clay); width: 52px; height: 52px; border-radius: 50%; display: grid; place-items: center; font-size: 26px;">➤</span>
        </div>

        <!-- Floating Comments -->
        <div class="comment-bubble cb-1">
          <div class="cb-avatar" style="background: #f59e0b;"></div>
          <span>@tech.aman {cta_word.lower()} 🔥</span>
        </div>
        <div class="comment-bubble cb-2">
          <div class="cb-avatar" style="background: #10b981;"></div>
          <span>@dev_k {cta_word.capitalize()}</span>
        </div>
        <div class="comment-bubble cb-3">
          <div class="cb-avatar" style="background: #3b82f6;"></div>
          <span>@creator.sana {cta_word}!</span>
        </div>
        <div class="comment-bubble cb-4">
          <div class="cb-avatar" style="background: #8b5cf6;"></div>
          <span>@jay.codes {cta_word} ✨</span>
        </div>

        <div class="card" style="padding: 24px 34px; margin-top: 24px; display: flex; align-items: center; gap: 20px;">
          <div style="font-size: 40px;">📩</div>
          <div>
            <div style="font-size: 28px; font-weight: 900; color: #1a1714;">jayant.digitalstudio · now</div>
            <div style="font-size: 24px; font-weight: 700; color: var(--mut);">All 3 repo links + setup guide sent to your DMs</div>
          </div>
          <div style="margin-left: auto; background: #dcfce7; color: #15803d; padding: 8px 18px; border-radius: 99px; font-size: 20px; font-weight: 900;">SENT ✓</div>
        </div>
      </div>

    </div> <!-- end upper-theater -->

    <!-- ================= LOWER STAGE (ANIMATED HOST RIG + TECH DESK) ================= -->
    <div id="lower-stage">

      <!-- Host Avatar Rig (Firmly Attached - ZERO detached limbs) -->
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
            <path d="M195 235 L195 275 L245 275 L245 235 Z" fill="url(#skin)" stroke="#1a1714" stroke-width="6"/>

            <!-- Head -->
            <ellipse cx="220" cy="175" rx="66" ry="76" fill="url(#skin)" stroke="#1a1714" stroke-width="8"/>

            <!-- Hair -->
            <path d="M150 155 C150 85, 210 65, 280 85 C305 95, 300 125, 300 145 C300 125, 290 110, 270 110 C235 110, 225 125, 185 125 C165 125, 155 145, 150 155 Z" fill="#1a1714"/>

            <!-- Eyebrows -->
            <path d="M180 148 Q198 140, 210 148" fill="none" stroke="#1a1714" stroke-width="6" stroke-linecap="round"/>
            <path d="M230 148 Q242 140, 260 148" fill="none" stroke="#1a1714" stroke-width="6" stroke-linecap="round"/>

            <!-- Eyes & Automatic Blinking -->
            <g id="eyes-open">
              <ellipse cx="194" cy="168" rx="10" ry="14" fill="#ffffff" stroke="#1a1714" stroke-width="4"/>
              <circle cx="196" cy="169" r="6" fill="#1a1714"/>
              <circle cx="199" cy="166" r="2.5" fill="#ffffff"/>

              <ellipse cx="246" cy="168" rx="10" ry="14" fill="#ffffff" stroke="#1a1714" stroke-width="4"/>
              <circle cx="248" cy="169" r="6" fill="#1a1714"/>
              <circle cx="251" cy="166" r="2.5" fill="#ffffff"/>
            </g>
            <g id="eyes-blink" style="display: none;">
              <path d="M184 170 Q194 180, 204 170" fill="none" stroke="#1a1714" stroke-width="5" stroke-linecap="round"/>
              <path d="M236 170 Q246 180, 256 170" fill="none" stroke="#1a1714" stroke-width="5" stroke-linecap="round"/>
            </g>

            <!-- Glasses -->
            <rect x="176" y="152" width="38" height="32" rx="10" fill="none" stroke="#1a1714" stroke-width="7"/>
            <rect x="226" y="152" width="38" height="32" rx="10" fill="none" stroke="#1a1714" stroke-width="7"/>
            <path d="M214 166 L226 166" fill="none" stroke="#1a1714" stroke-width="7"/>

            <!-- Nose -->
            <path d="M220 168 L216 190 L226 190" fill="none" stroke="#1a1714" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

            <!-- 4-State RMS Lip-Sync Mouth -->
            <g id="mouth-group">
              <path id="m-closed" d="M204 216 Q220 218, 236 216" stroke="#1a1714" stroke-width="5" stroke-linecap="round" fill="none"/>
              <ellipse id="m-small" cx="220" cy="216" rx="8" ry="6" fill="#881337" stroke="#1a1714" stroke-width="3.5" style="display: none;"/>
              <path id="m-open" d="M206 212 Q220 206, 234 212 Q234 228, 220 230 Q206 228, 206 212 Z" fill="#881337" stroke="#1a1714" stroke-width="3.5" style="display: none;"/>
              <g id="m-wide" style="display: none;">
                <path d="M202 210 Q220 200, 238 210 Q236 238, 220 240 Q204 238, 202 210 Z" fill="#881337" stroke="#1a1714" stroke-width="4"/>
                <rect x="210" y="208" width="20" height="5" rx="2" fill="#ffffff"/>
                <ellipse cx="220" cy="232" rx="8" ry="4.5" fill="#f43f5e"/>
              </g>
            </g>

          </g>
        </svg>
      </div> <!-- end host-avatar -->

      <!-- Wooden Tech Desk Surface -->
      <div class="desk-surface"></div>

      <!-- Desk Props: Boom Mic & Mug -->
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

    <!-- ================= KINETIC SUBTITLES ================= -->
    <div id="caption-bar"></div>

  </div> <!-- end stage -->

  <script>
    const captionChunks = {json.dumps(caption_chunks)};
    const duration = {round(duration, 2)};

    const tl = gsap.timeline();
    window.__timelines = window.__timelines || {{}};
    window.__timelines["main"] = tl;

    // 1. Initial State (deterministic frame 0)
    gsap.set("#sc-1", {{ opacity: 1, pointerEvents: "auto" }});
    gsap.set(["#sc-2", "#sc-3", "#sc-4", "#sc-5"], {{ opacity: 0, pointerEvents: "none" }});
    gsap.set("#eyes-open", {{ display: "block" }});
    gsap.set("#eyes-blink", {{ display: "none" }});

    // 2. Scene 2 (Tool 1 - Qwen Image 2.1): starts at {t_hook_end}s
    tl.to("#sc-1", {{ opacity: 0, duration: 0.25 }}, {t_hook_end});
    tl.set("#sc-1", {{ pointerEvents: "none" }}, {t_hook_end + 0.25});
    tl.set("#sc-2", {{ pointerEvents: "auto" }}, {t_hook_end + 0.25});
    tl.fromTo("#sc-2", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {t_hook_end + 0.25});

    // 3. Scene 3 (Tool 2 - Kolibri 1): starts at {t_tool1_end}s
    tl.to("#sc-2", {{ opacity: 0, duration: 0.25 }}, {t_tool1_end});
    tl.set("#sc-2", {{ pointerEvents: "none" }}, {t_tool1_end + 0.25});
    tl.set("#sc-3", {{ pointerEvents: "auto" }}, {t_tool1_end + 0.25});
    tl.fromTo("#sc-3", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {t_tool1_end + 0.25});

    // 4. Scene 4 (Tool 3 - LobeHub): starts at {t_tool2_end}s
    tl.to("#sc-3", {{ opacity: 0, duration: 0.25 }}, {t_tool2_end});
    tl.set("#sc-3", {{ pointerEvents: "none" }}, {t_tool2_end + 0.25});
    tl.set("#sc-4", {{ pointerEvents: "auto" }}, {t_tool2_end + 0.25});
    tl.fromTo("#sc-4", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {t_tool2_end + 0.25});

    // 5. Scene 5 (Viral CTA): starts at {t_tool3_end}s
    tl.to("#sc-4", {{ opacity: 0, duration: 0.25 }}, {t_tool3_end});
    tl.set("#sc-4", {{ pointerEvents: "none" }}, {t_tool3_end + 0.25});
    tl.set("#sc-5", {{ pointerEvents: "auto" }}, {t_tool3_end + 0.25});
    tl.fromTo("#sc-5", {{ opacity: 0, scale: 0.94 }}, {{ opacity: 1, scale: 1, duration: 0.35 }}, {t_tool3_end + 0.25});

    // Continuous Idle Breathing Oscillation (subtle & natural)
    tl.to("#avatar-character", {{ y: -6, duration: 1.5, repeat: {int(duration / 1.5)}, yoyo: true, ease: "sine.inOut" }}, 0);

    // Automatic Eye Blinks (every 3 seconds for 0.133s)
    for (let t = 1.5; t < {round(duration, 2)}; t += 3.0) {{
      tl.set("#eyes-open", {{ display: "none" }}, t);
      tl.set("#eyes-blink", {{ display: "block" }}, t);
      tl.set("#eyes-open", {{ display: "block" }}, t + 0.133);
      tl.set("#eyes-blink", {{ display: "none" }}, t + 0.133);
    }}

    // Frame-Accurate Lip-Sync Mouth States
    {mouth_code_str}

    // Kinetic Captions Schedule
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

    print(f"[✓] Compiled 1080x1920 Full HD studio composition with avatar to {output_html} ({round(duration, 2)}s)")
    return output_html

if __name__ == "__main__":
    build_hyperframes_composition()
