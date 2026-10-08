import json
import os

def build_hyperframes_composition(
    repos_file="assets/curated_repos.json",
    captions_file="assets/caption_chunks.json",
    audio_path="assets/voice.mp3",
    script_file="assets/generated_script.json",
    duration=38.0,
    output_html="index.html"
):
    """
    Builds a high-retention, hyper-motion graphics video composition with zero static frames,
    featuring real scraped UI screenshots, 3D perspective camera motion, laser scanlines,
    and exact word-level synchronized kinetic typography.
    """
    with open(repos_file) as f:
        repos = json.load(f)[:3]
        
    with open(captions_file) as f:
        caption_chunks = json.load(f)

    # Load structured script timestamps if available
    script_data = {}
    if os.path.exists(script_file):
        try:
            with open(script_file) as f:
                script_data = json.load(f)
        except Exception:
            pass

    # Calculate dynamic scene timings based on total audio duration
    t_hook_end = min(3.8, duration * 0.10)
    t_tool1_end = duration * 0.38
    t_tool2_end = duration * 0.66
    t_tool3_end = duration * 0.88
    t_cta_end = duration

    # Real media assets for each repo
    repo_media = []
    for r in repos:
        img = r.get("demo_media") or r.get("og_image") or "assets/repos/default_banner.png"
        repo_media.append({
            "name": r["name"].split("/")[-1].upper(),
            "owner": r.get("owner", "open-source"),
            "img": img,
            "stars": f"★ {r.get('stars', 12000):,}",
            "lang": r.get("language", "AI").upper(),
            "desc": r.get("description", "")[:80]
        })

    # Update hyperframes.json duration to match audio exactly
    hf_config = {
        "name": "daily-automation-engine",
        "version": "2.0.0",
        "fps": 30,
        "width": 720,
        "height": 1280,
        "duration": round(duration, 2)
    }
    with open("hyperframes.json", "w") as f:
        json.dump(hf_config, f, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=720, height=1280">
  <title>Hyper-Motion AI Developer Reel</title>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{
      width: 720px;
      height: 1280px;
      overflow: hidden;
      background: #080C15;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;
      user-select: none;
      color: #FFFFFF;
    }}
    #root {{
      position: relative;
      width: 720px;
      height: 1280px;
      overflow: hidden;
      background: radial-gradient(circle at 50% 30%, #151D33 0%, #080C15 80%);
    }}

    /* Continuous animated cyber grid & particle drift */
    .grid-bg {{
      position: absolute;
      inset: -200px;
      background-image: 
        linear-gradient(rgba(0, 240, 255, 0.08) 1.5px, transparent 1.5px),
        linear-gradient(90deg, rgba(0, 240, 255, 0.08) 1.5px, transparent 1.5px);
      background-size: 48px 48px;
      transform: perspective(600px) rotateX(45deg);
      animation: gridDrift 20s linear infinite;
      z-index: 1;
      opacity: 0.7;
    }}
    @keyframes gridDrift {{
      0% {{ transform: perspective(600px) rotateX(45deg) translateY(0); }}
      100% {{ transform: perspective(600px) rotateX(45deg) translateY(48px); }}
    }}

    /* Glowing ambient light orbs */
    .ambient-orb {{
      position: absolute;
      border-radius: 50%;
      filter: blur(90px);
      z-index: 2;
      opacity: 0.55;
      animation: pulseOrb 6s ease-in-out infinite alternate;
    }}
    .orb-1 {{ width: 420px; height: 420px; background: #6366F1; top: 100px; left: -100px; }}
    .orb-2 {{ width: 380px; height: 380px; background: #06B6D4; top: 400px; right: -80px; animation-delay: -3s; }}
    .orb-3 {{ width: 320px; height: 320px; background: #EC4899; bottom: 150px; left: 80px; animation-delay: -1.5s; }}
    @keyframes pulseOrb {{
      0% {{ transform: scale(1) translate(0, 0); opacity: 0.45; }}
      100% {{ transform: scale(1.25) translate(30px, -20px); opacity: 0.7; }}
    }}

    /* Top HUD Header */
    .top-hud {{
      position: absolute;
      top: 50px;
      left: 36px;
      right: 36px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 50;
    }}
    .hud-badge {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(56, 189, 248, 0.4);
      padding: 10px 20px;
      border-radius: 30px;
      font-size: 16px;
      font-weight: 800;
      letter-spacing: 1px;
      color: #38BDF8;
      box-shadow: 0 0 25px rgba(56, 189, 248, 0.25);
    }}
    .hud-dot {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #EF4444;
      box-shadow: 0 0 10px #EF4444;
      animation: blink 1s ease infinite alternate;
    }}
    @keyframes blink {{ 0% {{ opacity: 0.3; }} 100% {{ opacity: 1; }} }}
    .hud-stars {{
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(250, 204, 21, 0.4);
      padding: 10px 20px;
      border-radius: 30px;
      font-size: 16px;
      font-weight: 800;
      color: #FACC15;
      box-shadow: 0 0 25px rgba(250, 204, 21, 0.2);
    }}

    /* Timeline progress meter line */
    .hud-progress-bar {{
      position: absolute;
      top: 0;
      left: 0;
      height: 6px;
      background: linear-gradient(90deg, #06B6D4, #3B82F6, #EC4899);
      width: 0%;
      z-index: 100;
      box-shadow: 0 0 15px #06B6D4;
    }}

    /* Scene Layers */
    .scene-container {{
      position: absolute;
      inset: 0;
      z-index: 10;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      opacity: 0;
      pointer-events: none;
    }}

    /* Hero Glass Window for Real Media */
    .media-window {{
      position: relative;
      width: 650px;
      height: 720px;
      background: rgba(15, 23, 42, 0.92);
      border-radius: 20px;
      border: 1.5px solid rgba(255, 255, 255, 0.15);
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8), 0 0 40px rgba(99, 102, 241, 0.35);
      overflow: hidden;
      margin-top: -20px;
    }}
    .window-header {{
      height: 48px;
      background: rgba(30, 41, 59, 0.95);
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      align-items: center;
      padding: 0 18px;
      gap: 8px;
    }}
    .win-dot {{ width: 12px; height: 12px; border-radius: 50%; }}
    .win-dot.r {{ background: #EF4444; }}
    .win-dot.y {{ background: #F59E0B; }}
    .win-dot.g {{ background: #10B981; }}
    .window-title {{
      margin-left: 12px;
      font-size: 14px;
      font-weight: 700;
      color: #94A3B8;
      letter-spacing: 0.5px;
    }}

    /* Continuous Ken Burns Zoom & 3D Pan on Real Media */
    .media-viewport {{
      position: relative;
      width: 100%;
      height: calc(100% - 48px);
      overflow: hidden;
    }}
    .media-viewport img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: top center;
      transform-origin: center center;
    }}

    /* Live Scanning Laser Line */
    .scanline {{
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, transparent, #00F0FF, #FFFFFF, #00F0FF, transparent);
      box-shadow: 0 0 20px #00F0FF, 0 0 40px #00F0FF;
      animation: scanSweep 3.5s ease-in-out infinite alternate;
      z-index: 15;
    }}
    @keyframes scanSweep {{
      0% {{ top: 5%; opacity: 0.8; }}
      100% {{ top: 92%; opacity: 1; }}
    }}

    /* Floating kinetic feature pills */
    .floating-pill {{
      position: absolute;
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 14px;
      padding: 10px 18px;
      font-size: 16px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
      z-index: 25;
      animation: floatBadge 3s ease-in-out infinite alternate;
    }}
    @keyframes floatBadge {{
      0% {{ transform: translateY(0px); }}
      100% {{ transform: translateY(-12px); }}
    }}

    /* Terminal Command Strip */
    .terminal-bar {{
      position: absolute;
      bottom: 240px;
      left: 36px;
      right: 36px;
      background: rgba(15, 23, 42, 0.9);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(56, 189, 248, 0.35);
      border-radius: 14px;
      padding: 14px 22px;
      font-family: "JetBrains Mono", Menlo, Consolas, monospace;
      font-size: 17px;
      color: #38BDF8;
      display: flex;
      align-items: center;
      gap: 12px;
      z-index: 40;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7);
    }}
    .cursor-blink {{
      display: inline-block;
      width: 10px;
      height: 18px;
      background: #38BDF8;
      animation: blink 0.8s infinite;
    }}

    /* High-Impact Kinetic Captions (Centered Bottom) */
    .caption-container {{
      position: absolute;
      bottom: 70px;
      left: 36px;
      right: 36px;
      z-index: 100;
      display: flex;
      justify-content: center;
      align-items: center;
      pointer-events: none;
    }}
    .caption-pill {{
      background: rgba(10, 15, 29, 0.94);
      backdrop-filter: blur(20px);
      border: 2px solid rgba(250, 204, 21, 0.5);
      border-radius: 24px;
      padding: 16px 28px;
      text-align: center;
      box-shadow: 0 15px 45px rgba(0, 0, 0, 0.9), 0 0 30px rgba(250, 204, 21, 0.25);
      max-width: 660px;
      min-height: 80px;
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      align-items: center;
      gap: 10px;
    }}
    .caption-word {{
      font-size: 32px;
      font-weight: 900;
      color: #E2E8F0;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      transition: all 0.08s ease;
    }}
    .caption-word.active {{
      color: #FACC15;
      text-shadow: 0 0 25px rgba(250, 204, 21, 0.9), 0 0 45px rgba(250, 204, 21, 0.6);
      transform: scale(1.18);
    }}

    /* Hook Scene Specific */
    .hook-headline {{
      font-size: 58px;
      font-weight: 900;
      text-align: center;
      line-height: 1.15;
      background: linear-gradient(135deg, #FFFFFF 20%, #38BDF8 60%, #818CF8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      padding: 0 40px;
      margin-bottom: 30px;
      text-shadow: 0 0 40px rgba(56, 189, 248, 0.3);
    }}
    .hook-badge-wrap {{
      display: flex;
      gap: 16px;
      justify-content: center;
      margin-top: 20px;
    }}

    /* CTA Outro Specific */
    .cta-box {{
      background: rgba(15, 23, 42, 0.92);
      border: 2px solid #FACC15;
      border-radius: 28px;
      padding: 40px 36px;
      text-align: center;
      box-shadow: 0 0 60px rgba(250, 204, 21, 0.35);
      width: 620px;
    }}
    .cta-keyword {{
      font-size: 64px;
      font-weight: 900;
      color: #FACC15;
      letter-spacing: 3px;
      margin: 15px 0;
      text-shadow: 0 0 35px rgba(250, 204, 21, 0.8);
      animation: pulseCta 1.5s ease-in-out infinite alternate;
    }}
    @keyframes pulseCta {{
      0% {{ transform: scale(1); }}
      100% {{ transform: scale(1.06); }}
    }}
  </style>
</head>
<body>
  <div id="root">
    <!-- Top Progress Bar -->
    <div id="progress-bar" class="hud-progress-bar"></div>

    <!-- Background Elements -->
    <div class="grid-bg"></div>
    <div class="ambient-orb orb-1"></div>
    <div class="ambient-orb orb-2"></div>
    <div class="ambient-orb orb-3"></div>

    <!-- Top HUD Bar -->
    <div class="top-hud">
      <div id="top-badge" class="hud-badge">
        <div class="hud-dot"></div>
        <span>AI RADAR 2026</span>
      </div>
      <div id="hud-stars" class="hud-stars">★ 3 KILLER REPOS</div>
    </div>

    <!-- SCENE 0: HOOK -->
    <div id="scene-hook" class="scene-container" style="opacity: 1;">
      <div class="hook-headline">STOP PAYING<br>MONTHLY AI FEES</div>
      <div style="font-size: 24px; color: #94A3B8; font-weight: 700; text-align: center; max-width: 540px;">
        3 Free Open-Source Repos That Grant Real Superpowers
      </div>
      <div class="hook-badge-wrap">
        <div class="hud-badge" style="border-color: #10B981; color: #10B981;">✓ 100% FREE</div>
        <div class="hud-badge" style="border-color: #818CF8; color: #818CF8;">⚡ LOCAL RUN</div>
      </div>
    </div>

    <!-- SCENE 1: REPO 1 -->
    <div id="scene-tool1" class="scene-container">
      <div class="media-window">
        <div class="window-header">
          <div class="win-dot r"></div><div class="win-dot y"></div><div class="win-dot g"></div>
          <div class="window-title">{repo_media[0]['owner']} / {repo_media[0]['name']}</div>
          <div style="margin-left: auto; color: #FACC15; font-size: 13px; font-weight: 800;">{repo_media[0]['stars']}</div>
        </div>
        <div class="media-viewport">
          <img id="img-tool1" src="{repo_media[0]['img']}" alt="Repo 1 demo">
          <div class="scanline"></div>
        </div>
      </div>
      <div class="floating-pill" style="top: 240px; right: 20px; border-color: #38BDF8; color: #38BDF8;">
        ⚡ 01 · {repo_media[0]['name']}
      </div>
    </div>

    <!-- SCENE 2: REPO 2 -->
    <div id="scene-tool2" class="scene-container">
      <div class="media-window">
        <div class="window-header">
          <div class="win-dot r"></div><div class="win-dot y"></div><div class="win-dot g"></div>
          <div class="window-title">{repo_media[1]['owner']} / {repo_media[1]['name']}</div>
          <div style="margin-left: auto; color: #FACC15; font-size: 13px; font-weight: 800;">{repo_media[1]['stars']}</div>
        </div>
        <div class="media-viewport">
          <img id="img-tool2" src="{repo_media[1]['img']}" alt="Repo 2 demo">
          <div class="scanline"></div>
        </div>
      </div>
      <div class="floating-pill" style="top: 240px; right: 20px; border-color: #A855F7; color: #A855F7;">
        🚀 02 · {repo_media[1]['name']}
      </div>
    </div>

    <!-- SCENE 3: REPO 3 -->
    <div id="scene-tool3" class="scene-container">
      <div class="media-window">
        <div class="window-header">
          <div class="win-dot r"></div><div class="win-dot y"></div><div class="win-dot g"></div>
          <div class="window-title">{repo_media[2]['owner']} / {repo_media[2]['name']}</div>
          <div style="margin-left: auto; color: #FACC15; font-size: 13px; font-weight: 800;">{repo_media[2]['stars']}</div>
        </div>
        <div class="media-viewport">
          <img id="img-tool3" src="{repo_media[2]['img']}" alt="Repo 3 demo">
          <div class="scanline"></div>
        </div>
      </div>
      <div class="floating-pill" style="top: 240px; right: 20px; border-color: #10B981; color: #10B981;">
        🔥 03 · {repo_media[2]['name']}
      </div>
    </div>

    <!-- SCENE 4: CTA OUTRO -->
    <div id="scene-cta" class="scene-container">
      <div class="cta-box">
        <div style="font-size: 22px; color: #94A3B8; font-weight: 800; text-transform: uppercase; letter-spacing: 2px;">
          Want all 3 repositories?
        </div>
        <div style="font-size: 28px; color: #FFFFFF; font-weight: 900; margin-top: 10px;">
          COMMENT BELOW:
        </div>
        <div class="cta-keyword">TOOLS</div>
        <div style="font-size: 18px; color: #E2E8F0; font-weight: 700; line-height: 1.5;">
          I'll DM you direct GitHub links right now! 🚀<br>
          <span style="color: #38BDF8;">Follow for daily open-source AI drops.</span>
        </div>
      </div>
    </div>

    <!-- Terminal Command Strip -->
    <div id="terminal-bar" class="terminal-bar">
      <span style="color: #10B981; font-weight: 900;">❯</span>
      <span id="term-text">git clone open-source-ai-repos</span>
      <span class="cursor-blink"></span>
    </div>

    <!-- Word-by-Word Kinetic Subtitles -->
    <div class="caption-container">
      <div id="caption-pill" class="caption-pill">
        <span class="caption-word active">READY</span>
      </div>
    </div>

  </div>

  <script>
    const tl = gsap.timeline({{ paused: true }});
    window.__timelines = {{ root: tl }};
    tl.to({{}}, {{ duration: {duration} }}, 0);

    // Continuous timeline progress bar
    tl.to("#progress-bar", {{ width: "100%", duration: {duration}, ease: "none" }}, 0);

    // Continuous Ken Burns 3D Camera zooms on real images
    tl.fromTo("#img-tool1", 
      {{ scale: 1.05, x: 0, y: 0 }}, 
      {{ scale: 1.25, x: -15, y: -20, duration: {t_tool1_end - t_hook_end}, ease: "power1.inOut" }}, 
      {t_hook_end}
    );
    tl.fromTo("#img-tool2", 
      {{ scale: 1.05, x: 0, y: 0 }}, 
      {{ scale: 1.25, x: 15, y: -25, duration: {t_tool2_end - t_tool1_end}, ease: "power1.inOut" }}, 
      {t_tool1_end}
    );
    tl.fromTo("#img-tool3", 
      {{ scale: 1.05, x: 0, y: 0 }}, 
      {{ scale: 1.25, x: -20, y: -15, duration: {t_tool3_end - t_tool2_end}, ease: "power1.inOut" }}, 
      {t_tool2_end}
    );

    // Scene Transition Timings (Exact Synced Pacing)
    const sceneCuts = [
      {{ id: "#scene-hook", start: 0, end: {t_hook_end}, stars: "3 KILLER REPOS", badge: "AI RADAR 2026", cmd: "npx scan-ai-repos" }},
      {{ id: "#scene-tool1", start: {t_hook_end}, end: {t_tool1_end}, stars: "{repo_media[0]['stars']}", badge: "01 · {repo_media[0]['name']}", cmd: "git clone {repo_media[0]['name'].lower()}" }},
      {{ id: "#scene-tool2", start: {t_tool1_end}, end: {t_tool2_end}, stars: "{repo_media[1]['stars']}", badge: "02 · {repo_media[1]['name']}", cmd: "npm install {repo_media[1]['name'].lower()}" }},
      {{ id: "#scene-tool3", start: {t_tool2_end}, end: {t_tool3_end}, stars: "{repo_media[2]['stars']}", badge: "03 · {repo_media[2]['name']}", cmd: "pip install {repo_media[2]['name'].lower()}" }},
      {{ id: "#scene-cta", start: {t_tool3_end}, end: {t_cta_end}, stars: "COMMENT 'TOOLS'", badge: "GET LINKS NOW", cmd: "echo 'DM sent!'" }}
    ];

    sceneCuts.forEach(sc => {{
      tl.set(sc.id, {{ opacity: 1, pointerEvents: "auto" }}, sc.start);
      if (sc.end < {duration}) {{
        tl.set(sc.id, {{ opacity: 0, pointerEvents: "none" }}, sc.end);
      }}
      tl.set("#hud-stars", {{ innerText: sc.stars }}, sc.start);
      tl.set("#top-badge span", {{ innerText: sc.badge }}, sc.start);
      tl.set("#term-text", {{ innerText: sc.cmd }}, sc.start);
    }});

    // Synchronized Kinetic Captions
    const captionData = {json.dumps(caption_chunks)};
    captionData.forEach(chunk => {{
      tl.call(() => {{
        const pill = document.getElementById("caption-pill");
        pill.innerHTML = "";
        chunk.words.forEach((w, wIdx) => {{
          const span = document.createElement("span");
          span.className = "caption-word" + (wIdx === chunk.active ? " active" : "");
          span.innerText = w;
          pill.appendChild(span);
        }});
      }}, null, chunk.start);
    }});
  </script>
</body>
</html>
"""
    with open(output_html, "w") as f:
        f.write(html)
    print(f"[✓] Generated 100% Hyper-Motion Composition ({round(duration, 1)}s) at {output_html}")
    return output_html

if __name__ == "__main__":
    build_hyperframes_composition(duration=38.0)
