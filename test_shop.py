#!/usr/bin/env python3
"""
Teste simplificado para verificar se TAB abre a loja
"""

import pygame
import sys
import os

def test_shop():
    # Configurar pygame com SDL
    os.environ['SDL_VIDEODRIVER'] = 'x11'
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Teste - TAB para Loja")
    
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    shop_open = False
    
    print("🎮 Jogo iniciado!")
    print("📝 Controles:")
    print("   TAB - Abrir/Fechar loja")
    print("   ESC - Sair")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_TAB:
                    shop_open = not shop_open
                    if shop_open:
                        print("🛒 LOJA ABERTA!")
                    else:
                        print("❌ LOJA FECHADA!")
        
        # Desenhar
        if shop_open:
            screen.fill((50, 50, 100))  # Azul escuro para loja
            text = font.render("LOJA ABERTA", True, (255, 255, 255))
            text2 = font.render("TAB para fechar", True, (200, 200, 200))
        else:
            screen.fill((20, 20, 20))   # Preto para jogo
            text = font.render("JOGO PRINCIPAL", True, (255, 255, 255))
            text2 = font.render("TAB para abrir loja", True, (200, 200, 200))
        
        screen.blit(text, (400 - text.get_width()//2, 250))
        screen.blit(text2, (400 - text2.get_width()//2, 300))
        
        # Instruções
        esc_text = font.render("ESC para sair", True, (100, 100, 100))
        screen.blit(esc_text, (400 - esc_text.get_width()//2, 400))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("🛑 Teste finalizado!")

if __name__ == "__main__":
    test_shop()