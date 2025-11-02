import pygame

class SkinSystem:
    """Sistema de skins para a nave do jogador"""
    
    def __init__(self, save_system):
        self.save_system = save_system
        
        # Definir skins disponíveis
        self.skins = {
            'classic': {
                'name': '🚀 Clássico',
                'description': 'Nave padrão',
                'color': (100, 200, 255),
                'unlocked': True,
                'unlock_condition': 'Inicial'
            },
            'gold': {
                'name': '👑 Dourada',
                'description': 'Para os vitoriosos',
                'color': (255, 215, 0),
                'unlocked': False,
                'unlock_condition': 'Nível 10',
                'unlock_level': 10
            },
            'rainbow': {
                'name': '🌈 Arco-íris',
                'description': 'Cores psicodélicas',
                'color': None,  # Animado
                'unlocked': False,
                'unlock_condition': 'Nível 20',
                'unlock_level': 20
            },
            'ghost': {
                'name': '👻 Fantasma',
                'description': 'Invisível e mortal',
                'color': (150, 150, 255),
                'unlocked': False,
                'unlock_condition': 'Nível 30',
                'unlock_level': 30,
                'alpha': 180
            },
            'dragon': {
                'name': '🐉 Dragão',
                'description': 'Fogo e fúria',
                'color': (255, 50, 0),
                'unlocked': False,
                'unlock_condition': 'Nível 40',
                'unlock_level': 40,
                'trail': True
            },
            'prestige': {
                'name': '✨ Prestígio',
                'description': 'Para os lendários',
                'color': (255, 100, 255),
                'unlocked': False,
                'unlock_condition': 'Prestígio 1',
                'unlock_prestige': 1,
                'glow': True
            }
        }
        
        # Carregar skin selecionada
        self.selected_skin = self.save_system.get_setting('selected_skin', 'classic')
        
        # Carregar skins desbloqueadas
        unlocked = self.save_system.get_setting('unlocked_skins', ['classic'])
        for skin_id in unlocked:
            if skin_id in self.skins:
                self.skins[skin_id]['unlocked'] = True
        
        # Animação rainbow
        self.rainbow_hue = 0
        
        # Trail do dragão
        self.dragon_trail = []
    
    def check_unlocks(self, player_level, prestige_level):
        """Verificar desbloqueios baseado no nível"""
        newly_unlocked = []
        
        for skin_id, skin in self.skins.items():
            if not skin['unlocked']:
                # Verificar nível
                if 'unlock_level' in skin and player_level >= skin['unlock_level']:
                    skin['unlocked'] = True
                    newly_unlocked.append(skin_id)
                    print(f"🎨 Skin desbloqueada: {skin['name']}")
                
                # Verificar prestígio
                if 'unlock_prestige' in skin and prestige_level >= skin['unlock_prestige']:
                    skin['unlocked'] = True
                    newly_unlocked.append(skin_id)
                    print(f"🎨 Skin desbloqueada: {skin['name']}")
        
        # Salvar skins desbloqueadas
        if newly_unlocked:
            unlocked_list = [sid for sid, s in self.skins.items() if s['unlocked']]
            self.save_system.update_setting('unlocked_skins', unlocked_list)
        
        return newly_unlocked
    
    def select_skin(self, skin_id):
        """Selecionar skin"""
        if skin_id in self.skins and self.skins[skin_id]['unlocked']:
            self.selected_skin = skin_id
            self.save_system.update_setting('selected_skin', skin_id)
            return True
        return False
    
    def get_selected_skin(self):
        """Obter skin selecionada"""
        return self.skins[self.selected_skin]
    
    def get_skin_color(self):
        """Obter cor da skin atual"""
        skin = self.skins[self.selected_skin]
        
        # Rainbow animado
        if self.selected_skin == 'rainbow':
            self.rainbow_hue = (self.rainbow_hue + 2) % 360
            return self.hsv_to_rgb(self.rainbow_hue, 1.0, 1.0)
        
        return skin.get('color', (100, 200, 255))
    
    def hsv_to_rgb(self, h, s, v):
        """Converter HSV para RGB"""
        h = h / 360.0
        i = int(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        
        i = i % 6
        if i == 0: r, g, b = v, t, p
        elif i == 1: r, g, b = q, v, p
        elif i == 2: r, g, b = p, v, t
        elif i == 3: r, g, b = p, q, v
        elif i == 4: r, g, b = t, p, v
        elif i == 5: r, g, b = v, p, q
        
        return (int(r * 255), int(g * 255), int(b * 255))
    
    def update_trail(self, position):
        """Atualizar trail do dragão"""
        if self.selected_skin == 'dragon':
            self.dragon_trail.append({
                'pos': position,
                'alpha': 255,
                'size': 20
            })
            
            # Limitar tamanho do trail
            if len(self.dragon_trail) > 20:
                self.dragon_trail.pop(0)
            
            # Atualizar trail
            for particle in self.dragon_trail:
                particle['alpha'] -= 15
                particle['size'] -= 1
    
    def render_effects(self, screen, player_rect):
        """Renderizar efeitos especiais da skin"""
        skin = self.skins[self.selected_skin]
        
        # Glow do Prestígio
        if skin.get('glow'):
            import math
            glow_size = int(30 + math.sin(pygame.time.get_ticks() * 0.005) * 10)
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*skin['color'], 50), (glow_size, glow_size), glow_size)
            screen.blit(glow_surf, (player_rect.centerx - glow_size, player_rect.centery - glow_size))
        
        # Trail do Dragão
        if self.selected_skin == 'dragon':
            for particle in self.dragon_trail:
                if particle['alpha'] > 0 and particle['size'] > 0:
                    trail_surf = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                    pygame.draw.circle(trail_surf, (255, 100, 0, particle['alpha']), 
                                     (particle['size'], particle['size']), particle['size'])
                    screen.blit(trail_surf, 
                              (particle['pos'][0] - particle['size'], 
                               particle['pos'][1] - particle['size']))
    
    def get_available_skins(self):
        """Obter lista de skins disponíveis"""
        return self.skins
    
    def get_unlocked_count(self):
        """Contar skins desbloqueadas"""
        return sum(1 for skin in self.skins.values() if skin['unlocked'])
    
    def get_total_count(self):
        """Contar total de skins"""
        return len(self.skins)
