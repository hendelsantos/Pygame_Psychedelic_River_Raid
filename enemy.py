import pygame
import math
import random
import colorsys
from bullet import Bullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type='basic'):
        super().__init__()
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.animation_frame = 0
        
        # Inicializar atributos padrão (antes de setup_enemy_type)
        self.shield_health = 0
        self.max_shield = 0
        
        # Configurações baseadas no tipo
        self.setup_enemy_type()
        
        # Criar sprite
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Sistema de tiro
        self.shoot_cooldown = 0
        self.shoot_delay = random.randint(60, 120)  # frames entre tiros
        
        # Movimento
        self.movement_pattern = random.choice(['straight', 'zigzag', 'circle'])
        self.movement_timer = 0
        self.base_x = x
        
        # Efeitos visuais
        self.trail = []
        self.energy_field = random.uniform(0, 2 * math.pi)
    
    def setup_enemy_type(self):
        """Configurar propriedades baseadas no tipo de inimigo"""
        if self.enemy_type == 'basic':
            self.width = 25
            self.height = 25
            self.speed = 2
            self.health = 1
            self.max_health = 1
            self.color_base = 0.0  # Vermelho
            self.points = 100
            self.shoot_enabled = False
            
        elif self.enemy_type == 'fast':
            self.width = 20
            self.height = 20
            self.speed = 4
            self.health = 1
            self.max_health = 1
            self.color_base = 0.3  # Amarelo
            self.points = 150
            self.shoot_enabled = False
            
        elif self.enemy_type == 'shooter':
            self.width = 30
            self.height = 30
            self.speed = 1.5
            self.health = 2
            self.max_health = 2
            self.color_base = 0.8  # Magenta
            self.points = 200
            self.shoot_delay = 40  # Atira mais frequentemente
            self.shoot_enabled = True
        
        # NOVOS TIPOS DE INIMIGOS
        elif self.enemy_type == 'kamikaze':
            # Voa em direção ao jogador rapidamente
            self.width = 22
            self.height = 22
            self.speed = 5
            self.health = 1
            self.max_health = 1
            self.color_base = 0.05  # Laranja/Vermelho
            self.points = 180
            self.shoot_enabled = False
            self.kamikaze_mode = False
            self.target_x = 0
            self.target_y = 0
        
        elif self.enemy_type == 'tank':
            # Lento mas com muita vida
            self.width = 40
            self.height = 35
            self.speed = 1
            self.health = 10
            self.max_health = 10
            self.color_base = 0.55  # Ciano
            self.points = 500
            self.shoot_enabled = True
            self.shoot_delay = 80
        
        elif self.enemy_type == 'sniper':
            # Fica parado no topo e atira com precisão
            self.width = 25
            self.height = 25
            self.speed = 0.5
            self.health = 2
            self.max_health = 2
            self.color_base = 0.72  # Azul
            self.points = 250
            self.shoot_enabled = True
            self.shoot_delay = 90
            self.sniper_locked = False
            self.lock_position_y = 0
        
        elif self.enemy_type == 'splitter':
            # Divide em 2 menores ao morrer
            self.width = 35
            self.height = 35
            self.speed = 2
            self.health = 3
            self.max_health = 3
            self.color_base = 0.16  # Verde-amarelo
            self.points = 300
            self.shoot_enabled = False
            self.splits_enabled = True
        
        elif self.enemy_type == 'bomber':
            # Solta bombas que caem lentamente
            self.width = 32
            self.height = 28
            self.speed = 1.8
            self.health = 2
            self.max_health = 2
            self.color_base = 0.0  # Vermelho escuro
            self.points = 220
            self.shoot_enabled = True
            self.shoot_delay = 60
            self.bomb_mode = True
        
        elif self.enemy_type == 'healer':
            # Cura inimigos próximos
            self.width = 28
            self.height = 28
            self.speed = 1.5
            self.health = 2
            self.max_health = 2
            self.color_base = 0.33  # Verde
            self.points = 350
            self.shoot_enabled = False
            self.heal_cooldown = 0
            self.heal_delay = 180  # 3 segundos
        
        elif self.enemy_type == 'shield':
            # Tem escudo frontal que absorve dano
            self.width = 30
            self.height = 30
            self.speed = 1.5
            self.health = 4
            self.max_health = 4
            self.color_base = 0.66  # Azul claro
            self.points = 400
            self.shoot_enabled = True
            self.shoot_delay = 100
            self.has_shield = True
            self.shield_health = 5
        
        elif self.enemy_type == 'giant':
            # INIMIGO GIGANTE - Explosão espetacular!
            self.width = 80
            self.height = 80
            self.speed = 0.8
            self.health = 50  # MUITO MAIS DIFÍCIL DE MATAR!
            self.max_health = 50
            self.color_base = 0.9  # Rosa/Magenta
            self.points = 1000
            self.shoot_enabled = True
            self.shoot_delay = 30  # Atira muito!
            self.is_giant = True
            self.rotation = 0
            self.pulse = 0
        
        elif self.enemy_type == 'elite':
            # Inimigo ELITE - Muito forte
            self.width = 50
            self.height = 50
            self.speed = 2.5
            self.health = 30  # Mais resistente!
            self.max_health = 30
            self.color_base = 0.83  # Roxo
            self.points = 750
            self.shoot_enabled = True
            self.shoot_delay = 25
            self.is_elite = True
            self.dash_cooldown = 0
        
        else:
            # Padrão
            self.width = 25
            self.height = 25
            self.speed = 2
            self.health = 1
            self.max_health = 1
            self.color_base = 0.0
            self.points = 100
            self.shoot_enabled = False
            self.width = 30
            self.height = 30
            self.speed = 1.5
            self.health = 3
            self.max_health = 3
            self.shield_health = 5
            self.max_shield = 5
            self.color_base = 0.6  # Ciano
            self.points = 400
            self.shoot_enabled = True
            self.shoot_delay = 70
    
    def update(self, game_speed, player_x=None, player_y=None, enemies_group=None):
        """Atualizar inimigo"""
        # Movimento baseado no padrão
        self.movement_timer += 1
        
        # Comportamentos especiais por tipo
        if self.enemy_type == 'kamikaze' and player_x is not None and player_y is not None:
            # Kamikaze voa em direção ao jogador
            if not self.kamikaze_mode and self.y > 100:
                self.kamikaze_mode = True
                self.target_x = player_x
                self.target_y = player_y
            
            if self.kamikaze_mode:
                dx = self.target_x - self.x
                dy = self.target_y - self.y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist > 0:
                    self.x += (dx / dist) * (self.speed + 2)
                    self.y += (dy / dist) * (self.speed + 2)
            else:
                self.y += self.speed + game_speed
        
        elif self.enemy_type == 'sniper':
            # Sniper para em uma posição e atira
            if not self.sniper_locked and self.y > 100:
                self.sniper_locked = True
                self.lock_position_y = self.y
            
            if self.sniper_locked:
                self.y = self.lock_position_y  # Fica parado
                # Pequeno movimento horizontal
                self.x += math.sin(self.movement_timer * 0.05) * 1
            else:
                self.y += self.speed + game_speed
        
        elif self.enemy_type == 'healer' and enemies_group:
            # Healer cura inimigos próximos
            self.heal_cooldown -= 1
            if self.heal_cooldown <= 0:
                self.heal_nearby_enemies(enemies_group)
                self.heal_cooldown = self.heal_delay
            
            # Movimento padrão
            if self.movement_pattern == 'straight':
                self.y += self.speed + game_speed
            elif self.movement_pattern == 'zigzag':
                self.y += self.speed + game_speed
                amplitude = 40
                frequency = 0.08
                self.x = self.base_x + math.sin(self.movement_timer * frequency) * amplitude
        
        else:
            # Movimento padrão para outros tipos
            if self.movement_pattern == 'straight':
                self.y += self.speed + game_speed
                
            elif self.movement_pattern == 'zigzag':
                self.y += self.speed + game_speed
                amplitude = 50
                frequency = 0.1
                self.x = self.base_x + math.sin(self.movement_timer * frequency) * amplitude
                
            elif self.movement_pattern == 'circle':
                self.y += (self.speed + game_speed) * 0.7
                radius = 30
                angle = self.movement_timer * 0.1
                self.x = self.base_x + math.cos(angle) * radius
        
        # Atualizar posição do rect
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        
        # Reduzir cooldown de tiro
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # Atualizar animação
        self.animation_frame += 0.15
        self.energy_field += 0.1
        
        # Adicionar posição ao rastro
        self.trail.append((self.x, self.y))
        if len(self.trail) > 8:
            self.trail.pop(0)
    
    def heal_nearby_enemies(self, enemies_group):
        """Curar inimigos próximos (habilidade do healer)"""
        heal_range = 100
        heal_amount = 1
        
        for enemy in enemies_group:
            if enemy != self and hasattr(enemy, 'health') and hasattr(enemy, 'max_health'):
                dx = enemy.x - self.x
                dy = enemy.y - self.y
                dist = math.sqrt(dx*dx + dy*dy)
                
                if dist < heal_range and enemy.health < enemy.max_health:
                    enemy.health = min(enemy.max_health, enemy.health + heal_amount)
                    # Criar partícula de cura visual (opcional)
    
    def take_damage(self, amount=1):
        """Receber dano (considera escudo se tiver)"""
        if self.enemy_type == 'shield' and hasattr(self, 'shield_health') and self.shield_health > 0:
            # Escudo absorve o dano
            self.shield_health -= amount
            if self.shield_health < 0:
                # Dano excedente vai para a vida
                self.health += self.shield_health  # shield_health é negativo
                self.shield_health = 0
            return self.health > 0
        else:
            # Dano normal
            self.health -= amount
            return self.health > 0
    
    def can_split(self):
        """Verificar se o inimigo pode dividir (splitter)"""
        return self.enemy_type == 'splitter' and hasattr(self, 'splits_enabled') and self.splits_enabled
    
    def shoot(self, bullets_group, player_x=None, player_y=None):
        """Atirar projétil"""
        if self.shoot_cooldown > 0:
            return
        
        if not hasattr(self, 'shoot_enabled') or not self.shoot_enabled:
            return
        
        # Comportamento especial de tiro para cada tipo
        if self.enemy_type == 'shooter':
            # Tiro duplo
            bullet1 = Bullet(self.x - 10, self.y + self.height // 2, 
                            direction=1, color=(255, 0, 255), speed=6)
            bullet2 = Bullet(self.x + 10, self.y + self.height // 2, 
                            direction=1, color=(255, 0, 255), speed=6)
            bullets_group.add(bullet1, bullet2)
            self.shoot_cooldown = self.shoot_delay
        
        elif self.enemy_type == 'sniper' and player_x is not None and player_y is not None:
            # Tiro preciso em direção ao jogador
            dx = player_x - self.x
            dy = player_y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0:
                bullet = Bullet(self.x, self.y + self.height // 2,
                              direction=1, color=(0, 100, 255), speed=8)
                bullet.vel_x = (dx / dist) * 8
                bullet.vel_y = (dy / dist) * 8
                bullet.use_custom_movement = True
                bullets_group.add(bullet)
            self.shoot_cooldown = self.shoot_delay
        
        elif self.enemy_type == 'bomber':
            # Solta bomba que cai lentamente
            bomb = Bullet(self.x, self.y + self.height // 2,
                         direction=1, color=(255, 50, 0), speed=2)
            bullets_group.add(bomb)
            self.shoot_cooldown = self.shoot_delay
        
        elif self.enemy_type == 'tank':
            # Tiro triplo pesado
            for offset in [-15, 0, 15]:
                bullet = Bullet(self.x + offset, self.y + self.height // 2,
                              direction=1, color=(0, 255, 255), speed=5)
                bullets_group.add(bullet)
            self.shoot_cooldown = self.shoot_delay
        
        elif self.enemy_type == 'shield':
            # Tiro único mas poderoso
            bullet = Bullet(self.x, self.y + self.height // 2,
                          direction=1, color=(100, 255, 255), speed=7)
            bullets_group.add(bullet)
            self.shoot_cooldown = self.shoot_delay
        
        else:
            # Tiro padrão
            bullet = Bullet(self.x, self.y + self.height // 2, 
                          direction=1, color=(255, 100, 0), speed=5)
            bullets_group.add(bullet)
            self.shoot_cooldown = self.shoot_delay
    
    def get_psychedelic_color(self, hue_offset=0.0, brightness=1.0):
        """Gerar cor psicodélica"""
        hue = (self.color_base + hue_offset + self.animation_frame * 0.02) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 1.0, brightness)
        return tuple(int(c * 255) for c in rgb)
    
    def draw(self, screen):
        """Desenhar inimigo com efeitos psicodélicos"""
        # Desenhar rastro
        for i, pos in enumerate(self.trail):
            if i > 0:
                alpha = i / len(self.trail)
                size = max(1, int(alpha * 4))
                trail_color = self.get_psychedelic_color(0.5, alpha * 0.5)
                pygame.draw.circle(screen, trail_color, (int(pos[0]), int(pos[1])), size)
        
        # Desenhar campo de energia ao redor
        energy_radius = 15 + int(math.sin(self.energy_field) * 3)
        energy_color = self.get_psychedelic_color(0.3, 0.3)
        
        # Criar múltiplos anéis de energia
        for i in range(3):
            radius = energy_radius + i * 5
            alpha = 100 - i * 30
            
            energy_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            energy_with_alpha = (energy_color[0], energy_color[1], energy_color[2], alpha)  # RGBA correto
            pygame.draw.circle(energy_surface, energy_with_alpha, 
                             (radius, radius), radius, 1)
            screen.blit(energy_surface, 
                       (self.x - radius, self.y - radius))
        
        # Desenhar corpo principal do inimigo
        if self.enemy_type == 'basic':
            self.draw_basic(screen)
        elif self.enemy_type == 'fast':
            self.draw_fast(screen)
        elif self.enemy_type == 'shooter':
            self.draw_shooter(screen)
        elif self.enemy_type == 'kamikaze':
            self.draw_kamikaze(screen)
        elif self.enemy_type == 'tank':
            self.draw_tank(screen)
        elif self.enemy_type == 'sniper':
            self.draw_sniper(screen)
        elif self.enemy_type == 'splitter':
            self.draw_splitter(screen)
        elif self.enemy_type == 'bomber':
            self.draw_bomber(screen)
        elif self.enemy_type == 'healer':
            self.draw_healer(screen)
        elif self.enemy_type == 'shield':
            self.draw_shield(screen)
        else:
            self.draw_basic(screen)
    
    def draw_basic(self, screen):
        """Desenhar inimigo básico - losango"""
        main_color = self.get_psychedelic_color()
        
        points = [
            (self.x, self.y - self.height // 2),  # Topo
            (self.x + self.width // 2, self.y),  # Direita
            (self.x, self.y + self.height // 2),  # Baixo
            (self.x - self.width // 2, self.y)   # Esquerda
        ]
        
        pygame.draw.polygon(screen, main_color, points)
        
        # Contorno brilhante
        outline_color = self.get_psychedelic_color(0.5)
        pygame.draw.polygon(screen, outline_color, points, 2)
        
        # Centro brilhante
        center_color = self.get_psychedelic_color(0.8)
        pygame.draw.circle(screen, center_color, (int(self.x), int(self.y)), 5)
    
    def draw_fast(self, screen):
        """Desenhar inimigo rápido - triângulo"""
        main_color = self.get_psychedelic_color()
        
        points = [
            (self.x, self.y - self.height // 2),  # Ponta
            (self.x - self.width // 2, self.y + self.height // 2),  # Base esquerda
            (self.x + self.width // 2, self.y + self.height // 2)   # Base direita
        ]
        
        pygame.draw.polygon(screen, main_color, points)
        
        # Adicionar "chamas" de velocidade
        flame_color = self.get_psychedelic_color(0.1)
        flame_points = [
            (self.x - 5, self.y + self.height // 2),
            (self.x, self.y + self.height // 2 + 10),
            (self.x + 5, self.y + self.height // 2)
        ]
        pygame.draw.polygon(screen, flame_color, flame_points)
        
        # Contorno
        outline_color = self.get_psychedelic_color(0.6)
        pygame.draw.polygon(screen, outline_color, points, 2)
    
    def draw_shooter(self, screen):
        """Desenhar inimigo atirador - hexágono"""
        main_color = self.get_psychedelic_color()
        
        # Criar hexágono
        angles = [i * math.pi / 3 for i in range(6)]
        radius = self.width // 2
        points = []
        
        for angle in angles:
            x = self.x + radius * math.cos(angle)
            y = self.y + radius * math.sin(angle)
            points.append((x, y))
        
        pygame.draw.polygon(screen, main_color, points)
        
        # Canhões laterais
        cannon_color = self.get_psychedelic_color(0.3)
        
        # Canhão esquerdo
        pygame.draw.rect(screen, cannon_color, 
                        (self.x - 15, self.y - 3, 8, 6))
        
        # Canhão direito
        pygame.draw.rect(screen, cannon_color, 
                        (self.x + 7, self.y - 3, 8, 6))
        
        # Núcleo central pulsante
        pulse_size = 8 + int(math.sin(self.animation_frame * 0.5) * 3)
        core_color = self.get_psychedelic_color(0.9)
        pygame.draw.circle(screen, core_color, (int(self.x), int(self.y)), pulse_size)
        
        # Contorno
        outline_color = self.get_psychedelic_color(0.7)
        pygame.draw.polygon(screen, outline_color, points, 2)
    
    def draw_kamikaze(self, screen):
        """Desenhar inimigo kamikaze - triângulo pontiagudo com chamas"""
        main_color = self.get_psychedelic_color()
        
        # Triângulo agressivo
        points = [
            (self.x, self.y - self.height // 2 - 5),  # Ponta afiada
            (self.x - self.width // 2, self.y + self.height // 2),
            (self.x + self.width // 2, self.y + self.height // 2)
        ]
        pygame.draw.polygon(screen, main_color, points)
        
        # Chamas intensas se em modo kamikaze
        if self.kamikaze_mode:
            for i in range(3):
                flame_size = 8 - i * 2
                flame_y = self.y + self.height // 2 + i * 5
                flame_color = self.get_psychedelic_color(0.05, 1.0 - i * 0.3)
                pygame.draw.circle(screen, flame_color, (int(self.x), int(flame_y)), flame_size)
        
        # Olho vermelho
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 3)
        
        # Contorno
        pygame.draw.polygon(screen, (255, 255, 255), points, 2)
    
    def draw_tank(self, screen):
        """Desenhar tanque - retângulo robusto com barra de vida"""
        main_color = self.get_psychedelic_color()
        
        # Corpo principal
        body_rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2,
                               self.width, self.height)
        pygame.draw.rect(screen, main_color, body_rect)
        pygame.draw.rect(screen, (255, 255, 255), body_rect, 3)
        
        # Torreta
        turret_size = self.width // 3
        pygame.draw.circle(screen, self.get_psychedelic_color(0.2), 
                         (int(self.x), int(self.y)), turret_size)
        pygame.draw.circle(screen, (200, 200, 200), 
                         (int(self.x), int(self.y)), turret_size, 2)
        
        # Barra de vida
        bar_width = self.width
        bar_height = 4
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.height // 2 - 8
        
        # Fundo
        pygame.draw.rect(screen, (50, 50, 50), 
                        (bar_x, bar_y, bar_width, bar_height))
        
        # Vida atual
        health_ratio = self.health / self.max_health
        health_width = int(bar_width * health_ratio)
        health_color = (0, 255, 0) if health_ratio > 0.5 else (255, 255, 0) if health_ratio > 0.25 else (255, 0, 0)
        pygame.draw.rect(screen, health_color, 
                        (bar_x, bar_y, health_width, bar_height))
    
    def draw_sniper(self, screen):
        """Desenhar sniper - losango com mira"""
        main_color = self.get_psychedelic_color()
        
        # Losango
        points = [
            (self.x, self.y - self.height // 2),
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height // 2),
            (self.x - self.width // 2, self.y)
        ]
        pygame.draw.polygon(screen, main_color, points)
        pygame.draw.polygon(screen, (100, 100, 255), points, 2)
        
        # Mira laser
        if self.sniper_locked:
            laser_color = (255, 0, 0, 100)
            pygame.draw.line(screen, (255, 0, 0), 
                           (int(self.x), int(self.y)), 
                           (int(self.x), int(self.y + 200)), 2)
        
        # Scope
        pygame.draw.circle(screen, (0, 0, 255), (int(self.x), int(self.y)), 6)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 6, 1)
    
    def draw_splitter(self, screen):
        """Desenhar splitter - octógono"""
        main_color = self.get_psychedelic_color()
        
        # Octógono
        angles = [i * math.pi / 4 for i in range(8)]
        radius = self.width // 2
        points = []
        
        for angle in angles:
            x = self.x + radius * math.cos(angle)
            y = self.y + radius * math.sin(angle)
            points.append((x, y))
        
        pygame.draw.polygon(screen, main_color, points)
        
        # Linhas de divisão
        pygame.draw.line(screen, (255, 255, 0), 
                        (self.x - radius, self.y), 
                        (self.x + radius, self.y), 2)
        pygame.draw.line(screen, (255, 255, 0), 
                        (self.x, self.y - radius), 
                        (self.x, self.y + radius), 2)
        
        # Contorno
        pygame.draw.polygon(screen, (255, 255, 0), points, 2)
    
    def draw_bomber(self, screen):
        """Desenhar bomber - trapézio com compartimento de bombas"""
        main_color = self.get_psychedelic_color()
        
        # Corpo trapézio
        points = [
            (self.x - self.width // 3, self.y - self.height // 2),
            (self.x + self.width // 3, self.y - self.height // 2),
            (self.x + self.width // 2, self.y + self.height // 2),
            (self.x - self.width // 2, self.y + self.height // 2)
        ]
        pygame.draw.polygon(screen, main_color, points)
        
        # Compartimento de bombas
        bomb_slots = 3
        for i in range(bomb_slots):
            slot_x = self.x - 10 + i * 10
            slot_y = self.y
            pygame.draw.circle(screen, (255, 100, 0), (int(slot_x), int(slot_y)), 3)
        
        # Contorno
        pygame.draw.polygon(screen, (255, 150, 0), points, 2)
    
    def draw_healer(self, screen):
        """Desenhar healer - cruz médica com aura"""
        main_color = self.get_psychedelic_color()
        
        # Círculo principal
        pygame.draw.circle(screen, main_color, (int(self.x), int(self.y)), 
                         self.width // 2)
        
        # Cruz médica
        cross_size = 8
        pygame.draw.rect(screen, (255, 255, 255), 
                        (self.x - 2, self.y - cross_size, 4, cross_size * 2))
        pygame.draw.rect(screen, (255, 255, 255), 
                        (self.x - cross_size, self.y - 2, cross_size * 2, 4))
        
        # Aura de cura pulsante
        pulse = int(math.sin(self.animation_frame * 0.3) * 10)
        aura_radius = self.width // 2 + 10 + pulse
        pygame.draw.circle(screen, (0, 255, 100), (int(self.x), int(self.y)), 
                         aura_radius, 2)
        
        # Contorno
        pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y)), 
                         self.width // 2, 2)
    
    def draw_shield(self, screen):
        """Desenhar escudo - pentágono com escudo frontal"""
        main_color = self.get_psychedelic_color()
        
        # Pentágono
        angles = [i * 2 * math.pi / 5 - math.pi / 2 for i in range(5)]
        radius = self.width // 2
        points = []
        
        for angle in angles:
            x = self.x + radius * math.cos(angle)
            y = self.y + radius * math.sin(angle)
            points.append((x, y))
        
        pygame.draw.polygon(screen, main_color, points)
        
        # Escudo frontal
        if hasattr(self, 'shield_health') and self.shield_health > 0:
            shield_alpha = int(255 * (self.shield_health / self.max_shield))
            shield_size = self.width // 2 + 8
            
            # Escudo semitransparente
            shield_surface = pygame.Surface((shield_size * 2, shield_size * 2), pygame.SRCALPHA)
            shield_color = (100, 200, 255, shield_alpha)
            pygame.draw.circle(shield_surface, shield_color, 
                             (shield_size, shield_size), shield_size)
            screen.blit(shield_surface, 
                       (self.x - shield_size, self.y - self.height // 2 - shield_size))
        
        # Contorno
        pygame.draw.polygon(screen, (100, 200, 255), points, 2)