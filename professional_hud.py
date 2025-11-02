import pygame
import math
import colorsys

class ProfessionalHUD:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Fontes customizadas com tamanhos maiores
        pygame.font.init()
        self.large_font = pygame.font.Font(None, 56)
        self.medium_font = pygame.font.Font(None, 42)
        self.small_font = pygame.font.Font(None, 28)
        
        # Cores psicodélicas
        self.primary_color = (255, 255, 255)
        self.score_color = (255, 200, 100)
        self.level_color = (100, 200, 255)
        self.health_color = (255, 100, 100)
        self.energy_color = (100, 255, 150)
        self.lives_color = (255, 100, 255)
        
        # Animações
        self.score_pulse = 0
        self.last_score = 0
        self.score_animation_timer = 0
        self.color_shift = 0
        
        # Timer para dicas de controle (10 segundos)
        self.controls_display_timer = 10.0
        self.show_controls = True
        self.controls_visible = True  # Atributo para compatibilidade
        
        # Margens da tela
        self.margin = 30
    
    def update(self, dt, score, lives, level, player_health=100):
        """Atualizar animações do HUD"""
        self.score_pulse += dt * 5
        self.color_shift += dt * 2
        
        # Animação de score aumentando
        if score != self.last_score:
            self.score_animation_timer = 0.5
            self.last_score = score
        
        if self.score_animation_timer > 0:
            self.score_animation_timer -= dt
        
        # Timer para esconder dicas de controle após 10 segundos
        if self.controls_display_timer > 0:
            self.controls_display_timer -= dt
            if self.controls_display_timer <= 0:
                self.show_controls = False
    
    def get_psychedelic_color(self, base_color, intensity=1.0):
        """Gerar cor psicodélica animada"""
        hue = (self.color_shift % 1.0)
        rgb = colorsys.hsv_to_rgb(hue, 0.8, intensity)
        return tuple(int(c * 255) for c in rgb)
    
    def draw_glow_text(self, screen, text, font, color, pos, glow=True):
        """Desenhar texto com efeito de brilho"""
        if glow:
            # Efeito de brilho
            glow_color = tuple(min(255, c + 50) for c in color)
            for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
                glow_surf = font.render(text, True, glow_color)
                glow_surf.set_alpha(80)
                screen.blit(glow_surf, (pos[0] + offset[0], pos[1] + offset[1]))
        
        # Texto principal
        text_surf = font.render(text, True, color)
        screen.blit(text_surf, pos)
        return text_surf.get_rect(topleft=pos)
    
    def draw_score(self, screen, score):
        """Desenhar SCORE no canto superior esquerdo"""
        x = self.margin
        y = self.margin
        
        # Label
        label_color = self.score_color
        self.draw_glow_text(screen, "SCORE", self.small_font, label_color, (x, y))
        
        # Valor do score com animação
        scale = 1.0
        if self.score_animation_timer > 0:
            scale = 1.0 + 0.15 * (self.score_animation_timer / 0.5)
        
        score_text = f"{score:,}"
        if scale != 1.0:
            temp_surf = self.large_font.render(score_text, True, self.primary_color)
            original_size = temp_surf.get_size()
            new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
            scaled_surf = pygame.transform.scale(temp_surf, new_size)
            screen.blit(scaled_surf, (x, y + 35))
        else:
            self.draw_glow_text(screen, score_text, self.large_font, self.primary_color, (x, y + 35))
    
    def draw_level(self, screen, level):
        """Desenhar LEVEL abaixo do SCORE"""
        x = self.margin
        y = self.margin + 110
        
        # Label
        label_color = self.level_color
        self.draw_glow_text(screen, "LEVEL", self.small_font, label_color, (x, y))
        
        # Valor do level
        level_text = f"{level}"
        self.draw_glow_text(screen, level_text, self.large_font, self.primary_color, (x, y + 35))
    
    def draw_lives(self, screen, lives):
        """Desenhar VIDAS no canto superior direito"""
        x = self.width - self.margin - 150
        y = self.margin
        
        # Label
        label_color = self.lives_color
        self.draw_glow_text(screen, "VIDAS", self.small_font, label_color, (x, y))
        
        # Ícones de vidas (corações psicodélicos)
        icon_y = y + 40
        for i in range(lives):
            icon_x = x + i * 40
            self.draw_life_icon(screen, icon_x, icon_y)
    
    def draw_life_icon(self, screen, x, y):
        """Desenhar ícone de vida (nave com efeito psicodélico)"""
        # Cores psicodélicas
        hue = (self.color_shift + 0.3) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        color = tuple(int(c * 255) for c in rgb)
        
        # Nave triangular
        points = [
            (x + 15, y),
            (x, y + 25),
            (x + 30, y + 25)
        ]
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, self.primary_color, points, 2)
    
    def draw_energy_bar(self, screen, health, max_health=100):
        """Desenhar barra de ENERGIA abaixo das VIDAS"""
        x = self.width - self.margin - 200
        y = self.margin + 110
        
        # Label
        label_color = self.energy_color
        self.draw_glow_text(screen, "ENERGIA", self.small_font, label_color, (x, y))
        
        # Barra de energia
        bar_width = 180
        bar_height = 30
        bar_x = x
        bar_y = y + 40
        
        # Fundo da barra (escuro)
        background_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, (30, 30, 30), background_rect)
        
        # Barra preenchida com cor dinâmica
        health_ratio = health / max_health
        filled_width = int(bar_width * health_ratio)
        filled_rect = pygame.Rect(bar_x, bar_y, filled_width, bar_height)
        
        # Cor baseada na saúde com efeito psicodélico
        if health_ratio > 0.6:
            base_hue = 0.33  # Verde
        elif health_ratio > 0.3:
            base_hue = 0.16  # Amarelo
        else:
            base_hue = 0.0   # Vermelho
        
        rgb = colorsys.hsv_to_rgb(base_hue, 0.9, 1.0)
        bar_color = tuple(int(c * 255) for c in rgb)
        
        # Gradiente na barra
        for i in range(filled_width):
            progress = i / bar_width
            intensity = 0.7 + 0.3 * math.sin(self.score_pulse + progress * 10)
            segment_color = tuple(int(c * intensity) for c in bar_color)
            pygame.draw.line(screen, segment_color, 
                           (bar_x + i, bar_y), 
                           (bar_x + i, bar_y + bar_height))
        
        # Borda externa com brilho
        pygame.draw.rect(screen, self.primary_color, background_rect, 3)
        
        # Texto da porcentagem centralizado
        percent_text = f"{int(health)}%"
        text_surf = self.medium_font.render(percent_text, True, self.primary_color)
        text_rect = text_surf.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
        
        # Sombra do texto
        shadow_surf = self.medium_font.render(percent_text, True, (0, 0, 0))
        screen.blit(shadow_surf, (text_rect.x + 2, text_rect.y + 2))
        screen.blit(text_surf, text_rect)
    
    def draw_controls_help(self, screen):
        """Desenhar ajuda de controles (aparece nos primeiros 10 segundos)"""
        controls = [
            "WASD/Setas - Mover",
            "ESPAÇO - Atirar", 
            "P - Pausar",
            "ESC - Sair"
        ]
        
        # Centralizado na parte inferior
        start_x = self.width // 2 - 120
        start_y = self.height - 130
        
        # Fundo semi-transparente
        panel_width = 240
        panel_height = 120
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.set_alpha(160)
        panel_surface.fill((10, 10, 30))
        screen.blit(panel_surface, (start_x - 10, start_y - 10))
        
        # Borda com efeito psicodélico
        border_color = self.get_psychedelic_color((255, 255, 255), 0.8)
        pygame.draw.rect(screen, border_color, (start_x - 10, start_y - 10, panel_width, panel_height), 2)
        
        for i, control in enumerate(controls):
            color = self.get_psychedelic_color(self.primary_color, 0.9)
            text = self.small_font.render(control, True, color)
            screen.blit(text, (start_x, start_y + i * 28))
    
    def draw_complete_hud(self, screen, score, lives, level, health=100, player_y=0, level_generator=None, coins=0, fps=0.0, show_fps=False):
        """Desenhar HUD completo e limpo"""
        # Esquerda: Score (topo) e Level (abaixo)
        self.draw_score(screen, score)
        self.draw_level(screen, level)
        
        # Direita: Vidas (topo) e Energia (abaixo)
        self.draw_lives(screen, lives)
        self.draw_energy_bar(screen, health)
        
        # Centro-topo: Moedas
        if coins > 0:
            self.draw_coins(screen, coins)
        
        # FPS (canto superior direito)
        if show_fps and fps > 0:
            self.draw_fps(screen, fps)
        
        # Controles (primeiros 10 segundos)
        if self.show_controls:
            self.draw_controls_help(screen)
    
    def draw_coins(self, screen, coins):
        """Desenhar contador de moedas"""
        coin_text = f"💰 {coins}"
        text_color = self.get_psychedelic_color(0.15)  # Cor dourada
        
        # Renderizar com brilho
        self.draw_glow_text(screen, coin_text, self.medium_font, text_color, 
                           (self.width // 2, 30), glow=True)
    
    def draw_fps(self, screen, fps):
        """Desenhar contador de FPS"""
        fps_text = f"FPS: {int(fps)}"
        
        # Cor baseada no FPS
        if fps >= 55:
            color = (0, 255, 0)  # Verde
        elif fps >= 30:
            color = (255, 255, 0)  # Amarelo
        else:
            color = (255, 0, 0)  # Vermelho
        
        fps_surface = self.small_font.render(fps_text, True, color)
        screen.blit(fps_surface, (self.width - 100, 10))
    
    def reset_controls_timer(self):
        """Reativar dicas de controle"""
        self.controls_display_timer = 10.0
        self.show_controls = True
    
    def force_show_controls(self, show=True):
        """Forçar mostrar ou esconder dicas de controle"""
        self.show_controls = show