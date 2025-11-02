#!/usr/bin/env python3
"""
Trailer Editor - Criar trailer final com efeitos para Steam e redes sociais
"""

import subprocess
import os
from datetime import datetime

class TrailerEditor:
    def __init__(self):
        self.project_dir = "/home/hendel/Estudos/Pygame/game1"
        self.input_dir = f"{self.project_dir}/trailer_footage"
        self.output_dir = f"{self.project_dir}/trailer_output"
        
        os.makedirs(self.output_dir, exist_ok=True)
        
    def create_steam_trailer(self, input_video):
        """Cria trailer otimizado para Steam (30s máximo)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{self.output_dir}/steam_trailer_{timestamp}.mp4"
        
        print("🎬 Criando trailer para Steam...")
        
        # FFmpeg command para criar trailer profissional
        cmd = [
            "ffmpeg",
            "-i", input_video,
            
            # Cortar para os melhores 20 segundos (pula primeiros 5s)
            "-ss", "5",
            "-t", "20",
            
            # Filtros de vídeo para melhorar qualidade
            "-vf", (
                "format=yuv420p,"  # Converter para formato compatível
                "scale=1280:720,"  # Resolução HD
                "fps=30,"          # 30 FPS para web
                "eq=contrast=1.2:brightness=0.1:saturation=1.3"  # Melhorar cores
            ),
            
            # Codificação otimizada para web
            "-c:v", "libx264",
            "-preset", "slow",     # Melhor qualidade
            "-crf", "20",          # Alta qualidade
            "-pix_fmt", "yuv420p", # Formato de pixel compatível
            "-profile:v", "main",  # Perfil mais compatível
            "-level", "4.0",
            
            # Sem audio por enquanto (podemos adicionar depois)
            "-an",
            
            # Otimização para streaming
            "-movflags", "+faststart",
            
            "-y",  # Sobrescrever
            output_file
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Trailer Steam criado: {output_file}")
                return output_file
            else:
                print(f"❌ Erro: {result.stderr}")
                return None
        except Exception as e:
            print(f"❌ Erro na criação: {e}")
            return None
    
    def create_social_versions(self, steam_trailer):
        """Cria versões para diferentes redes sociais"""
        if not steam_trailer:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Versões para criar
        versions = {
            "twitter": {
                "size": "1280x720",
                "duration": "15",
                "output": f"{self.output_dir}/twitter_trailer_{timestamp}.mp4"
            },
            "instagram": {
                "size": "1080x1080",  # Quadrado
                "duration": "15",
                "output": f"{self.output_dir}/instagram_trailer_{timestamp}.mp4"
            },
            "tiktok": {
                "size": "1080x1920",  # Vertical
                "duration": "15",
                "output": f"{self.output_dir}/tiktok_trailer_{timestamp}.mp4"
            }
        }
        
        for platform, config in versions.items():
            print(f"📱 Criando versão para {platform.upper()}...")
            
            cmd = [
                "ffmpeg",
                "-i", steam_trailer,
                
                # Duração
                "-t", config["duration"],
                
                # Redimensionar para a plataforma
                "-vf", f"scale={config['size']}:force_original_aspect_ratio=decrease,pad={config['size']}:(ow-iw)/2:(oh-ih)/2:black",
                
                # Codificação otimizada
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "23",
                
                "-an",  # Sem audio
                "-movflags", "+faststart",
                
                "-y",
                config["output"]
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {platform.capitalize()}: {config['output']}")
                else:
                    print(f"❌ Erro {platform}: {result.stderr}")
            except Exception as e:
                print(f"❌ Erro {platform}: {e}")
    
    def create_gif_version(self, steam_trailer):
        """Cria versão GIF para uso em posts"""
        if not steam_trailer:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        gif_output = f"{self.output_dir}/gameplay_preview_{timestamp}.gif"
        
        print("🎞️ Criando GIF animado...")
        
        cmd = [
            "ffmpeg",
            "-i", steam_trailer,
            
            # Pegar apenas 8 segundos
            "-t", "8",
            
            # Filtros para GIF otimizado
            "-vf", "scale=640:480:flags=lanczos,fps=15",
            
            # Reduzir cores para menor tamanho
            "-c:v", "gif",
            
            "-y",
            gif_output
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ GIF criado: {gif_output}")
                return gif_output
            else:
                print(f"❌ Erro GIF: {result.stderr}")
                return None
        except Exception as e:
            print(f"❌ Erro GIF: {e}")
            return None
    
    def process_all(self):
        """Processa todos os vídeos encontrados"""
        # Encontrar vídeos na pasta footage
        video_files = []
        if os.path.exists(self.input_dir):
            for file in os.listdir(self.input_dir):
                if file.endswith(('.mp4', '.avi', '.mov')):
                    video_files.append(os.path.join(self.input_dir, file))
        
        if not video_files:
            print("❌ Nenhum vídeo encontrado em trailer_footage/")
            return
        
        # Usar o vídeo mais recente
        latest_video = max(video_files, key=os.path.getctime)
        print(f"🎥 Processando: {latest_video}")
        
        # 1. Criar trailer principal para Steam
        steam_trailer = self.create_steam_trailer(latest_video)
        
        if steam_trailer:
            # 2. Criar versões para redes sociais
            self.create_social_versions(steam_trailer)
            
            # 3. Criar GIF
            self.create_gif_version(steam_trailer)
        
        print("\n✅ PROCESSAMENTO COMPLETO!")
        print(f"📁 Arquivos salvos em: {self.output_dir}")
        
        # Listar arquivos criados
        if os.path.exists(self.output_dir):
            print("\n📋 ARQUIVOS CRIADOS:")
            for file in sorted(os.listdir(self.output_dir)):
                file_path = os.path.join(self.output_dir, file)
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                print(f"  📄 {file} ({size_mb:.1f} MB)")

if __name__ == "__main__":
    editor = TrailerEditor()
    editor.process_all()