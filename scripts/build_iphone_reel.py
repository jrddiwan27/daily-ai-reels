import os
import re
import json
import subprocess
import numpy as np
from pipeline.lipsync_engine import generate_lipsync_data
from pipeline.audio_enhancer import produce_master_audio

def parse_vtt(vtt_path):
    with open(vtt_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.strip().split("\n\n")
    cues = []
    for b in blocks:
        lines = [line.strip() for line in b.split("\n") if line.strip()]
        if len(lines) >= 2:
            time_line = None
            text_lines = []
            for l in lines:
                if "-->" in l:
                    time_line = l
                elif not l.isdigit() and time_line:
                    text_lines.append(l)
            if time_line and text_lines:
                m = re.match(r"(\d+):(\d+):(\d+)[,\.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,\.](\d+)", time_line)
                if m:
                    h1, m1, s1, ms1, h2, m2, s2, ms2 = map(int, m.groups())
                    t_start = h1 * 3600 + m1 * 60 + s1 + ms1 / 1000.0
                    t_end = h2 * 3600 + m2 * 60 + s2 + ms2 / 1000.0
                    text = " ".join(text_lines)
                    cues.append({"start": round(t_start, 3), "end": round(t_end, 3), "text": text})
    return cues

def main():
    voice_path = "assets/voice_iphone.mp3"
    vtt_path = "assets/voice_iphone.vtt"

    # Get duration
    cmd_dur = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", voice_path
    ]
    duration = round(float(subprocess.check_output(cmd_dur).decode().strip()), 2)
    print(f"[*] Voice duration: {duration}s")

    # Parse cues
    vtt_cues = parse_vtt(vtt_path)
    print(f"[*] Parsed {len(vtt_cues)} VTT subtitle cues")

    # Generate 1-2 word caption chunks for kinetic word animations
    caption_chunks = []
    for cue in vtt_cues:
        words = cue["text"].split()
        if not words:
            continue
        step = (cue["end"] - cue["start"]) / len(words)
        for i, w in enumerate(words):
            w_start = round(cue["start"] + i * step, 3)
            w_end = round(w_start + step, 3)
            caption_chunks.append({"start": w_start, "end": w_end, "text": w})

    with open("assets/caption_chunks_iphone.json", "w") as f:
        json.dump(caption_chunks, f, indent=2)

    # Generate Lip-sync mouth data
    print("[*] Generating RMS lip-sync mouth data...")
    mouth_data = generate_lipsync_data(
        audio_path=voice_path,
        caption_chunks_path="assets/caption_chunks_iphone.json",
        output_mouth_path="assets/mouth_iphone.json",
        fps=30
    )
    print(f"[✓] Generated {len(mouth_data)} mouth frames")

    # Define Scenes based on VTT cues:
    # Scene 1: Stop testing mobile apps manually. An open-source AI agent just learned how to control your physical iPhone over USB. (0.05 -> 7.59)
    # Scene 2: Cloud bots can only test web browsers. They cannot touch real iOS apps or bypass device security. (7.59 -> 14.10)
    # Scene 3: Meet iPhone Use. A brand new open-source repo with three thousand GitHub stars. (14.10 -> 19.44)
    # Scene 4: One. Plug your iPhone into your Mac with a USB cable. Zero jailbreak needed. (19.44 -> 24.52)
    # Scene 5: Two. The AI captures the live screen, detects every button, and taps and swipes in real time. (24.52 -> 31.42)
    # Scene 6: Three. It runs completely offline using local models, or connects directly to Claude and GPT-4o. (31.42 -> 38.90)
    # Scene 7: Setup takes two commands. Pip install iphone use, and your agent is tapping your screen. (38.90 -> 44.25)
    # Scene 8: Comment IPHONE below, and I will DM you the direct GitHub repo link and setup guide right now. (44.25 -> duration)
    scenes = [
        {"idx": 0, "start": 0.0, "end": 7.59, "theme": "rd", "label": "MANUAL TESTING IS DEAD", "num": "0/3"},
        {"idx": 1, "start": 7.59, "end": 14.10, "theme": "yl", "label": "THE BOTTLENECK", "num": "0/3"},
        {"idx": 2, "start": 14.10, "end": 19.44, "theme": "bl", "label": "GITHUB REVEAL", "num": "0/3"},
        {"idx": 3, "start": 19.44, "end": 24.52, "theme": "gr", "label": "01 · DIRECT HARDWARE", "num": "1/3"},
        {"idx": 4, "start": 24.52, "end": 31.42, "theme": "pk", "label": "02 · VISION GROUNDING", "num": "2/3"},
        {"idx": 5, "start": 31.42, "end": 38.90, "theme": "yl", "label": "03 · LOCAL INFERENCE", "num": "3/3"},
        {"idx": 6, "start": 38.90, "end": 44.25, "theme": "dk", "label": "TERMINAL INSTALL", "num": "3/3"},
        {"idx": 7, "start": 44.25, "end": duration, "theme": "rd", "label": "DM AUTOMATION", "num": "3/3"}
    ]

    # Generate SFX cues
    sfx_cues = []
    for sc in scenes:
        t = sc["start"]
        sfx_cues.append({"type": "whoosh", "time": t})
        sfx_cues.append({"type": "pop", "time": round(t + 0.3, 3)})
        if sc["idx"] in [0, 2, 6, 7]:
            sfx_cues.append({"type": "boom", "time": round(t + 0.05, 3)})
        if sc["idx"] in [3, 4, 5]:
            sfx_cues.append({"type": "ding", "time": round(t + 0.8, 3)})
            sfx_cues.append({"type": "click", "time": round(t + 1.6, 3)})

    with open("assets/sfx_cues_iphone.json", "w") as f:
        json.dump(sfx_cues, f, indent=2)

    # Produce Master Audio (Voice + SFX + ducked BGM)
    master_audio_path = "assets/master_audio_iphone.mp3"
    print("[*] Mixing master audio with ducked beat and 30+ SFX cues...")
    produce_master_audio(
        voice_path=voice_path,
        output_audio=master_audio_path,
        duration=duration,
        scene_transitions=[(c["type"], float(c["time"])) for c in sfx_cues]
    )

    # Update hyperframes.json
    hf_config = {
        "name": "daily-automation-engine",
        "version": "3.1.0",
        "fps": 30,
        "width": 1080,
        "height": 1920,
        "duration": duration
    }
    with open("hyperframes.json", "w") as f:
        json.dump(hf_config, f, indent=2)

    # Build mouth calls for GSAP
    mouth_calls = []
    last_m = None
    for item in mouth_data:
        m = item.get("mouth", "closed")
        f = item.get("f", 0)
        t = round(f / 30.0, 3)
        if m != last_m and t <= duration:
            mouth_calls.append(f'tl.call(() => setMouth("{m}"), null, {t});')
            last_m = m

    # Build scene transitions for GSAP
    scene_calls = []
    for sc in scenes:
        scene_calls.append(f'tl.call(() => mountScene({sc["idx"]}), null, {sc["start"]});')

    # Build caption calls for GSAP
    caption_calls = []
    for c in caption_chunks:
        caption_calls.append(f'tl.call(() => setWord({json.dumps(c["text"])}), null, {c["start"]});')
    caption_calls.append(f'tl.call(() => setWord(""), null, {duration - 0.2});')

    # Compile the upgraded 1080x1920 HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=1080, height=1920, initial-scale=1">
  <title>iPhone-Use: AI Controls iPhone Over USB</title>
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

    /* Full Stage (1080x1920) */
    #stage {{
      position: absolute;
      inset: 0;
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: var(--b, #e8695c);
      transition: background 0.3s ease;
      color: #111;
    }}

    /* Dynamic Theme Color Palettes (Matches Claude Template) */
    #stage.rd {{ --b: #e8695c; --d: #b8352b; }}
    #stage.yl {{ --b: #f6c85a; --d: #d97a14; }}
    #stage.bl {{ --b: #6f9ee8; --d: #2147b8; }}
    #stage.gr {{ --b: #7fcfb3; --d: #0f7a5c; }}
    #stage.pk {{ --b: #f3a6c8; --d: #b3407a; }}
    #stage.dk {{ --b: #17141f; --d: #3a2f5c; color: #fff; }}

    /* Infinite Moving Background Stripes (Zero Static Seconds) */
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

    /* Global Subtle Camera Zoom/Tilt Drift */
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

    /* Ambient Floating Dust / Glow Particles */
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

    /* Flash Transition Wipe */
    #fl {{
      position: absolute;
      inset: 0;
      background: #111;
      transform: translateX(-101%);
      pointer-events: none;
      z-index: 15;
    }}
    @keyframes flashWipe {{
      0% {{ transform: translateX(-101%); }}
      50% {{ transform: translateX(0%); }}
      100% {{ transform: translateX(101%); }}
    }}

    /* Top Badges (Neo-Brutalist Tilted Header) */
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

    /* Active Content Canvas (Fill the Middle - Zero Empty Space!) */
    .sc-body {{
      position: absolute;
      top: 170px;
      left: 48px;
      right: 48px;
      bottom: 290px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 32px;
      z-index: 5;
    }}

    /* Neo-Brutalist Cards */
    .card {{
      background: #fff;
      border: 6px solid #111;
      border-radius: 28px;
      box-shadow: 12px 12px 0 #111;
      padding: 36px 44px;
      width: 100%;
      max-width: 980px;
    }}

    /* Big Punchy Neo-Brutalist Typography */
    .big-title {{
      font: 900 84px/0.95 'Bricolage Grotesque';
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
      font: 800 38px 'Bricolage Grotesque';
      background: #ffd23f;
      color: #111;
      border: 5px solid #111;
      padding: 10px 28px;
      border-radius: 16px;
      box-shadow: 6px 6px 0 #111;
      rotate: -4deg;
    }}

    /* Terminal / IDE Window */
    .win {{
      width: 100%;
      background: #14121a;
      color: #fff;
      border: 6px solid #111;
      border-radius: 24px;
      box-shadow: 12px 12px 0 #111;
      font: 600 32px/1.7 'IBM Plex Mono', monospace;
      overflow: hidden;
    }}
    .win .hd {{
      background: #2a2633;
      padding: 16px 24px;
      display: flex;
      gap: 12px;
      align-items: center;
      font-size: 24px;
      color: #aaa;
      border-bottom: 4px solid #111;
    }}
    .win .hd i {{
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: #ff5f57;
      border: 2px solid #111;
    }}
    .win .hd i+i {{ background: #febc2e; }}
    .win .hd i+i+i {{ background: #28c840; margin-right: 14px; }}
    .win .bd {{
      padding: 32px 36px;
    }}
    .win .g {{ color: #22c55e; }}
    .win .y {{ color: #ffd23f; }}
    .win .c {{ color: #38bdf8; }}

    /* Physical Phone Device Mockup */
    .phone-mock {{
      width: 440px;
      height: 740px;
      background: #0f172a;
      border: 8px solid #111;
      border-radius: 56px;
      box-shadow: 14px 14px 0 #111;
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 24px 20px;
      color: #fff;
    }}
    .phone-notch {{
      width: 150px;
      height: 28px;
      background: #000;
      border-radius: 20px;
      margin-bottom: 24px;
    }}
    .screen-grid {{
      width: 100%;
      flex: 1;
      background: #1e293b;
      border-radius: 36px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 18px;
      position: relative;
    }}
    .app-row {{
      display: flex;
      gap: 16px;
      justify-content: space-around;
    }}
    .app-icon {{
      width: 72px;
      height: 72px;
      border-radius: 18px;
      background: #fff;
      border: 4px solid #111;
      display: grid;
      place-items: center;
      font-size: 36px;
      box-shadow: 4px 4px 0 #111;
    }}
    .tap-target {{
      position: absolute;
      border: 4px dashed #ff3b30;
      background: rgba(255, 59, 48, 0.25);
      border-radius: 14px;
      padding: 8px 16px;
      font: 800 20px 'IBM Plex Mono';
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
      animation: pulseTarget 1.2s infinite alternate;
    }}
    @keyframes pulseTarget {{
      from {{ transform: scale(0.96); }}
      to {{ transform: scale(1.04); }}
    }}
    .tap-ripple {{
      width: 80px;
      height: 80px;
      border-radius: 50%;
      background: rgba(255, 210, 63, 0.7);
      border: 4px solid #111;
      position: absolute;
      animation: ripple 1s infinite;
    }}
    @keyframes ripple {{
      0% {{ transform: scale(0.3); opacity: 1; }}
      100% {{ transform: scale(1.8); opacity: 0; }}
    }}

    /* Seesaw Balance Beam */
    .see-container {{
      position: relative;
      width: 720px;
      height: 220px;
      display: grid;
      place-items: center;
    }}
    .plank {{
      position: absolute;
      top: 50px;
      width: 680px;
      height: 72px;
      background: #111;
      border-radius: 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 32px;
      animation: rockSeesaw 1.8s ease-in-out infinite alternate;
      transform-origin: 50% 100%;
      box-shadow: 8px 8px 0 rgba(0,0,0,0.3);
    }}
    @keyframes rockSeesaw {{
      from {{ rotate: -9deg; }}
      to {{ rotate: 9deg; }}
    }}
    .plank b {{
      background: #fff;
      border: 4px solid #111;
      border-radius: 14px;
      padding: 8px 24px;
      font: 900 30px 'Bricolage Grotesque';
      color: #111;
      box-shadow: 4px 4px 0 #111;
    }}
    .pivot {{
      position: absolute;
      bottom: 20px;
      border: 36px solid transparent;
      border-bottom: 72px solid #111;
      border-top: 0;
    }}

    /* Speedometer Gauge */
    .gauge-card {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 16px;
    }}

    /* Checklist Container */
    .chk {{
      width: 100%;
      max-width: 840px;
      background: #fff;
      border: 6px solid #111;
      border-radius: 24px;
      box-shadow: 10px 10px 0 #111;
      padding: 24px 36px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .ck {{
      display: flex;
      align-items: center;
      gap: 20px;
      font-weight: 800;
      font-size: 34px;
      padding: 12px 0;
      border-bottom: 3px dashed #ccc;
    }}
    .ck:last-child {{ border-bottom: none; }}
    .ck u {{
      width: 48px;
      height: 48px;
      border-radius: 14px;
      background: #22c55e;
      color: #fff;
      text-decoration: none;
      font-size: 28px;
      display: grid;
      place-items: center;
      border: 4px solid #111;
      box-shadow: 3px 3px 0 #111;
    }}

    /* Equalizer Bars */
    .bars {{
      display: flex;
      gap: 16px;
      align-items: flex-end;
      height: 140px;
      margin-top: 12px;
    }}
    .bars i {{
      width: 44px;
      height: var(--h);
      background: #fff;
      border: 5px solid #111;
      border-radius: 8px;
      box-shadow: 4px 4px 0 #111;
      transform-origin: bottom;
      animation: barAnim 0.45s infinite alternate;
    }}
    @keyframes barAnim {{
      to {{ scale: 1 0.45; }}
    }}

    /* CTA Card with Pulsing Follow & Reactions */
    .fol-btn {{
      background: #ff2d55;
      color: #fff;
      border: 6px solid #fff;
      border-radius: 999px;
      font: 900 68px 'Bricolage Grotesque';
      padding: 18px 72px;
      box-shadow: 10px 10px 0 #111;
      animation: pulseBtn 1.2s infinite;
      text-transform: uppercase;
      letter-spacing: 2px;
    }}
    @keyframes pulseBtn {{
      0% {{ box-shadow: 0 0 0 0 rgba(255, 45, 85, 0.7), 10px 10px 0 #111; }}
      100% {{ box-shadow: 0 0 0 44px transparent, 10px 10px 0 #111; }}
    }}
    .reactions-row {{
      display: flex;
      gap: 28px;
      margin-top: 14px;
    }}
    .reaction-ic {{
      width: 96px;
      height: 96px;
      border-radius: 28px;
      background: #fff;
      color: #111;
      display: grid;
      place-items: center;
      font-size: 46px;
      border: 5px solid #111;
      box-shadow: 6px 6px 0 #111;
    }}

    /* Desk & Vector Rig Host Anchor */
    #desk {{
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      height: 290px;
      background: repeating-linear-gradient(90deg, rgba(0, 0, 0, 0.14) 0 6px, transparent 6px 240px), var(--d, #b8352b);
      border-top: 8px solid #111;
      z-index: 10;
      transition: background 0.3s ease;
    }}

    /* Character Presenter Rig */
    #ch {{
      position: absolute;
      right: 48px;
      bottom: 230px;
      width: 380px;
      z-index: 12;
      animation: bnc 0.6s ease-in-out infinite alternate;
    }}
    @keyframes bnc {{
      to {{ transform: translateY(-12px); }}
    }}
    #hd {{
      transform-origin: 100px 150px;
      animation: nod 0.7s ease-in-out infinite alternate;
    }}
    @keyframes nod {{
      from {{ transform: rotate(-3deg); }}
      to {{ transform: rotate(3deg); }}
    }}
    .arm {{
      transform-origin: 52px 172px;
      animation: wave 1s ease-in-out infinite alternate;
    }}
    @keyframes wave {{
      from {{ transform: rotate(-22deg); }}
      to {{ transform: rotate(14deg); }}
    }}
    .eye {{
      transform-box: fill-box;
      transform-origin: center;
    }}
    .mouth {{
      transform-box: fill-box;
      transform-origin: center;
      transition: transform 0.05s ease;
    }}
    .brow {{
      animation: brw 1.3s infinite alternate;
    }}
    @keyframes brw {{
      to {{ transform: translateY(-6px); }}
    }}

    /* Neo-Brutalist Kinetic Caption Pill */
    #cap {{
      position: absolute;
      left: 60px;
      right: 60px;
      bottom: 70px;
      text-align: center;
      z-index: 20;
      pointer-events: none;
    }}
    #cap .cap-pill {{
      display: inline-block;
      font: 900 48px 'Bricolage Grotesque';
      background: #ffd23f;
      color: #111;
      border: 6px solid #111;
      border-radius: 20px;
      padding: 8px 36px;
      box-shadow: 8px 8px 0 #111;
      text-transform: uppercase;
      letter-spacing: 1px;
    }}
  </style>
</head>
<body>

  <!-- Audio Element -->
  <audio id="voice" src="{master_audio_path}" preload="auto"></audio>

  <div id="stage" class="rd" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{duration}">
    
    <!-- Ambient Floating Particles -->
    <div id="pt"></div>

    <div id="scene-container">
      
      <!-- Top Persistent Neo-Brutalist Header -->
      <div class="top-header">
        <div id="top-label" class="lab">MANUAL TESTING IS DEAD</div>
        <div id="top-progress" class="pr">
          <i id="dot1"></i>
          <i id="dot2"></i>
          <i id="dot3"></i>
          <span id="pr-text">0/3</span>
        </div>
      </div>

      <!-- Active Kinetic Content Area (Changes each scene) -->
      <div id="active-scene" class="sc-body">
        <!-- Injected dynamically by mountScene() -->
      </div>

    </div>

    <!-- Desk Base -->
    <div id="desk"></div>

    <!-- Character Presenter Rig (Full SVG with live lip sync & blinking) -->
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
        <g id="eyes" class="eye">
          <circle cx="82" cy="101" r="5" fill="#222"/>
          <circle cx="118" cy="101" r="5" fill="#222"/>
        </g>
        <g fill="none" stroke="#222" stroke-width="3">
          <circle cx="82" cy="101" r="15"/>
          <circle cx="118" cy="101" r="15"/>
          <path d="M97 101h6"/>
        </g>
        <path class="brow" d="M70 80q12-7 24 0M106 80q12-7 24 0" stroke="#2a1d1a" stroke-width="4" fill="none" stroke-linecap="round"/>
        <ellipse id="mouth-shape" class="mouth" cx="100" cy="130" rx="12" ry="4" fill="#7a2a2a"/>
        <circle cx="66" cy="120" r="6" fill="#f08a7a" opacity="0.5"/>
        <circle cx="134" cy="120" r="6" fill="#f08a7a" opacity="0.5"/>
      </g>
    </svg>

    <!-- Bottom Kinetic Caption Pill -->
    <div id="cap">
      <div id="cap-box" class="cap-pill" style="display: none;"></div>
    </div>

    <!-- Flash Scene Transition Wipe -->
    <div id="fl"></div>

  </div>

  <script>
    // Spawn ambient floating particles
    const pt = document.getElementById('pt');
    for (let i = 0; i < 28; i++) {{
      const p = document.createElement('i');
      p.style.cssText = `left: ${{Math.random() * 100}}%; --s: ${{6 + Math.random() * 14}}px; --t: ${{3 + Math.random() * 4}}s; --dl: -${{Math.random() * 6}}s`;
      pt.appendChild(p);
    }}

    // Lip sync mouth setter
    function setMouth(state) {{
      const el = document.getElementById('mouth-shape');
      if (!el) return;
      if (state === 'closed') {{
        el.setAttribute('rx', '12');
        el.setAttribute('ry', '3');
      }} else if (state === 'small') {{
        el.setAttribute('rx', '13');
        el.setAttribute('ry', '7');
      }} else if (state === 'open') {{
        el.setAttribute('rx', '15');
        el.setAttribute('ry', '12');
      }} else if (state === 'wide') {{
        el.setAttribute('rx', '18');
        el.setAttribute('ry', '16');
      }}
    }}

    // Kinetic Caption Setter
    function setWord(txt) {{
      const box = document.getElementById('cap-box');
      if (!box) return;
      if (!txt || txt.trim() === '') {{
        box.style.display = 'none';
      }} else {{
        box.textContent = txt.toUpperCase();
        box.style.display = 'inline-block';
      }}
    }}

    // Flash Wipe Trigger
    function triggerFlash() {{
      const f = document.getElementById('fl');
      if (!f) return;
      f.style.animation = 'none';
      void f.offsetWidth;
      f.style.animation = 'flashWipe 0.35s ease-out forwards';
    }}

    // Update Progress Dots
    function updateProgress(num) {{
      const pText = document.getElementById('pr-text');
      const d1 = document.getElementById('dot1');
      const d2 = document.getElementById('dot2');
      const d3 = document.getElementById('dot3');
      pText.textContent = num;
      d1.className = (num >= '1/3' && num !== '0/3') ? 'on' : '';
      d2.className = (num >= '2/3') ? 'on' : '';
      d3.className = (num === '3/3') ? 'on' : '';
    }}

    // Scene Definitions (Rich neo-brutalist graphics, NO empty space!)
    const scenesContent = [
      // 0: HOOK - Manual Testing Dead + USB AI Agent
      `
      <div class="big-title">STOP TESTING APPS MANUALLY</div>
      <div class="sub-stamp">⚡ USB AI AGENT IS HERE</div>
      <div class="card" style="display: flex; gap: 32px; align-items: center; justify-content: space-around;">
        <div style="text-align: center;">
          <div style="font-size: 80px;">📱</div>
          <div style="font: 800 28px 'IBM Plex Mono';">Physical iPhone</div>
        </div>
        <div style="font: 900 64px 'Bricolage Grotesque'; color: #ff3b30;">⚡ USB-C ⚡</div>
        <div style="text-align: center;">
          <div style="font-size: 80px;">🤖</div>
          <div style="font: 800 28px 'IBM Plex Mono';">Local AI Agent</div>
        </div>
      </div>
      `,

      // 1: PROBLEM - Cloud Bots Cant Touch Real iOS
      `
      <div class="big-title">THE CLOUD BOT BOTTLENECK</div>
      <div class="see-container">
        <div class="plank">
          <b>☁️ CLOUD BOTS (WEB ONLY)</b>
          <b>🔒 REAL iOS HARDWARE</b>
        </div>
        <div class="pivot"></div>
      </div>
      <div class="card" style="background: #111; color: #fff;">
        <div style="font: 800 32px 'IBM Plex Mono'; color: #ff5f57;">❌ Zero Access to Native iOS Gestures</div>
        <div style="font: 800 32px 'IBM Plex Mono'; color: #ff5f57; margin-top: 12px;">❌ Blocked by Apple Security & Sandbox</div>
      </div>
      `,

      // 2: REVEAL - iPhone Use (GitHub Repo)
      `
      <div class="big-title">MEET iPHONE-USE</div>
      <div class="win">
        <div class="hd"><i></i><i></i><i></i>github.com/zhongerxin/iPhone-use</div>
        <div class="bd">
          <div><span class="c">repo:</span> zhongerxin / <span class="y">iPhone-use</span></div>
          <div style="margin-top: 14px;"><span class="g">★ 3,000+ GitHub Stars</span> (Trending Worldwide)</div>
          <div style="margin-top: 14px; color: #aaa;">Autonomous mobile agent control via native USB protocol</div>
        </div>
      </div>
      <div class="sub-stamp" style="background: #22c55e; color: #fff; rotate: 3deg;">★ 100% OPEN SOURCE</div>
      `,

      // 3: STEP 1 - USB Connection + Zero Jailbreak
      `
      <div class="big-title">01 · PLUG & PLAY VIA USB</div>
      <div class="chk">
        <div class="ck"><u>✔</u> Connect Mac & iPhone via USB-C or Lightning</div>
        <div class="ck"><u>✔</u> Pure Native Debugging Protocol</div>
        <div class="ck"><u>✔</u> Zero Jailbreak Required (100% Stock iOS)</div>
      </div>
      <div class="sub-stamp" style="background: #6f9ee8; color: #fff;">STOCK iOS COMPLIANT</div>
      `,

      // 4: STEP 2 - Vision Grounding & Live Tapping
      `
      <div class="big-title">02 · REAL-TIME VISION GROUNDING</div>
      <div class="card" style="display: flex; gap: 36px; align-items: center; justify-content: center;">
        <div class="phone-mock">
          <div class="phone-notch"></div>
          <div class="screen-grid">
            <div class="app-row">
              <div class="app-icon">💬</div>
              <div class="app-icon">📷</div>
              <div class="app-icon">🗺️</div>
            </div>
            <div class="tap-target" style="top: 180px; left: 30px;">
              <span>🎯 [TAP: Confirm Order]</span>
              <div class="tap-ripple"></div>
            </div>
            <div class="tap-target" style="bottom: 90px; right: 20px; border-color: #ffd23f;">
              <span>👆 [SWIPE UP: Feed]</span>
            </div>
          </div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 20px;">
          <div class="sub-stamp" style="rotate: 0deg;">DETECTS EVERY BUTTON</div>
          <div class="sub-stamp" style="rotate: 0deg; background: #22c55e; color: #fff;">AUTONOMOUS SWIPES</div>
          <div class="sub-stamp" style="rotate: 0deg; background: #6f9ee8; color: #fff;">LIVE OCR GROUNDING</div>
        </div>
      </div>
      `,

      // 5: STEP 3 - Local LLM vs Frontier Claude/GPT
      `
      <div class="big-title">03 · LOCAL & CLOUD LLMs</div>
      <div class="card" style="display: flex; gap: 32px; justify-content: space-around;">
        <div style="text-align: center; border-right: 4px dashed #ccc; padding-right: 32px;">
          <div style="font: 900 48px 'Bricolage Grotesque'; color: #22c55e;">100% OFFLINE</div>
          <div style="font: 700 28px 'IBM Plex Mono'; margin-top: 14px;">Ollama & Local Vision Models</div>
          <div style="margin-top: 10px; font-size: 24px; color: #666;">$0 Cost · Total Privacy</div>
        </div>
        <div style="text-align: center;">
          <div style="font: 900 48px 'Bricolage Grotesque'; color: #6f9ee8;">FRONTIER APIS</div>
          <div style="font: 700 28px 'IBM Plex Mono'; margin-top: 14px;">Claude 3.7 & GPT-4o</div>
          <div style="margin-top: 10px; font-size: 24px; color: #666;">Complex Multi-Step Logic</div>
        </div>
      </div>
      <div class="bars">
        <i style="--h: 120px; animation-delay: -0.1s;"></i>
        <i style="--h: 80px; animation-delay: -0.3s;"></i>
        <i style="--h: 140px; animation-delay: -0.2s;"></i>
        <i style="--h: 95px; animation-delay: -0.4s;"></i>
        <i style="--h: 130px; animation-delay: -0.15s;"></i>
        <i style="--h: 70px; animation-delay: -0.35s;"></i>
      </div>
      `,

      // 6: SETUP - Two Terminal Commands
      `
      <div class="big-title">SETUP IN 60 SECONDS</div>
      <div class="win">
        <div class="hd"><i></i><i></i><i></i>Terminal — zsh</div>
        <div class="bd">
          <div><span class="y">$</span> pip install iphone-use</div>
          <div style="margin-top: 18px;"><span class="y">$</span> iphone-use --device usb --model ollama/vision</div>
          <div style="margin-top: 18px;" class="g">✔ iPhone 16 Pro Connected (USB-C)</div>
          <div style="margin-top: 10px;" class="g">✔ Vision Agent Active & Ready</div>
        </div>
      </div>
      <div class="sub-stamp" style="background: #22c55e; color: #fff;">ONE-LINE EXECUTION</div>
      `,

      // 7: CTA - Comment IPHONE
      `
      <div class="big-title">GET THE SETUP CODE</div>
      <div class="fol-btn">COMMENT "IPHONE"</div>
      <div class="card" style="text-align: center; max-width: 720px; background: #ffd23f;">
        <div style="font: 900 36px 'Bricolage Grotesque';">📩 I will DM you the direct repo link + setup guide</div>
      </div>
      <div class="reactions-row">
        <div class="reaction-ic">♥</div>
        <div class="reaction-ic">🔖</div>
        <div class="reaction-ic">↗</div>
      </div>
      `
    ];

    const sceneThemes = ["rd", "yl", "bl", "gr", "pk", "yl", "dk", "rd"];
    const sceneLabels = [
      "MANUAL TESTING IS DEAD",
      "THE BOTTLENECK",
      "GITHUB REVEAL",
      "01 · DIRECT HARDWARE",
      "02 · VISION GROUNDING",
      "03 · LOCAL INFERENCE",
      "TERMINAL INSTALL",
      "DM AUTOMATION"
    ];
    const sceneProgress = ["0/3", "0/3", "0/3", "1/3", "2/3", "3/3", "3/3", "3/3"];

    function mountScene(idx) {{
      const stage = document.getElementById('stage');
      const activeArea = document.getElementById('active-scene');
      const label = document.getElementById('top-label');

      stage.className = sceneThemes[idx] || 'rd';
      label.textContent = sceneLabels[idx] || '';
      updateProgress(sceneProgress[idx] || '0/3');
      activeArea.innerHTML = scenesContent[idx] || '';
      triggerFlash();
    }}

    // Setup Master GSAP Timeline for HyperFrames deterministic rendering
    const tl = gsap.timeline({{ paused: true }});

    // Mount initial scene
    mountScene(0);

    // Register all scene calls
    {chr(10).join("    " + sc for sc in scene_calls)}

    // Register all lip-sync mouth calls
    {chr(10).join("    " + mc for mc in mouth_calls)}

    // Register all word caption calls
    {chr(10).join("    " + cc for cc in caption_calls)}

    // Auto eye blinking
    for (let t = 0; t < {duration}; t += 2.8) {{
      tl.call(() => {{
        const eyes = document.getElementById('eyes');
        if (eyes) eyes.style.transform = 'scale(1, 0.1)';
      }}, null, t);
      tl.call(() => {{
        const eyes = document.getElementById('eyes');
        if (eyes) eyes.style.transform = 'scale(1, 1)';
      }}, null, t + 0.12);
    }}

    // Expose timeline to HyperFrames
    window.__timelines = window.__timelines || {{}};
    window.__timelines["main"] = tl;
  </script>
</body>
</html>
"""

    with open("index.html", "w") as f:
        f.write(html_content)

    print("[✓] index.html successfully compiled with upgraded Claude-style engine!")

if __name__ == "__main__":
    main()
