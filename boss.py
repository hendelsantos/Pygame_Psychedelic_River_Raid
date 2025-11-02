import pygame
import math
import random
import colorsys
from bullet import Bullet

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, boss_type='standard', level=1):
        super().__init__()
        self.x = x
        self.y = y
        self.boss_type = boss_type
        self.level = level
        
        # Dimensões maiores para boss
        self.width = 120
        self.height = 100
        
        # Status
        self.max_health = 1000 + (level * 500)  # Mais vida a cada nível
        self.health = self.max_health
        self.speed = 1.5
        self.phase = 1  # Fase atual do boss (1, 2, 3)
        self.max_phases = 3
        
        # Criar sprite
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Sistema de ataque
        self.shoot_cooldown = 0
        self.shoot_delay = 30  # Frames entre ataques
        self.attack_pattern = 0
        self.pattern_timer = 0
        
        # Movimento
        self.movement_pattern = 'enter'  # enter, circular, zigzag, stationary
        self.movement_timer = 0
        self.initial_y = y
        self.angle = 0
        
        # Animação
        self.animation_frame = 0
        self.pulse = 0
        
        # Partes do boss (para ataques múltiplos)
        self.parts = []
        self.create_boss_parts()
        
        # Invulnerabilidade temporária (para fases)
        self.invulnerable = False
        self.invulnerable_timer = 0
        
    def create_boss_parts(self):
        """Criar partes do boss (turrets, asas, etc)"""
        if self.boss_type == 'standard':
            # Boss padrão com 2 canhões laterais
            self.parts = [
                {'x_offset': -40, 'y_offset': 0, 'active': True, 'health': 200},
                {'x_offset': 40, 'y_offset': 0, 'active': True, 'health': 200}
            ]
        elif self.boss_type == 'fortress':
            # Fortaleza voadora com 4 turrets
            self.parts = [
                {'x_offset': -50, 'y_offset': -30, 'active': True, 'health': 150},
                {'x_offset': 50, 'y_offset': -30, 'active': True, 'health': 150},
                {'x_offset': -50, 'y_offset': 30, 'active': True, 'health': 150},
                {'x_offset': 50, 'y_offset': 30, 'active': True, 'health': 150}
            ]
        elif self.boss_type == 'serpent':
            # Serpente com segmentos
            self.parts = [
                {'x_offset': 0, 'y_offset': i * 30, 'active': True, 'health': 100}
                for i in range(1, 5)
            ]
    
    def update(self, screen_width, screen_height):
        """Atualizar boss"""
        # Atualizar animação
        self.animation_frame += 0.1
        self.pulse += 0.15
        
        # Atualizar movimento
        self.update_movement(screen_width, screen_height)
        
        # Atualizar fase baseado na vida
        self.update_phase()
        
        # Atualizar invulnerabilidade
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
        
        # Atualizar cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # Atualizar posição do rect
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        
        # Padrão de ataque
        self.pattern_timer += 1
        if self.pattern_timer > 180:  # Mudar padrão a cada 3 segundos
            self.attack_pattern = (self.attack_pattern + 1) % 4
            self.pattern_timer = 0
    
    def update_movement(self, screen_width, screen_height):
        """Atualizar padrão de movimento"""
        self.movement_timer += 1
        
        if self.movement_pattern == 'enter':
            # Entrar na tela
            if self.y < 150:
                self.y += self.speed
            else:
                self.movement_pattern = 'circular'
                self.initial_y = self.y
        
        elif self.movement_pattern == 'circular':
            # Movimento circular
            self.angle += 0.02
            radius = 50
            self.x = screen_width // 2 + math.cos(self.angle) * radius
            self.y = self.initial_y + math.sin(self.angle * 2) * 30
        
        elif self.movement_pattern == 'zigzag':
            # Movimento em zigue-zague
            self.x += math.sin(self.movement_timer * 0.05) * 3
            self.y += math.cos(self.movement_timer * 0.03) * 2
        
        elif self.movement_pattern == 'stationary':
            # Parado (fase de ataque intenso)
            pass
        
        # Manter dentro da tela
        self.x = max(self.width // 2, min(screen_width - self.width // 2, self.x))
        self.y = max(self.height // 2, min(screen_height // 3, self.y))
    
    def update_phase(self):
        """Atualizar fase do boss baseado na vida"""
        health_ratio = self.health / self.max_health
        
        new_phase = 1
        if health_ratio < 0.66:
            new_phase = 2
        if health_ratio < 0.33:
            new_phase = 3
        
        if new_phase > self.phase:
            self.enter_new_phase(new_phase)
    
    def enter_new_phase(self, phase):
        """Entrar em nova fase com efeitos"""
        print(f"🐉 BOSS FASE {phase}!")
        self.phase = phase
        
        # Invulnerabilidade temporária
        self.invulnerable = True
        self.invulnerable_timer = 60  # 1 segundo
        
        # Mudar padrão de movimento
        if phase == 2:
            self.movement_pattern = 'zigzag'
            self.shoot_delay = 20  # Atirar mais rápido
        elif phase == 3:
            self.movement_pattern = 'stationary'
            self.shoot_delay = 15  # Atirar ainda mais rápido
    
    def shoot(self, bullets_group):
        """Atirar baseado no padrão atual"""
        if self.shoot_cooldown > 0:
            return []
        
        bullets = []
        
        # Padrão 0: Tiro simples direto
        if self.attack_pattern == 0:
            bullet = Bullet(self.x, self.y + self.height // 2, 
                          direction=1, color=(255, 0, 0), speed=5)
            bullets.append(bullet)
        
        # Padrão 1: Tiro triplo
        elif self.attack_pattern == 1:
            for angle in [-0.3, 0, 0.3]:
                bullet = Bullet(self.x, self.y + self.height // 2,
                              direction=1, color=(255, 100, 0), speed=5)
                bullet.angle = angle
                bullets.append(bullet)
        
        # Padrão 2: Tiro circular (8 direções)
        elif self.attack_pattern == 2:
            for i in range(8):
                angle = (i / 8) * 2 * math.pi
                bullet = Bullet(self.x, self.y,
                              direction=1, color=(255, 0, 255), speed=4)
                bullet.vel_x = math.cos(angle) * 4
                bullet.vel_y = math.sin(angle) * 4
                bullets.append(bullet)
        
        # Padrão 3: Tiro das partes
        elif self.attack_pattern == 3:
            for part in self.parts:
                if part['active']:
                    part_x = self.x + part['x_offset']
                    part_y = self.y + part['y_offset']
                    bullet = Bullet(part_x, part_y,
                                  direction=1, color=(0, 255, 255), speed=6)
                    bullets.append(bullet)
        
        # Adicionar bullets ao grupo
        for bullet in bullets:
            bullets_group.add(bullet)
        
        self.shoot_cooldown = self.shoot_delay
        return bullets
    
    def take_damage(self, amount=10):
        """Receber dano"""
        if self.invulnerable:
            return False
        
        self.health -= amount
        if self.health < 0:
            self.health = 0
        
        return True
    
    def is_dead(self):
        """Verificar se o boss está morto"""
        return self.health <= 0
    
    def get_health_ratio(self):
        """Obter razão de vida atual"""
        return self.health / self.max_health
    
    def draw(self, screen):
        """Desenhar boss com efeitos psicodélicos"""
        # Cor baseada na fase
        phase_hues = {1: 0.0, 2: 0.33, 3: 0.66}  # Vermelho, Verde, Azul
        base_hue = phase_hues.get(self.phase, 0.0)
        
        # Pulso de cor
        hue = (base_hue + self.pulse * 0.1) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        color = tuple(int(c * 255) for c in rgb)
        
        # Efeito de invulnerabilidade
        if self.invulnerable:
            alpha = 128 if int(self.animation_frame * 10) % 2 else 255
        else:
            alpha = 255
        
        # Corpo principal do boss
        self.draw_boss_body(screen, color, alpha)
        
        # Desenhar partes
        for part in self.parts:
            if part['active']:
                self.draw_boss_part(screen, part, color, alpha)
        
        # Barra de vida
        self.draw_health_bar(screen)
    
    def draw_boss_body(self, screen, color, alpha):
        """Desenhar corpo principal do boss"""
        # Forma do boss baseada no tipo
        if self.boss_type == 'standard':
            # Boss padrão - forma de diamante
            points = [
                (self.x, self.y - self.height // 2),
                (self.x + self.width // 2, self.y),
                (self.x, self.y + self.height // 2),
                (self.x - self.width // 2, self.y)
            ]
            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, (255, 255, 255), points, 3)
        
        elif self.boss_type == 'fortress':
            # Fortaleza - retângulo robusto
            rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2,
                             self.width, self.height)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)
        
        elif self.boss_type == 'serpent':
            # Serpente - círculo (cabeça)
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 
                             self.width // 3)
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)),
                             self.width // 3, 3)
        
        # Olho/núcleo central pulsante
        pulse_size = 10 + int(5 * math.sin(self.pulse))
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 
                         pulse_size)
    
    def draw_boss_part(self, screen, part, color, alpha):
        """Desenhar parte do boss (turret, asa, etc)"""
        part_x = int(self.x + part['x_offset'])
        part_y = int(self.y + part['y_offset'])
        
        # Turret/canhão
        size = 15
        pygame.draw.circle(screen, color, (part_x, part_y), size)
        pygame.draw.circle(screen, (200, 200, 200), (part_x, part_y), size, 2)
        
        # Cano do canhão
        pygame.draw.line(screen, color, (part_x, part_y),
                        (part_x, part_y + 20), 4)
    
    def draw_health_bar(self, screen):
        """Desenhar barra de vida do boss"""
        bar_width = 200
        bar_height = 20
        bar_x = screen.get_width() // 2 - bar_width // 2
        bar_y = 20
        
        # Fundo
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, (50, 50, 50), bg_rect)
        
        # Barra de vida
        health_ratio = self.get_health_ratio()
        filled_width = int(bar_width * health_ratio)
        health_rect = pygame.Rect(bar_x, bar_y, filled_width, bar_height)
        
        # Cor baseada na vida
        if health_ratio > 0.6:
            bar_color = (0, 255, 0)
        elif health_ratio > 0.3:
            bar_color = (255, 255, 0)
        else:
            bar_color = (255, 0, 0)
        
        pygame.draw.rect(screen, bar_color, health_rect)
        
        # Marcadores de fase
        for i in range(1, self.max_phases):
            marker_x = bar_x + int(bar_width * (1 - i / self.max_phases))
            pygame.draw.line(screen, (255, 255, 255), 
                           (marker_x, bar_y), (marker_x, bar_y + bar_height), 2)
        
        # Borda
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, 2)
        
        # Texto
        font = pygame.font.Font(None, 24)
        text = font.render(f"BOSS - FASE {self.phase}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(bar_x + bar_width // 2, bar_y - 15))
        screen.blit(text, text_rect)
        
        # Vida numérica
        health_text = font.render(f"{int(self.health)}/{int(self.max_health)}", 
                                 True, (255, 255, 255))
        health_text_rect = health_text.get_rect(center=(bar_x + bar_width // 2, 
                                                        bar_y + bar_height // 2))
        screen.blit(health_text, health_text_rect)
    
    def get_score_value(self):
        """Retornar valor de pontos do boss"""
        base_score = 5000
        return base_score * self.level * self.phase
