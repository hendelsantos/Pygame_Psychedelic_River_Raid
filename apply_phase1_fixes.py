#!/usr/bin/env python3
"""
Script para remover prints de debug e aplicar multiplicadores de score
"""

import re

# Ler o arquivo
with open('game.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Padrões para remover prints específicos
prints_to_remove = [
    r'        print\("🚀 Lançando bomba atômica!"\)\n',
    r'                print\(f"💥 Bomba atingiu o topo.*EXPLODINDO!"\)\n',
    r'        print\(f"🐉 BOSS APARECEU! Nível \{self\.level\}"\)\n',
    r'        print\(f"🏆 BOSS DERROTADO! \+\{boss_score:,\} pontos!"\)\n',
    r'            print\(f"🎉 LEVEL UP! Nível \{self\.progression\.player_level\}"\)\n',
    r'        print\(f"💰💰💰 \+\{boss_coins\} moedas pelo BOSS!"\)\n',
    r'        print\("💥💥💥 EXPLOSÃO FENOMENAL DO BOSS! 💥💥💥"\)\n',
    r'            print\(f"🐉 Próximo boss do nível.*"\)\n',
    r'        print\(f"   🎯 Dificuldade ajustada.*"\)\n',
    r'            print\(f"💚 Power-up de VIDA coletado!.*"\)\n',
    r'            print\(f"⚡ Power-up de VELOCIDADE coletado!.*"\)\n',
    r'            print\(f"🔫 Power-up de TIRO RÁPIDO coletado!.*"\)\n',
    r'            print\(f"🛡️ Power-up de ESCUDO coletado!.*"\)\n',
    r'                    print\(f"💥 EXPLOSÃO ESPETACULAR!.*"\)\n',
    r'        print\("💥💥💥 EXPLOSÃO ATÔMICA ÉPICA! 💥💥💥"\)\n',
    r'            print\(f"⚡ Boss levou.*"\)\n',
    r'        print\(f"💣 \{enemies_destroyed\} inimigos destruídos!.*"\)\n',
    r'            print\(f"💰 \{coins_with_multiplier\} moedas salvas!.*"\)\n',
    r'        print\(f"🎮 Level:.*"\)\n',
    r'            print\("🎵 Finalizando sistema de áudio\.\.\."\)\n',
    r'                print\(f"⚠️ Aviso ao limpar áudio:.*"\)\n',
    r'        print\("🧹 Limpando recursos do jogo\.\.\."\)\n',
]

# Remover os prints
for pattern in prints_to_remove:
    content = re.sub(pattern, '', content)

# Substituir adds de score diretos por add_score()
replacements = [
    (r'self\.score \+= boss_score', 'self.add_score(boss_score)'),
    (r'self\.score \+= 50', 'self.add_score(50)'),
    (r'self\.score \+= base_points', 'self.add_score(base_points)'),
    (r'self\.score \+= 10', 'self.add_score(10)'),
    (r'self\.score \+= enemy\.points \* 2  # DOBRO de pontos!', 'self.add_score(enemy.points * 2)  # Bomba atômica'),
]

for old, new in replacements:
    content = re.sub(old, new, content)

# Salvar o arquivo
with open('game.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Prints removidos e multiplicadores aplicados!")
print("📊 Scores agora usam add_score() com multiplicadores de modo")
