"""
Configurações de Áudio do Psychedelic River Raid
Ajuste estes valores para personalizar a experiência sonora
"""

# =============================================================================
# CONFIGURAÇÕES GERAIS DE ÁUDIO
# =============================================================================

# Volume inicial (0.0 a 1.0)
DEFAULT_VOLUME = 0.3

# Buffer de áudio (valores maiores = menos cliques, mais latência)
AUDIO_BUFFER = 1024

# Sample rate (qualidade do áudio)
SAMPLE_RATE = 22050

# =============================================================================
# VOLUMES DOS CANAIS (proporção do volume geral)
# =============================================================================

MUSIC_VOLUME_RATIO = 0.3    # Música de fundo
SFX_VOLUME_RATIO = 0.7      # Efeitos sonoros
AMBIENT_VOLUME_RATIO = 0.2  # Sons ambiente (motor)

# =============================================================================
# CONFIGURAÇÕES DOS EFEITOS SONOROS
# =============================================================================

# Laser
LASER_DURATION = 0.12
LASER_START_FREQ = 600
LASER_END_FREQ = 150
LASER_AMPLITUDE = 0.6

# Explosão
EXPLOSION_DURATION = 0.6
EXPLOSION_AMPLITUDE = 0.5
EXPLOSION_NOISE_CUTOFF = 4000

# Motor da nave
ENGINE_BASE_FREQ = 80
ENGINE_AMPLITUDE = 0.3
ENGINE_CUTOFF_FREQ = 3000

# Inimigo atingido
HIT_BASE_FREQ = 400
HIT_MODULATION_FREQ = 20
HIT_DURATION = 0.25

# =============================================================================
# CONFIGURAÇÕES DA MÚSICA PROCEDURAL
# =============================================================================

# Duração de cada track (segundos)
MUSIC_TRACK_DURATION = 16.0

# Amplitude geral da música
MUSIC_AMPLITUDE = 0.4

# Volumes das camadas musicais
BASS_VOLUME = 0.8
CHORD_VOLUME = 0.4
MELODY_VOLUME = 0.5

# Filtros de frequência
MUSIC_CUTOFF_FREQ = 6000
BASS_CUTOFF_FREQ = 2000
MELODY_CUTOFF_FREQ = 5000

# =============================================================================
# CONFIGURAÇÕES DE ENVELOPE ADSR
# =============================================================================

# Envelope padrão suave
DEFAULT_ATTACK = 0.05
DEFAULT_DECAY = 0.1
DEFAULT_SUSTAIN = 0.6
DEFAULT_RELEASE = 0.25

# Envelope para música
MUSIC_ATTACK = 0.1
MUSIC_DECAY = 0.1
MUSIC_SUSTAIN = 0.7
MUSIC_RELEASE = 0.3

# =============================================================================
# CONFIGURAÇÕES DE FILTROS
# =============================================================================

# Filtro anti-aliasing geral
DEFAULT_CUTOFF_FREQ = 8000

# Amplitude de normalização
DEFAULT_NORMALIZE_AMPLITUDE = 0.8

# =============================================================================
# CONFIGURAÇÕES DE REVERB
# =============================================================================

# Reverb suave
REVERB_DELAY = 0.2
REVERB_FEEDBACK = 0.2
REVERB_MIX = 0.15

# =============================================================================
# PROGRESSÕES DE ACORDES PARA MÚSICA PROCEDURAL
# =============================================================================

CHORD_PROGRESSIONS = [
    ['C', 'Am', 'F', 'G'],      # Pop progression
    ['Am', 'F', 'C', 'G'],      # Alternative
    ['C', 'G', 'Am', 'F'],      # Classic
    ['Dm', 'Bb', 'F', 'C'],     # Dorian
    ['Em', 'C', 'G', 'D']       # Emotional
]

# =============================================================================
# ESCALAS MUSICAIS (frequências em Hz)
# =============================================================================

MUSICAL_SCALES = {
    'C': [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88],  # C major
    'Am': [220.00, 246.94, 261.63, 293.66, 329.63, 349.23, 392.00], # A minor
    'F': [174.61, 196.00, 220.00, 233.08, 261.63, 293.66, 329.63],  # F major
    'G': [196.00, 220.00, 246.94, 261.63, 293.66, 329.63, 369.99],  # G major
    'Dm': [146.83, 164.81, 174.61, 196.00, 220.00, 233.08, 261.63], # D minor
    'Bb': [116.54, 130.81, 146.83, 155.56, 174.61, 196.00, 220.00], # Bb major
    'Em': [164.81, 185.00, 196.00, 220.00, 246.94, 261.63, 293.66], # E minor
    'D': [146.83, 164.81, 185.00, 196.00, 220.00, 246.94, 277.18]   # D major
}

# =============================================================================
# DICAS DE AJUSTE
# =============================================================================

"""
DICAS PARA AJUSTAR O ÁUDIO:

1. Se o áudio estiver muito alto:
   - Diminua DEFAULT_VOLUME
   - Ajuste os ratios dos canais

2. Se a música estiver muito alta:
   - Diminua MUSIC_VOLUME_RATIO
   - Reduza MUSIC_AMPLITUDE

3. Se os efeitos estiverem muito agressivos:
   - Aumente os valores de CUTOFF_FREQ
   - Diminua as amplitudes individuais
   - Ajuste os envelopes para serem mais suaves

4. Se houver cliques ou pops:
   - Aumente AUDIO_BUFFER
   - Ajuste os envelopes de attack e release
   - Verifique os filtros passa-baixa

5. Para melhor qualidade:
   - Aumente SAMPLE_RATE (cuidado com performance)
   - Ajuste os filtros de frequência
   - Use envelopes mais suaves

6. Para performance:
   - Diminua SAMPLE_RATE
   - Reduza MUSIC_TRACK_DURATION
   - Simplifique os efeitos
"""