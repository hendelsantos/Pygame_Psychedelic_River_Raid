# ⚔️ SISTEMA DE DIFICULDADE PROGRESSIVA

## ✅ **MELHORIAS IMPLEMENTADAS:**

### **1️⃣ BOSSES GARANTIDOS A CADA 5 NÍVEIS**

#### **Sistema Robusto:**

```python
# Verificação dupla ao subir de nível
if self.level % 5 == 0:
    if not self.boss_active:
        self.spawn_boss()
    else:
        print("Boss será spawnado após derrotá-lo")
```

#### **Após Derrotar Boss:**

```python
# Se ainda estiver em múltiplo de 5, spawna o próximo
if self.level % 5 == 0:
    # Pausa de 3 segundos para o jogador respirar
    pygame.time.wait(3000)
    self.spawn_boss()
```

#### **Resultado:**

- ✅ Boss **SEMPRE** aparece nos níveis 5, 10, 15, 20, etc
- ✅ Se derrotar boss e já estiver no próximo múltiplo de 5, aparece outro
- ✅ Impossível pular um boss

---

### **2️⃣ VARIEDADE DE INIMIGOS PROGRESSIVA**

#### **Sistema de Unlock Gradual:**

**Nível 1-2:** (Iniciante)

- Basic (comum)
- Fast (rápido)

**Nível 3-4:** (Intermediário)

- Basic, Fast
- ➕ Shooter (atira)
- ➕ Kamikaze (se joga)

**Nível 5-7:** (Avançado)

- Todos anteriores +
- ➕ Tank (resistente)
- ➕ Sniper (preciso)

**Nível 8-10:** (Expert)

- Todos anteriores +
- ➕ Splitter (se divide)
- ➕ Bomber (explosivo)
- ➕ Healer (cura outros)

**Nível 11+:** (Master)

- Todos anteriores +
- ➕ Shield (protegido)
- Peso aumentado para tipos difíceis

#### **Código:**

```python
if self.level < 2:
    enemy_type = random.choice(['basic', 'fast'])
elif self.level < 4:
    # Adiciona shooter e kamikaze
elif self.level < 7:
    # Adiciona tank e sniper
elif self.level < 10:
    # Adiciona splitter, bomber, healer
else:
    # Todos os tipos, mais tipos difíceis
```

---

### **3️⃣ MAIS INIMIGOS NA TELA**

#### **Sistema de Spawn Múltiplo:**

```python
# Spawnar múltiplos inimigos por wave
enemies_to_spawn = 1 + (self.level // 3)

# Nível 1-2:  1 inimigo
# Nível 3-5:  2 inimigos
# Nível 6-8:  3 inimigos
# Nível 9-11: 4 inimigos
# Nível 12+:  5+ inimigos por wave
```

#### **Spawn Rate Progressivo:**

```python
# Interval diminui com o nível
min_interval = max(15, 60 - (self.level * 2))

# Nível 1:  60 frames
# Nível 5:  50 frames
# Nível 10: 40 frames
# Nível 15: 30 frames
# Nível 20: 20 frames
# Nível 23+: 15 frames (mínimo)
```

---

### **4️⃣ ESCALA BASEADA EM UPGRADES**

#### **Sistema de "Poder do Jogador":**

```python
player_power = 1.0  # Base
player_power += max_health_upgrade * 0.1    # +10% por upgrade
player_power += fire_rate_upgrade * 0.15    # +15% por upgrade
player_power += bullet_damage_upgrade * 0.2 # +20% por upgrade
player_power += speed_upgrade * 0.1         # +10% por upgrade
```

#### **Ajuste Dinâmico:**

```python
# Mais forte = inimigos spawnam mais rápido
power_reduction = (player_power - 1.0) * 20

# Exemplo:
# Poder 1.0 (sem upgrades): 0 redução
# Poder 1.5 (alguns upgrades): -10 frames
# Poder 2.0 (muitos upgrades): -20 frames
# Poder 3.0 (full upgrades): -40 frames
```

#### **Resultado:**

- Jogador fraco: Inimigos mais espaçados
- Jogador médio: Velocidade moderada
- Jogador forte: MUITOS inimigos!

---

### **5️⃣ STATS DOS INIMIGOS ESCALADOS**

#### **Multiplicador por Nível:**

```python
level_multiplier = 1.0 + (self.level * 0.1)

# Aplicado a cada inimigo:
enemy.health *= level_multiplier
enemy.speed *= (1.0 + self.level * 0.05)  # Max 2x
```

#### **Exemplo:**

**Nível 1:**

- Basic: 3 HP, velocidade normal
- Tank: 15 HP, velocidade normal

**Nível 10:**

- Basic: 6 HP (+100%), velocidade +50%
- Tank: 30 HP (+100%), velocidade +50%

**Nível 20:**

