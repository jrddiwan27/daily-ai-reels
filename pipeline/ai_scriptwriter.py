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
    # Remove http/https links
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"github\.com/\S+", "", text)
    # Remove markdown links [text](url) -> text
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    # Remove special characters
    text = re.sub(r"[#*_~`><]", "", text)
    # Clean whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

def generate_viral_script_with_gemini(repos: list, trending_samples: list) -> dict:
    """
    Uses Gemini to synthesize top creator transcripts and curated repos into a 
    high-retention viral 38-42 second voiceover script.
    """
    print("[*] AI Scriptwriter: Crafting high-retention viral script with Gemini...")
    
    # Select top 3 repos to allow deep visual pacing without rushing
    top_3 = repos[:3]
    
    # Format style references from trending creators
    style_context = ""
    for sample in trending_samples[:3]:
        style_context += f"- Creator {sample['creator']} (Topic: {sample['video_title']}):\n  Hook: \"{sample['transcript_sample'][:180]}...\"\n"

    repo_context = ""
    for idx, r in enumerate(top_3, 1):
        clean_desc = sanitize_voice_script(r.get("description", ""))
        repo_context += f"Repo {idx}: Name: {r['name'].split('/')[-1]}, Star count: {r.get('stars', 1000)}, Feature: {clean_desc[:140]}\n"

    system_instruction = (
        "You are the world's best viral tech scriptwriter (Fireship & Alex Hormozi style pacing). "
        "Your task is to write an electrifying 38-to-42 second Instagram Reel script about 3 open-source AI tools. "
        "RULES:\n"
        "1. STRICT WORD COUNT: EXACTLY 95 to 105 words total. Not more, not less.\n"
        "2. ZERO URLs: NEVER mention 'http', 'https', 'dot com', or raw links.\n"
        "3. HIGH ENERGY SPOKEN ENGLISH: Write as if speaking to a friend who wants free AI superpowers.\n"
        "4. STRUCTURE:\n"
        "   - Hook (0-3s): Punchy curiosity statement (~12 words)\n"
        "   - Tool 1 (3-14s): What it does and why it's insane (~25 words)\n"
        "   - Tool 2 (14-25s): Unique superpower (~25 words)\n"
        "   - Tool 3 (25-35s): The ultimate secret tool (~25 words)\n"
        "   - CTA (35-40s): Comment trigger keyword (~12 words)\n"
        "5. Output valid JSON only with keys: 'hook', 'tool_1_text', 'tool_2_text', 'tool_3_text', 'cta', 'full_script'."
    )

    prompt = f"""
VIRAL CREATOR HOOK REFERENCES:
{style_context}

REPOSITORIES TO FEATURE:
{repo_context}

Write the viral reel script following the strict word count rules.
"""

    api_key = get_gemini_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": f"{system_instruction}\n\n{prompt}"}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.7
        }
    }

    try:
        res = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=60)
        if res.status_code == 200:
            data = res.json()
            raw_json = data["candidates"][0]["content"]["parts"][0]["text"]
            script_data = json.loads(raw_json)
        else:
            raise RuntimeError(f"Gemini API returned status {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[!] Primary Gemini API warning ({e}), synthesizing curated viral script...")
        # High-retention viral fallback template
        t1, t2, t3 = top_3[0]["name"].split("/")[-1], top_3[1]["name"].split("/")[-1], top_3[2]["name"].split("/")[-1]
        script_data = {
            "hook": "Stop paying monthly software fees. These three open source tools grant total superpowers.",
            "tool_1_text": f"First is {t1}. It automates complex engineering tasks in seconds with zero manual coding.",
            "tool_2_text": f"Next is {t2}. An insane self-hosted powerhouse that runs locally on your own machine.",
            "tool_3_text": f"Finally, {t3}. The ultimate breakthrough developer secret that saves hundreds of hours.",
            "cta": "Comment the word TOOLS below, and I will send every repository straight to you."
        }
    
    # Ensure sanitized full script
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
    print(f"[✓] Script generated successfully ({word_count} words). Estimated duration: {word_count * 0.38:.1f}s")
    
    return script_data

if __name__ == "__main__":
    with open("assets/curated_repos.json") as f:
        repos = json.load(f)
    with open("assets/creator_trends.json") as f:
        trends = json.load(f)
    result = generate_viral_script_with_gemini(repos, trends)
    print("\n--- GENERATED SCRIPT ---")
    print(result["full_script"])
