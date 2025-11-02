import pygame
import colorsys

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction=-1, color=(255, 255, 0), speed=8, damage=1):
        super().__init__()
        self.x = x
        self.y = y
        self.direction = direction  # -1 para cima, 1 para baixo
        self.speed = speed
        self.color = color
        self.damage = damage  # Adicionando o atributo de dano
        
        # Movimento customizado (para bosses)
        self.vel_x = 0.0  # Float para aceitar valores decimais
        self.vel_y = 0.0  # Float para aceitar valores decimais
        self.angle = 0
        self.use_custom_movement = False
        
        # Criar sprite do projétil
        self.image = pygame.Surface((4, 10), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Efeito visual
        self.trail = []
        self.animation_frame = 0
    
    def update(self):
        """Atualizar projétil"""
        if self.use_custom_movement or self.vel_x != 0 or self.vel_y != 0:
            # Movimento customizado (para ataques de boss)
            self.x += self.vel_x
            self.y += self.vel_y
            self.rect.centerx = self.x
            self.rect.centery = self.y
        else:
            # Movimento padrão
            if self.angle != 0:
                # Movimento angular
                import math
                self.x += math.sin(self.angle) * self.speed * abs(self.direction)
            self.y += self.speed * self.direction
            self.rect.centerx = self.x
            self.rect.centery = self.y
        
        self.animation_frame += 0.3
        
        # Adicionar posição atual ao rastro
        self.trail.append((self.x, self.y))
        if len(self.trail) > 5:
            self.trail.pop(0)
        
        # Remover se saiu da tela
        if self.y < -20 or self.y > 800 or self.x < -20 or self.x > 820:
            self.kill()
    
    def draw(self, screen):
        """Desenhar projétil com efeito de rastro"""
        # Desenhar rastro
        for i, pos in enumerate(self.trail):
            alpha = (i + 1) / len(self.trail)
            size = max(1, int(alpha * 3))
            
            # Cor do rastro com transparência
            trail_color = [int(c * alpha) for c in self.color]
            pygame.draw.circle(screen, trail_color, (int(pos[0]), int(pos[1])), size)
        
        # Desenhar projétil principal
        time_factor = self.animation_frame * 0.2
        hue = (time_factor) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        bullet_color = tuple(int(c * 255) for c in rgb)
        
        pygame.draw.circle(screen, bullet_color, (int(self.x), int(self.y)), 3)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 1)