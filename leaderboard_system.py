"""
Sistema de Leaderboards Local
Preparado para futura integração com Steam Leaderboards
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from game_modes import GameMode

class LeaderboardEntry:
    """Entrada individual do leaderboard"""
    
    def __init__(self, player_name: str, score: int, level: int, 
                 mode: str, kills: int, timestamp: Optional[str] = None):
        self.player_name = player_name
        self.score = score
        self.level = level
        self.mode = mode
        self.kills = kills
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        return {
            'player_name': self.player_name,
            'score': self.score,
            'level': self.level,
            'mode': self.mode,
            'kills': self.kills,
            'timestamp': self.timestamp
        }
    
    @staticmethod
    def from_dict(data):
        return LeaderboardEntry(
            data['player_name'],
            data['score'],
            data['level'],
            data['mode'],
            data['kills'],
            data.get('timestamp')
        )

class LeaderboardSystem:
    """Sistema de leaderboards local"""
    
    def __init__(self, save_file='leaderboards.json'):
        self.save_file = save_file
        self.leaderboards = {
            'arcade': [],
            'survival': [],
            'boss_rush': [],
            'time_attack': [],
            'global': []  # Todos os modos combinados
        }
        self.max_entries = 100  # Manter top 100 de cada modo
        self.load()
    
    def load(self):
        """Carregar leaderboards do arquivo"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for mode in self.leaderboards.keys():
                    if mode in data:
                        self.leaderboards[mode] = [
                            LeaderboardEntry.from_dict(entry) 
                            for entry in data[mode]
                        ]
            except Exception as e:
                print(f"⚠️ Erro ao carregar leaderboards: {e}")
    
    def save(self):
        """Salvar leaderboards no arquivo"""
        try:
            data = {}
            for mode, entries in self.leaderboards.items():
                data[mode] = [entry.to_dict() for entry in entries]
            
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar leaderboards: {e}")
    
    def add_entry(self, entry: LeaderboardEntry):
        """Adicionar nova entrada ao leaderboard"""
        # Adicionar ao leaderboard específico do modo
        mode_key = entry.mode.lower()
        if mode_key in self.leaderboards:
            self.leaderboards[mode_key].append(entry)
            self.leaderboards[mode_key].sort(key=lambda x: x.score, reverse=True)
            self.leaderboards[mode_key] = self.leaderboards[mode_key][:self.max_entries]
        
        # Adicionar ao leaderboard global
        self.leaderboards['global'].append(entry)
        self.leaderboards['global'].sort(key=lambda x: x.score, reverse=True)
        self.leaderboards['global'] = self.leaderboards['global'][:self.max_entries]
        
        self.save()
    
    def get_top_entries(self, mode: str = 'global', limit: int = 10) -> List[LeaderboardEntry]:
        """Obter top N entradas de um modo"""
        mode_key = mode.lower()
        if mode_key in self.leaderboards:
            return self.leaderboards[mode_key][:limit]
        return []
    
    def get_player_rank(self, score: int, mode: str = 'global') -> int:
        """Obter rank de uma pontuação"""
        mode_key = mode.lower()
        if mode_key not in self.leaderboards:
            return -1
        
        entries = self.leaderboards[mode_key]
        rank = 1
        for entry in entries:
            if score >= entry.score:
                return rank
            rank += 1
        
        return rank
    
    def is_high_score(self, score: int, mode: str = 'global') -> bool:
        """Verifica se é um high score (top 10)"""
        mode_key = mode.lower()
        if mode_key not in self.leaderboards:
            return True
        
        entries = self.leaderboards[mode_key]
        if len(entries) < 10:
            return True
        
        return score > entries[9].score
    
    def get_stats(self, mode: str = 'global') -> Dict:
        """Obter estatísticas do leaderboard"""
        mode_key = mode.lower()
        if mode_key not in self.leaderboards:
            return {}
        
        entries = self.leaderboards[mode_key]
        if not entries:
            return {
                'total_entries': 0,
                'highest_score': 0,
                'average_score': 0,
                'total_kills': 0
            }
        
        scores = [e.score for e in entries]
        kills = [e.kills for e in entries]
        
        return {
            'total_entries': len(entries),
            'highest_score': max(scores),
            'average_score': sum(scores) // len(scores),
            'total_kills': sum(kills)
        }

