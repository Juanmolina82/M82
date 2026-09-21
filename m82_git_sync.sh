#!/data/data/com.termux/files/usr/bin/bash

BASE_DIR="$HOME/M82"
cd "$BASE_DIR" || exit

git add .
if [ -n "$(git status --porcelain)" ]; then
    echo "⚡ [GIT] Cambios detectados. Sincronizando con GitHub..."
    git commit -m "update: M82 Core & Refinitiv Infrastructure"
    git push origin main
else
    echo "✅ [GIT] Infraestructura al día. Nada que subir."
fi
