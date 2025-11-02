#!/usr/bin/env python3
"""
Teste simples do pygame para verificar se a janela abre
"""

import pygame
import sys

def test_pygame():
    print("🔧 Testando pygame...")
    
    # Inicializar pygame
    pygame.init()
    
    # Criar janela
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Teste - Psychedelic River Raid")
    
    # Cores
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    
    # Clock para controlar FPS
    clock = pygame.time.Clock()
    
    print("✅ Janela criada! Deveria aparecer na tela.")
    print("📝 Controles: ESC para sair")
    
    # Loop principal
    running = True
    while running:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Desenhar
        screen.fill(BLACK)
        
        # Desenhar um quadrado vermelho se movendo
        time_now = pygame.time.get_ticks()
        x = 400 + 200 * math.sin(time_now / 1000)
        y = 300 + 100 * math.cos(time_now / 1000)
        
        pygame.draw.rect(screen, RED, (x-25, y-25, 50, 50))
        
        # Texto
        font = pygame.font.Font(None, 74)
        text = font.render("TESTE DO JOGO", True, WHITE)
        text_rect = text.get_rect(center=(400, 100))
        screen.blit(text, text_rect)
        
        # Atualizar tela
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("🛑 Jogo fechado.")

if __name__ == "__main__":
    import math
    test_pygame()