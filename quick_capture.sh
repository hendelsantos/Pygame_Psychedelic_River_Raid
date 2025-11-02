#!/bin/bash
#
# Quick Game Capture Script
# Captura gameplay diretamente via FFmpeg
#

echo "🎥 QUICK GAME CAPTURE - Psychedelic River Raid"
echo "=============================================="

# Configurações
DURATION=${1:-30}  # Duração padrão: 30 segundos
OUTPUT_DIR="/home/hendel/Estudos/Pygame/game1/trailer_footage"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="$OUTPUT_DIR/gameplay_$TIMESTAMP.mp4"

# Criar diretório se não existir
mkdir -p "$OUTPUT_DIR"

echo "⏱️  Duração: $DURATION segundos"
echo "📁 Saída: $OUTPUT_FILE"
echo ""
echo "🎮 INSTRUÇÕES:"
echo "1. Abra o jogo Psychedelic River Raid"
echo "2. Deixe pronto para uma boa sequência"
echo "3. Pressione ENTER quando estiver pronto"
echo ""

read -p "Pressione ENTER para começar a captura..."

echo ""
echo "⏰ Iniciando em:"
for i in {5..1}; do
    echo "   $i..."
    sleep 1
done

echo ""
echo "🔴 GRAVANDO! Duração: $DURATION segundos"
echo "   (Pressione Ctrl+C para parar antes)"

# Comando FFmpeg para captura
ffmpeg \
    -f x11grab \
    -s 800x600 \
    -r 60 \
    -i :0.0 \
    -t $DURATION \
    -c:v libx264 \
    -preset fast \
    -crf 18 \
    -pix_fmt yuv420p \
    -y \
    "$OUTPUT_FILE" \
    2>/dev/null

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Captura concluída com sucesso!"
    echo "📄 Arquivo salvo: $OUTPUT_FILE"
    echo ""
    echo "📊 INFORMAÇÕES DO ARQUIVO:"
    ls -lh "$OUTPUT_FILE"
    echo ""
    echo "🎬 Para visualizar:"
    echo "   vlc '$OUTPUT_FILE'"
    echo ""
    echo "📝 Para converter para GIF (redes sociais):"
    echo "   ffmpeg -i '$OUTPUT_FILE' -vf 'fps=15,scale=640:-1' '${OUTPUT_FILE%.*}.gif'"
else
    echo ""
    echo "❌ Erro na captura!"
    echo "💡 Dicas para solucionar:"
    echo "   - Verifique se o jogo está na resolução 800x600"
    echo "   - Certifique-se que não há outros programas usando X11"
    echo "   - Tente executar o script novamente"
fi