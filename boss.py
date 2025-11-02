import pygame
import math
import random
import colorsys
from bullet import Bullet
from boss_types import BossType, BossConfig, BossAttackPattern, BossMovementPattern

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, boss_type=BossType.STANDARD, level=1):
        super().__init__()
        self.x = x
        self.y = y
        self.level = level
        
        # Garantir que boss_type seja BossType enum
        if isinstance(boss_type, str):
            # Compatibilidade com código antigo
            try:
                self.boss_type = BossType(boss_type)
            except ValueError:
                self.boss_type = BossType.STANDARD
        else:
            self.boss_type = boss_type
        
        # Carregar configuração do boss
        self.config = BossConfig.get_config(self.boss_type, level)
        
        # Dimensões do boss (da config)
        self.width, self.height = self.config['size']
        
        # Status (da config)
        self.max_health = self.config['max_health']
        self.health = self.max_health
        self.speed = self.config['speed']
        self.phase = 1
        self.max_phases = self.config['phases']
        
        # Criar sprite
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Sistema de ataque (da config)
        self.shoot_cooldown = 0
        self.shoot_delay = self.config['shoot_delay']
        self.attack_pattern = 0
        self.attack_patterns = self.config['attack_patterns']
        self.pattern_timer = 0
        
        # Movimento (da config)
        self.movement_pattern = 'enter'
        self.movement_patterns = self.config['movement_patterns']
        self.movement_timer = 0
        self.initial_y = y
        self.angle = 0
        
        # Animação
        self.animation_frame = 0
        self.pulse = 0
        
        # Habilidades especiais
        self.special_ability = self.config.get('special_ability')
        self.special_timer = 0
        self.special_data = {}  # Dados específicos da habilidade
        
        # Partes do boss (para ataques múltiplos)
        self.parts = []
        self.create_boss_parts()
        
        # Invulnerabilidade temporária (para fases)
        self.invulnerable = False
        self.invulnerable_timer = 0
        
    def create_boss_parts(self):
        """Criar partes do boss (turrets, asas, etc) - compatibilidade com código antigo"""
        # Apenas para compatibilidade - a maioria dos bosses novos não usa parts
        if self.boss_type == BossType.STANDARD:
            self.parts = [
                {'x_offset': -40, 'y_offset': 0, 'active': True, 'health': 200},
                {'x_offset': 40, 'y_offset': 0, 'active': True, 'health': 200}
            ]
        elif self.boss_type == BossType.KRAKEN:
            # Kraken usa tentáculos via special_ability, não parts
            self.parts = []
        else:
            self.parts = []
    
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
        
        # Padrão de ataque - alternar entre os padrões disponíveis
        self.pattern_timer += 1
        if self.pattern_timer > 180:  # Mudar padrão a cada 3 segundos
            self.attack_pattern = (self.attack_pattern + 1) % len(self.attack_patterns)
            self.pattern_timer = 0
    
    def update_movement(self, screen_width, screen_height):
        """Atualizar padrão de movimento"""
        self.movement_timer += 1
        
        if self.movement_pattern == 'enter':
            # Entrar na tela
            if self.y < 150:
                self.y += self.speed
            else:
                # Escolher próximo padrão de movimento dos disponíveis
                if self.movement_patterns:
                    self.movement_pattern = self.movement_patterns[0]
                else:
                    self.movement_pattern = 'circular'
                self.initial_y = self.y
                self.initial_x = self.x
        else:
            # Usar BossMovementPattern para atualizar posição
            # Simular dt em frames (60 FPS = 1/60 por frame)
            BossMovementPattern.update_position(self, self.movement_pattern, 1/60)
        
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
        
        # Usar padrão de ataque da configuração
        if self.attack_pattern < len(self.attack_patterns):
            pattern_name = self.attack_patterns[self.attack_pattern]
            bullets = BossAttackPattern.create_attack(
                pattern_name,
                self.x,
                self.y,
                self.width,
                self.height,
                self.config['color_primary']
            )
        else:
            bullets = []
        
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
        if self.max_health == 0:
            return 0
        return self.health / self.max_health
    
    def draw(self, screen):
        """Desenhar boss com efeitos psicodélicos"""
        # Usar cores da configuração
        primary_color = self.config['color_primary']
        secondary_color = self.config['color_secondary']
        
        # Pulso de cor baseado na animação
        pulse_factor = 0.5 + 0.5 * math.sin(self.pulse)
        
        # Misturar cores primary e secondary baseado no pulso
        color = tuple(
            int(primary_color[i] * pulse_factor + secondary_color[i] * (1 - pulse_factor))
            for i in range(3)
        )
        
        # Efeito de invulnerabilidade
        if self.invulnerable:
            alpha = 128 if int(self.animation_frame * 10) % 2 else 255
        else:
            alpha = 255
        
        # Corpo principal do boss
        self.draw_boss_body(screen, color, alpha)
        
        # Desenhar partes (se houver)
        for part in self.parts:
            if part['active']:
                self.draw_boss_part(screen, part, color, alpha)
        
        # Ícone do tipo de boss
        self.draw_boss_icon(screen)
        
        # Barra de vida
        self.draw_health_bar(screen)
    
    def draw_boss_body(self, screen, color, alpha):
        """Desenhar corpo principal do boss"""
        # Desenhar forma genérica baseada no tamanho do boss
        # Forma de diamante para todos (simples e efetivo)
        points = [
            (int(self.x), int(self.y - self.height // 2)),
            (int(self.x + self.width // 2), int(self.y)),
            (int(self.x), int(self.y + self.height // 2)),
            (int(self.x - self.width // 2), int(self.y))
        ]
        
        # Desenhar corpo principal
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, (255, 255, 255), points, 3)
        
        # Círculo central (núcleo/core)
        core_size = min(self.width, self.height) // 4
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), core_size)
        
        # Olho/núcleo pulsante
        pulse_size = int(core_size * 0.6 + core_size * 0.4 * math.sin(self.pulse))
        pulse_color = tuple(int(c * 1.5) % 256 for c in color)  # Cor mais brilhante
        pygame.draw.circle(screen, pulse_color, (int(self.x), int(self.y)), pulse_size)
    
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
    
    def draw_boss_icon(self, screen):
        """Desenhar ícone do tipo de boss"""
        icon = self.config.get('icon', '👾')
        font = pygame.font.Font(None, 48)
        try:
            text = font.render(icon, True, (255, 255, 255))
            text_rect = text.get_rect(center=(int(self.x), int(self.y) - self.height // 2 - 30))
            screen.blit(text, text_rect)
        except:
            # Se não conseguir renderizar emoji, mostrar nome
            name = self.config.get('name', 'BOSS')
            text = font.render(name, True, (255, 255, 255))
            text_rect = text.get_rect(center=(int(self.x), int(self.y) - self.height // 2 - 30))
            screen.blit(text, text_rect)
    
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
        
        # Texto com nome do boss
        font = pygame.font.Font(None, 24)
        boss_name = self.config.get('name', 'BOSS')
        text = font.render(f"{boss_name} - FASE {self.phase}", True, (255, 255, 255))
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
