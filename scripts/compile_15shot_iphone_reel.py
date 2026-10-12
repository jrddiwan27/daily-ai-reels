import os
import json
import subprocess

def main():
    duration = 49.85
    voice_path = "assets/voice_iphone.mp3"
    master_audio_path = "assets/master_audio_iphone.mp3"
    mouth_data = json.load(open("assets/mouth_iphone.json"))
    caption_chunks = json.load(open("assets/caption_chunks_iphone.json"))

    # 15 distinct shots with exact timestamps
    shots = [
        {"id": 0, "start": 0.00, "end": 2.30, "theme": "rd", "label": "MANUAL TESTING IS DEAD", "pr": "0/3"},
        {"id": 1, "start": 2.30, "end": 4.80, "theme": "dk", "label": "AUTONOMOUS AGENT", "pr": "0/3"},
        {"id": 2, "start": 4.80, "end": 7.59, "theme": "bl", "label": "DIRECT USB PROTOCOL", "pr": "0/3"},
        {"id": 3, "start": 7.59, "end": 10.00, "theme": "yl", "label": "THE CLOUD BOT BOTTLENECK", "pr": "0/3"},
        {"id": 4, "start": 10.00, "end": 14.10, "theme": "rd", "label": "iOS SECURITY SANDBOX", "pr": "0/3"},
        {"id": 5, "start": 14.10, "end": 16.50, "theme": "bl", "label": "GITHUB REVEAL", "pr": "0/3"},
        {"id": 6, "start": 16.50, "end": 19.44, "theme": "gr", "label": "3,000+ STARS TRENDING", "pr": "0/3"},
        {"id": 7, "start": 19.44, "end": 22.90, "theme": "gr", "label": "01 · DIRECT HARDWARE", "pr": "1/3"},
        {"id": 8, "start": 22.90, "end": 24.52, "theme": "yl", "label": "ZERO JAILBREAK NEEDED", "pr": "1/3"},
        {"id": 9, "start": 24.52, "end": 27.80, "theme": "pk", "label": "02 · REAL-TIME VISION", "pr": "2/3"},
        {"id": 10, "start": 27.80, "end": 31.42, "theme": "bl", "label": "NATIVE GESTURE GROUNDING", "pr": "2/3"},
        {"id": 11, "start": 31.42, "end": 35.00, "theme": "gr", "label": "03 · 100% OFFLINE OLLAMA", "pr": "3/3"},
        {"id": 12, "start": 35.00, "end": 38.90, "theme": "yl", "label": "FRONTIER LLM CLOUD", "pr": "3/3"},
        {"id": 13, "start": 38.90, "end": 44.25, "theme": "dk", "label": "ONE-LINE TERMINAL SETUP", "pr": "3/3"},
        {"id": 14, "start": 44.25, "end": duration, "theme": "rd", "label": "DM AUTOMATION", "pr": "3/3"}
    ]

    # Build mouth calls
    mouth_calls = []
    last_m = None
    for item in mouth_data:
        m = item.get("mouth", "closed")
        f = item.get("f", 0)
        t = round(f / 30.0, 3)
        if m != last_m and t <= duration:
            mouth_calls.append(f'tl.call(() => setMouth("{m}"), null, {t});')
            last_m = m

    # Build shot transition calls
    shot_calls = []
    for s in shots:
        shot_calls.append(f'tl.call(() => mountShot({s["id"]}), null, {s["start"]});')

    # Build caption calls
    caption_calls = []
    for c in caption_chunks:
        caption_calls.append(f'tl.call(() => setWord({json.dumps(c["text"])}), null, {c["start"]});')
    caption_calls.append(f'tl.call(() => setWord(""), null, {duration - 0.2});')

    # Shots HTML content templates
    shots_html = [
        # Shot 0: Stop testing apps manually (Finger tapping with red hazard stamp & animated strike)
        """
        <div class="big-title">STOP TESTING APPS MANUALLY</div>
        <div class="sub-stamp" style="background:#ff3b30; color:#fff; animation: stampPop 0.4s cubic-bezier(0.3,1.7,0.5,1) forwards;">⚠️ MANUAL TAP BOTTLENECK</div>
        <div class="card" style="display:flex; flex-direction:column; align-items:center; gap:24px; position:relative;">
          <div style="display:flex; gap:36px; align-items:center;">
            <div style="font-size:110px; animation: jitterBug 0.15s infinite alternate;">🐛</div>
            <div style="font-size:120px; animation: tapFinger 0.35s infinite alternate;">👆</div>
            <div style="font-size:110px; animation: jitterBug 0.2s infinite alternate;">🐛</div>
          </div>
          <div class="strike-bar"></div>
          <div style="font:800 32px 'IBM Plex Mono'; color:#ff3b30; text-align:center;">SLUGGY · ERROR-PRONE · REPETITIVE</div>
        </div>
        """,

        # Shot 1: AI Agent robot head drops in with shockwave
        """
        <div class="big-title">AN OPEN-SOURCE AI AGENT</div>
        <div class="sub-stamp" style="background:#22c55e; color:#fff;">🤖 AUTONOMOUS EXECUTOR</div>
        <div class="card" style="background:#14121a; color:#fff; display:flex; flex-direction:column; align-items:center; gap:28px; position:relative;">
          <div class="shockwave-ring"></div>
          <div style="font-size:130px; animation: bobbing 1.2s infinite alternate;">🦾</div>
          <div style="font:800 36px 'IBM Plex Mono'; color:#38bdf8;">{ agent.execute(device="iPhone") }</div>
          <div style="display:flex; gap:16px;">
            <span class="sub-stamp" style="font-size:24px; padding:6px 16px;">AUTONOMOUS DECISIONS</span>
            <span class="sub-stamp" style="font-size:24px; padding:6px 16px; background:#6f9ee8; color:#fff;">ZERO HUMAN DELAY</span>
          </div>
        </div>
        """,

        # Shot 2: MacBook <-> iPhone over USB with electric lightning
        """
        <div class="big-title">CONTROLS PHYSICAL iPHONE</div>
        <div class="sub-stamp" style="background:#ffd23f; color:#111;">⚡ NATIVE USB-C PROTOCOL</div>
        <div class="card" style="display:flex; justify-content:space-around; align-items:center; position:relative; overflow:hidden;">
          <div style="text-align:center;">
            <div style="font-size:100px;">💻</div>
            <div style="font:800 28px 'IBM Plex Mono'; margin-top:8px;">MacBook Pro</div>
          </div>
          <div class="lightning-flow">
            <div class="lightning-bolt">⚡⚡⚡</div>
            <div style="font:900 32px 'IBM Plex Mono'; color:#ff3b30;">USB CABLE</div>
          </div>
          <div style="text-align:center;">
            <div style="font-size:100px; animation: phoneGlow 1s infinite alternate;">📱</div>
            <div style="font:800 28px 'IBM Plex Mono'; margin-top:8px;">Physical iPhone</div>
          </div>
        </div>
        """,

        # Shot 3: Cloud bots web-only boundary
        """
        <div class="big-title">CLOUD BOTS ARE TRAPPED</div>
        <div class="sub-stamp" style="background:#ff3b30; color:#fff;">WEB BROWSERS ONLY</div>
        <div class="card" style="background:#1e293b; color:#fff; display:flex; flex-direction:column; align-items:center; gap:24px;">
          <div class="trapped-cage">
            <div style="font-size:90px;">☁️</div>
            <div style="font:800 30px 'IBM Plex Mono'; color:#ef4444; margin-top:12px;">❌ CANNOT ACCESS MOBILE OS</div>
          </div>
          <div style="font:700 28px 'IBM Plex Mono'; color:#94a3b8; text-align:center;">Selenium & Puppeteer can't touch native mobile hardware</div>
        </div>
        """,

        # Shot 4: Seesaw balance between cloud and locked iOS
        """
        <div class="big-title">iOS SECURITY BARRIER</div>
        <div class="see-container">
          <div class="plank">
            <b>☁️ CLOUD BOTS (BLOCKED)</b>
            <b>🔒 NATIVE iOS SANDBOX</b>
          </div>
          <div class="pivot"></div>
        </div>
        <div class="card" style="background:#111; color:#fff; padding:24px 36px;">
          <div style="font:800 30px 'IBM Plex Mono'; color:#ff5f57;">❌ Sandbox blocks remote cloud connections</div>
          <div style="font:800 30px 'IBM Plex Mono'; color:#22c55e; margin-top:10px;">✔ Only physical USB debuggers can enter</div>
        </div>
        """,

        # Shot 5: Meet iPhone Use repo reveal
        """
        <div class="big-title">MEET iPHONE-USE</div>
        <div class="win">
          <div class="hd"><i></i><i></i><i></i>github.com/zhongerxin/iPhone-use</div>
          <div class="bd">
            <div><span class="c">repo:</span> zhongerxin / <span class="y">iPhone-use</span></div>
            <div style="margin-top:14px;"><span class="g">★ 3,000+ GitHub Stars</span> (Trending Worldwide)</div>
            <div style="margin-top:14px; color:#aaa;">Autonomous mobile agent control via native USB protocol</div>
          </div>
        </div>
        <div class="sub-stamp" style="background:#22c55e; color:#fff; rotate:3deg;">★ 100% OPEN SOURCE</div>
        """,

        # Shot 6: Live repo stats & commits
        """
        <div class="big-title">GLOBAL #1 TRENDING REPO</div>
        <div class="card" style="display:flex; justify-content:space-around; align-items:center;">
          <div style="text-align:center;">
            <div style="font:900 84px 'Bricolage Grotesque'; color:#2563eb;">3,000+</div>
            <div style="font:800 28px 'IBM Plex Mono';">GITHUB STARS</div>
          </div>
          <div style="height:120px; width:4px; background:#ddd;"></div>
          <div style="text-align:center;">
            <div style="font:900 84px 'Bricolage Grotesque'; color:#16a34a;">0 ms</div>
            <div style="font:800 28px 'IBM Plex Mono';">CLOUD LATENCY</div>
          </div>
        </div>
        <div class="sub-stamp" style="background:#f6c85a; color:#111;">★ ZERO MONTHLY FEES</div>
        """,

        # Shot 7: Step 1 - Plug iPhone into Mac via USB
        """
        <div class="big-title">01 · PLUG & PLAY VIA USB</div>
        <div class="chk">
          <div class="ck"><u>✔</u> Connect Mac & iPhone via USB-C or Lightning</div>
          <div class="ck"><u>✔</u> Pure Native Debugging Protocol</div>
          <div class="ck"><u>✔</u> Instant Device Handshake in Terminal</div>
        </div>
        <div class="sub-stamp" style="background:#6f9ee8; color:#fff;">PLUG AND PLAY</div>
        """,

        # Shot 8: Zero jailbreak needed
        """
        <div class="big-title">ZERO JAILBREAK NEEDED</div>
        <div class="card" style="display:flex; flex-direction:column; align-items:center; gap:20px; background:#0f172a; color:#fff;">
          <div style="display:flex; gap:32px; align-items:center;">
            <div style="font-size:100px;">🛡️</div>
            <div style="font-size:90px; color:#22c55e;">✔</div>
            <div style="font-size:100px;">🔓</div>
          </div>
          <div style="font:900 42px 'Bricolage Grotesque'; color:#22c55e;">100% STOCK iOS COMPLIANT</div>
          <div style="font:600 28px 'IBM Plex Mono'; color:#94a3b8;">No root access, no warranty void, no custom ROMs</div>
        </div>
        """,

        # Shot 9: Step 2 - Real-time vision screen capture & bounding boxes
        """
        <div class="big-title">02 · REAL-TIME VISION GROUNDING</div>
        <div class="card" style="display:flex; gap:36px; align-items:center; justify-content:center;">
          <div class="phone-mock">
            <div class="phone-notch"></div>
            <div class="screen-grid">
              <div class="laser-scanner"></div>
              <div class="app-row">
                <div class="app-icon">💬</div>
                <div class="app-icon">📷</div>
                <div class="app-icon">🗺️</div>
              </div>
              <div class="tap-target" style="top:180px; left:30px;">
                <span>🎯 [TAP: Confirm Order]</span>
              </div>
              <div class="tap-target" style="bottom:90px; right:20px; border-color:#ffd23f;">
                <span>👆 [SWIPE UP: Feed]</span>
              </div>
            </div>
          </div>
          <div style="display:flex; flex-direction:column; gap:20px;">
            <div class="sub-stamp" style="rotate:0deg;">DETECTS EVERY BUTTON</div>
            <div class="sub-stamp" style="rotate:0deg; background:#22c55e; color:#fff;">AUTONOMOUS SWIPES</div>
            <div class="sub-stamp" style="rotate:0deg; background:#6f9ee8; color:#fff;">LIVE OCR GROUNDING</div>
          </div>
        </div>
        """,

        # Shot 10: Tapping and Swiping in real time
        """
        <div class="big-title">TAPS & SWIPES IN REAL TIME</div>
        <div class="card" style="display:flex; flex-direction:column; align-items:center; gap:24px;">
          <div style="display:flex; gap:40px; align-items:center;">
            <div class="action-bubble">
              <div style="font-size:72px;">👆</div>
              <div style="font:800 26px 'IBM Plex Mono';">TAP BUTTON</div>
            </div>
            <div class="action-bubble" style="border-color:#22c55e;">
              <div style="font-size:72px;">📜</div>
              <div style="font:800 26px 'IBM Plex Mono';">SCROLL FEED</div>
            </div>
            <div class="action-bubble" style="border-color:#6f9ee8;">
              <div style="font-size:72px;">⌨️</div>
              <div style="font:800 26px 'IBM Plex Mono';">TYPE TEXT</div>
            </div>
          </div>
          <div style="font:800 32px 'IBM Plex Mono'; color:#111;">SUB-100ms INTERACTION SPEED</div>
        </div>
        """,

        # Shot 11: Step 3 - Offline Local Models (Ollama)
        """
        <div class="big-title">03 · 100% OFFLINE LOCAL AI</div>
        <div class="card" style="display:flex; flex-direction:column; align-items:center; gap:24px; background:#0f172a; color:#fff;">
          <div style="display:flex; justify-content:space-around; width:100%; align-items:center;">
            <div>
              <div style="font:900 48px 'Bricolage Grotesque'; color:#22c55e;">OLLAMA + LOCAL VISION</div>
              <div style="font:600 26px 'IBM Plex Mono'; color:#94a3b8; margin-top:8px;">Zero internet required · 100% Private</div>
            </div>
            <div class="sub-stamp" style="background:#22c55e; color:#fff;">$0 FEES</div>
          </div>
          <div class="bars">
            <i style="--h: 120px; animation-delay: -0.1s;"></i>
            <i style="--h: 80px; animation-delay: -0.3s;"></i>
            <i style="--h: 140px; animation-delay: -0.2s;"></i>
            <i style="--h: 95px; animation-delay: -0.4s;"></i>
            <i style="--h: 130px; animation-delay: -0.15s;"></i>
            <i style="--h: 70px; animation-delay: -0.35s;"></i>
          </div>
        </div>
        """,

        # Shot 12: Frontier Cloud LLMs (Claude 3.7 / GPT-4o) with Speedometer
        """
        <div class="big-title">OR CONNECT FRONTIER LLMs</div>
        <div class="card" style="display:flex; justify-content:space-around; align-items:center;">
          <div style="text-align:center;">
            <div style="font:900 44px 'Bricolage Grotesque'; color:#d9694a;">CLAUDE 3.7 SONNET</div>
            <div style="font:700 26px 'IBM Plex Mono'; margin-top:10px;">Deep Cognitive Reasoning</div>
          </div>
          <div class="gauge-box">
            <div class="gauge-needle"></div>
            <div style="position:absolute; bottom:12px; font:900 22px 'IBM Plex Mono';">MAX SPEED</div>
          </div>
          <div style="text-align:center;">
            <div style="font:900 44px 'Bricolage Grotesque'; color:#2563eb;">GPT-4o MULTIMODAL</div>
            <div style="font:700 26px 'IBM Plex Mono'; margin-top:10px;">Zero Hallucination Vision</div>
          </div>
        </div>
        """,

        # Shot 13: Terminal setup in 60s
        """
        <div class="big-title">SETUP IN 60 SECONDS</div>
        <div class="win">
          <div class="hd"><i></i><i></i><i></i>Terminal — zsh</div>
          <div class="bd">
            <div><span class="y">$</span> pip install iphone-use</div>
            <div style="margin-top:18px;"><span class="y">$</span> iphone-use --device usb --model ollama/vision</div>
            <div style="margin-top:18px;" class="g">✔ iPhone 16 Pro Connected (USB-C)</div>
            <div style="margin-top:10px;" class="g">✔ Vision Agent Active & Ready</div>
          </div>
        </div>
        <div class="sub-stamp" style="background:#22c55e; color:#fff;">ONE-LINE EXECUTION</div>
        """,

        # Shot 14: CTA Comment IPHONE
        """
        <div class="big-title">GET THE SETUP CODE</div>
        <div class="fol-btn">COMMENT "IPHONE"</div>
        <div class="card" style="text-align:center; max-width:760px; background:#ffd23f;">
          <div style="font:900 36px 'Bricolage Grotesque';">📩 I will DM you the direct repo link + setup guide right now</div>
        </div>
        <div class="reactions-row">
          <div class="reaction-ic">♥</div>
          <div class="reaction-ic">🔖</div>
          <div class="reaction-ic">↗</div>
        </div>
        """
    ]

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
      top: 160px;
      left: 48px;
      right: 48px;
      bottom: 290px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 28px;
      z-index: 5;
    }}

    .card {{
      background: #fff;
      border: 6px solid #111;
      border-radius: 28px;
      box-shadow: 12px 12px 0 #111;
      padding: 36px 44px;
      width: 100%;
      max-width: 980px;
    }}

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
      font: 800 36px 'Bricolage Grotesque';
      background: #ffd23f;
      color: #111;
      border: 5px solid #111;
      padding: 10px 28px;
      border-radius: 16px;
      box-shadow: 6px 6px 0 #111;
      rotate: -4deg;
    }}

    /* Micro-Animations */
    @keyframes jitterBug {{
      from {{ transform: translate(-4px, -4px) rotate(-6deg); }}
      to {{ transform: translate(4px, 4px) rotate(6deg); }}
    }}
    @keyframes tapFinger {{
      from {{ transform: translateY(0); }}
      to {{ transform: translateY(24px) scale(0.92); }}
    }}
    @keyframes bobbing {{
      from {{ transform: translateY(-8px); }}
      to {{ transform: translateY(8px); }}
    }}
    @keyframes phoneGlow {{
      from {{ transform: scale(0.96); filter: drop-shadow(0 0 10px #38bdf8); }}
      to {{ transform: scale(1.04); filter: drop-shadow(0 0 35px #38bdf8); }}
    }}

    .strike-bar {{
      position: absolute;
      top: 50%;
      left: 10%;
      right: 10%;
      height: 12px;
      background: #ff3b30;
      border-radius: 8px;
      rotate: -8deg;
      animation: strikeWipe 0.4s ease-out forwards;
    }}
    @keyframes strikeWipe {{
      from {{ transform: scaleX(0); }}
      to {{ transform: scaleX(1); }}
    }}

    .shockwave-ring {{
      position: absolute;
      width: 240px;
      height: 240px;
      border-radius: 50%;
      border: 6px solid #38bdf8;
      animation: shockwave 1.4s infinite;
      pointer-events: none;
    }}
    @keyframes shockwave {{
      0% {{ transform: scale(0.4); opacity: 1; }}
      100% {{ transform: scale(2.2); opacity: 0; }}
    }}

    .lightning-flow {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
      animation: pulseLightning 0.3s infinite alternate;
    }}
    @keyframes pulseLightning {{
      from {{ opacity: 0.7; transform: scale(0.96); }}
      to {{ opacity: 1; transform: scale(1.04); }}
    }}
    .lightning-bolt {{
      font-size: 56px;
      color: #ffd23f;
      text-shadow: 0 0 20px #ffd23f;
    }}

    .trapped-cage {{
      border: 6px dashed #ef4444;
      border-radius: 24px;
      padding: 24px 48px;
      text-align: center;
      animation: cageJiggle 0.6s infinite alternate;
    }}
    @keyframes cageJiggle {{
      from {{ transform: rotate(-2deg); }}
      to {{ transform: rotate(2deg); }}
    }}

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

    .phone-mock {{
      width: 440px;
      height: 700px;
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
      overflow: hidden;
    }}
    .laser-scanner {{
      position: absolute;
      left: 0;
      right: 0;
      height: 8px;
      background: #ff3b30;
      box-shadow: 0 0 20px #ff3b30;
      animation: scanLaser 1.5s infinite linear;
      z-index: 10;
    }}
    @keyframes scanLaser {{
      0% {{ top: 0%; }}
      100% {{ top: 100%; }}
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

    .action-bubble {{
      border: 5px solid #111;
      background: #fff;
      border-radius: 24px;
      padding: 24px 32px;
      text-align: center;
      box-shadow: 6px 6px 0 #111;
      animation: bobbing 1s infinite alternate;
    }}

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

    .bars {{
      display: flex;
      gap: 16px;
      align-items: flex-end;
      height: 120px;
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

    .gauge-box {{
      position: relative;
      width: 180px;
      height: 100px;
      border: 6px solid #111;
      border-bottom: 0;
      border-radius: 180px 180px 0 0;
      background: #f6c85a;
      display: flex;
      justify-content: center;
    }}
    .gauge-needle {{
      position: absolute;
      bottom: 0;
      width: 8px;
      height: 70px;
      background: #111;
      border-radius: 4px;
      transform-origin: bottom center;
      animation: sweepNeedle 1.2s infinite alternate ease-in-out;
    }}
    @keyframes sweepNeedle {{
      from {{ transform: rotate(-65deg); }}
      to {{ transform: rotate(65deg); }}
    }}

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

    #desk {{
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      height: 290px;
      background: repeating-linear-gradient(90deg, rgba(0, 0, 0, 0.14) 0 6px, transparent 6px 240px), var(--d, #b8352b);
      border-top: 8px solid #111;
      z-index: 10;
      transition: background 0.25s ease;
    }}

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

  <audio id="voice" src="{master_audio_path}" preload="auto"></audio>

  <div id="stage" class="rd" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{duration}">
    
    <div id="pt"></div>

    <div id="scene-container">
      
      <div class="top-header">
        <div id="top-label" class="lab">MANUAL TESTING IS DEAD</div>
        <div id="top-progress" class="pr">
          <i id="dot1"></i>
          <i id="dot2"></i>
          <i id="dot3"></i>
          <span id="pr-text">0/3</span>
        </div>
      </div>

      <div id="active-scene" class="sc-body"></div>

    </div>

    <div id="desk"></div>

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

    <div id="cap">
      <div id="cap-box" class="cap-pill" style="display: none;"></div>
    </div>

    <div id="fl"></div>

  </div>

  <script>
    const pt = document.getElementById('pt');
    for (let i = 0; i < 28; i++) {{
      const p = document.createElement('i');
      p.style.cssText = `left: ${{Math.random() * 100}}%; --s: ${{6 + Math.random() * 14}}px; --t: ${{3 + Math.random() * 4}}s; --dl: -${{Math.random() * 6}}s`;
      pt.appendChild(p);
    }}

    function setMouth(state) {{
      const el = document.getElementById('mouth-shape');
      if (!el) return;
      if (state === 'closed') {{
        el.setAttribute('rx', '12'); el.setAttribute('ry', '3');
      }} else if (state === 'small') {{
        el.setAttribute('rx', '13'); el.setAttribute('ry', '7');
      }} else if (state === 'open') {{
        el.setAttribute('rx', '15'); el.setAttribute('ry', '12');
      }} else if (state === 'wide') {{
        el.setAttribute('rx', '18'); el.setAttribute('ry', '16');
      }}
    }}

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

    function triggerFlash() {{
      const f = document.getElementById('fl');
      if (!f) return;
      f.style.animation = 'none';
      void f.offsetWidth;
      f.style.animation = 'flashWipe 0.35s ease-out forwards';
    }}

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

    const shotsHtml = {json.dumps(shots_html)};
    const shotThemes = {json.dumps([s["theme"] for s in shots])};
    const shotLabels = {json.dumps([s["label"] for s in shots])};
    const shotProgress = {json.dumps([s["pr"] for s in shots])};

    function mountShot(idx) {{
      const stage = document.getElementById('stage');
      const activeArea = document.getElementById('active-scene');
      const label = document.getElementById('top-label');

      stage.className = shotThemes[idx] || 'rd';
      label.textContent = shotLabels[idx] || '';
      updateProgress(shotProgress[idx] || '0/3');
      activeArea.innerHTML = shotsHtml[idx] || '';
      triggerFlash();
    }}

    const tl = gsap.timeline({{ paused: true }});
    mountShot(0);

    // Register all shot calls
    {chr(10).join("    " + sc for sc in shot_calls)}

    // Register all lip-sync mouth calls
    {chr(10).join("    " + mc for mc in mouth_calls)}

    // Register all word caption calls
    {chr(10).join("    " + cc for cc in caption_calls)}

    // Eye blinking
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

    window.__timelines = window.__timelines || {{}};
    window.__timelines["main"] = tl;
  </script>
</body>
</html>
"""

    with open("index.html", "w") as f:
        f.write(html_content)

    print("[✓] index.html successfully compiled with 15 dynamic micro-shots!")

if __name__ == "__main__":
    main()
