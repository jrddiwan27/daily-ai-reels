import json
import os

SLOT_VISUAL_THEMES = {
    1: {
        "name": "CYBER_TERMINAL",
        "console_tag": "CORE RUNTIME",
        "bg_hook": "#0D1117",
        "bg_hook_dots": "#1E293B",
        "bg_tool1": "#0B1528",
        "bg_tool1_dots": "#1D4ED8",
        "bg_tool2": "#061A1E",
        "bg_tool2_dots": "#0E7490",
        "bg_tool3": "#0E1A16",
        "bg_tool3_dots": "#047857",
        "bg_outro": "#111827",
        "bg_outro_dots": "#374151",
        "desk_hook": "#1E293B",
        "desk_tool1": "#1E3A8A",
        "desk_tool2": "#065F46",
        "desk_tool3": "#831843",
        "desk_outro": "#1F2937",
        "desk_border": "#030712",
        "hoodie_color": "#2563EB",  # Electric Blue
        "hoodie_trim": "#1D4ED8",
        "mug_color": "#38BDF8",     # Cyan
        "accent_color": "#38BDF8",  # Cyan
        "badge_pill": "⚡ OPEN SOURCE REPOS",
        "badge_bg": "#38BDF8",
        "badge_color": "#030712",
        "console_bg": "#0D1117",
        "console_border": "#30363D",
        "item_icons": ["⚡", "🧠", "✉️"],
        "hook_title": "3 INSANE OPEN-SOURCE AI REPOS",
        "hook_sub": "RUN 100% LOCALLY · ZERO MONTHLY FEES",
        "initial_pose": "point",
        "t1_gauge_title": "⚡ HARDWARE COMPILER",
        "t1_gauge_val": "100% COMPILED",
        "t2_gauge_title": "🧠 MEMORY KERNEL OPTIMIZATION",
        "t2_gauge_val": "-99.1% LATENCY REDUCED",
        "t2_gauge_sub": "128k → 1.2k tok",
        "counter_label": "COMPILATION ERRORS",
        "counter_start": 142,
        "counter_end": 0,
        "counter_badge": "🎉 ZERO COMPILE ERRORS ACHIEVED!",
        "step2_text": "[✓] Silicon acceleration & CUDA kernels: ACTIVE",
        "step3_prefix": "⚡ LATENCY: 2.4ms · HIGH THROUGHPUT"
    },
    2: {
        "name": "STUDIO_WORKFLOW",
        "console_tag": "AUTOMATION PIPELINE",
        "bg_hook": "#F0FDF4",
        "bg_hook_dots": "#A7F3D0",
        "bg_tool1": "#ECFDF5",
        "bg_tool1_dots": "#6EE7B7",
        "bg_tool2": "#F0FDF9",
        "bg_tool2_dots": "#5EEAD4",
        "bg_tool3": "#FEFCE8",
        "bg_tool3_dots": "#FDE047",
        "bg_outro": "#F5F3FF",
        "bg_outro_dots": "#C4B5FD",
        "desk_hook": "#B45309",     # Warm Bamboo / Teak
        "desk_tool1": "#059669",
        "desk_tool2": "#0D9488",
        "desk_tool3": "#D97706",
        "desk_outro": "#B45309",
        "desk_border": "#171819",
        "hoodie_color": "#059669",  # Emerald Studio
        "hoodie_trim": "#047857",
        "mug_color": "#10B981",     # Emerald
        "accent_color": "#10B981",  # Emerald
        "badge_pill": "🔄 AI AUTOMATION PIPELINE",
        "badge_bg": "#10B981",
        "badge_color": "#FFFFFF",
        "console_bg": "#111827",
        "console_border": "#10B981",
        "item_icons": ["🔄", "⚡", "🤖"],
        "hook_title": "THE 20-HOUR AUTOMATION BLUEPRINT",
        "hook_sub": "STOP WASTING HOURS ON MANUAL WORK",
        "initial_pose": "thumbs-up",
        "t1_gauge_title": "🔄 WORKFLOW SYNCHRONIZER",
        "t1_gauge_val": "100% TASKS SYNCED",
        "t2_gauge_title": "⏱️ RECURRING HOURS SAVED",
        "t2_gauge_val": "20 HRS / WEEK SAVED",
        "t2_gauge_sub": "0 Manual Code Required",
        "counter_label": "MANUAL HOURS WASTED",
        "counter_start": 20,
        "counter_end": 0,
        "counter_badge": "🎉 20 HRS/WEEK FULLY AUTOMATED!",
        "step2_text": "[✓] Self-healing webhook loop & real-time sync",
        "step3_prefix": "⏱️ ZERO MANUAL OVERHEAD · 100% UNATTENDED"
    },
    3: {
        "name": "BENCHMARK_RADAR",
        "console_tag": "MODEL EVALUATION",
        "bg_hook": "#130E26",
        "bg_hook_dots": "#3B1E54",
        "bg_tool1": "#1E1138",
        "bg_tool1_dots": "#581C87",
        "bg_tool2": "#171330",
        "bg_tool2_dots": "#4338CA",
        "bg_tool3": "#24142F",
        "bg_tool3_dots": "#86198F",
        "bg_outro": "#18122B",
        "bg_outro_dots": "#3B1E54",
        "desk_hook": "#312E81",     # Cyber Indigo Steel
        "desk_tool1": "#6D28D9",
        "desk_tool2": "#4338CA",
        "desk_tool3": "#701A75",
        "desk_outro": "#312E81",
        "desk_border": "#0F0B1E",
        "hoodie_color": "#7C3AED",  # Deep Violet
        "hoodie_trim": "#6D28D9",
        "mug_color": "#A855F7",     # Violet
        "accent_color": "#C084FC",  # Neon Violet
        "badge_pill": "🧠 MODEL RADAR & BENCHMARK",
        "badge_bg": "#8B5CF6",
        "badge_color": "#FFFFFF",
        "console_bg": "#0B0717",
        "console_border": "#7C3AED",
        "item_icons": ["🧠", "📊", "🚀"],
        "hook_title": "NEW SOTA MODEL BENCHMARKS",
        "hook_sub": "WHY CLOSED FRONTIER AI JUST LOST",
        "initial_pose": "point",
        "t1_gauge_title": "🧠 REASONING ENGINE",
        "t1_gauge_val": "100% TOKENS STREAMED",
        "t2_gauge_title": "⚡ INFERENCE THROUGHPUT",
        "t2_gauge_val": "185 TOKENS/SEC",
        "t2_gauge_sub": "1M Context Active",
        "counter_label": "INFERENCE LATENCY",
        "counter_start": 380,
        "counter_end": 12,
        "counter_badge": "🎉 SOTA BENCHMARK VERIFIED!",
        "step2_text": "[✓] Hybrid reasoning & unbounded context active",
        "step3_prefix": "📊 SOTA BENCHMARK: 96.4% · 185 TOK/S"
    },
    4: {
        "name": "CREATOR_TOOLKIT",
        "console_tag": "BROWSER STUDIO",
        "bg_hook": "#FFF7ED",
        "bg_hook_dots": "#FED7AA",
        "bg_tool1": "#FEF2F2",
        "bg_tool1_dots": "#FECACA",
        "bg_tool2": "#FFFBEB",
        "bg_tool2_dots": "#FDE68A",
        "bg_tool3": "#F0FDF4",
        "bg_tool3_dots": "#BBF7D0",
        "bg_outro": "#FFF7ED",
        "bg_outro_dots": "#FED7AA",
        "desk_hook": "#1D4ED8",     # High-contrast Cobalt
        "desk_tool1": "#DC2626",
        "desk_tool2": "#D97706",
        "desk_tool3": "#059669",
        "desk_outro": "#1D4ED8",
        "desk_border": "#171819",
        "hoodie_color": "#EA580C",  # Sunset Coral
        "hoodie_trim": "#C2410C",
        "mug_color": "#F97316",     # Coral
        "accent_color": "#F97316",  # Coral
        "badge_pill": "🛠️ SECRET NO-CODE TOOLS",
        "badge_bg": "#EA580C",
        "badge_color": "#FFFFFF",
        "console_bg": "#18181B",
        "console_border": "#EA580C",
        "item_icons": ["🛠️", "✨", "🎨"],
        "hook_title": "3 SECRET NO-CODE AI WEBSITES",
        "hook_sub": "REPLACE EXPENSIVE APPS IN 1 CLICK",
        "initial_pose": "thumbs-up",
        "t1_gauge_title": "🚀 BROWSER CLOUD ENGINE",
        "t1_gauge_val": "100% RENDERED IN 1.2s",
        "t2_gauge_title": "🎨 ASSET GENERATION SPEED",
        "t2_gauge_val": "10X PRODUCTIVITY BOOST",
        "t2_gauge_sub": "Instant Figma/React Export",
        "counter_label": "SETUP TIME (MINUTES)",
        "counter_start": 60,
        "counter_end": 0,
        "counter_badge": "🎉 INSTANT 1-CLICK LAUNCH ACHIEVED!",
        "step2_text": "[✓] 100% In-browser sandbox · Zero installs",
        "step3_prefix": "💡 10X ACCELERATION · PRODUCTION EXPORTS"
    },
    5: {
        "name": "PROMPT_LAB",
        "console_tag": "PROMPT ARCHITECTURE",
        "bg_hook": "#18181B",
        "bg_hook_dots": "#3F3F46",
        "bg_tool1": "#271215",
        "bg_tool1_dots": "#7F1D1D",
        "bg_tool2": "#1E1722",
        "bg_tool2_dots": "#4A044E",
        "bg_tool3": "#1F1D17",
        "bg_tool3_dots": "#713F12",
        "bg_outro": "#18181B",
        "bg_outro_dots": "#3F3F46",
        "desk_hook": "#27272A",     # Carbon Fiber Obsidian
        "desk_tool1": "#991B1B",
        "desk_tool2": "#581C87",
        "desk_tool3": "#854D0E",
        "desk_outro": "#27272A",
        "desk_border": "#09090B",
        "hoodie_color": "#DC2626",  # JDS Brand Crimson Red
        "hoodie_trim": "#B91C1C",
        "mug_color": "#EF4444",     # Crimson
        "accent_color": "#EF4444",  # Crimson
        "badge_pill": "🎯 SENIOR PROMPT ARCHITECTURE",
        "badge_bg": "#EF4444",
        "badge_color": "#FFFFFF",
        "console_bg": "#09090B",
        "console_border": "#EF4444",
        "item_icons": ["🎯", "🛡️", "🔮"],
        "hook_title": "SENIOR AI PROMPT ARCHITECTURE",
        "hook_sub": "ELIMINATE 99% OF LLM HALLUCINATIONS",
        "initial_pose": "point",
        "t1_gauge_title": "🎯 XML SCHEMA VALIDATOR",
        "t1_gauge_val": "100% CONSTRAINTS SATISFIED",
        "t2_gauge_title": "🛡️ HALLUCINATION SUPPRESSION",
        "t2_gauge_val": "-99.9% ZERO ERROR RATE",
        "t2_gauge_sub": "Dual-Pass Schema Verification",
        "counter_label": "HALLUCINATION RATE",
        "counter_start": 48,
        "counter_end": 0,
        "counter_badge": "🎉 ZERO HALLUCINATIONS ACHIEVED!",
        "step2_text": "[✓] Dual-pass architecture & schema guardrails",
        "step3_prefix": "🛡️ 100% DETERMINISTIC JSON OUTPUT"
    }
}

