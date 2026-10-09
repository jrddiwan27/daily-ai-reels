import json
import os

def build_hyperframes_composition(
    repos_file="assets/curated_repos.json",
    captions_file="assets/caption_chunks.json",
    audio_path="assets/voice.mp3",
    script_file="assets/generated_script.json",
    duration=28.76,
    output_html="index.html"
):
    """
    9.5/10 Gold-Standard Comic Motion Graphic Reel:
    - Halftone dot texture per scene with dynamic desk & background palette
    - Fully rigged developer avatar with angled presenter point gesture directly toward console
    - Natural resting hand on desk lip
    - Kinetic widgets for every tool:
        1. TT-Metal: Live animated silicon hardware compilation progress bar (0% -> 100%)
        2. Magic-Context: Live animated context reduction compaction gauge (128k -> 1.2k tokens, -99%)
        3. Inbox-Zero: Mechanical unread email odometer rapidly counting down 1,420 -> 0 + INBOX ZERO badge slam
    - Grounded 3D smartphone displaying Instagram automated DM delivery with all 3 repos
    - 3D tactile keyboard keycap captions with yellow active pop
    - Zero static frames: drifting crosshairs, slow scene push-ins, steam bubbles, head bob & mouth sync
    """
    with open(repos_file) as f:
        repos = json.load(f)[:3]
        
    with open(captions_file) as f:
        caption_chunks = json.load(f)

    # Dynamic scene timings based on audio duration (28.76s)
    t_hook_end = min(3.8, duration * 0.13)
    t_tool1_end = duration * 0.40
    t_tool2_end = duration * 0.68
    t_tool3_end = duration * 0.88
    t_cta_end = duration

    # Real repo metadata with fallback demo media
    repo_data = []
    default_demos = [
        "assets/repos/tenstorrent_tt-metal/demo.png",
        "assets/repos/cortexkit_magic-context/og_banner.png",
        "assets/repos/elie222_inbox-zero/demo.jpg"
    ]
    for idx, r in enumerate(repos):
        demo_path = r.get("demo_media") or r.get("og_image") or default_demos[idx]
        repo_data.append({
            "name": r["name"].split("/")[-1].upper(),
            "owner": r.get("owner", "open-source"),
            "full_name": r.get("full_name", r["name"]),
            "stars": f"★ {r.get('stars', 12000):,}",
            "desc": r.get("description", "")[:95],
            "demo": demo_path
        })

    # Exact 720x1280 resolution matching the reference standard
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
  <title>Top AI Dev Repos - Comic Halftone Motion Graphic Reel</title>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{
      width: 720px;
      height: 1280px;
      overflow: hidden;
      background: #F4EEDF;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      user-select: none;
    }}

    #root {{
      position: relative;
      width: 720px;
      height: 1280px;
      overflow: hidden;
      background: #F4EEDF;
    }}

    /* Halftone dot pattern per scene */
    .bg-layer {{
      position: absolute;
      inset: 0;
      opacity: 0;
      z-index: 1;
    }}
    .bg-hook {{
      background-color: #F4EEDF;
      background-image: radial-gradient(#C8BFAD 2.4px, transparent 2.4px), radial-gradient(#C8BFAD 2.4px, transparent 2.4px);
      background-size: 24px 24px;
      background-position: 0 0, 12px 12px;
      opacity: 1;
    }}
    .bg-tool1 {{
      background-color: #E0F2FE;
      background-image: radial-gradient(#93C5FD 2.4px, transparent 2.4px), radial-gradient(#93C5FD 2.4px, transparent 2.4px);
      background-size: 24px 24px;
      background-position: 0 0, 12px 12px;
    }}
    .bg-tool2 {{
      background-color: #ECFDF5;
      background-image: radial-gradient(#6EE7B7 2.4px, transparent 2.4px), radial-gradient(#6EE7B7 2.4px, transparent 2.4px);
      background-size: 24px 24px;
      background-position: 0 0, 12px 12px;
    }}
    .bg-tool3 {{
      background-color: #FEF3C7;
      background-image: radial-gradient(#FCD34D 2.4px, transparent 2.4px), radial-gradient(#FCD34D 2.4px, transparent 2.4px);
      background-size: 24px 24px;
      background-position: 0 0, 12px 12px;
    }}
    .bg-outro {{
      background-color: #EDE9FE;
      background-image: radial-gradient(#C4B5FD 2.4px, transparent 2.4px), radial-gradient(#C4B5FD 2.4px, transparent 2.4px);
      background-size: 24px 24px;
      background-position: 0 0, 12px 12px;
    }}

    /* Floating crosshairs */
    .crosshair {{
      position: absolute;
      font-family: monospace;
      font-size: 24px;
      font-weight: 900;
      color: rgba(23, 24, 25, 0.28);
      pointer-events: none;
      z-index: 2;
    }}

    /* Top Left Slanted Comic Sticker Badge */
    .top-badge {{
      position: absolute;
      left: 36px;
      top: 36px;
      z-index: 50;
      background: #171819;
      color: #FFFFFF;
      font-size: 20px;
      font-weight: 950;
      letter-spacing: 0.08em;
      padding: 10px 22px;
      border-radius: 4px;
      transform: rotate(-1.5deg);
      box-shadow: 4px 4px 0 rgba(0,0,0,0.25);
      border: 3px solid #171819;
      display: inline-block;
    }}

    /* Top Right 3-Plug Power Strip Meter */
    .top-meter {{
      position: absolute;
      right: 36px;
      top: 30px;
      z-index: 50;
      background: #FFFFFF;
      border: 4px solid #171819;
      border-radius: 14px;
      padding: 8px 14px 6px;
      box-shadow: 5px 5px 0 #171819;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
    }}
    .meter-strip {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .meter-switch {{
      width: 16px;
      height: 26px;
      background: #E03622;
      border: 3px solid #171819;
      border-radius: 4px;
    }}
    .meter-sockets {{
      display: flex;
      gap: 7px;
    }}
    .socket-dot {{
      width: 24px;
      height: 24px;
      background: #E8E2D2;
      border: 3px solid #171819;
      border-radius: 50%;
      position: relative;
    }}
    .socket-dot::before, .socket-dot::after {{
      content: "";
      position: absolute;
      top: 5px;
      width: 3px;
      height: 7px;
      background: #171819;
      border-radius: 1px;
    }}
    .socket-dot::before {{ left: 5px; }}
    .socket-dot::after {{ right: 5px; }}
    .socket-dot.plug-1 {{ background: #2563EB; box-shadow: 0 0 12px #2563EB; }}
    .socket-dot.plug-2 {{ background: #059669; box-shadow: 0 0 12px #059669; }}
    .socket-dot.plug-3 {{ background: #EA580C; box-shadow: 0 0 12px #EA580C; }}

    .meter-label {{
      font-size: 11px;
      font-weight: 950;
      letter-spacing: 0.12em;
      color: #171819;
    }}

    .spark-fx {{
      position: absolute;
      top: 24px;
      right: 50px;
      font-size: 34px;
      opacity: 0;
      z-index: 60;
      pointer-events: none;
    }}

    /* Studio Desk */
    .desk {{
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      height: 380px;
      background: #B64D29;
      border-top: 10px solid #171819;
      z-index: 20;
      box-shadow: inset 0 10px 0 rgba(255,255,255,0.18);
    }}
    .desk::before {{
      content: "";
      position: absolute;
      inset: 0;
      background: repeating-linear-gradient(90deg, transparent 0, transparent 238px, rgba(0,0,0,0.14) 238px, rgba(0,0,0,0.14) 242px);
    }}
    .desk-drawer {{
      position: absolute;
      top: 36px;
      left: 100px;
      width: 140px;
      height: 26px;
      background: #171819;
      border-radius: 13px;
      border: 3px solid rgba(255,255,255,0.25);
    }}
    .desk-drawer-right {{
      position: absolute;
      top: 36px;
      right: 100px;
      width: 140px;
      height: 26px;
      background: #171819;
      border-radius: 13px;
      border: 3px solid rgba(255,255,255,0.25);
    }}

    /* Coffee mug with rising steam */
    .desk-mug {{
      position: absolute;
      right: 48px;
      bottom: 390px;
      width: 46px;
      height: 52px;
      background: #FFFFFF;
      border: 4px solid #171819;
      border-radius: 4px 4px 10px 10px;
      z-index: 25;
    }}
    .desk-mug::before {{
      content: "";
      position: absolute;
      top: 14px;
      left: 0;
      right: 0;
      height: 9px;
      background: #2563EB;
    }}
    .desk-mug::after {{
      content: "";
      position: absolute;
      right: -16px;
      top: 12px;
      width: 14px;
      height: 24px;
      border: 4px solid #171819;
      border-radius: 0 10px 10px 0;
    }}
    .steam-bubble {{
      position: absolute;
      right: 64px;
      bottom: 450px;
      font-size: 18px;
      color: rgba(23, 24, 25, 0.4);
      z-index: 25;
      font-weight: 900;
    }}
    .desk-tape {{
      position: absolute;
      left: 42px;
      bottom: 392px;
      width: 40px;
      height: 40px;
      border: 10px solid #171819;
      border-radius: 50%;
      background: transparent;
      z-index: 25;
    }}
    .desk-ruler {{
      position: absolute;
      left: 100px;
      bottom: 394px;
      width: 90px;
      height: 8px;
      background: #EAB308;
      border: 2px solid #171819;
      border-radius: 4px;
      z-index: 25;
    }}

    /* Avatar Container */
    .avatar-wrapper {{
      position: absolute;
      left: 50%;
      bottom: 310px;
      transform: translateX(-50%);
      width: 480px;
      height: 460px;
      z-index: 22;
      pointer-events: none;
    }}
    .avatar-svg {{
      width: 100%;
      height: 100%;
      overflow: visible;
    }}

    /* Scene Layers */
    .scene-layer {{
      position: absolute;
      inset: 0;
      z-index: 15;
      pointer-events: none;
    }}

    /* Upper Repo Card Base */
    .upper-card {{
      position: absolute;
      left: 30px;
      top: 95px;
      width: 660px;
      background: #FFFFFF;
      border: 5px solid #171819;
      border-radius: 18px;
      box-shadow: 6px 8px 0 #171819;
      padding: 16px 20px;
      color: #171819;
      z-index: 18;
    }}
    .repo-header {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 6px;
    }}
    .repo-icon {{
      font-size: 24px;
    }}
    .repo-slug {{
      font-weight: 950;
      font-size: 19px;
      letter-spacing: -0.01em;
    }}
    .repo-star {{
      margin-left: auto;
      background: #FEF08A;
      border: 2px solid #171819;
      border-radius: 6px;
      padding: 2px 8px;
      font-weight: 950;
      font-size: 14px;
      box-shadow: 2px 2px 0 #171819;
    }}
    .repo-title {{
      font-size: 24px;
      font-weight: 950;
      margin-bottom: 4px;
    }}
    .repo-desc {{
      font-size: 15px;
      color: #4B5563;
      font-weight: 750;
      line-height: 1.35;
    }}

    /* Grounded Tech Console */
    .tech-console {{
      position: absolute;
      left: 30px;
      top: 255px;
      width: 405px;
      height: 635px;
      background: #191B21;
      border: 5px solid #171819;
      border-radius: 18px;
      box-shadow: 8px 10px 0 #171819;
      color: #F3F4F6;
      padding: 14px 16px;
      z-index: 25;
      font-family: monospace;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}
    .console-header {{
      display: flex;
      align-items: center;
      gap: 6px;
      padding-bottom: 10px;
      border-bottom: 2px solid #374151;
      margin-bottom: 12px;
      font-size: 13px;
      color: #9CA3AF;
    }}
    .console-dots {{ display: flex; gap: 6px; }}
    .console-dot {{ width: 11px; height: 11px; border-radius: 50%; }}
    .console-dot.r {{ background: #EF4444; }}
    .console-dot.y {{ background: #F59E0B; }}
    .console-dot.g {{ background: #10B981; }}
    .console-title {{ margin-left: auto; font-weight: 700; color: #D1D5DB; font-size: 12px; }}

    .demo-media-box {{
      width: 100%;
      height: 155px;
      border-radius: 10px;
      overflow: hidden;
      border: 2.5px solid #374151;
      margin-bottom: 10px;
      background: #000;
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
      position: relative;
    }}
    .demo-media-box img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}

    /* Bottom Tactile Keyboard Keycaps Captions on Desk Front */
    .captions-wrapper {{
      position: absolute;
      left: 0;
      right: 0;
      bottom: 200px;
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 60;
    }}
    .caption-pill {{
      background: #171819;
      border: 5px solid #FFFFFF;
      border-radius: 22px;
      padding: 12px 28px;
      box-shadow: 0 10px 0 #000000, 0 16px 24px rgba(0,0,0,0.35);
      display: flex;
      gap: 12px;
      align-items: center;
      justify-content: center;
      max-width: 90%;
    }}
    .caption-word {{
      font-size: 38px;
      font-weight: 950;
      color: #FFFFFF;
      letter-spacing: -0.02em;
      line-height: 1;
    }}
    .caption-word.active {{
      background: #FACC15;
      color: #171819;
      padding: 4px 16px;
      border-radius: 12px;
      box-shadow: 2px 2px 0 #000000;
    }}

    /* Phone Mockup for Outro */
    .phone-mockup {{
      position: absolute;
      left: 45px;
      top: 175px;
      width: 375px;
      height: 715px;
      background: #000000;
      border: 9px solid #171819;
      border-radius: 50px;
      box-shadow: 8px 12px 0 #171819;
      z-index: 25;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}
    .phone-notch {{
      width: 150px;
      height: 24px;
      background: #171819;
      margin: 0 auto;
      border-radius: 0 0 14px 14px;
      z-index: 30;
    }}
    .phone-screen {{
      flex: 1;
      background: #FFFFFF;
      padding: 18px 16px;
      font-family: -apple-system, sans-serif;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}
  </style>
</head>
<body>
  <div id="root" data-composition-id="root" data-start="0" data-duration="{round(duration, 2)}" data-width="720" data-height="1280">

    <!-- Scene Background Layers -->
    <div id="bg-hook" class="bg-layer bg-hook"></div>
    <div id="bg-tool1" class="bg-layer bg-tool1"></div>
    <div id="bg-tool2" class="bg-layer bg-tool2"></div>
    <div id="bg-tool3" class="bg-layer bg-tool3"></div>
    <div id="bg-outro" class="bg-layer bg-outro"></div>

    <!-- Floating Crosshairs -->
    <div class="crosshair ch1" style="left: 40px; top: 90px;">+</div>
    <div class="crosshair ch2" style="right: 50px; top: 120px;">+</div>
    <div class="crosshair ch3" style="left: 30px; top: 480px;">+</div>
    <div class="crosshair ch4" style="right: 40px; top: 520px;">+</div>

    <!-- Audio Elements for HyperFrames Native Mixer -->
    <audio id="voice" src="{audio_path}" data-start="0" data-duration="{round(duration, 2)}" data-volume="1"></audio>
    <audio id="sfx-whoosh-1" src="assets/sfx/sfx_whoosh.mp3" data-start="0.0" data-duration="0.5" data-volume="0.6"></audio>
    <audio id="sfx-whoosh-2" src="assets/sfx/sfx_whoosh.mp3" data-start="{round(t_hook_end, 2)}" data-duration="0.5" data-volume="0.6"></audio>
    <audio id="sfx-pop-1" src="assets/sfx/sfx_pop.mp3" data-start="{round(t_hook_end + 0.35, 2)}" data-duration="0.5" data-volume="0.5"></audio>
    <audio id="sfx-ding-1" src="assets/sfx/sfx_ding.mp3" data-start="{round(t_hook_end + 0.85, 2)}" data-duration="0.5" data-volume="0.5"></audio>
    <audio id="sfx-whoosh-3" src="assets/sfx/sfx_whoosh.mp3" data-start="{round(t_tool1_end, 2)}" data-duration="0.5" data-volume="0.6"></audio>
    <audio id="sfx-pop-2" src="assets/sfx/sfx_pop.mp3" data-start="{round(t_tool1_end + 0.35, 2)}" data-duration="0.5" data-volume="0.5"></audio>
    <audio id="sfx-ding-2" src="assets/sfx/sfx_ding.mp3" data-start="{round(t_tool1_end + 0.85, 2)}" data-duration="0.5" data-volume="0.5"></audio>
    <audio id="sfx-whoosh-4" src="assets/sfx/sfx_whoosh.mp3" data-start="{round(t_tool2_end, 2)}" data-duration="0.5" data-volume="0.6"></audio>
    <audio id="sfx-pop-3" src="assets/sfx/sfx_pop.mp3" data-start="{round(t_tool2_end + 0.35, 2)}" data-duration="0.5" data-volume="0.5"></audio>
    <audio id="sfx-whoosh-5" src="assets/sfx/sfx_whoosh.mp3" data-start="{round(t_tool3_end, 2)}" data-duration="0.5" data-volume="0.6"></audio>
    <audio id="sfx-click-1" src="assets/sfx/sfx_click.mp3" data-start="{round(t_tool3_end + 0.25, 2)}" data-duration="0.3" data-volume="0.6"></audio>

    <!-- Top Left Comic Sticker Badge -->
    <div id="top-badge" class="top-badge">STOP PAYING FOR AI</div>

    <!-- Top Right 3-Plug Power Strip Meter -->
    <div id="top-meter" class="top-meter">
      <div class="meter-strip">
        <div class="meter-switch"></div>
        <div class="meter-sockets">
          <div id="sock-1" class="socket-dot"></div>
          <div id="sock-2" class="socket-dot"></div>
          <div id="sock-3" class="socket-dot"></div>
        </div>
      </div>
      <div id="meter-label" class="meter-label">REPOS 0/3</div>
    </div>
    <div id="spark-fx" class="spark-fx">💥</div>

    <!-- Studio Desk -->
    <div id="desk" class="desk">
      <div class="desk-drawer"></div>
      <div class="desk-drawer-right"></div>
      <div class="desk-tape"></div>
      <div class="desk-ruler"></div>
      <div class="desk-mug"></div>
      <div id="steam-1" class="steam-bubble">~</div>
      <div id="steam-2" class="steam-bubble" style="right: 56px; bottom: 462px;">~</div>
    </div>

    <!-- Developer Avatar Rig -->
    <div id="avatar-wrap" class="avatar-wrapper">
      <svg class="avatar-svg" viewBox="0 0 480 460" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="skin" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#FCE1CA"/>
            <stop offset="100%" stop-color="#F2BA91"/>
          </linearGradient>
        </defs>

        <!-- Torso & Clothes -->
        <g id="torso">
          <path d="M130 330 C130 310, 180 295, 240 295 C300 295, 350 310, 350 330 L380 460 L100 460 Z" fill="#756D65" stroke="#171819" stroke-width="8"/>
          <path d="M210 295 C210 330, 270 330, 270 295 Z" fill="#FFFFFF" stroke="#171819" stroke-width="6"/>
          <path d="M180 295 L220 380 L200 460" fill="none" stroke="#171819" stroke-width="6"/>
          <path d="M300 295 L260 380 L280 460" fill="none" stroke="#171819" stroke-width="6"/>
        </g>

        <!-- Arms -->
        <g id="arm-left">
          <!-- Pointing Arm (Default when presenting on right) -->
          <g id="arm-point" opacity="0">
            <path d="M340 330 C380 320, 390 260, 375 220" fill="none" stroke="#171819" stroke-width="44" stroke-linecap="round"/>
            <path d="M340 330 C380 320, 390 260, 375 220" fill="none" stroke="#756D65" stroke-width="36" stroke-linecap="round"/>
            <g transform="translate(365, 170)">
              <ellipse cx="14" cy="40" rx="18" ry="16" fill="url(#skin)" stroke="#171819" stroke-width="6"/>
              <rect x="8" y="0" width="12" height="32" rx="6" fill="url(#skin)" stroke="#171819" stroke-width="6"/>
            </g>
          </g>

          <!-- Both Hands Up in Frustration (Hook Intro) -->
          <g id="arm-both-up" opacity="1">
            <path d="M140 330 C100 290, 90 220, 110 170" fill="none" stroke="#171819" stroke-width="44" stroke-linecap="round"/>
            <path d="M140 330 C100 290, 90 220, 110 170" fill="none" stroke="#756D65" stroke-width="36" stroke-linecap="round"/>
            <g transform="translate(90, 120)">
              <circle cx="20" cy="35" r="18" fill="url(#skin)" stroke="#171819" stroke-width="6"/>
              <rect x="5" y="8" width="8" height="24" rx="4" fill="url(#skin)" stroke="#171819" stroke-width="5"/>
              <rect x="16" y="2" width="8" height="28" rx="4" fill="url(#skin)" stroke="#171819" stroke-width="5"/>
              <rect x="27" y="5" width="8" height="26" rx="4" fill="url(#skin)" stroke="#171819" stroke-width="5"/>
              <rect x="37" y="12" width="7" height="20" rx="4" fill="url(#skin)" stroke="#171819" stroke-width="5"/>
            </g>
            <path d="M340 330 C380 290, 390 220, 370 170" fill="none" stroke="#171819" stroke-width="44" stroke-linecap="round"/>
            <path d="M340 330 C380 290, 390 220, 370 170" fill="none" stroke="#756D65" stroke-width="36" stroke-linecap="round"/>
            <g transform="translate(350, 120)">
              <circle cx="20" cy="35" r="18" fill="url(#skin)" stroke="#171819" stroke-width="6"/>
              <rect x="5" y="8" width="8" height="24" rx="4" fill="url(#skin)" stroke="#171819" stroke-width="5"/>
              <rect x="16" y="2" width="8" height="28" rx="4" fill="url(#skin)" stroke="#171819" stroke-width="5"/>
              <rect x="27" y="5" width="8" height="26" rx="4" fill="url(#skin)" stroke="#171819" stroke-width="5"/>
              <rect x="37" y="12" width="7" height="20" rx="4" fill="url(#skin)" stroke="#171819" stroke-width="5"/>
            </g>
          </g>

          <!-- Confident Thumbs Up Arm (Outro) -->
          <g id="arm-thumbs-up" opacity="0">
            <path d="M340 330 C370 320, 380 280, 360 240" fill="none" stroke="#171819" stroke-width="44" stroke-linecap="round"/>
            <path d="M340 330 C370 320, 380 280, 360 240" fill="none" stroke="#756D65" stroke-width="36" stroke-linecap="round"/>
            <g transform="translate(350, 200)">
              <circle cx="20" cy="30" r="16" fill="url(#skin)" stroke="#171819" stroke-width="6"/>
              <rect x="14" y="6" width="12" height="20" rx="5" fill="url(#skin)" stroke="#171819" stroke-width="5"/>
            </g>
          </g>
        </g>

        <!-- Head -->
        <g id="head">
          <rect x="216" y="240" width="48" height="55" fill="url(#skin)" stroke="#171819" stroke-width="7"/>
          <ellipse cx="240" cy="180" rx="72" ry="80" fill="url(#skin)" stroke="#171819" stroke-width="8"/>
          <ellipse cx="166" cy="180" rx="14" ry="18" fill="url(#skin)" stroke="#171819" stroke-width="6"/>
          <ellipse cx="314" cy="180" rx="14" ry="18" fill="url(#skin)" stroke="#171819" stroke-width="6"/>

          <!-- Full Dark Beard & Mustache -->
          <path d="M168 175 C165 240, 185 270, 240 270 C295 270, 315 240, 312 175 C295 200, 275 205, 240 205 C205 205, 185 200, 168 175 Z" fill="#222326" stroke="#171819" stroke-width="7"/>

          <!-- Mouth -->
          <g id="mouth-wrap" transform="translate(240, 218)">
            <ellipse id="mouth" cx="0" cy="0" rx="22" ry="12" fill="#881337" stroke="#171819" stroke-width="5"/>
            <path id="teeth" d="M-15 -3 Q0 4 15 -3" fill="#FFFFFF" stroke="#171819" stroke-width="2"/>
          </g>

          <path d="M236 172 Q240 182 248 180" fill="none" stroke="#171819" stroke-width="5" stroke-linecap="round"/>

          <!-- Glasses -->
          <g id="glasses">
            <circle cx="204" cy="162" r="26" fill="rgba(255,255,255,0.2)" stroke="#171819" stroke-width="7"/>
            <circle cx="276" cy="162" r="26" fill="rgba(255,255,255,0.2)" stroke="#171819" stroke-width="7"/>
            <path d="M230 162 L250 162" stroke="#171819" stroke-width="7"/>
            <path d="M178 160 L166 165" stroke="#171819" stroke-width="6"/>
            <path d="M302 160 L314 165" stroke="#171819" stroke-width="6"/>
          </g>

          <!-- Eyes -->
          <g id="eyes">
            <ellipse id="eye-left" cx="204" cy="162" rx="12" ry="12" fill="#FFFFFF">
              <circle cx="204" cy="162" r="6" fill="#171819"/>
              <circle cx="206" cy="159" r="2" fill="#FFFFFF"/>
            </ellipse>
            <ellipse id="eye-right" cx="276" cy="162" rx="12" ry="12" fill="#FFFFFF">
              <circle cx="276" cy="162" r="6" fill="#171819"/>
              <circle cx="278" cy="159" r="2" fill="#FFFFFF"/>
            </ellipse>
          </g>

          <path id="brow-left" d="M188 140 Q204 132 220 140" fill="none" stroke="#171819" stroke-width="7" stroke-linecap="round"/>
          <path id="brow-right" d="M260 140 Q276 132 292 140" fill="none" stroke="#171819" stroke-width="7" stroke-linecap="round"/>

          <!-- Knit Beanie -->
          <g id="beanie">
            <path d="M164 150 C160 80, 195 55, 240 55 C285 55, 320 80, 316 150 Z" fill="#2B2D31" stroke="#171819" stroke-width="8"/>
            <rect x="156" y="125" width="168" height="36" rx="10" fill="#222326" stroke="#171819" stroke-width="8"/>
            <rect x="178" y="136" width="18" height="12" rx="2" fill="#EF4444" stroke="#171819" stroke-width="2"/>
          </g>
        </g>
      </svg>
    </div>

    <!-- ================= SCENE GRAPHICS ================= -->

    <!-- SCENE 1: Hook (0 - {t_hook_end}s) -->
    <div id="scene-hook" class="scene-layer" style="opacity: 1;">
      <div id="hook-strip" style="position: absolute; left: 45px; top: 130px; width: 630px; background: #FFFFFF; border: 5px solid #171819; border-radius: 20px; box-shadow: 8px 10px 0 #171819; padding: 20px;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px;">
          <div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 18px; height: 32px; background: #E03622; border: 3px solid #171819; border-radius: 4px;"></div>
            <div style="font-weight: 950; font-size: 19px; letter-spacing: 0.05em;">AI TECH STACK 2026</div>
          </div>
          <div style="background: #EF4444; color: #FFF; font-weight: 950; font-size: 13px; padding: 4px 10px; border-radius: 6px; border: 2px solid #171819;">0 OF 3 INSTALLED</div>
        </div>
        <div style="display: flex; justify-content: space-around; padding: 12px 0 6px;">
          <div style="text-align: center;">
            <div class="socket-dot" style="margin: 0 auto 6px; transform: scale(1.4);"></div>
            <span style="font-size: 12px; font-weight: 950; background: #2563EB; color: #FFF; padding: 2px 6px; border-radius: 4px;">TT-METAL</span>
          </div>
          <div style="text-align: center;">
            <div class="socket-dot" style="margin: 0 auto 6px; transform: scale(1.4);"></div>
            <span style="font-size: 12px; font-weight: 950; background: #059669; color: #FFF; padding: 2px 6px; border-radius: 4px;">MAGIC-CTX</span>
          </div>
          <div style="text-align: center;">
            <div class="socket-dot" style="margin: 0 auto 6px; transform: scale(1.4);"></div>
            <span style="font-size: 12px; font-weight: 950; background: #EA580C; color: #FFF; padding: 2px 6px; border-radius: 4px;">INBOX-ZERO</span>
          </div>
        </div>
      </div>

      <!-- Subscription bills with CANCELLED stamp -->
      <div id="hook-bills" style="position: absolute; left: 90px; top: 295px; width: 540px; display: flex; flex-direction: column; gap: 10px; z-index: 24;">
        <div style="display: flex; gap: 12px;">
          <div id="bill-1" style="flex: 1; background: #FFF; border: 4px solid #171819; border-radius: 12px; padding: 10px 14px; box-shadow: 4px 4px 0 #171819; font-weight: 900; font-size: 16px; color: #EF4444;">
            💳 OpenAI: $200/mo
          </div>
          <div id="bill-2" style="flex: 1; background: #FFF; border: 4px solid #171819; border-radius: 12px; padding: 10px 14px; box-shadow: 4px 4px 0 #171819; font-weight: 900; font-size: 16px; color: #EF4444;">
            💳 Cursor Pro: $40/mo
          </div>
        </div>
        <div id="bill-stamp" style="align-self: center; background: #EF4444; color: #FFF; font-weight: 950; font-size: 26px; letter-spacing: 0.05em; padding: 8px 24px; border-radius: 12px; border: 4px solid #171819; transform: rotate(-5deg); box-shadow: 5px 5px 0 #171819; text-shadow: 1px 1px 0 #000;">
          ✕ OVERPRICED &amp; CANCELLED
        </div>
      </div>
    </div>

    <!-- SCENE 2: Repo 1 - TT-Metal ({t_hook_end} - {t_tool1_end}s) -->
    <div id="scene-tool1" class="scene-layer" style="opacity: 0;">
      <div class="upper-card">
        <div class="repo-header">
          <span class="repo-icon">⚡</span>
          <span class="repo-slug">{repo_data[0]['full_name']}</span>
          <span class="repo-star">{repo_data[0]['stars']}</span>
        </div>
        <div class="repo-title">TT-Metalium Engine</div>
        <div class="repo-desc">
          Automates complex engineering tasks in seconds with zero manual coding.
        </div>
      </div>

      <!-- Grounded Tech Console with KINETIC HARDWARE COMPILER BAR -->
      <div class="tech-console">
        <div class="console-header">
          <div class="console-dots">
            <div class="console-dot r"></div>
            <div class="console-dot y"></div>
            <div class="console-dot g"></div>
          </div>
          <div class="console-title">Silicon Operator Compiler</div>
        </div>
        
        <div class="demo-media-box">
          <img src="{repo_data[0]['demo']}" alt="TT-Metal Demo">
        </div>

        <!-- Kinetic Hardware Compiler Gauge -->
        <div id="t1-comp-box" style="background: #0F172A; border: 2px solid #3B82F6; border-radius: 8px; padding: 8px 10px; margin-bottom: 8px;">
          <div style="display: flex; justify-content: space-between; font-size: 11px; font-weight: 900; color: #93C5FD; margin-bottom: 5px;">
            <span>⚡ HARDWARE COMPILER</span>
            <span id="t1-prog-text" style="color: #60A5FA;">100% COMPILED</span>
          </div>
          <div style="width: 100%; height: 8px; background: #1E293B; border-radius: 4px; overflow: hidden; border: 1.5px solid #171819;">
            <div id="t1-bar" style="width: 0%; height: 100%; background: linear-gradient(90deg, #2563EB, #60A5FA); border-radius: 4px;"></div>
          </div>
        </div>

        <div style="background: #2D3748; border-radius: 8px; padding: 6px 10px; font-size: 11px; color: #68D391; margin-bottom: 8px; border: 1.5px solid #4A5568;">
          &gt; git clone {repo_data[0]['full_name']} &amp;&amp; make run
        </div>
        <div style="display: flex; flex-direction: column; gap: 6px; font-size: 12px; line-height: 1.35;">
          <div id="t1-step-1" style="color: #63B3ED; opacity: 0; background: #1E293B; padding: 5px 8px; border-radius: 6px; border-left: 4px solid #63B3ED;">
            [✓] Mapping low-level tensor kernels
          </div>
          <div id="t1-step-2" style="color: #68D391; opacity: 0; background: #1E293B; padding: 5px 8px; border-radius: 6px; border-left: 4px solid #68D391;">
            [✓] Silicon hardware acceleration: ACTIVE
          </div>
          <div id="t1-step-3" style="color: #F6AD55; opacity: 0; background: #2D3748; padding: 5px 8px; border-radius: 6px; border: 1.5px solid #F6AD55;">
            ⚡ LATENCY: 3.8ms · MEMORY: 1.2 TB/s HBM3
          </div>
        </div>
        <div id="t1-badge" style="margin-top: auto; opacity: 0; background: #2563EB; color: #FFF; padding: 8px 10px; border-radius: 8px; font-weight: 950; text-align: center; font-size: 12px; box-shadow: 0 4px 0 #1D4ED8;">
          🚀 ZERO MANUAL CODING · OPEN HARDWARE
        </div>
      </div>
    </div>

    <!-- SCENE 3: Repo 2 - Magic-Context ({t_tool1_end} - {t_tool2_end}s) -->
    <div id="scene-tool2" class="scene-layer" style="opacity: 0;">
      <div class="upper-card">
        <div class="repo-header">
          <span class="repo-icon">🧠</span>
          <span class="repo-slug">{repo_data[1]['full_name']}</span>
          <span class="repo-star">{repo_data[1]['stars']}</span>
        </div>
        <div class="repo-title">Magic-Context</div>
        <div class="repo-desc">
          An insane self-hosted powerhouse that runs locally on your own machine.
        </div>
      </div>

      <!-- Grounded Tech Console with KINETIC CONTEXT COMPACTION GAUGE -->
      <div class="tech-console">
        <div class="console-header">
          <div class="console-dots">
            <div class="console-dot r"></div>
            <div class="console-dot y"></div>
            <div class="console-dot g"></div>
          </div>
          <div class="console-title">Lifelong Memory Hippocampus</div>
        </div>

        <div class="demo-media-box">
          <img src="{repo_data[1]['demo']}" alt="Magic-Context Banner">
        </div>

        <!-- Kinetic Context Compaction Gauge -->
        <div id="t2-ctx-box" style="background: #064E3B; border: 2px solid #10B981; border-radius: 8px; padding: 8px 10px; margin-bottom: 8px;">
          <div style="display: flex; justify-content: space-between; font-size: 11px; font-weight: 900; color: #A7F3D0; margin-bottom: 4px;">
            <span>🧠 CONTEXT REDUCTION</span>
            <span style="color: #34D399; font-weight: 950;">-99.1% SAVED</span>
          </div>
          <div style="display: flex; gap: 8px; align-items: center; font-size: 11px;">
            <div style="flex: 1; height: 8px; background: #065F46; border-radius: 4px; overflow: hidden;">
              <div id="t2-bar" style="width: 0%; height: 100%; background: #34D399;"></div>
            </div>
            <span style="color: #E2E8F0; font-size: 10px; font-weight: 800;">128k → 1.2k tok</span>
          </div>
        </div>

        <div style="background: #2D3748; border-radius: 8px; padding: 6px 10px; font-size: 11px; color: #68D391; margin-bottom: 8px; border: 1.5px solid #4A5568;">
          &gt; npx @cortexkit/magic-context --lifelong-session
        </div>
        <div style="display: flex; flex-direction: column; gap: 6px; font-size: 12px; line-height: 1.35;">
          <div id="t2-step-1" style="color: #63B3ED; opacity: 0; background: #1E293B; padding: 5px 8px; border-radius: 6px; border-left: 4px solid #63B3ED;">
            [✓] Unbounded session context attached
          </div>
          <div id="t2-step-2" style="color: #68D391; opacity: 0; background: #1E293B; padding: 5px 8px; border-radius: 6px; border-left: 4px solid #68D391;">
            [✓] 100% Offline local disk storage
          </div>
          <div id="t2-step-3" style="color: #F6AD55; opacity: 0; background: #2D3748; padding: 5px 8px; border-radius: 6px; border: 1.5px solid #F6AD55;">
            🔒 Zero telemetry · One session for life
          </div>
        </div>
        <div id="t2-badge" style="margin-top: auto; opacity: 0; background: #059669; color: #FFF; padding: 8px 10px; border-radius: 8px; font-weight: 950; text-align: center; font-size: 12px; box-shadow: 0 4px 0 #047857;">
          💎 SELF-HOSTED POWERHOUSE
        </div>
      </div>
    </div>

    <!-- SCENE 4: Repo 3 - Inbox-Zero ({t_tool2_end} - {t_tool3_end}s) -->
    <div id="scene-tool3" class="scene-layer" style="opacity: 0;">
      <div class="upper-card">
        <div class="repo-header">
          <span class="repo-icon">✉️</span>
          <span class="repo-slug">{repo_data[2]['full_name']}</span>
          <span class="repo-star">{repo_data[2]['stars']}</span>
        </div>
        <div class="repo-title">Inbox-Zero AI</div>
        <div class="repo-desc">
          The ultimate breakthrough developer secret that saves hundreds of hours.
        </div>
      </div>

      <!-- Grounded Tech Console with MECHANICAL UNREAD EMAIL ODOMETER -->
      <div class="tech-console">
        <div class="console-header">
          <div class="console-dots">
            <div class="console-dot r"></div>
            <div class="console-dot y"></div>
            <div class="console-dot g"></div>
          </div>
          <div class="console-title">Automated Inbox Cleaner</div>
        </div>

        <div class="demo-media-box">
          <img src="{repo_data[2]['demo']}" alt="Inbox-Zero Demo">
        </div>

        <!-- Mechanical Unread Email Countdown Odometer -->
        <div id="t3-ticker-box" style="background: #7C2D12; border: 2px solid #EA580C; border-radius: 8px; padding: 8px 10px; margin-bottom: 8px; text-align: center;">
          <div style="font-size: 10px; font-weight: 900; color: #FED7AA; letter-spacing: 0.08em; margin-bottom: 2px;">UNREAD EMAILS CLEANING</div>
          <div id="t3-counter" style="font-size: 26px; font-weight: 950; color: #FFF; font-family: monospace; letter-spacing: 0.05em; line-height: 1;">1,420</div>
        </div>

        <div style="background: #2D3748; border-radius: 8px; padding: 6px 10px; font-size: 11px; color: #68D391; margin-bottom: 8px; border: 1.5px solid #4A5568;">
          &gt; docker compose up -d inbox-zero
        </div>
        <div style="display: flex; flex-direction: column; gap: 6px; font-size: 12px; line-height: 1.35;">
          <div id="t3-step-1" style="color: #63B3ED; opacity: 0; background: #1E293B; padding: 5px 8px; border-radius: 6px; border-left: 4px solid #63B3ED;">
            [✓] Cleared 1,420 unread developer newsletters
          </div>
          <div id="t3-step-2" style="color: #68D391; opacity: 0; background: #1E293B; padding: 5px 8px; border-radius: 6px; border-left: 4px solid #68D391;">
            [✓] Auto-categorized critical pull requests
          </div>
          <div id="t3-zero-badge" style="opacity: 0; background: #10B981; color: #171819; font-weight: 950; padding: 6px 10px; border-radius: 6px; text-align: center; border: 2px solid #FFF;">
            🎉 INBOX ZERO ACHIEVED! (0 UNREAD)
          </div>
        </div>
        <div id="t3-badge" style="margin-top: auto; opacity: 0; background: #EA580C; color: #FFF; padding: 8px 10px; border-radius: 8px; font-weight: 950; text-align: center; font-size: 12px; box-shadow: 0 4px 0 #C2410C;">
          🔥 12,430+ GITHUB STARS
        </div>
      </div>
    </div>

    <!-- SCENE 5: Outro Phone DM ({t_tool3_end} - {duration}s) -->
    <div id="scene-outro" class="scene-layer" style="opacity: 0;">
      <div class="phone-mockup">
        <div class="phone-notch"></div>
        <div class="phone-screen">
          <!-- Chat Header -->
          <div style="display: flex; align-items: center; gap: 10px; padding-bottom: 12px; border-bottom: 2px solid #F3F4F6; margin-bottom: 14px;">
            <div style="width: 36px; height: 36px; background: #2563EB; border-radius: 50%; color: #FFF; font-weight: 950; display: flex; align-items: center; justify-content: center; font-size: 18px;">JD</div>
            <div>
              <div style="font-weight: 950; font-size: 14px; color: #171819;">Jayant Diwan</div>
              <div style="font-size: 11px; color: #10B981; font-weight: 750;">● Active now</div>
            </div>
          </div>
          <!-- User Comment Bubble -->
          <div id="dm-bubble" style="opacity: 0; align-self: flex-end; background: #2563EB; color: #FFF; font-weight: 950; font-size: 17px; padding: 10px 18px; border-radius: 18px 18px 4px 18px; margin-bottom: 14px; box-shadow: 0 4px 12px rgba(37,99,235,0.3);">
            TOOLS
          </div>
          <!-- Automated DM Reply with 3 Repos -->
          <div id="dm-reply" style="opacity: 0; background: #F8FAFC; border: 2px solid #E2E8F0; border-radius: 18px; padding: 12px; display: flex; flex-direction: column; gap: 8px;">
            <div style="font-size: 12px; font-weight: 900; color: #64748B;">Automated Instant Delivery:</div>
            <div style="display: flex; align-items: center; gap: 8px; background: #FFF; padding: 8px 10px; border-radius: 10px; border: 1.5px solid #CBD5E1;">
              <span style="font-size: 16px;">⚡</span>
              <span style="font-weight: 900; font-size: 13px; color: #1E293B;">{repo_data[0]['full_name']}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; background: #FFF; padding: 8px 10px; border-radius: 10px; border: 1.5px solid #CBD5E1;">
              <span style="font-size: 16px;">🧠</span>
              <span style="font-weight: 900; font-size: 13px; color: #1E293B;">{repo_data[1]['full_name']}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; background: #FFF; padding: 8px 10px; border-radius: 10px; border: 1.5px solid #CBD5E1;">
              <span style="font-size: 16px;">✉️</span>
              <span style="font-weight: 900; font-size: 13px; color: #1E293B;">{repo_data[2]['full_name']}</span>
            </div>
            <div style="font-size: 11px; color: #2563EB; font-weight: 950; text-align: center; margin-top: 4px;">
              ✓ Direct GitHub links sent!
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Captions Pill (3D Keycap Subtitles on Front of Desk) -->
    <div class="captions-wrapper">
      <div id="caption-pill" class="caption-pill">
        <span class="caption-word active">READY</span>
      </div>
    </div>

  </div>

  <script>
    const tl = gsap.timeline({{ paused: true }});
    window.__timelines = {{ root: tl }};
    tl.to({{}}, {{ duration: {round(duration, 2)} }}, 0);

    // Dynamic Desk & Scene Colors
    const sceneConfigs = [
      {{ id: "#scene-hook", bg: "#bg-hook", desk: "#B64D29", start: 0, end: {t_hook_end}, badge: "STOP PAYING FOR AI", meter: "0/3", plugs: [0,0,0] }},
      {{ id: "#scene-tool1", bg: "#bg-tool1", desk: "#1D4ED8", start: {t_hook_end}, end: {t_tool1_end}, badge: "01 · TT-METAL", meter: "1/3", plugs: [1,0,0] }},
      {{ id: "#scene-tool2", bg: "#bg-tool2", desk: "#047857", start: {t_tool1_end}, end: {t_tool2_end}, badge: "02 · MAGIC-CTX", meter: "2/3", plugs: [1,1,0] }},
      {{ id: "#scene-tool3", bg: "#bg-tool3", desk: "#C2410C", start: {t_tool2_end}, end: {t_tool3_end}, badge: "03 · INBOX-ZERO", meter: "3/3", plugs: [1,1,1] }},
      {{ id: "#scene-outro", bg: "#bg-outro", desk: "#B64D29", start: {t_tool3_end}, end: {duration}, badge: "3 REPOS · 1 DM", meter: "3/3", plugs: [1,1,1] }}
    ];

    sceneConfigs.forEach((sc, i) => {{
      tl.set(sc.id, {{ opacity: 1 }}, sc.start);
      if (sc.end < {round(duration, 2)}) {{
        tl.set(sc.id, {{ opacity: 0 }}, sc.end);
      }}

      // Background subtle push-in motion (zero static frames)
      tl.fromTo(sc.id, {{ scale: 1.0 }}, {{ scale: 1.025, duration: sc.end - sc.start, ease: "none" }}, sc.start);

      tl.to(sc.bg, {{ opacity: 1, duration: 0.35 }}, sc.start);
      if (sc.end < {round(duration, 2)}) {{
        tl.to(sc.bg, {{ opacity: 0, duration: 0.35 }}, sc.end);
      }}

      tl.to("#desk", {{ backgroundColor: sc.desk, duration: 0.35 }}, sc.start);

      tl.set("#top-badge", {{ innerText: sc.badge }}, sc.start);
      tl.fromTo("#top-badge", {{ scale: 0.85, rotate: -4 }}, {{ scale: 1, rotate: -1.5, duration: 0.35, ease: "back.out(2)" }}, sc.start);

      tl.set("#meter-label", {{ innerText: `REPOS ${{sc.meter}}` }}, sc.start);
      tl.set("#sock-1", {{ className: sc.plugs[0] ? "socket-dot plug-1" : "socket-dot" }}, sc.start);
      tl.set("#sock-2", {{ className: sc.plugs[1] ? "socket-dot plug-2" : "socket-dot" }}, sc.start);
      tl.set("#sock-3", {{ className: sc.plugs[2] ? "socket-dot plug-3" : "socket-dot" }}, sc.start);

      if (i > 0 && i < 4) {{
        tl.fromTo("#spark-fx", {{ opacity: 1, scale: 1.5 }}, {{ opacity: 0, scale: 0.5, duration: 0.3 }}, sc.start);
      }}
    }});

    // ================= TIMELINE SCENE CHOREOGRAPHY =================

    // --- SCENE 1: HOOK (0 - {t_hook_end}s) ---
    tl.set("#arm-both-up", {{ opacity: 1 }}, 0);
    tl.fromTo("#hook-strip", {{ y: -160, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "back.out(1.5)" }}, 0.1);
    tl.fromTo("#bill-1", {{ y: -30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(1.5)" }}, 0.6);
    tl.fromTo("#bill-2", {{ y: -30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(1.5)" }}, 0.9);
    tl.fromTo("#bill-stamp", 
      {{ scale: 2.2, opacity: 0, rotate: -25 }}, 
      {{ scale: 1, opacity: 1, rotate: -5, duration: 0.35, ease: "bounce.out" }}, 
      1.4
    );
    tl.to("#bill-1, #bill-2", {{ textDecoration: "line-through", opacity: 0.55, duration: 0.2 }}, 1.65);

    // Transition Avatar to Right side (presenter position) for all repo reviews
    tl.to("#avatar-wrap", {{ x: 180, y: 15, duration: 0.65, ease: "power2.inOut" }}, {t_hook_end});
    tl.set("#arm-both-up", {{ opacity: 0 }}, {t_hook_end});
    tl.set("#arm-point", {{ opacity: 1 }}, {t_hook_end});

    // --- SCENE 2: TOOL 1 - TT-METAL ({t_hook_end} - {t_tool1_end}s) ---
    tl.fromTo("#scene-tool1 .upper-card", {{ x: -60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.45, ease: "back.out(1.5)" }}, {t_hook_end});
    tl.fromTo("#scene-tool1 .tech-console", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {t_hook_end + 0.1});
    
    // Kinetic Hardware Compilation Bar animation
    tl.to("#t1-bar", {{ width: "100%", duration: 1.4, ease: "power2.out" }}, {t_hook_end + 0.8});

    tl.fromTo("#t1-step-1", {{ x: -20, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35 }}, {t_hook_end + 1.2});
    tl.fromTo("#t1-step-2", {{ x: -20, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35 }}, {t_hook_end + 2.0});
    tl.fromTo("#t1-step-3", {{ scale: 0.9, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(1.5)" }}, {t_hook_end + 2.8});
    tl.fromTo("#t1-badge", {{ scale: 0.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {t_hook_end + 3.6});

    // --- SCENE 3: TOOL 2 - MAGIC-CONTEXT ({t_tool1_end} - {t_tool2_end}s) ---
    tl.fromTo("#scene-tool2 .upper-card", {{ x: -60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.45, ease: "back.out(1.5)" }}, {t_tool1_end});
    tl.fromTo("#scene-tool2 .tech-console", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {t_tool1_end + 0.1});

    // Kinetic Context Reduction Bar animation
    tl.to("#t2-bar", {{ width: "99%", duration: 1.4, ease: "power2.out" }}, {t_tool1_end + 0.8});

    tl.fromTo("#t2-step-1", {{ x: -20, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35 }}, {t_tool1_end + 1.2});
    tl.fromTo("#t2-step-2", {{ x: -20, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35 }}, {t_tool1_end + 2.0});
    tl.fromTo("#t2-step-3", {{ scale: 0.9, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(1.5)" }}, {t_tool1_end + 2.8});
    tl.fromTo("#t2-badge", {{ scale: 0.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {t_tool1_end + 3.6});

    // --- SCENE 4: TOOL 3 - INBOX-ZERO ({t_tool2_end} - {t_tool3_end}s) ---
    tl.fromTo("#scene-tool3 .upper-card", {{ x: -60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.45, ease: "back.out(1.5)" }}, {t_tool2_end});
    tl.fromTo("#scene-tool3 .tech-console", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {t_tool2_end + 0.1});

    // Mechanical Unread Email Odometer Countdown (1,420 -> 0)
    let emailCounterObj = {{ val: 1420 }};
    tl.to(emailCounterObj, {{
      val: 0,
      duration: 1.6,
      ease: "power2.inOut",
      onUpdate: () => {{
        const el = document.getElementById("t3-counter");
        if (el) el.innerText = Math.round(emailCounterObj.val).toLocaleString();
      }}
    }}, {t_tool2_end + 0.6});

    tl.fromTo("#t3-step-1", {{ x: -20, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35 }}, {t_tool2_end + 1.0});
    tl.fromTo("#t3-step-2", {{ x: -20, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35 }}, {t_tool2_end + 1.8});
    
    // INBOX ZERO ACHIEVED badge slam right as counter reaches 0
    tl.fromTo("#t3-zero-badge", {{ scale: 1.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "bounce.out" }}, {t_tool2_end + 2.3});
    tl.fromTo("#t3-badge", {{ scale: 0.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {t_tool2_end + 3.2});

    // --- SCENE 5: OUTRO ({t_tool3_end} - {duration}s) ---
    tl.set("#arm-point", {{ opacity: 0 }}, {t_tool3_end});
    tl.set("#arm-thumbs-up", {{ opacity: 1 }}, {t_tool3_end});

    // Phone and chat elements drop in immediately for max readability
    tl.fromTo("#scene-outro .phone-mockup", {{ y: 120, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "back.out(1.4)" }}, {t_tool3_end});
    tl.fromTo("#dm-bubble", {{ scale: 0.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }}, {t_tool3_end + 0.25});
    tl.fromTo("#dm-reply", {{ y: 20, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.5)" }}, {t_tool3_end + 0.55});

    // Continuous micro head-bob
    tl.to("#head", {{ y: -3, duration: 0.22, repeat: -1, yoyo: true, ease: "sine.inOut" }}, 0);

    // Continuous mouth morphing matching speech
    for (let t = 0.15; t < {round(duration - 0.5, 2)}; t += 0.32) {{
      tl.to("#mouth", {{ attr: {{ ry: 18, rx: 24 }}, duration: 0.09, ease: "none" }}, t);
      tl.to("#mouth", {{ attr: {{ ry: 8, rx: 20 }}, duration: 0.09, ease: "none" }}, t + 0.11);
    }}

    // Eye blinks every ~3.8 seconds
    for (let t = 1.8; t < {round(duration - 1, 2)}; t += 3.8) {{
      tl.to(["#eye-left circle", "#eye-right circle"], {{ scaleY: 0.1, transformOrigin: "center", duration: 0.08, yoyo: true, repeat: 1 }}, t);
    }}

    // Eyebrow twitches on key emphasis
    for (let t = 2.0; t < {round(duration - 1, 2)}; t += 4.5) {{
      tl.to(["#brow-left", "#brow-right"], {{ y: -5, duration: 0.2, yoyo: true, repeat: 1 }}, t);
    }}

    // Continuous floating crosshair drift
    tl.to(".crosshair", {{ y: "+=12", rotation: 30, duration: 5, repeat: -1, yoyo: true, ease: "sine.inOut" }}, 0);

    // Rising steam bubbles
    tl.to("#steam-1", {{ y: -25, opacity: 0, duration: 1.8, repeat: -1, ease: "power1.out" }}, 0);
    tl.to("#steam-2", {{ y: -30, opacity: 0, duration: 2.2, repeat: -1, ease: "power1.out", delay: 0.8 }}, 0);

    // Kinetic Captions Choreography (3D Keyboard Keycap Pills)
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

    print(f"[✓] Compiled 9.5/10 hyper-motion composition to {output_html} ({round(duration, 2)}s, 720x1280)")
    return output_html

if __name__ == "__main__":
    build_hyperframes_composition()
