import os
import re
import json
import subprocess
from dotenv import load_dotenv

load_dotenv()

def run_script_agent(dossier_path: str = "assets/research_dossier.json", cta_keyword: str = "REPOS", research_dossier: dict = None) -> dict:
    """
    SCRIPT AGENT:
    Deconstructs top-performing viral video hooks and analytics,
    then writes an electrifying 6-beat high-retention spoken script (95-105 words).
    """
    print("=" * 65)
    print(f"✍️ [AGENT 2: SCRIPT AGENT] Generating High-Retention Spoken Script (Target: 95-105 words)...")
    print("=" * 65)

    if research_dossier:
        dossier = research_dossier
    elif os.path.exists(dossier_path):
        with open(dossier_path, "r") as f:
            dossier = json.load(f)
    else:
        raise FileNotFoundError(f"Dossier {dossier_path} not found. Run Research Agent first.")

    items = dossier.get("items", [])
    if len(items) < 3:
        raise ValueError("Research dossier has fewer than 3 items.")

    t1_name = items[0].get("name", "Tool One")
    t1_desc = items[0].get("description", "")
    t2_name = items[1].get("name", "Tool Two")
    t2_desc = items[1].get("description", "")
    t3_name = items[2].get("name", "Tool Three")
    t3_desc = items[2].get("description", "")

    system_prompt = (
        "You are an elite viral tech short-form video creator for developers and AI builders (fast-paced, high retention, zero fluff).\n"
        "Your task: Write an electrifying, spoken script for an Instagram Reel and YouTube Short.\n\n"
        "STRICT CONSTRAINTS:\n"
        "1. EXACT 6-BEAT STRUCTURE (Output valid JSON only):\n"
        "   - 'hook': Curiosity punch or painful bottleneck (~12 words)\n"
        "   - 'shift': The new solution overview (~10 words)\n"
        f"   - 'tool_1': Name '{t1_name}' and explain its breakthrough capability (~20 words)\n"
        f"   - 'tool_2': Name '{t2_name}' and explain its breakthrough capability (~20 words)\n"
        f"   - 'tool_3': Name '{t3_name}' and explain its breakthrough capability (~20 words)\n"
        f"   - 'cta': Urgent call to action: 'Comment {cta_keyword} below, and I will DM you the setup code right now.' (~14 words)\n"
        "2. TOTAL WORD COUNT: Exactly between 95 and 105 words total across all 6 sections combined.\n"
        "3. SPOKEN NATURAL LANGUAGE: No markdown asterisks, no URLs, no hashtags, no parentheses.\n"
        "4. Return ONLY valid JSON with keys: 'hook', 'shift', 'tool_1', 'tool_2', 'tool_3', 'cta'."
    )

    user_prompt = (
        f"TOOL 1: {t1_name} - {t1_desc}\n"
        f"TOOL 2: {t2_name} - {t2_desc}\n"
        f"TOOL 3: {t3_name} - {t3_desc}\n\n"
        f"Write the JSON script now with CTA keyword '{cta_keyword}'."
    )

    gemini_key = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
    
    payload = {
        "contents": [{"parts": [{"text": f"{system_prompt}\n\n{user_prompt}"}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.65
        }
    }

    script_data = None
    try:
        curl_cmd = [
            "curl", "-s", "--max-time", "15", "-X", "POST", url,
            "-H", "Content-Type: application/json",
            "-d", json.dumps(payload)
        ]
        out = subprocess.check_output(curl_cmd, text=True)
        res_json = json.loads(out)
        raw_text = res_json["candidates"][0]["content"]["parts"][0]["text"]
        script_data = json.loads(raw_text)
    except Exception as e:
        print(f"[!] Curl Gemini note ({e}), using optimized high-retention fallback...")

    if not script_data or "tool_1" not in script_data:
        script_data = {
            "hook": "Stop wasting hours paying for expensive SaaS when open-source AI does this automatically.",
            "shift": "Three brand-new developer tools just dropped on GitHub that change the game.",
            "tool_1": f"First is {t1_name}, an open-source powerhouse that eliminates manual workflows with local model execution.",
            "tool_2": f"Second is {t2_name}, an autonomous engine running deterministic pipelines with lightning-fast sub-millisecond response times.",
            "tool_3": f"Third is {t3_name}, a zero-latency runtime executing complex workflows directly in WebAssembly with zero cloud lock-in.",
            "cta": f"Comment {cta_keyword} below, and I will DM you the full setup code and GitHub repos right now."
        }

    sections = [
        script_data["hook"],
        script_data["shift"],
        script_data["tool_1"],
        script_data["tool_2"],
        script_data["tool_3"],
        script_data["cta"]
    ]
    full_text = " ".join(sections)
    words = re.findall(r'\S+', full_text)
    script_data["full_script"] = full_text
    script_data["word_count"] = len(words)
    script_data["cta_keyword"] = cta_keyword
    script_data["sections_list"] = [
        ("hook", script_data["hook"]),
        ("shift", script_data["shift"]),
        ("tool_1", script_data["tool_1"]),
        ("tool_2", script_data["tool_2"]),
        ("tool_3", script_data["tool_3"]),
        ("cta", script_data["cta"])
    ]

    os.makedirs("assets", exist_ok=True)
    with open("assets/viral_script.json", "w") as f:
        json.dump(script_data, f, indent=2)

    print(f"[✓] Script Agent complete! Total Words: {len(words)}")
    print(f"    Hook: \"{script_data['hook']}\"")
    print(f"    Full Script: \"{full_text}\"\n")

    return script_data

if __name__ == "__main__":
    run_script_agent()
