"""
Menu de Seleção de Modo de Jogo
Interface para escolher entre os diferentes modos
"""

import pygame
import math
from game_modes import GameMode, GameModeConfig

class ModeSelectionMenu:
    """Menu para seleção de modo de jogo"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Fontes
        self.title_font = pygame.font.Font(None, 64)
        self.mode_font = pygame.font.Font(None, 48)
        self.desc_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 24)
        
        # Estado
        self.selected_mode = 0
        self.modes = GameModeConfig.get_all_modes()
        self.animation_time = 0
        
        # Cores
        self.bg_color = (10, 10, 30)
        self.selected_color = (255, 255, 100)
        self.normal_color = (200, 200, 200)
        self.accent_color = (100, 255, 255)
    
    def handle_event(self, event):
        """Processar eventos"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_mode = (self.selected_mode - 1) % len(self.modes)
                return None
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_mode = (self.selected_mode + 1) % len(self.modes)
                return None
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.modes[self.selected_mode]
            elif event.key == pygame.K_ESCAPE:
                return "back"
        
        return None
    
    def update(self, dt):
        """Atualizar animações"""
        self.animation_time += dt
    
    def render(self, screen):
        """Renderizar menu de seleção"""
        screen.fill(self.bg_color)
        
        # Título
        title_surf = self.title_font.render("SELECIONE O MODO", True, self.accent_color)
        title_rect = title_surf.get_rect(centerx=self.width//2, top=30)
        screen.blit(title_surf, title_rect)
        
        # Renderizar modos
        start_y = 150
        spacing = 110
        
        for i, mode in enumerate(self.modes):
            config = GameModeConfig.get_config(mode)
            y_pos = start_y + i * spacing
            
            # Animação de seleção
            is_selected = (i == self.selected_mode)
            color = self.selected_color if is_selected else self.normal_color
            
            # Offset de animação
            offset = 0
            if is_selected:
                offset = int(math.sin(self.animation_time * 5) * 5)
            
            # Ícone e nome do modo
            icon_text = config['icon']
            name_text = config['name']
            
            mode_text = f"{icon_text} {name_text}"
            mode_surf = self.mode_font.render(mode_text, True, color)
            mode_rect = mode_surf.get_rect(centerx=self.width//2 + offset, top=y_pos)
            screen.blit(mode_surf, mode_rect)
            
            # Descrição
            desc_surf = self.desc_font.render(config['description'], True, color)
            desc_rect = desc_surf.get_rect(centerx=self.width//2, top=y_pos + 40)
            screen.blit(desc_surf, desc_rect)
            
            # Detalhes do modo (se selecionado)
            if is_selected:
                details = []
                
                if config['time_limit']:
                    details.append(f"⏱️ {config['time_limit']//60} minutos")
                
                details.append(f"❤️ {config['starting_lives']} vidas")
                
                if config['score_multiplier'] != 1.0:
                    details.append(f"⭐ {config['score_multiplier']}x pontos")
                
                if not config['allow_shop']:
                    details.append("🚫 Sem loja")
                
                details_text = " | ".join(details)
                details_surf = self.small_font.render(details_text, True, self.accent_color)
                details_rect = details_surf.get_rect(centerx=self.width//2, top=y_pos + 70)
                screen.blit(details_surf, details_rect)
        
        # Instruções
        inst_y = self.height - 40
        instructions = [
            "↑↓: Navegar",
            "ENTER: Selecionar",
            "ESC: Voltar"
        ]
        
        inst_text = " | ".join(instructions)
        inst_surf = self.small_font.render(inst_text, True, (150, 150, 150))
        inst_rect = inst_surf.get_rect(centerx=self.width//2, top=inst_y)
        screen.blit(inst_surf, inst_rect)
