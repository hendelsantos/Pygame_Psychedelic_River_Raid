#!/usr/bin/env python3
"""
Teste específico da loja - Debug TAB
"""

import pygame
import sys
import os
from shop import Shop
from save_system import SaveSystem

def test_shop_integration():
    os.environ['SDL_VIDEODRIVER'] = 'x11'
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Teste Loja - Pressione TAB")
    
    clock = pygame.time.Clock()
    
    # Criar sistema de save e loja
    save_system = SaveSystem()
    shop = Shop(800, 600, save_system)
    
    # Estados
    in_game = True
    in_shop = False
    
    print("🎮 Teste da Loja Iniciado!")
    print("📝 Controles:")
    print("   TAB - Abrir loja")
    print("   ESC - Sair da loja/jogo")
    print("   No menu da loja: ENTER para comprar, setas para navegar")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                print(f"🔍 TECLA PRESSIONADA: {pygame.key.name(event.key)} (código: {event.key})")
                
                if not in_shop:  # No jogo
                    if event.key == pygame.K_TAB:
                        print("🛒 TAB DETECTADO! Abrindo loja...")
                        in_shop = True
                        in_game = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                else:  # Na loja
                    action = shop.handle_input(event)
                    print(f"🛒 Ação da loja: {action}")
                    
                    if action == 'exit' or event.key == pygame.K_ESCAPE:
                        print("🛒 Fechando loja...")
                        in_shop = False
                        in_game = True
        
        # Desenhar
        if in_shop:
            # Desenhar loja
            shop.update()
            shop.draw(screen)
        else:
            # Desenhar "jogo"
            screen.fill((20, 40, 20))
            font = pygame.font.Font(None, 48)
            text = font.render("PRESSIONE TAB PARA LOJA", True, (255, 255, 255))
            screen.blit(text, (400 - text.get_width()//2, 250))
            
            font_small = pygame.font.Font(None, 24)
            coins_text = font_small.render(f"Moedas: {save_system.get_coins()}", True, (255, 255, 0))
            screen.blit(coins_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("🛑 Teste finalizado!")

if __name__ == "__main__":
    test_shop_integration()