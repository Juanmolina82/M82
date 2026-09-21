#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock 2>/dev/null

if ! pgrep -f "m82_launch_all.py" > /dev/null; then
    nohup python3 -u ~/M82/m82_launch_all.py > ~/M82/m82_factory.log 2>&1 &
    echo "⚡ [M82 INFRASTRUCTURE] Fábrica iniciada en segundo plano."
else
    echo "✅ [M82 INFRASTRUCTURE] La fábrica ya está corriendo en segundo plano."
fi
