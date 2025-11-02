"""
Sistema de Input de Nome do Jogador
Para salvar no leaderboard com nome personalizado
"""

import pygame

class NameInputDialog:
    """Diálogo para input de nome do jogador"""
    
    def __init__(self, width, height, default_name="Player"):
        self.width = width
        self.height = height
        self.active = False
        self.name = default_name
        self.max_length = 12
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_speed = 0.5
        
        # Fontes
        self.title_font = pygame.font.Font(None, 56)
        self.input_font = pygame.font.Font(None, 64)
        self.instruction_font = pygame.font.Font(None, 32)
        
        # Cores
        self.bg_color = (20, 20, 40, 220)
        self.title_color = (255, 255, 100)
        self.input_color = (255, 255, 255)
        self.cursor_color = (255, 255, 100)
        self.instruction_color = (200, 200, 200)
        
        # Dimensões do diálogo
        self.dialog_width = 500
        self.dialog_height = 300
        self.dialog_x = (width - self.dialog_width) // 2
        self.dialog_y = (height - self.dialog_height) // 2
        
    def activate(self, initial_name="Player"):
        """Ativar o diálogo"""
        self.active = True
        self.name = initial_name
        self.cursor_visible = True
        self.cursor_timer = 0
    
    def deactivate(self):
        """Desativar o diálogo"""
        self.active = False
    
    def handle_event(self, event):
        """Processar eventos de input"""
        if not self.active:
            return None
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Confirmar nome
                if len(self.name.strip()) > 0:
                    self.deactivate()
                    return self.name.strip()
            
            elif event.key == pygame.K_ESCAPE:
                # Cancelar
                self.deactivate()
                return "Player"
            
            elif event.key == pygame.K_BACKSPACE:
                # Apagar último caractere
                self.name = self.name[:-1]
            
            elif len(self.name) < self.max_length:
                # Adicionar caractere (apenas letras, números, espaço)
                char = event.unicode
                if char.isalnum() or char == ' ':
                    self.name += char
        
        return None
    
    def update(self, dt):
        """Atualizar animações"""
        if not self.active:
            return
        
        # Piscar cursor
        self.cursor_timer += dt
        if self.cursor_timer >= self.cursor_blink_speed:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def render(self, screen):
        """Renderizar diálogo"""
        if not self.active:
            return
        
        # Overlay escuro
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Fundo do diálogo
        dialog_surf = pygame.Surface((self.dialog_width, self.dialog_height), pygame.SRCALPHA)
        dialog_surf.fill(self.bg_color)
        
        # Borda
        pygame.draw.rect(dialog_surf, self.title_color, 
                        (0, 0, self.dialog_width, self.dialog_height), 3)
        
        # Título
        title_text = "ENTER YOUR NAME"
        title_surf = self.title_font.render(title_text, True, self.title_color)
        title_rect = title_surf.get_rect(centerx=self.dialog_width//2, top=30)
        dialog_surf.blit(title_surf, title_rect)
        
        # Input box
        input_box_y = 110
        input_box_height = 80
        pygame.draw.rect(dialog_surf, (50, 50, 80), 
                        (20, input_box_y, self.dialog_width-40, input_box_height))
        pygame.draw.rect(dialog_surf, self.input_color, 
                        (20, input_box_y, self.dialog_width-40, input_box_height), 2)
        
        # Texto do nome
        name_surf = self.input_font.render(self.name, True, self.input_color)
        name_rect = name_surf.get_rect(center=(self.dialog_width//2, input_box_y + input_box_height//2))
        dialog_surf.blit(name_surf, name_rect)
        
        # Cursor
        if self.cursor_visible and len(self.name) < self.max_length:
            cursor_x = name_rect.right + 5
            cursor_y = name_rect.centery
            pygame.draw.line(dialog_surf, self.cursor_color,
                           (cursor_x, cursor_y - 20),
                           (cursor_x, cursor_y + 20), 3)
        
        # Instruções
        instructions = [
            "Type your name",
            "ENTER to confirm | ESC to skip",
            f"{len(self.name)}/{self.max_length} characters"
        ]
        
        y_pos = 220
        for instruction in instructions:
            inst_surf = self.instruction_font.render(instruction, True, self.instruction_color)
            inst_rect = inst_surf.get_rect(centerx=self.dialog_width//2, top=y_pos)
            dialog_surf.blit(inst_surf, inst_rect)
            y_pos += 28
        
        # Blitar diálogo na tela
        screen.blit(dialog_surf, (self.dialog_x, self.dialog_y))
