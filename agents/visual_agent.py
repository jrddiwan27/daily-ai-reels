import os
import json
import re

def run_visual_agent(
    dossier_path: str = "assets/research_dossier.json",
    script_path: str = "assets/viral_script.json",
    timings_path: str = "assets/section_timings.json",
    timeline_path: str = "assets/word_timeline.json",
    duration: float = 30.0,
    output_html: str = "index.html",
    script_data: dict = None,
    research_dossier: dict = None
) -> str:
    """
    VISUAL AGENT:
    Compiles 1080x1920 Full HD Kinetic Explainer Composition matching the user's
    exact animated explainer template:
    - Prominent animated host avatar with headphones, glasses, blushing cheeks,
      waving arm, bobbing head, talking mouth, and wooden tech desk.
    - Dynamic color-shifting stage backgrounds (Coral Red, Vibrant Yellow, Tech Blue, Emerald Green, Pink, Dark).
    - Scanlines, ambient bubble particles, and fast flash cut transitions.
    - Code/terminal windows, big typography, popping checklists, badges, and equalizer bars.
    - Word-by-word highlighted yellow pill captions right above the desk.
    """
    print("=" * 65)
    print("🎨 [AGENT 4: VISUAL AGENT] Compiling Animated Explainer Composition with Host Avatar...")
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
    cta_keyword = script_data.get("cta_keyword", "WORKFLOW").upper()

    section_timings = []
    if os.path.exists(timings_path):
        with open(timings_path, "r") as f:
            section_timings = json.load(f)

    word_timeline = []
    if os.path.exists(timeline_path):
        with open(timeline_path, "r") as f:
            word_timeline = json.load(f)

    # Clean items
    it1 = items[0] if len(items) > 0 else {"name": "Hermes AI", "title": "Hermes AI Engine", "description": "Local agent execution"}
    it2 = items[1] if len(items) > 1 else {"name": "vLLM-SR", "title": "vLLM Semantic Router", "description": "Sub-millisecond routing"}
    it3 = items[2] if len(items) > 2 else {"name": "Mistral Large", "title": "Mistral Large 4", "description": "1.05T Multimodal Preview"}

    def clean_name(it):
        n = it.get("name") or it.get("title") or "AI TOOL"
        return n.split("·")[0].split("–")[0].split(":")[0].strip()[:24]

    name1 = clean_name(it1)
    name2 = clean_name(it2)
    name3 = clean_name(it3)

    # Extract exact section start times from voiceover timings
    timings_map = {st["label"]: st for st in section_timings}
    t_hook = timings_map.get("hook", {}).get("start", 0.0)
    t_shift = timings_map.get("shift", {}).get("start", 4.0)
    t_tool1 = timings_map.get("tool_1", {}).get("start", 8.0)
    t_tool2 = timings_map.get("tool_2", {}).get("start", 14.0)
    t_tool3 = timings_map.get("tool_3", {}).get("start", 20.0)
    t_cta = timings_map.get("cta", {}).get("start", 26.0)

    # 6 Scenes
    scenes_meta = [
        {"id": 0, "start": t_hook, "theme": "rd", "label": "BEFORE YOU PROMPT", "pr": 0},
        {"id": 1, "start": t_shift, "theme": "yl", "label": "THE FIX · 3 TOOLS", "pr": 0},
        {"id": 2, "start": t_tool1, "theme": "bl", "label": f"01 · {name1.upper()[:16]}", "pr": 1},
        {"id": 3, "start": t_tool2, "theme": "gr", "label": f"02 · {name2.upper()[:16]}", "pr": 2},
        {"id": 4, "start": t_tool3, "theme": "pk", "label": f"03 · {name3.upper()[:16]}", "pr": 3},
        {"id": 5, "start": t_cta, "theme": "dk", "label": "FREE GITHUB REPOS", "pr": 3}
    ]

    # Generate frame-accurate SFX cues
    sfx_cues = [
        {"time": round(t_hook, 2), "type": "boom"},
        {"time": round(t_hook + 0.1, 2), "type": "whoosh"},
        {"time": round(t_hook + 0.5, 2), "type": "pop"},
        {"time": round(t_shift, 2), "type": "whoosh"},
        {"time": round(t_shift + 0.4, 2), "type": "pop"},
        {"time": round(t_shift + 1.0, 2), "type": "ding"},
        {"time": round(t_tool1, 2), "type": "whoosh"},
        {"time": round(t_tool1 + 0.3, 2), "type": "pop"},
        {"time": round(t_tool1 + 0.8, 2), "type": "ding"},
        {"time": round(t_tool2, 2), "type": "whoosh"},
        {"time": round(t_tool2 + 0.3, 2), "type": "pop"},
        {"time": round(t_tool2 + 0.8, 2), "type": "ding"},
        {"time": round(t_tool3, 2), "type": "whoosh"},
        {"time": round(t_tool3 + 0.3, 2), "type": "pop"},
        {"time": round(t_tool3 + 0.8, 2), "type": "ding"},
        {"time": round(t_cta, 2), "type": "boom"},
        {"time": round(t_cta + 0.2, 2), "type": "ding"},
        {"time": round(t_cta + 0.6, 2), "type": "pop"}
    ]

    with open("assets/sfx_cues.json", "w") as f:
        json.dump(sfx_cues, f, indent=2)

    # Subtitle word timeline schedule
    caption_calls = []
    for w_info in word_timeline:
        w = w_info.get("word", "").replace('"', '\\"')
        caption_calls.append(f'tl.call(() => setWord("{w}"), null, {w_info.get("start", 0)});')
    caption_calls.append(f'tl.call(() => setWord(""), null, {max(0, duration - 0.2)});')

    # Scene transition calls
    scene_calls = []
    for s in scenes_meta:
        scene_calls.append(f'tl.call(() => mountScene({s["id"]}), null, {s["start"]});')

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Daily AI Explainer</title>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;800;900&family=IBM+Plex+Mono:wght@500;700&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <style>
    :root {{
      --page: #e9e5dc;
      --clay: #d9694a;
    }}
    html, body {{
      margin: 0;
      padding: 0;
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #0f0e0d;
      font-family: 'Bricolage Grotesque', system-ui, sans-serif;
    }}

    /* Scaler: Native 3x rendering into 1080x1920 Full HD */
    #scaler {{
      width: 360px;
      height: 640px;
      transform: scale(3);
      transform-origin: 0 0;
      position: absolute;
      left: 0;
      top: 0;
    }}

    #stage {{
      --b: #e8695c;
      --d: #b8352b;
      position: absolute;
      left: 0;
      top: 0;
      width: 360px;
      height: 640px;
      overflow: hidden;
      background: var(--b);
      transition: background 0.25s ease;
      color: #111;
    }}

    #stage.rd {{ --b: #e8695c; --d: #b8352b; }}
    #stage.bl {{ --b: #6f9ee8; --d: #2147b8; }}
    #stage.gr {{ --b: #7fcfb3; --d: #0f7a5c; }}
    #stage.yl {{ --b: #f6c85a; --d: #d97a14; }}
    #stage.pk {{ --b: #f3a6c8; --d: #b3407a; }}
    #stage.dk {{ --b: #17141f; --d: #3a2f5c; color: #fff; }}

    /* Background kinetic moving scanlines */
    #stage::before {{
      content: "";
      position: absolute;
      inset: 0;
      background: repeating-linear-gradient(90deg, rgba(255, 255, 255, 0.12) 0 22px, transparent 22px 44px);
      animation: gs 1.6s linear infinite;
      pointer-events: none;
      z-index: 1;
    }}
    @keyframes gs {{
      to {{ background-position: 44px 0; }}
    }}

    #scene-container {{
      position: absolute;
      inset: 0;
      z-index: 2;
    }}

    .sc {{
      position: absolute;
      inset: 0;
      padding-top: 54px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
    }}

    .a {{
      animation: bob 1.5s ease-in-out infinite alternate;
    }}
    .pop {{
      animation: pop 0.45s cubic-bezier(0.3, 1.7, 0.5, 1) forwards, bob 1.2s ease-in-out infinite alternate;
    }}
    @keyframes pop {{
      from {{ opacity: 0; transform: scale(0.6) rotate(-6deg); }}
      to {{ opacity: 1; transform: none; }}
    }}
    @keyframes bob {{
      from {{ translate: 0 -4px; }}
      to {{ translate: 0 5px; }}
    }}

    /* Rising ambient particles */
    #pt {{
      position: absolute;
      inset: 0;
      overflow: hidden;
      pointer-events: none;
      z-index: 2;
    }}
    #pt i {{
      position: absolute;
      bottom: -10px;
      width: var(--s);
      height: var(--s);
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.65);
      animation: rise var(--t) var(--dl) linear infinite;
    }}
    @keyframes rise {{
      to {{ transform: translate(20px, -680px); }}
    }}

    /* Screen flash cut */
    #fl {{
      position: absolute;
      inset: 0;
      background: #111;
      transform: translateX(-101%);
      pointer-events: none;
      z-index: 60;
    }}
    @keyframes fl {{
      0% {{ transform: translateX(-101%); }}
      50% {{ transform: translateX(0); }}
      100% {{ transform: translateX(101%); }}
    }}

    /* Top navigation badges */
    .lab {{
      position: absolute;
      top: 14px;
      left: 12px;
      background: #111;
      color: #fff;
      font: 700 10px 'IBM Plex Mono', monospace;
      padding: 5px 9px;
      rotate: -1.5deg;
      z-index: 10;
    }}
    .pr {{
      position: absolute;
      top: 12px;
      right: 12px;
      display: flex;
      gap: 4px;
      align-items: center;
      background: #fff;
      border: 3px solid #111;
      border-radius: 99px;
      padding: 3px 8px;
      font: 700 9px 'IBM Plex Mono', monospace;
      color: #111;
      z-index: 10;
    }}
    .pr i {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      border: 2px solid #111;
      background: #fff;
    }}
    .pr i.on {{
      background: #ff3b30;
    }}

    /* Mac / Terminal windows */
    .win {{
      width: 300px;
      background: #14121a;
      color: #fff;
      border: 3px solid #111;
      border-radius: 12px;
      box-shadow: 5px 5px 0 #111;
      font: 500 11px 'IBM Plex Mono', monospace;
      overflow: hidden;
      margin-top: 6px;
      text-align: left;
    }}
    .win .hd {{
      background: #2a2633;
      padding: 6px 10px;
      display: flex;
      gap: 5px;
      align-items: center;
      font-size: 9px;
      color: #aaa;
      border-bottom: 2px solid #111;
    }}
    .win .hd i {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #ff5f57;
      display: inline-block;
    }}
    .win .hd i:nth-child(2) {{ background: #febc2e; }}
    .win .hd i:nth-child(3) {{ background: #28c840; margin-right: 6px; }}
    .win .bd {{
      padding: 10px;
      line-height: 1.6;
    }}
    .ty {{
      display: block;
      overflow: hidden;
      white-space: nowrap;
      color: #fff;
    }}
    .ty.g {{ color: #f6c85a; }}

    .st {{
      position: absolute;
      font: 800 24px 'Bricolage Grotesque';
      border: 4px solid;
      padding: 2px 10px;
      rotate: -10deg;
      border-radius: 6px;
    }}
    .big {{
      font: 800 48px/0.95 'Bricolage Grotesque';
      color: #fff;
      -webkit-text-stroke: 3px #111;
      paint-order: stroke fill;
      text-shadow: 5px 5px 0 #111;
      text-align: center;
      margin-top: 14px;
    }}

    .bars {{
      display: flex;
      gap: 8px;
      align-items: flex-end;
      height: 70px;
      margin-top: 8px;
    }}
    .bars i {{
      width: 20px;
      height: var(--h);
      background: #fff;
      border: 3px solid #111;
      transform-origin: bottom;
      animation: bar 0.45s infinite alternate;
    }}
    @keyframes bar {{
      to {{ scale: 1 0.55; }}
    }}

    .slot {{
      width: 70px;
      height: 70px;
      border: 4px solid #111;
      border-radius: 12px;
      background: #fff;
      font: 800 36px/62px 'Bricolage Grotesque';
      text-align: center;
      box-shadow: 4px 4px 0 #111;
    }}
    .row3 {{
      display: flex;
      gap: 12px;
      margin-top: 6px;
    }}

    /* Checklist */
    .chk {{
      width: 280px;
      background: #fff;
      border: 4px solid #111;
      border-radius: 12px;
      box-shadow: 5px 5px 0 #111;
      padding: 6px 14px;
      margin-top: 6px;
      text-align: left;
    }}
    .ck {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 800;
      font-size: 14px;
      padding: 5px 0;
      color: #111;
      border-bottom: 2px dashed #ccc;
    }}
    .ck:last-child {{ border-bottom: none; }}
    .ck u {{
      width: 20px;
      height: 20px;
      border-radius: 6px;
      background: #22c55e;
      color: #fff;
      text-decoration: none;
      font-size: 13px;
      display: grid;
      place-items: center;
      border: 2px solid #111;
      flex-shrink: 0;
    }}

    .stamp {{
      font: 800 24px 'Bricolage Grotesque';
      border: 4px solid #111;
      border-radius: 10px;
      padding: 4px 18px;
      box-shadow: 5px 5px 0 #111;
      margin-top: 6px;
      display: inline-block;
    }}

    .fol {{
      background: #ff2d55;
      color: #fff;
      border: 4px solid #fff;
      border-radius: 99px;
      font: 800 28px 'Bricolage Grotesque';
      padding: 6px 30px;
      margin-top: 24px;
      animation: pu 1s infinite;
      box-shadow: 5px 5px 0 #111;
    }}
    @keyframes pu {{
      0% {{ box-shadow: 0 0 0 0 rgba(255, 45, 85, 0.7), 5px 5px 0 #111; }}
      100% {{ box-shadow: 0 0 0 20px transparent, 5px 5px 0 #111; }}
    }}

    .ic {{
      width: 48px;
      height: 48px;
      border-radius: 14px;
      background: #fff;
      color: #111;
      display: grid;
      place-items: center;
      font-size: 22px;
      border: 3px solid #111;
      box-shadow: 4px 4px 0 #111;
    }}

    /* Host Avatar + Tech Desk */
    #desk {{
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      height: 112px;
      background: repeating-linear-gradient(90deg, rgba(0, 0, 0, 0.14) 0 3px, transparent 3px 120px), var(--d);
      border-top: 5px solid #111;
      z-index: 3;
      transition: background 0.25s;
    }}

    #ch {{
      position: absolute;
      right: 4px;
      bottom: 100px;
      width: 178px;
      z-index: 4;
      animation: bnc 0.5s ease-in-out infinite alternate;
    }}
    @keyframes bnc {{
      to {{ translate: 0 -5px; }}
    }}

    #hd {{
      transform-origin: 100px 150px;
      animation: nod 0.6s ease-in-out infinite alternate;
    }}
    @keyframes nod {{
      from {{ rotate: -3deg; }}
      to {{ rotate: 3deg; }}
    }}

    .arm {{
      transform-origin: 52px 172px;
      animation: wave 0.9s ease-in-out infinite alternate;
    }}
    @keyframes wave {{
      from {{ rotate: -20deg; }}
      to {{ rotate: 12deg; }}
    }}

    .eye {{
      transform-box: fill-box;
      transform-origin: center;
      animation: blink 2.8s infinite;
    }}
    @keyframes blink {{
      0%, 93%, 100% {{ scale: 1; }}
      96% {{ scale: 1 0.1; }}
    }}

    .mouth {{
      transform-box: fill-box;
      transform-origin: center;
      scale: 1 0.4;
      animation: talk 0.18s infinite alternate;
    }}
    @keyframes talk {{
      to {{ scale: 1.1 1.5; }}
    }}

    .brow {{
      animation: brw 1.3s infinite alternate;
    }}
    @keyframes brw {{
      to {{ translate: 0 -3px; }}
    }}

    /* Caption Word Pill */
    #cap {{
      position: absolute;
      left: 0;
      right: 0;
      bottom: 30px;
      text-align: center;
      z-index: 10;
      pointer-events: none;
    }}
    #cap .w {{
      display: inline-block;
      font: 800 28px 'Bricolage Grotesque';
      background: #ffd23f;
      color: #111;
      border: 4px solid #111;
      border-radius: 10px;
      padding: 2px 16px;
      box-shadow: 5px 5px 0 #111;
      animation: cp 0.2s cubic-bezier(0.3, 1.8, 0.5, 1);
    }}
    @keyframes cp {{
      from {{ scale: 0.7; rotate: -5deg; }}
    }}
  </style>
