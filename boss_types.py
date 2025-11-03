"""
Sistema de Tipos de Boss
Cada boss tem mecânicas, padrões de ataque e visuais únicos
"""

import pygame
import math
import random
from enum import Enum

class BossType(Enum):
    """Tipos de bosses disponíveis"""
    STANDARD = "standard"           # Boss padrão (já existe)
    KRAKEN = "kraken"               # Boss com tentáculos
    PHOENIX = "phoenix"             # Boss de fogo que ressuscita
    MECHA = "mecha"                 # Boss robótico com escudo
    VOID_LORD = "void_lord"         # Boss que teletransporta
    CRYSTAL_BEAST = "crystal_beast" # Boss que spawna cristais
    SWARM_QUEEN = "swarm_queen"     # Boss que spawna minions
    TITAN = "titan"                 # Boss gigante lento
    SPECTER = "specter"             # Boss fantasma intangível

class BossConfig:
    """Configurações específicas de cada tipo de boss"""
    
    @staticmethod
    def get_config(boss_type: BossType, level: int = 1):
        """Retorna configuração completa do boss"""
        
        configs = {
            BossType.STANDARD: {
                'name': 'Guardian',
                'icon': '🛸',
                'max_health': 1000 + (level * 500),
                'size': (120, 100),
                'speed': 1.5,
                'shoot_delay': 30,
                'color_primary': (255, 100, 100),
                'color_secondary': (255, 150, 150),
                'attack_patterns': ['spread', 'spiral', 'aimed'],
                'movement_patterns': ['circular', 'zigzag'],
                'phases': 3,
                'special_ability': None,
                'score_value': 5000
            },
            
            BossType.KRAKEN: {
                'name': 'Deep Kraken',
                'icon': '🐙',
                'max_health': 1200 + (level * 600),
                'size': (150, 120),
                'speed': 1.0,
                'shoot_delay': 25,
                'color_primary': (100, 100, 255),
                'color_secondary': (50, 50, 200),
                'attack_patterns': ['tentacle_sweep', 'ink_cloud', 'whirlpool'],
                'movement_patterns': ['wave', 'dive'],
                'phases': 4,
                'special_ability': 'tentacles',  # Spawna tentáculos
                'tentacle_count': 8,
                'score_value': 7000
            },
            
            BossType.PHOENIX: {
                'name': 'Eternal Phoenix',
                'icon': '🔥',
                'max_health': 800 + (level * 400),
                'size': (140, 110),
                'speed': 2.5,
                'shoot_delay': 20,
                'color_primary': (255, 150, 0),
                'color_secondary': (255, 200, 0),
                'attack_patterns': ['fireball', 'flame_wave', 'meteor_shower'],
                'movement_patterns': ['swooping', 'ascension'],
                'phases': 2,  # Só 2 fases, mas ressuscita!
                'special_ability': 'rebirth',  # Ressuscita com 50% HP
                'rebirth_count': 1,
                'score_value': 10000
            },
            
            BossType.MECHA: {
                'name': 'Assault Mecha',
                'icon': '🤖',
                'max_health': 1500 + (level * 700),
                'size': (130, 140),
                'speed': 1.2,
                'shoot_delay': 15,
                'color_primary': (150, 150, 150),
                'color_secondary': (200, 200, 200),
                'attack_patterns': ['laser_beam', 'missile_barrage', 'emp_pulse'],
                'movement_patterns': ['hovering', 'charge'],
                'phases': 3,
                'special_ability': 'shield',  # Escudo que absorve dano
                'shield_health': 500,
                'shield_recharge_time': 10,  # segundos
                'score_value': 8000
            },
            
            BossType.VOID_LORD: {
                'name': 'Void Lord',
                'icon': '👁️',
                'max_health': 900 + (level * 450),
                'size': (110, 110),
                'speed': 2.0,
                'shoot_delay': 35,
                'color_primary': (100, 0, 150),
                'color_secondary': (150, 0, 200),
                'attack_patterns': ['void_orb', 'shadow_wave', 'dimension_rift'],
                'movement_patterns': ['teleport', 'phase_shift'],
                'phases': 3,
                'special_ability': 'teleport',  # Teletransporta aleatoriamente
                'teleport_frequency': 5,  # segundos
                'score_value': 9000
            },
            
            BossType.CRYSTAL_BEAST: {
                'name': 'Crystal Guardian',
                'icon': '💎',
                'max_health': 1100 + (level * 550),
                'size': (135, 115),
                'speed': 0.8,
                'shoot_delay': 40,
                'color_primary': (0, 255, 255),
                'color_secondary': (100, 200, 255),
                'attack_patterns': ['crystal_shard', 'prism_beam', 'crystal_rain'],
                'movement_patterns': ['floating', 'rotation'],
                'phases': 3,
                'special_ability': 'spawn_crystals',  # Spawna cristais destrutíveis
                'crystal_spawn_rate': 8,  # segundos
                'score_value': 7500
            },
            
            BossType.SWARM_QUEEN: {
                'name': 'Hive Queen',
                'icon': '👑',
                'max_health': 700 + (level * 350),
                'size': (125, 105),
                'speed': 1.3,
                'shoot_delay': 45,
                'color_primary': (255, 255, 0),
                'color_secondary': (200, 200, 0),
                'attack_patterns': ['stinger', 'pheromone_cloud', 'swarm_call'],
                'movement_patterns': ['erratic', 'hovering'],
                'phases': 3,
                'special_ability': 'spawn_minions',  # Spawna mini inimigos
                'minion_spawn_rate': 6,  # segundos
                'minions_per_wave': 5,
                'score_value': 6500
            },
            
            BossType.TITAN: {
                'name': 'Ancient Titan',
                'icon': '⚔️',
                'max_health': 2000 + (level * 1000),
                'size': (180, 160),
                'speed': 0.5,
                'shoot_delay': 50,
                'color_primary': (139, 69, 19),
                'color_secondary': (160, 82, 45),
                'attack_patterns': ['ground_slam', 'boulder_throw', 'shockwave'],
                'movement_patterns': ['stomp', 'charge'],
                'phases': 4,
                'special_ability': 'earthquake',  # Screen shake + debris
                'earthquake_damage': 50,
                'score_value': 12000
            },
            
            BossType.SPECTER: {
                'name': 'Phantom Specter',
                'icon': '👻',
                'max_health': 600 + (level * 300),
                'size': (115, 115),
                'speed': 3.0,
                'shoot_delay': 25,
                'color_primary': (200, 200, 255),
                'color_secondary': (150, 150, 255),
                'attack_patterns': ['ghost_orb', 'haunting_echo', 'soul_drain'],
                'movement_patterns': ['phasing', 'ethereal'],
                'phases': 2,
                'special_ability': 'intangible',  # Fica intangível periodicamente
                'intangible_duration': 3,  # segundos
                'intangible_frequency': 10,  # segundos
                'score_value': 8500
            }
        }
        
        return configs.get(boss_type, configs[BossType.STANDARD])
    
    @staticmethod
    def get_all_types() -> list:
        """Retorna lista de todos os tipos de boss"""
        return list(BossType)
    
    @staticmethod
    def get_random_type(exclude_standard=False):
        """Retorna tipo aleatório de boss"""
        types = list(BossType)  # Chamada direta ao invés de método
        if exclude_standard:
            types = [t for t in types if t != BossType.STANDARD]
        return random.choice(types)
    
    @staticmethod
    def get_type_for_level(level: int):
        """Retorna tipo de boss apropriado para o nível"""
        # Progressão de dificuldade
        if level <= 5:
            return random.choice([BossType.STANDARD, BossType.SWARM_QUEEN])
        elif level <= 10:
            return random.choice([BossType.STANDARD, BossType.KRAKEN, BossType.CRYSTAL_BEAST])
        elif level <= 15:
            return random.choice([BossType.KRAKEN, BossType.MECHA, BossType.VOID_LORD])
        elif level <= 20:
            return random.choice([BossType.PHOENIX, BossType.SPECTER, BossType.MECHA])
        else:
            # Níveis avançados - qualquer boss, incluindo Titan
            return random.choice(list(BossType))

