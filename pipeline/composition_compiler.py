import os
import re
import json
import math
import subprocess
from pipeline.lipsync_engine import generate_lipsync_data

SLOT_THEMES = {
    1: {"primary": "bl", "label": "AI OPEN SOURCE", "accent": "#2563eb", "desc": "3 Verified GitHub Superpowers"},
    2: {"primary": "gr", "label": "AI WORKFLOW BLUEPRINT", "accent": "#16a34a", "desc": "Production Agency Automations"},
    3: {"primary": "pk", "label": "TECH RADAR TEARDOWN", "accent": "#d946ef", "desc": "Frontier Model Benchmarks"},
    4: {"primary": "yl", "label": "SECRET WEB AI TOOLS", "accent": "#f59e0b", "desc": "No-Code Superpower Websites"},
    5: {"primary": "rd", "label": "SENIOR PROMPT LAB", "accent": "#ef4444", "desc": "Elite Architect Frameworks"}
}

def build_hyperframes_composition(
    repos_file="assets/curated_repos.json",
    captions_file="assets/caption_chunks.json",
    audio_path="assets/voice.mp3",
    script_file="assets/generated_script.json",
    duration=45.0,
    output_html="index.html",
    slot_meta=None
):
    """
    Hyper-Paced Neo-Brutalist Movie Engine (1080x1920 @ 60fps):
    - Full-frame neo-brutalist candy stripes with animated translation (zero static seconds).
    - 12 to 15 distinct micro-scenes (shots) changing every 1.8s - 3.2s.
    - Floating motes & macro camera zoom drift.
    - High-density visual atoms: Code terminals, macOS windows, device mockups, speedometers,
      equalizer bars, 3D star cards, checkmark grids, strike-through wipes.
    - Dynamic lower-corner Anchor Avatar (blinking eyes, waving/pointing arm, 4-state RMS lip-sync).
    - Real-time word-by-word kinetic subtitle pill.
    - Frame-accurate SFX cues written to assets/sfx_cues.json.
    - Clean GSAP registration: window.__timelines["main"] = tl.
    """
    if slot_meta is None:
        slot_meta = {
            "slot_id": 1,
            "slot_name": "Morning Breakthrough",
            "badge_title": "AI OPEN SOURCE",
            "badge_sub": "3 VERIFIED REPOS",
            "cta_keyword": "REPOS",
            "post_title": "3 Insane Open-Source AI Developer Repos!"
        }

    sid = slot_meta.get("slot_id", 1)
    slot_theme = SLOT_THEMES.get(sid, SLOT_THEMES[1])
    cta_word = slot_meta.get("cta_keyword", "TOOLS").upper()

    # Update hyperframes.json with exact duration
    try:
        hf_conf = {
            "name": "daily-automation-engine",
            "version": "3.1.0",
            "fps": 30,
            "width": 1080,
            "height": 1920,
            "duration": round(float(duration), 2)
        }
        with open("hyperframes.json", "w") as hf_file:
            json.dump(hf_conf, hf_file, indent=2)
    except Exception as e:
        print(f"[!] Warning updating hyperframes.json: {e}")

    # 1. Load curated items
    repos = []
    if os.path.exists(repos_file):
        try:
            with open(repos_file) as f:
                repos = json.load(f)[:3]
        except Exception:
            repos = []

    # 2. Load script data
    script_data = {}
    if os.path.exists(script_file):
        try:
            with open(script_file) as f:
                script_data = json.load(f)
        except Exception:
            pass

    # Ensure 3 valid items with clean titles & badges
    items = []
    for idx, r in enumerate(repos):
        full_name = r.get("full_name") or r.get("name") or f"tool-{idx+1}"
        short_name = r.get("name") or full_name.split("/")[-1]
        clean_name = short_name.replace("-", " ").title()
        stars_val = r.get("stars", 15000 + idx * 8000)
        stars_str = f"{stars_val:,}" if isinstance(stars_val, int) else str(stars_val)
        desc = r.get("description", "High performance autonomous developer capability")[:100]
        badge = r.get("badge", slot_theme["label"])
        url = r.get("url", f"https://github.com/{full_name}")
        items.append({
            "name": clean_name,
            "full_name": full_name,
            "stars": stars_str,
            "desc": desc,
            "badge": badge,
            "url": url
        })

    while len(items) < 3:
        i = len(items) + 1
        items.append({
            "name": f"AI Engine {i}",
            "full_name": f"developer/engine-{i}",
            "stars": "24,000",
            "desc": "Next generation AI acceleration framework",
            "badge": slot_theme["label"],
            "url": "https://github.com"
        })

    it1, it2, it3 = items[0], items[1], items[2]

    # 3. Load or generate lip-sync data
    mouth_json_path = "assets/mouth.json"
    mouth_data = []
    if os.path.exists(audio_path) and os.path.exists(captions_file):
        try:
            mouth_data = generate_lipsync_data(
                audio_path=audio_path,
                caption_chunks_path=captions_file,
                output_mouth_path=mouth_json_path,
                fps=30
            )
        except Exception as e:
            print(f"[!] Lip-sync generation warning: {e}")

    if not mouth_data and os.path.exists(mouth_json_path):
        try:
            with open(mouth_json_path) as f:
                mouth_data = json.load(f)
        except Exception:
            mouth_data = []

    # 4. Load captions
    caption_chunks = []
    if os.path.exists(captions_file):
        try:
            with open(captions_file) as f:
                caption_chunks = json.load(f)
        except Exception:
            caption_chunks = []

    # 5. Build 14 Dynamic Micro-Shots proportional to duration
    # Shot timing breakdown across ~45s
    d = max(35.0, float(duration))
    t0 = 0.0
    t1 = round(d * 0.06, 2)   # ~2.7s
    t2 = round(d * 0.13, 2)   # ~5.8s
    t3 = round(d * 0.20, 2)   # ~9.0s
    t4 = round(d * 0.28, 2)   # ~12.6s (Item 1 Reveal)
    t5 = round(d * 0.36, 2)   # ~16.2s (Item 1 Superpower)
    t6 = round(d * 0.44, 2)   # ~19.8s (Item 1 Metric)
    t7 = round(d * 0.52, 2)   # ~23.4s (Item 2 Reveal)
    t8 = round(d * 0.60, 2)   # ~27.0s (Item 2 Superpower)
    t9 = round(d * 0.68, 2)   # ~30.6s (Item 2 Metric)
    t10 = round(d * 0.75, 2)  # ~33.7s (Item 3 Reveal)
    t11 = round(d * 0.82, 2)  # ~36.9s (Item 3 Superpower)
    t12 = round(d * 0.88, 2)  # ~39.6s (Stack Synergy / CLI)
    t13 = round(d * 0.92, 2)  # ~41.4s (CTA)
    t_end = round(d, 2)

    shots = [
        {"id": 0, "start": t0, "end": t1, "theme": "rd", "label": "STOP DOING THIS MANUALLY", "pr": "0/3"},
        {"id": 1, "start": t1, "end": t2, "theme": "dk", "label": slot_theme["label"], "pr": "0/3"},
        {"id": 2, "start": t2, "end": t3, "theme": "bl", "label": "THE NEW WORKFLOW", "pr": "0/3"},
        {"id": 3, "start": t3, "end": t4, "theme": "yl", "label": "OLD SAAS IS DEAD", "pr": "0/3"},
        {"id": 4, "start": t4, "end": t5, "theme": "gr", "label": f"01 · {it1['name']}", "pr": "1/3"},
        {"id": 5, "start": t5, "end": t6, "theme": "bl", "label": "SUPERPOWER UNLOCKED", "pr": "1/3"},
        {"id": 6, "start": t6, "end": t7, "theme": "rd", "label": "100% OPEN SOURCE", "pr": "1/3"},
        {"id": 7, "start": t7, "end": t8, "theme": "pk", "label": f"02 · {it2['name']}", "pr": "2/3"},
        {"id": 8, "start": t8, "end": t9, "theme": "bl", "label": "REAL-TIME VISION & EXECUTION", "pr": "2/3"},
        {"id": 9, "start": t9, "end": t10, "theme": "yl", "label": "MAX PERFORMANCE", "pr": "2/3"},
        {"id": 10, "start": t10, "end": t11, "theme": "dk", "label": f"03 · {it3['name']}", "pr": "3/3"},
        {"id": 11, "start": t11, "end": t12, "theme": "gr", "label": "100% PRIVATE & OFFLINE", "pr": "3/3"},
        {"id": 12, "start": t12, "end": t13, "theme": "bl", "label": "60-SECOND QUICKSTART", "pr": "3/3"},
        {"id": 13, "start": t13, "end": t_end, "theme": "rd", "label": f"COMMENT '{cta_word}'", "pr": "3/3"}
    ]

    # SFX Cues matched to shot boundaries
    sfx_cues = [
        {"type": "boom", "time": t0},
        {"type": "whoosh", "time": round(t0 + 0.05, 2)},
        {"type": "ding", "time": round(t0 + 0.8, 2)},
        {"type": "whoosh", "time": t1},
        {"type": "pop", "time": round(t1 + 0.3, 2)},
        {"type": "whoosh", "time": t2},
        {"type": "click", "time": round(t2 + 0.4, 2)},
        {"type": "whoosh", "time": t3},
        {"type": "pop", "time": round(t3 + 0.35, 2)},
        {"type": "whoosh", "time": t4},
        {"type": "ding", "time": round(t4 + 0.4, 2)},
        {"type": "whoosh", "time": t5},
        {"type": "click", "time": round(t5 + 0.3, 2)},
        {"type": "whoosh", "time": t6},
        {"type": "pop", "time": round(t6 + 0.35, 2)},
        {"type": "whoosh", "time": t7},
        {"type": "ding", "time": round(t7 + 0.4, 2)},
        {"type": "whoosh", "time": t8},
        {"type": "click", "time": round(t8 + 0.3, 2)},
        {"type": "whoosh", "time": t9},
        {"type": "ding", "time": round(t9 + 0.4, 2)},
        {"type": "whoosh", "time": t10},
        {"type": "pop", "time": round(t10 + 0.3, 2)},
        {"type": "whoosh", "time": t11},
        {"type": "click", "time": round(t11 + 0.3, 2)},
        {"type": "whoosh", "time": t12},
        {"type": "ding", "time": round(t12 + 0.4, 2)},
        {"type": "boom", "time": t13},
        {"type": "pop", "time": round(t13 + 0.4, 2)}
    ]
    with open("assets/sfx_cues.json", "w") as f:
        json.dump(sfx_cues, f, indent=2)

    # Mouth call generation
    mouth_calls = []
    last_m = None
    for item in mouth_data:
        m = item.get("mouth", "closed")
        f = item.get("f", item.get("frame", 0))
        t = round(f / 30.0, 3)
        if m != last_m and t <= d:
            mouth_calls.append(f'tl.call(() => setMouth("{m}"), null, {t});')
            last_m = m

    # Shot call generation
    shot_calls = []
    for s in shots:
        shot_calls.append(f'tl.call(() => mountShot({s["id"]}), null, {s["start"]});')

    # Caption call generation
    caption_calls = []
    for c in caption_chunks:
        word_text = " ".join(c.get("words", [])) if "words" in c else c.get("text", "")
        clean_word = word_text.strip().replace('"', '\\"')
        caption_calls.append(f'tl.call(() => setWord("{clean_word}"), null, {c.get("start", 0)});')
    caption_calls.append(f'tl.call(() => setWord(""), null, {max(0, d - 0.2)});')

    # HTML templates for the 14 shots
    shots_html = [
        # Shot 0: The Hook / Stop Paying / Manual Bottleneck
        f"""
        <div class="big-title">STOP DOING THIS MANUALLY</div>
        <div class="sub-stamp" style="background:#ff3b30; color:#fff;">⚠️ WASTING 20 HOURS/WEEK</div>
        <div class="card" style="display:flex; flex-direction:column; align-items:center; gap:24px; position:relative;">
          <div style="display:flex; gap:36px; align-items:center;">
            <div style="font-size:110px; animation: jitterBug 0.15s infinite alternate;">❌</div>
            <div style="font-size:120px; animation: tapFinger 0.35s infinite alternate;">⏳</div>
            <div style="font-size:110px; animation: jitterBug 0.2s infinite alternate;">💸</div>
          </div>
          <div class="strike-bar"></div>
          <div style="font:800 32px 'IBM Plex Mono'; color:#ff3b30; text-align:center;">SLOW · EXPENSIVE · REPETITIVE</div>
        </div>
        """,

        # Shot 1: The Solution
        f"""
        <div class="big-title">THE NEW AI STACK</div>
        <div class="sub-stamp" style="background:#22c55e; color:#fff;">⚡ {slot_theme['label']}</div>
        <div class="card" style="background:#14121a; color:#fff; display:flex; flex-direction:column; align-items:center; gap:28px; position:relative;">
          <div class="shockwave-ring"></div>
          <div style="font-size:120px; animation: bobbing 1.2s infinite alternate;">🚀</div>
          <div style="font:800 36px 'IBM Plex Mono'; color:#38bdf8;">{{ autonomous.execute() }}</div>
          <div style="display:flex; gap:16px;">
            <span class="sub-stamp" style="font-size:24px; padding:6px 16px;">ZERO MONTHLY SAAS</span>
            <span class="sub-stamp" style="font-size:24px; padding:6px 16px; background:#6f9ee8; color:#fff;">10X PRODUCTIVITY</span>
          </div>
        </div>
        """,

        # Shot 2: Architecture / Connection
        f"""
        <div class="big-title">THE AUTOMATED PIPELINE</div>
        <div class="sub-stamp" style="background:#ffd23f; color:#111;">⚡ END-TO-END EXECUTION</div>
        <div class="card" style="display:flex; justify-content:space-around; align-items:center; position:relative;">
          <div style="text-align:center;">
            <div style="font-size:90px;">💻</div>
            <div style="font:800 26px 'IBM Plex Mono'; margin-top:8px;">Your Laptop</div>
          </div>
          <div class="lightning-flow">
            <div class="lightning-bolt">⚡⚡⚡</div>
            <div style="font:900 28px 'IBM Plex Mono'; color:#ff3b30;">AUTONOMOUS AGENT</div>
          </div>
          <div style="text-align:center;">
            <div style="font-size:90px; animation: phoneGlow 1s infinite alternate;">⚡</div>
            <div style="font:800 26px 'IBM Plex Mono'; margin-top:8px;">Full Production</div>
          </div>
        </div>
        """,

        # Shot 3: Old SaaS is Dead
        f"""
        <div class="big-title">LEGACY SAAS IS DEAD</div>
        <div class="sub-stamp" style="background:#ff3b30; color:#fff;">STOP PAYING SUBSCRIPTIONS</div>
        <div class="card" style="background:#1e293b; color:#fff; display:flex; flex-direction:column; align-items:center; gap:20px;">
          <div style="font-size:90px;">💸</div>
          <div style="font:800 32px 'IBM Plex Mono'; color:#ef4444;">❌ $200+/MONTH SAVED</div>
          <div style="font:700 26px 'IBM Plex Mono'; color:#94a3b8; text-align:center;">Replace expensive proprietary platforms with open code</div>
        </div>
        """,

        # Shot 4: Item 1 Reveal
        f"""
        <div class="big-title">01 · {it1['name']}</div>
        <div class="win">
          <div class="hd"><i></i><i></i><i></i>{it1['url']}</div>
          <div class="bd">
            <div><span class="c">repo:</span> <span class="y">{it1['full_name']}</span></div>
            <div style="margin-top:14px;"><span class="g">★ {it1['stars']} GitHub Stars</span></div>
            <div style="margin-top:14px; color:#aaa;">{it1['desc']}</div>
          </div>
        </div>
        <div class="sub-stamp" style="background:#22c55e; color:#fff; rotate:2deg;">★ {it1['badge']}</div>
        """,

        # Shot 5: Item 1 Superpower
        f"""
        <div class="big-title">{it1['name'].upper()} SUPERPOWER</div>
        <div class="sub-stamp" style="background:#38bdf8; color:#111;">HIGH-PERFORMANCE ARCHITECTURE</div>
        <div class="card" style="display:flex; flex-direction:column; gap:20px;">
          <div class="chk">
            <div class="ck"><u>✔</u> Complete autonomous local execution</div>
            <div class="ck"><u>✔</u> Zero rate limits & zero telemetry</div>
            <div class="ck"><u>✔</u> Seamless integration into existing workflows</div>
          </div>
        </div>
        """,

        # Shot 6: Item 1 Metric
        f"""
        <div class="big-title">VERIFIED BENCHMARKS</div>
        <div class="card" style="display:flex; justify-content:space-around; align-items:center;">
          <div style="text-align:center;">
            <div style="font:900 80px 'Bricolage Grotesque'; color:#2563eb;">{it1['stars']}</div>
            <div style="font:800 26px 'IBM Plex Mono';">DEVELOPER STARS</div>
          </div>
          <div style="height:110px; width:4px; background:#ddd;"></div>
          <div style="text-align:center;">
            <div style="font:900 80px 'Bricolage Grotesque'; color:#16a34a;">$0</div>
            <div style="font:800 26px 'IBM Plex Mono';">MONTHLY COST</div>
          </div>
        </div>
        <div class="sub-stamp" style="background:#f6c85a; color:#111;">★ PRODUCTION READY</div>
        """,

        # Shot 7: Item 2 Reveal
        f"""
        <div class="big-title">02 · {it2['name']}</div>
        <div class="win">
          <div class="hd"><i></i><i></i><i></i>{it2['url']}</div>
          <div class="bd">
            <div><span class="c">engine:</span> <span class="y">{it2['full_name']}</span></div>
            <div style="margin-top:14px;"><span class="g">★ {it2['stars']} Stars</span> · Verified Production</div>
            <div style="margin-top:14px; color:#aaa;">{it2['desc']}</div>
          </div>
        </div>
        <div class="sub-stamp" style="background:#f43f5e; color:#fff; rotate:-2deg;">★ {it2['badge']}</div>
        """,

        # Shot 8: Item 2 Superpower
        f"""
        <div class="big-title">AUTONOMOUS GROUNDING</div>
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
              <div class="bbox red-box" style="top:200px;">🎯 [DETECT: Superpower]</div>
              <div class="bbox green-box" style="top:420px;">⚡ [EXECUTE: Automation]</div>
            </div>
          </div>
          <div style="display:flex; flex-direction:column; gap:16px;">
            <span class="sub-stamp" style="font-size:26px; background:#f6c85a; color:#111;">DETECTS EVERYTHING</span>
            <span class="sub-stamp" style="font-size:26px; background:#22c55e; color:#fff;">AUTONOMOUS ACTIONS</span>
            <span class="sub-stamp" style="font-size:26px; background:#38bdf8; color:#fff;">ZERO HUMAN DELAY</span>
          </div>
        </div>
        """,

        # Shot 9: Item 2 Metric / Speed
        f"""
        <div class="big-title">EXTREME SPEED & ACCURACY</div>
        <div class="card" style="display:flex; justify-content:space-around; align-items:center;">
          <div style="text-align:center;">
            <div style="font:900 42px 'Bricolage Grotesque'; color:#2563eb;">LATENCY</div>
            <div style="font:700 26px 'IBM Plex Mono'; margin-top:8px;">Sub-Second Response</div>
          </div>
          <div class="gauge-box">
            <div class="gauge-needle"></div>
            <div style="position:absolute; bottom:12px; font:900 22px 'IBM Plex Mono';">MAX SPEED</div>
          </div>
          <div style="text-align:center;">
            <div style="font:900 42px 'Bricolage Grotesque'; color:#16a34a;">ACCURACY</div>
            <div style="font:700 26px 'IBM Plex Mono'; margin-top:8px;">99.4% Deterministic</div>
          </div>
        </div>
        """,

        # Shot 10: Item 3 Reveal
        f"""
        <div class="big-title">03 · {it3['name']}</div>
        <div class="win">
          <div class="hd"><i></i><i></i><i></i>{it3['url']}</div>
          <div class="bd">
            <div><span class="c">target:</span> <span class="y">{it3['full_name']}</span></div>
            <div style="margin-top:14px;"><span class="g">★ {it3['stars']} Stars</span></div>
            <div style="margin-top:14px; color:#aaa;">{it3['desc']}</div>
          </div>
        </div>
        <div class="sub-stamp" style="background:#22c55e; color:#fff;">★ {it3['badge']}</div>
        """,

        # Shot 11: Item 3 Superpower / 100% Private Offline
        f"""
        <div class="big-title">100% PRIVATE & LOCAL</div>
        <div class="card" style="display:flex; justify-content:space-between; align-items:center; background:#111; color:#fff;">
          <div>
            <div style="font:900 48px 'Bricolage Grotesque'; color:#38bdf8;">OFFLINE INFERENCE</div>
            <div style="font:700 26px 'IBM Plex Mono'; color:#aaa; margin-top:8px;">Zero cloud dependencies</div>
            <div class="sub-stamp" style="background:#22c55e; color:#fff; margin-top:16px;">$0 API BILLS</div>
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

        # Shot 12: Stack Quickstart CLI
        f"""
        <div class="big-title">RUN IN 60 SECONDS</div>
        <div class="win">
          <div class="hd"><i></i><i></i><i></i>Terminal — Quickstart</div>
          <div class="bd">
            <div><span class="y">$</span> pip install {it1['name'].lower().replace(' ', '-')}</div>
            <div style="margin-top:18px;"><span class="y">$</span> git clone {it2['url']}</div>
            <div style="margin-top:18px;" class="g">✔ Stack Initialized & Connected</div>
            <div style="margin-top:10px;" class="g">✔ All 3 Superpowers Active</div>
          </div>
        </div>
        <div class="sub-stamp" style="background:#22c55e; color:#fff;">ONE-LINE SETUP</div>
        """,

        # Shot 13: Viral High-Converting CTA
        f"""
        <div class="big-title">GET THE FULL BLUEPRINT</div>
        <div class="fol-btn">COMMENT "{cta_word}"</div>
        <div class="card" style="text-align:center; max-width:760px; background:#ffd23f;">
          <div style="font:900 36px 'Bricolage Grotesque';">📩 I will DM you the direct repo links + setup guide right now</div>
        </div>
        <div class="reactions-row">
          <div class="reaction-ic">♥</div>
          <div class="reaction-ic">🔖</div>
          <div class="reaction-ic">↗</div>
        </div>
        """
    ]

    # Assemble HTML document
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
  <title>{slot_meta.get('post_title', 'Daily AI Reel')}</title>
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
      padding: 36px 44px;
      font-size: 30px;
      line-height: 1.5;
    }}
    .win .bd .c {{ color: #38bdf8; }}
    .win .bd .y {{ color: #ffd23f; }}
    .win .bd .g {{ color: #4ade80; }}

    /* Interactive Elements */
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
      gap: 20px;
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
      height: 520px;
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
      height: 160px;
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

    /* ================= LOWER ANCHOR AVATAR RIG ================= */
    #char-rig {{
      position: absolute;
      bottom: 0;
      right: 36px;
      width: 320px;
      height: 340px;
      z-index: 20;
      pointer-events: none;
    }}

    /* Arm Waving Animation */
    #arm-wave {{
      transform-origin: 220px 240px;
      animation: armWave 1.4s ease-in-out infinite alternate;
    }}
    @keyframes armWave {{
      0% {{ transform: rotate(0deg); }}
      100% {{ transform: rotate(-16deg); }}
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

      <!-- 14 Dynamic Shots Container -->
      {all_shots_markup}
    </div>

    <!-- Word-by-Word Subtitle Pill -->
    <div id="word-pill">READY</div>

    <!-- Anchored Vector Character Rig with Synced Mouth & Gestures -->
    <svg id="char-rig" viewBox="0 0 320 340">
      <!-- Animated Waving Arm -->
      <g id="arm-wave">
        <path d="M 220 250 Q 250 170 230 130" stroke="#1f2937" stroke-width="36" stroke-linecap="round" fill="none" />
        <circle cx="230" cy="120" r="18" fill="#e5b89a" />
      </g>
      <!-- Body & Dark Hoodie -->
      <path d="M 60 340 C 60 270 90 240 160 240 C 230 240 260 270 260 340 Z" fill="#1f2937" />
      <path d="M 148 240 L 148 300 M 172 240 L 172 300" stroke="#fff" stroke-width="4" stroke-linecap="round" />
      <!-- Head -->
      <circle cx="160" cy="170" r="66" fill="#e5b89a" />
      <path d="M 94 160 C 94 95 226 95 226 160 C 210 130 110 130 94 160 Z" fill="#111827" />
      <!-- Red Headset -->
      <path d="M 90 170 A 70 70 0 0 1 230 170" stroke="#ef4444" stroke-width="12" fill="none" />
      <rect x="80" y="150" width="18" height="40" rx="9" fill="#ef4444" />
      <rect x="222" y="150" width="18" height="40" rx="9" fill="#ef4444" />
      <!-- Glasses -->
      <circle cx="135" cy="165" r="22" stroke="#111" stroke-width="7" fill="none" />
      <circle cx="185" cy="165" r="22" stroke="#111" stroke-width="7" fill="none" />
      <line x1="157" y1="165" x2="163" y2="165" stroke="#111" stroke-width="7" />
      <!-- Blinking Eyes -->
      <g class="eye-blink">
        <circle cx="135" cy="165" r="7" fill="#111" />
        <circle cx="185" cy="165" r="7" fill="#111" />
      </g>
      <!-- Dynamic Lip-Sync Mouth States -->
      <g id="mouth-group">
        <ellipse id="m-closed" cx="160" cy="205" rx="16" ry="3" fill="#601a1a" />
        <ellipse id="m-slight" cx="160" cy="205" rx="18" ry="8" fill="#601a1a" style="display:none;" />
        <ellipse id="m-half" cx="160" cy="206" rx="20" ry="15" fill="#601a1a" style="display:none;" />
        <ellipse id="m-wide" cx="160" cy="208" rx="22" ry="24" fill="#601a1a" style="display:none;" />
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
    with open(output_html, "w") as f:
        f.write(html_content)

    print(f"[✓] Compiled {len(shots)}-Shot Neo-Brutalist Reel Composition to {output_html} ({round(os.path.getsize(output_html)/1024, 1)} KB)")
    return output_html

if __name__ == "__main__":
    build_hyperframes_composition()
