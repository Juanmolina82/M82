#!/bin/bash

# 1. Asegurar persistencia y energía en Android
termux-wake-lock 2>/dev/null

echo "=================================================="
echo "🛡️ CONFIGURANDO PROTECCIÓN DE SISTEMA Y GITHUB"
echo "=================================================="

# 2. Crear Script Guardián (Keep-Alive / Auto-recuperación)
cat << 'GUARDIAN_EOF' > ~/M82/m82_guardian.sh
#!/bin/bash
termux-wake-lock 2>/dev/null
if ! pgrep -f "m82_core_orchestrator.py" > /dev/null; then
    echo "[$(date)] ⚠️ Orquestador M82 caído. Reiniciando infraestructura..." >> ~/m82_guardian.log
    nohup python3 -u ~/M82/m82_core_orchestrator.py > ~/m82_telegram.log 2>&1 &
fi
GUARDIAN_EOF

chmod +x ~/M82/m82_guardian.sh

# 3. Configurar Tarea Programada (Cron) para Ejecución en Segundo Plano
crontab -l 2>/dev/null | grep -v "m82_guardian.sh" > ~/M82/cron_tmp
echo "*/5 * * * * bash ~/M82/m82_guardian.sh" >> ~/M82/cron_tmp
crontab ~/M82/cron_tmp 2>/dev/null
rm ~/M82/cron_tmp

# 4. Asegurar la inclusión en ~/.bashrc para inicio de sesión
sed -i '/m82_boot_autostart.sh/d' ~/.bashrc
echo "bash ~/M82/m82_boot_autostart.sh" >> ~/.bashrc

echo "✅ Protección contra caídas configurada exitosamente."
echo "=================================================="
echo "📦 RESPALDANDO CÓDIGO Y ESTRUCTURA EN GITHUB"
echo "=================================================="

# 5. Inicialización y Respaldo en Git / GitHub
cd ~/M82

if [ ! -d ".git" ]; then
    git init
    git config user.name "MolinaHoldings"
    git config user.email "admin@molinaholdings.com"
fi

# Ignorar archivos temporales o bases de datos con datos volátiles
cat << 'GITIGNORE' > .gitignore
*.db
*.log
*.png
backups/
GITIGNORE

git add .
git commit -m "M82 Infrastructure: Full release with 32 Daemons, Auto-Recovery, and Orchestrator"

# Intentar sincronización con el repositorio remoto si está configurado
if git remote | grep -q "origin"; then
    git push -u origin main || git push -u origin master
    echo "✅ Cambios subidos correctamente al repositorio remoto en GitHub."
else
    echo "ℹ️ Repositorio local inicializado y commit creado."
    echo "⚠️ Para vincular con tu repositorio de GitHub, ejecuta:"
    echo "   cd ~/M82 && git remote add origin <URL_DE_TU_REPOSITORIO_GITHUB> && git push -u origin main"
fi

echo "=================================================="
echo "🔒 SISTEMA M82 BLINDADO Y PROTEGIDO CORRECTAMENTE"
echo "=================================================="
