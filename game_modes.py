"""
Sistema de Modos de Jogo
- Arcade Mode: Jogo clássico progressivo
- Survival Mode: Sem upgrades, máxima dificuldade
- Boss Rush: Apenas bosses consecutivos
- Time Attack: Score máximo em 3 minutos
"""

import pygame
from enum import Enum

class GameMode(Enum):
    ARCADE = "arcade"
    SURVIVAL = "survival"
    BOSS_RUSH = "boss_rush"
    TIME_ATTACK = "time_attack"

class GameModeConfig:
    """Configurações específicas de cada modo"""
    
    @staticmethod
    def get_config(mode: GameMode):
        """Retorna configuração do modo"""
        configs = {
            GameMode.ARCADE: {
                'name': 'ARCADE',
                'description': 'Modo clássico com dificuldade progressiva',
                'icon': '🎮',
                'allow_shop': True,
                'allow_powerups': True,
                'time_limit': None,
                'starting_lives': 3,
                'difficulty_multiplier': 1.0,
                'score_multiplier': 1.0,
                'boss_frequency': 5,  # Boss a cada 5 níveis
                'enemy_spawn_rate': 1.0,
            },
            GameMode.SURVIVAL: {
                'name': 'SURVIVAL',
                'description': 'Sobreviva o máximo possível sem upgrades',
                'icon': '💀',
                'allow_shop': False,
                'allow_powerups': False,
                'time_limit': None,
                'starting_lives': 1,
                'difficulty_multiplier': 1.5,
                'score_multiplier': 2.0,
                'boss_frequency': 3,
                'enemy_spawn_rate': 1.5,
            },
            GameMode.BOSS_RUSH: {
                'name': 'BOSS RUSH',
                'description': 'Enfrente bosses consecutivos',
                'icon': '👹',
                'allow_shop': True,
                'allow_powerups': True,
                'time_limit': None,
                'starting_lives': 5,
                'difficulty_multiplier': 1.2,
                'score_multiplier': 1.5,
                'boss_frequency': 1,  # Boss a cada nível!
                'enemy_spawn_rate': 0.3,  # Menos inimigos comuns
            },
            GameMode.TIME_ATTACK: {
                'name': 'TIME ATTACK',
                'description': 'Score máximo em 3 minutos',
                'icon': '⏱️',
                'allow_shop': True,
                'allow_powerups': True,
                'time_limit': 180,  # 3 minutos
                'starting_lives': 5,
                'difficulty_multiplier': 0.8,
                'score_multiplier': 1.5,
                'boss_frequency': 10,  # Menos bosses
                'enemy_spawn_rate': 1.2,
            }
        }
        return configs.get(mode, configs[GameMode.ARCADE])
    
    @staticmethod
    def get_all_modes():
        """Retorna lista de todos os modos"""
        return [
            GameMode.ARCADE,
            GameMode.SURVIVAL,
            GameMode.BOSS_RUSH,
            GameMode.TIME_ATTACK
        ]

class GameModeManager:
    """Gerenciador de modo de jogo"""
    
    def __init__(self):
        self.current_mode = GameMode.ARCADE
        self.config = GameModeConfig.get_config(self.current_mode)
        self.time_elapsed = 0
        self.time_remaining = None
    
    def set_mode(self, mode: GameMode):
        """Define o modo de jogo"""
        self.current_mode = mode
        self.config = GameModeConfig.get_config(mode)
        self.time_elapsed = 0
        
        # Configurar timer se necessário
        if self.config['time_limit']:
            self.time_remaining = self.config['time_limit']
        else:
            self.time_remaining = None
        
        print(f"🎮 Modo de jogo: {self.config['name']}")
        print(f"   {self.config['description']}")
    
    def update(self, dt):
        """Atualizar timer se necessário"""
        self.time_elapsed += dt
        
        if self.time_remaining is not None:
            self.time_remaining -= dt
            if self.time_remaining <= 0:
                self.time_remaining = 0
                return True  # Tempo esgotado
        
        return False
    
    def is_shop_allowed(self):
        """Verifica se a loja está permitida"""
        return self.config['allow_shop']
    
    def is_powerup_allowed(self):
        """Verifica se powerups estão permitidos"""
        return self.config['allow_powerups']
    
    def get_starting_lives(self):
        """Retorna vidas iniciais"""
        return self.config['starting_lives']
    
    def get_difficulty_multiplier(self):
        """Retorna multiplicador de dificuldade"""
        return self.config['difficulty_multiplier']
    
    def get_score_multiplier(self):
        """Retorna multiplicador de pontuação"""
        return self.config['score_multiplier']
    
    def get_boss_frequency(self):
        """Retorna frequência de bosses"""
        return self.config['boss_frequency']
    
    def get_enemy_spawn_rate(self):
        """Retorna taxa de spawn de inimigos"""
        return self.config['enemy_spawn_rate']
    
    def should_spawn_boss(self, level):
        """Verifica se deve spawnar boss neste nível"""
        freq = self.config['boss_frequency']
        return level % freq == 0
    
    def get_time_display(self):
        """Retorna string formatada do tempo"""
        if self.time_remaining is not None:
            minutes = int(self.time_remaining // 60)
            seconds = int(self.time_remaining % 60)
            return f"{minutes:02d}:{seconds:02d}"
        else:
            minutes = int(self.time_elapsed // 60)
            seconds = int(self.time_elapsed % 60)
            return f"{minutes:02d}:{seconds:02d}"
    
    def get_mode_icon(self):
        """Retorna ícone do modo"""
        return self.config['icon']
    
    def get_mode_name(self):
        """Retorna nome do modo"""
        return self.config['name']