</head>
<body>

  <div id="scaler">
    <div id="stage" class="rd">
      <div id="pt"></div>
      <div id="fl"></div>

      <!-- Persistent Top Navigation -->
      <div id="top-label" class="lab">BEFORE YOU PROMPT</div>
      <div id="top-pr" class="pr"><i></i><i></i><i></i> 0/3</div>

      <!-- Kinetic Scenes Container -->
      <div id="scene-container">
        <!-- Scene 0: Hook -->
        <div id="sc-0" class="sc">
          <div class="win a">
            <div class="hd"><i></i><i></i><i></i>terminal</div>
            <div class="bd">
              <span class="ty">> stop paying expensive SaaS</span>
              <span class="ty g">> open-source AI does this now</span>
            </div>
          </div>
          <div class="big pop">STOP<br>WASTING<br>HOURS</div>
          <div class="bars">
            <i style="--h:45px; animation-delay:-0.1s;"></i>
            <i style="--h:70px; animation-delay:-0.3s; background:#ff3b30;"></i>
            <i style="--h:50px; animation-delay:-0.5s;"></i>
            <i style="--h:65px; animation-delay:-0.2s; background:#ff3b30;"></i>
            <i style="--h:40px; animation-delay:-0.4s;"></i>
          </div>
        </div>

        <!-- Scene 1: Shift -->
        <div id="sc-1" class="sc" style="display:none; opacity:0;">
          <div class="big pop" style="font-size:110px; margin-top:8px;">3</div>
          <div class="stamp pop" style="background:#22c55e; color:#fff; rotate:2deg;">NEW AI TOOLS</div>
          <div class="row3">
            <div class="slot pop">1</div>
            <div class="slot pop">2</div>
            <div class="slot pop">3</div>
          </div>
        </div>

        <!-- Scene 2: Tool 1 -->
        <div id="sc-2" class="sc" style="display:none; opacity:0;">
          <div class="win a">
            <div class="hd"><i></i><i></i><i></i>{name1.lower()[:18]}</div>
            <div class="bd">
              <span class="ty">> {it1.get('description', 'High performance model')[:36]}</span>
              <span class="ty g">> Sub-millisecond response</span>
            </div>
          </div>
          <div class="chk a">
            <div class="ck"><u>✔</u>Zero Monthly Fees</div>
            <div class="ck"><u>✔</u>100% Local Inference</div>
            <div class="ck"><u>✔</u>Open Source Weights</div>
          </div>
        </div>

        <!-- Scene 3: Tool 2 -->
        <div id="sc-3" class="sc" style="display:none; opacity:0;">
          <div class="win a">
            <div class="hd"><i></i><i></i><i></i>{name2.lower()[:18]}</div>
            <div class="bd">
              <span class="ty">> {it2.get('description', 'Autonomous agent')[:36]}</span>
              <span class="ty g">> Executes complex workflows</span>
            </div>
          </div>
          <div class="chk a">
            <div class="ck"><u>✔</u>Autonomous Pipelines</div>
            <div class="ck"><u>✔</u>Zero Cloud Lock-in</div>
            <div class="ck"><u>✔</u>Deterministic Speed</div>
          </div>
        </div>

        <!-- Scene 4: Tool 3 -->
        <div id="sc-4" class="sc" style="display:none; opacity:0;">
          <div class="win a">
            <div class="hd"><i></i><i></i><i></i>{name3.lower()[:18]}</div>
            <div class="bd">
              <span class="ty">> {it3.get('description', 'Instant extraction')[:36]}</span>
              <span class="ty g">> WebAssembly Runtime</span>
            </div>
          </div>
          <div class="chk a">
            <div class="ck"><u>✔</u>Browser & Local Execution</div>
            <div class="ck"><u>✔</u>Zero API Latency</div>
            <div class="ck"><u>✔</u>Production Ready</div>
          </div>
        </div>

        <!-- Scene 5: Viral CTA -->
        <div id="sc-5" class="sc" style="display:none; opacity:0;">
          <div class="stamp pop" style="background:#ffd23f; rotate:-3deg; margin-top:12px;">COMMENT "{cta_keyword}"</div>
          <div class="fol">FOLLOW @JAYANT</div>
          <div style="display:flex; gap:14px; margin-top:14px;">
            <div class="ic pop">♥</div>
            <div class="ic pop">🔖</div>
            <div class="ic pop">↗</div>
          </div>
        </div>
      </div>

      <!-- Wooden Tech Desk -->
      <div id="desk"></div>

      <!-- Animated Host Character SVG -->
      <svg id="ch" viewBox="0 0 200 220">
        <g class="arm">
          <path d="M52 176Q18 156 18 114" stroke="#2b2f45" stroke-width="24" fill="none" stroke-linecap="round"/>
          <circle cx="18" cy="104" r="13" fill="#f0c19b"/>
        </g>
        <path d="M26 220Q28 160 100 154Q172 160 174 220Z" fill="#2b2f45"/>
        <path d="M84 156Q100 178 116 156Z" fill="#e0ad86"/>
        <path d="M92 172v28M108 172v28" stroke="#fff" stroke-width="3" stroke-linecap="round"/>
        <g id="hd">
          <rect x="88" y="128" width="24" height="30" fill="#e0ad86"/>
          <ellipse cx="100" cy="98" rx="46" ry="50" fill="#f0c19b"/>
          <path d="M54 94Q54 44 100 44Q146 44 146 94Q130 68 100 68Q70 68 54 94Z" fill="#2a1d1a"/>
          <path d="M50 98Q48 34 100 34Q152 34 150 98" fill="none" stroke="#d9694a" stroke-width="8"/>
          <rect x="40" y="86" width="16" height="32" rx="8" fill="#d9694a"/>
          <rect x="144" y="86" width="16" height="32" rx="8" fill="#d9694a"/>
          <g class="eye">
            <circle cx="82" cy="101" r="5" fill="#222"/>
            <circle cx="118" cy="101" r="5" fill="#222"/>
          </g>
          <g fill="none" stroke="#222" stroke-width="3">
            <circle cx="82" cy="101" r="15"/>
            <circle cx="118" cy="101" r="15"/>
            <path d="M97 101h6"/>
          </g>
          <path class="brow" d="M70 80q12-7 24 0M106 80q12-7 24 0" stroke="#2a1d1a" stroke-width="4" fill="none" stroke-linecap="round"/>
          <ellipse class="mouth" cx="100" cy="130" rx="11" ry="8" fill="#7a2a2a"/>
          <circle cx="66" cy="120" r="6" fill="#f08a7a" opacity=".5"/>
          <circle cx="134" cy="120" r="6" fill="#f08a7a" opacity=".5"/>
        </g>
      </svg>

      <!-- Active Kinetic Caption Bar -->
      <div id="cap">
        <span id="cap-word" class="w">WATCH THIS</span>
      </div>
    </div>
  </div>

  <script>
    // Particle dots
    const pt = document.getElementById("pt");
    for (let i = 0; i < 20; i++) {{
      const dot = document.createElement("i");
      dot.style.cssText = `left: ${{Math.random() * 100}}%; --s: ${{3 + Math.random() * 6}}px; --t: ${{2.5 + Math.random() * 3}}s; --dl: -${{Math.random() * 5}}s;`;
      pt.appendChild(dot);
    }}

    const scenes = {json.dumps(scenes_meta)};
    const stage = document.getElementById("stage");
    const topLabel = document.getElementById("top-label");
    const topPr = document.getElementById("top-pr");
    const capWord = document.getElementById("cap-word");
    const fl = document.getElementById("fl");

    function mountScene(id) {{
      const s = scenes[id];
      if (!s) return;

      // Update stage theme
      stage.className = s.theme;
      topLabel.textContent = s.label;

      // Update progress dots
      const p = s.pr;
      topPr.innerHTML = `
        <i class="${{p >= 1 ? 'on' : ''}}"></i>
        <i class="${{p >= 2 ? 'on' : ''}}"></i>
        <i class="${{p >= 3 ? 'on' : ''}}"></i>
        ${{p}}/3
      `;

      // Switch visible scene div
      for (let i = 0; i < scenes.length; i++) {{
        const el = document.getElementById("sc-" + i);
        if (el) {{
          if (i === id) {{
            el.style.display = "flex";
            el.style.opacity = 1;
          }} else {{
            el.style.display = "none";
            el.style.opacity = 0;
          }}
        }}
      }}

      // Flash transition cut
      fl.style.animation = "none";
      void fl.offsetWidth;
      fl.style.animation = "fl 0.28s ease-out";
    }}

    function setWord(w) {{
      if (!w) {{
        capWord.style.display = "none";
        return;
      }}
      capWord.textContent = w;
      capWord.style.display = "inline-block";
    }}

    // GSAP master timeline driving HyperFrames
    const tl = gsap.timeline({{ paused: true }});
    window.__timelines = window.__timelines || {{}};
    window.__timelines["main"] = tl;

    // Initial mount
    mountScene(0);

    // Call schedule
    {chr(10).join("    " + c for c in scene_calls)}
    {chr(10).join("    " + c for c in caption_calls)}

    // Final timeline boundary
    tl.to({{}}, {{ duration: 0.01 }}, {duration});
  </script>
</body>
</html>"""

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Update hyperframes.json
    hf_config = {
        "name": "daily-automation-engine",
        "version": "4.2.0",
        "fps": 30,
        "width": 1080,
        "height": 1920,
        "duration": round(duration, 2)
    }
    with open("hyperframes.json", "w") as f:
        json.dump(hf_config, f, indent=2)

    print(f"[✓] Visual Composition compiled to {output_html} ({duration:.2f}s, 1080x1920 @ 30fps with Host Avatar)")
    print(f"[✓] Frame-accurate SFX cues written: {len(sfx_cues)} cues in assets/sfx_cues.json")
    return output_html

if __name__ == "__main__":
    run_visual_agent()
