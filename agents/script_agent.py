import os
import re
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

def run_script_agent(dossier_path: str = "assets/research_dossier.json", cta_keyword: str = "REPOS", research_dossier: dict = None) -> dict:
    """
    SCRIPT AGENT:
    Deconstructs top-performing viral video hooks and analytics,
    then writes an electrifying 95-to-105-word high-retention spoken script.
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

    items_text = ""
    for idx, it in enumerate(items[:3], 1):
        name = it.get("name") or it.get("title", f"Tool {idx}")
        desc = it.get("description", "")
        items_text += f"Item {idx}: {name} - {desc}\n"

    system_prompt = (
        "You are an elite viral tech short-form video creator (combining Fireship's technical humor and Alex Hormozi's punchy retention pacing).\n"
        "Your task: Write an electrifying, spoken script for an Instagram Reel and YouTube Short.\n\n"
        "STRICT CONSTRAINTS:\n"
        "1. EXACT WORD COUNT: Between 95 and 105 words total. Count every word carefully.\n"
        "2. SPOKEN LANGUAGE ONLY: No markdown formatting, no hashtags, no URLs, no 'dot com', no parentheses.\n"
        "3. HIGH ENERGY PACING: Every sentence must be punchy, urgent, and conversational.\n"
        "4. STRUCTURE:\n"
        "   - Hook (0-3s): Punchy curiosity question or bottleneck (~12 words)\n"
        "   - Item 1 (3-15s): Introduce the first tool and its unique superpower (~25 words)\n"
        "   - Item 2 (15-27s): Introduce the second tool and why it changes everything (~25 words)\n"
        "   - Item 3 (27-38s): Introduce the third tool and its ultimate capability (~25 words)\n"
        f"   - CTA (38-43s): Urgent call to action: 'Comment {cta_keyword} below, and I will DM you the links right now.' (~12 words)\n"
        "5. Output valid JSON only with keys: 'hook', 'tool_1', 'tool_2', 'tool_3', 'cta', 'full_script', 'word_count'."
    )

    user_prompt = f"CURATED BREAKING TOPICS:\n{items_text}\n\nWrite the script now ending with CTA keyword '{cta_keyword}'."

    gemini_key = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
    
    payload = {
        "contents": [{"parts": [{"text": f"{system_prompt}\n\n{user_prompt}"}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.7
        }
    }

    for attempt in range(2):
        try:
            res = requests.post(url, json=payload, timeout=35)
            if res.status_code == 200:
                break
        except Exception as e:
            if attempt == 1:
                raise e
            time.sleep(2)

    if res.status_code != 200:
        raise RuntimeError(f"Gemini API error ({res.status_code}): {res.text}")

    raw_json = res.json()["candidates"][0]["content"]["parts"][0]["text"]
    script_data = json.loads(raw_json)

    # Clean & verify word count
    full_text = script_data.get("full_script", "")
    words = re.findall(r'\S+', full_text)
    script_data["word_count"] = len(words)
    script_data["cta_keyword"] = cta_keyword

    with open("assets/viral_script.json", "w") as f:
        json.dump(script_data, f, indent=2)

    print(f"[✓] Script Agent complete! Total Words: {len(words)}")
    print(f"    Hook: \"{script_data.get('hook')}\"")
    print(f"    Full Script:\n    \"{full_text}\"\n")

    return script_data

if __name__ == "__main__":
    run_script_agent()
