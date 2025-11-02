#!/usr/bin/env python3
"""
Trailer Creator para Psychedelic River Raid
Script automatizado para capturar gameplay e criar trailer profissional
"""

import subprocess
import time
import os
import sys
from datetime import datetime

class TrailerCreator:
    def __init__(self):
        self.project_dir = "/home/hendel/Estudos/Pygame/game1"
        self.trailer_dir = f"{self.project_dir}/trailer_footage"
        self.output_dir = f"{self.project_dir}/trailer_output"
        
        # Criar diretórios se não existirem
        os.makedirs(self.trailer_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        print("🎬 TRAILER CREATOR - Psychedelic River Raid")
        print("=" * 50)
    
    def capture_gameplay(self, duration=60, scene_name="gameplay"):
        """Captura gameplay usando FFmpeg"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{self.trailer_dir}/{scene_name}_{timestamp}.mp4"
        
        print(f"🎥 Iniciando captura: {scene_name}")
        print(f"⏱️ Duração: {duration} segundos")
        print("🎮 INICIE O JOGO AGORA!")
        print("⏰ Captura começará em 5 segundos...")
        
        # Countdown
        for i in range(5, 0, -1):
            print(f"   {i}...")
            time.sleep(1)
        
        print("🔴 GRAVANDO!")
        
        # Comando FFmpeg para capturar tela
        cmd = [
            "ffmpeg",
            "-f", "x11grab",
            "-s", "800x600",  # Resolução do jogo
            "-r", "60",       # 60 FPS
            "-i", ":0.0",     # Display
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",     # Alta qualidade
            "-y",             # Sobrescrever
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ Captura salva: {output_file}")
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro na captura: {e}")
            return None
    
    def create_trailer_script(self):
        """Cria roteiro de captura para o trailer"""
        scenes = [
            {
                "name": "intro_gameplay",
                "duration": 15,
                "description": "Gameplay inicial - movimentação e tiro básico"
            },
            {
                "name": "powerups",
                "duration": 20,
                "description": "Coletando power-ups e evoluindo"
            },
            {
                "name": "boss_fight",
                "duration": 25,
                "description": "Luta contra boss do nível 5"
            },
            {
                "name": "progression",
                "duration": 15,
                "description": "Sistema de progressão e loja"
            }
        ]
        
        print("\n🎬 ROTEIRO DE CAPTURA")
        print("=" * 30)
        
        for i, scene in enumerate(scenes, 1):
            print(f"\n📹 CENA {i}: {scene['name']}")
            print(f"   Duração: {scene['duration']}s")
            print(f"   Foco: {scene['description']}")
            
            input("\n   Pressione ENTER quando estiver pronto para gravar...")
            
            captured_file = self.capture_gameplay(
                duration=scene['duration'],
                scene_name=scene['name']
            )
            
            if captured_file:
                print(f"   ✅ Cena {i} capturada com sucesso!")
            else:
                print(f"   ❌ Falha na captura da cena {i}")
                
            print("\n" + "─" * 50)
    
    def create_trailer_effects(self):
        """Cria efeitos visuais para o trailer"""
        effects_script = f"""
# TRAILER EFFECTS SCRIPT
# Para usar com editor de vídeo como DaVinci Resolve, Premiere, etc.

## EFEITOS RECOMENDADOS:

### 1. INTRO (0-3s)
- Fade in do logo "Psychedelic River Raid"
- Efeito de glitch psicodélico
- Música crescente

### 2. GAMEPLAY CORE (3-20s)
- Cortes rápidos do gameplay
- Zoom nos efeitos visuais psicodélicos
- Sincronização com a música chiptune

### 3. FEATURES HIGHLIGHT (20-35s)
- Text overlays mostrando features:
  * "Sistema de Progressão"
  * "5 Sistemas de Engajamento"
  * "Boss Fights Épicos"
  * "Audio Engine Procedural"

### 4. BOSS FIGHT (35-50s)
- Sequência intensa da luta contra boss
- Slow motion nos momentos épicos
- Música mais intensa

### 5. CALL TO ACTION (50-60s)
- "Available on Steam"
- Logo Steam
- "Wishlist Now!"
- URL do jogo

## TRANSIÇÕES:
- Glitch effects
- Chromatic aberration
- Flash cuts sincronizados com música

## TRILHA SONORA:
- Usar a música chiptune do próprio jogo
- Aumentar intensidade gradualmente
- Picos nos momentos de ação
"""
        
        effects_file = f"{self.output_dir}/trailer_effects_guide.txt"
        with open(effects_file, 'w') as f:
            f.write(effects_script)
        
        print(f"📝 Guia de efeitos salvo em: {effects_file}")
    
    def generate_steam_assets(self):
        """Gera templates para assets do Steam"""
        
        # Steam Capsule sizes
        steam_assets = {
            "header": "460x215",      # Store header
            "small": "231x87",        # Small capsule
            "main": "616x353",        # Main capsule
            "library": "600x900",     # Library hero
            "background": "1920x1080" # Page background
        }
        
        steam_guide = f"""
# 🎨 STEAM ASSETS GUIDE - Psychedelic River Raid

## DIMENSÕES OBRIGATÓRIAS:

### 1. Header Capsule: 460x215px
- Principal imagem da loja
- Deve ter logo + nave + efeitos

### 2. Small Capsule: 231x87px  
- Versão pequena para listas
- Logo legível em tamanho pequeno

### 3. Main Capsule: 616x353px
- Imagem principal da página
- Mais espaço para detalhes visuais

### 4. Library Hero: 600x900px
- Imagem vertical para biblioteca
- Composição diferente

### 5. Page Background: 1920x1080px
- Fundo da página da loja
- Pode ser screenshot do jogo

## DIRETRIZES VISUAIS:

### ELEMENTOS OBRIGATÓRIOS:
- Logo "Psychedelic River Raid"
- Nave do jogador em destaque
- Efeitos psicodélicos de fundo
- Cores vibrantes do jogo

### ESTILO:
- Manter paleta de cores do jogo
- Efeitos de neon/glow
- Partículas e trails
- Fundo com inimigos desfocados

### TEXTO:
- Fonte readable mesmo em tamanho pequeno
- Contraste adequado com fundo
- Tagline: "Psychedelic Shoot 'Em Up Experience"

## SCREENSHOTS (6 obrigatórios):
1. Gameplay básico - nave + inimigos
2. Boss fight em ação
3. Sistema de progressão/loja
4. Efeitos visuais em destaque
5. Power-ups sendo coletados
6. Menu principal

Todos em 1920x1080 ou 1280x720
"""
        
        assets_file = f"{self.output_dir}/steam_assets_guide.txt"
        with open(assets_file, 'w') as f:
            f.write(steam_guide)
        
        print(f"🎨 Guia de assets Steam salvo em: {assets_file}")
    
    def create_social_media_templates(self):
        """Cria templates para redes sociais"""
        social_guide = f"""
# 📱 SOCIAL MEDIA TEMPLATES - Psychedelic River Raid

## DIMENSÕES POR PLATAFORMA:

### TWITTER/X:
- Post Image: 1200x675px
- Header: 1500x500px
- Video: 1280x720px (máx 2:20)

### INSTAGRAM:
- Feed Post: 1080x1080px (quadrado)
- Stories: 1080x1920px (9:16)
- Reels: 1080x1920px (vertical)

### YOUTUBE:
- Thumbnail: 1280x720px
- Banner: 2560x1440px
- Shorts: 1080x1920px

### TIKTOK:
- Video: 1080x1920px (9:16)
- Duração: 15-60s

## CONTEÚDO SUGERIDO:

### POSTS PROMOCIONAIS:
1. "Coming to Steam soon!"
2. "Boss fights are intense! 🐉"
3. "Psychedelic visuals + chiptune music = ❤️"
4. "5 engagement systems keep you hooked!"
5. "River Raid meets Psychedelic art"

### HASHTAGS:
#IndieGame #Steam #GameDev #PsychedelicArt
#RetroGaming #ShootEmUp #ChiptuneMusic
#IndieGameDev #PixelArt #Pygame #Python

### GIFs/VIDEOS:
- Boss fight montage (15s)
- Power-up collection compilation
- Visual effects showcase
- Before/after progression
"""
        
        social_file = f"{self.output_dir}/social_media_guide.txt"
        with open(social_file, 'w') as f:
            f.write(social_guide)
        
        print(f"📱 Guia de redes sociais salvo em: {social_file}")
    
    def run_full_trailer_creation(self):
        """Executa o processo completo de criação do trailer"""
        print("🚀 INICIANDO CRIAÇÃO COMPLETA DO TRAILER")
        print("=" * 50)
        
        # 1. Capturar gameplay
        print("\n📹 FASE 1: CAPTURA DE GAMEPLAY")
        choice = input("Deseja capturar novo gameplay? (y/n): ").lower()
        
        if choice == 'y':
            self.create_trailer_script()
        
        # 2. Gerar guias
        print("\n📝 FASE 2: GERANDO GUIAS E TEMPLATES")
        self.create_trailer_effects()
        self.generate_steam_assets()
        self.create_social_media_templates()
        
        # 3. Resumo final
        print("\n✅ TRAILER CREATION COMPLETO!")
        print("=" * 50)
        print(f"📁 Arquivos salvos em: {self.output_dir}")
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Editar vídeos capturados com DaVinci Resolve/Premiere")
        print("2. Criar assets gráficos para Steam")
        print("3. Preparar posts para redes sociais")
        print("4. Upload no Steam e divulgação!")
        
    def quick_screen_capture(self):
        """Captura rápida de 30 segundos para teste"""
        print("🎥 CAPTURA RÁPIDA - 30 segundos")
        print("🎮 Inicie o jogo e prepare uma boa sequência!")
        
        input("Pressione ENTER quando estiver pronto...")
        
        return self.capture_gameplay(duration=30, scene_name="quick_test")

def main():
    creator = TrailerCreator()
    
    print("\n🎬 OPÇÕES DISPONÍVEIS:")
    print("1. Captura rápida (30s)")
    print("2. Criação completa do trailer")
    print("3. Apenas gerar guias e templates")
    print("4. Sair")
    
    choice = input("\nEscolha uma opção (1-4): ")
    
    if choice == "1":
        creator.quick_screen_capture()
    elif choice == "2":
        creator.run_full_trailer_creation()
    elif choice == "3":
        creator.create_trailer_effects()
        creator.generate_steam_assets()
        creator.create_social_media_templates()
        print("✅ Guias gerados com sucesso!")
    elif choice == "4":
        print("👋 Até logo!")
    else:
        print("❌ Opção inválida!")

if __name__ == "__main__":
    main()