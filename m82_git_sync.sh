#!/bin/bash
termux-wake-lock 2>/dev/null
cd ~/M82
git add .
git commit -m "Auto-Sync M82 Infrastructure: $(date +'%Y-%m-%d %H:%M:%S')" 2>/dev/null
git push origin main 2>/dev/null