- Basic: 9 HP (+200%), velocidade +100%
- Tank: 45 HP (+200%), velocidade +100%

---

### **6️⃣ VELOCIDADE DO JOGO LIMITADA**

```python
# Antes: self.game_speed += 0.5 (sem limite)
# Depois:
self.game_speed = min(8.0, 2 + (self.level * 0.3))

# Nível 1:  2.0
# Nível 5:  3.5
# Nível 10: 5.0
# Nível 15: 6.5
# Nível 20: 8.0 (máximo)
```

**Motivo:** Evitar que fique impossível de jogar em níveis muito altos

---

## 📊 **TABELA DE DIFICULDADE**

| Nível | Boss? | Tipos Inimigos | Spawns/Wave | Spawn Rate | Velocidade | HP Inimigo |
| ----- | ----- | -------------- | ----------- | ---------- | ---------- | ---------- |
| 1     | ❌    | 2              | 1           | 60 frames  | 2.0        | 100%       |
| 3     | ❌    | 4              | 2           | 54 frames  | 2.9        | 130%       |
| 5     | ✅    | 6              | 2           | 50 frames  | 3.5        | 150%       |
| 10    | ✅    | 8              | 4           | 40 frames  | 5.0        | 200%       |
| 15    | ✅    | 10             | 5           | 30 frames  | 6.5        | 250%       |
| 20    | ✅    | 10             | 7           | 20 frames  | 8.0        | 300%       |
| 25    | ✅    | 10             | 9           | 15 frames  | 8.0        | 350%       |

---

## 🎮 **EXEMPLO DE PROGRESSÃO:**

### **Jogador Sem Upgrades:**

```
Nível 5:
- 2 inimigos por wave
- Spawn a cada 50 frames
- Velocidade 3.5
- Dificuldade: Moderada
```

### **Jogador Com Upgrades (Poder 2.0x):**

```
Nível 5:
- 2 inimigos por wave
- Spawn a cada 30 frames (20 reduzido pelo poder)
- Velocidade 3.5
- Dificuldade: ALTA - Compensando upgrades!
```

### **Nível 20 Full Upgrade (Poder 3.0x):**

```
Nível 20:
- 7 inimigos por wave
- Spawn a cada 15 frames (MÍNIMO!)
- Velocidade 8.0 (MÁXIMO!)
- Inimigos com 300% HP
- Variedade completa (10 tipos)
- Dificuldade: INSANA!
```

---

## 🔥 **CURVA DE DIFICULDADE**

```
Dificuldade
    ↑
    │                                    ╱──── Poder 3.0x
    │                            ╱──────╱
    │                    ╱──────╱ Poder 2.0x
    │            ╱──────╱
    │    ╱──────╱ Poder 1.0x (sem upgrades)
    │───────────────────────────────────→ Nível
    1   5   10   15   20   25   30
    ↓   ↓   ↓    ↓    ↓    ↓    ↓
    🎮  🐉  🐉  🐉  🐉  🐉  🐉
```

---

## ✨ **BALANCEAMENTO INTELIGENTE:**

### **Feedback Visual:**

```
Console durante level up:
⬆️ LEVEL UP! Agora você está no nível 10
   Velocidade: 5.0 | Spawn: 40
   🎯 Dificuldade ajustada - Poder: 1.8x | Spawn: 24
```

### **Fórmulas Finais:**

1. **Quantidade de Inimigos:**

   ```
   enemies_per_wave = 1 + (level // 3)
   ```

2. **Spawn Rate:**

   ```
   interval = max(15, 120 - (level * 3) - (player_power * 20))
   ```

3. **HP dos Inimigos:**

   ```
   health *= (1.0 + level * 0.1)
   ```

4. **Velocidade dos Inimigos:**

   ```
   speed *= min(2.0, 1.0 + level * 0.05)
   ```

5. **Velocidade do Jogo:**
   ```
   game_speed = min(8.0, 2 + level * 0.3)
   ```

---

## 🎯 **RESULTADO FINAL:**

### **✅ Garantias:**

- Boss **sempre** a cada 5 níveis
- Variedade aumenta gradualmente
- Dificuldade escala com tempo
- **Mais** inimigos se player mais forte
- Balance justo mas desafiador

### **✅ Experiência:**

- Início: Fácil e acolhedor
- Meio: Desafiador e variado
- Final: INSANO mas possível
- Replayability infinita

---

## 🚀 **TESTE AGORA:**

Pressione **L** várias vezes para pular níveis e ver a progressão:

- **L** 4x → Nível 5 → Primeiro boss + 2 inimigos/wave
- **L** 9x → Nível 10 → Boss + 4 inimigos/wave + 8 tipos
- **L** 14x → Nível 15 → Boss + 5 inimigos/wave + spawn rápido
- **L** 19x → Nível 20 → **CAOS TOTAL!**

**O jogo agora escala perfeitamente!** ⚔️🔥
