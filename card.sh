#!/data/data/com.termux/files/usr/bin/bash

# 1. Configuración de Entorno & Validaciones
[ -f "$HOME/M82/.env" ] && source "$HOME/M82/.env"
TOKEN="${M82_TELEGRAM_TOKEN:-8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y}"
CHAT="${M82_TELEGRAM_CHAT:--1004335849125}"

TITLE="$1"
TAG="$2"
# Definición explícita de rutas
TMP_DIR="/data/data/com.termux/files/usr/tmp"
IMG_PATH="$TMP_DIR/m82_card.jpg"

if [ -z "$TITLE" ]; then
    echo "❌ Error: Se requiere un título. Uso: $0 \"Título\" \"Tag\""
    exit 1
fi

mkdir -p "$TMP_DIR"

# 2. Generación Gráfica (ImageMagick v7)
FORMATTED_TITLE=$(echo "$TITLE" | fold -w 30 -s)
magick -size 1080x1350 xc:"#0A0A0C" \
  -stroke "#22222B" -strokewidth 4 -draw "rectangle 30,30 1050,1320" \
  -stroke none \
  -fill "#FF3B30" -pointsize 54 -annotate +70+140 "🚨 #M82 BREAKING STREAM" \
  -fill "#FFFFFF" -pointsize 46 -annotate +70+380 "$FORMATTED_TITLE" \
  -fill "#000000" -draw "roundrectangle 70,720 1010,840 15,15" \
  -fill "#34C759" -pointsize 44 -annotate +90+795 "$TAG" \
  -fill "#8E8E93" -pointsize 32 -annotate +70+1240 "🏛 @MolinaHoldings LLC | PP/PE Direct Access" \
  "$IMG_PATH"

echo "🖼️ Card M82 generada localmente."

# 3. Preparación de Caption
CAPTION="🚨 #M82 BREAKING STREAM

🔴 $TITLE
$TAG

🏛 @MolinaHoldings LLC"

# 4. Despacho a Telegram
curl -s -F chat_id="$CHAT" \
        -F photo="@$IMG_PATH" \
        -F caption="$CAPTION" \
        "https://api.telegram.org/bot$TOKEN/sendPhoto" | grep -q '"ok":true' && echo "⚡ [DESPACHO OK] Imagen enviada a Telegram" || echo "❌ Error en Telegram"

# 5. Integración WhatsApp (termux-share 1-clic)
# Copiar texto al portapapeles de Android
echo "$CAPTION" | termux-clipboard-set
echo "📋 Texto copiado al portapapeles."

# Compartir imagen e invocar menú de Android
echo "📲 Abriendo menú de compartir para WhatsApp..."
termux-share -a send -t image/jpeg "$IMG_PATH"

