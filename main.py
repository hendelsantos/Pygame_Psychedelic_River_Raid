#!/usr/bin/env python3
"""
Psychedelic River Raid - Um jogo estilo River Raid com gráficos psicodélicos
e geração procedural de níveis.
"""

import pygame
import sys
from game import Game
from menu_system import MenuSystem
from save_system import SaveSystem
from settings_menu import SettingsMenu
from mode_selection_menu import ModeSelectionMenu
from leaderboard_system import LeaderboardSystem, LeaderboardRenderer
from game_modes import GameMode

class GameManager:
    def __init__(self):
        # Inicializar Pygame
        pygame.init()
        
        # Configurações da tela
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Psychedelic River Raid")
        
        # Clock para FPS
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Sistema de save global
        self.save_system = SaveSystem()
        
        # Sistema de leaderboards
        self.leaderboard = LeaderboardSystem()
        self.leaderboard_renderer = LeaderboardRenderer(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        # Estados do jogo
        self.state = "menu"  # menu, mode_select, game, leaderboard, achievements
        
        # Sistemas
        self.menu = MenuSystem(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.mode_menu = ModeSelectionMenu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.game = None
        self.settings_menu = SettingsMenu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.save_system)
        
        # Modo de jogo selecionado
        self.selected_mode = GameMode.ARCADE
        
        # Delta time para animações suaves
        self.last_time = pygame.time.get_ticks()
        self.leaderboard_mode_index = 0
        self.leaderboard_modes = ['global', 'arcade', 'survival', 'boss_rush', 'time_attack']
    
    def handle_events(self):
        """Gerenciar eventos globais"""
        # Se estiver no jogo, não processar eventos aqui
        if self.state == "game" and self.game:
            return
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    # Toggle fullscreen
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    if self.state == "game":
                        self.state = "menu"
                        if self.game:
                            self.game.cleanup()
                            self.game = None
                        if hasattr(self.menu, 'audio'):
                            self.menu.audio.start_background_music()
                            self.menu.apply_volume_setting()
                    elif self.state in ["leaderboard", "achievements", "mode_select"]:
                        self.state = "menu"
                
                # Trocar modo no leaderboard
                if self.state == "leaderboard" and event.key == pygame.K_TAB:
                    self.leaderboard_mode_index = (self.leaderboard_mode_index + 1) % len(self.leaderboard_modes)
            
            # Passar eventos para o sistema atual
            if self.state == "menu":
                result = self.menu.handle_event(event)
                if result:
                    self.handle_menu_result(result)
            elif self.state == "mode_select":
                result = self.mode_menu.handle_event(event)
                if result:
                    self.handle_mode_selection(result)
    
    def handle_menu_result(self, result):
        """Processar resultados do menu"""
        if result == "mode_select":
            self.state = "mode_select"
        elif result == "leaderboard":
            self.state = "leaderboard"
            self.leaderboard_mode_index = 0
        elif result == "achievements":
            self.state = "achievements"
        elif result == "settings":
            self.open_settings_menu()
        elif result == "quit":
            self.running = False
    
    def handle_mode_selection(self, result):
        """Processar seleção de modo"""
        if result == "back":
            self.state = "menu"
        elif isinstance(result, GameMode):
            # Modo selecionado - iniciar jogo
            self.selected_mode = result
            self.start_game(result)
    
    def start_game(self, mode: GameMode):
        """Iniciar jogo com modo específico"""
        self.state = "game"
        self.game = Game(
            self.SCREEN_WIDTH, 
            self.SCREEN_HEIGHT, 
            self.save_system
        )
        
        # TODO: Integrar modo de jogo quando game.py estiver atualizado
        # self.game.set_mode(mode)
        
        # Aplicar configurações de volume
        volume = self.menu.get_volume_setting()
        self.game.audio.set_volume(volume)
    
    def open_settings_menu(self):
        """Abrir menu de configurações"""
        in_settings = True
        
        while in_settings and self.running:
            dt = self.clock.tick(60) / 1000.0
            
            # Processar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    in_settings = False
                    return
                
                action = self.settings_menu.handle_input(event)
                if action == 'exit':
                    in_settings = False
                elif action in ['change', 'navigate']:
                    # Sons opcionais
                    pass
            
            # Atualizar
            self.settings_menu.update(dt)
            
            # Desenhar
            self.settings_menu.draw(self.screen)
            pygame.display.flip()
    
    def update(self):
        """Atualizar lógica do jogo"""
        # Calcular delta time
        current_time = pygame.time.get_ticks()
        dt = (current_time - self.last_time) / 1000.0  # Converter para segundos
        self.last_time = current_time
        
        if self.state == "menu":
            self.menu.update(dt)
        elif self.state == "game" and self.game:
            # O jogo processa seus próprios eventos
            self.game.handle_events()
            self.game.update()
            
            # Verificar se o jogo acabou
            if not self.game.running:
                # Voltar ao menu
                print("🎵 Retornando ao menu - reativando música do menu...")
                self.state = "menu"
                if self.game:
                    self.game.cleanup()
                    self.game = None
                # Reativar música do menu
                if hasattr(self.menu, 'audio'):
                    self.menu.audio.start_background_music()
                    volume = self.menu.get_volume_setting()
                    self.menu.apply_volume_setting()
                    self.game = None
    
    def render(self):
        """Renderizar o frame atual"""
        if self.state == "menu":
            self.menu.draw(self.screen)
        elif self.state == "game" and self.game:
            self.game.render()
        
        pygame.display.flip()
    
    def run(self):
        """Loop principal do jogo"""
        print("🚀 Iniciando Psychedelic River Raid...")
        print("🎮 Sistema de menu profissional ativado!")
        
        while self.running:
            try:
                self.handle_events()
                self.update()
                self.render()
                self.clock.tick(60)  # 60 FPS
            except KeyboardInterrupt:
                print("\n🛑 Jogo interrompido pelo usuário")
                break
            except Exception as e:
                print(f"❌ Erro durante a execução: {e}")
                break
        
        # Cleanup
        print("🧹 Limpando recursos...")
        try:
            if self.game:
                self.game.cleanup()
        except Exception as e:
            print(f"⚠️ Aviso ao limpar jogo: {e}")
        
        try:
            if hasattr(self, 'menu'):
                self.menu.cleanup()
        except Exception as e:
            print(f"⚠️ Aviso ao limpar menu: {e}")
        
        try:
            pygame.quit()
        except Exception as e:
            print(f"⚠️ Aviso ao finalizar pygame: {e}")

def main():
    """Função principal do jogo"""
    try:
        game_manager = GameManager()
        game_manager.run()
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
    finally:
        try:
            pygame.quit()
        except:
            pass  # Ignorar se já foi finalizado
        sys.exit()

if __name__ == "__main__":
    main()