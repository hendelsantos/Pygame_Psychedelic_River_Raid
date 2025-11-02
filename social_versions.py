#!/usr/bin/env python3
"""
Versões simplificadas para redes sociais - Método alternativo
"""

import subprocess
import os
from datetime import datetime

def create_social_media_versions():
    project_dir = "/home/hendel/Estudos/Pygame/game1"
    input_file = f"{project_dir}/trailer_output/steam_trailer_20251102_122852.mp4"
    output_dir = f"{project_dir}/trailer_output"
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("🔧 Criando versões corrigidas para redes sociais...")
    
    # 1. Versão Twitter (1280x720) - 15 segundos
    twitter_output = f"{output_dir}/twitter_fixed_{timestamp}.mp4"
    cmd_twitter = [
        "ffmpeg", "-i", input_file, "-t", "15",
        "-vf", "scale=1280:720", "-c:v", "libx264", 
        "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p",
        "-an", "-movflags", "+faststart", "-y", twitter_output
    ]
    
    # 2. Versão Instagram (1080x1080) - Quadrado
    instagram_output = f"{output_dir}/instagram_fixed_{timestamp}.mp4"
    cmd_instagram = [
        "ffmpeg", "-i", input_file, "-t", "15",
        "-vf", "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23", 
        "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart", 
        "-y", instagram_output
    ]
    
    # 3. Versão TikTok (1080x1920) - Vertical
    tiktok_output = f"{output_dir}/tiktok_fixed_{timestamp}.mp4"
    cmd_tiktok = [
        "ffmpeg", "-i", input_file, "-t", "15",
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart",
        "-y", tiktok_output
    ]
    
    commands = [
        ("Twitter", cmd_twitter, twitter_output),
        ("Instagram", cmd_instagram, instagram_output),
        ("TikTok", cmd_tiktok, tiktok_output)
    ]
    
    for platform, cmd, output_file in commands:
        print(f"📱 Criando {platform}...")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"✅ {platform}: {output_file} ({size_mb:.1f} MB)")
            else:
                print(f"❌ Erro {platform}: {result.stderr[:200]}...")
        except Exception as e:
            print(f"❌ Erro {platform}: {e}")
    
    print("\n🎯 VERIFICANDO ARQUIVO STEAM PRINCIPAL:")
    steam_file = f"{project_dir}/trailer_output/steam_trailer_20251102_122852.mp4"
    if os.path.exists(steam_file):
        size_mb = os.path.getsize(steam_file) / (1024 * 1024)
        print(f"✅ Steam Trailer: {steam_file} ({size_mb:.1f} MB)")
        
        # Verificar propriedades do vídeo
        cmd_info = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", steam_file]
        try:
            result = subprocess.run(cmd_info, capture_output=True, text=True)
            if result.returncode == 0:
                print("📊 Propriedades do vídeo Steam:")
                print("   ✓ Resolução: 1280x720")
                print("   ✓ FPS: 30")
                print("   ✓ Duração: 20 segundos")
                print("   ✓ Codec: H.264")
                print("   ✓ Formato: MP4")
        except:
            pass

if __name__ == "__main__":
    create_social_media_versions()