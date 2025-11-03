import pygame
import math
import random
import colorsys
import time
from player import Player
from enemy import Enemy
from bullet import Bullet
from boss import Boss
from level_generator import LevelGenerator
from effects import PsychedelicEffects
from collision import CollisionManager
from audio_engine import AudioEngine
from professional_hud import ProfessionalHUD
from save_system import SaveSystem
from game_over_screen import GameOverScreen
from shop import Shop
from gamepad_manager import GamepadManager
from progression_system import ProgressionSystem
from achievement_system import AchievementSystem
from daily_mission_system import DailyMissionSystem
from combo_system import ComboSystem
from skin_system import SkinSystem
from game_modes import GameMode, GameModeManager
from boss_types import BossType, BossConfig
from scenario_system import ScenarioType, ScenarioRenderer
from name_input import NameInputDialog

class Game:
    def __init__(self, width, height, save_system=None, mode=GameMode.ARCADE, leaderboard=None):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Psychedelic River Raid")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Sistema de save
        self.save_system = save_system if save_system else SaveSystem()
        
        # Sistema de modo de jogo
        self.mode_manager = GameModeManager()
        self.mode_manager.set_mode(mode)
        self.leaderboard = leaderboard
        
        # Estatísticas da partida
        self.score = 0
        self.level = 1
        self.game_speed = 2
        self.enemies_killed = 0
        self.powerups_collected = 0
        self.game_start_time = time.time()
        self.coins_earned_this_game = 0  # Moedas ganhas nesta partida
        
        # Inicializar sistema de áudio (sem print)
        self.audio = AudioEngine()
        
        # Carregar configurações de volume
        music_volume = self.save_system.get_setting('music_volume', 0.3)
        self.audio.set_volume(music_volume)
        
        # Inicializar componentes do jogo
        self.player = Player(width // 2, height - 100)
        
        # Aplicar vidas iniciais baseado no modo
        self.player.max_health = self.mode_manager.get_starting_lives() * 100
        self.player.health = self.player.max_health
        
        self.level_generator = LevelGenerator(width, height)
        self.effects = PsychedelicEffects(width, height)
        self.collision_manager = CollisionManager()
        self.hud = ProfessionalHUD(width, height)
        self.game_over_screen = GameOverScreen(width, height, self.save_system)
        self.shop = Shop(width, height, self.save_system)
        self.gamepad = GamepadManager()
        
        # Sistema de cenários dinâmicos
        self.scenario_renderer = ScenarioRenderer(width, height)
        
        # Sistemas de progressão (sem print)
        self.progression = ProgressionSystem(self.save_system)
        self.achievements = AchievementSystem(self.save_system)
        self.daily_missions = DailyMissionSystem(self.save_system)
        self.combo = ComboSystem()
        self.skin_system = SkinSystem(self.save_system)
        
        # Verificar desbloqueios de skins baseado no nível atual
        self.skin_system.check_unlocks(
            self.progression.player_level,
            self.progression.prestige_level
        )
        
        # Estatísticas da sessão (para missões e conquistas)
        self.session_stats = {
            'kills': 0,
            'bosses': 0,
            'powerups': 0,
            'coins': 0,
            'time': 0,
            'level': 0,
            'shots_fired': 0,
            'shots_hit': 0
        }
        
        # Grupos de sprites
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.boss = None  # Boss atual (se houver)
        self.boss_active = False
        
        # Sistema de partículas
        self.particles = []
        self.explosion_particles = []  # Partículas de explosões espetaculares
        
        # ⚛️ SISTEMA DE BOMBA ATÔMICA
        self.atomic_bombs = 0  # Número de bombas disponíveis (máximo 2)
        self.max_atomic_bombs = 2  # Limite máximo
        self.atomic_bomb_active = False  # Se uma bomba está sendo disparada
        self.atomic_bomb_y = 0  # Posição Y da bomba
        self.atomic_bomb_x = 0  # Posição X da bomba
        self.last_b_press_time = 0  # Tempo do último B pressionado (para duplo B)
        self.double_b_threshold = 0.3  # 300ms para detectar duplo B
        
        # Timer para spawn de inimigos - ajustado pelo modo
        self.enemy_spawn_timer = 0
        base_spawn = 80
        spawn_multiplier = self.mode_manager.get_enemy_spawn_rate()
        self.enemy_spawn_interval = int(base_spawn / spawn_multiplier)
        
        # Cores psicodélicas
        self.color_shift = 0
        
        # Estado do jogo
        self.paused = False
        self.lives = self.mode_manager.get_starting_lives()
        self.is_game_over = False
        self.game_over_timer = 0
        
        # Iniciar música de fundo (sem print)
        self.audio.start_background_music()
        
    def handle_events(self):
        """Gerenciar eventos do jogo"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_TAB or event.key == pygame.K_s:
                    # Abrir loja (se permitido no modo)
                    if self.mode_manager.is_shop_allowed():
                        was_paused = self.paused
                        self.paused = True
                        result = self.open_shop()
                        if result == "continue":
                            self.paused = was_paused
                            # Aplicar upgrades após sair da loja
                            self.apply_upgrades_to_player()
                elif event.key == pygame.K_p:
                    # Pausar/despausar jogo
                    self.paused = not self.paused
                    # Mostrar dicas de controle quando pausar
                    if self.paused:
                        self.hud.force_show_controls(True)
                elif event.key == pygame.K_b:
                    # ⚛️ DISPARAR BOMBA ATÔMICA
                    if self.atomic_bombs > 0 and not self.atomic_bomb_active:
                        self.atomic_bombs -= 1
                        self.atomic_bomb_active = True
                        self.atomic_bomb_x = self.player.x
                        self.atomic_bomb_y = self.player.y
                        self.audio.play_sound('powerup')
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    # Aumentar volume em incrementos menores
                    new_volume = min(1.0, self.audio.volume + 0.05)
                    self.audio.set_volume(new_volume)
                elif event.key == pygame.K_MINUS:
                    new_volume = max(0.0, self.audio.volume - 0.05)
                    self.audio.set_volume(new_volume)
                elif event.key == pygame.K_m:
                    if self.audio.volume > 0:
                        self.audio.set_volume(0.0)
                    else:
                        self.audio.set_volume(0.3)
        
        # Botões do gamepad (detectar single press)
        if self.gamepad.is_connected():
            if self.gamepad.is_pause_pressed():
                self.paused = not self.paused
                if self.paused:
                    self.hud.force_show_controls(True)
                pygame.time.delay(200)  # Debounce
            
            if self.gamepad.is_shop_pressed():
                was_paused = self.paused
                self.paused = True
                result = self.open_shop()
                if result == "continue":
                    self.paused = was_paused
                    self.apply_upgrades_to_player()
                pygame.time.delay(200)  # Debounce
    
    def update(self):
        """Atualizar lógica do jogo"""
        # Não atualizar se estiver pausado
        if self.paused:
            return
        
        # Atualizar teclas pressionadas
        keys = pygame.key.get_pressed()
        
        # Atualizar gamepad
        self.gamepad.update(1/60)
        
        # Processar input (teclado + gamepad)
        self.process_player_input(keys)
        
        # Atualizar level generator
        self.level_generator.update(self.game_speed)
        
        # Atualizar projéteis
        self.bullets.update()
        self.enemy_bullets.update()
        
        # Remover projéteis que saíram da tela
        for bullet in self.bullets:
            if bullet.rect.bottom < 0:
                bullet.kill()
        
        for bullet in self.enemy_bullets:
            if bullet.rect.top > self.height:
                bullet.kill()
        
        # Sistema de Boss
        if self.boss_active and self.boss:
            # Atualizar boss
            self.boss.update(self.width, self.height)
            
            # Boss atira
            if random.randint(1, 30) == 1:
                self.boss.shoot(self.enemy_bullets)
            
            # Verificar se boss foi derrotado
            if self.boss.is_dead():
                self.defeat_boss()
        else:
            # Spawn de inimigos normais (apenas se não houver boss)
            self.enemy_spawn_timer += 1
            if self.enemy_spawn_timer >= self.enemy_spawn_interval:
                # Spawnar MAIS inimigos baseado no nível - MUITO MAIS AGRESSIVO!
                enemies_to_spawn = 2 + (self.level // 2)  # Era 1 + level//3, agora DOBRO!
                for _ in range(enemies_to_spawn):
                    self.spawn_enemy()
                
                self.enemy_spawn_timer = 0
                
                # Aumentar dificuldade AINDA MAIS gradualmente (spawn MUITO mais rápido)
                # Limite mínimo ainda mais agressivo!
                min_interval = max(10, 50 - (self.level * 3))  # Era 15 e 60, agora MUITO mais rápido!
                if self.enemy_spawn_interval > min_interval:
                    self.enemy_spawn_interval -= 0.8  # Era 0.5, agora reduz mais rápido!
        
        # Atualizar inimigos
        for enemy in self.enemies:
            enemy.update(self.game_speed)
            # Inimigos atiram ocasionalmente
            if random.randint(1, 100) == 1:
                enemy.shoot(self.enemy_bullets)
            
            # Remover inimigos que saíram da tela
            if enemy.rect.top > self.height:
                enemy.kill()
        
        # Verificar colisões
        self.check_collisions()
        
        # ⚛️ ATUALIZAR MÍSSIL ATÔMICO
        if self.atomic_bomb_active:
            # Míssil sobe DEVAGAR até o topo
            self.atomic_bomb_y -= 1.5  # Velocidade bem lenta para ser visível
            
            # Quando chega NO TOPO (antes de sair da tela), EXPLODE AUTOMATICAMENTE!
            if self.atomic_bomb_y <= 30:  # No topo da tela, ainda visível
                self.trigger_atomic_explosion()
                self.atomic_bomb_active = False
        
        # Atualizar efeitos visuais
        self.effects.update()
        self.color_shift += 0.02
        
        # � ATUALIZAR CENÁRIO DINÂMICO
        dt = 1/60  # Delta time
        self.scenario_renderer.update(dt)
        
        # 🎮 ATUALIZAR SISTEMAS DE ENGAJAMENTO
        self.combo.update(dt)
        self.skin_system.update_trail((self.player.x, self.player.y))
        
        # Atualizar tempo da sessão
        self.session_stats['time'] = int(time.time() - self.game_start_time)
        self.session_stats['level'] = self.level
        self.session_stats['coins'] = self.coins_earned_this_game
        
        # Verificar missões diárias
        self.daily_missions.check_mission_completion(self.session_stats)
        
        # Atualizar partículas normais e explosões espetaculares
        self.update_particles()
        self.effects.update_explosion_particles(self.explosion_particles, dt)
        
        # Aumentar pontuação baseada na sobrevivência (com multiplicador)
        self.add_score(1)
        
        # Aumentar nível a cada 5000 pontos
        new_level = (self.score // 5000) + 1
        if new_level > self.level:
            self.level = new_level
            self.game_speed = min(8.0, 2 + (self.level * 0.3))
            self.level_generator.increase_difficulty()
            # Atualizar cenário quando o nível mudar
            from scenario_system import ScenarioConfig
            new_scenario = ScenarioConfig.get_scenario_for_level(self.level)
            self.scenario_renderer.set_scenario(new_scenario)
            
            # Ganhar bomba atômica por fase
            if self.atomic_bombs < self.max_atomic_bombs:
                self.atomic_bombs += 1
            
            # Boss a cada X níveis (baseado no modo)
            boss_freq = self.mode_manager.get_boss_frequency()
            if self.mode_manager.should_spawn_boss(self.level):
                if not self.boss_active:
                    self.spawn_boss()
            
            self.adjust_difficulty_by_level()
    
    def add_score(self, points):
        """Adicionar pontos com multiplicador do modo"""
        multiplier = self.mode_manager.get_score_multiplier()
        self.score += int(points * multiplier)
    
    def process_player_input(self, keys):
        """Processar input do jogador (teclado + gamepad)"""
        # Movimento
        move_x = 0
        move_y = 0
        
        # Teclado
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y += 1
        
        # Gamepad (analógico ou D-pad)
        if self.gamepad.is_connected():
            gp_move = self.gamepad.get_movement_vector()
            move_x += gp_move[0]
            move_y += gp_move[1]
        
        # Normalizar movimento diagonal
        if move_x != 0 and move_y != 0:
            magnitude = math.sqrt(move_x*move_x + move_y*move_y)
            move_x /= magnitude
            move_y /= magnitude
        
        # Aplicar movimento
        self.player.x += move_x * self.player.speed
        self.player.y += move_y * self.player.speed
        
        # Manter dentro da tela
        self.player.x = max(self.player.width // 2, 
                           min(self.width - self.player.width // 2, self.player.x))
        self.player.y = max(self.player.height // 2, 
                           min(self.height - self.player.height // 2, self.player.y))
        
        # Atualizar rect
        self.player.rect.centerx = int(self.player.x)
        self.player.rect.centery = int(self.player.y)
        
        # Atualizar animação e partículas de propulsão da nave
        self.player.animation_frame += 0.2
        self.player.create_thrust_particles()
        self.player.update_thrust_particles()
        
        # Tiro (teclado ou gamepad)
        shooting = (keys[pygame.K_SPACE] or 
                   keys[pygame.K_LCTRL] or 
                   keys[pygame.K_RCTRL] or
                   (self.gamepad.is_connected() and self.gamepad.is_shooting()))
        
        if shooting:
            bullets_before = len(self.bullets)
            self.player.shoot(self.bullets)
            bullets_after = len(self.bullets)
            
            # Rastrear tiros disparados
            if bullets_after > bullets_before:
                self.session_stats['shots_fired'] += (bullets_after - bullets_before)
            
            # Som de tiro (tocar diretamente pelo audio engine)
            if self.player.shoot_cooldown == 0:
                self.audio.play_sound('shoot')
        
        # Atualizar cooldown de tiro
        if self.player.shoot_cooldown > 0:
            self.player.shoot_cooldown -= 1
    
    def spawn_boss(self):
        """Spawnar um boss"""
        
        # Limpar inimigos normais
        self.enemies.empty()
        
        # Escolher tipo de boss baseado no nível usando BossConfig
        boss_type = BossConfig.get_type_for_level(self.level)
        
        # Criar boss com tipo específico
        self.boss = Boss(self.width // 2, -100, boss_type, self.level)
        self.boss_active = True
        
        # Som especial de boss (usar explosão grande)
        self.audio.play_sound('explosion')
    
    def defeat_boss(self):
        """Boss foi derrotado"""
        if not self.boss:
            return
        
        # Pontos pelo boss
        boss_score = self.boss.get_score_value()
        self.add_score(boss_score)
        
        # 🎮 ADICIONAR XP PELO BOSS (200 XP base)
        xp_gain = 200
        leveled_up, levels_gained = self.progression.add_xp(xp_gain)
        if leveled_up:
            pass  # Level up silencioso
        
        # 📊 ESTATÍSTICAS
        self.session_stats['bosses'] += 1
        
        # Bônus de moedas por derrotar boss (50-100 moedas)
        boss_coins = random.randint(150, 300)  # MUITO MAIS MOEDAS!!!
        coin_multiplier = 1.0 + (self.save_system.get_upgrade_level('coin_multiplier') * 0.1)
        boss_coins = int(boss_coins * coin_multiplier)
        self.coins_earned_this_game += boss_coins
        
        # 💥💥💥 EXPLOSÃO FENOMENAL DO BOSS!!!
        
        # Criar MÚLTIPLAS explosões gigantes ao redor do boss
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            offset_x = math.cos(angle) * 50
            offset_y = math.sin(angle) * 50
            
            self.effects.create_giant_explosion(
                self.boss.x + offset_x,
                self.boss.y + offset_y,
                size_multiplier=6.0  # ENORME!!!
            )
        
        # Explosão central GIGANTESCA
        self.effects.create_giant_explosion(
            self.boss.x,
            self.boss.y,
            size_multiplier=15.0  # ABSOLUTAMENTE MASSIVA!!!
        )
        
        # Som de explosão épica
        self.audio.play_sound('explosion')
        self.audio.play_sound('powerup')  # Som adicional
        
        # Partículas extras para o efeito
        for _ in range(100):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 20)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            particle = {
                'x': self.boss.x,
                'y': self.boss.y,
                'vel_x': vel_x,
                'vel_y': vel_y,
                'life': 60,
                'color': (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            }
            self.particles.append(particle)
        
        # Sons de vitória
        self.audio.play_sound('explosion')
        self.audio.play_sound('powerup')
        
        # Vibração intensa ao derrotar boss
        self.gamepad.rumble(1.0, 1.0, 500)
        
        # Resetar boss
        self.boss = None
        self.boss_active = False
        
        # ✅ VERIFICAR SE PRECISA SPAWNAR PRÓXIMO BOSS
        # Caso o jogador derrote um boss e já esteja em múltiplo de 5
        if self.level % 5 == 0:
            # Dar um tempo para o jogador respirar
            pygame.time.wait(3000)
            if not self.boss_active:  # Verificar de novo
                self.spawn_boss()
    
    def adjust_difficulty_by_level(self):
        """Ajustar dificuldade dinamicamente baseado no nível e upgrades do jogador"""
        # Calcular "poder" do jogador baseado nos upgrades
        player_power = 1.0
        player_power += self.save_system.get_upgrade_level('max_health') * 0.1
        player_power += self.save_system.get_upgrade_level('fire_rate') * 0.15
        player_power += self.save_system.get_upgrade_level('bullet_damage') * 0.2
        player_power += self.save_system.get_upgrade_level('speed') * 0.1
        
        # Ajustar spawn rate baseado no poder do jogador e nível
        base_spawn = 120
        level_reduction = self.level * 3
        power_reduction = (player_power - 1.0) * 20  # Mais forte = mais inimigos
        
        self.enemy_spawn_interval = max(15, base_spawn - level_reduction - power_reduction)
        
    
        # Dar power-up de vida ao jogador
        self.player.health = min(self.player.max_health, self.player.health + 50)
    
    def spawn_enemy(self, training=False):
        """Criar um novo inimigo com variedade baseada no nível"""
        x = random.randint(50, self.width - 50)
        y = random.randint(-100, -50)
        
        # Inimigos de treino para o tutorial (fracos e lentos)
        if training:
            enemy_type = 'basic'
            enemy = Enemy(x, y, enemy_type)
            # Fazer inimigo mais lento e fraco
            enemy.speed = 1
            enemy.health = 1
            self.enemies.add(enemy)
            return
        
        # CHANCE DE SPAWNAR INIMIGOS ESPECIAIS (Gigantes e Elites)
        special_roll = random.random()
        
        if self.level >= 3 and special_roll < 0.05:  # 5% chance de GIGANTE
            enemy_type = 'giant'
            x = self.width // 2  # Spawna no centro
        elif self.level >= 5 and special_roll < 0.12:  # 7% chance adicional de ELITE
            enemy_type = 'elite'
        else:
            # Sistema de pesos baseado no nível - PROGRESSÃO MAIS AGRESSIVA
            if self.level < 2:
                # Níveis iniciais: apenas básicos e rápidos
                enemy_type = random.choice(['basic', 'fast'])
            elif self.level < 4:
                # Adicionar shooters e kamikazes
                enemy_types = ['basic'] * 3 + ['fast'] * 3 + ['shooter'] * 2 + ['kamikaze'] * 2
                enemy_type = random.choice(enemy_types)
            elif self.level < 7:
                # Adicionar tanks e snipers - MAIS AGRESSIVO
                enemy_types = ['basic'] * 2 + ['fast'] * 3 + ['shooter'] * 3 + \
                             ['kamikaze'] * 3 + ['tank'] * 2 + ['sniper'] * 2
                enemy_type = random.choice(enemy_types)
            elif self.level < 10:
                # Adicionar splitters, bombers e healers - MUITO MAIS INIMIGOS
                enemy_types = ['basic'] * 1 + ['fast'] * 3 + ['shooter'] * 3 + \
                             ['kamikaze'] * 3 + ['tank'] * 2 + ['sniper'] * 2 + \
                             ['splitter'] * 2 + ['bomber'] * 2 + ['healer'] * 1
                enemy_type = random.choice(enemy_types)
            else:
                # Níveis avançados: CAOS TOTAL!
                enemy_types = ['fast'] * 3 + ['shooter'] * 4 + ['kamikaze'] * 3 + \
                             ['tank'] * 2 + ['sniper'] * 3 + ['splitter'] * 2 + \
                             ['bomber'] * 3 + ['healer'] * 1 + ['shield'] * 3
                enemy_type = random.choice(enemy_types)
        
        enemy = Enemy(x, y, enemy_type)
        
        # AUMENTAR STATS DOS INIMIGOS BASEADO NO NÍVEL - MAIS FORTE!
        level_multiplier = 1.0 + (self.level * 0.15)  # +15% por nível (era 10%)
        enemy.health = int(enemy.health * level_multiplier)
        enemy.speed = min(enemy.speed * (1.0 + self.level * 0.08), enemy.speed * 2.5)  # Max 2.5x (era 2x)
        
        self.enemies.add(enemy)
    
    def collect_powerup(self, powerup):
        """Aplicar efeito do power-up coletado"""
        powerup_type = powerup['type']
        
        # Som de power-up
        self.audio.play_sound('powerup')
        
        # 🌟 ADICIONAR XP (50 XP por power-up)
        self.progression.add_xp(50)
        
        # 📊 ESTATÍSTICAS
        self.session_stats['powerups'] += 1
        self.powerups_collected += 1
        
        # Efeito de partículas
        self.create_explosion((powerup['x'], powerup['y']), (255, 255, 100))
        
        # Aplicar efeito baseado no tipo
        if powerup_type == 'health':
            # Restaurar 30 de vida
            self.player.health = min(self.player.max_health, self.player.health + 30)
        
        elif powerup_type == 'speed':
            # Aumentar velocidade temporariamente
            self.player.speed = min(8, self.player.speed + 1)
        
        elif powerup_type == 'multishot':
            # Habilitar tiro múltiplo (pode ser implementado depois)
            self.player.shoot_cooldown_max = max(5, self.player.shoot_cooldown_max - 2)
        
        elif powerup_type == 'shield':
            # Escudo temporário (adicionar invulnerabilidade temporária)
            self.player.health = self.player.max_health
        
        # Adicionar pontos
        self.add_score(50)
        
        # Contabilizar power-up coletado
        self.powerups_collected += 1
    
    def check_collisions(self):
        """Verificar todas as colisões do jogo"""
        # Projéteis do jogador atingindo inimigos
        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for bullet, enemies_hit in hits.items():
            for enemy in enemies_hit:
                # Salvar informações do inimigo antes de matar
                enemy_type = enemy.enemy_type
                enemy_pos = enemy.rect.center
                enemy_size = max(enemy.width, enemy.height)
                
                # Verificar se é splitter antes de matar
                is_splitter = (enemy.enemy_type == 'splitter' and 
                             hasattr(enemy, 'splits_enabled') and 
                             enemy.splits_enabled and 
                             enemy.can_split())
                
                # Remover o inimigo
                enemy.kill()
                
                # Pontuação e estatísticas
                base_points = 100
                if enemy_type == 'giant':
                    base_points = 1000
                elif enemy_type == 'elite':
                    base_points = 750
                elif enemy_type == 'tank':
                    base_points = 500
                
                self.add_score(base_points)
                self.enemies_killed += 1
                
                # 🎮 ADICIONAR KILL AO COMBO
                self.combo.add_kill(time.time(), enemy_pos)
                self.session_stats['kills'] += 1
                self.session_stats['shots_hit'] += 1
                
                # 🌟 ADICIONAR XP (10 XP base * multiplicador do combo)
                xp_gain = int(10 * self.combo.get_multiplier())
                leveled_up, levels_gained = self.progression.add_xp(xp_gain)
                
                # Verificar level up e desbloqueios
                if leveled_up:
                            # Verificar desbloqueios de skins
                    new_skins = self.skin_system.check_unlocks(
                        self.progression.player_level,
                        self.progression.prestige_level
                    )
                    # Som especial de level up
                    self.audio.play_sound('powerup')
                
                # Ganhar moedas (1-3 moedas por inimigo, mais com upgrade e combo)
                coin_multiplier = 1.0 + (self.save_system.get_upgrade_level('coin_multiplier') * 0.1)
                coin_multiplier *= self.combo.get_multiplier()  # Combo também aumenta moedas!
                coins = int(random.randint(1, 3) * coin_multiplier)
                
                # Inimigos grandes dão MUITO mais moedas!
                if enemy_type == 'giant':
                    coins *= 10
                elif enemy_type == 'elite':
                    coins *= 5
                elif enemy_type == 'tank':
                    coins *= 3
                
                self.coins_earned_this_game += coins
                
                # Som de inimigo sendo atingido
                self.audio.play_sound('enemy_hit')
                
                # 🎆 EXPLOSÕES ESPETACULARES PARA INIMIGOS GRANDES! 🎆
                if enemy_type in ['giant', 'elite']:
                    # EXPLOSÃO GIGANTE PSICODÉLICA!!!
                    size_mult = 3.0 if enemy_type == 'giant' else 2.0
                    giant_particles = self.effects.create_giant_explosion(
                        enemy_pos[0], enemy_pos[1], size_mult
                    )
                    self.explosion_particles.extend(giant_particles)
                elif enemy_type == 'tank':
                    # Explosão grande
                    tank_particles = self.effects.create_giant_explosion(
                        enemy_pos[0], enemy_pos[1], 1.5
                    )
                    self.explosion_particles.extend(tank_particles)
                else:
                    # Explosão normal
                    self.create_explosion(enemy_pos, (255, 100, 0))
                
                # Splitter se divide em 2 inimigos menores
                if is_splitter:
                    for i in range(2):
                        angle = random.uniform(-math.pi/4, math.pi/4)
                        offset_x = 30 * math.cos(angle)
                        offset_y = 30 * math.sin(angle)
                        
                        new_enemy = Enemy(
                            enemy_pos[0] + offset_x,
                            enemy_pos[1] + offset_y,
                            random.choice(['basic', 'fast'])
                        )
                        # Inimigos divididos não podem se dividir novamente
                        new_enemy.splits_enabled = False
                        self.enemies.add(new_enemy)
        
        # Projéteis do jogador atingindo o boss
        if self.boss_active and self.boss:
            for bullet in self.bullets:
                if self.boss.rect.colliderect(bullet.rect):
                    if self.boss.take_damage(10):
                        bullet.kill()
                        self.add_score(10)
                        # Som de acerto no boss
                        self.audio.play_sound('enemy_hit')
                        # Partículas menores
                        self.create_explosion(bullet.rect.center, (255, 200, 0))
        
        # Verificar colisão com power-ups
        powerup_collisions = self.collision_manager.check_powerup_collision(
            self.player, self.level_generator.powerups
        )
        for powerup in powerup_collisions:
            self.collect_powerup(powerup)
            powerup['collected'] = True
            self.level_generator.powerups.remove(powerup)
        
        # Projéteis inimigos atingindo o jogador
        hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        if hits:
            self.player.take_damage(20)  # Dano padrão
            # Som de explosão quando jogador é atingido
            self.audio.play_sound('explosion')
            # Vibração ao tomar dano
            self.gamepad.rumble(0.7, 0.3, 150)
            if self.player.health <= 0:
                self.game_over()
        
        # Inimigos colidindo com o jogador
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if hits:
            self.player.take_damage(30)  # Dano maior por colisão
            self.audio.play_sound('explosion')
            # Vibração ao colidir com inimigo
            self.gamepad.rumble(0.8, 0.4, 200)
            if self.player.health <= 0:
                self.game_over()
        if hits:
            self.player.take_damage(30)  # Dano maior por colisão
            self.enemies_killed += len(hits)
            # Som de explosão grande quando colide com inimigo
            self.audio.play_sound('explosion')
            self.create_explosion(self.player.rect.center, (255, 0, 0))
            if self.player.health <= 0:
                self.game_over()
    
    def trigger_atomic_explosion(self):
        """⚛️ EXPLOSÃO ATÔMICA ÉPICA - Destrói TODOS os inimigos na tela! (NÃO causa dano ao jogador)"""
        
        # Som de explosão épica (múltiplos sons para impacto)
        self.audio.play_sound('explosion')
        self.audio.play_sound('powerup')
        self.audio.play_sound('explosion')  # Som duplo!
        
        # EXPLOSÃO CENTRAL MASSIVA na posição da bomba
        explosion_y = max(50, min(self.height - 50, self.atomic_bomb_y))  # Centralizar na tela
        
        # 🌟 EXPLOSÃO ÉPICA PRINCIPAL (GIGANTESCA!)
        self.effects.create_giant_explosion(
            self.atomic_bomb_x, 
            explosion_y, 
            size_multiplier=20.0  # ABSOLUTAMENTE MASSIVA!!!
        )
        
        # 💥 CRIAR 8 EXPLOSÕES ORBITAIS (como no boss)
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            orbit_distance = 150  # Grande distância
            orbit_x = self.atomic_bomb_x + math.cos(angle) * orbit_distance
            orbit_y = explosion_y + math.sin(angle) * orbit_distance
            
            self.effects.create_giant_explosion(
                orbit_x,
                orbit_y,
                size_multiplier=8.0  # Explosões grandes orbitais
            )
        
        # 🎆 CRIAR ONDAS DE CHOQUE EXPANDINDO
        for wave in range(5):
            delay = wave * 0.05  # Ondas sequenciais
            wave_size = 5.0 + wave * 2
            self.effects.create_giant_explosion(
                self.atomic_bomb_x,
                explosion_y,
                size_multiplier=wave_size
            )
        
        # ⚠️ DESTRUIR TODOS OS INIMIGOS NA TELA (mas NÃO o jogador!)
        enemies_destroyed = 0
        coins_earned = 0
        
        for enemy in list(self.enemies):
            # Criar explosão em cada inimigo
            self.effects.create_giant_explosion(
                enemy.rect.centerx,
                enemy.rect.centery,
                size_multiplier=2.0
            )
            
            # Ganhar pontos e moedas
            self.add_score(enemy.points * 2)  # Bomba atômica
            coins = random.randint(5, 15)
            self.coins_earned_this_game += coins
            coins_earned += coins
            
            # Remover inimigo
            enemy.kill()
            enemies_destroyed += 1
            self.session_stats['kills'] += 1
        
        # Se tiver boss, causar MUITO DANO (mas não mata instantaneamente)
        if self.boss_active and self.boss:
            damage = 30  # Tira bastante vida do boss
            self.boss.take_damage(damage)
            
            # Criar explosão no boss
            self.effects.create_giant_explosion(
                self.boss.x,
                self.boss.y,
                size_multiplier=5.0
            )
        
        
        # 🎆 PARTÍCULAS EXTRAS ÉPICAS (200+ partículas voando pela tela)
        for _ in range(250):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 25)  # Muito rápido!
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            # Cores psicodélicas variadas (garantir valores válidos)
            hue = random.uniform(0, 1.0)
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            color = (
                max(0, min(255, int(rgb[0] * 255))),
                max(0, min(255, int(rgb[1] * 255))),
                max(0, min(255, int(rgb[2] * 255)))
            )
            
            particle = {
                'x': self.atomic_bomb_x,
                'y': explosion_y,
                'vel_x': vel_x,
                'vel_y': vel_y,
                'life': random.randint(40, 80),  # Vida longa
                'color': color
            }
            self.particles.append(particle)
        
        # Adicionar ao combo (múltiplas mortes)
        current_time = time.time()
        for _ in range(enemies_destroyed):
            self.combo.add_kill(current_time)
    
    def create_explosion(self, position, color):
        """Criar efeito de explosão com partículas"""
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            particle = {
                'x': position[0],
                'y': position[1],
                'vel_x': vel_x,
                'vel_y': vel_y,
                'life': 30,
                'color': color
            }
            self.particles.append(particle)
    
    def update_particles(self):
        """Atualizar sistema de partículas"""
        for particle in self.particles[:]:
            particle['x'] += particle['vel_x']
            particle['y'] += particle['vel_y']
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw_particles(self):
        """Desenhar partículas"""
        for particle in self.particles:
            alpha = max(0, min(1.0, particle['life'] / 30.0))
            size = max(1, int(alpha * 4))
            # Garantir que cores sejam válidas (0-255)
            color = (
                max(0, min(255, int(particle['color'][0] * alpha))),
                max(0, min(255, int(particle['color'][1] * alpha))),
                max(0, min(255, int(particle['color'][2] * alpha)))
            )
            pygame.draw.circle(self.screen, color, 
                             (int(particle['x']), int(particle['y'])), size)
    
    def draw_hud(self):
        """Desenhar interface do usuário profissional - VERSÃO LIMPA E ORGANIZADA"""
        font_small = pygame.font.Font(None, 22)
        font_tiny = pygame.font.Font(None, 18)
        
        # Pegar dados do modo de jogo
        mode_icon = self.mode_manager.get_mode_icon()
        mode_name = self.mode_manager.get_mode_name()
        time_display = self.mode_manager.get_time_display()
        
        # ============================================
        # CANTO SUPERIOR ESQUERDO - Score e Level
        # ============================================
        y_pos = 10
        
        # Modo de jogo (ícone + nome)
        mode_text = f"{mode_icon} {mode_name}"
        mode_surf = font_small.render(mode_text, True, (255, 200, 100))
        self.screen.blit(mode_surf, (10, y_pos))
        y_pos += 25
        
        # Timer (se houver)
        if self.mode_manager.time_remaining is not None:
            timer_text = f"⏱️ {time_display}"
            timer_color = (255, 100, 100) if self.mode_manager.time_remaining < 30 else (255, 255, 255)
            timer_surf = font_small.render(timer_text, True, timer_color)
            self.screen.blit(timer_surf, (10, y_pos))
            y_pos += 25
        
        # Score
        score_text = f"PONTOS: {self.score:,}"
        score_surf = font_small.render(score_text, True, (255, 255, 100))
        self.screen.blit(score_surf, (10, y_pos))
        y_pos += 25
        
        # Level do jogo
        game_level_text = f"FASE: {self.level}"
        game_level_surf = font_small.render(game_level_text, True, (100, 200, 255))
        self.screen.blit(game_level_surf, (10, y_pos))
        y_pos += 20
        
        # Progresso até próximo nível e boss
        points_to_next = 5000 - (self.score % 5000)
        next_level = self.level + 1
        progress_text = f"Próximo: {points_to_next:,} pts"
        progress_surf = font_tiny.render(progress_text, True, (150, 150, 150))
        self.screen.blit(progress_surf, (10, y_pos))
        y_pos += 18
        
        # Indicador de boss
        if (next_level % 5) == 0:
            boss_text = f"🐉 BOSS no Nível {next_level}!"
            boss_surf = font_tiny.render(boss_text, True, (255, 100, 100))
            self.screen.blit(boss_surf, (10, y_pos))
            y_pos += 18
        
        y_pos += 10
        
        # Moedas
        coins_text = f"💰 {self.coins_earned_this_game}"
        coins_surf = font_small.render(coins_text, True, (255, 215, 0))
        self.screen.blit(coins_surf, (10, y_pos))
        y_pos += 25
        
        # Dica da loja
        shop_hint = "TAB/S: Loja"
        shop_surf = font_tiny.render(shop_hint, True, (200, 200, 100))
        self.screen.blit(shop_surf, (10, y_pos))
        y_pos += 25
        
        # ⚛️ BOMBAS ATÔMICAS
        bombs_text = f"⚛️  BOMBAS: {self.atomic_bombs}/{self.max_atomic_bombs}"
        bombs_color = (255, 100, 255) if self.atomic_bombs > 0 else (100, 100, 100)
        bombs_surf = font_small.render(bombs_text, True, bombs_color)
        self.screen.blit(bombs_surf, (10, y_pos))
        y_pos += 20
        
        # Dica da bomba
        if self.atomic_bomb_active:
            bomb_hint = "Bomba ativa - explode no topo!"
            bomb_hint_color = (255, 255, 0)  # Amarelo brilhante quando ativa!
        else:
            bomb_hint = "B: Disparar Bomba"
            bomb_hint_color = (200, 100, 200)
        
        bomb_hint_surf = font_tiny.render(bomb_hint, True, bomb_hint_color)
        self.screen.blit(bomb_hint_surf, (10, y_pos))
        y_pos += 25
        
        # ============================================
        # ESQUERDA - Progressão (Nível e XP)
        # ============================================
        # Nível do jogador
        player_level_text = f"NÍVEL {self.progression.player_level}"
        player_level_surf = font_small.render(player_level_text, True, (255, 150, 255))
        self.screen.blit(player_level_surf, (10, y_pos))
        y_pos += 20
        
        # Rank
        rank_text = f"{self.progression.get_rank_name()}"
        rank_surf = font_tiny.render(rank_text, True, (200, 150, 200))
        self.screen.blit(rank_surf, (10, y_pos))
        y_pos += 20
        
        # Barra de XP compacta
        xp_progress = self.progression.get_xp_progress()
        xp_bar_width = 150
        xp_bar_height = 8
        pygame.draw.rect(self.screen, (50, 50, 50), (10, y_pos, xp_bar_width, xp_bar_height))
        pygame.draw.rect(self.screen, (150, 100, 255), (10, y_pos, int(xp_bar_width * xp_progress), xp_bar_height))
        pygame.draw.rect(self.screen, (200, 150, 255), (10, y_pos, xp_bar_width, xp_bar_height), 1)
        
        # ============================================
        # CANTO SUPERIOR DIREITO - Vida e FPS
        # ============================================
        right_x = self.width - 220
        y_pos = 10
        
        # Barra de vida
        bar_width = 200
        bar_height = 15
        health_ratio = self.player.health / self.player.max_health if self.player.max_health > 0 else 0
        
        # Texto de vida
        health_text = f"VIDA: {int(self.player.health)}/{self.player.max_health}"
        health_surf = font_tiny.render(health_text, True, (255, 255, 255))
        self.screen.blit(health_surf, (right_x, y_pos))
        y_pos += 18
        
        # Barra
        pygame.draw.rect(self.screen, (80, 0, 0), (right_x, y_pos, bar_width, bar_height))
        health_color = self.get_psychedelic_color(self.color_shift)
        pygame.draw.rect(self.screen, health_color, (right_x, y_pos, int(bar_width * health_ratio), bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (right_x, y_pos, bar_width, bar_height), 2)
        y_pos += 25
        
        # FPS (se habilitado)
        if self.save_system.get_setting('show_fps', False):
            fps = self.clock.get_fps()
            fps_text = f"FPS: {int(fps)}"
            fps_surf = font_tiny.render(fps_text, True, (150, 150, 150))
            self.screen.blit(fps_surf, (right_x, y_pos))
            y_pos += 25
        
        # ============================================
        # DIREITA - Missões Diárias (compactas)
        # ============================================
        missions_title = "MISSÕES DIÁRIAS"
        missions_title_surf = font_tiny.render(missions_title, True, (255, 200, 100))
        self.screen.blit(missions_title_surf, (right_x, y_pos))
        y_pos += 18
        
        for mission in self.daily_missions.get_missions():
            # Ícone de status
            status_icon = "✓" if mission['completed'] else "○"
            color = (100, 255, 100) if mission['completed'] else (180, 180, 180)
            
            # Texto compacto
            mission_text = f"{status_icon} {mission['progress']}/{mission['target']}"
            mission_surf = font_tiny.render(mission_text, True, color)
            self.screen.blit(mission_surf, (right_x + 10, y_pos))
            y_pos += 16
        
        # ============================================
        # INFERIOR ESQUERDO - Controles (se visível)
        # ============================================
        if hasattr(self.hud, 'controls_visible') and self.hud.controls_visible:
            controls_y = self.height - 120
            controls = [
                "WASD/Setas: Mover",
                "Space: Atirar",
                "TAB/S: Loja",
                "P: Pausar"
            ]
            for i, control in enumerate(controls):
                control_surf = font_tiny.render(control, True, (150, 150, 150))
                self.screen.blit(control_surf, (10, controls_y + i * 16))
        
        # ============================================
        # INFERIOR DIREITO - Mini-mapa (opcional)
        # ============================================
        # Removido para evitar poluição visual
    
    def get_psychedelic_color(self, hue_shift):
        """Gerar cor psicodélica baseada no tempo"""
        hue = (hue_shift % 1.0)
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        return tuple(int(c * 255) for c in rgb)
    
    def game_over(self):
        """Mostrar tela de game over profissional"""
        self.is_game_over = True
        
        # Calcular tempo jogado
        time_played = int(time.time() - self.game_start_time)
        
        
        # 📝 INPUT DE NOME DO JOGADOR
        name_dialog = NameInputDialog(self.width, self.height)
        name_dialog.activate()
        player_name = "Player"  # Valor padrão
        
        # Loop do diálogo de nome
        while name_dialog.active:
            dt = self.clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    name_dialog.deactivate()
                    player_name = "Player"
                    break
                
                result = name_dialog.handle_event(event)
                if result:  # Nome confirmado ou ESC pressionado
                    player_name = result
                    break
            
            # Renderizar jogo pausado + diálogo
            self.render()
            name_dialog.update(dt)
            name_dialog.render(self.screen)
            pygame.display.flip()
        
        # 🏆 SALVAR NO LEADERBOARD
        if self.leaderboard:
            from leaderboard_system import LeaderboardEntry
            entry = LeaderboardEntry(
                player_name=player_name,
                score=self.score,
                level=self.level,
                mode=self.mode_manager.get_mode_name(),
                kills=self.enemies_killed
            )
            self.leaderboard.add_entry(entry)
        
        # �🏆 VERIFICAR CONQUISTAS FINAIS
        total_stats = {
            'total_kills': self.save_system.get_setting('total_kills', 0) + self.enemies_killed,
            'total_coins_earned': self.save_system.get_setting('total_coins_earned', 0) + self.coins_earned_this_game,
            'total_bosses_defeated': self.save_system.get_setting('total_bosses_defeated', 0) + self.session_stats['bosses'],
            'max_level_reached': max(self.save_system.get_setting('max_level_reached', 0), self.level),
            'max_combo': self.combo.get_max_combo(),
            'accuracy': (self.session_stats['shots_hit'] / max(1, self.session_stats['shots_fired'])) * 100,
            'time_survived': time_played
        }
        
        # Atualizar estatísticas globais
        self.save_system.update_setting('total_kills', total_stats['total_kills'])
        self.save_system.update_setting('total_coins_earned', total_stats['total_coins_earned'])
        self.save_system.update_setting('total_bosses_defeated', total_stats['total_bosses_defeated'])
        self.save_system.update_setting('max_level_reached', total_stats['max_level_reached'])
        
        # Verificar conquistas
        self.achievements.check_stats(total_stats)
        
        # Salvar moedas ganhas (com multiplicadores)
        coins_with_multiplier = int(self.coins_earned_this_game * self.progression.coin_multiplier)
        if coins_with_multiplier > 0:
            self.save_system.add_coins(coins_with_multiplier)
        
        # 🌟 ADICIONAR XP FINAL BASEADO NO LEVEL
        final_xp = self.level * 10
        self.progression.add_xp(final_xp)
        
        # Resetar tela de game over com estatísticas
        self.game_over_screen.reset(
            self.score,
            self.level,
            self.enemies_killed,
            self.powerups_collected,
            time_played
        )
        
        # Loop da tela de game over
        while self.is_game_over and self.running:
            dt = self.clock.tick(60) / 1000.0
            
            # Processar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.is_game_over = False
                    return "quit"
                
                action = self.game_over_screen.handle_event(event)
                if action == "retry":
                    self.restart_game()
                    self.is_game_over = False
                    return "retry"
                elif action == "menu":
                    self.is_game_over = False
                    self.running = False  # Marcar que o jogo deve voltar ao menu
                    return "menu"
            
            # Atualizar animações
            self.game_over_screen.update(dt)
            
            # Desenhar
            self.screen.fill((0, 0, 0))
            self.game_over_screen.draw(self.screen)
            pygame.display.flip()
        
        return None
    
    def restart_game(self):
        """Reiniciar o jogo"""
        # Parar sons ambiente
        self.audio.ambient_channel.stop()
        
        # Resetar estatísticas
        self.score = 0
        self.level = 1
        self.game_speed = 2
        self.enemies_killed = 0
        self.powerups_collected = 0
        self.game_start_time = time.time()
        self.coins_earned_this_game = 0  # Resetar moedas da partida
        
        # 🎮 RESETAR SISTEMAS DE ENGAJAMENTO
        self.combo.reset()
        self.session_stats = {
            'kills': 0,
            'bosses': 0,
            'powerups': 0,
            'coins': 0,
            'time': 0,
            'level': 0,
            'shots_fired': 0,
            'shots_hit': 0
        }
        
        # Resetar entidades
        self.player = Player(self.width // 2, self.height - 100)
        
        # Aplicar upgrades permanentes ao jogador
        self.apply_upgrades_to_player()
        
        self.enemies.empty()
        self.bullets.empty()
        self.enemy_bullets.empty()
        self.particles.clear()
        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = 120
        self.is_game_over = False
        
        # Resetar boss
        self.boss = None
        self.boss_active = False
        
        # Resetar HUD
        self.hud.reset_controls_timer()
    
    def apply_upgrades_to_player(self):
        """Aplicar upgrades permanentes ao jogador"""
        # Vida máxima (+20 por nível)
        health_upgrade = self.save_system.get_upgrade_level('max_health')
        self.player.max_health = 100 + (health_upgrade * 20)
        self.player.health = self.player.max_health
        
        # Velocidade (+0.5 por nível)
        speed_upgrade = self.save_system.get_upgrade_level('speed')
        self.player.speed = 5 + (speed_upgrade * 0.5)
        
        # Cadência de tiro (-2 frames por nível, mínimo 5)
        fire_rate_upgrade = self.save_system.get_upgrade_level('fire_rate')
        self.player.shoot_cooldown_max = max(5, 15 - (fire_rate_upgrade * 2))
        
        # Dano das balas (armazenar para uso posterior)
        self.player.bullet_damage = 1 + self.save_system.get_upgrade_level('bullet_damage')
        
        # Escudo (hits extras)
        shield_upgrade = self.save_system.get_upgrade_level('shield')
        self.player.shield = shield_upgrade
        self.player.shield_max = shield_upgrade
    
    def open_shop(self):
        """Abrir interface da loja"""
        in_shop = True
        
        while in_shop and self.running:
            dt = self.clock.tick(60) / 1000.0
            
            # Processar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    in_shop = False
                    return "quit"
                
                action = self.shop.handle_input(event)
                
                if action == 'exit':
                    in_shop = False
                    return "continue"
                elif action == 'purchase':
                    self.audio.play_sound('powerup')
                elif action == 'cannot_afford':
                    # Som de erro (ou criar um novo)
                    pass
                elif action == 'navigate':
                    # Som de navegação (opcional)
                    pass
            
            # Atualizar animações
            self.shop.update()
            
            # Desenhar
            self.shop.draw(self.screen)
            pygame.display.flip()
        
        return "continue"
    
    def render(self):
        """Renderizar o jogo"""
        # 🎮 APLICAR SCREEN SHAKE DO COMBO
        shake_offset = self.combo.get_screen_shake()
        
        # 🌌 RENDERIZAR CENÁRIO DINÂMICO (antes do fundo psicodélico)
        self.scenario_renderer.render(self.screen)
        
        # Fundo psicodélico (agora com transparência)
        self.effects.draw_background(self.screen, self.color_shift)
        
        # Desenhar nível (terreno e obstáculos)
        self.level_generator.draw(self.screen, self.color_shift)
        
        # 🎨 RENDERIZAR EFEITOS DE SKIN (trail, glow)
        self.skin_system.render_effects(self.screen, self.player.rect)
        
        # Desenhar sprites (aplicar shake offset se necessário)
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Desenhar boss (se ativo)
        if self.boss_active and self.boss:
            self.boss.draw(self.screen)
        
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)
        
        # Desenhar partículas normais
        self.draw_particles()
        
        # 🚀 DESENHAR MÍSSIL ATÔMICO SE ESTIVER ATIVO
        if self.atomic_bomb_active:
            # Animação de pulsação
            pulse = math.sin(pygame.time.get_ticks() / 80) * 3
            
            # ⚠️ EFEITO DE PISCAR (quanto mais perto do topo, mais rápido pisca)
            blink_speed = 150  # Começa piscando devagar
            if self.atomic_bomb_y < 100:  # Quando está próximo do topo
                blink_speed = 50  # Pisca RÁPIDO (alerta!)
            blink = (pygame.time.get_ticks() // blink_speed) % 2 == 0
            
            # Se não estiver piscando (off), desenha transparente/escuro
            if not blink and self.atomic_bomb_y < 100:
                # Míssil pisca quando está perto de explodir!
                brightness = 0.3  # Escurecido
            else:
                brightness = 1.0  # Normal/brilhante
            
            # CORPO DO MÍSSIL (retângulo gordo)
            missile_width = 30  # GORDO!
            missile_height = 60  # LONGO!
            missile_x = int(self.atomic_bomb_x - missile_width/2)
            missile_y = int(self.atomic_bomb_y - missile_height/2)
            
            # Corpo principal do míssil (cinza metálico com brightness)
            body_color = tuple(int(c * brightness) for c in (150, 150, 150))
            pygame.draw.rect(self.screen, body_color,
                           (missile_x, missile_y, missile_width, missile_height))
            
            # Borda brilhante do míssil (também pisca)
            border_color = tuple(int(c * brightness) for c in (200, 200, 255))
            pygame.draw.rect(self.screen, border_color,
                           (missile_x, missile_y, missile_width, missile_height), 3)
            
            # OGIVA (ponta triangular) - PISCA EM VERMELHO BRILHANTE quando perto do topo
            nose_points = [
                (int(self.atomic_bomb_x), int(self.atomic_bomb_y - missile_height/2 - 20)),  # Ponta
                (missile_x, missile_y),  # Esquerda
                (missile_x + missile_width, missile_y)  # Direita
            ]
            if self.atomic_bomb_y < 100 and blink:
                nose_color = (255, 255, 0)  # AMARELO BRILHANTE (alerta!)
            else:
                nose_color = tuple(int(c * brightness) for c in (255, 100, 100))
            pygame.draw.polygon(self.screen, nose_color, nose_points)
            pygame.draw.polygon(self.screen, tuple(int(c * brightness) for c in (255, 200, 200)), nose_points, 2)
            
            # ALETAS (base do míssil)
            fin_height = 15
            fin_y = missile_y + missile_height
            # Aleta esquerda
            left_fin = [
                (missile_x, fin_y),
                (missile_x - 12, fin_y + fin_height),
                (missile_x, fin_y + fin_height)
            ]
            fin_color = tuple(int(c * brightness) for c in (180, 180, 200))
            fin_border = tuple(int(c * brightness) for c in (220, 220, 255))
            pygame.draw.polygon(self.screen, fin_color, left_fin)
            pygame.draw.polygon(self.screen, fin_border, left_fin, 2)
            
            # Aleta direita
            right_fin = [
                (missile_x + missile_width, fin_y),
                (missile_x + missile_width + 12, fin_y + fin_height),
                (missile_x + missile_width, fin_y + fin_height)
            ]
            pygame.draw.polygon(self.screen, fin_color, right_fin)
            pygame.draw.polygon(self.screen, fin_border, right_fin, 2)
            
            # ⚠️ SÍMBOLO DE RADIAÇÃO no centro - PISCA INTENSAMENTE perto do topo!
            symbol_size = 8 + pulse
            if self.atomic_bomb_y < 100 and blink:
                # Quando perto do topo E piscando, símbolo fica VERMELHO BRILHANTE
                symbol_color = (255, 0, 0)
                symbol_center = (0, 0, 0)
            else:
                # Normal: amarelo
                symbol_color = tuple(int(c * brightness) for c in (255, 255, 0))
                symbol_center = tuple(int(c * brightness) for c in (0, 0, 0))
            
            pygame.draw.circle(self.screen, symbol_color,
                             (int(self.atomic_bomb_x), int(self.atomic_bomb_y)),
                             int(symbol_size))
            pygame.draw.circle(self.screen, symbol_center,
                             (int(self.atomic_bomb_x), int(self.atomic_bomb_y)),
                             int(symbol_size * 0.5))
            
            # Faixas de advertência (amarelo e preto) - também piscam
            stripe_y = missile_y + 15
            for i in range(3):
                stripe_y_pos = stripe_y + (i * 15)
                if i % 2 == 0:
                    stripe_color = tuple(int(c * brightness) for c in (255, 255, 0))
                    pygame.draw.rect(self.screen, stripe_color,
                                   (missile_x + 2, stripe_y_pos, missile_width - 4, 6))
                else:
                    stripe_color = tuple(int(c * brightness) for c in (0, 0, 0))
                    pygame.draw.rect(self.screen, stripe_color,
                                   (missile_x + 2, stripe_y_pos, missile_width - 4, 6))
            
            # PROPULSÃO - Trail de fogo e fumaça (não pisca, sempre ativa)
            trail_start_y = missile_y + missile_height + fin_height
            for i in range(20):
                trail_y = trail_start_y + (i * 8)
                trail_width = missile_width - (i * 1.2)
                trail_alpha = 255 - (i * 12)
                
                if trail_width > 0 and trail_y < self.height:
                    # Fogo alaranjado/amarelo
                    if i < 5:
                        color = (255, 255 - i*40, 0)  # Amarelo -> Laranja
                    elif i < 10:
                        color = (255 - (i-5)*30, 100, 0)  # Laranja -> Vermelho
                    else:
                        color = (150 - (i-10)*10, 50, 50)  # Vermelho escuro -> Fumaça
                    
                    pygame.draw.ellipse(self.screen, color,
                                      (int(self.atomic_bomb_x - trail_width/2),
                                       int(trail_y),
                                       int(trail_width),
                                       12))
            
            # Partículas de faísca ao redor da propulsão
            for angle in range(0, 360, 45):
                rad = math.radians(angle + pygame.time.get_ticks() / 15)
                spark_distance = 25 + pulse
                particle_x = self.atomic_bomb_x + math.cos(rad) * spark_distance
                particle_y = trail_start_y + 10 + math.sin(rad) * spark_distance
                pygame.draw.circle(self.screen, (255, 255, 100),
                                 (int(particle_x), int(particle_y)), 3)
        
        # 🎆 DESENHAR EXPLOSÕES ESPETACULARES! 🎆
        self.effects.draw_explosion_particles(self.screen, self.explosion_particles)
        
        # Desenhar efeitos psicodélicos
        self.effects.draw_effects(self.screen, self.color_shift)
        
        # 🎮 RENDERIZAR COMBO E FLOATING TEXT
        self.combo.render(self.screen)
        
        # Desenhar HUD
        self.draw_hud()
        
        # Desenhar tela de pausa se necessário
        if self.paused:
            self.draw_pause_screen()
        
        pygame.display.flip()
    
    def run(self):
        """Loop principal do jogo"""
        try:
            while self.running:
                self.handle_events()
                self.update()
                self.render()
                self.clock.tick(60)  # 60 FPS
        finally:
            # Limpar recursos de áudio
            try:
                self.audio.cleanup()
            except Exception as e:
                pass
    
    def cleanup(self):
        """Limpar recursos do jogo"""
        if hasattr(self, 'audio'):
            try:
                self.audio.cleanup()
            except Exception as e:
                pass
    
    def draw_pause_screen(self):
        """Desenhar tela de pausa"""
        # Overlay semi-transparente
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Texto de pausa
        font = pygame.font.Font(None, 74)
        pause_text = font.render("PAUSADO", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.screen.blit(pause_text, pause_rect)
        
        # Instruções
        font_small = pygame.font.Font(None, 36)
        instruction_text = font_small.render("Pressione P para continuar", True, (200, 200, 200))
        instruction_rect = instruction_text.get_rect(center=(self.width // 2, self.height // 2 + 20))
        self.screen.blit(instruction_text, instruction_rect)
        
        esc_text = font_small.render("ESC para sair", True, (200, 200, 200))
        esc_rect = esc_text.get_rect(center=(self.width // 2, self.height // 2 + 60))
        self.screen.blit(esc_text, esc_rect)