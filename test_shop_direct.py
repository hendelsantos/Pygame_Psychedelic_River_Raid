#!/usr/bin/env python3
"""
Teste DIRETO da loja - Sem menu, direto na loja
"""

import pygame
import os
from shop import Shop
from save_system import SaveSystem

def test_shop_direct():
    os.environ['SDL_VIDEODRIVER'] = 'x11'
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("🛒 TESTE DIRETO DA LOJA")
    
    clock = pygame.time.Clock()
    
    # Criar sistema de save e loja
    print("💾 Inicializando save system...")
    save_system = SaveSystem()
    
    print(f"💰 Moedas disponíveis: {save_system.get_coins()}")
    
    # Se não tiver moedas, adicionar algumas para teste
    if save_system.get_coins() < 100:
        print("💰 Adicionando 1000 moedas para teste...")
        save_system.add_coins(1000)
    
    print("🛒 Inicializando loja...")
    shop = Shop(800, 600, save_system)
    
    print("\n" + "="*60)
    print("🎮 LOJA ABERTA!")
    print("="*60)
    print("📝 Controles:")
    print("   ⬆️  ⬇️  - Navegar entre upgrades")
    print("   ENTER ou ESPAÇO - Comprar upgrade selecionado")
    print("   ESC - Sair da loja")
    print("="*60)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Processar input da loja
            action = shop.handle_input(event)
            
            if action == 'exit':
                print("\n✅ Saindo da loja...")
                running = False
            elif action == 'purchase':
                print("✅ Compra realizada!")
            elif action == 'cannot_afford':
                print("❌ Moedas insuficientes!")
            elif action == 'navigate':
                print(f"🔄 Navegando... (Item {shop.selected_upgrade})")
        
        # Atualizar e desenhar
        shop.update()
        shop.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("\n🛑 Teste finalizado!")
    print(f"💰 Moedas restantes: {save_system.get_coins()}")

if __name__ == "__main__":
    test_shop_direct()