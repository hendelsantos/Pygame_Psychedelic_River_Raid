import pygame
import math
import colorsys

class GameOverScreen:
    def __init__(self, width, height, save_system):
        self.width = width
        self.height = height
        self.save_system = save_system
        
        # Fontes
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 96)
        self.large_font = pygame.font.Font(None, 64)
        self.medium_font = pygame.font.Font(None, 42)
        self.small_font = pygame.font.Font(None, 32)
        
        # Cores
        self.bg_color = (10, 10, 20)
        self.text_color = (255, 255, 255)
        self.accent_color = (255, 200, 100)
        self.high_score_color = (255, 215, 0)
        
        # Animações
        self.alpha = 0
        self.fade_speed = 5
        self.pulse = 0
        self.star_particles = []
        
        # Estado
        self.selected_option = 0
        self.options = ["JOGAR NOVAMENTE", "HIGH SCORES", "MENU PRINCIPAL"]
        self.show_high_scores = False
        self.is_new_high_score = False
        self.ranking_position = None
        self.player_name = ""
        self.entering_name = False
        
        # Estatísticas da partida
        self.game_stats = {}
        
        # Criar partículas de fundo
        self.create_background_particles()
    
    def create_background_particles(self):
        """Criar partículas de estrelas para o fundo"""
        import random
        for _ in range(50):
            self.star_particles.append({
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'speed': random.uniform(0.5, 2),
                'size': random.randint(1, 3),
                'brightness': random.uniform(0.3, 1.0)
            })
    
    def reset(self, score, level, kills, powerups, time_played):
        """Resetar tela de game over com novos dados"""
        self.alpha = 0
        self.pulse = 0
        self.show_high_scores = False
        self.selected_option = 0
        self.entering_name = False
        self.player_name = ""
        
        # Salvar estatísticas da partida
        self.game_stats = {
            'score': score,
            'level': level,
            'kills': kills,
            'powerups': powerups,
            'time_played': time_played
        }
        
        # Verificar se é high score
        self.is_new_high_score = self.save_system.is_high_score(score)
        
        if self.is_new_high_score:
            self.entering_name = True
            self.player_name = "PLAYER"
        
        # Atualizar estatísticas globais
        self.save_system.update_stats(
            total_games_played=1,
            total_enemies_killed=kills,
            total_powerups_collected=powerups,
            total_time_played=time_played
        )
        
        if level > self.save_system.get_stat('highest_level_reached'):
            self.save_system.update_stats(highest_level_reached=level)
    
    def handle_event(self, event):
        """Processar eventos"""
        if self.entering_name:
            # Entrada de nome para high score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Confirmar nome
                    self.ranking_position = self.save_system.add_high_score(
                        self.game_stats['score'],
                        self.game_stats['level'],
                        self.player_name if self.player_name else "PLAYER"
                    )
                    self.entering_name = False
                    self.show_high_scores = True
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    self.entering_name = False
                elif len(self.player_name) < 12 and event.unicode.isprintable():
                    self.player_name += event.unicode.upper()
        
        elif self.show_high_scores:
            # Navegação no high score
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE]:
                    self.show_high_scores = False
        
        else:
            # Navegação no menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return self.get_selected_action()
        
        return None
    
    def get_selected_action(self):
        """Retornar ação selecionada"""
        if self.selected_option == 0:
            return "retry"
        elif self.selected_option == 1:
            self.show_high_scores = True
            return None
        elif self.selected_option == 2:
            return "menu"
        return None
    
    def update(self, dt):
        """Atualizar animações"""
        # Fade in
        if self.alpha < 255:
            self.alpha = min(255, self.alpha + self.fade_speed)
        
        # Pulso
        self.pulse += dt * 3
        
        # Atualizar partículas de fundo
        for particle in self.star_particles:
            particle['y'] += particle['speed']
            if particle['y'] > self.height:
                particle['y'] = 0
                particle['x'] = pygame.time.get_ticks() % self.width
    
    def draw(self, screen):
        """Desenhar tela de game over"""
        # Fundo escuro com fade
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill(self.bg_color)
        overlay.set_alpha(min(200, self.alpha))
        screen.blit(overlay, (0, 0))
        
        # Partículas de fundo
        self.draw_background_particles(screen)
        
        if self.entering_name:
            self.draw_name_entry(screen)
        elif self.show_high_scores:
            self.draw_high_scores(screen)
        else:
            self.draw_game_over_screen(screen)
    
    def draw_background_particles(self, screen):
        """Desenhar partículas de estrelas"""
        for particle in self.star_particles:
            brightness = int(255 * particle['brightness'] * (self.alpha / 255))
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
    
    def draw_game_over_screen(self, screen):
        """Desenhar tela principal de game over"""
        center_x = self.width // 2
        
        # Título "GAME OVER" com efeito
        title_text = "GAME OVER"
        pulse_scale = 1.0 + 0.1 * math.sin(self.pulse)
        
        for offset in [(4, 4), (-4, -4), (4, -4), (-4, 4)]:
            shadow = self.title_font.render(title_text, True, (100, 0, 0))
            shadow.set_alpha(int(100 * (self.alpha / 255)))
            shadow_rect = shadow.get_rect(center=(center_x + offset[0], 100 + offset[1]))
            screen.blit(shadow, shadow_rect)
        
        title = self.title_font.render(title_text, True, (255, 50, 50))
        title.set_alpha(self.alpha)
        title_rect = title.get_rect(center=(center_x, 100))
        screen.blit(title, title_rect)
        
        # Estatísticas da partida
        y_offset = 200
        stats = [
            ("PONTUAÇÃO", f"{self.game_stats.get('score', 0):,}"),
            ("NÍVEL ALCANÇADO", str(self.game_stats.get('level', 0))),
            ("INIMIGOS ELIMINADOS", str(self.game_stats.get('kills', 0))),
            ("POWER-UPS COLETADOS", str(self.game_stats.get('powerups', 0)))
        ]
        
        for label, value in stats:
            # Label
            label_surf = self.small_font.render(label, True, self.text_color)
            label_surf.set_alpha(self.alpha)
            label_rect = label_surf.get_rect(midright=(center_x - 20, y_offset))
            screen.blit(label_surf, label_rect)
            
            # Valor
            value_surf = self.medium_font.render(value, True, self.accent_color)
            value_surf.set_alpha(self.alpha)
            value_rect = value_surf.get_rect(midleft=(center_x + 20, y_offset))
            screen.blit(value_surf, value_rect)
            
            y_offset += 50
        
        # High score
        if self.is_new_high_score:
            hs_text = "🏆 NOVO HIGH SCORE! 🏆"
            pulse_color = self.get_pulse_color()
            hs_surf = self.large_font.render(hs_text, True, pulse_color)
            hs_surf.set_alpha(self.alpha)
            hs_rect = hs_surf.get_rect(center=(center_x, y_offset + 30))
            screen.blit(hs_surf, hs_rect)
        
        # Menu de opções
        menu_y = self.height - 250
        for i, option in enumerate(self.options):
            is_selected = (i == self.selected_option)
            
            if is_selected:
                color = self.get_pulse_color()
                prefix = "> "
                suffix = " <"
            else:
                color = self.text_color
                prefix = "  "
                suffix = "  "
            
            option_text = prefix + option + suffix
            option_surf = self.medium_font.render(option_text, True, color)
            option_surf.set_alpha(self.alpha)
            option_rect = option_surf.get_rect(center=(center_x, menu_y + i * 60))
            screen.blit(option_surf, option_rect)
    
    def draw_name_entry(self, screen):
        """Desenhar tela de entrada de nome"""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Título
        title = self.large_font.render("NOVO HIGH SCORE!", True, self.high_score_color)
        title.set_alpha(self.alpha)
        title_rect = title.get_rect(center=(center_x, center_y - 100))
        screen.blit(title, title_rect)
        
        # Instruções
        instruction = self.small_font.render("Digite seu nome:", True, self.text_color)
        instruction.set_alpha(self.alpha)
        inst_rect = instruction.get_rect(center=(center_x, center_y - 30))
        screen.blit(instruction, inst_rect)
        
        # Campo de nome
        name_bg = pygame.Rect(center_x - 200, center_y + 20, 400, 60)
        pygame.draw.rect(screen, (40, 40, 60), name_bg)
        pygame.draw.rect(screen, self.get_pulse_color(), name_bg, 3)
        
        name_text = self.player_name + ("|" if int(self.pulse * 2) % 2 else " ")
        name_surf = self.large_font.render(name_text, True, self.text_color)
        name_rect = name_surf.get_rect(center=(center_x, center_y + 50))
        screen.blit(name_surf, name_rect)
        
        # Dica
        hint = self.small_font.render("Pressione ENTER para confirmar", True, self.accent_color)
        hint.set_alpha(int(self.alpha * 0.7))
        hint_rect = hint.get_rect(center=(center_x, center_y + 120))
        screen.blit(hint, hint_rect)
    
    def draw_high_scores(self, screen):
        """Desenhar tabela de high scores"""
        center_x = self.width // 2
        
        # Título
        title = self.title_font.render("HIGH SCORES", True, self.high_score_color)
        title.set_alpha(self.alpha)
        title_rect = title.get_rect(center=(center_x, 80))
        screen.blit(title, title_rect)
        
        # Tabela
        high_scores = self.save_system.get_high_scores()
        start_y = 180
        
        if not high_scores:
            no_scores = self.medium_font.render("Nenhuma pontuação ainda!", True, self.text_color)
            no_scores.set_alpha(self.alpha)
            no_rect = no_scores.get_rect(center=(center_x, start_y + 100))
            screen.blit(no_scores, no_rect)
        else:
            for i, entry in enumerate(high_scores):
                y_pos = start_y + i * 45
                
                # Destacar posição do jogador atual
                is_current = (self.ranking_position == i + 1)
                color = self.get_pulse_color() if is_current else self.text_color
                
                # Posição
                pos_text = f"#{i+1}"
                pos_surf = self.medium_font.render(pos_text, True, color)
                pos_surf.set_alpha(self.alpha)
                screen.blit(pos_surf, (center_x - 300, y_pos))
                
                # Nome
                name_surf = self.medium_font.render(entry['player_name'], True, color)
                name_surf.set_alpha(self.alpha)
                screen.blit(name_surf, (center_x - 220, y_pos))
                
                # Pontuação
                score_surf = self.medium_font.render(f"{entry['score']:,}", True, self.accent_color if not is_current else color)
                score_surf.set_alpha(self.alpha)
                score_rect = score_surf.get_rect(right=center_x + 150, centery=y_pos + 15)
                screen.blit(score_surf, score_rect)
                
                # Nível
                level_surf = self.small_font.render(f"Nv.{entry['level']}", True, color)
                level_surf.set_alpha(int(self.alpha * 0.7))
                screen.blit(level_surf, (center_x + 170, y_pos))
        
        # Instruções
        hint = self.small_font.render("Pressione qualquer tecla para continuar", True, self.accent_color)
        hint.set_alpha(int(self.alpha * 0.7 * (0.5 + 0.5 * math.sin(self.pulse * 2))))
        hint_rect = hint.get_rect(center=(center_x, self.height - 50))
        screen.blit(hint, hint_rect)
    
    def get_pulse_color(self):
        """Obter cor pulsante"""
        hue = (pygame.time.get_ticks() % 3000) / 3000
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        return tuple(int(c * 255) for c in rgb)
