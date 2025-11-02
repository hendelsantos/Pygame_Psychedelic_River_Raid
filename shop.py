import pygame
import math
import random
import colorsys


class Shop:
    """Sistema de loja com upgrades permanentes"""
    
    def __init__(self, width, height, save_system):
        self.width = width
        self.height = height
        self.save_system = save_system
        
        # Fonte
        self.title_font = pygame.font.Font(None, 72)
        self.upgrade_font = pygame.font.Font(None, 40)
        self.desc_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 24)
        
        # Estado da loja
        self.selected_upgrade = 0
        self.animation_frame = 0
        self.particles = []
        
        # Definir upgrades disponíveis
        self.upgrades = [
            {
                'id': 'max_health',
                'name': 'Vida Máxima',
                'description': 'Aumenta vida máxima em 20',
                'icon': '❤️',
                'base_cost': 100,
                'max_level': 10,
                'color': (255, 50, 50)
            },
            {
                'id': 'fire_rate',
                'name': 'Cadência de Tiro',
                'description': 'Reduz tempo entre tiros',
                'icon': '⚡',
                'base_cost': 150,
                'max_level': 5,
                'color': (255, 255, 50)
            },
            {
                'id': 'bullet_damage',
                'name': 'Dano de Bala',
                'description': 'Aumenta dano causado',
                'icon': '💥',
                'base_cost': 200,
                'max_level': 5,
                'color': (255, 100, 0)
            },
            {
                'id': 'speed',
                'name': 'Velocidade',
                'description': 'Aumenta velocidade de movimento',
                'icon': '🚀',
                'base_cost': 120,
                'max_level': 5,
                'color': (50, 150, 255)
            },
            {
                'id': 'shield',
                'name': 'Escudo',
                'description': 'Absorve 1 hit por nível',
                'icon': '🛡️',
                'base_cost': 250,
                'max_level': 3,
                'color': (100, 200, 255)
            },
            {
                'id': 'coin_multiplier',
                'name': 'Multiplicador de Moedas',
                'description': '+10% moedas por nível',
                'icon': '💰',
                'base_cost': 180,
                'max_level': 5,
                'color': (255, 215, 0)
            }
        ]
        
    def get_upgrade_level(self, upgrade_id):
        """Obter nível atual de um upgrade"""
        upgrades_data = self.save_system.get_upgrades()
        return upgrades_data.get(upgrade_id, 0)
    
    def get_upgrade_cost(self, upgrade):
        """Calcular custo baseado no nível atual"""
        current_level = self.get_upgrade_level(upgrade['id'])
        # Custo aumenta exponencialmente
        return int(upgrade['base_cost'] * (1.5 ** current_level))
    
    def can_afford(self, upgrade):
        """Verificar se jogador pode comprar upgrade"""
        coins = self.save_system.get_coins()
        cost = self.get_upgrade_cost(upgrade)
        current_level = self.get_upgrade_level(upgrade['id'])
        return coins >= cost and current_level < upgrade['max_level']
    
    def purchase_upgrade(self, upgrade):
        """Comprar upgrade"""
        if not self.can_afford(upgrade):
            return False
        
        cost = self.get_upgrade_cost(upgrade)
        current_level = self.get_upgrade_level(upgrade['id'])
        
        # Deduzir moedas
        self.save_system.spend_coins(cost)
        
        # Aumentar nível do upgrade
        self.save_system.upgrade_stat(upgrade['id'], current_level + 1)
        
        # Criar partículas de compra
        self.create_purchase_particles(upgrade['color'])
        
        return True
    
    def create_purchase_particles(self, color):
        """Criar partículas de efeito de compra"""
        for _ in range(30):
            angle = math.radians(random.uniform(0, 360))
            speed = random.uniform(2, 8)
            self.particles.append({
                'x': self.width // 2,
                'y': self.height // 2,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 60,
                'max_life': 60,
                'color': color,
                'size': random.uniform(2, 6)
            })
    
    def update(self):
        """Atualizar animações"""
        self.animation_frame += 0.05
        
        # Atualizar partículas
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # Gravidade
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def handle_input(self, event):
        """Processar entrada do jogador"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_upgrade = (self.selected_upgrade - 1) % len(self.upgrades)
                return 'navigate'
            elif event.key == pygame.K_DOWN:
                self.selected_upgrade = (self.selected_upgrade + 1) % len(self.upgrades)
                return 'navigate'
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                upgrade = self.upgrades[self.selected_upgrade]
                if self.purchase_upgrade(upgrade):
                    return 'purchase'
                else:
                    return 'cannot_afford'
            elif event.key == pygame.K_ESCAPE:
                return 'exit'
        
        return None
    
    def get_psychedelic_color(self, hue_offset=0.0, brightness=1.0):
        """Gerar cor psicodélica animada"""
        hue = (hue_offset + self.animation_frame * 0.02) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 1.0, brightness)
        return tuple(int(c * 255) for c in rgb)
    
    def draw(self, screen):
        """Desenhar interface da loja"""
        # Fundo escuro com gradiente
        for y in range(0, self.height, 4):
            alpha = y / self.height
            color = self.get_psychedelic_color(alpha * 0.3, 0.1 + alpha * 0.1)
            pygame.draw.line(screen, color, (0, y), (self.width, y), 4)
        
        # Título
        title_color = self.get_psychedelic_color(0.0, 1.0)
        title = self.title_font.render("🛒 LOJA", True, title_color)
        title_rect = title.get_rect(center=(self.width // 2, 40))
        screen.blit(title, title_rect)
        
        # Moedas disponíveis
        coins = self.save_system.get_coins()
        coins_text = self.upgrade_font.render(f"💰 {coins}", True, (255, 215, 0))
        coins_rect = coins_text.get_rect(center=(self.width // 2, 85))
        screen.blit(coins_text, coins_rect)
        
        # Desenhar upgrades - LAYOUT EM GRADE 2x4
        start_y = 130
        spacing_y = 55  # Espaçamento vertical reduzido
        items_per_row = 2
        column_width = 380
        start_x_left = 20
        start_x_right = 420
        
        for i, upgrade in enumerate(self.upgrades):
            # Calcular posição em grade
            row = i // items_per_row
            col = i % items_per_row
            
            x_pos = start_x_left if col == 0 else start_x_right
            y_pos = start_y + row * spacing_y
            
            # Verificar se está selecionado
            is_selected = (i == self.selected_upgrade)
            
            # Nível atual
            current_level = self.get_upgrade_level(upgrade['id'])
            cost = self.get_upgrade_cost(upgrade)
            can_buy = self.can_afford(upgrade)
            is_maxed = current_level >= upgrade['max_level']
            
            # Background da opção
            if is_selected:
                pulse = math.sin(self.animation_frame * 0.2) * 5 + 5
                rect_width = column_width + int(pulse)
                bg_color = (*upgrade['color'], 80)
            else:
                rect_width = column_width
                bg_color = (40, 40, 40, 100)
            
            bg_rect = pygame.Rect(x_pos, y_pos - 5, rect_width - 20, 50)
            
            # Desenhar background
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(bg_surface, bg_color, bg_surface.get_rect(), border_radius=8)
            screen.blit(bg_surface, bg_rect)
            
            # Borda
            border_color = self.get_psychedelic_color(i * 0.15) if is_selected else (100, 100, 100)
            pygame.draw.rect(screen, border_color, bg_rect, 2, border_radius=8)
            
            # Ícone (menor)
            icon_text = self.desc_font.render(upgrade['icon'], True, (255, 255, 255))
            screen.blit(icon_text, (bg_rect.x + 10, y_pos))
            
            # Nome (compacto)
            name_color = upgrade['color'] if not is_maxed else (150, 150, 150)
            name_text = self.desc_font.render(upgrade['name'], True, name_color)
            screen.blit(name_text, (bg_rect.x + 45, y_pos - 2))
            
            # Nível (compacto) 
            level_text = f"Lv.{current_level}/{upgrade['max_level']}"
            level_surface = self.small_font.render(level_text, True, (180, 180, 180))
            screen.blit(level_surface, (bg_rect.x + 45, y_pos + 18))
            
            # Custo ou MAX (à direita)
            if is_maxed:
                status_text = "MAX"
                status_color = (0, 255, 0)
                status_font = self.small_font
            elif can_buy:
                status_text = f"{cost}"
                status_color = (255, 215, 0)
                status_font = self.small_font
            else:
                status_text = f"{cost}"
                status_color = (120, 120, 120)
                status_font = self.small_font
            
            status_surface = status_font.render(status_text, True, status_color)
            status_rect = status_surface.get_rect(right=bg_rect.right - 10, centery=bg_rect.centery)
            screen.blit(status_surface, status_rect)
        
        # Descrição do upgrade selecionado (parte inferior)
        selected = self.upgrades[self.selected_upgrade]
        desc_y = self.height - 80
        
        # Box de descrição
        desc_box = pygame.Rect(50, desc_y - 10, self.width - 100, 40)
        desc_surface = pygame.Surface((desc_box.width, desc_box.height), pygame.SRCALPHA)
        pygame.draw.rect(desc_surface, (30, 30, 30, 200), desc_surface.get_rect(), border_radius=5)
        screen.blit(desc_surface, desc_box)
        pygame.draw.rect(screen, self.get_psychedelic_color(0.5), desc_box, 2, border_radius=5)
        
        desc_text = self.desc_font.render(selected['description'], True, (220, 220, 220))
        desc_rect = desc_text.get_rect(center=(self.width // 2, desc_y + 10))
        screen.blit(desc_text, desc_rect)
        
        # Instruções (rodapé)
        inst_y = self.height - 25
        inst_text = self.small_font.render("↑↓ Navegar | ENTER Comprar | ESC Sair", True, (130, 130, 130))
        inst_rect = inst_text.get_rect(center=(self.width // 2, inst_y))
        screen.blit(inst_text, inst_rect)
        
        # Desenhar partículas
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / particle['max_life']))
            color = (*particle['color'], alpha)
            size = int(particle['size'] * (particle['life'] / particle['max_life']))
            
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color, (size, size), size)
            screen.blit(particle_surface, (int(particle['x']) - size, int(particle['y']) - size))
