import pygame
import math

class ComboSystem:
    """Sistema de combo com feedback visual"""
    
    def __init__(self):
        self.reset()
        
        # Configurações visuais
        self.font_large = pygame.font.Font(None, 80)
        self.font_medium = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 30)
        
        # Floating text
        self.floating_texts = []
        
        # Screen effects
        self.screen_shake = 0
        self.slow_motion_timer = 0
        self.flash_timer = 0
        self.flash_color = (255, 255, 255)
    
    def reset(self):
        """Resetar combo"""
        self.combo = 0
        self.max_combo = 0
        self.last_kill_time = 0
        self.combo_timer = 0
        self.combo_timeout = 2.0  # 2 segundos para manter combo
        self.multiplier = 1.0
    
    def add_kill(self, current_time, position=None):
        """Adicionar kill ao combo"""
        self.combo += 1
        self.max_combo = max(self.max_combo, self.combo)
        self.last_kill_time = current_time
        self.combo_timer = self.combo_timeout
        
        # Calcular multiplicador baseado no combo
        if self.combo >= 100:
            self.multiplier = 5.0
        elif self.combo >= 50:
            self.multiplier = 4.0
        elif self.combo >= 25:
            self.multiplier = 3.0
        elif self.combo >= 10:
            self.multiplier = 2.0
        elif self.combo >= 5:
            self.multiplier = 1.5
        else:
            self.multiplier = 1.0
        
        # Efeitos especiais baseados no combo
        if self.combo % 50 == 0:
            self.trigger_slow_motion(1.0)
            self.screen_shake = 15
            self.flash_timer = 0.3
            self.flash_color = (255, 215, 0)  # Ouro
        elif self.combo % 25 == 0:
            self.screen_shake = 10
            self.flash_timer = 0.2
            self.flash_color = (255, 140, 0)  # Laranja
        elif self.combo % 10 == 0:
            self.screen_shake = 5
            self.flash_timer = 0.1
            self.flash_color = (255, 255, 255)  # Branco
        
        # Adicionar texto flutuante
        if position:
            self.add_floating_text(f"+{int(10 * self.multiplier)}", position)
            
            if self.combo >= 5:
                combo_text = f"x{self.combo} COMBO!"
                self.add_floating_text(combo_text, (position[0], position[1] - 30), 
                                     color=self.get_combo_color(), size='large')
    
    def update(self, dt):
        """Atualizar sistema de combo"""
        # Atualizar timer do combo
        if self.combo > 0:
            self.combo_timer -= dt
            if self.combo_timer <= 0:
                # Combo quebrado
                if self.combo >= 5:
                    print(f"❌ Combo perdido! Máximo: {self.combo}")
                self.reset()
        
        # Atualizar textos flutuantes
        for text in self.floating_texts[:]:
            text['y'] -= text['speed'] * dt * 60
            text['alpha'] -= dt * 200
            text['scale'] += dt * 0.5
            
            if text['alpha'] <= 0:
                self.floating_texts.remove(text)
        
        # Atualizar screen shake
        if self.screen_shake > 0:
            self.screen_shake -= dt * 30
            self.screen_shake = max(0, self.screen_shake)
        
        # Atualizar slow motion
        if self.slow_motion_timer > 0:
            self.slow_motion_timer -= dt
        
        # Atualizar flash
        if self.flash_timer > 0:
            self.flash_timer -= dt
    
    def trigger_slow_motion(self, duration):
        """Ativar câmera lenta"""
        self.slow_motion_timer = duration
    
    def is_slow_motion(self):
        """Verificar se está em câmera lenta"""
        return self.slow_motion_timer > 0
    
    def get_time_scale(self):
        """Obter escala de tempo (para câmera lenta)"""
        if self.is_slow_motion():
            return 0.5
        return 1.0
    
    def get_screen_shake(self):
        """Obter offset para screen shake"""
        if self.screen_shake > 0:
            import random
            offset_x = random.uniform(-self.screen_shake, self.screen_shake)
            offset_y = random.uniform(-self.screen_shake, self.screen_shake)
            return (int(offset_x), int(offset_y))
        return (0, 0)
    
    def add_floating_text(self, text, position, color=None, size='medium'):
        """Adicionar texto flutuante"""
        if color is None:
            color = (255, 255, 255)
        
        self.floating_texts.append({
            'text': text,
            'x': position[0],
            'y': position[1],
            'color': color,
            'alpha': 255,
            'speed': 1.0,
            'scale': 1.0,
            'size': size
        })
    
    def get_combo_color(self):
        """Obter cor baseada no combo"""
        if self.combo >= 100:
            return (255, 215, 0)  # Ouro
        elif self.combo >= 50:
            return (255, 0, 255)  # Magenta
        elif self.combo >= 25:
            return (255, 140, 0)  # Laranja
        elif self.combo >= 10:
            return (255, 255, 0)  # Amarelo
        elif self.combo >= 5:
            return (0, 255, 255)  # Ciano
        return (255, 255, 255)  # Branco
    
    def render(self, screen):
        """Renderizar combo e efeitos - VERSÃO COMPACTA"""
        screen_width, screen_height = screen.get_size()
        
        # Renderizar flash de tela (mantém)
        if self.flash_timer > 0:
            alpha = int((self.flash_timer / 0.3) * 80)  # Reduzido de 100 para 80
            flash_surf = pygame.Surface((screen_width, screen_height))
            flash_surf.fill(self.flash_color)
            flash_surf.set_alpha(alpha)
            screen.blit(flash_surf, (0, 0))
        
        # Renderizar combo COMPACTO (só se >= 5)
        if self.combo >= 5:
            # POSIÇÃO AJUSTADA: Mais no centro-inferior para não sobrepor HUD
            combo_y = screen_height // 2 + 50  # Movido mais para baixo
            
            combo_text = f"{self.combo}x COMBO"
            multiplier_text = f"Mult: x{self.multiplier:.1f}"
            
            # Texto menor
            color = self.get_combo_color()
            text_surf = self.font_medium.render(combo_text, True, color)  # font_medium em vez de large
            text_rect = text_surf.get_rect(center=(screen_width // 2, combo_y))
            
            # Sombra sutil
            shadow_surf = self.font_medium.render(combo_text, True, (0, 0, 0))
            shadow_rect = shadow_surf.get_rect(center=(screen_width // 2 + 2, combo_y + 2))
            screen.blit(shadow_surf, shadow_rect)
            screen.blit(text_surf, text_rect)
            
            # Multiplicador menor
            mult_surf = self.font_small.render(multiplier_text, True, (255, 215, 0))
            mult_rect = mult_surf.get_rect(center=(screen_width // 2, combo_y + 35))
            screen.blit(mult_surf, mult_rect)
            
            # Barra de timer MENOR
            bar_width = 150  # Reduzido de 200
            bar_height = 6   # Reduzido de 10
            bar_x = screen_width // 2 - bar_width // 2
            bar_y = combo_y + 55
            
            # Fundo da barra
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            
            # Barra preenchida
            fill_width = int((self.combo_timer / self.combo_timeout) * bar_width)
            bar_color = color if self.combo_timer > 0.5 else (255, 0, 0)
            pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_width, bar_height))
            
            # Borda
            pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)
        
        # Renderizar textos flutuantes (reduzidos)
        for text_obj in self.floating_texts:
            # Usar fonte menor para textos flutuantes
            if text_obj['size'] == 'large':
                font = self.font_medium  # Reduzido
            elif text_obj['size'] == 'small':
                font = pygame.font.Font(None, 20)  # Ainda menor
            else:
                font = self.font_small
            
            text_surf = font.render(text_obj['text'], True, text_obj['color'])
            text_surf.set_alpha(max(0, int(text_obj['alpha'])))
            
            # Aplicar escala
            if text_obj['scale'] != 1.0:
                width = int(text_surf.get_width() * text_obj['scale'])
                height = int(text_surf.get_height() * text_obj['scale'])
                text_surf = pygame.transform.scale(text_surf, (width, height))
            
            text_rect = text_surf.get_rect(center=(int(text_obj['x']), int(text_obj['y'])))
            screen.blit(text_surf, text_rect)
        
        # Indicador de slow motion COMPACTO (canto inferior direito)
        if self.is_slow_motion():
            slow_text = "⏱️ SLOW-MO"
            slow_surf = self.font_small.render(slow_text, True, (0, 255, 255))
            slow_rect = slow_surf.get_rect(bottomright=(screen_width - 20, screen_height - 20))
            
            # Efeito piscante sutil
            alpha = int((math.sin(pygame.time.get_ticks() * 0.01) + 1) * 100)
            slow_surf.set_alpha(alpha)
            
            screen.blit(slow_surf, slow_rect)
    
    def get_combo(self):
        """Obter combo atual"""
        return self.combo
    
    def get_multiplier(self):
        """Obter multiplicador atual"""
        return self.multiplier
    
    def get_max_combo(self):
        """Obter combo máximo"""
        return self.max_combo
