#!/data/data/com.termux/files/usr/bin/bash
pkill -f daemon.py 2>/dev/null
nohup python ~/M82/daemon.py > ~/M82/logs/daemon.out 2>&1 &
echo $! > ~/M82/pid.txt
termux-wake-lock
echo "M82 CORE-V6 Activo bajo PID: $(cat ~/M82/pid.txt)"