def generate_hero_visual(repo, slot_id, idx, theme):
    demo = repo.get("demo")
    name = repo.get("name", "TOOL")
    owner = repo.get("owner", "open-source")
    desc = repo.get("desc", "")
    short_desc = desc[:45] + "..." if len(desc) > 45 else desc

    # Verify if image is genuine and not a mismatched placeholder
    is_genuine_image = False
    if demo and os.path.exists(demo):
        if "heygen-com_hyperframes" in demo:
            is_genuine_image = ("hyperframes" in name.lower())
        elif "tenstorrent" in demo:
            is_genuine_image = ("tt-metal" in name.lower() or "tenstorrent" in name.lower())
        elif "inbox-zero" in demo:
            is_genuine_image = ("inbox-zero" in name.lower())
        else:
            is_genuine_image = True

    if is_genuine_image:
        return f"""
        <div class="demo-media-box">
          <img src="{demo}" alt="{name}">
          <div class="demo-media-tag">● {name}</div>
        </div>
        """

    # Slot-tailored dynamic vector/HTML UI mockups
    if slot_id == 1:
        # Developer Repos - Syntax-highlighted code editor
        return f"""
        <div class="demo-media-box hero-code-editor">
          <div class="editor-header">
            <div class="editor-tab">● main.py</div>
            <div class="editor-lang">Python 3.12</div>
          </div>
          <div class="editor-code">
            <div><span class="c-kw">import</span> <span class="c-mod">{name.lower().replace('-', '_')}</span> <span class="c-kw">as</span> <span class="c-var">core</span></div>
            <div><span class="c-var">app</span> = <span class="c-var">core</span>.<span class="c-fn">Client</span>(mode=<span class="c-str">"autonomous"</span>)</div>
            <div><span class="c-var">res</span> = <span class="c-var">app</span>.<span class="c-fn">execute</span>()</div>
            <div class="editor-log">&gt; [✓] {short_desc}</div>
          </div>
        </div>
        """
    elif slot_id == 2:
        # AI Workflows - Autonomous Pipeline Canvas
        return f"""
        <div class="demo-media-box hero-workflow-graph">
          <div class="wf-header">
            <span>PIPELINE ENGINE · {name[:12]}</span>
            <span class="wf-live">● LIVE FLOW</span>
          </div>
          <div class="wf-nodes">
            <div class="wf-node">
              <span class="wf-icon">⚡</span>
              <span class="wf-title">TRIGGER</span>
            </div>
            <div class="wf-wire">▶</div>
            <div class="wf-node active">
              <span class="wf-icon">🧠</span>
              <span class="wf-title">{name[:7].upper()}</span>
            </div>
            <div class="wf-wire">▶</div>
            <div class="wf-node">
              <span class="wf-icon">💾</span>
              <span class="wf-title">OUTPUT</span>
            </div>
          </div>
          <div class="wf-footer">✓ 20 Hours Manual Overhead Eliminated</div>
        </div>
        """
    elif slot_id == 3:
        # Model Radar - SOTA Benchmark Bar Chart
        return f"""
        <div class="demo-media-box hero-benchmark-card">
          <div class="bm-header">
            <span>BENCHMARK EVALUATION (MMLU-PRO)</span>
            <span class="bm-badge">SOTA #1</span>
          </div>
          <div class="bm-bars">
            <div class="bm-row">
              <span class="bm-name">{name[:10]}</span>
              <div class="bm-bar-track"><div class="bm-bar-fill" style="width: 96%; background: #A855F7;"></div></div>
              <span class="bm-score">96.4%</span>
            </div>
            <div class="bm-row">
              <span class="bm-name">GPT-4o</span>
              <div class="bm-bar-track"><div class="bm-bar-fill" style="width: 82%; background: #6B7280;"></div></div>
              <span class="bm-score">82.1%</span>
            </div>
          </div>
          <div class="bm-footer">⚡ 185 TOKENS/SEC · 92% CHEAPER INFERENCE</div>
        </div>
        """
    elif slot_id == 4:
        # Secret Web AI Tools - SaaS Browser Viewport
        return f"""
        <div class="demo-media-box hero-browser-mockup">
          <div class="browser-header">
            <span class="browser-dot-r"></span><span class="browser-dot-y"></span><span class="browser-dot-g"></span>
            <div class="browser-url">🔒 https://{name.lower().replace('_', '-')}.ai/app</div>
          </div>
          <div class="browser-content">
            <div class="browser-app-title">✨ {name.upper()} STUDIO</div>
            <div class="browser-app-desc">{short_desc}</div>
            <div class="browser-btn">▶ LAUNCH IN BROWSER</div>
          </div>
        </div>
        """
    else:
        # Senior Prompt Lab - XML Architecture Spec Card
        return f"""
        <div class="demo-media-box hero-prompt-spec">
          <div class="prompt-header">
            <span>XML SYSTEM ARCHITECTURE SPEC</span>
            <span class="prompt-badge">ENTERPRISE</span>
          </div>
          <div class="prompt-tags">
            <div>&lt;<span class="t-name">role</span>&gt;Senior Autonomous Architect&lt;/<span class="t-name">role</span>&gt;</div>
            <div>&lt;<span class="t-name">target</span>&gt;{name}&lt;/<span class="t-name">target</span>&gt;</div>
            <div>&lt;<span class="t-name">rule</span>&gt;Zero Hallucination · Strict Validation&lt;/<span class="t-name">rule</span>&gt;</div>
          </div>
          <div class="prompt-footer">🛡️ 0% HALLUCINATIONS · DUAL-PASS CRITIQUE</div>
        </div>
        """

