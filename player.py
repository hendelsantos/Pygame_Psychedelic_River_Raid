import pygame
import math
import colorsys
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_x = x
        self.original_y = y
        
        # Propriedades do jogador
        self.x = x
        self.y = y
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.shield = 0
        self.shield_max = 0
        
        # Sistema de tiro
        self.bullet_damage = 1
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = 15  # Usado pelos upgrades
        
        # Dimensões da nave
        self.width = 30
        self.height = 40
        
        # Criar sprite da nave
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Animação e efeitos visuais
        self.animation_frame = 0
        self.thrust_particles = []
        
        # Atributos para compatibilidade
        self.skin = None
        
    def apply_skin(self, skin_data):
        """Aplica uma nova skin ao jogador."""
        self.skin = skin_data
        # Skin aplicada com sucesso

    def update(self, keys, screen_width, screen_height, bullets_group=None, audio=None, gamepad=None):
        """Atualizar o jogador"""
        
        # Obter input do gamepad se disponível
        axis_x, axis_y = 0, 0
        shoot_pressed = False
        if gamepad and gamepad.is_connected():
            axis_x = gamepad.get_axis('left_x')
            axis_y = gamepad.get_axis('left_y')
            shoot_pressed = gamepad.get_button('A')

        # Movimento horizontal
        if keys[pygame.K_LEFT] or keys[pygame.K_a] or axis_x < -0.5:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] or axis_x > 0.5:
            self.x += self.speed
        
        # Movimento vertical
        if keys[pygame.K_UP] or keys[pygame.K_w] or axis_y < -0.5:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s] or axis_y > 0.5:
            self.y += self.speed
        
        # Tiro contínuo
        if (keys[pygame.K_SPACE] or shoot_pressed) and bullets_group is not None:
            if self.shoot(bullets_group):
                if audio:
                    audio.play_sound('laser')
        
        # Manter dentro da tela
        self.x = max(self.width // 2, min(screen_width - self.width // 2, self.x))
        self.y = max(self.height // 2, min(screen_height - self.height // 2, self.y))
        
        # Atualizar posição do rect
        self.rect.centerx = self.x
        self.rect.centery = self.y
        
        # Reduzir cooldown de tiro
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # Atualizar animação
        self.animation_frame += 0.2
        
        # Criar partículas de propulsão
        self.create_thrust_particles()
        self.update_thrust_particles()
    
    def create_thrust_particles(self):
        """Criar partículas de propulsão atrás da nave"""
        import random
        
        # Adicionar partículas na parte traseira da nave
        for _ in range(2):
            particle = {
                'x': self.x + random.uniform(-5, 5),
                'y': self.y + self.height // 2 + random.uniform(0, 10),
                'vel_x': random.uniform(-1, 1),
                'vel_y': random.uniform(2, 5),
                'life': random.randint(15, 25),
                'max_life': 25,
                'hue': random.uniform(0.1, 0.3)  # Cores quentes (vermelho/laranja)
            }
            self.thrust_particles.append(particle)
    
    def update_thrust_particles(self):
        """Atualizar partículas de propulsão"""
        for particle in self.thrust_particles[:]:
            particle['x'] += particle['vel_x']
            particle['y'] += particle['vel_y']
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.thrust_particles.remove(particle)
    
    def shoot(self, bullets_group):
        """Atira um projétil"""
        if self.shoot_cooldown == 0:
            bullet = Bullet(self.x, self.y - self.height // 2, damage=self.bullet_damage)
            bullets_group.add(bullet)
            self.shoot_cooldown = self.shoot_cooldown_max
            return True
        return False

    def take_damage(self, amount):
        """Reduz a vida do jogador, usando o escudo primeiro."""
        if self.shield > 0:
            self.shield -= amount
            if self.shield < 0:
                self.health += self.shield  # Dano restante vai para a vida
                self.shield = 0
        else:
            self.health -= amount
        
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        """Cura o jogador."""
        self.health = min(self.max_health, self.health + amount)

    def reset(self):
        """Reseta o estado do jogador para o início de uma nova partida."""
        self.x = self.original_x
        self.y = self.original_y
        self.health = self.max_health
        self.shield = self.shield_max  # Começa com escudo cheio
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.shoot_cooldown = 0

    def get_psychedelic_color(self, base_hue, time_offset=0.0):
        """Gerar cor psicodélica"""
        hue = (base_hue + time_offset) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        return tuple(int(c * 255) for c in rgb)

    def draw(self, screen):
        """Desenha o jogador com efeitos psicodélicos"""
        # Desenhar partículas de propulsão primeiro
        self.draw_thrust_particles(screen)
        
        # Desenhar a nave com efeito psicodélico
        time_factor = self.animation_frame * 0.1
        
        # Corpo principal da nave (triângulo)
        points = [
            (self.x, self.y - self.height // 2),  # Ponta superior
            (self.x - self.width // 2, self.y + self.height // 2),  # Base esquerda
            (self.x + self.width // 2, self.y + self.height // 2)   # Base direita
        ]
        
        # Cor principal psicodélica
        main_color = self.get_psychedelic_color(0.6, time_factor)  # Começando com azul
        pygame.draw.polygon(screen, main_color, points)
        
        # Desenhar detalhes da nave
        # Cockpit
        cockpit_color = self.get_psychedelic_color(0.8, time_factor)
        pygame.draw.circle(screen, cockpit_color, (int(self.x), int(self.y - 5)), 8)
        
        # Asas laterais
        wing_color = self.get_psychedelic_color(0.4, time_factor)
        
        # Asa esquerda
        wing_left = [
            (self.x - self.width // 2, self.y),
            (self.x - self.width // 2 - 10, self.y + 10),
            (self.x - self.width // 2, self.y + 15)
        ]
        pygame.draw.polygon(screen, wing_color, wing_left)
        
        # Asa direita
        wing_right = [
            (self.x + self.width // 2, self.y),
            (self.x + self.width // 2 + 10, self.y + 10),
            (self.x + self.width // 2, self.y + 15)
        ]
        pygame.draw.polygon(screen, wing_color, wing_right)
        
        # Contorno brilhante
        outline_color = self.get_psychedelic_color(0.1, time_factor * 2)
        pygame.draw.polygon(screen, outline_color, points, 2)
        
        # Efeito de energia ao redor da nave
        if int(self.animation_frame) % 20 < 10:  # Piscar
            energy_radius = 25 + int(math.sin(time_factor * 3) * 5)
            energy_color = self.get_psychedelic_color(0.9, time_factor * 3)
            
            # Criar surface temporária para transparência
            energy_surface = pygame.Surface((energy_radius * 2, energy_radius * 2), pygame.SRCALPHA)
            energy_rgba = (*energy_color[:3], 50)  # Adicionar transparência
            pygame.draw.circle(energy_surface, energy_rgba, 
                             (energy_radius, energy_radius), energy_radius, 2)
            screen.blit(energy_surface, 
                       (self.x - energy_radius, self.y - energy_radius))
        
        # Desenhar escudo se ativo
        if self.shield > 0 and self.shield_max > 0:
            shield_alpha = int(50 + (self.shield / self.shield_max) * 100) if self.shield_max > 0 else 50
            shield_color = (main_color[0], main_color[1], main_color[2], shield_alpha)  # RGBA para surface
            
            shield_surface = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
            pygame.draw.ellipse(shield_surface, shield_color, shield_surface.get_rect())
            
            screen.blit(shield_surface, (self.x - (self.width + 20) // 2, self.y - (self.height + 20) // 2))

    def draw_thrust_particles(self, screen):
        """Desenha as partículas de propulsão."""
        for particle in self.thrust_particles:
            life_ratio = particle['life'] / particle['max_life']
            size = max(1, int(life_ratio * 8))  # Tamanho mínimo 1
            
            # Cor muda de quente para fria (garantindo que hue seja válido)
            hue = max(0.0, min(1.0, particle['hue'] - (1 - life_ratio) * 0.2))
            rgb = colorsys.hsv_to_rgb(hue, 1, 1)
            color = tuple(max(0, min(255, int(c * 255))) for c in rgb)  # Clamp RGB values
            
            if size > 0:  # Só desenhar se o tamanho for válido
                pygame.draw.circle(screen, color, (int(particle['x']), int(particle['y'])), size)