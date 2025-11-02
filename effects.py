import pygame
import math
import random
import colorsys

class PsychedelicEffects:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.time = 0
        
        # Ondas de fundo
        self.wave_patterns = []
        for i in range(5):
            pattern = {
                'amplitude': random.uniform(10, 30),
                'frequency': random.uniform(0.01, 0.05),
                'phase': random.uniform(0, 2 * math.pi),
                'speed': random.uniform(0.02, 0.08),
                'hue_base': random.uniform(0, 1)
            }
            self.wave_patterns.append(pattern)
        
        # Partículas flutuantes
        self.floating_particles = []
        for _ in range(30):
            particle = self.create_floating_particle()
            self.floating_particles.append(particle)
        
        # Fractais em movimento
        self.fractal_points = []
        self.generate_fractal_points()
        
        # Túnel psicodélico
        self.tunnel_rings = []
        for i in range(20):
            ring = {
                'radius': i * 15 + 50,
                'z': i * 20,
                'rotation': random.uniform(0, 2 * math.pi),
                'hue_offset': i * 0.1
            }
            self.tunnel_rings.append(ring)
    
    def create_floating_particle(self):
        """Criar partícula flutuante"""
        return {
            'x': random.uniform(0, self.width),
            'y': random.uniform(0, self.height),
            'vel_x': random.uniform(-0.5, 0.5),
            'vel_y': random.uniform(-0.5, 0.5),
            'size': random.uniform(2, 8),
            'hue': random.uniform(0, 1),
            'pulse_speed': random.uniform(0.05, 0.15),
            'pulse_phase': random.uniform(0, 2 * math.pi)
        }
    
    def generate_fractal_points(self):
        """Gerar pontos fractais"""
        self.fractal_points.clear()
        center_x, center_y = self.width // 2, self.height // 2
        
        # Mandelbrot simplificado
        for i in range(100):
            angle = (i / 100) * 2 * math.pi * 3  # Múltiplas voltas
            radius = (i / 100) * 150
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            if 0 <= x < self.width and 0 <= y < self.height:
                self.fractal_points.append({
                    'x': x,
                    'y': y,
                    'index': i,
                    'base_radius': radius
                })
    
    def update(self):
        """Atualizar efeitos"""
        self.time += 1
        
        # Atualizar partículas flutuantes
        for particle in self.floating_particles:
            particle['x'] += particle['vel_x']
            particle['y'] += particle['vel_y']
            
            # Wraparound nas bordas
            if particle['x'] < 0:
                particle['x'] = self.width
            elif particle['x'] > self.width:
                particle['x'] = 0
            
            if particle['y'] < 0:
                particle['y'] = self.height
            elif particle['y'] > self.height:
                particle['y'] = 0
        
        # Atualizar anéis do túnel
        for ring in self.tunnel_rings:
            ring['z'] -= 2
            ring['rotation'] += 0.02
            
            if ring['z'] < -100:
                ring['z'] = 400
                ring['radius'] = random.uniform(30, 80)
    
    def draw_background(self, screen, color_shift):
        """Desenhar fundo psicodélico"""
        # Gradiente de fundo animado
        for y in range(0, self.height, 4):
            progress = y / self.height
            hue = (color_shift + progress * 0.5) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.3)
            color = tuple(int(c * 255) for c in rgb)
            
            pygame.draw.rect(screen, color, (0, y, self.width, 4))
        
        # Ondas de fundo
        for pattern in self.wave_patterns:
            self.draw_wave_pattern(screen, pattern, color_shift)
    
    def draw_wave_pattern(self, screen, pattern, color_shift):
        """Desenhar padrão de ondas"""
        points = []
        
        for x in range(0, self.width, 8):
            wave_y = (self.height // 2 + 
                     pattern['amplitude'] * math.sin(
                         x * pattern['frequency'] + 
                         self.time * pattern['speed'] + 
                         pattern['phase']
                     ))
            points.append((x, wave_y))
        
        if len(points) > 1:
            hue = (pattern['hue_base'] + color_shift * 0.5) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 0.6)
            color = tuple(int(c * 255) for c in rgb)
            
            # Desenhar linha espessa com transparência
            try:
                pygame.draw.lines(screen, color, False, points, 3)
            except:
                pass  # Evitar erro se pontos inválidos
    
    def draw_effects(self, screen, color_shift):
        """Desenhar efeitos visuais principais"""
        # Túnel psicodélico
        self.draw_tunnel(screen, color_shift)
        
        # Partículas flutuantes
        self.draw_floating_particles(screen, color_shift)
        
        # Fractais
        self.draw_fractals(screen, color_shift)
        
        # Raios de energia
        self.draw_energy_rays(screen, color_shift)
    
    def draw_tunnel(self, screen, color_shift):
        """Desenhar túnel psicodélico"""
        center_x, center_y = self.width // 2, self.height // 2
        
        for ring in self.tunnel_rings:
            if ring['z'] > 0:
                # Perspectiva
                scale = 200 / (ring['z'] + 200)
                radius = ring['radius'] * scale
                
                if radius > 2:
                    # Cor baseada na profundidade
                    depth_factor = ring['z'] / 400
                    hue = (color_shift + ring['hue_offset'] + depth_factor) % 1.0
                    rgb = colorsys.hsv_to_rgb(hue, 1.0, 0.8 * (1 - depth_factor))
                    color = tuple(int(c * 255) for c in rgb)
                    
                    # Desenhar anel rotacionado
                    points = []
                    for i in range(12):
                        angle = ring['rotation'] + (i / 12) * 2 * math.pi
                        x = center_x + radius * math.cos(angle)
                        y = center_y + radius * math.sin(angle)
                        points.append((x, y))
                    
                    if len(points) > 2:
                        try:
                            pygame.draw.polygon(screen, color, points, 2)
                        except:
                            pass
    
    def draw_floating_particles(self, screen, color_shift):
        """Desenhar partículas flutuantes"""
        for particle in self.floating_particles:
            # Pulsar baseado no tempo
            pulse = math.sin(self.time * particle['pulse_speed'] + particle['pulse_phase'])
            size = particle['size'] * (0.8 + 0.4 * pulse)
            
            # Cor psicodélica
            hue = (particle['hue'] + color_shift * 0.3) % 1.0
            brightness = 0.7 + 0.3 * pulse
            rgb = colorsys.hsv_to_rgb(hue, 1.0, brightness)
            color = tuple(int(c * 255) for c in rgb)
            
            # Desenhar partícula com halo
            pygame.draw.circle(screen, color, 
                             (int(particle['x']), int(particle['y'])), 
                             int(size))
            
            # Halo externo
            halo_color = (*color[:3], 50)
            halo_surface = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
            pygame.draw.circle(halo_surface, halo_color, 
                             (size * 2, size * 2), int(size * 2))
            screen.blit(halo_surface, 
                       (particle['x'] - size * 2, particle['y'] - size * 2))
    
    def draw_fractals(self, screen, color_shift):
        """Desenhar padrões fractais"""
        for point in self.fractal_points:
            # Rotação baseada no tempo
            angle = self.time * 0.01 + point['index'] * 0.1
            
            # Movimento em espiral
            radius_mod = point['base_radius'] * (1 + 0.3 * math.sin(self.time * 0.02 + point['index']))
            
            center_x, center_y = self.width // 2, self.height // 2
            x = center_x + radius_mod * math.cos(angle)
            y = center_y + radius_mod * math.sin(angle)
            
            # Cor baseada no índice e tempo
            hue = (point['index'] / 100 + color_shift) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 0.8)
            color = tuple(int(c * 255) for c in rgb)
            
            if 0 <= x < self.width and 0 <= y < self.height:
                size = max(1, int(3 + 2 * math.sin(self.time * 0.05 + point['index'])))
                pygame.draw.circle(screen, color, (int(x), int(y)), size)
    
    def draw_energy_rays(self, screen, color_shift):
        """Desenhar raios de energia"""
        center_x, center_y = self.width // 2, self.height // 2
        
        # Raios rotativos
        for i in range(8):
            angle = (self.time * 0.02) + (i / 8) * 2 * math.pi
            
            # Comprimento variável
            length = 100 + 50 * math.sin(self.time * 0.03 + i)
            
            end_x = center_x + length * math.cos(angle)
            end_y = center_y + length * math.sin(angle)
            
            # Cor do raio
            hue = (color_shift + i * 0.125) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 0.6)
            color = tuple(int(c * 255) for c in rgb)
            
            # Desenhar raio com múltiplas linhas para espessura
            for thickness in range(3):
                offset = thickness - 1
                start_pos = (center_x + offset, center_y + offset)
                end_pos = (end_x + offset, end_y + offset)
                
                try:
                    pygame.draw.line(screen, color, start_pos, end_pos, 2)
                except:
                    pass
    
    def create_giant_explosion(self, x, y, size_multiplier=1.0):
        """Criar explosão GIGANTE e espetacular com muitas partículas psicodélicas"""
        particles = []
        num_particles = int(200 * size_multiplier)  # Muitas partículas!
        
        # Partículas principais (explosão radial)
        for i in range(num_particles):
            angle = (i / num_particles) * 2 * math.pi
            speed = random.uniform(3, 12) * size_multiplier
            
            particle = {
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.uniform(0.8, 1.5),
                'max_life': random.uniform(0.8, 1.5),
                'size': random.uniform(4, 12) * size_multiplier,
                'color': colorsys.hsv_to_rgb(random.uniform(0, 1), 1.0, 1.0),
                'gravity': random.uniform(0.05, 0.2),
                'trail': []
            }
            particles.append(particle)
        
        # Partículas secundárias (mais lentas, maiores)
        for i in range(int(50 * size_multiplier)):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4) * size_multiplier
            
            particle = {
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.uniform(1.0, 2.0),
                'max_life': random.uniform(1.0, 2.0),
                'size': random.uniform(8, 20) * size_multiplier,
                'color': colorsys.hsv_to_rgb(random.uniform(0, 1), 0.8, 1.0),
                'gravity': 0.05,
                'trail': []
            }
            particles.append(particle)
        
        # Anéis de energia
        for i in range(int(5 * size_multiplier)):
            particle = {
                'x': x,
                'y': y,
                'radius': 10 + i * 20,
                'expand_speed': random.uniform(8, 15) * size_multiplier,
                'life': 0.5,
                'max_life': 0.5,
                'color': colorsys.hsv_to_rgb(i * 0.2, 1.0, 1.0),
                'type': 'ring'
            }
            particles.append(particle)
        
        return particles
    
    def update_explosion_particles(self, particles, dt=1.0/60.0):
        """Atualizar partículas de explosão"""
        particles_to_remove = []
        
        for particle in particles:
            # Partículas normais
            if 'type' not in particle:
                # Atualizar posição
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['vy'] += particle['gravity']
                
                # Adicionar à trilha
                if 'trail' in particle and len(particle['trail']) < 10:
                    particle['trail'].append((particle['x'], particle['y']))
                    if len(particle['trail']) > 10:
                        particle['trail'].pop(0)
                
                # Reduzir vida
                particle['life'] -= dt
                
            # Anéis de energia
            elif particle['type'] == 'ring':
                particle['radius'] += particle['expand_speed']
                particle['life'] -= dt
            
            # Remover partículas mortas
            if particle['life'] <= 0:
                particles_to_remove.append(particle)
        
        for particle in particles_to_remove:
            particles.remove(particle)
        
        return len(particles) > 0  # Retorna True se ainda há partículas
    
    def draw_explosion_particles(self, screen, particles):
        """Desenhar partículas de explosão"""
        for particle in particles:
            if 'type' not in particle:
                # Partículas normais
                alpha_factor = particle['life'] / particle['max_life']
                size = int(particle['size'] * alpha_factor)
                
                if size > 0:
                    # Cor com alpha
                    color = tuple(int(c * 255) for c in particle['color'])
                    
                    # Desenhar trilha
                    if 'trail' in particle and len(particle['trail']) > 1:
                        for i in range(len(particle['trail']) - 1):
                            trail_alpha = (i / len(particle['trail'])) * alpha_factor
                            if trail_alpha > 0:
                                start = particle['trail'][i]
                                end = particle['trail'][i + 1]
                                try:
                                    pygame.draw.line(screen, color, start, end, 1)
                                except:
                                    pass
                    
                    # Desenhar partícula
                    try:
                        pygame.draw.circle(screen, color, (int(particle['x']), int(particle['y'])), size)
                        # Brilho interno
                        if size > 2:
                            pygame.draw.circle(screen, (255, 255, 255), 
                                             (int(particle['x']), int(particle['y'])), size // 2)
                    except:
                        pass
            
            elif particle['type'] == 'ring':
                # Anéis de energia
                alpha_factor = particle['life'] / particle['max_life']
                color = tuple(int(c * 255 * alpha_factor) for c in particle['color'])
                
                try:
                    pygame.draw.circle(screen, color, 
                                     (int(particle['x']), int(particle['y'])), 
                                     int(particle['radius']), 3)
                except:
                    pass