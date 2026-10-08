import json
import os

def build_hyperframes_composition(repos_file="assets/curated_repos.json", captions_file="assets/caption_chunks.json", audio_path="assets/voice.mp3", output_html="index.html"):
    """
    Assembles the complete grounded hyper-motion HyperFrames composition incorporating real scraped media assets.
    """
    with open(repos_file) as f:
        repos = json.load(f)
        
    with open(captions_file) as f:
        caption_chunks = json.load(f)

    # Repo color themes
    themes = [
        {"bg": "bg-browser", "desk": "#1D4ED8", "badge": "01 · " + repos[0]["name"].upper(), "sock": [1,0,0,0,0]},
        {"bg": "bg-ollama", "desk": "#047857", "badge": "02 · " + repos[1]["name"].upper(), "sock": [1,1,0,0,0]},
        {"bg": "bg-firecrawl", "desk": "#C2410C", "badge": "03 · " + repos[2]["name"].upper(), "sock": [1,1,1,0,0]},
        {"bg": "bg-cline", "desk": "#6D28D9", "badge": "04 · " + repos[3]["name"].upper(), "sock": [1,1,1,1,0]},
        {"bg": "bg-hyperframes", "desk": "#854D0E", "badge": "05 · " + repos[4]["name"].upper(), "sock": [1,1,1,1,1]},
    ]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=720, height=1280">
  <title>Autonomous Daily AI Developer Reel</title>
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
    .bg-browser {{
      background-color: #E0F2FE;
      background-image: radial-gradient(#93C5FD 2.4px, transparent 2.4px), radial-gradient(#93C5FD 2.4px, transparent 2.4px);
      background-size: 24px 24px;
      background-position: 0 0, 12px 12px;
    }}
    .bg-ollama {{
      background-color: #ECFDF5;
      background-image: radial-gradient(#6EE7B7 2.4px, transparent 2.4px), radial-gradient(#6EE7B7 2.4px, transparent 2.4px);
      background-size: 24px 24px;
      background-position: 0 0, 12px 12px;
    }}
    .bg-firecrawl {{
      background-color: #FEF3C7;
      background-image: radial-gradient(#FCD34D 2.4px, transparent 2.4px), radial-gradient(#FCD34D 2.4px, transparent 2.4px);
      background-size: 24px 24px;
      background-position: 0 0, 12px 12px;
    }}
    .bg-cline {{
      background-color: #EDE9FE;
      background-image: radial-gradient(#C4B5FD 2.4px, transparent 2.4px), radial-gradient(#C4B5FD 2.4px, transparent 2.4px);
      background-size: 24px 24px;
      background-position: 0 0, 12px 12px;
    }}
    .bg-hyperframes {{
      background-color: #FEF08A;
      background-image: radial-gradient(#F59E0B 2.4px, transparent 2.4px), radial-gradient(#F59E0B 2.4px, transparent 2.4px);
      background-size: 24px 24px;
      background-position: 0 0, 12px 12px;
    }}
    .bg-outro {{
      background-color: #F4EEDF;
      background-image: radial-gradient(#C8BFAD 2.4px, transparent 2.4px), radial-gradient(#C8BFAD 2.4px, transparent 2.4px);
      background-size: 24px 24px;
      background-position: 0 0, 12px 12px;
    }}

    .crosshair {{
      position: absolute;
      font-family: monospace;
      font-size: 22px;
      font-weight: 900;
      color: rgba(23, 24, 25, 0.28);
      pointer-events: none;
      z-index: 2;
    }}

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
    .meter-strip {{ display: flex; align-items: center; gap: 8px; }}
    .meter-switch {{ width: 16px; height: 26px; background: #E03622; border: 3px solid #171819; border-radius: 4px; }}
    .meter-sockets {{ display: flex; gap: 6px; position: relative; }}
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
    .socket-dot.plug-4 {{ background: #7C3AED; box-shadow: 0 0 12px #7C3AED; }}
    .socket-dot.plug-5 {{ background: #EAB308; box-shadow: 0 0 16px #EAB308; }}

    .meter-label {{ font-size: 11px; font-weight: 950; letter-spacing: 0.12em; color: #171819; }}

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
    .desk-drawer {{ position: absolute; top: 36px; left: 100px; width: 140px; height: 26px; background: #171819; border-radius: 13px; border: 3px solid rgba(255,255,255,0.25); }}
    .desk-drawer-right {{ position: absolute; top: 36px; right: 100px; width: 140px; height: 26px; background: #171819; border-radius: 13px; border: 3px solid rgba(255,255,255,0.25); }}

    .desk-mug {{ position: absolute; right: 48px; bottom: 390px; width: 46px; height: 52px; background: #FFFFFF; border: 4px solid #171819; border-radius: 4px 4px 10px 10px; z-index: 25; }}
    .desk-mug::before {{ content: ""; position: absolute; top: 14px; left: 0; right: 0; height: 9px; background: #2563EB; }}
    .desk-mug::after {{ content: ""; position: absolute; right: -16px; top: 12px; width: 14px; height: 24px; border: 4px solid #171819; border-radius: 0 10px 10px 0; }}
    .steam-bubble {{ position: absolute; right: 64px; bottom: 450px; font-size: 18px; color: rgba(23, 24, 25, 0.4); z-index: 25; font-weight: 900; }}

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
    .avatar-svg {{ width: 100%; height: 100%; overflow: visible; }}

    .scene-layer {{ position: absolute; inset: 0; z-index: 15; pointer-events: none; }}

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
    .repo-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }}
    .repo-slug {{ font-weight: 950; font-size: 19px; letter-spacing: -0.01em; }}
    .repo-star {{ margin-left: auto; background: #FEF08A; border: 2px solid #171819; border-radius: 6px; padding: 2px 8px; font-weight: 950; font-size: 14px; box-shadow: 2px 2px 0 #171819; }}
    .repo-title {{ font-size: 24px; font-weight: 950; margin-bottom: 4px; }}
    .repo-desc {{ font-size: 15px; color: #4B5563; font-weight: 750; line-height: 1.35; }}

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

    /* Real Image / Video Container inside Console */
    .media-card {{
      width: 100%;
      border-radius: 10px;
      overflow: hidden;
      border: 2px solid #374151;
      margin-bottom: 12px;
      background: #000;
    }}
    .media-card img {{
      width: 100%;
      height: auto;
      display: block;
      object-fit: cover;
    }}

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
    .caption-word {{ font-size: 38px; font-weight: 950; color: #FFFFFF; letter-spacing: -0.02em; line-height: 1; }}
    .caption-word.active {{ background: #FACC15; color: #171819; padding: 4px 16px; border-radius: 12px; box-shadow: 2px 2px 0 #000000; }}

    .phone-mockup {{
      position: absolute;
      left: 45px;
      top: 175px;
      width: 375px;
      height: 715px;
      background: #000000;
      border: 9px solid #171819;
      border-radius: 50px;
      box-shadow: 12px 16px 0 rgba(0,0,0,0.3);
      z-index: 35;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}
    .phone-notch {{ width: 130px; height: 26px; background: #171819; margin: 0 auto; border-radius: 0 0 16px 16px; }}
    .phone-screen {{ flex: 1; background: #FFFFFF; padding: 18px 16px; font-family: -apple-system, sans-serif; overflow: hidden; display: flex; flex-direction: column; }}
  </style>
</head>
<body>
  <div id="root" data-composition-id="root" data-start="0" data-duration="60.9" data-width="720" data-height="1280">
    <div id="bg-hook" class="bg-layer bg-hook"></div>
    <div id="bg-browser" class="bg-layer bg-browser"></div>
    <div id="bg-ollama" class="bg-layer bg-ollama"></div>
    <div id="bg-firecrawl" class="bg-layer bg-firecrawl"></div>
    <div id="bg-cline" class="bg-layer bg-cline"></div>
    <div id="bg-hyperframes" class="bg-layer bg-hyperframes"></div>
    <div id="bg-outro" class="bg-layer bg-outro"></div>

    <audio id="voice" src="{audio_path}" data-start="0" data-duration="60.9" data-volume="1"></audio>

    <div id="top-badge" class="top-badge" style="opacity: 0;">TOP 5 AI DEV REPOS</div>
    <div id="top-meter" class="top-meter" style="opacity: 0;">
      <div class="meter-strip">
        <div class="meter-switch"></div>
        <div class="meter-sockets">
          <div id="sock-1" class="socket-dot"></div>
          <div id="sock-2" class="socket-dot"></div>
          <div id="sock-3" class="socket-dot"></div>
          <div id="sock-4" class="socket-dot"></div>
          <div id="sock-5" class="socket-dot"></div>
        </div>
      </div>
      <div id="meter-label" class="meter-label">REPOS 0/5</div>
    </div>

    <div id="desk" class="desk">
      <div class="desk-drawer"></div>
      <div class="desk-drawer-right"></div>
      <div class="desk-mug"></div>
      <div id="steam-1" class="steam-bubble">~</div>
    </div>

    <!-- Avatar Character Rig -->
    <div id="avatar-wrap" class="avatar-wrapper">
      <svg class="avatar-svg" viewBox="0 0 480 460" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="skin" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#FCE1CA"/>
            <stop offset="100%" stop-color="#F2BA91"/>
          </linearGradient>
        </defs>
        <g id="torso">
          <path d="M130 330 C130 310, 180 295, 240 295 C300 295, 350 310, 350 330 L380 460 L100 460 Z" fill="#756D65" stroke="#171819" stroke-width="8"/>
          <path d="M210 295 C210 330, 270 330, 270 295 Z" fill="#FFFFFF" stroke="#171819" stroke-width="6"/>
        </g>
        <g id="arm-left">
          <g id="arm-point" opacity="0">
            <path d="M340 330 C380 320, 390 260, 375 220" fill="none" stroke="#171819" stroke-width="44" stroke-linecap="round"/>
            <path d="M340 330 C380 320, 390 260, 375 220" fill="none" stroke="#756D65" stroke-width="36" stroke-linecap="round"/>
            <g transform="translate(365, 170)">
              <ellipse cx="14" cy="40" rx="18" ry="16" fill="url(#skin)" stroke="#171819" stroke-width="6"/>
              <rect x="8" y="0" width="12" height="32" rx="6" fill="url(#skin)" stroke="#171819" stroke-width="6"/>
            </g>
          </g>
          <g id="arm-both-up" opacity="1">
            <path d="M140 330 C100 290, 90 220, 110 170" fill="none" stroke="#171819" stroke-width="44" stroke-linecap="round"/>
            <path d="M140 330 C100 290, 90 220, 110 170" fill="none" stroke="#756D65" stroke-width="36" stroke-linecap="round"/>
            <path d="M340 330 C380 290, 390 220, 370 170" fill="none" stroke="#171819" stroke-width="44" stroke-linecap="round"/>
            <path d="M340 330 C380 290, 390 220, 370 170" fill="none" stroke="#756D65" stroke-width="36" stroke-linecap="round"/>
          </g>
          <g id="arm-thumbs-up" opacity="0">
            <path d="M340 330 C370 320, 380 280, 360 240" fill="none" stroke="#171819" stroke-width="44" stroke-linecap="round"/>
            <path d="M340 330 C370 320, 380 280, 360 240" fill="none" stroke="#756D65" stroke-width="36" stroke-linecap="round"/>
            <g transform="translate(350, 200)">
              <circle cx="20" cy="30" r="16" fill="url(#skin)" stroke="#171819" stroke-width="6"/>
              <rect x="14" y="6" width="12" height="20" rx="5" fill="url(#skin)" stroke="#171819" stroke-width="5"/>
            </g>
          </g>
        </g>
        <g id="head">
          <rect x="216" y="240" width="48" height="55" fill="url(#skin)" stroke="#171819" stroke-width="7"/>
          <ellipse cx="240" cy="180" rx="72" ry="80" fill="url(#skin)" stroke="#171819" stroke-width="8"/>
          <path d="M168 175 C165 240, 185 270, 240 270 C295 270, 315 240, 312 175 C295 200, 275 205, 240 205 C205 205, 185 200, 168 175 Z" fill="#222326" stroke="#171819" stroke-width="7"/>
          <g id="mouth-wrap" transform="translate(240, 218)">
            <ellipse id="mouth" cx="0" cy="0" rx="22" ry="12" fill="#881337" stroke="#171819" stroke-width="5"/>
          </g>
          <g id="glasses">
            <circle cx="204" cy="162" r="26" fill="rgba(255,255,255,0.2)" stroke="#171819" stroke-width="7"/>
            <circle cx="276" cy="162" r="26" fill="rgba(255,255,255,0.2)" stroke="#171819" stroke-width="7"/>
            <path d="M230 162 L250 162" stroke="#171819" stroke-width="7"/>
          </g>
          <g id="eyes">
            <ellipse id="eye-left" cx="204" cy="162" rx="12" ry="12" fill="#FFFFFF"><circle cx="204" cy="162" r="6" fill="#171819"/></ellipse>
            <ellipse id="eye-right" cx="276" cy="162" rx="12" ry="12" fill="#FFFFFF"><circle cx="276" cy="162" r="6" fill="#171819"/></ellipse>
            <path id="eye-wink" d="M264 162 Q276 172 288 162" fill="none" stroke="#171819" stroke-width="6" stroke-linecap="round" opacity="0"/>
          </g>
          <g id="beanie">
            <path d="M164 150 C160 80, 195 55, 240 55 C285 55, 320 80, 316 150 Z" fill="#2B2D31" stroke="#171819" stroke-width="8"/>
            <rect x="156" y="125" width="168" height="36" rx="10" fill="#222326" stroke="#171819" stroke-width="8"/>
          </g>
        </g>
      </svg>
    </div>

    <!-- SCENE 1: Hook -->
    <div id="scene-hook" class="scene-layer" style="opacity: 1;">
      <div id="hook-strip" style="position: absolute; top: 180px; left: 45px; width: 630px; background: #FFFFFF; border: 6px solid #171819; border-radius: 24px; box-shadow: 8px 10px 0 #171819; padding: 16px 20px 20px; display: flex; flex-direction: column; gap: 14px; z-index: 28;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
          <div style="font-size: 21px; font-weight: 950; letter-spacing: 0.08em; color: #171819;">AI TECH STACK 2026</div>
          <div style="background: #EF4444; color: #FFF; font-weight: 950; font-size: 15px; padding: 4px 14px; border-radius: 6px; border: 2px solid #171819;">0 OF 5 INSTALLED</div>
        </div>
      </div>
      <div id="hook-banner" style="position: absolute; left: 45px; top: 270px; width: 630px; opacity: 0; background: #FEF08A; border: 6px solid #171819; border-radius: 20px; box-shadow: 8px 12px 0 #171819; padding: 22px; text-align: center; z-index: 30;">
        <div style="font-size: 38px; font-weight: 950; margin-bottom: 6px;">5 INSANE AI REPOS</div>
        <div style="font-size: 19px; font-weight: 850; color: #374151;">Every Developer Needs Right Now</div>
      </div>
    </div>

    <!-- SCENES 2 to 6: The 5 Repos with Real Media -->
    """

    # Dynamically inject each of the 5 curated repos with their actual scraped media assets
    scene_ids = ["#scene-browser", "#scene-ollama", "#scene-firecrawl", "#scene-cline", "#scene-hyperframes"]
    bg_ids = ["#bg-browser", "#bg-ollama", "#bg-firecrawl", "#bg-cline", "#bg-hyperframes"]
    
    for i, repo in enumerate(repos[:5]):
        sc_id = scene_ids[i].replace("#", "")
        media_img = repo.get("demo_media") or repo.get("og_image") or "assets/repos/default_banner.png"
        
        html += f"""
    <div id="{sc_id}" class="scene-layer" style="opacity: 0;">
      <div class="upper-card">
        <div class="repo-header">
          <span class="repo-slug">{repo["full_name"]}</span>
          <span class="repo-star">★ {repo["stars"]:,}</span>
        </div>
        <div class="repo-title">{repo["name"]}</div>
        <div class="repo-desc">{repo["description"]}</div>
      </div>
      <div class="tech-console">
        <div class="console-header">
          <div class="console-dots"><div class="console-dot r"></div><div class="console-dot y"></div><div class="console-dot g"></div></div>
          <div class="console-title">{repo["language"]} · Live Repository Demo</div>
        </div>
        <div class="media-card">
          <img src="{media_img}" alt="{repo['name']} demo">
        </div>
        <div style="background: #111827; border: 1px solid #374151; border-radius: 8px; padding: 12px; margin-top: auto;">
          <div style="font-size: 12px; color: #10B981; font-weight: 900;">✓ VERIFIED OPEN SOURCE</div>
          <div style="font-size: 14px; color: #F3F4F6; font-weight: 800; margin-top: 4px;">Language: {repo["language"]}</div>
        </div>
      </div>
    </div>
"""

    html += f"""
    <!-- SCENE 7: Outro -->
    <div id="scene-outro" class="scene-layer" style="opacity: 0; z-index: 35;">
      <div class="phone-mockup">
        <div class="phone-notch"></div>
        <div class="phone-screen">
          <div style="font-weight: 900; font-size: 16px; margin-bottom: 12px;">Jayant Digital Studio</div>
          <div style="background: #2563EB; color: #FFF; padding: 10px 18px; border-radius: 18px 18px 4px 18px; margin-left: auto; max-width: 75%; font-weight: 900; margin-bottom: 14px;">REPOS</div>
          <div style="background: #F3F4F6; border: 3px solid #171819; border-radius: 16px; padding: 14px;">
            <div style="font-weight: 950; font-size: 15px; margin-bottom: 8px;">Here are all 5 links:</div>
            <div style="font-size: 13px; font-weight: 850; line-height: 1.6;">
              <div>1. <b>{repos[0]['name']}</b></div>
              <div>2. <b>{repos[1]['name']}</b></div>
              <div>3. <b>{repos[2]['name']}</b></div>
              <div>4. <b>{repos[3]['name']}</b></div>
              <div>5. <b>{repos[4]['name']}</b></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Word Captions -->
    <div class="captions-wrapper">
      <div id="caption-pill" class="caption-pill">
        <span class="caption-word active">Stop</span>
        <span class="caption-word">paying</span>
      </div>
    </div>
  </div>

  <script>
    const tl = gsap.timeline({{ paused: true }});
    window.__timelines = {{ root: tl }};
    tl.to({{}}, {{ duration: 60.9 }}, 0);

    const scenes = [
      {{ id: "#scene-hook", bg: "#bg-hook", desk: "#B64D29", start: 0, end: 7.05, badge: "AI DEV REPOS", meter: "0/5" }},
      {{ id: "#scene-browser", bg: "#bg-browser", desk: "#1D4ED8", start: 7.05, end: 17.09, badge: "01 · {repos[0]['name'].upper()}", meter: "1/5" }},
      {{ id: "#scene-ollama", bg: "#bg-ollama", desk: "#047857", start: 17.09, end: 26.00, badge: "02 · {repos[1]['name'].upper()}", meter: "2/5" }},
      {{ id: "#scene-firecrawl", bg: "#bg-firecrawl", desk: "#C2410C", start: 26.00, end: 36.31, badge: "03 · {repos[2]['name'].upper()}", meter: "3/5" }},
      {{ id: "#scene-cline", bg: "#bg-cline", desk: "#6D28D9", start: 36.31, end: 44.60, badge: "04 · {repos[3]['name'].upper()}", meter: "4/5" }},
      {{ id: "#scene-hyperframes", bg: "#bg-hyperframes", desk: "#854D0E", start: 44.60, end: 55.91, badge: "05 · {repos[4]['name'].upper()}", meter: "5/5" }},
      {{ id: "#scene-outro", bg: "#bg-outro", desk: "#B64D29", start: 55.91, end: 60.90, badge: "5 REPOS · 1 DM", meter: "5/5" }}
    ];

    scenes.forEach((sc, i) => {{
      tl.set(sc.id, {{ opacity: 1 }}, sc.start);
      if (sc.end < 60.9) tl.set(sc.id, {{ opacity: 0 }}, sc.end);
      tl.to(sc.bg, {{ opacity: 1, duration: 0.35 }}, sc.start);
      if (sc.end < 60.9) tl.to(sc.bg, {{ opacity: 0, duration: 0.35 }}, sc.end);
      tl.to("#desk", {{ backgroundColor: sc.desk, duration: 0.35 }}, sc.start);
      if (sc.start >= 2.85) {{
        tl.set("#top-badge", {{ opacity: 1 }}, 2.85);
        tl.set("#top-meter", {{ opacity: 1 }}, 2.85);
      }}
      tl.set("#top-badge", {{ innerText: sc.badge }}, sc.start);
      tl.set("#meter-label", {{ innerText: `REPOS ${{sc.meter}}` }}, sc.start);
    }});

    // Avatar movement
    tl.to("#avatar-wrap", {{ x: 180, duration: 0.65, ease: "power2.inOut" }}, 6.7);
    tl.set("#arm-both-up", {{ opacity: 0 }}, 6.8);
    tl.set("#arm-point", {{ opacity: 1 }}, 6.8);
    tl.set("#arm-point", {{ opacity: 0 }}, 56.8);
    tl.set("#arm-thumbs-up", {{ opacity: 1 }}, 56.8);
    tl.set("#eye-right", {{ opacity: 0 }}, 57.2);
    tl.set("#eye-wink", {{ opacity: 1 }}, 57.2);

    // Continuous avatar face motion
    for (let t = 1.5; t < 59; t += 3.2) {{
      tl.to(["#eye-left", "#eye-right"], {{ scaleY: 0.1, duration: 0.08, transformOrigin: "50% 50%", yoyo: true, repeat: 1 }}, t);
    }}
    for (let t = 0.15; t < 59; t += 0.32) {{
      tl.to("#mouth", {{ attr: {{ ry: 18, rx: 24 }}, duration: 0.09, ease: "none" }}, t);
      tl.to("#mouth", {{ attr: {{ ry: 8, rx: 20 }}, duration: 0.09, ease: "none" }}, t + 0.11);
    }}

    // Synchronized kinetic captions
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
    print(f"[✓] Generated complete dynamic HyperFrames composition incorporating real scraped media at {output_html}")
    return output_html

if __name__ == "__main__":
    build_hyperframes_composition()
