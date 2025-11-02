#!/usr/bin/env python3
"""
Steam Assets Generator
Cria templates e capturas para assets do Steam automaticamente
"""

import pygame
import sys
import os
from datetime import datetime

# Adicionar o diretório do jogo ao path para importar módulos
sys.path.append('/home/hendel/Estudos/Pygame/game1')

class SteamAssetsGenerator:
    def __init__(self):
        pygame.init()
        
        # Dimensões dos assets Steam
        self.steam_sizes = {
            "header": (460, 215),      # Store header
            "small": (231, 87),        # Small capsule  
            "main": (616, 353),        # Main capsule
            "library": (600, 900),     # Library hero
            "background": (1920, 1080) # Page background
        }
        
        self.output_dir = "/home/hendel/Estudos/Pygame/game1/steam_assets"
        os.makedirs(self.output_dir, exist_ok=True)
        
        print("🎨 STEAM ASSETS GENERATOR")
        print("========================")
    
    def create_psychedelic_background(self, width, height, intensity=1.0):
        """Cria fundo psicodélico similar ao do jogo"""
        surface = pygame.Surface((width, height))
        surface.fill((0, 0, 0))
        
        import math
        import random
        
        # Criar efeito de ondas coloridas
        for y in range(0, height, 2):
            for x in range(0, width, 2):
                # Calcular cor baseada na posição
                wave1 = math.sin((x + y) * 0.01) * 50
                wave2 = math.cos(x * 0.015) * 30
                wave3 = math.sin(y * 0.02) * 40
                
                r = int(abs(wave1 + 100) * intensity) % 255
                g = int(abs(wave2 + 150) * intensity) % 255  
                b = int(abs(wave3 + 200) * intensity) % 255
                
                color = (min(255, r), min(255, g), min(255, b))
                pygame.draw.rect(surface, color, (x, y, 2, 2))
        
        return surface
    
    def draw_psychedelic_ship(self, surface, x, y, scale=1.0):
        """Desenha a nave psicodélica do jogo"""
        import math
        
        # Escala base
        base_size = int(20 * scale)
        
        # Cores psicodélicas
        def get_psychedelic_color(offset=0):
            time_factor = pygame.time.get_ticks() * 0.01 + offset
            r = int(abs(math.sin(time_factor) * 255))
            g = int(abs(math.sin(time_factor + 2) * 255))
            b = int(abs(math.sin(time_factor + 4) * 255))
            return (r, g, b)
        
        # Corpo principal da nave
        main_points = [
            (x, y - base_size),  # Topo
            (x - base_size//2, y + base_size//2),  # Esquerda
            (x, y),  # Centro
            (x + base_size//2, y + base_size//2)   # Direita
        ]
        pygame.draw.polygon(surface, get_psychedelic_color(), main_points)
        
        # Cockpit
        cockpit_size = int(base_size * 0.3)
        pygame.draw.circle(surface, get_psychedelic_color(1), 
                         (x, y - cockpit_size), cockpit_size)
        
        # Asas energéticas
        wing_color = get_psychedelic_color(2)
        wing_points_left = [
            (x - base_size//2, y),
            (x - base_size, y - base_size//4),
            (x - base_size, y + base_size//4)
        ]
        wing_points_right = [
            (x + base_size//2, y),
            (x + base_size, y - base_size//4),
            (x + base_size, y + base_size//4)
        ]
        
        pygame.draw.polygon(surface, wing_color, wing_points_left)
        pygame.draw.polygon(surface, wing_color, wing_points_right)
        
        # Efeitos de energia
        for i in range(5):
            energy_color = get_psychedelic_color(i)
            radius = int((base_size * 0.2) + i * 2)
            pygame.draw.circle(surface, energy_color, 
                             (x, y), radius, 1)
    
    def create_logo_text(self, surface, text, x, y, size, color=(255, 255, 255)):
        """Cria texto do logo com efeito glow"""
        font = pygame.font.Font(None, size)
        
        # Efeito glow
        for offset in range(3, 0, -1):
            glow_color = (color[0]//2, color[1]//2, color[2]//2)
            for dx in range(-offset, offset+1):
                for dy in range(-offset, offset+1):
                    if dx*dx + dy*dy <= offset*offset:
                        text_surface = font.render(text, True, glow_color)
                        text_rect = text_surface.get_rect(center=(x+dx, y+dy))
                        surface.blit(text_surface, text_rect)
        
        # Texto principal
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        surface.blit(text_surface, text_rect)
        
        return text_rect
    
    def create_header_capsule(self):
        """Cria header capsule 460x215"""
        width, height = self.steam_sizes["header"]
        surface = pygame.Surface((width, height))
        
        # Fundo psicodélico
        bg = self.create_psychedelic_background(width, height, 0.8)
        surface.blit(bg, (0, 0))
        
        # Nave principal
        ship_x = width // 4
        ship_y = height // 2
        self.draw_psychedelic_ship(surface, ship_x, ship_y, 2.0)
        
        # Logo
        title_x = width * 3 // 4
        title_y = height // 3
        self.create_logo_text(surface, "PSYCHEDELIC", title_x, title_y, 36)
        self.create_logo_text(surface, "RIVER RAID", title_x, title_y + 40, 32)
        
        # Tagline
        self.create_logo_text(surface, "Mind-Bending Shoot 'Em Up", 
                            title_x, title_y + 80, 16, (200, 200, 255))
        
        return surface
    
    def create_main_capsule(self):
        """Cria main capsule 616x353"""
        width, height = self.steam_sizes["main"]
        surface = pygame.Surface((width, height))
        
        # Fundo mais elaborado
        bg = self.create_psychedelic_background(width, height, 1.0)
        surface.blit(bg, (0, 0))
        
        # Múltiplas naves para mostrar gameplay
        positions = [
            (width//6, height//3, 1.5),
            (width//3, height*2//3, 1.2),
            (width*2//3, height//4, 1.8)
        ]
        
        for x, y, scale in positions:
            self.draw_psychedelic_ship(surface, x, y, scale)
        
        # Logo centralizado
        logo_x = width // 2
        logo_y = height // 6
        self.create_logo_text(surface, "PSYCHEDELIC RIVER RAID", 
                            logo_x, logo_y, 42)
        
        # Features
        features = [
            "5 Engagement Systems",
            "Epic Boss Battles", 
            "Procedural Music",
            "Psychedelic Visuals"
        ]
        
        feature_y = height * 5 // 6
        for i, feature in enumerate(features):
            feature_x = (width * (i + 1)) // (len(features) + 1)
            self.create_logo_text(surface, feature, feature_x, feature_y, 18, 
                                (255, 255, 100))
        
        return surface
    
    def create_small_capsule(self):
        """Cria small capsule 231x87"""
        width, height = self.steam_sizes["small"]
        surface = pygame.Surface((width, height))
        
        # Fundo simples
        bg = self.create_psychedelic_background(width, height, 0.6)
        surface.blit(bg, (0, 0))
        
        # Nave pequena
        ship_x = width // 4
        ship_y = height // 2
        self.draw_psychedelic_ship(surface, ship_x, ship_y, 1.0)
        
        # Logo compacto
        logo_x = width * 3 // 4
        logo_y = height // 2
        self.create_logo_text(surface, "PSYCHEDELIC", logo_x, logo_y - 10, 16)
        self.create_logo_text(surface, "RIVER RAID", logo_x, logo_y + 10, 14)
        
        return surface
    
    def create_library_hero(self):
        """Cria library hero 600x900"""
        width, height = self.steam_sizes["library"]
        surface = pygame.Surface((width, height))
        
        # Fundo vertical
        bg = self.create_psychedelic_background(width, height, 1.2)
        surface.blit(bg, (0, 0))
        
        # Nave grande centralizada
        ship_x = width // 2
        ship_y = height // 3
        self.draw_psychedelic_ship(surface, ship_x, ship_y, 3.0)
        
        # Logo no topo
        logo_y = height // 8
        self.create_logo_text(surface, "PSYCHEDELIC", width//2, logo_y, 48)
        self.create_logo_text(surface, "RIVER RAID", width//2, logo_y + 50, 42)
        
        # Informações na parte inferior
        info_y = height * 3 // 4
        info_items = [
            "Classic Arcade Action",
            "Modern Visual Effects", 
            "5 Progression Systems",
            "Epic Boss Battles",
            "Procedural Chiptune Music"
        ]
        
        for i, item in enumerate(info_items):
            item_y = info_y + (i * 30)
            self.create_logo_text(surface, item, width//2, item_y, 24, 
                                (255, 255, 150))
        
        return surface
    
    def generate_all_assets(self):
        """Gera todos os assets Steam"""
        print("🎨 Gerando assets Steam...")
        
        assets = {
            "header": self.create_header_capsule(),
            "main": self.create_main_capsule(), 
            "small": self.create_small_capsule(),
            "library": self.create_library_hero()
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for name, surface in assets.items():
            filename = f"{self.output_dir}/steam_{name}_{timestamp}.png"
            pygame.image.save(surface, filename)
            print(f"   ✅ {name}: {filename}")
        
        print(f"\n📁 Assets salvos em: {self.output_dir}")
        
        # Criar arquivo README com instruções
        readme_content = f"""
# Steam Assets - Psychedelic River Raid

Assets gerados em: {timestamp}

## Arquivos criados:
- steam_header_*.png (460x215) - Header da loja Steam
- steam_main_*.png (616x353) - Imagem principal da página
- steam_small_*.png (231x87) - Cápsula pequena para listas  
- steam_library_*.png (600x900) - Hero da biblioteca

## Como usar:
1. Faça upload no Steamworks
2. Configure cada asset na seção correspondente
3. Teste a visualização em diferentes resoluções
4. Ajuste cores/contraste se necessário

## Próximos passos:
- Criar screenshots do gameplay (1920x1080)
- Capturar trailer (1280x720 ou 1920x1080)
- Preparar descrições e tags
- Configurar preço e disponibilidade
"""
        
        readme_file = f"{self.output_dir}/README.md"
        with open(readme_file, 'w') as f:
            f.write(readme_content)
        
        print(f"📝 Instruções salvas em: {readme_file}")

def main():
    try:
        generator = SteamAssetsGenerator()
        generator.generate_all_assets()
        print("\n🎉 Assets Steam gerados com sucesso!")
        print("💡 Execute o trailer_creator.py para capturar gameplay")
        
    except Exception as e:
        print(f"❌ Erro ao gerar assets: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()