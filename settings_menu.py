import pygame
import math
import colorsys


class SettingsMenu:
    """Menu de configurações avançadas"""
    
    def __init__(self, width, height, save_system):
        self.width = width
        self.height = height
        self.save_system = save_system
        
        # Fontes
        self.title_font = pygame.font.Font(None, 72)
        self.option_font = pygame.font.Font(None, 40)
        self.value_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Estado
        self.selected_option = 0
        self.animation_frame = 0
        self.particles = []
        
        # Resoluções disponíveis
        self.resolutions = [
            (800, 600),
            (1024, 768),
            (1280, 720),
            (1366, 768),
            (1920, 1080)
        ]
        
        # Opções de configuração
        self.options = [
            {
                'id': 'music_volume',
                'name': 'Volume Música',
                'type': 'slider',
                'min': 0.0,
                'max': 1.0,
                'step': 0.05,
                'format': lambda v: f"{int(v * 100)}%"
            },
            {
                'id': 'sfx_volume',
                'name': 'Volume SFX',
                'type': 'slider',
                'min': 0.0,
                'max': 1.0,
                'step': 0.05,
                'format': lambda v: f"{int(v * 100)}%"
            },
            {
                'id': 'resolution',
                'name': 'Resolução',
                'type': 'list',
                'values': self.resolutions,
                'format': lambda v: f"{v[0]}x{v[1]}"
            },
            {
                'id': 'fullscreen',
                'name': 'Tela Cheia',
                'type': 'toggle',
                'format': lambda v: "SIM" if v else "NÃO"
            },
            {
                'id': 'show_fps',
                'name': 'Mostrar FPS',
                'type': 'toggle',
                'format': lambda v: "SIM" if v else "NÃO"
            },
            {
                'id': 'particle_quality',
                'name': 'Qualidade Partículas',
                'type': 'list',
                'values': ['baixa', 'média', 'alta', 'ultra'],
                'format': lambda v: v.upper()
            },
            {
                'id': 'screen_shake',
                'name': 'Screen Shake',
                'type': 'toggle',
                'format': lambda v: "SIM" if v else "NÃO"
            }
        ]
        
        # Carregar configurações atuais
        self.load_settings()
    
    def load_settings(self):
        """Carregar configurações do save system"""
        self.current_values = {}
        
        for option in self.options:
            option_id = option['id']
            
            if option_id == 'resolution':
                # Resolução especial - armazenada como lista
                res = self.save_system.get_setting('resolution', [800, 600])
                self.current_values[option_id] = tuple(res)
            elif option_id == 'particle_quality':
                # Qualidade das partículas (novo)
                self.current_values[option_id] = self.save_system.get_setting(option_id, 'alta')
            elif option_id == 'screen_shake':
                # Screen shake (novo)
                self.current_values[option_id] = self.save_system.get_setting(option_id, True)
            else:
                # Carregar valor padrão
                default = {
                    'music_volume': 0.3,
                    'sfx_volume': 0.5,
                    'fullscreen': False,
                    'show_fps': False
                }.get(option_id, False)
                
                self.current_values[option_id] = self.save_system.get_setting(option_id, default)
    
    def save_settings(self):
        """Salvar todas as configurações"""
        for option_id, value in self.current_values.items():
            self.save_system.update_setting(option_id, value)
    
    def get_current_value(self, option):
        """Obter valor atual de uma opção"""
        return self.current_values.get(option['id'])
    
    def modify_value(self, option, direction):
        """Modificar valor de uma opção"""
        option_id = option['id']
        current = self.get_current_value(option)
        
        if option['type'] == 'slider':
            # Slider numérico
            new_value = current + (option['step'] * direction)
            new_value = max(option['min'], min(option['max'], new_value))
            self.current_values[option_id] = round(new_value, 2)
            
        elif option['type'] == 'toggle':
            # Toggle booleano
            self.current_values[option_id] = not current
            
        elif option['type'] == 'list':
            # Lista de valores
            values = option['values']
            current_index = values.index(current) if current in values else 0
            new_index = (current_index + direction) % len(values)
            self.current_values[option_id] = values[new_index]
        
        # Salvar automaticamente
        self.save_settings()
        
        # Aplicar mudanças imediatas (se necessário)
        self.apply_setting(option_id)
    
    def apply_setting(self, option_id):
        """Aplicar configuração imediatamente"""
        value = self.current_values[option_id]
        
        # Aqui você pode adicionar lógica para aplicar certas configurações imediatamente
        # Por exemplo, mudar volume, fullscreen, etc.
        pass
    
    def handle_input(self, event):
        """Processar entrada do usuário"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                return 'navigate'
            
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                return 'navigate'
            
            elif event.key == pygame.K_LEFT:
                option = self.options[self.selected_option]
                self.modify_value(option, -1)
                return 'change'
            
            elif event.key == pygame.K_RIGHT:
                option = self.options[self.selected_option]
                self.modify_value(option, 1)
                return 'change'
            
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                return 'exit'
        
        return None
    
    def update(self, dt=0.0):
        """Atualizar animações"""
        self.animation_frame += 0.05
        
        # Atualizar partículas (se houver)
        for particle in self.particles[:]:
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def get_psychedelic_color(self, hue_offset=0.0, brightness=1.0):
        """Gerar cor psicodélica animada"""
        hue = (hue_offset + self.animation_frame * 0.02) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 1.0, brightness)
        return tuple(int(c * 255) for c in rgb)
    
    def draw(self, screen):
        """Desenhar menu de configurações"""
        # Fundo escuro com gradiente
        for y in range(0, self.height, 4):
            alpha = y / self.height
            color = self.get_psychedelic_color(alpha * 0.3, 0.1 + alpha * 0.1)
            pygame.draw.line(screen, color, (0, y), (self.width, y), 4)
        
        # Título
        title_color = self.get_psychedelic_color(0.0, 1.0)
        title = self.title_font.render("⚙️ CONFIGURAÇÕES", True, title_color)
        title_rect = title.get_rect(center=(self.width // 2, 60))
        screen.blit(title, title_rect)
        
        # Desenhar opções
        start_y = 150
        spacing = 70
        
        for i, option in enumerate(self.options):
            y_pos = start_y + i * spacing
            is_selected = (i == self.selected_option)
            
            # Background da opção
            if is_selected:
                pulse = math.sin(self.animation_frame * 0.2) * 10 + 10
                bg_width = 700 + int(pulse)
                bg_color = (100, 100, 255, 50)
            else:
                bg_width = 700
                bg_color = (50, 50, 50, 30)
            
            bg_rect = pygame.Rect(
                self.width // 2 - bg_width // 2,
                y_pos - 25,
                bg_width,
                55
            )
            
            # Desenhar background
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(bg_surface, bg_color, bg_surface.get_rect(), border_radius=8)
            screen.blit(bg_surface, bg_rect)
            
            # Borda
            border_color = self.get_psychedelic_color(i * 0.15) if is_selected else (100, 100, 100)
            pygame.draw.rect(screen, border_color, bg_rect, 2, border_radius=8)
            
            # Nome da opção
            name_color = (255, 255, 255) if is_selected else (200, 200, 200)
            name_text = self.option_font.render(option['name'], True, name_color)
            screen.blit(name_text, (bg_rect.x + 30, y_pos - 15))
            
            # Valor atual
            current_value = self.get_current_value(option)
            value_str = option['format'](current_value)
            
            # Indicadores de mudança (← →)
            if is_selected and option['type'] != 'toggle':
                left_arrow = "←"
                right_arrow = "→"
            else:
                left_arrow = " "
                right_arrow = " "
            
            # Desenhar valor com setas
            value_display = f"{left_arrow}  {value_str}  {right_arrow}"
            value_color = self.get_psychedelic_color(0.3) if is_selected else (150, 150, 150)
            value_surface = self.value_font.render(value_display, True, value_color)
            value_rect = value_surface.get_rect(right=bg_rect.right - 30, centery=bg_rect.centery)
            screen.blit(value_surface, value_rect)
            
            # Barra visual para sliders
            if option['type'] == 'slider' and is_selected:
                bar_width = 200
                bar_height = 6
                bar_x = bg_rect.right - bar_width - 30
                bar_y = bg_rect.bottom + 5
                
                # Background da barra
                pygame.draw.rect(screen, (50, 50, 50), 
                               (bar_x, bar_y, bar_width, bar_height), border_radius=3)
                
                # Progresso
                progress = (current_value - option['min']) / (option['max'] - option['min'])
                progress_width = int(bar_width * progress)
                pygame.draw.rect(screen, self.get_psychedelic_color(0.3), 
                               (bar_x, bar_y, progress_width, bar_height), border_radius=3)
        
        # Instruções
        instructions = [
            "↑↓ Navegar  |  ←→ Ajustar  |  ENTER/ESC Voltar"
        ]
        
        inst_y = self.height - 50
        inst_text = self.small_font.render(instructions[0], True, (150, 150, 150))
        inst_rect = inst_text.get_rect(center=(self.width // 2, inst_y))
        screen.blit(inst_text, inst_rect)
        
        # Nota sobre restart
        note_text = self.small_font.render(
            "Algumas configurações requerem reiniciar o jogo", 
            True, (180, 180, 100)
        )
        note_rect = note_text.get_rect(center=(self.width // 2, self.height - 25))
        screen.blit(note_text, note_rect)
