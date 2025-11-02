import math

class ProgressionSystem:
    """Sistema de XP e níveis do jogador"""
    
    def __init__(self, save_system):
        self.save_system = save_system
        
        # Carregar dados salvos
        self.player_level = self.save_system.get_setting('player_level', 1)
        self.current_xp = self.save_system.get_setting('current_xp', 0)
        self.total_xp = self.save_system.get_setting('total_xp', 0)
        
        # Sistema de prestígio
        self.prestige_level = self.save_system.get_setting('prestige_level', 0)
        
        # Multiplicadores baseados no prestígio
        self.coin_multiplier = 1.0 + (self.prestige_level * 0.05)  # +5% por prestígio
        self.xp_multiplier = 1.0 + (self.prestige_level * 0.1)  # +10% por prestígio
        
    def get_xp_for_level(self, level):
        """Calcular XP necessário para um nível"""
        # Fórmula exponencial: 100 * (1.15 ^ level)
        return int(100 * math.pow(1.15, level - 1))
    
    def get_xp_to_next_level(self):
        """XP necessário para o próximo nível"""
        return self.get_xp_for_level(self.player_level + 1)
    
    def get_xp_progress(self):
        """Progresso para o próximo nível (0.0 a 1.0)"""
        xp_needed = self.get_xp_to_next_level()
        return min(1.0, self.current_xp / xp_needed)
    
    def add_xp(self, amount):
        """Adicionar XP e verificar level up"""
        amount = int(amount * self.xp_multiplier)
        self.current_xp += amount
        self.total_xp += amount
        
        leveled_up = False
        levels_gained = 0
        
        # Verificar múltiplos level ups
        while self.current_xp >= self.get_xp_to_next_level():
            xp_needed = self.get_xp_to_next_level()
            self.current_xp -= xp_needed
            self.player_level += 1
            levels_gained += 1
            leveled_up = True
            
            print(f"🎉 LEVEL UP! Agora você é nível {self.player_level}!")
        
        # Salvar progresso
        self.save_progress()
        
        return leveled_up, levels_gained
    
    def prestige(self):
        """Sistema de prestígio - resetar nível mas ganhar bônus permanente"""
        if self.player_level >= 50:
            self.prestige_level += 1
            self.player_level = 1
            self.current_xp = 0
            
            # Recalcular multiplicadores
            self.coin_multiplier = 1.0 + (self.prestige_level * 0.05)
            self.xp_multiplier = 1.0 + (self.prestige_level * 0.1)
            
            self.save_progress()
            print(f"⭐ PRESTÍGIO {self.prestige_level}! Bônus: +{self.prestige_level*5}% moedas, +{self.prestige_level*10}% XP")
            return True
        return False
    
    def get_rank_name(self):
        """Nome do rank baseado no nível"""
        if self.prestige_level > 0:
            return f"⭐ Prestígio {self.prestige_level}"
        elif self.player_level >= 50:
            return "👑 Lenda"
        elif self.player_level >= 40:
            return "💎 Elite"
        elif self.player_level >= 30:
            return "⚔️ Veterano"
        elif self.player_level >= 20:
            return "🎯 Experiente"
        elif self.player_level >= 10:
            return "🛡️ Guerreiro"
        else:
            return "🔰 Iniciante"
    
    def get_level_rewards(self, level):
        """Recompensas ao atingir um nível"""
        rewards = []
        
        # Moedas a cada nível
        coins = 100 * level
        rewards.append(f"+{coins} moedas")
        
        # Recompensas especiais
        if level % 5 == 0:
            rewards.append("🎁 Caixa de Recompensa")
        
        if level == 10:
            rewards.append("🚀 Skin Dourada desbloqueada")
        elif level == 20:
            rewards.append("🌈 Skin Rainbow desbloqueada")
        elif level == 30:
            rewards.append("👻 Skin Fantasma desbloqueada")
        elif level == 40:
            rewards.append("🐉 Skin Dragão desbloqueada")
        elif level == 50:
            rewards.append("⭐ Prestígio disponível!")
        
        return rewards
    
    def save_progress(self):
        """Salvar progresso"""
        self.save_system.update_setting('player_level', self.player_level)
        self.save_system.update_setting('current_xp', self.current_xp)
        self.save_system.update_setting('total_xp', self.total_xp)
        self.save_system.update_setting('prestige_level', self.prestige_level)
    
    def get_stats(self):
        """Obter estatísticas para display"""
        return {
            'level': self.player_level,
            'current_xp': self.current_xp,
            'xp_needed': self.get_xp_to_next_level(),
            'progress': self.get_xp_progress(),
            'rank': self.get_rank_name(),
            'prestige': self.prestige_level,
            'total_xp': self.total_xp,
            'coin_multiplier': self.coin_multiplier,
            'xp_multiplier': self.xp_multiplier
        }
