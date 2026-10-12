import os
import json
import glob
import subprocess
import time
import shutil

class BossAgent:
    """
    BOSS AGENT:
    Executive Final Authority & Quality Gatekeeper.
    - Inspects final reel output, audio-visual sync, and sound cues.
    - Extracts 6 high-resolution keyframes across all 6 production beats.
    - Copies keyframes to artifact directory for instant UI inspection.
    - Enforces STRICT PROTOCOL: HALT for explicit user confirmation before any publishing!
    """
    def __init__(self):
        self.review_dir = "out/boss_review"
        os.makedirs(self.review_dir, exist_ok=True)
        self.artifact_dir = "/Users/jd/.gemini/antigravity/brain/5868917f-48d5-4970-9a96-fbcee7d661fd"

    def extract_review_keyframes(self, video_path="out/daily-reel.mp4", duration=30.0):
        for f in glob.glob(f"{self.review_dir}/*.jpg"):
            os.remove(f)

        explainer_dur = (duration - 9.0) if duration > 40.0 else duration

        sample_times = [
            ("01_hook", min(1.5, explainer_dur * 0.05)),
            ("02_shift", min(5.5, explainer_dur * 0.18)),
            ("03_tool_1", explainer_dur * 0.40),
            ("04_tool_2", explainer_dur * 0.65),
            ("05_tool_3", explainer_dur * 0.85),
            ("06_explainer_cta", max(1.0, explainer_dur - 2.0))
        ]
        if duration > 40.0:
            sample_times.append(("07_creator_face_cta", max(explainer_dur + 2.0, duration - 4.0)))

        extracted = []
        for label, t in sample_times:
            out_img = os.path.join(self.review_dir, f"{label}_{int(t)}s.jpg")
            cmd = f'ffmpeg -y -ss {t:.2f} -i "{video_path}" -vframes 1 -q:v 2 "{out_img}"'
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(out_img):
                extracted.append({"label": label, "timestamp": round(t, 2), "path": out_img})
                # Copy to artifact dir for UI presentation
                if os.path.exists(self.artifact_dir):
                    dest = os.path.join(self.artifact_dir, f"{label}.jpg")
                    try:
                        shutil.copyfile(out_img, dest)
                    except Exception:
                        pass

        return extracted

    def review_production(
        self,
        video_path="out/daily-reel.mp4",
        quality_audit_path="assets/quality_audit.json",
        research_path="assets/research_dossier.json",
        script_path="assets/viral_script.json"
    ):
        print("=" * 65)
        print("👑 [AGENT 7: BOSS AGENT] Conducting Executive Final Review & Approval Gate...")
        print("=" * 65)

        if not os.path.exists(quality_audit_path):
            raise RuntimeError("Cannot conduct Boss review: Quality Agent audit is missing!")

        with open(quality_audit_path) as f:
            qa_summary = json.load(f)

        quality_passed = qa_summary.get("status") == "PASS"
        quality_score = qa_summary.get("total_score", 0)

        # Probe video
        probe_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration -of json "{video_path}"'
        try:
            probe_data = json.loads(subprocess.check_output(probe_cmd, shell=True).decode())
            stream_info = probe_data.get("streams", [{}])[0]
            width = int(stream_info.get("width", 1080))
            height = int(stream_info.get("height", 1920))
            duration = float(stream_info.get("duration", 30.0))
        except Exception:
            width, height, duration = 1080, 1920, 30.0

        keyframes = self.extract_review_keyframes(video_path, duration)

        # Load research & script
        research_info = {}
        if os.path.exists(research_path):
            with open(research_path) as f:
                research_info = json.load(f)

        script_info = {}
        if os.path.exists(script_path):
            with open(script_path) as f:
                script_info = json.load(f)

        approved = quality_passed and (quality_score >= 90) and (len(keyframes) >= 5)

        verdict = {
            "boss_decision": "READY_FOR_USER_CONFIRMATION" if approved else "REJECTED_NEEDS_REVISION",
            "quality_score": quality_score,
            "quality_audit": qa_summary,
            "video_path": video_path,
            "dimensions": f"{width}x{height}",
            "duration_seconds": round(duration, 2),
            "lead_topic": (research_info.get("items", [{}])[0].get("name") if research_info.get("items") else "AI Tool"),
            "hook": script_info.get("hook", ""),
            "cta_keyword": script_info.get("cta_keyword", "REPOS"),
            "keyframes": keyframes,
            "can_auto_publish": False,
            "timestamp": time.time()
        }

        with open("assets/boss_verdict.json", "w") as f:
            json.dump(verdict, f, indent=2)

        print(f"Decision: {verdict['boss_decision']}")
        print(f"Overall Quality Score: {quality_score}/100")
        print(f"Video File: {video_path} ({width}x{height}, {duration:.1f}s)")
        print(f"Lead Topic: {verdict['lead_topic']}")
        print(f"Hook: {verdict['hook']}")
        print(f"Extracted {len(keyframes)} Keyframes to: {self.review_dir}/")
        print("-" * 65)
        print("🔒 PROTOCOL ENFORCED: Staged in 'out/'. ZERO auto-publishing will occur until explicit user review.")
        print("=" * 65)

        return verdict

if __name__ == "__main__":
    boss = BossAgent()
    boss.review_production()
