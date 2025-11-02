# 🚀 Psychedelic River Raid

Um jogo inspirado no clássico River Raid com gráficos psicodélicos e geração procedural de níveis!

## 🎮 Sobre o Jogo

Este é um jogo de nave espacial estilo arcade onde você pilota uma nave através de um túnel infinito cheio de obstáculos e inimigos. O jogo apresenta:

- **Gráficos Psicodélicos**: Cores vibrantes que mudam constantemente, efeitos visuais hipnóticos
- **Geração Procedural**: Cada partida é única com terreno e obstáculos gerados algoritmicamente
- **Gameplay Desafiador**: Dificuldade progressiva com múltiplos tipos de inimigos
- **Efeitos Visuais**: Partículas, explosões, rastros e túneis psicodélicos

## 🎯 Objetivo

Sobreviva o máximo possível voando através do túnel, destruindo inimigos e evitando obstáculos. Sua pontuação aumenta com o tempo de sobrevivência e inimigos destruídos.

## 🕹️ Controles

### Movimento

- **Setas** ou **WASD**: Mover a nave
- **Espaço**: Atirar
- **ESC**: Sair do jogo

### Áudio

- **+/-**: Aumentar/Diminuir volume
- **M**: Mute/Unmute

### Tela de Game Over

- **R**: Reiniciar o jogo
- **ESC**: Sair

## 🚀 Como Executar

1. Certifique-se de ter Python 3.12+ instalado
2. Instale as dependências:
   ```bash
   pip install pygame numpy scipy pydub simpleaudio
   ```
3. Execute o jogo:
   ```bash
   python main.py
   ```

## 🎵 Sistema de Áudio Procedural

### Música de Fundo

- **Música Chiptune**: Gerada proceduralmente em tempo real
- **5 Progressões de Acordes**: Variações automáticas
- **Instrumentação**: Baixo, acordes e melodia separados
- **Loop Contínuo**: Transições suaves entre tracks

### Efeitos Sonoros

- **Tiro Laser**: Som futurista suavizado com filtros anti-aliasing
- **Explosões**: Ruído procedural filtrado para conforto auditivo
- **Inimigo Atingido**: Tom metálico modulado com envelope suave
- **Motor da Nave**: Loop contínuo filtrado em frequências baixas
- **Power-ups**: Arpejos ascendentes com reverb controlado (planejado)

### Características Técnicas

- **22 kHz Sample Rate**: Qualidade otimizada para jogos
- **Síntese Procedural**: Ondas filtradas para máximo conforto
- **Envelope ADSR Suave**: Transições graduais sem cliques
- **Filtros Anti-Aliasing**: Remoção de frequências desconfortáveis
- **Controle de Amplitude**: Normalização inteligente para evitar distorção
- **Volumes Balanceados**: Música 30%, SFX 70%, Ambiente 20%

### Melhorias de Conforto Auditivo

- **Filtros Passa-Baixa**: Removem frequências altas irritantes
- **Envelopes Suaves**: Eliminam cliques e pops
- **Volume Inicial Baixo**: Começa em 30% para conforto
- **Ajuste Fino**: Incrementos de 5% no volume
- **Normalização Controlada**: Previne picos de volume
- **Controle em Tempo Real**: Volume ajustável durante o jogo

## 🎨 Características Visuais

### Efeitos Psicodélicos

- **Cores Dinâmicas**: Sistema HSV que cria transições suaves de cores
- **Ondas de Fundo**: Padrões senoidais animados
- **Túnel 3D**: Anéis em perspectiva criando ilusão de profundidade
- **Partículas**: Sistema avançado de partículas para explosões e rastros
- **Fractais**: Padrões matemáticos em movimento
- **Raios de Energia**: Efeitos luminosos rotativos

### Nave do Jogador

- Design triangular futurista
- Cockpit e asas com cores psicodélicas
- Campo de energia pulsante ao redor
- Partículas de propulsão atrás da nave

## 👾 Inimigos

### Tipos de Inimigos

1. **Básico** (Losango vermelho)

   - Movimento reto
   - 100 pontos
   - 1 HP

