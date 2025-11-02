import pygame
import math


class GamepadManager:
    """Gerenciador de controles/gamepads"""
    
    def __init__(self):
        # Inicializar módulo de joystick
        pygame.joystick.init()
        
        # Controle conectado
        self.joystick = None
        self.joystick_name = None
        self.connected = False
        
        # Deadzone para analógicos
        self.deadzone = 0.15
        
        # Mapeamento de botões (Xbox/PlayStation padrão)
        self.button_map = {
            'A': 0,          # A (Xbox) / X (PS)
            'B': 1,          # B (Xbox) / Circle (PS)
            'X': 2,          # X (Xbox) / Square (PS)
            'Y': 3,          # Y (Xbox) / Triangle (PS)
            'LB': 4,         # Left Bumper
            'RB': 5,         # Right Bumper
            'BACK': 6,       # Back/Select
            'START': 7,      # Start
            'LS': 8,         # Left Stick Press
            'RS': 9,         # Right Stick Press
        }
        
        # Mapeamento de eixos
        self.axis_map = {
            'LEFT_X': 0,     # Analógico esquerdo X
            'LEFT_Y': 1,     # Analógico esquerdo Y
            'RIGHT_X': 2,    # Analógico direito X (pode ser 3 em alguns controles)
            'RIGHT_Y': 3,    # Analógico direito Y (pode ser 4 em alguns controles)
            'LT': 4,         # Left Trigger (pode ser 2 em alguns)
            'RT': 5,         # Right Trigger (pode ser 5 em alguns)
        }
        
        # Estado de vibração
        self.rumble_support = False
        self.rumble_time = 0
        self.rumble_strength = 0
        
        # Detectar controles
        self.detect_controllers()
    
    def detect_controllers(self):
        """Detectar e conectar ao primeiro controle disponível"""
        joystick_count = pygame.joystick.get_count()
        
        if joystick_count > 0:
            try:
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
                self.joystick_name = self.joystick.get_name()
                self.connected = True
                
                # Verificar suporte a rumble (haptic feedback)
                try:
                    # Pygame 2.0+ suporta rumble
                    if hasattr(self.joystick, 'rumble'):
                        self.rumble_support = True
                except:
                    self.rumble_support = False
                
                print(f"🎮 Controle detectado: {self.joystick_name}")
                print(f"   Botões: {self.joystick.get_numbuttons()}")
                print(f"   Eixos: {self.joystick.get_numaxes()}")
                print(f"   Rumble: {'✓' if self.rumble_support else '✗'}")
                
            except Exception as e:
                print(f"⚠️ Erro ao conectar controle: {e}")
                self.connected = False
        else:
            self.connected = False
    
    def is_connected(self):
        """Verificar se há um controle conectado"""
        return self.connected and self.joystick is not None
    
    def get_button(self, button_name):
        """Verificar se um botão está pressionado"""
        if not self.is_connected():
            return False
        
        try:
            button_id = self.button_map.get(button_name, -1)
            if self.joystick and button_id >= 0 and button_id < self.joystick.get_numbuttons():
                return self.joystick.get_button(button_id)
        except:
            pass
        
        return False
    
    def get_axis(self, axis_name):
        """Obter valor de um eixo analógico"""
        if not self.is_connected():
            return 0.0
        
        try:
            axis_id = self.axis_map.get(axis_name, -1)
            if self.joystick and axis_id >= 0 and axis_id < self.joystick.get_numaxes():
                value = self.joystick.get_axis(axis_id)
                
                # Aplicar deadzone
                if abs(value) < self.deadzone:
                    return 0.0
                
                return value
        except:
            pass
        
        return 0.0
    
    def get_dpad(self):
        """Obter estado do D-pad (retorna tupla (x, y))"""
        if not self.is_connected():
            return (0, 0)
        
        try:
            if self.joystick and self.joystick.get_numhats() > 0:
                return self.joystick.get_hat(0)
        except:
            pass
        
        return (0, 0)
    
    def rumble(self, low_frequency=0.5, high_frequency=0.5, duration=200):
        """
        Ativar vibração do controle
        
        Args:
            low_frequency: Intensidade do motor de baixa frequência (0.0 a 1.0)
            high_frequency: Intensidade do motor de alta frequência (0.0 a 1.0)
            duration: Duração em milissegundos
        """
        if not self.is_connected() or not self.rumble_support:
            return
        
        try:
            if self.joystick and hasattr(self.joystick, 'rumble'):
                self.joystick.rumble(low_frequency, high_frequency, duration)
                self.rumble_time = duration
                self.rumble_strength = max(low_frequency, high_frequency)
        except Exception as e:
            pass
    
    def stop_rumble(self):
        """Parar vibração"""
        if self.is_connected() and self.rumble_support:
            try:
                if self.joystick and hasattr(self.joystick, 'stop_rumble'):
                    self.joystick.stop_rumble()
            except:
                pass
        
        self.rumble_time = 0
        self.rumble_strength = 0
    
    def update(self, dt):
        """Atualizar estado do gamepad"""
        # Atualizar contador de rumble
        if self.rumble_time > 0:
            self.rumble_time -= dt * 1000
            if self.rumble_time <= 0:
                self.stop_rumble()
    
    def get_movement_vector(self):
        """
        Obter vetor de movimento do analógico esquerdo ou D-pad
        Retorna: (x, y) normalizado
        """
        # Tentar analógico esquerdo primeiro
        x = self.get_axis('LEFT_X')
        y = self.get_axis('LEFT_Y')
        
        # Se analógico não está sendo usado, tentar D-pad
        if abs(x) < 0.01 and abs(y) < 0.01:
            dpad = self.get_dpad()
            x = float(dpad[0])
            y = float(dpad[1])
        
        # Normalizar se necessário
        magnitude = math.sqrt(x*x + y*y)
        if magnitude > 1.0:
            x /= magnitude
            y /= magnitude
        
        return (x, y)
    
    def is_shooting(self):
        """Verificar se está atirando (A, RT ou RB)"""
        return (self.get_button('A') or 
                self.get_axis('RT') > 0.5 or 
                self.get_button('RB'))
    
    def is_pause_pressed(self):
        """Verificar se botão de pausa foi pressionado"""
        return self.get_button('START')
    
    def is_menu_pressed(self):
        """Verificar se botão de menu foi pressionado"""
        return self.get_button('BACK')
    
    def is_shop_pressed(self):
        """Verificar se botão de loja foi pressionado"""
        return self.get_button('Y')
    
    def get_menu_navigation(self):
        """
        Obter navegação de menu
        Retorna: 'up', 'down', 'left', 'right', 'select', 'back' ou None
        """
        # D-pad ou analógico esquerdo
        dpad = self.get_dpad()
        left_y = self.get_axis('LEFT_Y')
        left_x = self.get_axis('LEFT_X')
        
        # Priorizar D-pad
        if dpad[1] == -1 or left_y < -0.5:
            return 'up'
        elif dpad[1] == 1 or left_y > 0.5:
            return 'down'
        elif dpad[0] == -1 or left_x < -0.5:
            return 'left'
        elif dpad[0] == 1 or left_x > 0.5:
            return 'right'
        
        # Botões
        if self.get_button('A') or self.get_button('START'):
            return 'select'
        elif self.get_button('B') or self.get_button('BACK'):
            return 'back'
        
        return None
    
    def get_info(self):
        """Obter informações do controle"""
        if not self.is_connected():
            return {
                'connected': False,
                'name': 'Nenhum controle detectado',
                'buttons': 0,
                'axes': 0,
                'rumble': False
            }
        
        return {
            'connected': True,
            'name': self.joystick_name,
            'buttons': self.joystick.get_numbuttons() if self.joystick else 0,
            'axes': self.joystick.get_numaxes() if self.joystick else 0,
            'hats': self.joystick.get_numhats() if self.joystick else 0,
            'rumble': self.rumble_support
        }
    
    def cleanup(self):
        """Limpar recursos do controle"""
        if self.joystick:
            try:
                self.stop_rumble()
                self.joystick.quit()
            except:
                pass
        
        self.joystick = None
        self.connected = False
