import pygame
import random
import math

class LevelGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_level = 1
        self.obstacles = []
        self.powerups = []
        self.terrain_points = []
        
        # Configurações do terreno
        self.left_wall = []
        self.right_wall = []
        self.wall_width = 100  # Largura das paredes laterais
        
        # Geração procedural
        self.noise_offset = 0
        self.terrain_complexity = 1
        
        self.generate_initial_terrain()
    
    def generate_initial_terrain(self):
        """Gerar terreno inicial"""
        # Criar paredes laterais iniciais
        for y in range(0, self.height + 200, 20):
            left_x = self.wall_width + random.randint(-20, 20)
            right_x = self.width - self.wall_width + random.randint(-20, 20)
            
            self.left_wall.append((left_x, y))
            self.right_wall.append((right_x, y))
    
    def update(self, scroll_speed):
        """Atualizar geração de nível"""
        self.noise_offset += scroll_speed
        
        # Mover terreno para baixo
        self.move_terrain(scroll_speed)
        
        # Gerar novo terreno na parte superior
        self.generate_new_terrain()
        
        # Limpar terreno que saiu da tela
        self.cleanup_terrain()
    
    def move_terrain(self, speed):
        """Mover todo o terreno para baixo"""
        # Mover paredes
        for i in range(len(self.left_wall)):
            x, y = self.left_wall[i]
            self.left_wall[i] = (x, y + speed)
        
        for i in range(len(self.right_wall)):
            x, y = self.right_wall[i]
            self.right_wall[i] = (x, y + speed)
        
        # Mover obstáculos
        for obstacle in self.obstacles[:]:
            obstacle['y'] += speed
            if obstacle['y'] > self.height + 50:
                self.obstacles.remove(obstacle)
        
        # Mover power-ups
        for powerup in self.powerups[:]:
            powerup['y'] += speed
            if powerup['y'] > self.height + 50:
                self.powerups.remove(powerup)
    
    def generate_new_terrain(self):
        """Gerar novo terreno na parte superior"""
        # Adicionar novos pontos de parede
        if self.left_wall and self.left_wall[0][1] > -100:
            # Terreno procedural com ruído
            complexity = self.terrain_complexity + (self.current_level - 1) * 0.5
            
            # Parede esquerda
            last_left_x = self.left_wall[0][0] if self.left_wall else self.wall_width
            variation = int(complexity * 30)
            new_left_x = max(50, min(self.width // 3, 
                           last_left_x + random.randint(-variation, variation)))
            self.left_wall.insert(0, (new_left_x, -20))
            
            # Parede direita  
            last_right_x = self.right_wall[0][0] if self.right_wall else self.width - self.wall_width
            new_right_x = max(self.width * 2 // 3, min(self.width - 50,
                            last_right_x + random.randint(-variation, variation)))
            self.right_wall.insert(0, (new_right_x, -20))
        
        # Gerar obstáculos ocasionais
        if random.randint(1, 100) <= 3:  # 3% de chance
            self.generate_obstacle()
        
        # Gerar power-ups raramente
        if random.randint(1, 300) <= 1:  # 0.33% de chance
            self.generate_powerup()
    
    def generate_obstacle(self):
        """Gerar obstáculo no canal"""
        # Encontrar a largura do canal atual
        if self.left_wall and self.right_wall:
            left_x = self.left_wall[0][0]
            right_x = self.right_wall[0][0]
            channel_width = right_x - left_x
            
            if channel_width > 100:  # Canal suficientemente largo
                # Obstáculo no meio do canal
                obstacle_x = left_x + random.randint(20, int(channel_width - 20))
                obstacle_y = -50
                
                obstacle_type = random.choice(['rock', 'crystal', 'energy_field'])
                
                obstacle = {
                    'x': obstacle_x,
                    'y': obstacle_y,
                    'type': obstacle_type,
                    'size': random.randint(15, 30),
                    'rotation': 0,
                    'rotation_speed': random.uniform(-0.1, 0.1),
                    'pulse_phase': random.uniform(0, 2 * math.pi)
                }
                
                self.obstacles.append(obstacle)
    
    def generate_powerup(self):
        """Gerar power-up"""
        if self.left_wall and self.right_wall:
            left_x = self.left_wall[0][0]
            right_x = self.right_wall[0][0]
            channel_width = right_x - left_x
            
            if channel_width > 80:
                powerup_x = left_x + random.randint(20, int(channel_width - 20))
                powerup_y = -30
                
                powerup_type = random.choice(['health', 'speed', 'multishot', 'shield'])
                
                powerup = {
                    'x': powerup_x,
                    'y': powerup_y,
                    'type': powerup_type,
                    'rotation': 0,
                    'pulse_phase': random.uniform(0, 2 * math.pi),
                    'collected': False
                }
                
                self.powerups.append(powerup)
    
    def cleanup_terrain(self):
        """Limpar terreno que saiu da tela"""
        # Remover pontos de parede muito abaixo da tela
        self.left_wall = [(x, y) for x, y in self.left_wall if y < self.height + 100]
        self.right_wall = [(x, y) for x, y in self.right_wall if y < self.height + 100]
    
    def get_collision_rects(self):
        """Obter retângulos de colisão para paredes e obstáculos"""
        collision_rects = []
        
        # Paredes laterais
        for i in range(len(self.left_wall) - 1):
            x1, y1 = self.left_wall[i]
            x2, y2 = self.left_wall[i + 1]
            
            # Criar retângulo para segmento da parede
            wall_rect = pygame.Rect(0, min(y1, y2), x1, abs(y2 - y1) + 10)
            collision_rects.append(wall_rect)
        
        for i in range(len(self.right_wall) - 1):
            x1, y1 = self.right_wall[i]
            x2, y2 = self.right_wall[i + 1]
            
            wall_rect = pygame.Rect(x1, min(y1, y2), self.width - x1, abs(y2 - y1) + 10)
            collision_rects.append(wall_rect)
        
        # Obstáculos
        for obstacle in self.obstacles:
            size = obstacle['size']
            obstacle_rect = pygame.Rect(obstacle['x'] - size//2, obstacle['y'] - size//2, 
                                      size, size)
            collision_rects.append(obstacle_rect)
        
        return collision_rects
    
    def increase_difficulty(self):
        """Aumentar dificuldade do nível"""
        self.current_level += 1
        self.terrain_complexity += 0.3
        self.wall_width = max(80, self.wall_width - 5)  # Estreitar passagem
    
    def draw(self, screen, color_shift):
        """Desenhar o nível"""
        self.draw_terrain(screen, color_shift)
        self.draw_obstacles(screen, color_shift)
        self.draw_powerups(screen, color_shift)
    
    def draw_terrain(self, screen, color_shift):
        """Desenhar terreno das paredes"""
        import colorsys
        
        # Desenhar paredes laterais
        if len(self.left_wall) > 1:
            # Parede esquerda
            wall_color = colorsys.hsv_to_rgb((color_shift + 0.7) % 1.0, 0.8, 0.6)
            wall_color = tuple(int(c * 255) for c in wall_color)
            
            try:
                pygame.draw.polygon(screen, wall_color, 
                                  [(0, 0), (0, self.height)] + 
                                  [(x, y) for x, y in reversed(self.left_wall) if 0 <= y <= self.height])
            except:
                pass
        
        if len(self.right_wall) > 1:
            # Parede direita
            wall_color = colorsys.hsv_to_rgb((color_shift + 0.3) % 1.0, 0.8, 0.6)
            wall_color = tuple(int(c * 255) for c in wall_color)
            
            try:
                pygame.draw.polygon(screen, wall_color,
                                  [(self.width, 0), (self.width, self.height)] +
                                  [(x, y) for x, y in reversed(self.right_wall) if 0 <= y <= self.height])
            except:
                pass
        
        # Desenhar bordas das paredes com brilho
        edge_color = colorsys.hsv_to_rgb((color_shift + 0.1) % 1.0, 1.0, 1.0)
        edge_color = tuple(int(c * 255) for c in edge_color)
        
        if len(self.left_wall) > 1:
            wall_points = [(x, y) for x, y in self.left_wall if 0 <= y <= self.height]
            if len(wall_points) > 1:
                pygame.draw.lines(screen, edge_color, False, wall_points, 3)
        
        if len(self.right_wall) > 1:
            wall_points = [(x, y) for x, y in self.right_wall if 0 <= y <= self.height]
            if len(wall_points) > 1:
                pygame.draw.lines(screen, edge_color, False, wall_points, 3)
    
    def draw_obstacles(self, screen, color_shift):
        """Desenhar obstáculos"""
        import colorsys
        
        for obstacle in self.obstacles:
            obstacle['rotation'] += obstacle['rotation_speed']
            
            # Cor baseada no tipo
            if obstacle['type'] == 'rock':
                hue = (color_shift + 0.1) % 1.0
            elif obstacle['type'] == 'crystal':
                hue = (color_shift + 0.6) % 1.0
            else:  # energy_field
                hue = (color_shift + 0.9) % 1.0
            
            # Pulsar
            pulse = math.sin(pygame.time.get_ticks() * 0.005 + obstacle['pulse_phase'])
            size = obstacle['size'] * (1 + 0.2 * pulse)
            brightness = 0.7 + 0.3 * pulse
            
            rgb = colorsys.hsv_to_rgb(hue, 1.0, brightness)
            color = tuple(int(c * 255) for c in rgb)
            
            # Desenhar baseado no tipo
            if obstacle['type'] == 'rock':
                # Octágono rotacionado
                points = []
                for i in range(8):
                    angle = obstacle['rotation'] + (i / 8) * 2 * math.pi
                    x = obstacle['x'] + size * 0.5 * math.cos(angle)
                    y = obstacle['y'] + size * 0.5 * math.sin(angle)
                    points.append((x, y))
                
                pygame.draw.polygon(screen, color, points)
                
            elif obstacle['type'] == 'crystal':
                # Diamante
                points = [
                    (obstacle['x'], obstacle['y'] - size * 0.6),
                    (obstacle['x'] + size * 0.4, obstacle['y']),
                    (obstacle['x'], obstacle['y'] + size * 0.6),
                    (obstacle['x'] - size * 0.4, obstacle['y'])
                ]
                
                pygame.draw.polygon(screen, color, points)
                pygame.draw.polygon(screen, (255, 255, 255), points, 2)
                
            else:  # energy_field
                # Círculo pulsante com anéis
                pygame.draw.circle(screen, color, 
                                 (int(obstacle['x']), int(obstacle['y'])), 
                                 int(size * 0.5))
                
                for ring in range(3):
                    ring_radius = int(size * 0.3 * (ring + 1))
                    ring_color = [int(c * (1 - ring * 0.3)) for c in color]
                    pygame.draw.circle(screen, ring_color,
                                     (int(obstacle['x']), int(obstacle['y'])),
                                     ring_radius, 2)
    
    def draw_powerups(self, screen, color_shift):
        """Desenhar power-ups"""
        import colorsys
        
        for powerup in self.powerups:
            if not powerup['collected']:
                powerup['rotation'] += 0.05
                
                # Cor baseada no tipo
                type_colors = {
                    'health': 0.0,      # Vermelho
                    'speed': 0.16,      # Amarelo
                    'multishot': 0.66,  # Azul
                    'shield': 0.33      # Verde
                }
                
                hue = (type_colors.get(powerup['type'], 0) + color_shift * 0.3) % 1.0
                pulse = math.sin(pygame.time.get_ticks() * 0.008 + powerup['pulse_phase'])
                brightness = 0.8 + 0.2 * pulse
                
                rgb = colorsys.hsv_to_rgb(hue, 1.0, brightness)
                color = tuple(int(c * 255) for c in rgb)
                
                # Desenhar ícone baseado no tipo
                size = 12 + int(3 * pulse)
                
                if powerup['type'] == 'health':
                    # Cruz de vida
                    pygame.draw.rect(screen, color,
                                   (powerup['x'] - size//4, powerup['y'] - size,
                                    size//2, size*2))
                    pygame.draw.rect(screen, color,
                                   (powerup['x'] - size, powerup['y'] - size//4,
                                    size*2, size//2))
                
                elif powerup['type'] == 'speed':
                    # Seta para frente
                    points = [
                        (powerup['x'], powerup['y'] - size),
                        (powerup['x'] + size, powerup['y'] + size),
                        (powerup['x'] - size, powerup['y'] + size)
                    ]
                    pygame.draw.polygon(screen, color, points)
                
                elif powerup['type'] == 'multishot':
                    # Três linhas paralelas
                    for i in range(3):
                        y_offset = (i - 1) * size // 2
                        pygame.draw.rect(screen, color,
                                       (powerup['x'] - size, powerup['y'] + y_offset - 2,
                                        size * 2, 4))
                
                else:  # shield
                    # Escudo
                    points = [
                        (powerup['x'], powerup['y'] - size),
                        (powerup['x'] + size*0.7, powerup['y'] - size*0.3),
                        (powerup['x'] + size*0.7, powerup['y'] + size*0.3),
                        (powerup['x'], powerup['y'] + size),
                        (powerup['x'] - size*0.7, powerup['y'] + size*0.3),
                        (powerup['x'] - size*0.7, powerup['y'] - size*0.3)
                    ]
                    pygame.draw.polygon(screen, color, points)
                
                # Halo brilhante
                halo_surface = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
                halo_color = (*color, 50)
                pygame.draw.circle(halo_surface, halo_color, 
                                 (size * 2, size * 2), size * 2)
                screen.blit(halo_surface, 
                           (powerup['x'] - size * 2, powerup['y'] - size * 2))