import json
import os
import sys
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipeline.lipsync_engine import generate_lipsync_data

SLOT_VISUAL_THEMES = {
    1: {
        "name": "CYBER_OPENSOURCE",
        "badge_pill": "⚡ OPEN SOURCE AI",
        "accent": "#d9694a",       # Brand Clay
        "accent_bg": "#fbeae5",
        "hoodie_color": "#1f1d1a", # Charcoal Studio
        "hoodie_trim": "#d9694a",
        "mug_color": "#d9694a",
        "initial_pose": "facepalm",
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
        "initial_pose": "facepalm",
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
        "initial_pose": "pointLeft",
        "tagline": "New SOTA Architecture Teardown"
    },
    4: {
        "name": "SECRET_TOOLS",
        "badge_pill": "🛠️ SECRET NO-CODE TOOLS",
        "accent": "#ea580c",       # Sunset Coral
        "accent_bg": "#fff7ed",
        "hoodie_color": "#2c1710",
        "hoodie_trim": "#f97316",
        "mug_color": "#f97316",
        "initial_pose": "wave",
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
        "initial_pose": "facepalm",
        "tagline": "Zero Hallucination Framework"
    }
}

def build_hyperframes_composition(
    repos_file="assets/curated_repos.json",
    captions_file="assets/caption_chunks.json",
    audio_path="assets/voice.mp3",
    script_file="assets/generated_script.json",
    duration=38.0,
    output_html="index.html",
    slot_meta=None
):
    """
    1080x1920 Full HD High-Visibility Kinetic Visuals & Professional Host Vector Rig:
    - High-density editorial brutalist styling matching user's reference HTML
    - Large 68px titles, 36px-38px high-contrast descriptions, 240px strike numbers, 160px counters
    - Vector Host Character Rig with natural shoulder width and posture
    - Sleek broadcast tech desk with boom mic and steaming mug
    - 4-state RMS lip-sync & 90-frame auto eye-blinking
    - 5 Arm variant switcher: idle, wave, pointUp, pointLeft, facepalm (with sweat drop 💦)
    - Kinetic Subtitles with clay active-word highlight pill (.on)
    - Zero dead space: cards span Y:70-1140, host spans Y:1120-1700, desk spans Y:1700-1920
    """
    if slot_meta is None:
        slot_meta = {
            "slot_id": 1,
            "badge_title": "AI OPEN SOURCE",
            "badge_sub": "3 VERIFIED REPOS",
            "cta_keyword": "REPOS"
        }

    sid = slot_meta.get("slot_id", 1)
    theme = SLOT_VISUAL_THEMES.get(sid, SLOT_VISUAL_THEMES[1])

    # Ensure curated items
    if not os.path.exists(repos_file):
        repos = [
            {"name": "Local-LLM", "full_name": "ollama/ollama", "stars": 115000, "description": "Run open frontier models locally on your laptop with one command."},
            {"name": "Browser-Agent", "full_name": "browser-use/browser-use", "stars": 42000, "description": "Autonomous AI agent that browses and controls the web seamlessly."},
            {"name": "Firecrawl", "full_name": "mendableai/firecrawl", "stars": 28500, "description": "Converts entire websites into clean LLM-ready markdown."}
        ]
    else:
        with open(repos_file) as f:
            repos = json.load(f)[:3]

    # Ensure captions
    caption_chunks = []
    if os.path.exists(captions_file):
        with open(captions_file) as f:
            caption_chunks = json.load(f)

    # Ensure frame-accurate lip-sync & blink data
    mouth_json_path = "assets/mouth.json"
    if not os.path.exists(mouth_json_path):
        mouth_data = generate_lipsync_data(
            audio_path=audio_path,
            caption_chunks_path=captions_file,
            output_mouth_path=mouth_json_path,
            fps=30
        )
    else:
        with open(mouth_json_path) as mf:
            mouth_data = json.load(mf)

    # Scene timings
    t_hook_end = min(4.2, duration * 0.14)
    t_tool1_end = duration * 0.42
    t_tool2_end = duration * 0.70
    t_tool3_end = duration * 0.88
    t_cta_end = duration

    # Format item display data
    items_data = []
    for r in repos:
        name_clean = r["name"].split("/")[-1]
        stars_val = r.get("stars", 15000)
        star_str = f"{stars_val:,}" if isinstance(stars_val, int) else str(stars_val)
        items_data.append({
            "name": name_clean,
            "full_name": r.get("full_name", r["name"]),
            "stars": star_str,
            "desc": r.get("description", "")[:100],
            "badge": r.get("badge", "VERIFIED")
        })
    while len(items_data) < 3:
        items_data.append({"name": "AI Tool", "full_name": "developer/tool", "stars": "25,000", "desc": "High performance developer tool", "badge": "AI"})

    # Exact 1080x1920 Full HD configuration
    hf_config = {
        "name": "daily-automation-engine",
        "version": "2.0.0",
        "fps": 30,
        "width": 1080,
        "height": 1920,
        "duration": round(duration, 2)
    }
    with open("hyperframes.json", "w") as f:
        json.dump(hf_config, f, indent=2)

    cta_word = slot_meta.get("cta_keyword", "TOOLS").upper()

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

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=1080, height=1920, initial-scale=1">
  <title>Jayant Digital Studio – Full HD Broadcast</title>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800;900&family=Instrument+Serif:ital@1&family=JetBrains+Mono:wght@700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <style>
    :root {{
      --page: #f4f1ea;
      --bar: #1a1714;
      --clay: {theme['accent']};
      --ink: #1a1714;
      --mut: #8c857b;
      box-sizing: border-box;
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

    /* Architectural background grid */
    #stage::before {{
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

    /* Soft ambient drifting blobs */
    .blob {{
      position: absolute;
      border-radius: 50%;
      filter: blur(100px);
      opacity: 0.60;
      z-index: 2;
      pointer-events: none;
    }}
    .b1 {{ width: 600px; height: 600px; background: #f6c6b0; left: -150px; top: 100px; }}
    .b2 {{ width: 550px; height: 550px; background: #cfd2f3; right: -150px; top: 50px; }}
    .b3 {{ width: 680px; height: 500px; background: #f9d9c4; left: 120px; top: 600px; }}

    /* ================= UPPER THEATER (TOP 58%) ================= */
    #upper-theater {{
      position: absolute;
      left: 0;
      right: 0;
      top: 100px;
      height: 1040px;
      padding: 0 48px;
      z-index: 15;
    }}

    .scene-view {{
      position: absolute;
      inset: 0 48px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 30px;
      opacity: 0;
      pointer-events: none;
    }}
    .scene-view.active {{
      opacity: 1;
      pointer-events: auto;
    }}

    /* Header Pill Badge */
    .pill {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 28px;
      font-weight: 800;
      padding: 12px 34px;
      border-radius: 99px;
      background: #1a1714;
      color: #ffffff;
      box-shadow: 0 8px 20px rgba(0,0,0,0.15);
      display: inline-flex;
      align-items: center;
      gap: 12px;
    }}

    /* Clean Brutalist / Editorial Card */
    .card {{
      background: #ffffff;
      border-radius: 32px;
      box-shadow: 0 20px 48px rgba(70, 45, 20, 0.14);
      border: 5px solid #1a1714;
      padding: 38px 44px;
      width: 100%;
      max-width: 984px;
    }}

    h2 {{
      margin: 0;
      font-size: 70px;
      font-weight: 800;
      letter-spacing: -0.025em;
      line-height: 1.14;
      color: var(--ink);
      text-align: center;
    }}
    em {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-style: italic;
      font-weight: 400;
      color: var(--clay);
      font-size: 1.18em;
    }}

    /* Big Numbers & Strike-through */
    .big-wrap {{
      position: relative;
      margin: 15px 0 10px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .big-num {{
      font-size: 250px;
      font-weight: 900;
      line-height: 1;
      color: var(--ink);
      position: relative;
    }}
    .big-strike {{
      position: absolute;
      left: -24px;
      top: 50%;
      height: 26px;
      background: #ef4444;
      border-radius: 12px;
      width: calc(100% + 48px);
      transform: rotate(-9deg);
    }}
    .cnt {{
      font-size: 190px;
      font-weight: 900;
      color: var(--clay);
      line-height: 1;
    }}

    /* High Visibility List Card */
    .list-card {{
      width: 100%;
      padding: 26px 36px;
    }}
    .list-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 34px;
      font-weight: 800;
      padding: 22px 0;
      border-top: 2px solid #ede8df;
    }}
    .list-row:first-child {{ border-top: none; }}
    .bar-track {{
      width: 300px;
      height: 26px;
      border-radius: 99px;
      background: #ede8df;
      overflow: hidden;
      border: 2px solid #1a1714;
    }}
    .bar-fill {{
      height: 100%;
      background: var(--clay);
      border-radius: 99px;
    }}
    .tag {{
      font-size: 28px;
      font-weight: 800;
      background: #ece8df;
      color: #374151;
      padding: 10px 26px;
      border-radius: 99px;
      border: 2px solid rgba(0,0,0,0.08);
    }}

    /* Media Package Card */
    .pk-card {{
      display: flex;
      gap: 30px;
      align-items: center;
      padding: 34px 40px;
    }}
    .pk-thumb {{
      width: 220px;
      height: 140px;
      border-radius: 22px;
      background: #1a1714;
      color: #fff;
      display: grid;
      place-items: center;
      text-align: center;
      font-size: 28px;
      font-weight: 900;
      line-height: 1.15;
      flex-shrink: 0;
      border: 4px solid #1a1714;
      box-shadow: 5px 5px 0 #1a1714;
    }}
    .pk-info {{
      flex: 1;
    }}
    .pk-info h3 {{
      font-size: 46px;
      font-weight: 800;
      line-height: 1.2;
      color: var(--ink);
    }}
    .pk-info p {{
      font-size: 38px;
      font-weight: 700;
      line-height: 1.38;
      color: #1a1714;
      margin-top: 10px;
    }}

    /* Benchmark Duel Card */
    .duel-card {{
      width: 100%;
      background: #ffffff;
      padding: 30px 40px;
    }}
    .duel-row {{
      display: flex;
      align-items: center;
      gap: 22px;
      margin-top: 18px;
      font-size: 34px;
      font-weight: 800;
    }}
    .duel-name {{ width: 240px; color: var(--ink); }}
    .duel-track {{
      flex: 1;
      height: 26px;
      background: #e5e7eb;
      border-radius: 99px;
      overflow: hidden;
      border: 2px solid #1a1714;
    }}
    .duel-fill {{ height: 100%; border-radius: 99px; }}
    .duel-val {{ width: 120px; text-align: right; font-weight: 900; color: var(--clay); font-size: 38px; }}

    /* Callout Badges */
    .tg {{
      display: inline-block;
      font-weight: 900;
      color: #ffffff;
      box-shadow: 0 10px 24px rgba(0,0,0,0.2);
    }}

    /* ================= BOTTOM STAGE (HOST RIG + STUDIO DESK) ================= */
    #bottom-stage {{
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      height: 850px;
      z-index: 30;
      pointer-events: none;
    }}

    /* Sleek Low-Profile Tech Desk */
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

    /* Desk Props: Microphone & Steaming Mug */
    .desk-props {{
      position: absolute;
      left: 0;
      right: 0;
      bottom: 160px;
      height: 180px;
      z-index: 36;
      pointer-events: none;
    }}

    /* Studio Boom Arm Microphone (Left) */
    .studio-mic {{
      position: absolute;
      left: 60px;
      bottom: 0;
      width: 180px;
      height: 210px;
    }}

    /* Coffee Mug (Right) with Steam Curls */
    .desk-mug-wrap {{
      position: absolute;
      right: 80px;
      bottom: 0;
      width: 100px;
      height: 110px;
    }}
    .mug-cup {{
      width: 84px;
      height: 92px;
      background: #ffffff;
      border: 6px solid #1a1714;
      border-radius: 6px 6px 22px 22px;
      position: relative;
    }}
    .mug-cup::before {{
      content: "";
      position: absolute;
      top: 22px;
      left: 0;
      right: 0;
      height: 18px;
      background: {theme['mug_color']};
    }}
    .mug-cup::after {{
      content: "";
      position: absolute;
      right: -26px;
      top: 16px;
      width: 24px;
      height: 44px;
      border: 6px solid #1a1714;
      border-radius: 0 18px 18px 0;
    }}
    .steam-curl {{
      position: absolute;
      top: -46px;
      font-size: 34px;
      font-weight: 900;
      color: rgba(26,23,20,0.40);
      animation: steamFloat 2.2s infinite ease-out;
    }}
    .s1 {{ right: 44px; animation-delay: 0s; }}
    .s2 {{ right: 22px; animation-delay: 1.1s; }}
    @keyframes steamFloat {{
      0% {{ transform: translateY(0) scale(0.8); opacity: 0; }}
      40% {{ opacity: 0.65; }}
      100% {{ transform: translateY(-55px) scale(1.35); opacity: 0; }}
    }}

    /* Comic Disbelief Sweat Drop */
    #sweat-drop {{
      position: absolute;
      right: 320px;
      top: 130px;
      font-size: 52px;
      opacity: 0;
      z-index: 45;
      animation: sweatPulse 1s infinite alternate;
    }}
    @keyframes sweatPulse {{
      from {{ transform: translateY(0) scale(0.9); }}
      to {{ transform: translateY(10px) scale(1.1); }}
    }}

    /* Host Character Vector Rig */
    #host-avatar {{
      position: absolute;
      left: 50%;
      bottom: 160px;
      transform: translateX(-50%);
      width: 800px;
      height: 800px;
      z-index: 32;
    }}

    /* ================= KINETIC SUBTITLES ================= */
    #caption-bar {{
      position: absolute;
      left: 48px;
      right: 48px;
      bottom: 35px;
      z-index: 50;
      text-align: center;
      font-size: 38px;
      font-weight: 800;
      line-height: 1.45;
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 12px;
    }}
    .w {{
      color: rgba(255,255,255,0.70);
      padding: 4px 12px;
      border-radius: 12px;
      display: inline-block;
      transition: all 0.15s ease-out;
    }}
    .w.done {{ color: #ffffff; }}
    .w.on {{
      background: var(--clay);
      color: #ffffff !important;
      transform: scale(1.08);
      box-shadow: 0 4px 16px rgba(0,0,0,0.5);
    }}
  </style>
</head>
<body>
  <div id="stage" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{round(duration, 2)}">
    <!-- Drifting Ambient Blobs -->
    <div class="blob b1"></div>
    <div class="blob b2"></div>
    <div class="blob b3"></div>

    <!-- Audio Elements for HyperFrames Sync -->
    <audio id="voice" src="{audio_path}" data-start="0" data-duration="{round(duration, 2)}" data-volume="1"></audio>
    <audio id="sfx-whoosh" src="assets/sfx/sfx_whoosh.mp3" data-start="0" data-duration="0.5" data-volume="0.5"></audio>

    <!-- ================= UPPER THEATER (TOP 60%) ================= -->
    <div id="upper-theater">

      <!-- SCENE 1: HOOK -->
      <div id="sc-1" class="scene-view active">
        <div class="pill">⚡ {theme['badge_pill']}</div>
        <h2>{slot_meta.get('post_title', 'Stop Paying For Slow AI Tools!')}</h2>
        <div class="card" style="padding: 30px 38px;">
          <div style="font-size: 26px; font-weight: 800; color: var(--clay); margin-bottom: 8px;">✕ THE MANUAL TRAP</div>
          <div class="big-wrap">
            <div class="big-num">$200<div class="big-strike"></div></div>
          </div>
          <div style="text-align: center; font-size: 32px; font-weight: 800; color: #4b5563; margin-top: 4px;">
            Wasted monthly on slow, closed tools
          </div>
        </div>
        <div class="card list-card" style="padding: 24px 36px;">
          <div class="list-row">
            <span>Video & Script Pipeline</span>
            <div class="bar-track"><div class="bar-fill" style="width: 100%;"></div></div>
            <span class="tag" style="background: #fee2e2; color: #dc2626;">Manual</span>
          </div>
          <div class="list-row">
            <span>Autonomous Intelligence</span>
            <div class="bar-track"><div class="bar-fill" style="width: 100%; background: #10b981;"></div></div>
            <span class="tag" style="background: #dcfce7; color: #15803d;">Active 24/7</span>
          </div>
        </div>
      </div>

      <!-- SCENE 2: ITEM 1 -->
      <div id="sc-2" class="scene-view">
        <div class="pill">#1 {items_data[0]['badge']}</div>
        <h2><em>{items_data[0]['name']}</em></h2>
        <div class="card pk-card">
          <div class="pk-thumb">{items_data[0]['name'][:10].upper()}</div>
          <div class="pk-info">
            <h3>{items_data[0]['full_name']}</h3>
            <p>{items_data[0]['desc']}</p>
            <div style="margin-top: 14px; display: flex; gap: 14px;">
              <span class="tag">★ {items_data[0]['stars']}</span>
              <span class="tag" style="background: #dcfce7; color: #15803d;">100% Local</span>
            </div>
          </div>
        </div>
        <div class="card list-card" style="padding: 24px 36px;">
          <div class="list-row">
            <span>Local Inference Speed</span>
            <div class="bar-track"><div class="bar-fill" style="width: 95%;"></div></div>
            <span class="tag" style="background: #dcfce7; color: #15803d;">Zero Fees</span>
          </div>
          <div class="list-row">
            <span>Data Privacy & Weights</span>
            <div class="bar-track"><div class="bar-fill" style="width: 100%; background: var(--clay);"></div></div>
            <span class="tag">100% Offline</span>
          </div>
        </div>
      </div>

      <!-- SCENE 3: ITEM 2 -->
      <div id="sc-3" class="scene-view">
        <div class="pill">#2 {items_data[1]['badge']}</div>
        <h2><em>{items_data[1]['name']}</em></h2>
        <div class="card duel-card">
          <div style="display: flex; justify-content: space-between; font-size: 24px; font-weight: 800; color: #6b7280;">
            <span>SOTA BENCHMARK EVAL</span>
            <span class="tag">185 TOKENS/SEC</span>
          </div>
          <div class="duel-row">
            <span class="duel-name">{items_data[1]['name'][:12]}</span>
            <div class="duel-track"><div class="duel-fill" style="width: 96%; background: var(--clay);"></div></div>
            <span class="duel-val">96.4%</span>
          </div>
          <div class="duel-row">
            <span class="duel-name">Legacy Closed</span>
            <div class="duel-track"><div class="duel-fill" style="width: 82%; background: #9ca3af;"></div></div>
            <span class="duel-val" style="color: #6b7280;">82.1%</span>
          </div>
        </div>
        <div class="card pk-card" style="padding: 24px 32px;">
          <div class="pk-thumb" style="width: 160px; height: 110px; font-size: 24px;">SPEED</div>
          <div class="pk-info">
            <h3 style="font-size: 38px;">{items_data[1]['full_name']}</h3>
            <p>{items_data[1]['desc']}</p>
          </div>
        </div>
      </div>

      <!-- SCENE 4: ITEM 3 -->
      <div id="sc-4" class="scene-view">
        <div class="pill">#3 {items_data[2]['badge']}</div>
        <h2><em>{items_data[2]['name']}</em></h2>
        <div class="card pk-card">
          <div class="pk-thumb" style="background: #2563eb;">RELEASE</div>
          <div class="pk-info">
            <h3>{items_data[2]['full_name']}</h3>
            <p>{items_data[2]['desc']}</p>
            <div style="margin-top: 14px;">
              <span class="tag">★ {items_data[2]['stars']}</span>
            </div>
          </div>
        </div>
        <div class="card" style="padding: 24px 34px; text-align: center;">
          <div class="cnt">10x</div>
          <div style="font-size: 34px; font-weight: 800; color: #1a1714; margin-top: 6px;">Faster Execution Pipeline</div>
        </div>
      </div>

      <!-- SCENE 5: OUTRO CTA -->
      <div id="sc-5" class="scene-view">
        <div style="display: flex; gap: 18px; margin-top: 20px;">
          <div class="tg" style="background: #1a1714; rotate: -3deg; font-size: 44px; padding: 14px 38px; border-radius: 20px;">💬 COMMENT</div>
          <div class="tg" style="background: var(--clay); rotate: 2deg; font-size: 48px; padding: 14px 44px; border-radius: 20px;">▶ {cta_word}</div>
        </div>
        <div class="card" style="border-radius: 99px; padding: 18px 36px; display: flex; align-items: center; gap: 18px; margin-top: 16px;">
          <div style="width: 36px; height: 36px; border-radius: 50%; background: var(--clay);"></div>
          <span style="font-size: 34px; font-weight: 800; color: #1a1714;">{cta_word}</span>
          <span style="display: inline-block; width: 4px; height: 32px; background: #1a1714; margin-left: -8px;"></span>
          <span style="margin-left: auto; color: #fff; background: var(--clay); width: 48px; height: 48px; border-radius: 50%; display: grid; place-items: center; font-size: 24px;">➤</span>
        </div>
        <div class="card" style="padding: 30px 40px; border-radius: 28px;">
          <div style="font-size: 26px; font-weight: 800; color: var(--clay); margin-bottom: 6px;">✉ DIRECT MESSAGE READY</div>
          <div style="font-size: 36px; font-weight: 900; color: #1a1714; margin-bottom: 14px;">Here's your complete setup guide:</div>
          <div style="display: flex; flex-direction: column; gap: 10px; font-size: 28px; font-weight: 700; color: #374151;">
            <div>✓ 1. One-click local install command</div>
            <div>✓ 2. Free open-weights download link</div>
            <div>✓ 3. Complete production setup guide</div>
          </div>
        </div>
      </div>

    </div>

    <!-- ================= BOTTOM STAGE (HOST RIG + STUDIO DESK) ================= -->
    <div id="bottom-stage">

      <!-- Comic Sweat Drop for Facepalm -->
      <div id="sweat-drop">💦</div>

      <!-- Vector Host Character Rig -->
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

          <!-- Avatar Body Group (Subject to idle breathing oscillation) -->
          <g id="avatar-body">
            
            <!-- Torso / Broad Shoulders Hoodie -->
            <path d="M90 340 C90 280, 160 265, 220 265 C280 265, 350 280, 350 340 L370 440 L70 440 Z" 
                  fill="url(#hoodie)" stroke="#1a1714" stroke-width="8"/>
            <path d="M190 265 C190 305, 250 305, 250 265 Z" fill="#ffffff" stroke="#1a1714" stroke-width="6"/>
            <!-- Hoodie drawstring / accents -->
            <path d="M165 270 L195 365" stroke="{theme['hoodie_trim']}" stroke-width="6" stroke-linecap="round" fill="none"/>
            <path d="M275 270 L245 365" stroke="{theme['hoodie_trim']}" stroke-width="6" stroke-linecap="round" fill="none"/>

            <!-- Neck -->
            <path d="M195 245 L195 285 L245 285 L245 245 Z" fill="url(#skin)" stroke="#1a1714" stroke-width="6"/>

            <!-- Head -->
            <ellipse cx="220" cy="185" rx="66" ry="76" fill="url(#skin)" stroke="#1a1714" stroke-width="8"/>

            <!-- Hair -->
            <path d="M150 165 C150 95, 210 75, 280 95 C305 105, 300 135, 300 155 C300 135, 290 120, 270 120 C235 120, 225 135, 185 135 C165 135, 155 155, 150 165 Z" fill="#1a1714"/>

            <!-- Eyebrows -->
            <path id="brow-left" d="M180 158 Q198 150, 210 158" fill="none" stroke="#1a1714" stroke-width="6" stroke-linecap="round"/>
            <path id="brow-right" d="M230 158 Q242 150, 260 158" fill="none" stroke="#1a1714" stroke-width="6" stroke-linecap="round"/>

            <!-- Eyes & Eyelids (Automatic Blinking every 90 frames) -->
            <g id="eyes-open">
              <ellipse cx="194" cy="178" rx="10" ry="14" fill="#ffffff" stroke="#1a1714" stroke-width="4"/>
              <circle cx="196" cy="179" r="6" fill="#1a1714"/>
              <circle cx="199" cy="176" r="2.5" fill="#ffffff"/>

              <ellipse cx="246" cy="178" rx="10" ry="14" fill="#ffffff" stroke="#1a1714" stroke-width="4"/>
              <circle cx="248" cy="179" r="6" fill="#1a1714"/>
              <circle cx="251" cy="176" r="2.5" fill="#ffffff"/>
            </g>
            <g id="eyes-blink" style="display: none;">
              <path d="M184 180 Q194 190, 204 180" fill="none" stroke="#1a1714" stroke-width="5" stroke-linecap="round"/>
              <path d="M236 180 Q246 190, 256 180" fill="none" stroke="#1a1714" stroke-width="5" stroke-linecap="round"/>
            </g>

            <!-- Glasses -->
            <rect x="176" y="162" width="38" height="32" rx="10" fill="none" stroke="#1a1714" stroke-width="7"/>
            <rect x="226" y="162" width="38" height="32" rx="10" fill="none" stroke="#1a1714" stroke-width="7"/>
            <path d="M214 176 L226 176" fill="none" stroke="#1a1714" stroke-width="7"/>

            <!-- Nose -->
            <path d="M220 178 L216 200 L226 200" fill="none" stroke="#1a1714" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

            <!-- Dynamic Lip-Sync Mouth Group (4 States) -->
            <g id="mouth-group">
              <path id="m-closed" d="M204 226 Q220 228, 236 226" stroke="#1a1714" stroke-width="5" stroke-linecap="round" fill="none"/>
              <ellipse id="m-small" cx="220" cy="226" rx="8" ry="6" fill="#881337" stroke="#1a1714" stroke-width="3.5" style="display: none;"/>
              <path id="m-open" d="M206 222 Q220 216, 234 222 Q234 238, 220 240 Q206 238, 206 222 Z" fill="#881337" stroke="#1a1714" stroke-width="3.5" style="display: none;"/>
              <g id="m-wide" style="display: none;">
                <path d="M202 220 Q220 210, 238 220 Q236 248, 220 250 Q204 248, 202 220 Z" fill="#881337" stroke="#1a1714" stroke-width="4"/>
                <rect x="210" y="218" width="20" height="5" rx="2" fill="#ffffff"/>
                <ellipse cx="220" cy="242" rx="8" ry="4.5" fill="#f43f5e"/>
              </g>
            </g>

          </g> <!-- end avatar-body -->

          <!-- ================= 5 ARM VARIANTS ================= -->
          <g id="arms-layer">
            
            <!-- 1. IDLE (Resting naturally on desk with sleeves) -->
            <g id="pose-idle">
              <!-- Left arm resting -->
              <path d="M110 320 C95 360, 110 405, 155 420" fill="none" stroke="#1a1714" stroke-width="36" stroke-linecap="round"/>
              <path d="M110 320 C95 360, 110 405, 155 420" fill="none" stroke="{theme['hoodie_color']}" stroke-width="28" stroke-linecap="round"/>
              <circle cx="160" cy="422" r="14" fill="url(#skin)" stroke="#1a1714" stroke-width="5"/>
              <!-- Right arm resting -->
              <path d="M330 320 C345 360, 330 405, 285 420" fill="none" stroke="#1a1714" stroke-width="36" stroke-linecap="round"/>
              <path d="M330 320 C345 360, 330 405, 285 420" fill="none" stroke="{theme['hoodie_color']}" stroke-width="28" stroke-linecap="round"/>
              <circle cx="280" cy="422" r="14" fill="url(#skin)" stroke="#1a1714" stroke-width="5"/>
            </g>

            <!-- 2. WAVE (Right arm raised waving with periodic harmonic oscillation) -->
            <g id="pose-wave" style="display: none;">
              <!-- Left resting -->
              <path d="M110 320 C95 360, 110 405, 155 420" fill="none" stroke="#1a1714" stroke-width="36" stroke-linecap="round"/>
              <path d="M110 320 C95 360, 110 405, 155 420" fill="none" stroke="{theme['hoodie_color']}" stroke-width="28" stroke-linecap="round"/>
              <circle cx="160" cy="422" r="14" fill="url(#skin)" stroke="#1a1714" stroke-width="5"/>
              <!-- Right wave -->
              <g id="arm-wave-hand">
                <path d="M330 320 C370 260, 375 190, 360 140" fill="none" stroke="#1a1714" stroke-width="36" stroke-linecap="round"/>
                <path d="M330 320 C370 260, 375 190, 360 140" fill="none" stroke="{theme['hoodie_color']}" stroke-width="28" stroke-linecap="round"/>
                <circle cx="356" cy="118" r="20" fill="url(#skin)" stroke="#1a1714" stroke-width="5.5"/>
              </g>
            </g>

            <!-- 3. POINT UP (Right arm angled cleanly pointing up at drop cards) -->
            <g id="pose-pointUp" style="display: none;">
              <!-- Left resting -->
              <path d="M110 320 C95 360, 110 405, 155 420" fill="none" stroke="#1a1714" stroke-width="36" stroke-linecap="round"/>
              <path d="M110 320 C95 360, 110 405, 155 420" fill="none" stroke="{theme['hoodie_color']}" stroke-width="28" stroke-linecap="round"/>
              <circle cx="160" cy="422" r="14" fill="url(#skin)" stroke="#1a1714" stroke-width="5"/>
              <!-- Right pointing straight up -->
              <path d="M330 320 C355 260, 345 180, 335 110" fill="none" stroke="#1a1714" stroke-width="36" stroke-linecap="round"/>
              <path d="M330 320 C355 260, 345 180, 335 110" fill="none" stroke="{theme['hoodie_color']}" stroke-width="28" stroke-linecap="round"/>
              <g transform="translate(322, 60)">
                <ellipse cx="12" cy="38" rx="16" ry="16" fill="url(#skin)" stroke="#1a1714" stroke-width="5.5"/>
                <rect x="7" y="0" width="11" height="34" rx="5.5" fill="url(#skin)" stroke="#1a1714" stroke-width="5.5"/>
              </g>
            </g>

            <!-- 4. POINT LEFT (Left arm pointing across screen at benchmark graph) -->
            <g id="pose-pointLeft" style="display: none;">
              <!-- Right resting -->
              <path d="M330 320 C345 360, 330 405, 285 420" fill="none" stroke="#1a1714" stroke-width="36" stroke-linecap="round"/>
              <path d="M330 320 C345 360, 330 405, 285 420" fill="none" stroke="{theme['hoodie_color']}" stroke-width="28" stroke-linecap="round"/>
              <circle cx="280" cy="422" r="14" fill="url(#skin)" stroke="#1a1714" stroke-width="5"/>
              <!-- Left pointing left -->
              <path d="M110 320 C85 270, 65 220, 45 150" fill="none" stroke="#1a1714" stroke-width="36" stroke-linecap="round"/>
              <path d="M110 320 C85 270, 65 220, 45 150" fill="none" stroke="{theme['hoodie_color']}" stroke-width="28" stroke-linecap="round"/>
              <g transform="translate(32, 118)">
                <circle cx="14" cy="24" r="16" fill="url(#skin)" stroke="#1a1714" stroke-width="5.5"/>
                <rect x="8" y="0" width="11" height="32" rx="5.5" fill="url(#skin)" stroke="#1a1714" stroke-width="5.5" transform="rotate(-24, 14, 16)"/>
              </g>
            </g>

            <!-- 5. FACEPALM (Right arm reaching to forehead in comic disbelief) -->
            <g id="pose-facepalm" style="display: none;">
              <!-- Left resting -->
              <path d="M110 320 C95 360, 110 405, 155 420" fill="none" stroke="#1a1714" stroke-width="36" stroke-linecap="round"/>
              <path d="M110 320 C95 360, 110 405, 155 420" fill="none" stroke="{theme['hoodie_color']}" stroke-width="28" stroke-linecap="round"/>
              <circle cx="160" cy="422" r="14" fill="url(#skin)" stroke="#1a1714" stroke-width="5"/>
              <!-- Right arm up to face -->
              <path d="M330 320 C365 270, 330 190, 270 175" fill="none" stroke="#1a1714" stroke-width="36" stroke-linecap="round"/>
              <path d="M330 320 C365 270, 330 190, 270 175" fill="none" stroke="{theme['hoodie_color']}" stroke-width="28" stroke-linecap="round"/>
              <ellipse cx="260" cy="172" rx="20" ry="18" fill="url(#skin)" stroke="#1a1714" stroke-width="5.5"/>
            </g>

          </g> <!-- end arms-layer -->
        </svg>
      </div> <!-- end host-avatar -->

      <!-- Sleek Tech Desk Surface -->
      <div class="desk-surface"></div>

      <!-- Desk Props: Mic & Mug -->
      <div class="desk-props">
        <!-- Studio Boom Arm Microphone (Left) -->
        <div class="studio-mic">
          <svg viewBox="0 0 120 140" width="100%" height="100%">
            <!-- Desk Clamp -->
            <rect x="15" y="115" width="24" height="22" rx="4" fill="#1a1714"/>
            <!-- Articulated metal boom arms -->
            <path d="M26 115 L50 55 L82 78" stroke="#1a1714" stroke-width="8" stroke-linecap="round" fill="none"/>
            <path d="M30 115 L54 55 L86 78" stroke="#6b7280" stroke-width="3.5" stroke-linecap="round" fill="none"/>
            <!-- Joints -->
            <circle cx="26" cy="115" r="8" fill="#1a1714"/>
            <circle cx="50" cy="55" r="8" fill="#1a1714"/>
            <!-- Shock Mount Ring -->
            <circle cx="86" cy="82" r="18" fill="none" stroke="#1a1714" stroke-width="4.5"/>
            <!-- Condenser Capsule / Foam Filter -->
            <rect x="76" y="66" width="22" height="34" rx="11" fill="#2d3748" stroke="#1a1714" stroke-width="4"/>
            <path d="M79 78 L95 78 M79 84 L95 84" stroke="#4a5568" stroke-width="2.5"/>
          </svg>
        </div>

        <!-- Coffee Mug (Right) with Steam Curls -->
        <div class="desk-mug-wrap">
          <div class="steam-curl s1">~</div>
          <div class="steam-curl s2">~</div>
          <div class="mug-cup"></div>
        </div>
      </div>

    </div> <!-- end bottom-stage -->

    <!-- ================= KINETIC SUBTITLES ================= -->
    <div id="caption-bar"></div>

  </div> <!-- end stage -->

  <script>
    // Frame-Accurate Lip-Sync Data ({len(mouth_data)} frames)
    const mouthData = {json.dumps(mouth_data)};
    const captionChunks = {json.dumps(caption_chunks)};
    const totalDuration = {round(duration, 2)};
    const fps = 30;

    // Active Arm Variant
    let currentPose = "{theme['initial_pose']}";

    function setPose(poseName) {{
      currentPose = poseName;
      const poses = ["idle", "wave", "pointUp", "pointLeft", "facepalm"];
      poses.forEach(p => {{
        const el = document.getElementById("pose-" + p);
        if (el) el.style.display = (p === poseName) ? "block" : "none";
      }});
      // Toggle comic sweat drop for facepalm
      const sweat = document.getElementById("sweat-drop");
      if (sweat) sweat.style.opacity = (poseName === "facepalm") ? "1" : "0";
    }}

    function setMouthShape(shape) {{
      const shapes = ["closed", "small", "open", "wide"];
      shapes.forEach(s => {{
        const el = document.getElementById("m-" + s);
        if (el) el.style.display = (s === shape) ? "block" : "none";
      }});
    }}

    function setBlink(isBlinking) {{
      const openEl = document.getElementById("eyes-open");
      const blinkEl = document.getElementById("eyes-blink");
      if (openEl && blinkEl) {{
        openEl.style.display = isBlinking ? "none" : "block";
        blinkEl.style.display = isBlinking ? "block" : "none";
      }}
    }}

    // ================= GSAP SCENE & POSE CHOREOGRAPHY =================
    const tl = gsap.timeline();
    window.__timelines = window.__timelines || {{}};
    window.__timelines["main"] = tl;

    // 1. Initial State (outside timeline for deterministic frame 0)
    gsap.set("#sc-1", {{ display: "flex", opacity: 1 }});
    gsap.set(["#sc-2", "#sc-3", "#sc-4", "#sc-5"], {{ display: "none", opacity: 0 }});
    gsap.set("#pose-facepalm", {{ display: "block" }});
    gsap.set(["#pose-idle", "#pose-wave", "#pose-pointUp", "#pose-pointLeft"], {{ display: "none" }});
    gsap.set("#sweat-drop", {{ opacity: 1 }});
    gsap.set("#eyes-open", {{ display: "block" }});
    gsap.set("#eyes-blink", {{ display: "none" }});

    // 2. Scene 2: Item 1 ({t_hook_end} - {t_tool1_end}s) -> pointUp pose
    tl.to("#sc-1", {{ opacity: 0, duration: 0.2 }}, {t_hook_end});
    tl.set("#sc-1", {{ display: "none" }}, {t_hook_end + 0.2});
    tl.set("#sc-2", {{ display: "flex" }}, {t_hook_end + 0.2});
    tl.fromTo("#sc-2", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {t_hook_end + 0.2});

    tl.set(["#pose-facepalm", "#sweat-drop"], {{ display: "none", opacity: 0 }}, {t_hook_end});
    tl.set("#pose-pointUp", {{ display: "block" }}, {t_hook_end});

    // 3. Scene 3: Item 2 ({t_tool1_end} - {t_tool2_end}s) -> pointLeft pose
    tl.to("#sc-2", {{ opacity: 0, duration: 0.2 }}, {t_tool1_end});
    tl.set("#sc-2", {{ display: "none" }}, {t_tool1_end + 0.2});
    tl.set("#sc-3", {{ display: "flex" }}, {t_tool1_end + 0.2});
    tl.fromTo("#sc-3", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {t_tool1_end + 0.2});

    tl.set("#pose-pointUp", {{ display: "none" }}, {t_tool1_end});
    tl.set("#pose-pointLeft", {{ display: "block" }}, {t_tool1_end});

    // 4. Scene 4: Item 3 ({t_tool2_end} - {t_tool3_end}s) -> pointUp pose
    tl.to("#sc-3", {{ opacity: 0, duration: 0.2 }}, {t_tool2_end});
    tl.set("#sc-3", {{ display: "none" }}, {t_tool2_end + 0.2});
    tl.set("#sc-4", {{ display: "flex" }}, {t_tool2_end + 0.2});
    tl.fromTo("#sc-4", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {t_tool2_end + 0.2});

    tl.set("#pose-pointLeft", {{ display: "none" }}, {t_tool2_end});
    tl.set("#pose-pointUp", {{ display: "block" }}, {t_tool2_end});

    // 5. Scene 5: Outro CTA ({t_tool3_end} - {t_cta_end}s) -> wave pose
    tl.to("#sc-4", {{ opacity: 0, duration: 0.2 }}, {t_tool3_end});
    tl.set("#sc-4", {{ display: "none" }}, {t_tool3_end + 0.2});
    tl.set("#sc-5", {{ display: "flex" }}, {t_tool3_end + 0.2});
    tl.fromTo("#sc-5", {{ opacity: 0, scale: 0.95 }}, {{ opacity: 1, scale: 1, duration: 0.35 }}, {t_tool3_end + 0.2});

    tl.set("#pose-pointUp", {{ display: "none" }}, {t_tool3_end});
    tl.set("#pose-wave", {{ display: "block" }}, {t_tool3_end});

    // Continuous Idle Breathing Oscillation (bounded)
    tl.to("#avatar-body", {{ y: -8, duration: 1.4, repeat: {int(duration / 1.4)}, yoyo: true, ease: "sine.inOut" }}, 0);

    // Continuous Wave Arm Motion in Scene 5 (bounded)
    tl.to("#arm-wave-hand", {{ rotation: 16, transformOrigin: "330px 220px", duration: 0.28, repeat: {int((duration - t_tool3_end) / 0.28)}, yoyo: true, ease: "sine.inOut" }}, {t_tool3_end});

    // Automatic Eye Blinks (every 3s for 0.133s)
    for (let t = 1.6; t < {round(duration, 2)}; t += 3.0) {{
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

    print(f"[✓] Compiled 1080x1920 Full HD host vector rig composition to {output_html} ({round(duration, 2)}s)")
    return output_html

if __name__ == "__main__":
    build_hyperframes_composition()
