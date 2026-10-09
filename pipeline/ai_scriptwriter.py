import os
import json
import re
import requests

def get_gemini_key():
    key = os.environ.get("GEMINI_API_KEY")
    if not key and os.path.exists(".gemini_key"):
        with open(".gemini_key") as f:
            key = f.read().strip()
    return key

def sanitize_voice_script(text: str) -> str:
    """
    Strips any accidental URLs, markdown, repo slashes, and symbols that sound robotic in TTS.
    """
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"github\.com/\S+", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"[#*_~`><]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def generate_viral_script_with_gemini(items: list, trending_samples: list = None, slot_meta: dict = None) -> dict:
    """
    Uses Gemini to synthesize top creator transcripts and slot items into a 
    high-retention viral 38-to-42 second voiceover script tailored to the slot theme.
    """
    if trending_samples is None:
        trending_samples = []
    if slot_meta is None:
        slot_meta = {
            "slot_id": 1,
            "slot_name": "Morning Breakthrough",
            "cta_keyword": "REPOS",
            "hook_theme": "repos"
        }

    cta_keyword = slot_meta.get("cta_keyword", "TOOLS")
    slot_name = slot_meta.get("slot_name", "AI Radar")
    print(f"[*] AI Scriptwriter: Crafting script for [{slot_name}] with CTA '{cta_keyword}'...")

    top_3 = items[:3]

    style_context = ""
    for sample in trending_samples[:3]:
        style_context += f"- Creator {sample.get('creator', 'Tech')}: Hook: \"{sample.get('transcript_sample', '')[:160]}...\"\n"

    items_context = ""
    for idx, itm in enumerate(top_3, 1):
        clean_desc = sanitize_voice_script(itm.get("description", ""))
        name = itm["name"].split("/")[-1].replace("-", " ")
        items_context += f"Item {idx}: Name: {name}, Feature: {clean_desc[:140]}\n"

    system_instruction = (
        f"You are the world's best viral tech scriptwriter (Fireship & Alex Hormozi style pacing). "
        f"Write an electrifying 38-to-42 second Instagram Reel script for '{slot_name}'.\n"
        f"RULES:\n"
        f"1. STRICT WORD COUNT: EXACTLY 95 to 105 words total. Not more, not less.\n"
        f"2. ZERO URLs: NEVER mention 'http', 'https', 'dot com', or links.\n"
        f"3. HIGH ENERGY SPOKEN ENGLISH: Punchy, urgent, conversational.\n"
        f"4. STRUCTURE:\n"
        f"   - Hook (0-3s): Punchy curiosity statement (~12 words)\n"
        f"   - Tool 1 (3-14s): What it does and why it's insane (~25 words)\n"
        f"   - Tool 2 (14-25s): Unique superpower (~25 words)\n"
        f"   - Tool 3 (25-35s): The ultimate secret tool (~25 words)\n"
        f"   - CTA (35-40s): 'Comment the word {cta_keyword} below, and I will DM you the links immediately.' (~12 words)\n"
        f"5. Output valid JSON only with keys: 'hook', 'tool_1_text', 'tool_2_text', 'tool_3_text', 'cta', 'full_script'."
    )

    prompt = f"""
VIRAL REFERENCES:
{style_context}

ITEMS TO FEATURE:
{items_context}

Write the viral reel script following the strict word count rules and ending with CTA '{cta_keyword}'.
"""

    api_key = get_gemini_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}" if api_key else ""
    payload = {
        "contents": [{"parts": [{"text": f"{system_instruction}\n\n{prompt}"}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.7
        }
    }

    script_data = None
    if api_key:
        try:
            res = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=40)
            if res.status_code == 200:
                data = res.json()
                raw_json = data["candidates"][0]["content"]["parts"][0]["text"]
                script_data = json.loads(raw_json)
        except Exception as e:
            print(f"[!] Primary Gemini API warning ({e}), falling back to slot template...")

    if not script_data:
        t1 = top_3[0]["name"].split("/")[-1].replace("-", " ")
        t2 = top_3[1]["name"].split("/")[-1].replace("-", " ")
        t3 = top_3[2]["name"].split("/")[-1].replace("-", " ")
        
        slot_hooks = {
            1: "Stop paying monthly software fees. These three open source repos give you insane superpowers.",
            2: "Most developers waste twenty hours every week doing manual work. Here is the automated loop.",
            3: "Frontier AI just shifted again. These three breakthrough models completely break existing benchmarks.",
            4: "Bookmark this immediately. Three secret AI websites that feel totally illegal to know.",
            5: "If you are still prompting AI like a beginner in 2026, you are leaving massive results behind."
        }
        
        hook = slot_hooks.get(slot_meta.get("slot_id", 1), slot_hooks[1])
        script_data = {
            "hook": hook,
            "tool_1_text": f"First up is {t1}. It automates complex engineering tasks in seconds with zero manual friction.",
            "tool_2_text": f"Next is {t2}. A high-performance powerhouse that runs locally on your machine with extreme speed.",
            "tool_3_text": f"Finally, {t3}. The ultimate secret weapon that senior creators and engineers use silently.",
            "cta": f"Comment the word {cta_keyword} below, and I will DM you the exact links right now."
        }

    if "full_script" not in script_data:
        script_data["full_script"] = (
            f"{script_data.get('hook', '')} "
            f"{script_data.get('tool_1_text', '')} "
            f"{script_data.get('tool_2_text', '')} "
            f"{script_data.get('tool_3_text', '')} "
            f"{script_data.get('cta', '')}"
        )

    script_data["full_script"] = sanitize_voice_script(script_data["full_script"])
    word_count = len(script_data["full_script"].split())
    print(f"[✓] Script generated successfully ({word_count} words).")

    return script_data
