import pygame
import math

class CollisionManager:
    def __init__(self):
        self.collision_history = []  # Para debug
    
    def check_circle_collision(self, pos1, radius1, pos2, radius2):
        """Verificar colisão entre dois círculos"""
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        distance = math.sqrt(dx*dx + dy*dy)
        return distance < (radius1 + radius2)
    
    def check_rect_collision(self, rect1, rect2):
        """Verificar colisão entre dois retângulos"""
        return rect1.colliderect(rect2)
    
    def check_point_in_rect(self, point, rect):
        """Verificar se um ponto está dentro de um retângulo"""
        return rect.collidepoint(point)
    
    def check_line_collision(self, start1, end1, start2, end2):
        """Verificar colisão entre duas linhas"""
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
        
        def intersect(A, B, C, D):
            return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
        
        return intersect(start1, end1, start2, end2)
    
    def get_collision_normal(self, pos1, pos2):
        """Obter vetor normal da colisão"""
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        length = math.sqrt(dx*dx + dy*dy)
        
        if length > 0:
            return (dx / length, dy / length)
        return (0, 0)
    
    def check_player_enemy_collision(self, player, enemies):
        """Verificar colisão entre jogador e inimigos"""
        collisions = []
        player_pos = (player.x, player.y)
        player_radius = player.width // 2
        
        for enemy in enemies:
            enemy_pos = (enemy.x, enemy.y)
            enemy_radius = enemy.width // 2
            
            if self.check_circle_collision(player_pos, player_radius, 
                                         enemy_pos, enemy_radius):
                collisions.append(enemy)
        
        return collisions
    
    def check_bullet_enemy_collision(self, bullets, enemies):
        """Verificar colisão entre projéteis e inimigos"""
        collisions = []
        
        for bullet in bullets:
            bullet_pos = (bullet.x, bullet.y)
            bullet_radius = 3
            
            for enemy in enemies:
                enemy_pos = (enemy.x, enemy.y)
                enemy_radius = enemy.width // 2
                
                if self.check_circle_collision(bullet_pos, bullet_radius,
                                             enemy_pos, enemy_radius):
                    collisions.append((bullet, enemy))
        
        return collisions
    
    def check_player_bullet_collision(self, player, bullets):
        """Verificar colisão entre jogador e projéteis inimigos"""
        collisions = []
        player_pos = (player.x, player.y)
        player_radius = player.width // 2
        
        for bullet in bullets:
            bullet_pos = (bullet.x, bullet.y)
            bullet_radius = 3
            
            if self.check_circle_collision(player_pos, player_radius,
                                         bullet_pos, bullet_radius):
                collisions.append(bullet)
        
        return collisions
    
    def check_terrain_collision(self, entity, level_generator):
        """Verificar colisão com o terreno"""
        entity_rect = pygame.Rect(entity.x - entity.width//2, 
                                entity.y - entity.height//2,
                                entity.width, entity.height)
        
        collision_rects = level_generator.get_collision_rects()
        
        for rect in collision_rects:
            if self.check_rect_collision(entity_rect, rect):
                return True
        
        return False
    
    def check_powerup_collision(self, player, powerups):
        """Verificar colisão entre jogador e power-ups"""
        collisions = []
        player_pos = (player.x, player.y)
        player_radius = player.width // 2
        
        for powerup in powerups:
            if not powerup.get('collected', False):
                powerup_pos = (powerup['x'], powerup['y'])
                powerup_radius = 15
                
                if self.check_circle_collision(player_pos, player_radius,
                                             powerup_pos, powerup_radius):
                    collisions.append(powerup)
        
        return collisions
    
    def resolve_collision(self, entity1, entity2, collision_type='bounce'):
        """Resolver colisão entre duas entidades"""
        if collision_type == 'bounce':
            # Calcular vetor de colisão
            dx = entity2.x - entity1.x
            dy = entity2.y - entity1.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                # Normalizar vetor
                dx /= distance
                dy /= distance
                
                # Separar entidades
                overlap = (entity1.width + entity2.width) // 2 - distance
                if overlap > 0:
                    entity1.x -= dx * overlap * 0.5
                    entity1.y -= dy * overlap * 0.5
                    entity2.x += dx * overlap * 0.5
                    entity2.y += dy * overlap * 0.5
        
        elif collision_type == 'stop':
            # Parar movimento na direção da colisão
            pass  # Implementar se necessário
    
    def get_collision_effects(self, collision_type, position):
        """Obter efeitos visuais para diferentes tipos de colisão"""
        effects = {
            'player_enemy': {
                'particles': 10,
                'colors': [(255, 0, 0), (255, 100, 0), (255, 200, 0)],
                'size_range': (2, 6),
                'speed_range': (3, 8)
            },
            'bullet_enemy': {
                'particles': 8,
                'colors': [(0, 255, 255), (0, 200, 255), (100, 255, 255)],
                'size_range': (1, 4),
                'speed_range': (2, 6)
            },
            'player_powerup': {
                'particles': 15,
                'colors': [(255, 255, 0), (255, 255, 100), (255, 255, 200)],
                'size_range': (2, 5),
                'speed_range': (1, 4)
            }
        }
        
        return effects.get(collision_type, {
            'particles': 5,
            'colors': [(255, 255, 255)],
            'size_range': (1, 3),
            'speed_range': (2, 5)
        })
    
    def create_collision_particles(self, position, effect_data):
        """Criar partículas de efeito de colisão"""
        import random
        
        particles = []
        
        for _ in range(effect_data.get('particles', 5)):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(*effect_data.get('speed_range', (2, 5)))
            size = random.uniform(*effect_data.get('size_range', (1, 3)))
            color = random.choice(effect_data.get('colors', [(255, 255, 255)]))
            
            particle = {
                'x': position[0],
                'y': position[1],
                'vel_x': math.cos(angle) * speed,
                'vel_y': math.sin(angle) * speed,
                'size': size,
                'color': color,
                'life': random.randint(20, 40),
                'max_life': 40
            }
            
            particles.append(particle)
        
        return particles
    
    def update_collision_particles(self, particles):
        """Atualizar partículas de colisão"""
        for particle in particles[:]:
            particle['x'] += particle['vel_x']
            particle['y'] += particle['vel_y']
            particle['life'] -= 1
            
            # Reduzir velocidade por atrito
            particle['vel_x'] *= 0.98
            particle['vel_y'] *= 0.98
            
            if particle['life'] <= 0:
                particles.remove(particle)
    
    def draw_collision_particles(self, screen, particles):
        """Desenhar partículas de colisão"""
        for particle in particles:
            alpha = particle['life'] / particle['max_life']
            size = max(1, int(particle['size'] * alpha))
            
            # Aplicar transparência à cor
            color = [int(c * alpha) for c in particle['color']]
            
            pygame.draw.circle(screen, color,
                             (int(particle['x']), int(particle['y'])), size)
    
    def debug_draw_collision_boxes(self, screen, entities):
        """Desenhar caixas de colisão para debug"""
        for entity in entities:
            if hasattr(entity, 'rect'):
                pygame.draw.rect(screen, (255, 0, 0), entity.rect, 1)
            elif hasattr(entity, 'x') and hasattr(entity, 'width'):
                rect = pygame.Rect(entity.x - entity.width//2,
                                 entity.y - entity.height//2,
                                 entity.width, entity.height)
                pygame.draw.rect(screen, (255, 0, 0), rect, 1)