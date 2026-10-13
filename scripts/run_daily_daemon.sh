#!/bin/bash
set -e
export PATH="/Users/jd/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
export HOME="/Users/jd"
cd "/Users/jd/Desktop/JAYANT DIGITAL STUDIO/daily-automation-engine"

mkdir -p logs

# Load environment
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

echo "================================================================================" >> logs/daily_daemon.log
echo "⏰ [DAILY AUTOMATION ENGINE] Autonomous Run Started: $(date)" >> logs/daily_daemon.log
echo "================================================================================" >> logs/daily_daemon.log

/opt/homebrew/bin/python3 scripts/schedule_all_today.py >> logs/daily_daemon.log 2>&1

echo "✅ [DAILY AUTOMATION ENGINE] Run Finished at $(date)" >> logs/daily_daemon.log
