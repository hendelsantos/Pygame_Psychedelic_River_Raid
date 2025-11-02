#!/bin/bash
# Script para executar o Psychedelic River Raid

echo "🎮 Psychedelic River Raid"
echo "========================="

# Configurar ambiente gráfico
export DISPLAY=:0

# Tentar diferentes drivers de vídeo
echo "🔧 Configurando display..."

# Primeiro tentar com X11
echo "Tentando SDL_VIDEODRIVER=x11..."
SDL_VIDEODRIVER=x11 python game.py

# Se não funcionou, tentar padrão
if [ $? -ne 0 ]; then
    echo "Tentando driver padrão..."
    python game.py
fi