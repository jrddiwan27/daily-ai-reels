import os
import re
import json
import math
from dotenv import load_dotenv

load_dotenv()

def run_visual_agent(
    dossier_path: str = "assets/research_dossier.json",
    script_path: str = "assets/viral_script.json",
    timeline_path: str = "assets/word_timeline.json",
    mouth_path: str = "assets/mouth_sync.json",
    duration: float = 42.0,
    output_html: str = "index.html",
    script_data: dict = None,
    research_dossier: dict = None
) -> str:
    """
    VISUAL AGENT:
    Compiles full-screen 1080x1920 Neo-Brutalist cinematic composition with:
    - Prominent, large-scale animated character host (480x520px) with 4-state lip-sync & gestures.
    - Zero static frames (micro-scene changes every 1.8s - 2.5s matched to speech words).
    - High-density visual elements: Code terminals, device mockups, laser scanners, speedometers.
    - Subtitle tracking pill locked to word timestamps.
    """
    print("=" * 65)
    print(f"🎨 [AGENT 4: VISUAL AGENT] Building Hyper-Paced Movie Composition (1080x1920)...")
    print("=" * 65)

    if research_dossier:
        dossier = research_dossier
    elif os.path.exists(dossier_path):
        with open(dossier_path, "r") as f:
            dossier = json.load(f)
    else:
        dossier = {}
    items = dossier.get("items", [])

    if script_data:
        pass
    elif os.path.exists(script_path):
        with open(script_path, "r") as f:
            script_data = json.load(f)
    else:
        script_data = {}
    cta_keyword = script_data.get("cta_keyword", "TOOLS").upper()

    with open(timeline_path, "r") as f:
        timeline = json.load(f)

    mouth_data = []
    if os.path.exists(mouth_path):
        with open(mouth_path, "r") as f:
            mouth_data = json.load(f)

    # Clean items data
    it1 = items[0] if len(items) > 0 else {"name": "Tool One", "title": "Tool One", "description": "AI Agent", "stars": "3.5K"}
    it2 = items[1] if len(items) > 1 else {"name": "Tool Two", "title": "Tool Two", "description": "Workflow", "stars": "4.2K"}
    it3 = items[2] if len(items) > 2 else {"name": "Tool Three", "title": "Tool Three", "description": "Engine", "stars": "5.0K"}

    for it in [it1, it2, it3]:
        it["clean_name"] = (it.get("name") or it.get("title", "")).split("/")[-1].replace("-", " ").title()
        it["stars_str"] = it.get("stars", "3,500+")

    # 14 Chronological Micro-Shots matched to spoken duration
    d = max(35.0, float(duration))
    t0 = 0.0
    t1 = round(d * 0.07, 2)   # Hook strike
    t2 = round(d * 0.14, 2)   # Shift / Solution
    t3 = round(d * 0.22, 2)   # Architecture / Protocol
    t4 = round(d * 0.29, 2)   # Item 1 Reveal
    t5 = round(d * 0.37, 2)   # Item 1 Superpower
    t6 = round(d * 0.45, 2)   # Item 1 Metric / Proof
    t7 = round(d * 0.53, 2)   # Item 2 Reveal
    t8 = round(d * 0.61, 2)   # Item 2 Vision & Execution
    t9 = round(d * 0.69, 2)   # Item 2 Speed / Accuracy
    t10 = round(d * 0.77, 2)  # Item 3 Reveal
    t11 = round(d * 0.84, 2)  # Item 3 Offline & Cost
    t12 = round(d * 0.90, 2)  # CLI Quickstart
    t13 = round(d * 0.93, 2)  # High-Converting CTA
    t_end = round(d, 2)

    shots = [
        {"id": 0, "start": t0, "theme": "rd", "label": "STOP WASTING HOURS", "pr": "0/3"},
        {"id": 1, "start": t1, "theme": "dk", "label": "THE NEW AUTONOMOUS STACK", "pr": "0/3"},
        {"id": 2, "start": t2, "theme": "bl", "label": "NATIVE PROTOCOL", "pr": "0/3"},
        {"id": 3, "start": t3, "theme": "gr", "label": f"01 · {it1['clean_name'][:18]}", "pr": "1/3"},
        {"id": 4, "start": t4, "theme": "bl", "label": "SUPERPOWER UNLOCKED", "pr": "1/3"},
        {"id": 5, "start": t5, "theme": "rd", "label": "ZERO MONTHLY FEES", "pr": "1/3"},
        {"id": 6, "start": t6, "theme": "pk", "label": f"02 · {it2['clean_name'][:18]}", "pr": "2/3"},
        {"id": 7, "start": t7, "theme": "bl", "label": "REAL-TIME VISION GROUNDING", "pr": "2/3"},
        {"id": 8, "start": t8, "theme": "yl", "label": "MAX PERFORMANCE", "pr": "2/3"},
        {"id": 9, "start": t9, "theme": "dk", "label": f"03 · {it3['clean_name'][:18]}", "pr": "3/3"},
        {"id": 10, "start": t10, "theme": "gr", "label": "100% PRIVATE & LOCAL", "pr": "3/3"},
        {"id": 11, "start": t11, "theme": "bl", "label": "60-SECOND QUICKSTART", "pr": "3/3"},
        {"id": 12, "start": t12, "theme": "rd", "label": f"COMMENT '{cta_keyword}'", "pr": "3/3"}
    ]

    # Mouth lip-sync calls
    mouth_calls = []
    last_m = None
    for item in mouth_data:
        m = item.get("mouth", "closed")
        t = item.get("t", 0.0)
        if m != last_m and t <= d:
            mouth_calls.append(f'tl.call(() => setMouth("{m}"), null, {t});')
            last_m = m

    # Shot mounting calls
    shot_calls = []
    for s in shots:
        shot_calls.append(f'tl.call(() => mountShot({s["id"]}), null, {s["start"]});')

    # Subtitle word tracking calls
    caption_calls = []
    for w_info in timeline:
        word = w_info.get("word", "").replace('"', '\\"')
        caption_calls.append(f'tl.call(() => setWord("{word}"), null, {w_info.get("start", 0)});')
    caption_calls.append(f'tl.call(() => setWord(""), null, {max(0, d - 0.2)});')

    # Build shots HTML
    shots_html = [
        # Shot 0: Hook
        f"""
        <div class="big-title">STOP DOING THIS MANUALLY</div>
        <div class="sub-stamp" style="background:#ff3b30; color:#fff;">⚠️ THE 2026 BOTTLENECK</div>
        <div class="card" style="display:flex; flex-direction:column; align-items:center; gap:20px;">
          <div style="display:flex; gap:36px; align-items:center;">
            <div style="font-size:100px; animation: jitterBug 0.15s infinite alternate;">❌</div>
            <div style="font-size:110px; animation: tapFinger 0.35s infinite alternate;">⏳</div>
            <div style="font-size:100px; animation: jitterBug 0.2s infinite alternate;">💸</div>
          </div>
          <div class="strike-bar"></div>
          <div style="font:800 32px 'IBM Plex Mono'; color:#ff3b30;">SLOW · EXPENSIVE · REPETITIVE</div>
        </div>
        """,

        # Shot 1: The Solution
        f"""
        <div class="big-title">NEW OPEN AI STACK</div>
        <div class="sub-stamp" style="background:#22c55e; color:#fff;">⚡ AUTONOMOUS AGENTS</div>
        <div class="card" style="background:#14121a; color:#fff; display:flex; flex-direction:column; align-items:center; gap:24px;">
          <div class="shockwave-ring"></div>
          <div style="font-size:110px; animation: bobbing 1.2s infinite alternate;">🚀</div>
          <div style="font:800 34px 'IBM Plex Mono'; color:#38bdf8;">{{ autonomous.execute() }}</div>
          <div style="display:flex; gap:16px;">
            <span class="sub-stamp" style="font-size:24px; padding:6px 16px;">ZERO SAAS BILLS</span>
            <span class="sub-stamp" style="font-size:24px; padding:6px 16px; background:#6f9ee8; color:#fff;">10X PRODUCTIVITY</span>
          </div>
        </div>
        """,

        # Shot 2: Native Protocol
        f"""
        <div class="big-title">DIRECT EXECUTION</div>
        <div class="sub-stamp" style="background:#ffd23f; color:#111;">⚡ NATIVE HIGH-SPEED PIPELINE</div>
        <div class="card" style="display:flex; justify-content:space-around; align-items:center;">
          <div style="text-align:center;">
            <div style="font-size:90px;">💻</div>
            <div style="font:800 26px 'IBM Plex Mono'; margin-top:8px;">Local Host</div>
          </div>
          <div class="lightning-flow">
            <div class="lightning-bolt">⚡⚡⚡</div>
            <div style="font:900 26px 'IBM Plex Mono'; color:#ff3b30;">AI RUNTIME</div>
          </div>
          <div style="text-align:center;">
            <div style="font-size:90px; animation: phoneGlow 1s infinite alternate;">📱</div>
            <div style="font:800 26px 'IBM Plex Mono'; margin-top:8px;">Live Device</div>
          </div>
        </div>
        """,

        # Shot 3: Item 1 Reveal
        f"""
        <div class="big-title">01 · {it1['clean_name']}</div>
        <div class="win">
          <div class="hd"><i></i><i></i><i></i>{it1.get('url', 'github.com/repo')}</div>
          <div class="bd">
            <div><span class="c">repo:</span> <span class="y">{it1.get('title', it1['clean_name'])}</span></div>
            <div style="margin-top:14px;"><span class="g">★ {it1['stars_str']} GitHub Stars</span></div>
            <div style="margin-top:14px; color:#cbd5e1;">{it1.get('description', '')[:95]}</div>
          </div>
        </div>
        <div class="sub-stamp" style="background:#22c55e; color:#fff; rotate:2deg;">★ 100% OPEN SOURCE</div>
        """,

        # Shot 4: Item 1 Superpower
        f"""
        <div class="big-title">{it1['clean_name'].upper()} POWER</div>
        <div class="sub-stamp" style="background:#38bdf8; color:#111;">NATIVE WORKFLOW AUTOMATION</div>
        <div class="card" style="display:flex; flex-direction:column; gap:18px;">
          <div class="chk">
            <div class="ck"><u>✔</u> Complete local execution on device</div>
            <div class="ck"><u>✔</u> Zero API limits & zero telemetry</div>
            <div class="ck"><u>✔</u> High throughput production ready</div>
          </div>
        </div>
        """,

        # Shot 5: Item 1 Metric
        f"""
        <div class="big-title">VERIFIED PROOF</div>
        <div class="card" style="display:flex; justify-content:space-around; align-items:center;">
          <div style="text-align:center;">
            <div style="font:900 76px 'Bricolage Grotesque'; color:#2563eb;">{it1['stars_str']}</div>
            <div style="font:800 26px 'IBM Plex Mono';">COMMUNITY STARS</div>
          </div>
          <div style="height:100px; width:4px; background:#ddd;"></div>
          <div style="text-align:center;">
            <div style="font:900 76px 'Bricolage Grotesque'; color:#16a34a;">$0</div>
            <div style="font:800 26px 'IBM Plex Mono';">MONTHLY COST</div>
          </div>
        </div>
        <div class="sub-stamp" style="background:#f6c85a; color:#111;">★ ZERO RECURRING FEES</div>
        """,

        # Shot 6: Item 2 Reveal
        f"""
        <div class="big-title">02 · {it2['clean_name']}</div>
        <div class="win">
          <div class="hd"><i></i><i></i><i></i>{it2.get('url', 'github.com/repo')}</div>
          <div class="bd">
            <div><span class="c">engine:</span> <span class="y">{it2.get('title', it2['clean_name'])}</span></div>
            <div style="margin-top:14px;"><span class="g">★ {it2['stars_str']} Stars</span> · Trending Worldwide</div>
            <div style="margin-top:14px; color:#cbd5e1;">{it2.get('description', '')[:95]}</div>
          </div>
        </div>
        <div class="sub-stamp" style="background:#f43f5e; color:#fff; rotate:-2deg;">★ VERIFIED BREAKTHROUGH</div>
        """,

        # Shot 7: Item 2 Vision Grounding
        f"""
        <div class="big-title">LIVE VISION GROUNDING</div>
        <div class="card" style="display:flex; gap:36px; align-items:center; justify-content:center;">
          <div class="phone-mock">
            <div class="phone-notch"></div>
            <div class="screen-grid">
              <div class="laser-scanner"></div>
              <div class="app-row">
                <div class="app-icon">🤖</div>
                <div class="app-icon">⚡</div>
                <div class="app-icon">🎯</div>
              </div>
              <div class="bbox red-box" style="top:180px;">🎯 [VISION: Target Detected]</div>
              <div class="bbox green-box" style="top:360px;">⚡ [ACTION: Autonomous Click]</div>
            </div>
          </div>
          <div style="display:flex; flex-direction:column; gap:16px;">
            <span class="sub-stamp" style="font-size:24px; background:#f6c85a; color:#111;">DETECTS ALL ELEMENTS</span>
            <span class="sub-stamp" style="font-size:24px; background:#22c55e; color:#fff;">AUTONOMOUS EXECUTION</span>
            <span class="sub-stamp" style="font-size:24px; background:#38bdf8; color:#fff;">ZERO LATENCY DELAY</span>
          </div>
        </div>
        """,

        # Shot 8: Item 2 Speed
        f"""
        <div class="big-title">EXTREME EFFICIENCY</div>
        <div class="card" style="display:flex; justify-content:space-around; align-items:center;">
          <div style="text-align:center;">
            <div style="font:900 40px 'Bricolage Grotesque'; color:#2563eb;">LATENCY</div>
            <div style="font:700 24px 'IBM Plex Mono'; margin-top:8px;">Sub-Second</div>
          </div>
          <div class="gauge-box">
            <div class="gauge-needle"></div>
            <div style="position:absolute; bottom:12px; font:900 20px 'IBM Plex Mono';">MAX SPEED</div>
          </div>
          <div style="text-align:center;">
            <div style="font:900 40px 'Bricolage Grotesque'; color:#16a34a;">ACCURACY</div>
            <div style="font:700 24px 'IBM Plex Mono'; margin-top:8px;">99.4% Pass Rate</div>
          </div>
        </div>
        """,

        # Shot 9: Item 3 Reveal
        f"""
        <div class="big-title">03 · {it3['clean_name']}</div>
        <div class="win">
          <div class="hd"><i></i><i></i><i></i>{it3.get('url', 'github.com/repo')}</div>
          <div class="bd">
            <div><span class="c">runtime:</span> <span class="y">{it3.get('title', it3['clean_name'])}</span></div>
            <div style="margin-top:14px;"><span class="g">★ {it3['stars_str']} Stars</span></div>
            <div style="margin-top:14px; color:#cbd5e1;">{it3.get('description', '')[:95]}</div>
          </div>
        </div>
        <div class="sub-stamp" style="background:#22c55e; color:#fff;">★ HIGH-PERFORMANCE</div>
        """,

        # Shot 10: Item 3 Private Offline
        f"""
        <div class="big-title">100% PRIVATE & OFFLINE</div>
        <div class="card" style="display:flex; justify-content:space-between; align-items:center; background:#111; color:#fff;">
          <div>
            <div style="font:900 44px 'Bricolage Grotesque'; color:#38bdf8;">OFFLINE INFERENCE</div>
            <div style="font:700 24px 'IBM Plex Mono'; color:#aaa; margin-top:8px;">Zero cloud subscriptions</div>
            <div class="sub-stamp" style="background:#22c55e; color:#fff; margin-top:14px;">$0 API BILLS</div>
          </div>
          <div class="bars">
            <i style="--h: 110px; animation-delay: -0.1s;"></i>
            <i style="--h: 75px; animation-delay: -0.3s;"></i>
            <i style="--h: 130px; animation-delay: -0.2s;"></i>
            <i style="--h: 90px; animation-delay: -0.4s;"></i>
            <i style="--h: 120px; animation-delay: -0.15s;"></i>
            <i style="--h: 65px; animation-delay: -0.35s;"></i>
          </div>
        </div>
        """,

        # Shot 11: CLI Quickstart
        f"""
        <div class="big-title">RUN IN 60 SECONDS</div>
        <div class="win">
          <div class="hd"><i></i><i></i><i></i>Terminal — Quickstart</div>
          <div class="bd">
            <div><span class="y">$</span> pip install {it1['clean_name'].lower().replace(' ', '-')}</div>
            <div style="margin-top:16px;"><span class="y">$</span> git clone {it2.get('url', 'https://github.com')}</div>
            <div style="margin-top:16px;" class="g">✔ Stack Initialized & Connected</div>
            <div style="margin-top:10px;" class="g">✔ All 3 Superpowers Active</div>
          </div>
        </div>
        <div class="sub-stamp" style="background:#22c55e; color:#fff;">ONE-LINE EXECUTION</div>
        """,

        # Shot 12: High-Converting CTA
        f"""
        <div class="big-title">GET THE FULL BLUEPRINT</div>
        <div class="fol-btn">COMMENT "{cta_keyword}"</div>
        <div class="card" style="text-align:center; max-width:780px; background:#ffd23f;">
          <div style="font:900 34px 'Bricolage Grotesque';">📩 I will DM you the exact repo links + setup guide right now</div>
        </div>
        <div class="reactions-row">
          <div class="reaction-ic">♥</div>
          <div class="reaction-ic">🔖</div>
          <div class="reaction-ic">↗</div>
        </div>
        """
    ]

    shots_divs = []
    for s_idx, html_chunk in enumerate(shots_html):
        shots_divs.append(f'<div class="sc-body" id="sc{s_idx}" style="display:none;">{html_chunk}</div>')
    all_shots_markup = "\n".join(shots_divs)

    mouth_js = "\n      ".join(mouth_calls)
    shot_js = "\n      ".join(shot_calls)
    caption_js = "\n      ".join(caption_calls)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=1080, height=1920, initial-scale=1">
  <title>Daily Viral Reel</title>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700;800;900&family=IBM+Plex+Mono:wght@500;700&display=swap" rel="stylesheet">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>

  <style>
    :root {{
      box-sizing: border-box;
      --clay: #d9694a;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #111;
      font-family: 'Bricolage Grotesque', system-ui, sans-serif;
      position: relative;
    }}

    #stage {{
      position: absolute;
      inset: 0;
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: var(--b, #e8695c);
      transition: background 0.25s ease;
      color: #111;
    }}

    #stage.rd {{ --b: #e8695c; --d: #b8352b; }}
    #stage.yl {{ --b: #f6c85a; --d: #d97a14; }}
    #stage.bl {{ --b: #6f9ee8; --d: #2147b8; }}
    #stage.gr {{ --b: #7fcfb3; --d: #0f7a5c; }}
    #stage.pk {{ --b: #f3a6c8; --d: #b3407a; }}
    #stage.dk {{ --b: #17141f; --d: #3a2f5c; color: #fff; }}

    /* Continuous Background Movement (Zero Static Seconds) */
    #stage::before {{
      content: "";
      position: absolute;
      inset: 0;
      background: repeating-linear-gradient(90deg, rgba(255, 255, 255, 0.12) 0 66px, transparent 66px 132px);
      animation: gs 1.6s linear infinite;
      z-index: 1;
      pointer-events: none;
    }}
    @keyframes gs {{
      to {{ background-position: 132px 0; }}
    }}

    /* Camera Macro-Movement */
    #scene-container {{
      position: absolute;
      inset: 0;
      z-index: 2;
      animation: zoomDrift 3.5s ease-in-out infinite alternate;
    }}
    @keyframes zoomDrift {{
      from {{ transform: scale(1) rotate(-0.3deg); }}
      to {{ transform: scale(1.03) rotate(0.4deg); }}
    }}

    #pt {{
      position: absolute;
      inset: 0;
      overflow: hidden;
      pointer-events: none;
      z-index: 2;
    }}
    #pt i {{
      position: absolute;
      bottom: -30px;
      width: var(--s);
      height: var(--s);
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.65);
      box-shadow: 0 0 12px rgba(255, 255, 255, 0.8);
      animation: rise var(--t) var(--dl) linear infinite;
    }}
    @keyframes rise {{
      to {{ transform: translate(60px, -2040px); }}
    }}

    .top-header {{
      position: absolute;
      top: 48px;
      left: 48px;
      right: 48px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10;
    }}
    .lab {{
      background: #111;
      color: #fff;
      font: 800 28px 'IBM Plex Mono', monospace;
      padding: 14px 28px;
      border: 4px solid #fff;
      box-shadow: 6px 6px 0 #111;
      rotate: -1.5deg;
      letter-spacing: 1px;
    }}
    .pr {{
      display: flex;
      gap: 12px;
      align-items: center;
      background: #fff;
      border: 5px solid #111;
      border-radius: 999px;
      padding: 10px 24px;
      font: 800 26px 'IBM Plex Mono', monospace;
      color: #111;
      box-shadow: 6px 6px 0 #111;
    }}
    .pr i {{
      width: 22px;
      height: 22px;
      border-radius: 50%;
      border: 4px solid #111;
      background: #fff;
    }}
    .pr i.on {{
      background: #ff3b30;
      box-shadow: 0 0 10px #ff3b30;
    }}

    /* Full-Screen Content Canvas */
    .sc-body {{
      position: absolute;
      top: 140px;
      left: 48px;
      right: 48px;
      bottom: 340px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 26px;
      z-index: 5;
    }}

    .card {{
      background: #fff;
      border: 6px solid #111;
      border-radius: 28px;
      box-shadow: 12px 12px 0 #111;
      padding: 34px 44px;
      width: 100%;
      max-width: 980px;
    }}

    .big-title {{
      font: 900 80px/0.95 'Bricolage Grotesque';
      color: #fff;
      -webkit-text-stroke: 4px #111;
      paint-order: stroke fill;
      text-shadow: 8px 8px 0 #111;
      text-align: center;
      text-transform: uppercase;
      letter-spacing: -1px;
    }}

    .sub-stamp {{
      display: inline-block;
      font: 800 34px 'Bricolage Grotesque';
      background: #ffd23f;
      color: #111;
      padding: 10px 28px;
      border: 5px solid #111;
      border-radius: 999px;
      box-shadow: 6px 6px 0 #111;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    /* Code & Terminal Windows */
    .win {{
      background: #181524;
      color: #fff;
      border: 6px solid #111;
      border-radius: 24px;
      box-shadow: 12px 12px 0 #111;
      width: 100%;
      max-width: 980px;
      overflow: hidden;
      font-family: 'IBM Plex Mono', monospace;
    }}
    .win .hd {{
      background: #2b273b;
      padding: 16px 24px;
      display: flex;
      align-items: center;
      gap: 12px;
      border-bottom: 4px solid #111;
      font-size: 24px;
      color: #cbd5e1;
    }}
    .win .hd i {{
      width: 18px;
      height: 18px;
      border-radius: 50%;
      display: inline-block;
    }}
    .win .hd i:nth-child(1) {{ background: #ff5f57; }}
    .win .hd i:nth-child(2) {{ background: #febc2e; }}
    .win .hd i:nth-child(3) {{ background: #28c840; }}
    .win .bd {{
      padding: 34px 44px;
      font-size: 30px;
      line-height: 1.5;
    }}
    .win .bd .c {{ color: #38bdf8; }}
    .win .bd .y {{ color: #ffd23f; }}
    .win .bd .g {{ color: #4ade80; }}

    /* Animations */
    .strike-bar {{
      position: absolute;
      top: 50%;
      left: 10%;
      right: 10%;
      height: 8px;
      background: #ff3b30;
      rotate: -7deg;
      box-shadow: 0 0 16px rgba(255, 59, 48, 0.8);
    }}

    @keyframes jitterBug {{
      0% {{ transform: translate(0, 0) rotate(0deg); }}
      25% {{ transform: translate(-8px, 6px) rotate(-8deg); }}
      75% {{ transform: translate(8px, -6px) rotate(8deg); }}
      100% {{ transform: translate(0, 0) rotate(0deg); }}
    }}

    @keyframes tapFinger {{
      0% {{ transform: translateY(0) scale(1); }}
      100% {{ transform: translateY(24px) scale(0.92); }}
    }}

    @keyframes bobbing {{
      0% {{ transform: translateY(0) rotate(-4deg); }}
      100% {{ transform: translateY(-24px) rotate(4deg); }}
    }}

    @keyframes phoneGlow {{
      0% {{ filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.4)); }}
      100% {{ filter: drop-shadow(0 0 32px rgba(56, 189, 248, 0.95)); }}
    }}

    .lightning-flow {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
    }}
    .lightning-bolt {{
      font-size: 48px;
      color: #ffd23f;
      animation: flashBolt 0.3s infinite alternate;
    }}
    @keyframes flashBolt {{
      0% {{ opacity: 0.3; transform: scale(0.9); }}
      100% {{ opacity: 1; transform: scale(1.15); }}
    }}

    .shockwave-ring {{
      position: absolute;
      width: 220px;
      height: 220px;
      border-radius: 50%;
      border: 4px solid #38bdf8;
      top: 30px;
      animation: shockpulse 1.4s infinite ease-out;
    }}
    @keyframes shockpulse {{
      0% {{ transform: scale(0.5); opacity: 1; }}
      100% {{ transform: scale(2.2); opacity: 0; }}
    }}

    .chk {{
      display: flex;
      flex-direction: column;
      gap: 18px;
      width: 100%;
    }}
    .ck {{
      display: flex;
      align-items: center;
      gap: 20px;
      font: 800 32px 'Bricolage Grotesque';
    }}
    .ck u {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 52px;
      height: 52px;
      background: #22c55e;
      color: #fff;
      border: 4px solid #111;
      border-radius: 14px;
      text-decoration: none;
      font-weight: 900;
      box-shadow: 4px 4px 0 #111;
    }}

    .phone-mock {{
      width: 320px;
      height: 500px;
      background: #111827;
      border: 8px solid #1e293b;
      border-radius: 44px;
      box-shadow: 12px 12px 0 #0f172a;
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 16px;
    }}
    .phone-notch {{
      width: 120px;
      height: 20px;
      background: #000;
      border-radius: 12px;
      margin-bottom: 24px;
    }}
    .screen-grid {{
      width: 100%;
      height: 100%;
      background: #1e293b;
      border-radius: 28px;
      position: relative;
      overflow: hidden;
      padding: 20px 16px;
    }}
    .laser-scanner {{
      position: absolute;
      left: 0;
      right: 0;
      height: 6px;
      background: #ef4444;
      box-shadow: 0 0 16px #ef4444;
      animation: scanLaser 2s infinite ease-in-out;
    }}
    @keyframes scanLaser {{
      0% {{ top: 5%; }}
      50% {{ top: 90%; }}
      100% {{ top: 5%; }}
    }}
    .app-row {{
      display: flex;
      justify-content: space-around;
      margin-top: 10px;
    }}
    .app-icon {{
      width: 60px;
      height: 60px;
      border-radius: 16px;
      background: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 32px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }}
    .bbox {{
      position: absolute;
      left: 12px;
      right: 12px;
      padding: 8px 12px;
      font: 700 18px 'IBM Plex Mono';
      border-radius: 8px;
    }}
    .red-box {{
      border: 3px dashed #ef4444;
      background: rgba(239, 68, 68, 0.2);
      color: #fff;
    }}
    .green-box {{
      border: 3px dashed #22c55e;
      background: rgba(34, 197, 94, 0.2);
      color: #fff;
    }}

    .gauge-box {{
      width: 180px;
      height: 100px;
      border-top-left-radius: 100px;
      border-top-right-radius: 100px;
      background: #f6c85a;
      border: 6px solid #111;
      border-bottom: none;
      position: relative;
      display: flex;
      justify-content: center;
    }}
    .gauge-needle {{
      position: absolute;
      bottom: 0;
      width: 6px;
      height: 80px;
      background: #111;
      transform-origin: bottom center;
      rotate: -45deg;
      animation: needleSweep 1.6s infinite alternate cubic-bezier(0.4, 0, 0.2, 1);
    }}
    @keyframes needleSweep {{
      0% {{ rotate: -45deg; }}
      100% {{ rotate: 55deg; }}
    }}

    .bars {{
      display: flex;
      gap: 10px;
      align-items: flex-end;
      height: 150px;
    }}
    .bars i {{
      width: 22px;
      background: #38bdf8;
      border-radius: 8px;
      animation: eqBar 0.6s infinite alternate ease-in-out;
    }}
    @keyframes eqBar {{
      0% {{ height: 20px; }}
      100% {{ height: var(--h, 120px); }}
    }}

    .fol-btn {{
      font: 900 52px 'Bricolage Grotesque';
      background: #ff1269;
      color: #fff;
      padding: 24px 64px;
      border: 6px solid #fff;
      border-radius: 999px;
      box-shadow: 12px 12px 0 #111;
      animation: pulseBtn 0.9s infinite alternate;
      letter-spacing: 1px;
    }}
    @keyframes pulseBtn {{
      0% {{ transform: scale(0.96); }}
      100% {{ transform: scale(1.04); }}
    }}

    .reactions-row {{
      display: flex;
      gap: 28px;
    }}
    .reaction-ic {{
      width: 80px;
      height: 80px;
      border-radius: 24px;
      background: #fff;
      border: 5px solid #111;
      box-shadow: 6px 6px 0 #111;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 40px;
    }}

    /* ================= PROMINENT LARGE ANCHOR AVATAR RIG (480x520px) ================= */
    #char-rig {{
      position: absolute;
      bottom: 0;
      right: 40px;
      width: 440px;
      height: 480px;
      z-index: 25;
      pointer-events: none;
      filter: drop-shadow(0 16px 28px rgba(0,0,0,0.35));
    }}

    /* Arm Waving Animation */
    #arm-wave {{
      transform-origin: 290px 340px;
      animation: armWave 1.4s ease-in-out infinite alternate;
    }}
    @keyframes armWave {{
      0% {{ transform: rotate(0deg); }}
      100% {{ transform: rotate(-22deg); }}
    }}

    /* Eye Blinking */
    .eye-blink {{
      transform-origin: center;
      animation: eyeBlink 3.2s infinite;
    }}
    @keyframes eyeBlink {{
      0%, 95%, 100% {{ transform: scaleY(1); }}
      97% {{ transform: scaleY(0.1); }}
    }}

    /* ================= KINETIC SUBTITLE TRACKER ================= */
    #word-pill {{
      position: absolute;
      bottom: 40px;
      left: 50%;
      transform: translateX(-50%);
      background: #f6c85a;
      border: 5px solid #111;
      box-shadow: 6px 6px 0 #111;
      border-radius: 20px;
      padding: 12px 36px;
      font: 900 38px 'Bricolage Grotesque', sans-serif;
      color: #111;
      text-transform: uppercase;
      z-index: 100;
      white-space: nowrap;
      letter-spacing: 1px;
    }}
  </style>
</head>
<body>
  <div id="stage" class="rd">
    <!-- Camera Zoom Motion Container -->
    <div id="scene-container">
      <div id="pt">
        <i style="left:8%; --s:14px; --t:9s; --dl:0s;"></i>
        <i style="left:24%; --s:8px; --t:7s; --dl:1.2s;"></i>
        <i style="left:45%; --s:16px; --t:10s; --dl:0.5s;"></i>
        <i style="left:68%; --s:10px; --t:8s; --dl:2.1s;"></i>
        <i style="left:88%; --s:12px; --t:9.5s; --dl:1.7s;"></i>
      </div>

      <!-- Top Header -->
      <div class="top-header">
        <div class="lab" id="top-label">AI OPEN SOURCE</div>
        <div class="pr">
          <i id="pr1"></i>
          <i id="pr2"></i>
          <i id="pr3"></i>
          <span id="pr-text">0/3</span>
        </div>
      </div>

      <!-- 13 Dynamic Micro-Shots -->
      {all_shots_markup}
    </div>

    <!-- Word-by-Word Subtitle Pill -->
    <div id="word-pill">READY</div>

    <!-- Upgraded Large Animated Vector Character Rig (440x480px) -->
    <svg id="char-rig" viewBox="0 0 440 480">
      <!-- Animated Waving Arm -->
      <g id="arm-wave">
        <path d="M 290 350 Q 340 230 310 170" stroke="#1f2937" stroke-width="44" stroke-linecap="round" fill="none" />
        <circle cx="310" cy="155" r="24" fill="#e5b89a" />
      </g>
      <!-- Body & Dark Hoodie -->
      <path d="M 70 480 C 70 380 120 330 220 330 C 320 330 370 380 370 480 Z" fill="#1f2937" />
      <path d="M 204 330 L 204 420 M 236 330 L 236 420" stroke="#fff" stroke-width="5" stroke-linecap="round" />
      <!-- Head -->
      <circle cx="220" cy="230" r="92" fill="#e5b89a" />
      <path d="M 128 220 C 128 125 312 125 312 220 C 290 175 150 175 128 220 Z" fill="#111827" />
      <!-- Red Headset -->
      <path d="M 122 230 A 98 98 0 0 1 318 230" stroke="#ef4444" stroke-width="16" fill="none" />
      <rect x="108" y="200" width="24" height="56" rx="12" fill="#ef4444" />
      <rect x="308" y="200" width="24" height="56" rx="12" fill="#ef4444" />
      <!-- Glasses -->
      <circle cx="185" cy="225" r="30" stroke="#111" stroke-width="9" fill="none" />
      <circle cx="255" cy="225" r="30" stroke="#111" stroke-width="9" fill="none" />
      <line x1="215" y1="225" x2="225" y2="225" stroke="#111" stroke-width="9" />
      <!-- Blinking Eyes -->
      <g class="eye-blink">
        <circle cx="185" cy="225" r="10" fill="#111" />
        <circle cx="255" cy="225" r="10" fill="#111" />
      </g>
      <!-- Dynamic Lip-Sync Mouth States -->
      <g id="mouth-group">
        <ellipse id="m-closed" cx="220" cy="280" rx="22" ry="4" fill="#601a1a" />
        <ellipse id="m-slight" cx="220" cy="280" rx="24" ry="11" fill="#601a1a" style="display:none;" />
        <ellipse id="m-half" cx="220" cy="282" rx="28" ry="20" fill="#601a1a" style="display:none;" />
        <ellipse id="m-wide" cx="220" cy="285" rx="32" ry="32" fill="#601a1a" style="display:none;" />
      </g>
    </svg>
  </div>

  <script>
    const stage = document.getElementById('stage');
    const topLabel = document.getElementById('top-label');
    const prText = document.getElementById('pr-text');
    const pr1 = document.getElementById('pr1');
    const pr2 = document.getElementById('pr2');
    const pr3 = document.getElementById('pr3');
    const wordPill = document.getElementById('word-pill');

    const mClosed = document.getElementById('m-closed');
    const mSlight = document.getElementById('m-slight');
    const mHalf = document.getElementById('m-half');
    const mWide = document.getElementById('m-wide');

    const shotConfigs = {json.dumps(shots)};

    function setMouth(m) {{
      mClosed.style.display = 'none';
      mSlight.style.display = 'none';
      mHalf.style.display = 'none';
      mWide.style.display = 'none';
      if (m === 'wide') mWide.style.display = 'block';
      else if (m === 'half') mHalf.style.display = 'block';
      else if (m === 'slight') mSlight.style.display = 'block';
      else mClosed.style.display = 'block';
    }}

    function setWord(txt) {{
      if (!txt) {{
        wordPill.style.display = 'none';
        return;
      }}
      wordPill.style.display = 'block';
      wordPill.textContent = txt;
    }}

    function mountShot(id) {{
      for (let i = 0; i < {len(shots)}; i++) {{
        const el = document.getElementById('sc' + i);
        if (el) el.style.display = (i === id) ? 'flex' : 'none';
      }}
      const cfg = shotConfigs[id] || shotConfigs[0];
      stage.className = cfg.theme;
      topLabel.textContent = cfg.label;
      prText.textContent = cfg.pr;

      pr1.className = '';
      pr2.className = '';
      pr3.className = '';
      if (cfg.pr === '1/3') {{
        pr1.className = 'on';
      }} else if (cfg.pr === '2/3') {{
        pr1.className = 'on';
        pr2.className = 'on';
      }} else if (cfg.pr === '3/3') {{
        pr1.className = 'on';
        pr2.className = 'on';
        pr3.className = 'on';
      }}
    }}

    // Master GSAP Timeline registered for HyperFrames
    const tl = gsap.timeline({{ paused: true }});
    window.__timelines = window.__timelines || {{}};
    window.__timelines["main"] = tl;

    // Initial state
    mountShot(0);
    setMouth("closed");

    // Shot calls
    {shot_js}

    // Mouth lip-sync calls
    {mouth_js}

    // Word caption calls
    {caption_js}

    // Final timeline boundary
    tl.to({{}}, {{ duration: 0.01 }}, {duration});
  </script>
</body>
</html>
"""

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Update hyperframes.json
    hf_conf = {
        "name": "daily-automation-engine",
        "version": "4.0.0",
        "fps": 30,
        "width": 1080,
        "height": 1920,
        "duration": round(float(duration), 2)
    }
    with open("hyperframes.json", "w") as hf:
        json.dump(hf_conf, hf, indent=2)

    print(f"[✓] Visual Agent complete! Compiled {len(shots)} micro-scenes to {output_html} ({round(len(html_content)/1024, 1)} KB)")
    return output_html

if __name__ == "__main__":
    run_visual_agent()
