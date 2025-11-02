import time

class AchievementSystem:
    """Sistema de conquistas"""
    
    def __init__(self, save_system):
        self.save_system = save_system
        
        # Carregar conquistas desbloqueadas
        self.unlocked = set(self.save_system.get_setting('unlocked_achievements', []))
        
        # Definir todas as conquistas
        self.achievements = {
            # Conquistas de início
            'first_death': {
                'name': '💀 Primeira Morte',
                'description': 'Morra pela primeira vez',
                'reward': 100,
                'hidden': False
            },
            'first_kill': {
                'name': '🎯 Primeiro Sangue',
                'description': 'Mate seu primeiro inimigo',
                'reward': 50,
                'hidden': False
            },
            'first_boss': {
                'name': '🐉 Caçador de Dragões',
                'description': 'Derrote seu primeiro boss',
                'reward': 500,
                'hidden': False
            },
            
            # Conquistas de kills
            'killer_100': {
                'name': '⚔️ Exterminador',
                'description': 'Mate 100 inimigos',
                'reward': 500,
                'hidden': False
            },
            'killer_500': {
                'name': '⚔️ Genocida',
                'description': 'Mate 500 inimigos',
                'reward': 1000,
                'hidden': False
            },
            'killer_1000': {
                'name': '⚔️ Dizimador',
                'description': 'Mate 1.000 inimigos',
                'reward': 2000,
                'hidden': False
            },
            
            # Conquistas de moedas
            'rich_1000': {
                'name': '💰 Rico',
                'description': 'Acumule 1.000 moedas',
                'reward': 200,
                'hidden': False
            },
            'rich_10000': {
                'name': '💰 Milionário',
                'description': 'Acumule 10.000 moedas',
                'reward': 1000,
                'hidden': False
            },
            'rich_50000': {
                'name': '💎 Magnata',
                'description': 'Acumule 50.000 moedas',
                'reward': 5000,
                'hidden': False
            },
            
            # Conquistas de nível
            'level_10': {
                'name': '🛡️ Guerreiro',
                'description': 'Alcance o nível de jogo 10',
                'reward': 300,
                'hidden': False
            },
            'level_20': {
                'name': '🎯 Veterano',
                'description': 'Alcance o nível de jogo 20',
                'reward': 1000,
                'hidden': False
            },
            'level_30': {
                'name': '💎 Elite',
                'description': 'Alcance o nível de jogo 30',
                'reward': 3000,
                'hidden': False
            },
            
            # Conquistas de boss
            'boss_5': {
                'name': '🐲 Matador de Dragões',
                'description': 'Derrote 5 bosses',
                'reward': 1000,
                'hidden': False
            },
            'boss_10': {
                'name': '🐲 Exterminador de Dragões',
                'description': 'Derrote 10 bosses',
                'reward': 2000,
                'hidden': False
            },
            
            # Conquistas de upgrades
            'full_upgrades': {
                'name': '⚡ Poder Máximo',
                'description': 'Maximize todos os upgrades',
                'reward': 5000,
                'hidden': False
            },
            
            # Conquistas especiais
            'perfect_level': {
                'name': '👑 Perfeição',
                'description': 'Complete um nível sem tomar dano',
                'reward': 1000,
                'hidden': False
            },
            'speed_run': {
                'name': '⚡ Velocista',
                'description': 'Chegue ao nível 10 em menos de 5 minutos',
                'reward': 1500,
                'hidden': False
            },
            'sharpshooter': {
                'name': '🎯 Atirador de Elite',
                'description': 'Alcance 95% de precisão em uma partida',
                'reward': 2000,
                'hidden': False
            },
            'survivor': {
                'name': '🏆 Sobrevivente',
                'description': 'Sobreviva por 10 minutos em uma partida',
                'reward': 1000,
                'hidden': False
            },
            
            # Conquistas secretas
            'no_damage_boss': {
                'name': '⭐ Intocável',
                'description': 'Derrote um boss sem tomar dano',
                'reward': 3000,
                'hidden': True
            },
            'prestige_1': {
                'name': '⭐ Primeira Estrela',
                'description': 'Alcance seu primeiro prestígio',
                'reward': 10000,
                'hidden': True
            }
        }
        
        # Notificações pendentes
        self.pending_notifications = []
    
    def check_achievement(self, achievement_id):
        """Verificar e desbloquear conquista"""
        if achievement_id in self.achievements and achievement_id not in self.unlocked:
            self.unlock(achievement_id)
            return True
        return False
    
    def unlock(self, achievement_id):
        """Desbloquear conquista"""
        if achievement_id not in self.unlocked:
            self.unlocked.add(achievement_id)
            achievement = self.achievements[achievement_id]
            
            # Adicionar moedas de recompensa
            self.save_system.add_coins(achievement['reward'])
            
            # Adicionar notificação
            self.pending_notifications.append({
                'name': achievement['name'],
                'description': achievement['description'],
                'reward': achievement['reward'],
                'time': time.time()
            })
            
            # Salvar
            self.save_system.update_setting('unlocked_achievements', list(self.unlocked))
            
            print(f"🏆 CONQUISTA DESBLOQUEADA: {achievement['name']}")
            print(f"   {achievement['description']}")
            print(f"   Recompensa: {achievement['reward']} moedas")
    
    def check_stats(self, stats):
        """Verificar conquistas baseadas em estatísticas"""
        # Total de kills
        total_kills = stats.get('total_kills', 0)
        if total_kills == 1:
            self.check_achievement('first_kill')
        elif total_kills >= 100:
            self.check_achievement('killer_100')
        if total_kills >= 500:
            self.check_achievement('killer_500')
        if total_kills >= 1000:
            self.check_achievement('killer_1000')
        
        # Total de moedas acumuladas
        total_coins = stats.get('total_coins_earned', 0)
        if total_coins >= 1000:
            self.check_achievement('rich_1000')
        if total_coins >= 10000:
            self.check_achievement('rich_10000')
        if total_coins >= 50000:
            self.check_achievement('rich_50000')
        
        # Bosses derrotados
        bosses = stats.get('total_bosses_defeated', 0)
        if bosses == 1:
            self.check_achievement('first_boss')
        elif bosses >= 5:
            self.check_achievement('boss_5')
        if bosses >= 10:
            self.check_achievement('boss_10')
        
        # Nível máximo
        max_level = stats.get('max_level_reached', 0)
        if max_level >= 10:
            self.check_achievement('level_10')
        if max_level >= 20:
            self.check_achievement('level_20')
        if max_level >= 30:
            self.check_achievement('level_30')
    
    def get_notifications(self):
        """Obter e limpar notificações pendentes"""
        notifications = self.pending_notifications.copy()
        self.pending_notifications.clear()
        return notifications
    
    def get_progress(self):
        """Obter progresso geral de conquistas"""
        total = len(self.achievements)
        unlocked_count = len(self.unlocked)
        return {
            'unlocked': unlocked_count,
            'total': total,
            'percentage': (unlocked_count / total) * 100 if total > 0 else 0
        }
    
    def get_all_achievements(self):
        """Obter todas as conquistas com status"""
        result = []
        for achievement_id, achievement in self.achievements.items():
            result.append({
                'id': achievement_id,
                'name': achievement['name'],
                'description': achievement['description'],
                'reward': achievement['reward'],
                'hidden': achievement['hidden'],
                'unlocked': achievement_id in self.unlocked
            })
        return result