2. **Rápido** (Triângulo amarelo)

   - Movimento rápido com chamas
   - 150 pontos
   - 1 HP

3. **Atirador** (Hexágono magenta)
   - Atira projéteis duplos
   - 200 pontos
   - 2 HP

### Padrões de Movimento

- **Reto**: Movimento linear simples
- **Zigue-zague**: Movimento senoidal horizontal
- **Circular**: Movimento em espiral

## 🌍 Geração de Mundo

### Sistema Procedural

- **Terreno**: Paredes laterais com variação orgânica
- **Obstáculos**: Rochas, cristais e campos de energia
- **Power-ups**: Coletáveis raros com diferentes efeitos
- **Dificuldade Adaptativa**: Corredor fica mais estreito com o tempo

### Tipos de Obstáculos

- **Rochas**: Octágonos rotacionados
- **Cristais**: Diamantes brilhantes
- **Campos de Energia**: Esferas pulsantes com anéis

### Power-ups (Planejados)

- **Vida**: Restaura saúde (cruz vermelha)
- **Velocidade**: Aumenta velocidade temporariamente (seta)
- **Tiro Múltiplo**: Projéteis triplos (linhas paralelas)
- **Escudo**: Proteção temporária (escudo)

## 🎵 Sistema de Física

### Colisões

- **Detecção Circular**: Para jogador, inimigos e projéteis
- **Detecção Retangular**: Para terreno e obstáculos
- **Sistema de Partículas**: Explosões dinâmicas nas colisões

### Movimento

- **Jogador**: Controle suave em 8 direções
- **Projéteis**: Velocidade constante com rastros
- **Inimigos**: Padrões de movimento únicos por tipo

## 📊 Sistema de Pontuação

- **Sobrevivência**: +1 ponto por frame
- **Inimigo Básico**: +100 pontos
- **Inimigo Rápido**: +150 pontos
- **Inimigo Atirador**: +200 pontos
- **Aumento de Nível**: A cada 5000 pontos

## 🔧 Estrutura do Código

```
game1/
├── main.py              # Ponto de entrada
├── game.py              # Loop principal e lógica do jogo
├── player.py            # Classe do jogador e projéteis
├── enemy.py             # Classes dos inimigos
├── bullet.py            # Sistema de projéteis
├── effects.py           # Efeitos visuais psicodélicos
├── level_generator.py   # Geração procedural de níveis
├── collision.py         # Sistema de detecção de colisões
└── README.md           # Este arquivo
```

## 🎨 Paleta de Cores

O jogo usa o sistema HSV para criar transições suaves:

- **Jogador**: Azul/Ciano (hue 0.6)
- **Inimigos**: Vermelho/Magenta (hue 0.0-0.8)
- **Projéteis**: Arco-íris dinâmico
- **Efeitos**: Espectro completo HSV

## 🚀 Recursos Avançados

### Otimizações

- Remoção automática de objetos fora da tela
- Pools de objetos para partículas
- Renderização eficiente de efeitos

### Escalabilidade

- Sistema modular de componentes
- Fácil adição de novos tipos de inimigos
- Configuração flexível de dificuldade

## 🎯 Melhorias Futuras

- [ ] Sistema de som e música
- [ ] Power-ups funcionais
- [ ] Boss battles
- [ ] Múltiplas armas
- [ ] Sistema de upgrades
- [ ] Leaderboard local
- [ ] Modo cooperativo
- [ ] Customização da nave

## 🏆 Dicas de Jogo

1. **Mantenha-se em movimento**: Parado você é um alvo fácil
2. **Use o espaço**: Não fique apenas nas bordas
3. **Priorize inimigos atiradores**: Eles são mais perigosos
4. **Observe os padrões**: Cada tipo de inimigo tem movimento previsível
5. **Gerencie sua saúde**: Evite dano desnecessário

## 📜 Licença

Este projeto é de código aberto e foi criado para fins educacionais e de entretenimento.

---

**Divirta-se explorando o universo psicodélico! 🌈✨**
# Pygame_Psychedelic_River_Raid
