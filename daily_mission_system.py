import time
import random
from datetime import datetime, timedelta

class DailyMissionSystem:
    """Sistema de missões diárias"""
    
    def __init__(self, save_system):
        self.save_system = save_system
        
        # Carregar missões salvas
        self.daily_missions = self.save_system.get_setting('daily_missions', [])
        self.last_reset = self.save_system.get_setting('daily_missions_last_reset', 0)
        
        # Verificar se precisa resetar
        self.check_reset()
        
        # Se não há missões, gerar novas
        if not self.daily_missions:
            self.generate_daily_missions()
    
    def check_reset(self):
        """Verificar se precisa resetar as missões diárias"""
        now = time.time()
        last_reset_date = datetime.fromtimestamp(self.last_reset).date()
        today = datetime.now().date()
        
        if last_reset_date < today:
            # Novo dia, resetar missões
            self.generate_daily_missions()
            self.last_reset = now
            self.save_system.update_setting('daily_missions_last_reset', self.last_reset)
            print("📅 Novas missões diárias disponíveis!")
    
    def generate_daily_missions(self):
        """Gerar 3 missões diárias aleatórias"""
        mission_pool = [
            # Missões de kills
            {
                'id': 'kill_50',
                'name': '⚔️ Exterminador',
                'description': 'Mate 50 inimigos',
                'type': 'kills',
                'target': 50,
                'reward': 500,
                'progress': 0,
                'completed': False
            },
            {
                'id': 'kill_100',
                'name': '⚔️ Carnificina',
                'description': 'Mate 100 inimigos',
                'type': 'kills',
                'target': 100,
                'reward': 1000,
                'progress': 0,
                'completed': False
            },
            
            # Missões de nível
            {
                'id': 'reach_level_5',
                'name': '🎯 Explorador',
                'description': 'Alcance o nível 5',
                'type': 'level',
                'target': 5,
                'reward': 300,
                'progress': 0,
                'completed': False
            },
            {
                'id': 'reach_level_10',
                'name': '🎯 Aventureiro',
                'description': 'Alcance o nível 10',
                'type': 'level',
                'target': 10,
                'reward': 800,
                'progress': 0,
                'completed': False
            },
            
            # Missões de power-ups
            {
                'id': 'collect_20_powerups',
                'name': '💚 Colecionador',
                'description': 'Colete 20 power-ups',
                'type': 'powerups',
                'target': 20,
                'reward': 400,
                'progress': 0,
                'completed': False
            },
            
            # Missões de boss
            {
                'id': 'defeat_boss',
                'name': '🐉 Caçador',
                'description': 'Derrote 1 boss',
                'type': 'boss',
                'target': 1,
                'reward': 1000,
                'progress': 0,
                'completed': False
            },
            
            # Missões de moedas
            {
                'id': 'earn_1000_coins',
                'name': '💰 Coletor',
                'description': 'Ganhe 1000 moedas em uma partida',
                'type': 'coins',
                'target': 1000,
                'reward': 500,
                'progress': 0,
                'completed': False
            },
            
            # Missões de sobrevivência
            {
                'id': 'survive_5min',
                'name': '⏱️ Sobrevivente',
                'description': 'Sobreviva por 5 minutos',
                'type': 'time',
                'target': 300,  # 5 minutos em segundos
                'reward': 600,
                'progress': 0,
                'completed': False
            },
            
            # Missões de precisão
            {
                'id': 'accuracy_80',
                'name': '🎯 Precisão',
                'description': 'Alcance 80% de precisão',
                'type': 'accuracy',
                'target': 80,
                'reward': 800,
                'progress': 0,
                'completed': False
            },
        ]
        
        # Escolher 3 missões aleatórias
        self.daily_missions = random.sample(mission_pool, 3)
        self.save_system.update_setting('daily_missions', self.daily_missions)
        
        return self.daily_missions
    
    def update_progress(self, mission_type, value):
        """Atualizar progresso das missões"""
        updated = False
        
        for mission in self.daily_missions:
            if mission['type'] == mission_type and not mission['completed']:
                mission['progress'] = min(mission['target'], value)
                
                # Verificar se completou
                if mission['progress'] >= mission['target'] and not mission['completed']:
                    mission['completed'] = True
                    self.save_system.add_coins(mission['reward'])
                    print(f"🎉 MISSÃO COMPLETA: {mission['name']}")
                    print(f"   Recompensa: {mission['reward']} moedas")
                    updated = True
        
        if updated:
            self.save_system.update_setting('daily_missions', self.daily_missions)
        
        return updated
    
    def check_mission_completion(self, stats):
        """Verificar conclusão de missões baseado nas estatísticas"""
        # Kills
        self.update_progress('kills', stats.get('kills', 0))
        
        # Nível
        self.update_progress('level', stats.get('level', 0))
        
        # Power-ups
        self.update_progress('powerups', stats.get('powerups', 0))
        
        # Boss
        self.update_progress('boss', stats.get('bosses', 0))
        
        # Moedas
        self.update_progress('coins', stats.get('coins', 0))
        
        # Tempo
        self.update_progress('time', stats.get('time', 0))
        
        # Precisão
        if stats.get('shots_fired', 0) > 0:
            accuracy = (stats.get('shots_hit', 0) / stats.get('shots_fired', 0)) * 100
            self.update_progress('accuracy', int(accuracy))
    
    def get_missions(self):
        """Obter missões diárias"""
        return self.daily_missions
    
    def get_completed_count(self):
        """Contar missões completadas"""
        return sum(1 for m in self.daily_missions if m['completed'])
    
    def all_completed(self):
        """Verificar se todas as missões foram completadas"""
        return all(m['completed'] for m in self.daily_missions)
    
    def get_bonus_reward(self):
        """Recompensa bônus por completar todas as missões"""
        if self.all_completed():
            return 2000  # Bônus extra
        return 0
