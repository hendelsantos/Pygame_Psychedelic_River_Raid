import json
import os
from datetime import datetime

class SaveSystem:
    def __init__(self):
        self.save_dir = os.path.expanduser("~/.psychedelic_river_raid")
        self.save_file = os.path.join(self.save_dir, "save_data.json")
        
        # Criar diretório se não existir
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        # Dados padrão
        self.default_data = {
            'high_scores': [],
            'settings': {
                'music_volume': 0.3,
                'sfx_volume': 0.5,
                'fullscreen': False,
                'resolution': [800, 600],
                'show_fps': False,
                'particle_quality': 'alta',
                'screen_shake': True
            },
            'stats': {
                'total_games_played': 0,
                'total_enemies_killed': 0,
                'total_powerups_collected': 0,
                'total_time_played': 0,
                'highest_level_reached': 1
            },
            'unlocks': {
                'skins': ['default'],
                'weapons': ['basic']
            },
            'coins': 0,
            'upgrades': {
                'max_health': 0,
                'fire_rate': 0,
                'bullet_damage': 0,
                'speed': 0,
                'shield': 0,
                'coin_multiplier': 0
            }
        }
        
        # Carregar dados salvos
        self.data = self.load_game()
    
    def load_game(self):
        """Carregar dados salvos do arquivo"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Mesclar com dados padrão para adicionar novos campos
                    return self.merge_with_defaults(data)
            else:
                return self.default_data.copy()
        except Exception as e:
            print(f"⚠️ Erro ao carregar save: {e}")
            return self.default_data.copy()
    
    def merge_with_defaults(self, loaded_data):
        """Mesclar dados carregados com padrões para compatibilidade"""
        merged = self.default_data.copy()
        
        for key in merged:
            if key in loaded_data:
                if isinstance(merged[key], dict):
                    merged[key].update(loaded_data[key])
                else:
                    merged[key] = loaded_data[key]
        
        return merged
    
    def save_game(self):
        """Salvar dados no arquivo"""
        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"⚠️ Erro ao salvar: {e}")
            return False
    
    def add_high_score(self, score, level, player_name="Player"):
        """Adicionar nova pontuação ao ranking"""
        new_score = {
            'score': score,
            'level': level,
            'player_name': player_name,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Adicionar à lista
        self.data['high_scores'].append(new_score)
        
        # Ordenar por pontuação (maior primeiro)
        self.data['high_scores'].sort(key=lambda x: x['score'], reverse=True)
        
        # Manter apenas top 10
        self.data['high_scores'] = self.data['high_scores'][:10]
        
        # Salvar
        self.save_game()
        
        # Retornar posição no ranking (1-10, ou None se não entrou)
        for i, entry in enumerate(self.data['high_scores']):
            if (entry['score'] == score and 
                entry['player_name'] == player_name and 
                entry['date'] == new_score['date']):
                return i + 1
        return None
    
    def get_high_scores(self, limit=10):
        """Obter lista de high scores"""
        return self.data['high_scores'][:limit]
    
    def is_high_score(self, score):
        """Verificar se a pontuação entra no top 10"""
        if len(self.data['high_scores']) < 10:
            return True
        return score > self.data['high_scores'][-1]['score']
    
    def get_highest_score(self):
        """Obter a maior pontuação"""
        if self.data['high_scores']:
            return self.data['high_scores'][0]['score']
        return 0
    
    def update_stats(self, **kwargs):
        """Atualizar estatísticas do jogador"""
        for key, value in kwargs.items():
            if key in self.data['stats']:
                if isinstance(value, (int, float)):
                    self.data['stats'][key] += value
                else:
                    self.data['stats'][key] = value
        self.save_game()
    
    def get_stat(self, stat_name):
        """Obter estatística específica"""
        return self.data['stats'].get(stat_name, 0)
    
    def update_setting(self, setting_name, value):
        """Atualizar configuração"""
        if setting_name in self.data['settings']:
            self.data['settings'][setting_name] = value
            self.save_game()
    
    def get_setting(self, setting_name, default=None):
        """Obter configuração específica"""
        return self.data['settings'].get(setting_name, default)
    
    def unlock_item(self, category, item_name):
        """Desbloquear item (skin, arma, etc)"""
        if category in self.data['unlocks']:
            if item_name not in self.data['unlocks'][category]:
                self.data['unlocks'][category].append(item_name)
                self.save_game()
                return True
        return False
    
    def is_unlocked(self, category, item_name):
        """Verificar se item está desbloqueado"""
        if category in self.data['unlocks']:
            return item_name in self.data['unlocks'][category]
        return False
    
    def reset_save(self):
        """Resetar todos os dados salvos"""
        self.data = self.default_data.copy()
        self.save_game()
    
    def export_save(self, filepath):
        """Exportar save para outro arquivo"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            return True
        except:
            return False
    
    def import_save(self, filepath):
        """Importar save de outro arquivo"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.save_game()
            return True
        except:
            return False
    
    # ========== SISTEMA DE MOEDAS ==========
    
    def get_coins(self):
        """Obter quantidade de moedas"""
        return self.data.get('coins', 0)
    
    def add_coins(self, amount):
        """Adicionar moedas"""
        self.data['coins'] = self.data.get('coins', 0) + amount
        self.save_game()
    
    def spend_coins(self, amount):
        """Gastar moedas"""
        current = self.data.get('coins', 0)
        if current >= amount:
            self.data['coins'] = current - amount
            self.save_game()
            return True
        return False
    
    # ========== SISTEMA DE UPGRADES ==========
    
    def get_upgrades(self):
        """Obter todos os upgrades"""
        if 'upgrades' not in self.data:
            self.data['upgrades'] = self.default_data['upgrades'].copy()
        return self.data['upgrades']
    
    def get_upgrade_level(self, upgrade_id):
        """Obter nível de um upgrade específico"""
        upgrades = self.get_upgrades()
        return upgrades.get(upgrade_id, 0)
    
    def upgrade_stat(self, upgrade_id, new_level):
        """Atualizar nível de um upgrade"""
        if 'upgrades' not in self.data:
            self.data['upgrades'] = self.default_data['upgrades'].copy()
        
        self.data['upgrades'][upgrade_id] = new_level
        self.save_game()
