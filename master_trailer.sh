#!/bin/bash
#
# Master Trailer Creation Script
# Coordena todo o processo de criação de marketing materials
#

echo "🚀 PSYCHEDELIC RIVER RAID - TRAILER CREATION MASTER"
echo "=================================================="
echo ""

PROJECT_DIR="/home/hendel/Estudos/Pygame/game1"
cd "$PROJECT_DIR"

# Menu principal
show_menu() {
    echo "📋 OPÇÕES DISPONÍVEIS:"
    echo ""
    echo "1. 🎥 Captura rápida de gameplay (30s)"
    echo "2. 🎬 Criar trailer completo (roteiro guiado)"
    echo "3. 🎨 Gerar assets Steam automáticos"
    echo "4. 📱 Gerar guias de redes sociais"
    echo "5. 🎮 Testar o jogo antes da captura"
    echo "6. 📊 Ver estratégia de marketing completa"
    echo "7. 🔧 Setup completo (tudo de uma vez)"
    echo "8. ❌ Sair"
    echo ""
}

# Função para captura rápida
quick_capture() {
    echo "🎥 INICIANDO CAPTURA RÁPIDA"
    echo "=========================="
    
    if [ ! -f "./quick_capture.sh" ]; then
        echo "❌ Script de captura não encontrado!"
        return 1
    fi
    
    echo "💡 DICA: Para melhor resultado:"
    echo "   - Jogue por alguns níveis"
    echo "   - Colete power-ups"
    echo "   - Mostre os efeitos visuais"
    echo "   - Se possível, chegue até um boss"
    echo ""
    
    read -p "Duração da captura em segundos (padrão: 30): " duration
    duration=${duration:-30}
    
    ./quick_capture.sh "$duration"
}

# Função para trailer completo
full_trailer() {
    echo "🎬 CRIAÇÃO DE TRAILER COMPLETO"
    echo "============================="
    
    if [ ! -f "./trailer_creator.py" ]; then
        echo "❌ Script de trailer não encontrado!"
        return 1
    fi
    
    echo "📋 ROTEIRO SUGERIDO:"
    echo "1. Gameplay básico (15s) - Movimento e tiro"
    echo "2. Power-ups (15s) - Coletando upgrades"
    echo "3. Boss fight (20s) - Luta épica"
    echo "4. Sistemas (10s) - Loja e progressão"
    echo ""
    
    python3 ./trailer_creator.py
}

# Função para gerar assets Steam
generate_steam_assets() {
    echo "🎨 GERANDO ASSETS STEAM"
    echo "======================"
    
    if [ ! -f "./steam_assets_generator.py" ]; then
        echo "❌ Gerador de assets não encontrado!"
        return 1
    fi
    
    echo "🎨 Criando imagens para Steam Store..."
    echo "   - Header Capsule (460x215)"
    echo "   - Main Capsule (616x353)"
    echo "   - Small Capsule (231x87)"
    echo "   - Library Hero (600x900)"
    echo ""
    
    python3 ./steam_assets_generator.py
}

# Função para mostrar estratégia de marketing
show_marketing_strategy() {
    echo "📊 ESTRATÉGIA DE MARKETING"
    echo "========================="
    
    if [ -f "./marketing_strategy.md" ]; then
        echo "📄 Abrindo estratégia completa..."
        
        # Tentar abrir com diferentes editores
        if command -v code &> /dev/null; then
            code ./marketing_strategy.md
        elif command -v gedit &> /dev/null; then
            gedit ./marketing_strategy.md &
        elif command -v nano &> /dev/null; then
            nano ./marketing_strategy.md
        else
            cat ./marketing_strategy.md
        fi
    else
        echo "❌ Arquivo de estratégia não encontrado!"
    fi
}

# Função para testar o jogo
test_game() {
    echo "🎮 TESTANDO O JOGO"
    echo "================="
    
    if [ ! -f "./game.py" ]; then
        echo "❌ Arquivo do jogo não encontrado!"
        return 1
    fi
    
    echo "🎮 Iniciando Psychedelic River Raid..."
    echo "💡 Teste os controles e veja se tudo funciona antes de gravar"
    echo ""
    
    python3 ./game.py
}

# Função para setup completo
full_setup() {
    echo "🔧 SETUP COMPLETO - CRIAÇÃO DE TRAILER"
    echo "======================================"
    
    echo "📝 Passo 1: Gerando estratégia de marketing..."
    show_marketing_strategy
    
    echo ""
    echo "🎨 Passo 2: Gerando assets Steam..."
    generate_steam_assets
    
    echo ""
    echo "🎥 Passo 3: Preparando captura de trailer..."
    echo "💡 Agora você pode:"
    echo "   - Usar opção 1 para captura rápida"
    echo "   - Usar opção 2 para trailer completo guiado"
    echo ""
    
    read -p "Deseja fazer uma captura rápida agora? (y/n): " do_capture
    if [ "$do_capture" = "y" ] || [ "$do_capture" = "Y" ]; then
        quick_capture
    fi
}

