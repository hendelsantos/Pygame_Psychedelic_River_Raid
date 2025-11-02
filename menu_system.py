import pygame
import math
import time
from audio_engine import AudioEngine

class MenuSystem:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_menu = "main"  # main, settings, credits, game
        
        # Configurações de fonte
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 48)
        self.subtitle_font = pygame.font.Font(None, 32)
        
        # Configurações do menu
        self.selected_option = 0
        self.menu_options = ["JOGAR", "CONFIGURAÇÕES", "CRÉDITOS", "SAIR"]
        self.settings_options = ["VOLUME: ", "RESOLUÇÃO: ", "VOLTAR"]
        self.settings_values = ["70%", "800x600"]
        self.settings_selected = 0
        
        # Animações
        self.title_pulse = 0
        self.menu_wave = 0
        self.particle_time = 0
        self.particles = []
        
        # Cores
        self.primary_color = (255, 100, 255)  # Rosa vibrante
        self.secondary_color = (100, 255, 255)  # Ciano
        self.accent_color = (255, 255, 100)  # Amarelo
        self.text_color = (255, 255, 255)
        self.selected_color = (255, 255, 100)
        
        # Sistema de áudio para o menu
        print("🎵 Inicializando áudio do menu...")
        self.audio = AudioEngine()
        self.audio.set_volume(0.25)  # Volume menor para o menu
        
        # Iniciar música de fundo do menu
        print("🎶 Iniciando música no menu...")
        self.audio.start_background_music()
        
        # Background animado
        self.bg_waves = []
        for i in range(5):
            self.bg_waves.append({
                'frequency': 0.02 + i * 0.005,
                'amplitude': 30 + i * 10,
                'speed': 0.03 + i * 0.01,
                'offset': i * 50
            })
    
    def handle_event(self, event):
        """Gerenciar eventos do menu"""
        if self.current_menu == "main":
            return self.handle_main_menu_event(event)
        elif self.current_menu == "settings":
            return self.handle_settings_event(event)
        elif self.current_menu == "credits":
            return self.handle_credits_event(event)
        
        return None
    
    def handle_main_menu_event(self, event):
        """Eventos do menu principal"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected_option == 0:  # JOGAR
                    return "start_game"
                elif self.selected_option == 1:  # CONFIGURAÇÕES
                    self.current_menu = "settings"
                    self.settings_selected = 0
                elif self.selected_option == 2:  # CRÉDITOS
                    self.current_menu = "credits"
                elif self.selected_option == 3:  # SAIR
                    return "quit"
        
        return None
    
    def handle_settings_event(self, event):
        """Eventos do menu de configurações"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.settings_selected = (self.settings_selected - 1) % len(self.settings_options)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.settings_selected = (self.settings_selected + 1) % len(self.settings_options)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if self.settings_selected == 0:  # Volume
                    current_vol = int(self.settings_values[0].replace('%', ''))
                    new_vol = max(0, current_vol - 10)
                    self.settings_values[0] = f"{new_vol}%"
                    # Aplicar volume imediatamente
                    self.apply_volume_setting()
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if self.settings_selected == 0:  # Volume
                    current_vol = int(self.settings_values[0].replace('%', ''))
                    new_vol = min(100, current_vol + 10)
                    self.settings_values[0] = f"{new_vol}%"
                    # Aplicar volume imediatamente
                    self.apply_volume_setting()
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.settings_selected == 2:  # VOLTAR
                    self.current_menu = "main"
                    self.selected_option = 0
            elif event.key == pygame.K_ESCAPE:
                self.current_menu = "main"
                self.selected_option = 0
        
        return None
    
    def handle_credits_event(self, event):
        """Eventos do menu de créditos"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self.current_menu = "main"
                self.selected_option = 0
        
        return None
    
    def update(self, dt):
        """Atualizar animações do menu"""
        self.title_pulse += dt * 3
        self.menu_wave += dt * 2
        self.particle_time += dt
        
        # Atualizar partículas de fundo
        if self.particle_time > 0.1:  # Adicionar partícula a cada 100ms
            center_y = self.height / 2
            offset_vector = pygame.math.Vector2(0, 200).rotate(self.particle_time * 50)
            speed_vector = pygame.math.Vector2(100, 0).rotate(self.particle_time * 20)
            
            self.particles.append({
                'x': self.width + 10,
                'y': center_y + offset_vector.y,
                'speed': speed_vector,
                'life': 3.0,
                'size': 3
            })
            self.particle_time = 0
        
        # Atualizar partículas existentes
        for particle in self.particles[:]:
            particle['x'] -= particle['speed'].x * dt
            particle['y'] += particle['speed'].y * dt
            particle['life'] -= dt
            particle['size'] = max(0, particle['size'] - dt)
            
            if particle['life'] <= 0 or particle['x'] < -10:
                self.particles.remove(particle)
    
    def draw_background(self, screen):
        """Desenhar fundo animado"""
        # Fundo gradiente simples
        for y in range(0, self.height, 4):  # Pular linhas para performance
            color_ratio = y / self.height
            r = int(20 + 30 * math.sin(self.title_pulse + color_ratio * 2))
            g = int(10 + 20 * math.sin(self.title_pulse * 1.5 + color_ratio * 3))
            b = int(40 + 40 * math.sin(self.title_pulse * 0.8 + color_ratio))
            
            # Garantir que as cores estão no range válido
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            pygame.draw.line(screen, (r, g, b), (0, y), (self.width, y), 4)
        
        # Ondas de fundo simplificadas
        for i, wave in enumerate(self.bg_waves[:3]):  # Apenas 3 ondas para performance
            points = []
            for x in range(0, self.width, 10):  # Menos pontos para performance
                y = self.height / 2 + math.sin(x * wave['frequency'] + self.title_pulse * wave['speed']) * wave['amplitude']
                points.append((x, y + wave['offset']))
            
            if len(points) > 1:
                # Usar cores seguras
                color = (100, 50, 150)  # Cor fixa mais segura
                for i in range(len(points) - 1):
                    pygame.draw.line(screen, color, points[i], points[i + 1], 2)
        
        # Partículas
        for particle in self.particles:
            alpha = int(255 * particle['life'] / 3.0)
            size = int(particle['size'])
            if size > 0 and alpha > 0:
                # Cores seguras para as partículas
                r = min(255, max(0, alpha))
                g = min(255, max(0, alpha // 2))
                b = min(255, max(0, alpha))
                color = (r, g, b)
                pygame.draw.circle(screen, color, (int(particle['x']), int(particle['y'])), size)
    
    def draw_main_menu(self, screen):
        """Desenhar menu principal"""
        # Título com animação
        title_scale = 1.0 + 0.1 * math.sin(self.title_pulse)
        title_color = [
            int(255 * (0.5 + 0.5 * math.sin(self.title_pulse))),
            int(255 * (0.5 + 0.5 * math.sin(self.title_pulse + 2))),
            int(255 * (0.5 + 0.5 * math.sin(self.title_pulse + 4)))
        ]
        
        title_text = self.title_font.render("PSYCHEDELIC", True, title_color)
        subtitle_text = self.title_font.render("RIVER RAID", True, self.secondary_color)
        
        # Centralizar título
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 4))
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, self.height // 4 + 80))
        
        screen.blit(title_text, title_rect)
        screen.blit(subtitle_text, subtitle_rect)
        
        # Opções do menu
        menu_start_y = self.height // 2 + 50
        for i, option in enumerate(self.menu_options):
            # Animação de onda para opções
            wave_offset = math.sin(self.menu_wave + i * 0.5) * 10
            
            if i == self.selected_option:
                color = self.selected_color
                # Efeito de brilho na opção selecionada
                glow_text = self.menu_font.render(f"> {option} <", True, color)
            else:
                color = self.text_color
                glow_text = self.menu_font.render(option, True, color)
            
            text_rect = glow_text.get_rect(center=(self.width // 2 + wave_offset, menu_start_y + i * 60))
            screen.blit(glow_text, text_rect)
        
        # Instruções com indicação de música
        instruction_text = self.subtitle_font.render("Use WASD ou Setas para navegar, Enter para selecionar | ♪ Música ativa", True, (150, 150, 150))
        instruction_rect = instruction_text.get_rect(center=(self.width // 2, self.height - 50))
        screen.blit(instruction_text, instruction_rect)
    
    def draw_settings_menu(self, screen):
        """Desenhar menu de configurações"""
        # Título
        title_text = self.menu_font.render("CONFIGURAÇÕES", True, self.primary_color)
        title_rect = title_text.get_rect(center=(self.width // 2, 100))
        screen.blit(title_text, title_rect)
        
        # Opções de configuração
        menu_start_y = 200
        for i, (option, value) in enumerate(zip(self.settings_options[:2], self.settings_values)):
            if i == self.settings_selected:
                color = self.selected_color
                text = f"> {option}{value} <"
            else:
                color = self.text_color
                text = f"{option}{value}"
            
            option_text = self.subtitle_font.render(text, True, color)
            option_rect = option_text.get_rect(center=(self.width // 2, menu_start_y + i * 50))
            screen.blit(option_text, option_rect)
        
        # Botão voltar
        if self.settings_selected == 2:
            color = self.selected_color
            text = "> VOLTAR <"
        else:
            color = self.text_color
            text = "VOLTAR"
        
        back_text = self.subtitle_font.render(text, True, color)
        back_rect = back_text.get_rect(center=(self.width // 2, menu_start_y + 150))
        screen.blit(back_text, back_rect)
        
        # Instruções
        instruction_text = self.subtitle_font.render("Use A/D para ajustar valores, ESC para voltar", True, (150, 150, 150))
        instruction_rect = instruction_text.get_rect(center=(self.width // 2, self.height - 50))
        screen.blit(instruction_text, instruction_rect)
    
    def draw_credits_menu(self, screen):
        """Desenhar menu de créditos"""
        # Título
        title_text = self.menu_font.render("CRÉDITOS", True, self.primary_color)
        title_rect = title_text.get_rect(center=(self.width // 2, 100))
        screen.blit(title_text, title_rect)
        
        # Créditos
        credits = [
            "DESENVOLVIDO POR:",
            "Hendel Santos",
            "",
            "SISTEMA DE ÁUDIO:",
            "Chiptune Engine Procedural",
            "",
            "INSPIRADO EM:",
            "River Raid (Atari 2600)",
            "Galaga, Mega Man, Zelda",
            "",
            "TECNOLOGIA:",
            "Python + Pygame + NumPy",
            "",
            "ANO: 2025"
        ]
        
        start_y = 180
        for i, credit in enumerate(credits):
            if credit.endswith(":"):
                color = self.accent_color
                font = self.subtitle_font
            elif credit == "":
                continue
            elif credit in ["Hendel Santos", "Chiptune Engine Procedural"]:
                color = self.secondary_color
                font = self.subtitle_font
            else:
                color = self.text_color
                font = self.subtitle_font
            
            credit_text = font.render(credit, True, color)
            credit_rect = credit_text.get_rect(center=(self.width // 2, start_y + i * 25))
            screen.blit(credit_text, credit_rect)
        
        # Instruções
        instruction_text = self.subtitle_font.render("Pressione ESC ou Enter para voltar", True, (150, 150, 150))
        instruction_rect = instruction_text.get_rect(center=(self.width // 2, self.height - 50))
        screen.blit(instruction_text, instruction_rect)
    
    def draw(self, screen):
        """Desenhar o menu atual"""
        self.draw_background(screen)
        
        if self.current_menu == "main":
            self.draw_main_menu(screen)
        elif self.current_menu == "settings":
            self.draw_settings_menu(screen)
        elif self.current_menu == "credits":
            self.draw_credits_menu(screen)
    
    def get_volume_setting(self):
        """Obter configuração de volume como float"""
        return int(self.settings_values[0].replace('%', '')) / 100.0
    
    def apply_volume_setting(self):
        """Aplicar configuração de volume ao áudio do menu"""
        volume = self.get_volume_setting()
        self.audio.set_volume(volume * 0.25)  # 25% do volume configurado para o menu
    
    def cleanup(self):
        """Limpar recursos de áudio do menu"""
        if hasattr(self, 'audio'):
            print("🎵 Finalizando áudio do menu...")
            self.audio.cleanup()