class BossAttackPattern:
    """Padrões de ataque específicos de cada boss"""
    
    @staticmethod
    def create_attack(pattern_name: str, boss_x: int, boss_y: int, player_x: int, player_y: int, level: int = 1):
        """
        Cria projéteis baseado no padrão de ataque
        Retorna lista de bullets
        """
        bullets = []
        
        if pattern_name == 'spread':
            # Padrão clássico - leque de projéteis
            for i in range(5):
                angle = math.pi/2 + (i - 2) * 0.3
                bullets.append({
                    'x': boss_x,
                    'y': boss_y,
                    'dx': math.cos(angle) * 3,
                    'dy': math.sin(angle) * 3,
                    'damage': 20
                })
        
        elif pattern_name == 'spiral':
            # Espiral de projéteis
            for i in range(8):
                angle = (i / 8) * 2 * math.pi
                bullets.append({
                    'x': boss_x,
                    'y': boss_y,
                    'dx': math.cos(angle) * 2.5,
                    'dy': math.sin(angle) * 2.5,
                    'damage': 15
                })
        
        elif pattern_name == 'aimed':
            # Projétil mirando no jogador
            dx = player_x - boss_x
            dy = player_y - boss_y
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0:
                bullets.append({
                    'x': boss_x,
                    'y': boss_y,
                    'dx': (dx / distance) * 4,
                    'dy': (dy / distance) * 4,
                    'damage': 25
                })
        
        # Padrões específicos dos novos bosses
        elif pattern_name == 'tentacle_sweep':
            # Kraken - varredura de tentáculos
            for i in range(3):
                angle = math.pi/2 + (i - 1) * 0.5
                bullets.append({
                    'x': boss_x,
                    'y': boss_y,
                    'dx': math.cos(angle) * 2,
                    'dy': math.sin(angle) * 2,
                    'damage': 30,
                    'type': 'tentacle'
                })
        
        elif pattern_name == 'fireball':
            # Phoenix - bola de fogo grande
            dx = player_x - boss_x
            dy = player_y - boss_y
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0:
                bullets.append({
                    'x': boss_x,
                    'y': boss_y,
                    'dx': (dx / distance) * 3.5,
                    'dy': (dy / distance) * 3.5,
                    'damage': 40,
                    'type': 'fire',
                    'size': 20
                })
        
        elif pattern_name == 'laser_beam':
            # Mecha - laser reto
            bullets.append({
                'x': boss_x,
                'y': boss_y,
                'dx': 0,
                'dy': 5,
                'damage': 35,
                'type': 'laser',
                'width': 10
            })
        
        elif pattern_name == 'void_orb':
            # Void Lord - orbe que persegue
            dx = player_x - boss_x
            dy = player_y - boss_y
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0:
                bullets.append({
                    'x': boss_x,
                    'y': boss_y,
                    'dx': (dx / distance) * 2,
                    'dy': (dy / distance) * 2,
                    'damage': 30,
                    'type': 'homing',
                    'homing_strength': 0.1
                })
        
        return bullets