# Função para gerar conteúdo de redes sociais
social_media_guide() {
    echo "📱 GUIA DE REDES SOCIAIS"
    echo "======================="
    
    # Criar diretório para social media
    mkdir -p "./social_media_content"
    
    # Criar templates de posts
    cat > "./social_media_content/twitter_posts.txt" << 'EOF'
# 🐦 TWITTER/X POSTS - Psychedelic River Raid

## Post de Lançamento
🚀 The psychedelic journey begins! Pilot your cosmic ship through reality-bending levels in Psychedelic River Raid. Now available on Steam! 

✨ Features:
• Elaborate ship design with energy effects
• 5 engagement systems 
• Epic boss battles every 5 levels
• Procedural chiptune music

#IndieGame #PsychedelicArt #RetroGaming #Steam #ShootEmUp

## Posts de Gameplay
🎮 Master the art of psychedelic combat! Collect power-ups, chain combos, and face challenging bosses in this mind-bending shoot 'em up.

🎵 Our procedural chiptune engine creates unique soundtracks that adapt to your gameplay intensity!

🏆 5 progression systems keep you engaged:
• Daily missions
• Achievement unlocks  
• Combo mastery
• Ship customization
• Level progression

## Posts com Screenshots
[Include gameplay GIF] 
When classic River Raid meets psychedelic art magic happens! ✨

#GameDev #IndieGame #RetroGaming #PsychedelicArt
EOF

    cat > "./social_media_content/instagram_posts.txt" << 'EOF'
# 📸 INSTAGRAM POSTS - Psychedelic River Raid

## Post Principal
🚀✨ Dive into a psychedelic dimension where classic arcade action meets modern game design!

Psychedelic River Raid transforms the beloved shoot 'em up formula with:
🎨 Stunning psychedelic visuals
🎵 Dynamic chiptune music generation  
🎮 5 engaging progression systems
👾 Epic boss battles
🚁 Elaborate ship design

Perfect for retro gaming enthusiasts and psychedelic art lovers!

#IndieGame #PsychedelicArt #RetroGaming #GameDev #ShootEmUp #Steam #ChiptuneMusic #ArcadeGame

## Stories Ideas
- Behind-the-scenes development
- Polls: "Which visual effect is your favorite?"
- Quick gameplay clips
- Music samples with waveform visuals
- "Guess the boss level" challenges

## Reels Ideas  
- Ship customization showcase
- Boss fight compilation
- Visual effects montage
- Before/after power-up transformation
EOF

    cat > "./social_media_content/youtube_description.txt" << 'EOF'
# 📺 YOUTUBE VIDEO DESCRIPTIONS

## Trailer Oficial
🚀 Experience the ultimate psychedelic shoot 'em up adventure!

Psychedelic River Raid reimagines the classic arcade formula with:
✨ Mind-bending visual effects
🎵 Procedural chiptune music engine
🎮 5 comprehensive progression systems  
👾 Epic boss battles every 5 levels
🚁 Elaborate ship design with energy effects

Built with passion using Python and Pygame, this indie gem proves that classic gameplay can be enhanced with modern programming and artistic vision.

Perfect for fans of:
• Classic arcade shooters
• Retro gaming
• Psychedelic art
• Chiptune music
• Indie games

🎮 Available now on Steam!
💝 Support indie game development!

#PsychedelicRiverRaid #IndieGame #Steam #RetroGaming #ShootEmUp

Timestamps:
0:00 - Intro
0:05 - Core Gameplay
0:20 - Progression Systems
0:35 - Boss Battles  
0:50 - Available Now

## Gameplay Overview
Dive deep into the mechanics and features of Psychedelic River Raid! 

In this video, we explore:
• The elaborate ship design and controls
• All 5 engagement systems in detail
• Boss battle strategies
• Power-up combinations
• Visual effect customization
• Music generation system

Whether you're a retro gaming veteran or new to shoot 'em ups, this guide will help you master the psychedelic skies!

🎮 Get the game: [Steam Link]
💬 Join our community: [Discord Link]
🐦 Follow updates: [Twitter Link]
EOF

    echo "📱 Conteúdo para redes sociais criado em ./social_media_content/"
    echo ""
    echo "📋 Arquivos criados:"
    echo "   - twitter_posts.txt"
    echo "   - instagram_posts.txt"  
    echo "   - youtube_description.txt"
    echo ""
    echo "💡 Use estes templates para suas campanhas de marketing!"
}

# Loop principal
while true; do
    show_menu
    read -p "Escolha uma opção (1-8): " choice
    echo ""
    
    case $choice in
        1)
            quick_capture
            ;;
        2)
            full_trailer
            ;;
        3)
            generate_steam_assets
            ;;
        4)
            social_media_guide
            ;;
        5)
            test_game
            ;;
        6)
            show_marketing_strategy
            ;;
        7)
            full_setup
            ;;
        8)
            echo "👋 Obrigado por usar o Trailer Creator!"
            echo "🚀 Boa sorte com o lançamento do Psychedelic River Raid!"
            exit 0
            ;;
        *)
            echo "❌ Opção inválida! Escolha entre 1-8."
            ;;
    esac
    
    echo ""
    echo "─────────────────────────────────────────"
    read -p "Pressione ENTER para continuar..."
    echo ""
done