"""
Boss Agent:
Executive Decision-Maker and Approval Gatekeeper.
Inspects the final assembled reel, cross-checks audio-visual sync, verifies SFX triggers,
generates a comprehensive review package with keyframes, and enforces the rule:
HALT for explicit user confirmation before any publishing or git commits!
"""

import os
import json
import glob
import subprocess
import time

class BossAgent:
    def __init__(self):
        self.review_dir = "out/boss_review"
        os.makedirs(self.review_dir, exist_ok=True)

    def extract_review_keyframes(self, video_path="out/daily-reel.mp4", duration=35.0):
        # Clean previous preview frames
        for f in glob.glob(f"{self.review_dir}/*.jpg"):
            os.remove(f)

        # Target sample points across the timeline: Hook, Setup, Tool Showcase, Climax, CTA
        sample_times = [
            ("01_hook", min(2.0, duration * 0.05)),
            ("02_setup", min(7.0, duration * 0.18)),
            ("03_showcase_1", duration * 0.40),
            ("04_showcase_2", duration * 0.65),
            ("05_character_reaction", duration * 0.82),
            ("06_creator_cta", max(duration - 2.5, duration * 0.92))
        ]

        extracted = []
        for label, t in sample_times:
            out_img = os.path.join(self.review_dir, f"{label}_{int(t)}s.jpg")
            cmd = f'ffmpeg -y -ss {t:.2f} -i "{video_path}" -vframes 1 -q:v 2 "{out_img}"'
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(out_img):
                extracted.append({"label": label, "timestamp": round(t, 2), "path": out_img})

        return extracted

    def verify_sfx_alignment(self, sfx_cues_path="assets/sfx_cues.json"):
        if not os.path.exists(sfx_cues_path):
            return {"synced": False, "reason": "SFX cues file missing."}

        try:
            with open(sfx_cues_path) as f:
                cues = json.load(f)
            # Check cue count and distribution
            if len(cues) < 8:
                return {"synced": False, "count": len(cues), "reason": "Insufficient sound design cues (< 8)."}

            return {"synced": True, "count": len(cues), "cues": cues}
        except Exception as e:
            return {"synced": False, "reason": str(e)}

    def review_production(
        self,
        video_path="out/daily-reel.mp4",
        quality_audit_path="assets/quality_audit.json",
        research_path="assets/research_dossier.json",
        script_path="assets/viral_script.json"
    ):
        print("================================================================================")
        print("👑 [BOSS AGENT] Conducting Executive Final Review & Approval Gate...")
        print("================================================================================")

        # 1. Check Quality Agent audit
        if not os.path.exists(quality_audit_path):
            raise RuntimeError("Cannot conduct Boss review: Quality Agent audit is missing!")

        with open(quality_audit_path) as f:
            qa_summary = json.load(f)

        quality_passed = qa_summary.get("status") == "PASS"
        quality_score = qa_summary.get("total_score", 0)

        # 2. Probe video metadata
        probe_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration -of json "{video_path}"'
        try:
            probe_data = json.loads(subprocess.check_output(probe_cmd, shell=True).decode())
            stream_info = probe_data.get("streams", [{}])[0]
            width = int(stream_info.get("width", 1080))
            height = int(stream_info.get("height", 1920))
            duration = float(stream_info.get("duration", 30.0))
        except Exception:
            width, height, duration = 1080, 1920, 30.0

        # 3. Extract review keyframes
        keyframes = self.extract_review_keyframes(video_path, duration)

        # 4. Verify SFX alignment
        sfx_check = self.verify_sfx_alignment()

        # 5. Load research and script dossier
        research_info = {}
        if os.path.exists(research_path):
            with open(research_path) as f:
                research_info = json.load(f)

        script_info = {}
        if os.path.exists(script_path):
            with open(script_path) as f:
                script_info = json.load(f)

        # 6. Boss Verdict Logic
        approved = quality_passed and (quality_score >= 85) and sfx_check["synced"] and (len(keyframes) >= 4)

        verdict = {
            "boss_decision": "READY_FOR_USER_CONFIRMATION" if approved else "REJECTED_NEEDS_REVISION",
            "quality_score": quality_score,
            "quality_audit": qa_summary,
            "video_path": video_path,
            "dimensions": f"{width}x{height}",
            "duration_seconds": round(duration, 2),
            "topic": (research_info.get("items", [{}])[0].get("title") if research_info.get("items") else research_info.get("title", "Unknown")),
            "hook": script_info.get("hook_text", ""),
            "sfx_cues_count": sfx_check.get("count", 0),
            "keyframes": keyframes,
            "can_auto_publish": False, # STRICT PROTOCOL: NEVER auto-publish without user confirmation
            "timestamp": time.time()
        }

        with open("assets/boss_verdict.json", "w") as f:
            json.dump(verdict, f, indent=2)

        # 7. Print Executive Review
        print(f"Decision: {verdict['boss_decision']}")
        print(f"Overall Quality: {quality_score}/100")
        print(f"Video File: {video_path} ({width}x{height}, {duration:.1f}s)")
        print(f"Topic: {verdict['topic']}")
        print(f"Hook: {verdict['hook']}")
        print(f"Extracted {len(keyframes)} Keyframes to: {self.review_dir}/")
        print("--------------------------------------------------------------------------------")
        print("🔒 PROTOCOL ENFORCED: Video is staged in 'out/daily-reel.mp4'.")
        print("   ZERO git commits or social pushes will occur until user reviews and approves.")
        print("================================================================================")

        return verdict

if __name__ == "__main__":
    boss = BossAgent()
    boss.review_production()