class BossMovementPattern:
    """Padrões de movimento específicos de cada boss"""
    
    @staticmethod
    def update_position(boss, pattern_name: str, dt: float):
        """Atualiza posição do boss baseado no padrão"""
        
        if pattern_name == 'circular':
            boss.angle += dt * 2
            boss.x = boss.initial_x + math.cos(boss.angle) * 100
            boss.y = boss.initial_y + math.sin(boss.angle) * 50
        
        elif pattern_name == 'zigzag':
            boss.movement_timer += dt
            boss.x += math.sin(boss.movement_timer * 3) * 2
            boss.y = boss.initial_y + math.sin(boss.movement_timer) * 30
        
        elif pattern_name == 'hovering':
            boss.movement_timer += dt
            boss.y = boss.initial_y + math.sin(boss.movement_timer * 2) * 20
        
        elif pattern_name == 'teleport':
            # Void Lord - teletransporta aleatoriamente
            if hasattr(boss, 'teleport_timer'):
                boss.teleport_timer -= dt
                if boss.teleport_timer <= 0:
                    boss.x = random.randint(100, 700)
                    boss.y = random.randint(50, 200)
                    boss.teleport_timer = 5  # Reset
        
        elif pattern_name == 'phasing':
            # Specter - movimento fantasmagórico
            boss.movement_timer += dt
            boss.x += math.sin(boss.movement_timer * 4) * 3
            boss.y = boss.initial_y + math.cos(boss.movement_timer * 2) * 40
        
        elif pattern_name == 'swooping':
            # Phoenix - mergulhos rápidos
            boss.movement_timer += dt
            if boss.movement_timer > 3:  # A cada 3 segundos
                boss.y += 5  # Mergulha
                if boss.y > 400:
                    boss.y = 50  # Volta ao topo
                    boss.movement_timer = 0
