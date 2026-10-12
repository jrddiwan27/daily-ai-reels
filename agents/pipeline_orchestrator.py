"""
Pipeline Orchestrator:
Executes the full 7-Agent Production Pipeline in strict chronological order:
1. Research Agent -> 24h Breaking AI News & Repo Discovery
2. Script Agent   -> High-retention spoken script (90-110 words)
3. Voiceover Agent-> TTS with word-by-word timestamps & 30fps RMS visemes
4. Visual Agent   -> Kinetic Neo-Brutalist HTML composition with prominent avatar
5. Editor Agent   -> HyperFrames render, studio SFX mixing, rotating CTA outro
6. Quality Agent  -> Strict non-cheating audits across all 5 gates
7. Boss Agent     -> Executive review, keyframe extraction & user confirmation gate
"""

import os
import sys
import time
import json

from agents.research_agent import run_research_agent
from agents.script_agent import run_script_agent
from agents.voiceover_agent import run_voiceover_agent
from agents.visual_agent import run_visual_agent
from agents.editor_agent import run_editor_agent
from agents.quality_agent import QualityAgent
from agents.boss_agent import BossAgent

SLOT_CONFIGS = {
    1: {"theme": "open source AI agents GitHub", "cta": "REPOS", "name": "Morning Breakthrough"},
    2: {"theme": "autonomous AI automation workflows 2026", "cta": "WORKFLOW", "name": "Midday Cheat Code"},
    3: {"theme": "new open weights multimodal reasoning AI models", "cta": "MODELS", "name": "Tech Radar Teardown"},
    4: {"theme": "secret web AI developer productivity tools 2026", "cta": "TOOLS", "name": "Evening Toolkit"},
    5: {"theme": "advanced prompt engineering frameworks architectures 2026", "cta": "PROMPT", "name": "Night Owl Deep Dive"}
}

def run_production_pipeline(slot_id: int = 1, theme_focus: str = None, cta_keyword: str = None, max_retries: int = 2):
    start_total = time.time()
    slot_cfg = SLOT_CONFIGS.get(slot_id, SLOT_CONFIGS[1])
    theme = theme_focus or slot_cfg["theme"]
    cta = cta_keyword or slot_cfg["cta"]
    slot_name = slot_cfg["name"]

    print("################################################################################")
    print(f"🚀 LAUNCHING 7-AGENT PRODUCTION PIPELINE — SLOT {slot_id} ({slot_name})")
    print("################################################################################")

    final_video = f"out/slot_{slot_id}_daily_reel.mp4"
    raw_video = f"out/slot_{slot_id}_raw_video.mp4"

    for attempt in range(1, max_retries + 1):
        print(f"\n--- [PRODUCTION RUN ATTEMPT {attempt}/{max_retries}] ---")

        # -------------------------------------------------------------------------
        # AGENT 1: RESEARCH AGENT
        # -------------------------------------------------------------------------
        print("\n[STEP 1/7] Initializing Research Agent...")
        research_dossier = run_research_agent(slot_id=slot_id, theme_focus=theme)
        top_topic = research_dossier.get("items", [{}])[0].get("title", "Fresh AI News")
        print(f"-> Topic Locked: {top_topic}")

        # -------------------------------------------------------------------------
        # AGENT 2: SCRIPT AGENT
        # -------------------------------------------------------------------------
        print("\n[STEP 2/7] Initializing Script Agent...")
        script_data = run_script_agent(research_dossier=research_dossier, cta_keyword=cta)
        hook_display = script_data.get("hook") or script_data.get("hook_text") or "Viral Hook"
        print(f"-> Script Drafted: {script_data.get('word_count')} words | Hook: {hook_display}")

        # -------------------------------------------------------------------------
        # AGENT 3: VOICEOVER AGENT
        # -------------------------------------------------------------------------
        print("\n[STEP 3/7] Initializing Voiceover Agent...")
        vo_res = run_voiceover_agent(script_data=script_data)
        duration = vo_res.get("duration", 38.0)
        print(f"-> Voiceover Generated: {duration:.2f}s | Word Cues: {vo_res.get('word_count')} words")

        # -------------------------------------------------------------------------
        # AGENT 4: VISUAL AGENT
        # -------------------------------------------------------------------------
        print("\n[STEP 4/7] Initializing Visual Agent...")
        html_path = run_visual_agent(
            script_data=script_data,
            research_dossier=research_dossier,
            duration=duration
        )
        print(f"-> Visual Composition Compiled: {html_path}")

        # -------------------------------------------------------------------------
        # AGENT 5: EDITOR AGENT
        # -------------------------------------------------------------------------
        print("\n[STEP 5/7] Initializing Editor Agent...")
        editor_manifest = run_editor_agent(
            raw_video_path=raw_video,
            output_final_path=final_video,
            duration=duration
        )
        print(f"-> Master Render & Audio Assembly Complete: {final_video}")

        # -------------------------------------------------------------------------
        # AGENT 6: QUALITY AGENT (Strict Non-Cheating Audit)
        # -------------------------------------------------------------------------
        print("\n[STEP 6/7] Initializing Quality Agent (Strict Non-Cheating Audit)...")
        qa = QualityAgent()
        qa_summary = qa.run_full_audit(video_path=final_video, raw_video_path=raw_video)

        if qa_summary["status"] != "PASS":
            print(f"[!] Quality Agent audit rejected production (Score: {qa_summary['total_score']}/100).")
            if attempt < max_retries:
                print(f"[↺] Retrying pipeline to remediate quality failures...")
                continue
            else:
                print(f"[⚠️] Max retries reached. Handing over to Boss Agent with audit warnings.")

        # -------------------------------------------------------------------------
        # AGENT 7: BOSS AGENT (Executive Final Gate & User Review)
        # -------------------------------------------------------------------------
        print("\n[STEP 7/7] Initializing Boss Agent...")
        boss = BossAgent()
        verdict = boss.review_production(video_path=final_video)

        total_elapsed = time.time() - start_total
        print("\n################################################################################")
        print(f"🏆 PIPELINE EXECUTION COMPLETE IN {total_elapsed:.1f} SECONDS")
        print(f"   Final Reel: {final_video}")
        print(f"   Boss Verdict: {verdict['boss_decision']}")
        print(f"   Keyframes: out/boss_review/")
        print("################################################################################")
        return verdict

if __name__ == "__main__":
    run_production_pipeline()
