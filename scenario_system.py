"""
Sistema de Cenários/Temas Visuais
Alterna automaticamente entre diferentes ambientes visuais
"""

import pygame
import colorsys
import random
from enum import Enum

class ScenarioType(Enum):
    """Tipos de cenários disponíveis"""
    SPACE = "space"           # Espaço sideral (padrão)
    DESERT = "desert"         # Deserto alienígena
    OCEAN = "ocean"           # Profundezas oceânicas
    FIRE = "fire"             # Mundo de fogo/lava
    ICE = "ice"               # Planeta congelado
    FOREST = "forest"         # Floresta psicodélica
    CYBER = "cyber"           # Cidade cyberpunk
    VOID = "void"             # Vazio dimensional

class ScenarioConfig:
    """Configurações visuais de cada cenário"""
    
    @staticmethod
    def get_config(scenario_type: ScenarioType):
        """Retorna configuração visual completa do cenário"""
        
        configs = {
            ScenarioType.SPACE: {
                'name': 'Deep Space',
                'icon': '🌌',
                'bg_color_base': (10, 10, 30),
                'tunnel_colors': [(50, 50, 100), (30, 30, 80), (70, 70, 120)],
                'particle_colors': [(255, 255, 255), (200, 200, 255), (150, 150, 255)],
                'star_density': 1.0,
                'ambient_light': 0.3,
                'description': 'Viajando pelo espaço profundo'
            },
            
            ScenarioType.DESERT: {
                'name': 'Alien Desert',
                'icon': '🏜️',
                'bg_color_base': (139, 90, 43),
                'tunnel_colors': [(194, 133, 80), (160, 82, 45), (210, 150, 90)],
                'particle_colors': [(255, 200, 100), (255, 150, 50), (255, 220, 150)],
                'star_density': 0.3,
                'ambient_light': 0.7,
                'sandstorm': True,
                'description': 'Atravessando dunas alienígenas'
            },
            
            ScenarioType.OCEAN: {
                'name': 'Deep Ocean',
                'icon': '🌊',
                'bg_color_base': (0, 50, 100),
                'tunnel_colors': [(0, 100, 150), (0, 80, 130), (0, 120, 170)],
                'particle_colors': [(0, 255, 255), (100, 200, 255), (50, 150, 255)],
                'star_density': 0.0,
                'ambient_light': 0.4,
                'bubbles': True,
                'waves': True,
                'description': 'Navegando nas profundezas'
            },
            
            ScenarioType.FIRE: {
                'name': 'Inferno World',
                'icon': '🔥',
                'bg_color_base': (80, 20, 0),
                'tunnel_colors': [(255, 100, 0), (255, 50, 0), (255, 150, 0)],
                'particle_colors': [(255, 200, 0), (255, 150, 0), (255, 100, 0)],
                'star_density': 0.0,
                'ambient_light': 0.8,
                'flames': True,
                'heat_distortion': True,
                'description': 'Atravessando rios de lava'
            },
            
            ScenarioType.ICE: {
                'name': 'Frozen Planet',
                'icon': '❄️',
                'bg_color_base': (200, 220, 255),
                'tunnel_colors': [(220, 230, 255), (180, 200, 255), (240, 245, 255)],
                'particle_colors': [(255, 255, 255), (200, 220, 255), (180, 200, 255)],
                'star_density': 0.5,
                'ambient_light': 0.9,
                'snowfall': True,
                'ice_crystals': True,
                'description': 'Deslizando por cristais de gelo'
            },
            
            ScenarioType.FOREST: {
                'name': 'Mystic Forest',
                'icon': '🌳',
                'bg_color_base': (20, 50, 20),
                'tunnel_colors': [(50, 150, 50), (30, 100, 30), (70, 180, 70)],
                'particle_colors': [(100, 255, 100), (150, 255, 150), (50, 255, 50)],
                'star_density': 0.2,
                'ambient_light': 0.5,
                'fireflies': True,
                'vines': True,
                'description': 'Voando por uma floresta alienígena'
            },
            
            ScenarioType.CYBER: {
                'name': 'Neon City',
                'icon': '🌃',
                'bg_color_base': (20, 0, 40),
                'tunnel_colors': [(255, 0, 255), (0, 255, 255), (255, 0, 128)],
                'particle_colors': [(255, 0, 255), (0, 255, 255), (255, 100, 255)],
                'star_density': 0.0,
                'ambient_light': 0.6,
                'neon_signs': True,
                'digital_rain': True,
                'grid_lines': True,
                'description': 'Atravessando uma metrópole cyberpunk'
            },
            
            ScenarioType.VOID: {
                'name': 'Dimensional Void',
                'icon': '🕳️',
                'bg_color_base': (5, 0, 10),
                'tunnel_colors': [(100, 0, 150), (80, 0, 120), (120, 0, 180)],
                'particle_colors': [(200, 0, 255), (150, 0, 200), (255, 0, 255)],
                'star_density': 0.8,
                'ambient_light': 0.2,
                'void_rifts': True,
                'reality_distortion': True,
                'description': 'Navegando entre dimensões'
            }
        }
        
        return configs.get(scenario_type, configs[ScenarioType.SPACE])
    
    @staticmethod
    def get_scenario_for_level(level: int):
        """Retorna cenário baseado no nível"""
        # Progressão de cenários
        scenarios = [
            ScenarioType.SPACE,     # 1-5
            ScenarioType.DESERT,    # 6-10
            ScenarioType.OCEAN,     # 11-15
            ScenarioType.FIRE,      # 16-20
            ScenarioType.ICE,       # 21-25
            ScenarioType.FOREST,    # 26-30
            ScenarioType.CYBER,     # 31-35
            ScenarioType.VOID       # 36+
        ]
        
        index = min((level - 1) // 5, len(scenarios) - 1)
        return scenarios[index]
    
    @staticmethod
    def get_random_scenario():
        """Retorna cenário aleatório"""
        return random.choice(list(ScenarioType))

class ScenarioRenderer:
    """Renderizador de efeitos específicos de cada cenário"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_scenario = ScenarioType.SPACE
        self.config = ScenarioConfig.get_config(self.current_scenario)
        
        # Partículas ambientais
        self.ambient_particles = []
        self.animation_time = 0
        
        # Efeitos especiais
        self.special_effects = []
        
    def set_scenario(self, scenario_type: ScenarioType):
        """Muda o cenário atual"""
        self.current_scenario = scenario_type
        self.config = ScenarioConfig.get_config(scenario_type)
        self.ambient_particles = []
        self.special_effects = []
        self.init_scenario_effects()
    
    def init_scenario_effects(self):
        """Inicializa efeitos específicos do cenário"""
        # Criar partículas ambientais baseadas no cenário
        if self.config.get('sandstorm'):
            self.create_sandstorm_particles()
        elif self.config.get('bubbles'):
            self.create_bubble_particles()
        elif self.config.get('snowfall'):
            self.create_snow_particles()
        elif self.config.get('fireflies'):
            self.create_firefly_particles()
        elif self.config.get('digital_rain'):
            self.create_digital_rain()
    
    def create_sandstorm_particles(self):
        """Criar partículas de tempestade de areia"""
        for _ in range(50):
            self.ambient_particles.append({
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'speed': random.uniform(2, 5),
                'size': random.randint(2, 4),
                'color': (255, 200, 100, 150),
                'type': 'sand'
            })
    
    def create_bubble_particles(self):
        """Criar bolhas subaquáticas"""
        for _ in range(30):
            self.ambient_particles.append({
                'x': random.randint(0, self.width),
                'y': random.randint(self.height // 2, self.height),
                'speed': random.uniform(0.5, 2),
                'size': random.randint(3, 8),
                'color': (100, 200, 255, 100),
                'type': 'bubble'
            })
    
    def create_snow_particles(self):
        """Criar neve caindo"""
        for _ in range(100):
            self.ambient_particles.append({
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'speed': random.uniform(1, 3),
                'size': random.randint(2, 5),
                'color': (255, 255, 255, 200),
                'sway': random.uniform(-1, 1),
                'type': 'snow'
            })
    
    def create_firefly_particles(self):
        """Criar vaga-lumes"""
        for _ in range(40):
            self.ambient_particles.append({
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'speed': random.uniform(0.5, 1.5),
                'size': 3,
                'color': (255, 255, 100, 255),
                'glow': random.uniform(0, 1),
                'type': 'firefly'
            })
    
    def create_digital_rain(self):
        """Criar chuva digital estilo Matrix"""
        for _ in range(20):
            self.ambient_particles.append({
                'x': random.randint(0, self.width),
                'y': random.randint(-self.height, 0),
                'speed': random.uniform(3, 7),
                'length': random.randint(10, 30),
                'color': (0, 255, 255, 200),
                'type': 'digital'
            })
    
    def update(self, dt):
        """Atualizar animações do cenário"""
        self.animation_time += dt
        
        # Atualizar partículas ambientais
        for particle in self.ambient_particles:
            if particle['type'] == 'sand':
                particle['x'] += particle['speed']
                particle['y'] += particle['speed'] * 0.3
                if particle['x'] > self.width:
                    particle['x'] = 0
                if particle['y'] > self.height:
                    particle['y'] = 0
            
            elif particle['type'] == 'bubble':
                particle['y'] -= particle['speed']
                if particle['y'] < -10:
                    particle['y'] = self.height + 10
            
            elif particle['type'] == 'snow':
                particle['y'] += particle['speed']
                particle['x'] += particle.get('sway', 0)
                if particle['y'] > self.height:
                    particle['y'] = -10
            
            elif particle['type'] == 'firefly':
                import math
                particle['glow'] = (math.sin(self.animation_time * 3 + particle['x']) + 1) / 2
                particle['x'] += math.sin(self.animation_time + particle['y']) * 0.5
                particle['y'] += math.cos(self.animation_time * 1.5 + particle['x']) * 0.3
            
            elif particle['type'] == 'digital':
                particle['y'] += particle['speed']
                if particle['y'] > self.height:
                    particle['y'] = -particle['length']
                    particle['x'] = random.randint(0, self.width)
    
    def render(self, screen):
        """Renderizar efeitos visuais do cenário"""
        # Desenhar partículas ambientais
        for particle in self.ambient_particles:
            if particle['type'] == 'bubble':
                # Bolhas com borda
                color = particle['color']
                pygame.draw.circle(screen, color[:3], 
                                 (int(particle['x']), int(particle['y'])), 
                                 particle['size'])
                pygame.draw.circle(screen, (255, 255, 255, 50), 
                                 (int(particle['x']), int(particle['y'])), 
                                 particle['size'], 1)
            
            elif particle['type'] == 'firefly':
                # Vaga-lumes pulsantes
                glow = int(particle['glow'] * 255)
                color = (255, 255, 100, glow)
                size = particle['size'] + int(particle['glow'] * 2)
                pygame.draw.circle(screen, color[:3], 
                                 (int(particle['x']), int(particle['y'])), 
                                 size)
            
            elif particle['type'] == 'digital':
                # Chuva digital
                pygame.draw.line(screen, particle['color'][:3],
                               (particle['x'], particle['y']),
                               (particle['x'], particle['y'] + particle['length']), 2)
            
            else:
                # Partículas simples
                pygame.draw.circle(screen, particle['color'][:3], 
                                 (int(particle['x']), int(particle['y'])), 
                                 particle['size'])
    
    def get_tunnel_color(self, depth):
        """Retorna cor do túnel baseada na profundidade"""
        colors = self.config['tunnel_colors']
        index = int(depth * len(colors)) % len(colors)
        return colors[index]
    
    def get_background_color(self):
        """Retorna cor de fundo base"""
        return self.config['bg_color_base']