class LeaderboardRenderer:
    """Renderizador de leaderboards"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Fontes
        self.title_font = pygame.font.Font(None, 64)
        self.header_font = pygame.font.Font(None, 40)
        self.entry_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # Cores
        self.bg_color = (10, 10, 30, 200)
        self.title_color = (255, 255, 100)
        self.gold_color = (255, 215, 0)
        self.silver_color = (192, 192, 192)
        self.bronze_color = (205, 127, 50)
        self.text_color = (255, 255, 255)
    
    def render(self, screen, leaderboard: LeaderboardSystem, mode: str = 'global'):
        """Renderizar leaderboard"""
        # Fundo semi-transparente
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Título
        mode_names = {
            'global': '🏆 GLOBAL LEADERBOARD',
            'arcade': '🎮 ARCADE',
            'survival': '💀 SURVIVAL',
            'boss_rush': '👹 BOSS RUSH',
            'time_attack': '⏱️ TIME ATTACK'
        }
        
        title_text = mode_names.get(mode, '🏆 LEADERBOARD')
        title_surf = self.title_font.render(title_text, True, self.title_color)
        title_rect = title_surf.get_rect(centerx=self.width//2, top=30)
        screen.blit(title_surf, title_rect)
        
        # Headers
        y_pos = 120
        headers = ['#', 'PLAYER', 'SCORE', 'LEVEL', 'KILLS']
        x_positions = [100, 200, 450, 580, 680]
        
        for i, header in enumerate(headers):
            header_surf = self.header_font.render(header, True, (150, 150, 150))
            screen.blit(header_surf, (x_positions[i], y_pos))
        
        # Linha separadora
        pygame.draw.line(screen, (100, 100, 100), 
                        (80, y_pos + 40), (self.width - 80, y_pos + 40), 2)
        
        # Entradas
        entries = leaderboard.get_top_entries(mode, 10)
        y_pos = 170
        
        for i, entry in enumerate(entries):
            rank = i + 1
            
            # Cor baseada no rank
            if rank == 1:
                color = self.gold_color
            elif rank == 2:
                color = self.silver_color
            elif rank == 3:
                color = self.bronze_color
            else:
                color = self.text_color
            
            # Renderizar dados
            rank_surf = self.entry_font.render(f"{rank}.", True, color)
            name_surf = self.entry_font.render(entry.player_name[:12], True, color)
            score_surf = self.entry_font.render(f"{entry.score:,}", True, color)
            level_surf = self.entry_font.render(str(entry.level), True, color)
            kills_surf = self.entry_font.render(str(entry.kills), True, color)
            
            screen.blit(rank_surf, (x_positions[0], y_pos))
            screen.blit(name_surf, (x_positions[1], y_pos))
            screen.blit(score_surf, (x_positions[2], y_pos))
            screen.blit(level_surf, (x_positions[3], y_pos))
            screen.blit(kills_surf, (x_positions[4], y_pos))
            
            y_pos += 40
        
        # Estatísticas
        stats = leaderboard.get_stats(mode)
        stats_y = self.height - 80
        
        stats_text = f"Total Entries: {stats.get('total_entries', 0)} | "
        stats_text += f"Highest Score: {stats.get('highest_score', 0):,} | "
        stats_text += f"Avg Score: {stats.get('average_score', 0):,}"
        
        stats_surf = self.small_font.render(stats_text, True, (150, 150, 150))
        stats_rect = stats_surf.get_rect(centerx=self.width//2, top=stats_y)
        screen.blit(stats_surf, stats_rect)
        
        # Instruções
        inst_surf = self.small_font.render(
            "ESC: Voltar | TAB: Mudar Modo", 
            True, (200, 200, 200)
        )
        inst_rect = inst_surf.get_rect(centerx=self.width//2, bottom=self.height - 20)
        screen.blit(inst_surf, inst_rect)

import pygame
