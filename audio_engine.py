import pygame
import numpy as np
import math
import random
import threading
import time

class AudioEngine:
    def __init__(self, sample_rate=22050, channels=2):
        """Sistema de áudio procedural para o jogo"""
        # Configurações mais profissionais para reduzir ruído
        pygame.mixer.pre_init(frequency=sample_rate, size=-16, channels=channels, buffer=2048)
        pygame.mixer.init()
        
        self.sample_rate = sample_rate
        self.channels = channels
        self.volume = 0.25  # Volume inicial ainda mais baixo
        
        # Canais de áudio
        self.music_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)
        self.ambient_channel = pygame.mixer.Channel(2)
        
        # Estado da música
        self.music_playing = False
        self.current_track = 0
        self.music_tempo = 120  # BPM
        self.music_key = 'C'
        
        # Cache de sons
        self.sound_cache = {}
        
        # Thread para música contínua
        self.music_thread = None
        self.music_running = False
        
        # Configurações avançadas para áudio profissional
        self.dither_amount = 0.0001  # Dithering para reduzir quantização
        self.dc_offset_removal = True  # Remover DC offset
        self.noise_gate_threshold = 0.01  # Gate de ruído
        
        # Configurações de música procedural - Estilo Chiptune/8-bit clássico
        self.chiptune_progressions = [
            # Progressão clássica de jogos de arcade (estilo Galaga/Space Invaders)
            {
                'name': 'Classic Arcade',
                'chords': ['C', 'Am', 'F', 'G'],
                'melody_pattern': [0, 2, 4, 2, 0, 4, 2, 0],  # Padrão melódico
                'bass_pattern': [0, 0, 0, 0, 2, 2, 0, 0],    # Linha de baixo
                'tempo': 140
            },
            # Progressão estilo Mega Man
            {
                'name': 'Heroic Battle',
                'chords': ['Am', 'F', 'C', 'G'],
                'melody_pattern': [0, 3, 2, 4, 3, 1, 2, 0],
                'bass_pattern': [0, 0, 2, 2, 0, 0, 1, 1],
                'tempo': 160
            },
            # Progressão estilo Zelda/Nintendo
            {
                'name': 'Adventure Theme',
                'chords': ['C', 'G', 'Am', 'F'],
                'melody_pattern': [0, 2, 4, 5, 4, 2, 1, 0],
                'bass_pattern': [0, 4, 0, 2, 0, 4, 0, 2],
                'tempo': 120
            },
            # Progressão estilo Castlevania/Metroid
            {
                'name': 'Dark Underground',
                'chords': ['Dm', 'Bb', 'F', 'C'],
                'melody_pattern': [0, 1, 3, 2, 4, 3, 1, 0],
                'bass_pattern': [0, 0, 0, 0, 3, 3, 0, 0],
                'tempo': 110
            },
            # Progressão estilo Pac-Man/clássicos
            {
                'name': 'Retro Fun',
                'chords': ['C', 'E', 'Am', 'F'],
                'melody_pattern': [0, 4, 2, 3, 1, 2, 4, 0],
                'bass_pattern': [0, 2, 0, 1, 0, 2, 0, 1],
                'tempo': 180
            }
        ]
        
        # Escalas musicais para chiptune (frequências exatas de 8-bit)
        self.chiptune_scales = {
            'C': [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88],  # C major
            'Am': [220.00, 246.94, 261.63, 293.66, 329.63, 349.23, 392.00], # A minor
            'F': [174.61, 196.00, 220.00, 233.08, 261.63, 293.66, 329.63],  # F major
            'G': [196.00, 220.00, 246.94, 261.63, 293.66, 329.63, 369.99],  # G major
            'Dm': [146.83, 164.81, 174.61, 196.00, 220.00, 233.08, 261.63], # D minor
            'Bb': [116.54, 130.81, 146.83, 155.56, 174.61, 196.00, 220.00], # Bb major
            'Em': [164.81, 185.00, 196.00, 220.00, 246.94, 261.63, 293.66], # E minor
            'D': [146.83, 164.81, 185.00, 196.00, 220.00, 246.94, 277.18],  # D major
            'E': [164.81, 185.00, 207.65, 220.00, 246.94, 277.18, 311.13]   # E major
        }
        
        # Configurações específicas de chiptune
        self.chiptune_config = {
            'pulse_width': 0.5,        # Duty cycle para square wave
            'vibrato_rate': 6.0,       # Taxa de vibrato (Hz)
            'vibrato_depth': 0.02,     # Profundidade do vibrato
            'arpeggio_speed': 16,      # Velocidade do arpejo (divisões por segundo)
            'echo_delay': 0.125,       # Delay do eco (8th note)
            'echo_feedback': 0.3,      # Feedback do eco
            'channel_volumes': {
                'pulse1': 0.4,         # Canal de melodia principal
                'pulse2': 0.3,         # Canal de harmonias
                'triangle': 0.5,       # Canal de baixo
                'noise': 0.2           # Canal de percussão (não usado na música de fundo)
            }
        }
        
        print("🎵 Sistema de áudio inicializado!")
    
    def generate_wave(self, frequency, duration, wave_type='sine', amplitude=0.5):
        """Gerar onda sonora procedural"""
        frames = int(duration * self.sample_rate)
        arr = np.zeros(frames)
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            if wave_type == 'sine':
                arr[i] = amplitude * np.sin(2 * np.pi * frequency * t)
            elif wave_type == 'square':
                arr[i] = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
            elif wave_type == 'sawtooth':
                arr[i] = amplitude * (2 * (t * frequency - np.floor(t * frequency + 0.5)))
            elif wave_type == 'triangle':
                arr[i] = amplitude * (2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1)
            elif wave_type == 'noise':
                arr[i] = amplitude * random.uniform(-1, 1)
        
        return arr
    
    def apply_envelope(self, wave, attack=0.05, decay=0.1, sustain=0.6, release=0.25):
        """Aplicar envelope ADSR à onda com transições mais suaves"""
        length = len(wave)
        envelope = np.ones(length)
        
        # Attack mais suave
        attack_samples = int(attack * length)
        if attack_samples > 0:
            attack_curve = np.power(np.linspace(0, 1, attack_samples), 0.5)  # Curva exponencial suave
            envelope[:attack_samples] = attack_curve
        
        # Decay suave
        decay_samples = int(decay * length)
        if decay_samples > 0:
            start_idx = attack_samples
            end_idx = min(start_idx + decay_samples, length)
            decay_curve = np.power(np.linspace(1, sustain, end_idx - start_idx), 2)
            envelope[start_idx:end_idx] = decay_curve
        
        # Sustain (mantém o nível)
        sustain_start = attack_samples + decay_samples
        sustain_end = max(sustain_start, length - int(release * length))
        envelope[sustain_start:sustain_end] = sustain
        
        # Release muito suave
        release_samples = int(release * length)
        if release_samples > 0:
            start_idx = max(0, length - release_samples)
            release_curve = np.power(np.linspace(envelope[start_idx], 0, length - start_idx), 2)
            envelope[start_idx:] = release_curve
        
        return wave * envelope
    
    def remove_dc_offset(self, wave):
        """Remover DC offset (componente contínua) da onda"""
        if len(wave) > 0:
            dc_offset = np.mean(wave)
            wave = wave - dc_offset
        return wave
    
    def apply_noise_gate(self, wave, threshold=None):
        """Aplicar gate de ruído para eliminar sinais muito baixos"""
        if threshold is None:
            threshold = self.noise_gate_threshold
        
        # Calcular RMS (Root Mean Square) para detecção de sinal
        window_size = int(0.01 * self.sample_rate)  # 10ms window
        gated_wave = np.copy(wave)
        
        for i in range(0, len(wave) - window_size, window_size):
            window = wave[i:i + window_size]
            rms = np.sqrt(np.mean(window ** 2))
            
            if rms < threshold:
                # Fade suave para zero ao invés de corte abrupto
                fade_samples = min(window_size // 4, len(gated_wave) - i)
                if fade_samples > 0:
                    fade = np.linspace(1, 0, fade_samples)
                    gated_wave[i:i + fade_samples] *= fade
                    gated_wave[i + fade_samples:i + window_size] = 0
        
        return gated_wave
    
    def apply_soft_clipping(self, wave, threshold=0.95):
        """Aplicar soft clipping para evitar distorção digital"""
        # Soft clipping usando tanh para transições suaves
        clipped = np.where(np.abs(wave) > threshold,
                          np.sign(wave) * threshold * np.tanh(np.abs(wave) / threshold),
                          wave)
        return clipped
    
    def apply_dithering(self, wave):
        """Aplicar dithering para reduzir ruído de quantização"""
        if self.dither_amount > 0:
            dither_noise = np.random.uniform(-self.dither_amount, self.dither_amount, len(wave))
            wave = wave + dither_noise
        return wave
    
    def apply_professional_processing(self, wave):
        """Aplicar processamento profissional completo"""
        # 1. Remover DC offset
        if self.dc_offset_removal:
            wave = self.remove_dc_offset(wave)
        
        # 2. Aplicar filtro passa-baixa
        wave = self.apply_low_pass_filter(wave, 8000)
        
        # 3. Aplicar soft clipping
        wave = self.apply_soft_clipping(wave, 0.9)
        
        # 4. Aplicar gate de ruído
        wave = self.apply_noise_gate(wave)
        
        # 5. Aplicar dithering
        wave = self.apply_dithering(wave)
        
        # 6. Normalização final suave
        wave = self.normalize_wave(wave, 0.7)
        
        return wave
    
    def apply_low_pass_filter(self, wave, cutoff_freq=8000):
        """Aplicar filtro passa-baixa profissional para remover ruídos agudos"""
        nyquist = self.sample_rate / 2
        if cutoff_freq >= nyquist:
            return wave
        
        # Filtro Butterworth de primeira ordem simulado
        alpha = cutoff_freq / (cutoff_freq + nyquist)
        filtered_wave = np.zeros_like(wave)
        
        if len(wave) > 0:
            filtered_wave[0] = wave[0] * alpha
            for i in range(1, len(wave)):
                filtered_wave[i] = alpha * wave[i] + (1 - alpha) * filtered_wave[i-1]
        
        return filtered_wave
    
    def normalize_wave(self, wave, target_amplitude=0.8):
        """Normalizar onda com controle de amplitude"""
        max_val = np.max(np.abs(wave))
        if max_val > 0:
            wave = wave / max_val * target_amplitude
        return wave
    
    def add_reverb(self, wave, delay=0.2, feedback=0.2, mix=0.15):
        """Adicionar reverb suave à onda"""
        delay_samples = int(delay * self.sample_rate)
        reverb_wave = np.zeros(len(wave) + delay_samples)
        reverb_wave[:len(wave)] = wave
        
        # Adicionar ecos com feedback mais suave
        for i in range(len(wave)):
            if i + delay_samples < len(reverb_wave):
                reverb_wave[i + delay_samples] += wave[i] * feedback
        
        # Mixar com original (menos reverb para menos ruído)
        final_wave = np.zeros(len(reverb_wave))
        final_wave[:len(wave)] = wave * (1 - mix)
        final_wave += reverb_wave * mix
        
        return final_wave[:len(wave)]  # Manter tamanho original
        """Adicionar reverb à onda"""
        delay_samples = int(delay * self.sample_rate)
        reverb_wave = np.zeros(len(wave) + delay_samples)
        reverb_wave[:len(wave)] = wave
        
        # Adicionar ecos com feedback
        for i in range(len(wave)):
            if i + delay_samples < len(reverb_wave):
                reverb_wave[i + delay_samples] += wave[i] * feedback
        
        # Mixar com original
        final_wave = np.zeros(len(reverb_wave))
        final_wave[:len(wave)] = wave * (1 - mix)
        final_wave += reverb_wave * mix
        
        return final_wave[:len(wave)]  # Manter tamanho original
    
    def create_chord(self, root_freq, chord_type='major', duration=1.0):
        """Criar acorde procedural mais suave"""
        if chord_type == 'major':
            intervals = [1.0, 1.25, 1.5]  # Tônica, terça maior, quinta
        elif chord_type == 'minor':
            intervals = [1.0, 1.2, 1.5]   # Tônica, terça menor, quinta
        elif chord_type == 'dim':
            intervals = [1.0, 1.2, 1.4]   # Diminuto
        else:
            intervals = [1.0, 1.25, 1.5]
        
        chord_wave = np.zeros(int(duration * self.sample_rate))
        
        for interval in intervals:
            freq = root_freq * interval
            # Usar sine para acordes mais suaves
            note_wave = self.generate_wave(freq, duration, 'sine', 0.2)  # Amplitude menor
            note_wave = self.apply_envelope(note_wave, 0.1, 0.1, 0.7, 0.3)
            chord_wave += note_wave
        
        # Filtrar para suavizar
        chord_wave = self.apply_low_pass_filter(chord_wave, 4000)
        
        return chord_wave / len(intervals)  # Normalizar
    
    def create_laser_sound(self):
        """Som de tiro laser estilo arcade mais limpo e profissional"""
        duration = 0.1
        start_freq = 500
        end_freq = 120
        
        frames = int(duration * self.sample_rate)
        wave = np.zeros(frames)
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            progress = i / frames
            freq = start_freq + (end_freq - start_freq) * progress
            
            # Onda principal mais limpa com menos harmônicos
            wave[i] = (0.8 * np.sin(2 * np.pi * freq * t) +
                      0.15 * np.sin(2 * np.pi * freq * 2 * t) +
                      0.05 * np.sin(2 * np.pi * freq * 3 * t))
        
        # Envelope mais suave
        wave = self.apply_envelope(wave, 0.01, 0.05, 0.3, 0.7)
        
        # Aplicar processamento profissional
        wave = self.apply_professional_processing(wave)
        
        return self.wave_to_pygame_sound(wave)
    
    def create_explosion_sound(self):
        """Som de explosão procedural ultra-limpo"""
        duration = 0.5
        frames = int(duration * self.sample_rate)
        
        # Usar apenas frequências baixas controladas ao invés de ruído
        low_freq = self.generate_wave(50, duration, 'sine', 0.6)
        mid_freq = self.generate_wave(100, duration, 'triangle', 0.3)
        punch = self.generate_wave(80, duration * 0.1, 'square', 0.4)  # Punch inicial curto
        
        # Criar envelope de punch
        punch_padded = np.zeros(frames)
        punch_padded[:len(punch)] = punch
        
        wave = low_freq + mid_freq + punch_padded
        
        # Envelope de explosão ultra-suave
        wave = self.apply_envelope(wave, 0.001, 0.1, 0.2, 0.8)
        
        # Aplicar processamento profissional
        wave = self.apply_professional_processing(wave)
        
        return self.wave_to_pygame_sound(wave)
    
    def create_enemy_hit_sound(self):
        """Som de acerto no inimigo procedural ultra-limpo"""
        duration = 0.15
        
        # Som metálico usando apenas ondas puras
        metallic1 = self.generate_wave(800, duration, 'sine', 0.4)
        metallic2 = self.generate_wave(1200, duration, 'triangle', 0.3)
        impact = self.generate_wave(400, duration * 0.5, 'square', 0.2)  # Impacto curto
        
        # Padding para o impacto
        frames = int(duration * self.sample_rate)
        impact_padded = np.zeros(frames)
        impact_padded[:len(impact)] = impact
        
        wave = metallic1 + metallic2 + impact_padded
        
        # Envelope de impacto rápido
        wave = self.apply_envelope(wave, 0.001, 0.02, 0.03, 0.1)
        
        # Aplicar processamento profissional
        wave = self.apply_professional_processing(wave)
        
        return self.wave_to_pygame_sound(wave)
    
    def create_powerup_sound(self):
        """Som de power-up coletado"""
        duration = 0.6
        
        # Arpejo ascendente
        notes = [261.63, 329.63, 392.00, 523.25]  # C, E, G, C oitava acima
        note_duration = duration / len(notes)
        
        full_wave = np.array([])
        
        for note_freq in notes:
            note_wave = self.generate_wave(note_freq, note_duration, 'sine', 0.4)
            note_wave = self.apply_envelope(note_wave, 0.05, 0.1, 0.8, 0.2)
            full_wave = np.concatenate([full_wave, note_wave])
        
        # Adicionar reverb
        full_wave = self.add_reverb(full_wave, 0.2, 0.4, 0.3)
        
        return self.wave_to_pygame_sound(full_wave)
    
    def create_engine_sound(self):
        """Som de motor procedural ultra-limpo"""
        duration = 2.0
        
        # Som de motor usando apenas ondas puras
        base_freq = self.generate_wave(120, duration, 'sine', 0.3)
        harmonic1 = self.generate_wave(180, duration, 'triangle', 0.2)
        harmonic2 = self.generate_wave(240, duration, 'sine', 0.1)
        
        # Pequenas variações suaves na frequência
        vibrato = np.sin(np.linspace(0, 8 * np.pi, int(duration * self.sample_rate))) * 0.05
        base_freq = base_freq * (1 + vibrato)
        
        wave = base_freq + harmonic1 + harmonic2
        
        # Envelope muito suave para motor contínuo
        wave = self.apply_envelope(wave, 0.2, 1.6, 1.0, 0.2)
        
        # Aplicar processamento profissional
        wave = self.apply_professional_processing(wave)
        
        return self.wave_to_pygame_sound(wave)
    
    def create_background_music(self, track_number=0):
        """Criar música de fundo estilo chiptune/8-bit clássico"""
        track_info = self.chiptune_progressions[track_number % len(self.chiptune_progressions)]
        
        duration = 16.0  # 16 segundos por track
        tempo = track_info['tempo']
        chord_progression = track_info['chords']
        melody_pattern = track_info['melody_pattern']
        bass_pattern = track_info['bass_pattern']
        
        # Calcular duração de cada acorde (4 acordes por 16 segundos = 4 segundos cada)
        chord_duration = duration / len(chord_progression)
        
        full_track = np.array([])
        
        for i, chord_name in enumerate(chord_progression):
            # Canal 1: Melodia principal (Pulse Wave)
            melody_wave = self.create_chiptune_melody(
                self.chiptune_scales[chord_name], 
                melody_pattern, 
                chord_duration,
                'pulse1'
            )
            
            # Canal 2: Harmonias (Pulse Wave com duty cycle diferente)
            harmony_wave = self.create_chiptune_harmony(
                self.chiptune_scales[chord_name], 
                chord_duration,
                'pulse2'
            )
            
            # Canal 3: Linha de baixo (Triangle Wave)
            bass_freq = self.chiptune_scales[chord_name][bass_pattern[i % len(bass_pattern)]]
            bass_wave = self.create_chiptune_bass(bass_freq, chord_duration)
            
            # Normalizar tamanhos
            min_length = min(len(melody_wave), len(harmony_wave), len(bass_wave))
            melody_wave = melody_wave[:min_length]
            harmony_wave = harmony_wave[:min_length]
            bass_wave = bass_wave[:min_length]
            
            # Combinar canais com volumes balanceados (estilo NES)
            combined = (
                melody_wave * self.chiptune_config['channel_volumes']['pulse1'] +
                harmony_wave * self.chiptune_config['channel_volumes']['pulse2'] +
                bass_wave * self.chiptune_config['channel_volumes']['triangle']
            )
            
            full_track = np.concatenate([full_track, combined])
        
        # Aplicar processamento profissional e volume baixo para fundo
        if np.max(np.abs(full_track)) > 0:
            full_track = self.apply_professional_processing(full_track)
            full_track *= 0.25  # Volume baixo para música de fundo
        
        return self.wave_to_pygame_sound(full_track)
    
    def create_chiptune_melody(self, scale, pattern, duration, channel):
        """Criar melodia principal estilo chiptune com pulse wave"""
        note_duration = duration / len(pattern)
        melody = np.array([])
        
        for note_index in pattern:
            freq = scale[note_index % len(scale)]
            
            # Gerar pulse wave com duty cycle específico
            note_wave = self.generate_pulse_wave(freq, note_duration, 0.25)  # 25% duty cycle
            
            # Adicionar vibrato sutil (característica do chiptune)
            vibrato = np.sin(np.linspace(0, self.chiptune_config['vibrato_rate'] * 2 * np.pi, 
                                       int(note_duration * self.sample_rate))) 
            vibrato *= self.chiptune_config['vibrato_depth']
            note_wave = note_wave * (1 + vibrato)
            
            # Envelope rápido típico de chiptune
            note_wave = self.apply_envelope(note_wave, 0.001, 0.05, 0.8, 0.1)
            
            melody = np.concatenate([melody, note_wave])
        
        return melody
    
    def create_chiptune_harmony(self, scale, duration, channel):
        """Criar harmonias estilo chiptune com pulse wave diferente"""
        # Criar harmonias simples com terças e quintas
        harmony_pattern = [2, 4, 1, 3]  # Padrão harmônico
        note_duration = duration / len(harmony_pattern)
        harmony = np.array([])
        
        for note_index in harmony_pattern:
            freq = scale[note_index % len(scale)]
            
            # Gerar pulse wave com duty cycle diferente
            note_wave = self.generate_pulse_wave(freq, note_duration, 0.125)  # 12.5% duty cycle
            
            # Envelope mais sustentado para harmonias
            note_wave = self.apply_envelope(note_wave, 0.01, 0.1, 0.6, 0.2)
            
            harmony = np.concatenate([harmony, note_wave])
        
        return harmony
    
    def create_chiptune_bass(self, bass_freq, duration):
        """Criar linha de baixo estilo chiptune com triangle wave"""
        # Padrão rítmico típico de games 8-bit
        bass_pattern = [1, 0.5, 1, 0.5, 1, 0.5, 1, 1]  # Ritmo característico
        beat_duration = duration / len(bass_pattern)
        bass_line = np.array([])
        
        for amplitude in bass_pattern:
            if amplitude > 0:
                # Triangle wave para o baixo (típico do NES)
                beat_wave = self.generate_triangle_wave(bass_freq, beat_duration)
                beat_wave *= amplitude
                
                # Envelope percussivo para cada batida
                beat_wave = self.apply_envelope(beat_wave, 0.001, 0.02, 0.7, 0.1)
            else:
                # Silêncio para criar ritmo
                beat_wave = np.zeros(int(beat_duration * self.sample_rate))
            
            bass_line = np.concatenate([bass_line, beat_wave])
        
        return bass_line
    
    def generate_pulse_wave(self, frequency, duration, duty_cycle=0.5):
        """Gerar pulse wave autêntica estilo 8-bit"""
        frames = int(duration * self.sample_rate)
        wave = np.zeros(frames)
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            phase = (frequency * t) % 1.0
            wave[i] = 1.0 if phase < duty_cycle else -1.0
        
        return wave * 0.5  # Amplitude controlada
    
    def generate_triangle_wave(self, frequency, duration):
        """Gerar triangle wave autêntica estilo 8-bit"""
        frames = int(duration * self.sample_rate)
        wave = np.zeros(frames)
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            phase = (frequency * t) % 1.0
            if phase < 0.5:
                wave[i] = 4 * phase - 1
            else:
                wave[i] = 3 - 4 * phase
        
        return wave * 0.7  # Amplitude típica do triangle
    
    def wave_to_pygame_sound(self, wave_array):
        """Converter array numpy para pygame.mixer.Sound"""
        # Normalizar e converter para int16
        if np.max(np.abs(wave_array)) > 0:
            wave_array = wave_array / np.max(np.abs(wave_array))
        
        wave_int16 = (wave_array * 32767).astype(np.int16)
        
        # Se mono, converter para stereo
        if self.channels == 2:
            stereo_wave = np.zeros((len(wave_int16), 2), dtype=np.int16)
            stereo_wave[:, 0] = wave_int16  # Canal esquerdo
            stereo_wave[:, 1] = wave_int16  # Canal direito
            wave_int16 = stereo_wave
        
        return pygame.sndarray.make_sound(wave_int16)
    
    def play_sound(self, sound_name):
        """Tocar som específico"""
        if sound_name not in self.sound_cache:
            if sound_name == 'laser':
                self.sound_cache[sound_name] = self.create_laser_sound()
            elif sound_name == 'explosion':
                self.sound_cache[sound_name] = self.create_explosion_sound()
            elif sound_name == 'enemy_hit':
                self.sound_cache[sound_name] = self.create_enemy_hit_sound()
            elif sound_name == 'powerup':
                self.sound_cache[sound_name] = self.create_powerup_sound()
            elif sound_name == 'engine':
                self.sound_cache[sound_name] = self.create_engine_sound()
        
        if sound_name in self.sound_cache:
            # Usar canal específico baseado no tipo de som
            if sound_name == 'engine':
                self.ambient_channel.play(self.sound_cache[sound_name], loops=-1)
            else:
                self.sfx_channel.play(self.sound_cache[sound_name])
    
    def start_background_music(self):
        """Iniciar música de fundo em thread separada"""
        if not self.music_running:
            self.music_running = True
            self.music_thread = threading.Thread(target=self._music_loop, daemon=True)
            self.music_thread.start()
    
    def stop_background_music(self):
        """Parar música de fundo"""
        self.music_running = False
        self.music_channel.stop()
    
    def _music_loop(self):
        """Loop da música de fundo"""
        while self.music_running:
            # Criar nova track
            music_sound = self.create_background_music(self.current_track)
            
            # Tocar música
            self.music_channel.play(music_sound)
            
            # Esperar terminar (com check periódico para parar)
            while self.music_channel.get_busy() and self.music_running:
                time.sleep(0.1)
            
            # Próxima track
            self.current_track = (self.current_track + 1) % len(self.chiptune_progressions)
    
    def set_volume(self, volume):
        """Ajustar volume geral"""
        self.volume = max(0.0, min(1.0, volume))
        # Ajustar volume dos canais individuais com levels mais baixos
        try:
            self.music_channel.set_volume(self.volume * 0.3)  # Música bem mais baixa
            self.sfx_channel.set_volume(self.volume * 0.7)    # SFX moderado
            self.ambient_channel.set_volume(self.volume * 0.2)  # Ambiente muito baixo
        except:
            pass  # Ignorar se mixer não estiver inicializado
    
    def cleanup(self):
        """Limpar recursos de áudio"""
        try:
            self.stop_background_music()
        except:
            pass  # Ignorar erros ao parar música
        
        try:
            pygame.mixer.quit()
        except:
            pass  # Ignorar se mixer já foi finalizado