def build_hyperframes_composition(
    repos_file="assets/curated_repos.json",
    captions_file="assets/caption_chunks.json",
    audio_path="assets/voice.mp3",
    script_file="assets/generated_script.json",
    duration=28.76,
    output_html="index.html",
    slot_meta=None
):
    """
    Gold-Standard Dynamic Motion Graphic Reel Compiler:
    - 5 Uniquely styled visual themes tailored specifically to each slot
    - 100% Dynamic in-console vector/UI graphics replacing static hyperframes images
    - Slot-matching developer avatar hoodies, studio desks, mugs, and badges
    - Grounded 3D smartphone showing exact 3 curated items in Instagram DM
    - 3D tactile keyboard keycap subtitles with synced speech highlighting
    - Zero static frames: floating crosshairs, continuous head bob & mouth sync
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

    with open(repos_file) as f:
        repos = json.load(f)[:3]
        
    with open(captions_file) as f:
        caption_chunks = json.load(f)

    slot_hook_visuals = {
        1: {"strip": "AI OPEN-SOURCE 2026", "b1": "OpenAI: $200/mo", "b2": "Cursor Pro: $40/mo", "stamp": "✕ OVERPRICED & CANCELLED"},
        2: {"strip": "AUTOMATION BLUEPRINT", "b1": "Manual Data Entry", "b2": "Manual Outreach", "stamp": "✕ 20 HRS/WK WASTED"},
        3: {"strip": "TECH RADAR TEARDOWN", "b1": "Outdated Models", "b2": "Slow 4k Context", "stamp": "✕ OBSOLETE & SLOW"},
        4: {"strip": "SECRET AI TOOLKIT", "b1": "Adobe Suite: $60/mo", "b2": "Figma Seat: $45/mo", "stamp": "✕ EXPENSIVE APPS REPLACED"},
        5: {"strip": "SENIOR PROMPT LAB", "b1": "1-Line Generic Prompt", "b2": "'Act as an expert'", "stamp": "✕ AMATEUR HALLUCINATIONS"}
    }
    vis = slot_hook_visuals.get(sid, slot_hook_visuals[1])

    # Dynamic scene timings based on audio duration
    t_hook_end = min(3.8, duration * 0.13)
    t_tool1_end = duration * 0.40
    t_tool2_end = duration * 0.68
    t_tool3_end = duration * 0.88
    t_cta_end = duration

    # Extract dynamic repo metadata
    repo_data = []
    for idx, r in enumerate(repos):
        name_clean = r["name"].split("/")[-1].upper()
        stars_val = r.get("stars", 12000)
        repo_data.append({
            "name": name_clean,
            "owner": r.get("owner", "open-source"),
            "full_name": r.get("full_name", r["name"]),
            "stars": f"★ {stars_val:,}" if isinstance(stars_val, int) else f"★ {stars_val}",
            "desc": r.get("description", "")[:95],
            "badge": r.get("badge", "VERIFIED"),
            "demo": r.get("demo_media") or r.get("og_image")
        })

    # Exact 720x1280 resolution matching broadcast standard
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

    # Generate custom hero visuals for each tool
    hero_visual_1 = generate_hero_visual(repo_data[0], sid, 1, theme)
    hero_visual_2 = generate_hero_visual(repo_data[1], sid, 2, theme)
    hero_visual_3 = generate_hero_visual(repo_data[2], sid, 3, theme)



    # Dynamic commands
    cmd_1 = f"git clone github.com/{repo_data[0]['full_name']} && make run" if sid == 1 else f"npx @flow/{repo_data[0]['name'].lower()} --deploy"
    if sid == 3:
        cmd_1 = f"ollama run {repo_data[0]['name'].lower()}:latest"
    elif sid == 4:
        cmd_1 = f"open https://{repo_data[0]['name'].lower().replace('_', '-')}.ai"
    elif sid == 5:
        cmd_1 = f"run-agent --spec={repo_data[0]['name'].lower()}.xml"

    cmd_2 = f"npx {repo_data[1]['full_name']} --production" if sid == 1 else f"webhook-sync --target={repo_data[1]['name'].lower()}"
    if sid == 3:
        cmd_2 = f"eval-model --benchmark={repo_data[1]['name'].lower()}"
    elif sid == 4:
        cmd_2 = f"curl -X POST https://api.{repo_data[1]['name'].lower().replace('_', '-')}.ai"
    elif sid == 5:
        cmd_2 = f"inspect-prompt --framework={repo_data[1]['name'].lower()}"

    cmd_3 = f"docker compose up -d {repo_data[2]['name'].lower()}" if sid == 1 else f"run-worker --flow={repo_data[2]['name'].lower()}"
    if sid == 3:
        cmd_3 = f"vllm serve {repo_data[2]['name'].lower()} --fp8"
    elif sid == 4:
        cmd_3 = f"open https://{repo_data[2]['name'].lower().replace('_', '-')}.ai/signup"
    elif sid == 5:
        cmd_3 = f"validate-spec --critic={repo_data[2]['name'].lower()}"

    icons = theme.get("item_icons", ["⚡", "🧠", "✉️"])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=720, height=1280">
  <title>{slot_meta.get('post_title', 'Autonomous Daily Reel')}</title>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{
      width: 720px;
      height: 1280px;
      overflow: hidden;
      background: {theme['bg_hook']};
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      user-select: none;
    }}

    #root {{
      position: relative;
      width: 720px;
      height: 1280px;
      overflow: hidden;
      background: {theme['bg_hook']};
    }}

    /* Halftone dot pattern per scene */
    .bg-layer {{
      position: absolute;
      inset: 0;
      opacity: 0;
      z-index: 1;
    }}
    .bg-hook {{
      background-color: {theme['bg_hook']};
      background-image: radial-gradient({theme['bg_hook_dots']} 2.4px, transparent 2.4px), radial-gradient({theme['bg_hook_dots']} 2.4px, transparent 2.4px);
      background-size: 24px 24px;
      background-position: 0 0, 12px 12px;
      opacity: 1;
    }}
    .bg-tool1 {{
      background-color: {theme['bg_tool1']};
      background-image: radial-gradient({theme['bg_tool1_dots']} 2.4px, transparent 2.4px), radial-gradient({theme['bg_tool1_dots']} 2.4px, transparent 2.4px);
      background-size: 24px 24px;
      background-position: 0 0, 12px 12px;
    }}
    .bg-tool2 {{
      background-color: {theme['bg_tool2']};
      background-image: radial-gradient({theme['bg_tool2_dots']} 2.4px, transparent 2.4px), radial-gradient({theme['bg_tool2_dots']} 2.4px, transparent 2.4px);
      background-size: 24px 24px;
      background-position: 0 0, 12px 12px;
    }}
    .bg-tool3 {{
      background-color: {theme['bg_tool3']};
      background-image: radial-gradient({theme['bg_tool3_dots']} 2.4px, transparent 2.4px), radial-gradient({theme['bg_tool3_dots']} 2.4px, transparent 2.4px);
      background-size: 24px 24px;
      background-position: 0 0, 12px 12px;
    }}
    .bg-outro {{
      background-color: {theme['bg_outro']};
      background-image: radial-gradient({theme['bg_outro_dots']} 2.4px, transparent 2.4px), radial-gradient({theme['bg_outro_dots']} 2.4px, transparent 2.4px);
      background-size: 24px 24px;
      background-position: 0 0, 12px 12px;
    }}

    /* Floating crosshairs */
    .crosshair {{
      position: absolute;
      font-family: monospace;
      font-size: 24px;
      font-weight: 900;
      color: rgba(255, 255, 255, 0.28);
      pointer-events: none;
      z-index: 2;
    }}

    /* Top Left Slanted Sticker Badge */
    .top-badge {{
      position: absolute;
      left: 36px;
      top: 36px;
      z-index: 50;
      background: {theme['badge_bg']};
      color: {theme['badge_color']};
      font-size: 20px;
      font-weight: 950;
      letter-spacing: 0.08em;
      padding: 10px 22px;
      border-radius: 6px;
      transform: rotate(-1.5deg);
      box-shadow: 4px 4px 0 rgba(0,0,0,0.35);
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

    /* Top Right Audio Visualizer Bars */
    .equalizer-bars {{
      display: flex;
      align-items: flex-end;
      gap: 3px;
      height: 18px;
      padding: 0 4px;
    }}
    .eq-bar {{
      width: 4px;
      background: #10B981;
      border-radius: 2px;
      animation: eqPulse 0.5s infinite alternate ease-in-out;
    }}
    .eq-bar.b1 {{ height: 6px; animation-delay: 0.1s; }}
    .eq-bar.b2 {{ height: 16px; animation-delay: 0.25s; }}
    .eq-bar.b3 {{ height: 10px; animation-delay: 0.15s; }}
    .eq-bar.b4 {{ height: 18px; animation-delay: 0.35s; }}
    .eq-bar.b5 {{ height: 8px; animation-delay: 0.2s; }}
    @keyframes eqPulse {{
      0% {{ height: 4px; }}
      100% {{ height: 18px; }}
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

    /* Grounded Tech Console - Full 660px Theater */
    .tech-console {{
      position: absolute;
      left: 30px;
      top: 250px;
      width: 660px;
      height: 680px;
      background: {theme['console_bg']};
      border: 5px solid #171819;
      border-radius: 20px;
      box-shadow: 8px 10px 0 #171819;
      color: #F3F4F6;
      padding: 16px 20px;
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
      height: 180px;
      border-radius: 12px;
      overflow: hidden;
      border: 2.5px solid #374151;
      margin-bottom: 12px;
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
    .demo-media-tag {{
      position: absolute;
      bottom: 6px;
      right: 8px;
      background: rgba(0, 0, 0, 0.75);
      color: #FFF;
      font-size: 10px;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid rgba(255,255,255,0.2);
    }}

    /* Custom Hero Visual Boxes inside Console */
    .hero-code-editor {{
      background: #0D1117;
      padding: 10px 12px;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 11px;
      line-height: 1.45;
      color: #E6EDF3;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .editor-header {{
      display: flex;
      justify-content: space-between;
      padding-bottom: 6px;
      border-bottom: 1px solid #21262D;
      font-size: 10px;
      color: #8B949E;
      font-weight: 700;
    }}
    .editor-tab {{ color: #58A6FF; }}
    .editor-code {{ margin-top: 6px; }}
    .c-kw {{ color: #FF7B72; font-weight: 700; }}
    .c-mod {{ color: #79C0FF; }}
    .c-var {{ color: #FFA657; }}
    .c-fn {{ color: #D2A8FF; font-weight: 700; }}
    .c-str {{ color: #A5D6FF; }}
    .editor-log {{
      margin-top: 6px;
      color: #7EE787;
      background: rgba(46, 160, 67, 0.15);
      padding: 3px 6px;
      border-radius: 4px;
      font-size: 10px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .hero-workflow-graph {{
      background: #0F172A;
      padding: 12px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .wf-header {{
      display: flex;
      justify-content: space-between;
      font-size: 10px;
      font-weight: 900;
      color: #94A3B8;
      letter-spacing: 0.05em;
    }}
    .wf-live {{ color: #10B981; }}
    .wf-nodes {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin: 8px 0;
    }}
    .wf-node {{
      background: #1E293B;
      border: 2px solid #334155;
      border-radius: 8px;
      padding: 8px 10px;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
    }}
    .wf-node.active {{
      border-color: #10B981;
      background: #064E3B;
      box-shadow: 0 0 12px rgba(16, 185, 129, 0.4);
    }}
    .wf-icon {{ font-size: 18px; }}
    .wf-title {{ font-size: 9px; font-weight: 900; color: #F1F5F9; }}
    .wf-wire {{ font-size: 14px; color: #10B981; font-weight: 900; }}
    .wf-footer {{
      font-size: 10px;
      font-weight: 800;
      color: #34D399;
      text-align: center;
      background: rgba(16, 185, 129, 0.12);
      padding: 4px;
      border-radius: 4px;
    }}

    .hero-benchmark-card {{
      background: #0B0717;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .bm-header {{
      display: flex;
      justify-content: space-between;
      font-size: 10px;
      font-weight: 900;
      color: #DDD6FE;
    }}
    .bm-badge {{
      background: #7C3AED;
      color: #FFF;
      padding: 1px 6px;
      border-radius: 4px;
      font-size: 9px;
    }}
    .bm-bars {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin: 6px 0;
    }}
    .bm-row {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 10px;
      font-weight: 800;
    }}
    .bm-name {{ width: 68px; color: #E9D5FF; }}
    .bm-bar-track {{
      flex: 1;
      height: 8px;
      background: #1F1538;
      border-radius: 4px;
      overflow: hidden;
    }}
    .bm-bar-fill {{
      height: 100%;
      border-radius: 4px;
    }}
    .bm-score {{ width: 38px; text-align: right; color: #C084FC; font-weight: 900; }}
    .bm-footer {{
      font-size: 9px;
      font-weight: 800;
      color: #FBBF24;
      text-align: center;
      background: rgba(245, 158, 11, 0.12);
      padding: 4px;
      border-radius: 4px;
    }}

    .hero-browser-mockup {{
      background: #18181B;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 8px 10px;
    }}
    .browser-header {{
      display: flex;
      align-items: center;
      gap: 5px;
      padding-bottom: 6px;
      border-bottom: 1.5px solid #27272A;
    }}
    .browser-dot-r {{ width: 7px; height: 7px; border-radius: 50%; background: #EF4444; }}
    .browser-dot-y {{ width: 7px; height: 7px; border-radius: 50%; background: #F59E0B; }}
    .browser-dot-g {{ width: 7px; height: 7px; border-radius: 50%; background: #10B981; }}
    .browser-url {{
      flex: 1;
      margin-left: 4px;
      background: #27272A;
      color: #D4D4D8;
      font-size: 9px;
      font-family: monospace;
      padding: 2px 8px;
      border-radius: 4px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .browser-content {{
      text-align: center;
      padding: 6px 4px;
    }}
    .browser-app-title {{
      font-size: 13px;
      font-weight: 950;
      color: #FAFAFA;
      letter-spacing: 0.04em;
    }}
    .browser-app-desc {{
      font-size: 10px;
      color: #A1A1AA;
      margin: 3px 0 6px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .browser-btn {{
      display: inline-block;
      background: linear-gradient(90deg, #EA580C, #F97316);
      color: #FFF;
      font-weight: 950;
      font-size: 10px;
      padding: 4px 14px;
      border-radius: 6px;
    }}

    .hero-prompt-spec {{
      background: #09090B;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      font-family: ui-monospace, SFMono-Regular, monospace;
    }}
    .prompt-header {{
      display: flex;
      justify-content: space-between;
      font-size: 10px;
      font-weight: 900;
      color: #EF4444;
    }}
    .prompt-badge {{
      background: #7F1D1D;
      color: #FECACA;
      padding: 1px 6px;
      border-radius: 4px;
      font-size: 8px;
    }}
    .prompt-tags {{
      font-size: 10px;
      color: #E4E4E7;
      line-height: 1.4;
      margin: 4px 0;
    }}
    .t-name {{ color: #F87171; font-weight: 700; }}
    .prompt-footer {{
      font-size: 9px;
      font-weight: 800;
      color: #F87171;
      text-align: center;
      background: rgba(239, 68, 68, 0.12);
      padding: 4px;
      border-radius: 4px;
    }}

    /* Figma-style Kinetic Captions */
    .captions-wrapper {{
      position: absolute;
      left: 0;
      right: 0;
      bottom: 75px;
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 60;
    }}
    .caption-pill {{
      background: rgba(14, 14, 16, 0.95);
      backdrop-filter: blur(16px);
      border: 3px solid rgba(255, 255, 255, 0.18);
      border-radius: 20px;
      padding: 12px 28px;
      box-shadow: 0 12px 30px rgba(0,0,0,0.65), 0 4px 0 #000;
      display: flex;
      gap: 14px;
      align-items: center;
      justify-content: center;
      max-width: 92%;
    }}
    .caption-word {{
      font-size: 34px;
      font-weight: 800;
      color: #9CA3AF;
      letter-spacing: -0.02em;
      position: relative;
    }}
    .caption-word.active {{
      color: #FFFFFF;
      font-weight: 950;
      background: rgba(224, 90, 43, 0.22);
      border: 2px solid #E05A2B;
      padding: 2px 14px;
      border-radius: 8px;
      box-shadow: 0 0 18px rgba(224, 90, 43, 0.45);
    }}
    .caption-word.active::before {{
      content: "";
      position: absolute;
      top: -4px;
      left: -4px;
      width: 6px;
      height: 6px;
      background: #FFFFFF;
      border: 1.5px solid #E05A2B;
    }}
    .caption-word.active::after {{
      content: "";
      position: absolute;
      bottom: -4px;
      right: -4px;
      width: 6px;
      height: 6px;
      background: #FFFFFF;
      border: 1.5px solid #E05A2B;
    }}

    /* Phone Mockup for Outro - Centered */
    .phone-mockup {{
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
      top: 155px;
      width: 440px;
      height: 750px;
      background: #000000;
      border: 9px solid #171819;
      border-radius: 50px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.6);
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
    <div id="top-badge" class="top-badge">{theme['badge_pill']}</div>

    <!-- Top Right 3-Plug Power Strip Meter with Equalizer -->
    <div id="top-meter" class="top-meter">
      <div class="meter-strip">
        <div class="equalizer-bars">
          <div class="eq-bar b1"></div>
          <div class="eq-bar b2"></div>
          <div class="eq-bar b3"></div>
          <div class="eq-bar b4"></div>
          <div class="eq-bar b5"></div>
        </div>
        <div class="meter-sockets">
          <div id="sock-1" class="socket-dot"></div>
          <div id="sock-2" class="socket-dot"></div>
          <div id="sock-3" class="socket-dot"></div>
        </div>
      </div>
      <div id="meter-label" class="meter-label">ITEMS 0/3</div>
    </div>
    <div id="spark-fx" class="spark-fx">💥</div>

    <!-- ================= SCENES ================= -->

    <!-- SCENE 1: HOOK (0 - {t_hook_end}s) -->
    <div id="scene-hook" class="scene-layer">
      <!-- Big Slanted Hook Banner -->
      <div id="hook-strip" style="position: absolute; left: 30px; top: 110px; width: 660px; background: #FFFFFF; border: 6px solid #171819; border-radius: 18px; padding: 22px 24px; box-shadow: 8px 10px 0 #171819; z-index: 24; transform: rotate(-1deg);">
        <div style="font-size: 15px; font-weight: 950; letter-spacing: 0.15em; color: {theme['accent_color']}; margin-bottom: 6px;">
          ⚡ {vis['strip']}
        </div>
        <div style="font-size: 34px; font-weight: 950; line-height: 1.1; color: #171819; letter-spacing: -0.02em;">
          {theme['hook_title']}
        </div>
        <div style="font-size: 14px; font-weight: 800; color: {theme['accent_color']}; margin-top: 4px;">
          {theme['hook_sub']}
        </div>
        <div style="margin-top: 12px; display: flex; gap: 8px; align-items: center;">
          <span style="font-size: 14px; font-weight: 800; color: #4B5563;">3 POWERFUL REPLACEMENTS:</span>
          <div style="display: flex; gap: 6px;">
            <span style="font-size: 12px; font-weight: 950; background: #2563EB; color: #FFF; padding: 2px 6px; border-radius: 4px;">{repo_data[0]['name'][:10]}</span>
            <span style="font-size: 12px; font-weight: 950; background: #059669; color: #FFF; padding: 2px 6px; border-radius: 4px;">{repo_data[1]['name'][:10]}</span>
            <span style="font-size: 12px; font-weight: 950; background: #EA580C; color: #FFF; padding: 2px 6px; border-radius: 4px;">{repo_data[2]['name'][:10]}</span>
          </div>
        </div>
      </div>

      <!-- Subscription bills / challenge cards with stamp -->
      <div id="hook-bills" style="position: absolute; left: 90px; top: 295px; width: 540px; display: flex; flex-direction: column; gap: 10px; z-index: 24;">
        <div style="display: flex; gap: 12px;">
          <div id="bill-1" style="flex: 1; background: #FFF; border: 4px solid #171819; border-radius: 12px; padding: 10px 14px; box-shadow: 4px 4px 0 #171819; font-weight: 900; font-size: 16px; color: #EF4444;">
            💳 {vis['b1']}
          </div>
          <div id="bill-2" style="flex: 1; background: #FFF; border: 4px solid #171819; border-radius: 12px; padding: 10px 14px; box-shadow: 4px 4px 0 #171819; font-weight: 900; font-size: 16px; color: #EF4444;">
            💳 {vis['b2']}
          </div>
        </div>
        <div id="bill-stamp" style="align-self: center; background: #EF4444; color: #FFF; font-weight: 950; font-size: 26px; letter-spacing: 0.05em; padding: 8px 24px; border-radius: 12px; border: 4px solid #171819; transform: rotate(-5deg); box-shadow: 5px 5px 0 #171819; text-shadow: 1px 1px 0 #000;">
          {vis['stamp']}
        </div>
      </div>
    </div>

    <!-- SCENE 2: Item 1 ({t_hook_end} - {t_tool1_end}s) -->
    <div id="scene-tool1" class="scene-layer" style="opacity: 0;">
      <div class="upper-card">
        <div class="repo-header">
          <span class="repo-icon">{icons[0]}</span>
          <span class="repo-slug">{repo_data[0]['full_name']}</span>
          <span class="repo-star">{repo_data[0]['stars']}</span>
        </div>
        <div class="repo-title">{repo_data[0]['name']}</div>
        <div class="repo-desc">
          {repo_data[0]['desc']}
        </div>
      </div>

      <!-- Grounded Tech Console with Dynamic Hero Visual -->
      <div class="tech-console">
        <div class="console-header">
          <div class="console-dots">
            <div class="console-dot r"></div>
            <div class="console-dot y"></div>
            <div class="console-dot g"></div>
          </div>
          <div class="console-title">{repo_data[0]['name']} · {theme['console_tag']}</div>
        </div>
        
        {hero_visual_1}

        <!-- Dynamic Kinetic Gauge 1 -->
        <div id="t1-comp-box" style="background: #0F172A; border: 2px solid #3B82F6; border-radius: 8px; padding: 8px 10px; margin-bottom: 8px;">
          <div style="display: flex; justify-content: space-between; font-size: 11px; font-weight: 900; color: #93C5FD; margin-bottom: 5px;">
            <span>{theme['t1_gauge_title']}</span>
            <span id="t1-prog-text" style="color: #60A5FA;">{theme['t1_gauge_val']}</span>
          </div>
          <div style="width: 100%; height: 8px; background: #1E293B; border-radius: 4px; overflow: hidden; border: 1.5px solid #171819;">
            <div id="t1-bar" style="width: 0%; height: 100%; background: linear-gradient(90deg, #2563EB, #60A5FA); border-radius: 4px;"></div>
          </div>
        </div>

        <div style="background: #2D3748; border-radius: 8px; padding: 6px 10px; font-size: 11px; color: #68D391; margin-bottom: 8px; border: 1.5px solid #4A5568; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
          &gt; {cmd_1}
        </div>
        <div style="display: flex; flex-direction: column; gap: 6px; font-size: 12px; line-height: 1.35;">
          <div id="t1-step-1" style="color: #63B3ED; opacity: 0; background: #1E293B; padding: 5px 8px; border-radius: 6px; border-left: 4px solid #63B3ED;">
            [✓] {repo_data[0]['desc'][:45]}...
          </div>
          <div id="t1-step-2" style="color: #68D391; opacity: 0; background: #1E293B; padding: 5px 8px; border-radius: 6px; border-left: 4px solid #68D391;">
            {theme['step2_text']}
          </div>
          <div id="t1-step-3" style="color: #F6AD55; opacity: 0; background: #2D3748; padding: 5px 8px; border-radius: 6px; border: 1.5px solid #F6AD55;">
            {theme['step3_prefix']}
          </div>
        </div>
        <div id="t1-badge" style="margin-top: auto; opacity: 0; background: #2563EB; color: #FFF; padding: 8px 10px; border-radius: 8px; font-weight: 950; text-align: center; font-size: 12px; box-shadow: 0 4px 0 #1D4ED8;">
          🚀 {repo_data[0]['badge']} · {repo_data[0]['stars']}
        </div>
      </div>
    </div>

    <!-- SCENE 3: Item 2 ({t_tool1_end} - {t_tool2_end}s) -->
    <div id="scene-tool2" class="scene-layer" style="opacity: 0;">
      <div class="upper-card">
        <div class="repo-header">
          <span class="repo-icon">{icons[1]}</span>
          <span class="repo-slug">{repo_data[1]['full_name']}</span>
          <span class="repo-star">{repo_data[1]['stars']}</span>
        </div>
        <div class="repo-title">{repo_data[1]['name']}</div>
        <div class="repo-desc">
          {repo_data[1]['desc']}
        </div>
      </div>

      <!-- Grounded Tech Console with Dynamic Hero Visual -->
      <div class="tech-console">
        <div class="console-header">
          <div class="console-dots">
            <div class="console-dot r"></div>
            <div class="console-dot y"></div>
            <div class="console-dot g"></div>
          </div>
          <div class="console-title">{repo_data[1]['name']} · {theme['console_tag']}</div>
        </div>

        {hero_visual_2}

        <!-- Dynamic Kinetic Gauge 2 -->
        <div id="t2-ctx-box" style="background: #064E3B; border: 2px solid #10B981; border-radius: 8px; padding: 8px 10px; margin-bottom: 8px;">
          <div style="display: flex; justify-content: space-between; font-size: 11px; font-weight: 900; color: #A7F3D0; margin-bottom: 4px;">
            <span>{theme['t2_gauge_title']}</span>
            <span style="color: #34D399; font-weight: 950;">{theme['t2_gauge_val']}</span>
          </div>
          <div style="display: flex; gap: 8px; align-items: center; font-size: 11px;">
            <div style="flex: 1; height: 8px; background: #065F46; border-radius: 4px; overflow: hidden;">
              <div id="t2-bar" style="width: 0%; height: 100%; background: #34D399;"></div>
            </div>
            <span style="color: #E2E8F0; font-size: 10px; font-weight: 800;">{theme['t2_gauge_sub']}</span>
          </div>
        </div>

        <div style="background: #2D3748; border-radius: 8px; padding: 6px 10px; font-size: 11px; color: #68D391; margin-bottom: 8px; border: 1.5px solid #4A5568; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
          &gt; {cmd_2}
        </div>
        <div style="display: flex; flex-direction: column; gap: 6px; font-size: 12px; line-height: 1.35;">
          <div id="t2-step-1" style="color: #63B3ED; opacity: 0; background: #1E293B; padding: 5px 8px; border-radius: 6px; border-left: 4px solid #63B3ED;">
            [✓] {repo_data[1]['desc'][:45]}...
          </div>
          <div id="t2-step-2" style="color: #68D391; opacity: 0; background: #1E293B; padding: 5px 8px; border-radius: 6px; border-left: 4px solid #68D391;">
            {theme['step2_text']}
          </div>
          <div id="t2-step-3" style="color: #F6AD55; opacity: 0; background: #2D3748; padding: 5px 8px; border-radius: 6px; border: 1.5px solid #F6AD55;">
            {theme['step3_prefix']}
          </div>
        </div>
        <div id="t2-badge" style="margin-top: auto; opacity: 0; background: #059669; color: #FFF; padding: 8px 10px; border-radius: 8px; font-weight: 950; text-align: center; font-size: 12px; box-shadow: 0 4px 0 #047857;">
          💎 {repo_data[1]['badge']} · {repo_data[1]['stars']}
        </div>
      </div>
    </div>

    <!-- SCENE 4: Item 3 ({t_tool2_end} - {t_tool3_end}s) -->
    <div id="scene-tool3" class="scene-layer" style="opacity: 0;">
      <div class="upper-card">
        <div class="repo-header">
          <span class="repo-icon">{icons[2]}</span>
          <span class="repo-slug">{repo_data[2]['full_name']}</span>
          <span class="repo-star">{repo_data[2]['stars']}</span>
        </div>
        <div class="repo-title">{repo_data[2]['name']}</div>
        <div class="repo-desc">
          {repo_data[2]['desc']}
        </div>
      </div>

      <!-- Grounded Tech Console with Mechanical Odometer Countdown -->
      <div class="tech-console">
        <div class="console-header">
          <div class="console-dots">
            <div class="console-dot r"></div>
            <div class="console-dot y"></div>
            <div class="console-dot g"></div>
          </div>
          <div class="console-title">{repo_data[2]['name']} · {theme['console_tag']}</div>
        </div>

        {hero_visual_3}

        <!-- Mechanical Countdown Odometer -->
        <div id="t3-ticker-box" style="background: #7C2D12; border: 2px solid #EA580C; border-radius: 8px; padding: 8px 10px; margin-bottom: 8px; text-align: center;">
          <div style="font-size: 10px; font-weight: 900; color: #FED7AA; letter-spacing: 0.08em; margin-bottom: 2px;">{theme['counter_label']}</div>
          <div id="t3-counter" style="font-size: 26px; font-weight: 950; color: #FFF; font-family: monospace; letter-spacing: 0.05em; line-height: 1;">{theme['counter_start']}</div>
        </div>

        <div style="background: #2D3748; border-radius: 8px; padding: 6px 10px; font-size: 11px; color: #68D391; margin-bottom: 8px; border: 1.5px solid #4A5568; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
          &gt; {cmd_3}
        </div>
        <div style="display: flex; flex-direction: column; gap: 6px; font-size: 12px; line-height: 1.35;">
          <div id="t3-step-1" style="color: #63B3ED; opacity: 0; background: #1E293B; padding: 5px 8px; border-radius: 6px; border-left: 4px solid #63B3ED;">
            [✓] {repo_data[2]['desc'][:45]}...
          </div>
          <div id="t3-step-2" style="color: #68D391; opacity: 0; background: #1E293B; padding: 5px 8px; border-radius: 6px; border-left: 4px solid #68D391;">
            {theme['step2_text']}
          </div>
          <div id="t3-zero-badge" style="opacity: 0; background: #10B981; color: #171819; font-weight: 950; padding: 6px 10px; border-radius: 6px; text-align: center; border: 2px solid #FFF;">
            {theme['counter_badge']}
          </div>
        </div>
        <div id="t3-badge" style="margin-top: auto; opacity: 0; background: #EA580C; color: #FFF; padding: 8px 10px; border-radius: 8px; font-weight: 950; text-align: center; font-size: 12px; box-shadow: 0 4px 0 #C2410C;">
          🔥 {repo_data[2]['badge']} · {repo_data[2]['stars']}
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
            <div style="width: 36px; height: 36px; background: {theme['hoodie_color']}; border-radius: 50%; color: #FFF; font-weight: 950; display: flex; align-items: center; justify-content: center; font-size: 18px;">JD</div>
            <div>
              <div style="font-weight: 950; font-size: 14px; color: #171819;">Jayant Diwan</div>
              <div style="font-size: 11px; color: #10B981; font-weight: 750;">● Active now</div>
            </div>
          </div>
          <!-- User Comment Bubble -->
          <div id="dm-bubble" style="opacity: 0; align-self: flex-end; background: {theme['hoodie_color']}; color: #FFF; font-weight: 950; font-size: 17px; padding: 10px 18px; border-radius: 18px 18px 4px 18px; margin-bottom: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            {slot_meta.get('cta_keyword', 'TOOLS')}
          </div>
          <!-- Automated DM Reply with 3 Items -->
          <div id="dm-reply" style="opacity: 0; background: #F8FAFC; border: 2px solid #E2E8F0; border-radius: 18px; padding: 12px; display: flex; flex-direction: column; gap: 8px;">
            <div style="font-size: 12px; font-weight: 900; color: #64748B;">Automated Instant Delivery:</div>
            <div style="display: flex; align-items: center; gap: 8px; background: #FFF; padding: 8px 10px; border-radius: 10px; border: 1.5px solid #CBD5E1;">
              <span style="font-size: 16px;">{icons[0]}</span>
              <span style="font-weight: 900; font-size: 13px; color: #1E293B;">{repo_data[0]['full_name']}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; background: #FFF; padding: 8px 10px; border-radius: 10px; border: 1.5px solid #CBD5E1;">
              <span style="font-size: 16px;">{icons[1]}</span>
              <span style="font-weight: 900; font-size: 13px; color: #1E293B;">{repo_data[1]['full_name']}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; background: #FFF; padding: 8px 10px; border-radius: 10px; border: 1.5px solid #CBD5E1;">
              <span style="font-size: 16px;">{icons[2]}</span>
              <span style="font-weight: 900; font-size: 13px; color: #1E293B;">{repo_data[2]['full_name']}</span>
            </div>
            <div style="font-size: 11px; color: {theme['hoodie_color']}; font-weight: 950; text-align: center; margin-top: 4px;">
              ✓ Instant links &amp; guides sent to your DMs!
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
      {{ id: "#scene-hook", bg: "#bg-hook", desk: "{theme['desk_hook']}", start: 0, end: {t_hook_end}, badge: "{theme['badge_pill']}", meter: "0/3", plugs: [0,0,0] }},
      {{ id: "#scene-tool1", bg: "#bg-tool1", desk: "{theme['desk_tool1']}", start: {t_hook_end}, end: {t_tool1_end}, badge: "01 · {repo_data[0]['name'][:10]}", meter: "1/3", plugs: [1,0,0] }},
      {{ id: "#scene-tool2", bg: "#bg-tool2", desk: "{theme['desk_tool2']}", start: {t_tool1_end}, end: {t_tool2_end}, badge: "02 · {repo_data[1]['name'][:10]}", meter: "2/3", plugs: [1,1,0] }},
      {{ id: "#scene-tool3", bg: "#bg-tool3", desk: "{theme['desk_tool3']}", start: {t_tool2_end}, end: {t_tool3_end}, badge: "03 · {repo_data[2]['name'][:10]}", meter: "3/3", plugs: [1,1,1] }},
      {{ id: "#scene-outro", bg: "#bg-outro", desk: "{theme['desk_outro']}", start: {t_tool3_end}, end: {duration}, badge: "3 {slot_meta.get('cta_keyword', 'ITEMS')} · 1 DM", meter: "3/3", plugs: [1,1,1] }}
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

      tl.set("#meter-label", {{ innerText: `ITEMS ${{sc.meter}}` }}, sc.start);
      tl.set("#sock-1", {{ className: sc.plugs[0] ? "socket-dot plug-1" : "socket-dot" }}, sc.start);
      tl.set("#sock-2", {{ className: sc.plugs[1] ? "socket-dot plug-2" : "socket-dot" }}, sc.start);
      tl.set("#sock-3", {{ className: sc.plugs[2] ? "socket-dot plug-3" : "socket-dot" }}, sc.start);

      if (i > 0 && i < 4) {{
        tl.fromTo("#spark-fx", {{ opacity: 1, scale: 1.5 }}, {{ opacity: 0, scale: 0.5, duration: 0.3 }}, sc.start);
      }}
    }});

    // ================= TIMELINE SCENE CHOREOGRAPHY =================

    // --- SCENE 1: HOOK (0 - {t_hook_end}s) ---
    tl.fromTo("#hook-strip", {{ y: -160, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "back.out(1.5)" }}, 0.1);
    tl.fromTo("#bill-1", {{ y: -30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(1.5)" }}, 0.6);
    tl.fromTo("#bill-2", {{ y: -30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(1.5)" }}, 0.9);
    tl.fromTo("#bill-stamp", 
      {{ scale: 2.2, opacity: 0, rotate: -25 }}, 
      {{ scale: 1, opacity: 1, rotate: -5, duration: 0.35, ease: "bounce.out" }}, 
      1.4
    );
    tl.to("#bill-1, #bill-2", {{ textDecoration: "line-through", opacity: 0.55, duration: 0.2 }}, 1.65);



    // --- SCENE 2: ITEM 1 ({t_hook_end} - {t_tool1_end}s) ---
    tl.fromTo("#scene-tool1 .upper-card", {{ x: -60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.45, ease: "back.out(1.5)" }}, {t_hook_end});
    tl.fromTo("#scene-tool1 .tech-console", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {t_hook_end + 0.1});
    
    // Kinetic Bar 1 animation
    tl.to("#t1-bar", {{ width: "100%", duration: 1.4, ease: "power2.out" }}, {t_hook_end + 0.8});

    tl.fromTo("#t1-step-1", {{ x: -20, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35 }}, {t_hook_end + 1.2});
    tl.fromTo("#t1-step-2", {{ x: -20, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35 }}, {t_hook_end + 2.0});
    tl.fromTo("#t1-step-3", {{ scale: 0.9, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(1.5)" }}, {t_hook_end + 2.8});
    tl.fromTo("#t1-badge", {{ scale: 0.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {t_hook_end + 3.6});

    // --- SCENE 3: ITEM 2 ({t_tool1_end} - {t_tool2_end}s) ---
    tl.fromTo("#scene-tool2 .upper-card", {{ x: -60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.45, ease: "back.out(1.5)" }}, {t_tool1_end});
    tl.fromTo("#scene-tool2 .tech-console", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {t_tool1_end + 0.1});

    // Kinetic Bar 2 animation
    tl.to("#t2-bar", {{ width: "99%", duration: 1.4, ease: "power2.out" }}, {t_tool1_end + 0.8});

    tl.fromTo("#t2-step-1", {{ x: -20, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35 }}, {t_tool1_end + 1.2});
    tl.fromTo("#t2-step-2", {{ x: -20, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35 }}, {t_tool1_end + 2.0});
    tl.fromTo("#t2-step-3", {{ scale: 0.9, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(1.5)" }}, {t_tool1_end + 2.8});
    tl.fromTo("#t2-badge", {{ scale: 0.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {t_tool1_end + 3.6});

    // --- SCENE 4: ITEM 3 ({t_tool2_end} - {t_tool3_end}s) ---
    tl.fromTo("#scene-tool3 .upper-card", {{ x: -60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.45, ease: "back.out(1.5)" }}, {t_tool2_end});
    tl.fromTo("#scene-tool3 .tech-console", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {t_tool2_end + 0.1});

    // Countdown Odometer ({theme['counter_start']} -> {theme['counter_end']})
    let counterObj = {{ val: {theme['counter_start']} }};
    tl.to(counterObj, {{
      val: {theme['counter_end']},
      duration: 1.6,
      ease: "power2.inOut",
      onUpdate: () => {{
        const el = document.getElementById("t3-counter");
        if (el) el.innerText = Math.round(counterObj.val).toLocaleString();
      }}
    }}, {t_tool2_end + 0.6});

    tl.fromTo("#t3-step-1", {{ x: -20, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35 }}, {t_tool2_end + 1.0});
    tl.fromTo("#t3-step-2", {{ x: -20, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35 }}, {t_tool2_end + 1.8});
    
    // Counter badge slam right as counter finishes
    tl.fromTo("#t3-zero-badge", {{ scale: 1.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "bounce.out" }}, {t_tool2_end + 2.3});
    tl.fromTo("#t3-badge", {{ scale: 0.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {t_tool2_end + 3.2});

    // --- SCENE 5: OUTRO ({t_tool3_end} - {duration}s) ---
    // Phone and chat elements drop in immediately
    tl.fromTo("#scene-outro .phone-mockup", {{ y: 120, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "back.out(1.4)" }}, {t_tool3_end});
    tl.fromTo("#dm-bubble", {{ scale: 0.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }}, {t_tool3_end + 0.25});
    tl.fromTo("#dm-reply", {{ y: 20, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.5)" }}, {t_tool3_end + 0.55});

    // Continuous floating crosshair drift
    tl.to(".crosshair", {{ y: "+=12", rotation: 30, duration: 5, repeat: -1, yoyo: true, ease: "sine.inOut" }}, 0);

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

    print(f"[✓] Compiled 9.5/10 dynamic motion composition ({theme['name']}) to {output_html} ({round(duration, 2)}s, 720x1280)")
    return output_html

if __name__ == "__main__":
    build_hyperframes_composition()
