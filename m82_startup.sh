#!/data/data/com.termux/files/usr/bin/bash

echo "=================================================="
echo "🚀 INICIANDO RESTAURACIÓN M82 QUANTUM AGI TERMINAL"
echo "=================================================="

# 1. Prevenir que Android suspenda Termux
termux-wake-lock 2>/dev/null

# 2. Asegurar permisos de ejecución en toda la suite
chmod +x ~/M82/*.py 2>/dev/null
chmod +x ~/M82/*.sh 2>/dev/null
chmod +x ~/M82/tools/*.sh 2>/dev/null

# 3. Detener cualquier proceso previo colgado
pkill -f m82 2>/dev/null

# 4. Lanzar el Orquestador Principal (que supervisa los 16+ Daemons)
cd ~/M82
nohup python3 -u ~/M82/m82_core_orchestrator.py > ~/m82_telegram.log 2>&1 &

# 5. Lanzar el Demonio OSINT Delcy / N818CA
nohup python3 -u ~/M82/m82_delcy_osint_daemon.py > ~/m82_delcy_osint.log 2>&1 &

# 6. Sincronización inmediata con GitHub
bash ~/M82/m82_git_sync.sh 2>/dev/null

echo "=================================================="
echo "✅ INFRAESTRUCTURA RESTAURADA Y OPERATIVA EN SEGUNDO PLANO"
echo "=================================================="
