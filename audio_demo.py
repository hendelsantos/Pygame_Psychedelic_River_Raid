#!/usr/bin/env python3
"""
Demonstração do Sistema de Áudio Procedural
Testa todos os sons do jogo individualmente
"""

import pygame
import time
import sys
from audio_engine import AudioEngine

def main():
    """Demonstrar todos os sons do jogo"""
    print("🎵 PSYCHEDELIC RIVER RAID - DEMO DE ÁUDIO")
    print("=" * 50)
    
    # Inicializar pygame
    pygame.init()
    
    # Criar engine de áudio
    print("Inicializando sistema de áudio...")
    audio = AudioEngine()
    
    try:
        # Demonstrar cada som
        print("\n1. 🚀 Som do Motor da Nave (5 segundos)")
        audio.play_sound('engine')
        time.sleep(5)
        audio.ambient_channel.stop()
        
        print("\n2. 💥 Som de Tiro Laser")
        for i in range(3):
            audio.play_sound('laser')
            time.sleep(0.3)
        
        print("\n3. 🎯 Som de Inimigo Atingido")
        for i in range(3):
            audio.play_sound('enemy_hit')
            time.sleep(0.5)
        
        print("\n4. 💥 Som de Explosão")
        audio.play_sound('explosion')
        time.sleep(2)
        
        print("\n5. ⭐ Som de Power-up")
        audio.play_sound('powerup')
        time.sleep(2)
        
        print("\n6. 🎶 Música de Fundo Procedural (10 segundos)")
        print("   Pressione Ctrl+C para parar...")
        audio.start_background_music()
        time.sleep(10)
        
        print("\n🎵 Demonstração completa!")
        
    except KeyboardInterrupt:
        print("\n👋 Demonstração interrompida pelo usuário")
    
    finally:
        print("Limpando recursos de áudio...")
        audio.cleanup()
        pygame.quit()

if __name__ == "__main__":
    main()