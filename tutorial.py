import pygame
import math
import colorsys


class Tutorial:
    """Sistema de tutorial interativo"""
    
    def __init__(self, width, height, save_system):
        self.width = width
        self.height = height
        self.save_system = save_system
        
        # Fontes
        self.title_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # Estado do tutorial
        self.active = False
        self.current_step = 0
        self.step_completed = False
        self.animation_frame = 0
        
        # Passos do tutorial
        self.steps = [
            {
                'title': '🎮 Bem-vindo ao Tutorial!',
                'text': 'Vamos aprender os controles básicos.\nPressione ESPAÇO ou qualquer botão para continuar.',
                'action': 'wait_input',
                'completed': False
            },
            {
                'title': '⬅️➡️ Movimento',
                'text': 'Use as SETAS ou WASD para mover.\nGamepad: Analógico esquerdo ou D-pad.',
                'action': 'move',
                'target': 100,  # Distância total a mover
                'progress': 0,
                'completed': False
            },
            {
                'title': '🔫 Atirar',
                'text': 'Pressione ESPAÇO para atirar.\nGamepad: Botão A ou RT.',
                'action': 'shoot',
                'target': 5,  # Número de tiros
                'progress': 0,
                'completed': False
            },
            {
                'title': '🎯 Destruir Inimigos',
                'text': 'Destrua 3 inimigos de treino!\nEles são lentos e não atiram.',
                'action': 'kill_enemies',
                'target': 3,
                'progress': 0,
                'completed': False
            },
            {
                'title': '💚 Coletar Power-ups',
                'text': 'Colete o power-up verde de vida!\nPower-ups aparecem após matar inimigos.',
                'action': 'collect_powerup',
                'target': 1,
                'progress': 0,
                'completed': False
            },
            {
                'title': '⏸️ Pausar',
                'text': 'Pressione P para pausar.\nGamepad: START.',
                'action': 'pause',
                'target': 1,
                'progress': 0,
                'completed': False
            },
            {
                'title': '🛒 Loja',
                'text': 'Pressione TAB para abrir a loja.\nGamepad: Botão Y.\nCompre upgrades com suas moedas!',
                'action': 'open_shop',
                'target': 1,
                'progress': 0,
                'completed': False
            },
            {
                'title': '✅ Tutorial Completo!',
                'text': 'Você aprendeu tudo!\nBoa sorte na sua jornada.\nPressione ESPAÇO para começar o jogo.',
                'action': 'finish',
                'completed': False
            }
        ]
        
        # Tracking para o passo atual
        self.last_position = None
        self.total_distance_moved = 0
        
    def start(self):
        """Iniciar tutorial"""
        # Verificar se jogador já completou o tutorial
        if self.save_system.get_setting('tutorial_completed', False):
            return False
        
        self.active = True
        self.current_step = 0
        self.reset_step()
        return True
    
    def reset_step(self):
        """Resetar progresso do passo atual"""
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            step['progress'] = 0
            step['completed'] = False
            self.step_completed = False
            self.last_position = None
            self.total_distance_moved = 0
    
    def update(self, dt, player_pos=None, player_input=None):
        """Atualizar tutorial"""
        if not self.active or self.current_step >= len(self.steps):
            return
        
        self.animation_frame += 0.05
        
        step = self.steps[self.current_step]
        
        # Processar ação do passo atual
        if step['action'] == 'wait_input' and player_input:
            if player_input.get('any_key'):
                self.complete_step()
        
        elif step['action'] == 'move' and player_pos:
            # Calcular distância movida
            if self.last_position:
                dx = player_pos[0] - self.last_position[0]
                dy = player_pos[1] - self.last_position[1]
                distance = math.sqrt(dx*dx + dy*dy)
                self.total_distance_moved += distance
                step['progress'] = min(step['target'], self.total_distance_moved)
                
                if step['progress'] >= step['target']:
                    self.complete_step()
            
            self.last_position = player_pos
        
        elif step['action'] == 'shoot' and player_input:
            if player_input.get('shot'):
                step['progress'] = min(step['target'], step['progress'] + 1)
                if step['progress'] >= step['target']:
                    self.complete_step()
        
        elif step['action'] == 'kill_enemies' and player_input:
            if player_input.get('enemy_killed'):
                step['progress'] = min(step['target'], step['progress'] + 1)
                if step['progress'] >= step['target']:
                    self.complete_step()
        
        elif step['action'] == 'collect_powerup' and player_input:
            if player_input.get('powerup_collected'):
                step['progress'] = min(step['target'], step['progress'] + 1)
                if step['progress'] >= step['target']:
                    self.complete_step()
        
        elif step['action'] == 'pause' and player_input:
            if player_input.get('paused'):
                step['progress'] = 1
                self.complete_step()
        
        elif step['action'] == 'open_shop' and player_input:
            if player_input.get('shop_opened'):
                step['progress'] = 1
                self.complete_step()
        
        elif step['action'] == 'finish' and player_input:
            if player_input.get('any_key'):
                self.finish_tutorial()
    
    def complete_step(self):
        """Completar passo atual"""
        if self.current_step < len(self.steps):
            self.steps[self.current_step]['completed'] = True
            self.step_completed = True
            # Aguardar um momento antes de avançar
            pygame.time.delay(500)
            self.next_step()
    
    def next_step(self):
        """Avançar para próximo passo"""
        self.current_step += 1
        if self.current_step < len(self.steps):
            self.reset_step()
    
    def finish_tutorial(self):
        """Finalizar tutorial"""
        self.active = False
        self.save_system.update_setting('tutorial_completed', True)
        print("✅ Tutorial completo!")
    
    def skip_tutorial(self):
        """Pular tutorial"""
        self.active = False
        self.save_system.update_setting('tutorial_completed', True)
        print("⏭️ Tutorial pulado")
    
    def is_active(self):
        """Verificar se tutorial está ativo"""
        return self.active
    
    def get_current_step(self):
        """Obter passo atual"""
        if self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None
    
    def get_progress(self):
        """Obter progresso do tutorial (0.0 a 1.0)"""
        if len(self.steps) == 0:
            return 1.0
        return self.current_step / len(self.steps)
    
    def get_psychedelic_color(self, hue_offset=0.0, brightness=1.0):
        """Gerar cor psicodélica"""
        hue = (hue_offset + self.animation_frame * 0.02) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 1.0, brightness)
        return tuple(int(c * 255) for c in rgb)
    
    def draw(self, screen):
        """Desenhar UI do tutorial"""
        if not self.active or self.current_step >= len(self.steps):
            return
        
        step = self.steps[self.current_step]
        
        # Background semi-transparente
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))
        
        # Caixa de diálogo
        box_width = 700
        box_height = 250
        box_x = (self.width - box_width) // 2
        box_y = 50
        
        # Background da caixa
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(box_surface, (20, 20, 40, 230), 
                        box_surface.get_rect(), border_radius=15)
        screen.blit(box_surface, (box_x, box_y))
        
        # Borda animada
        border_color = self.get_psychedelic_color(0.0, 1.0)
        pygame.draw.rect(screen, border_color, 
                        (box_x, box_y, box_width, box_height), 3, border_radius=15)
        
        # Título
        title_surface = self.title_font.render(step['title'], True, 
                                               self.get_psychedelic_color(0.1))
        title_rect = title_surface.get_rect(centerx=self.width // 2, top=box_y + 20)
        screen.blit(title_surface, title_rect)
        
        # Texto
        text_lines = step['text'].split('\n')
        line_y = box_y + 80
        for line in text_lines:
            text_surface = self.text_font.render(line, True, (220, 220, 220))
            text_rect = text_surface.get_rect(centerx=self.width // 2, top=line_y)
            screen.blit(text_surface, text_rect)
            line_y += 35
        
        # Barra de progresso (se aplicável)
        if 'target' in step and step['target'] > 0:
            bar_width = 600
            bar_height = 20
            bar_x = (self.width - bar_width) // 2
            bar_y = box_y + box_height - 50
            
            # Background
            pygame.draw.rect(screen, (50, 50, 50), 
                           (bar_x, bar_y, bar_width, bar_height), border_radius=10)
            
            # Progresso
            progress_ratio = step['progress'] / step['target']
            progress_width = int(bar_width * progress_ratio)
            progress_color = self.get_psychedelic_color(0.3)
            pygame.draw.rect(screen, progress_color, 
                           (bar_x, bar_y, progress_width, bar_height), border_radius=10)
            
            # Texto do progresso
            progress_text = f"{int(step['progress'])}/{step['target']}"
            progress_surface = self.small_font.render(progress_text, True, (255, 255, 255))
            progress_rect = progress_surface.get_rect(center=(self.width // 2, bar_y + bar_height // 2))
            screen.blit(progress_surface, progress_rect)
        
        # Indicador de passo
        step_text = f"Passo {self.current_step + 1}/{len(self.steps)}"
        step_surface = self.small_font.render(step_text, True, (150, 150, 150))
        step_rect = step_surface.get_rect(center=(self.width // 2, box_y + box_height - 15))
        screen.blit(step_surface, step_rect)
        
        # Botão pular (canto superior direito)
        skip_text = "ESC - Pular Tutorial"
        skip_surface = self.small_font.render(skip_text, True, (180, 180, 180))
        screen.blit(skip_surface, (self.width - 200, 10))
