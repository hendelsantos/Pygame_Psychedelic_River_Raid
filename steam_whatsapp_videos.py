#!/usr/bin/env python3
"""
Criar versões específicas para Steam e WhatsApp
"""

import subprocess
import os
from datetime import datetime

def create_steam_whatsapp_versions():
    project_dir = "/home/hendel/Estudos/Pygame/game1"
    input_file = f"{project_dir}/trailer_output/steam_trailer_20251102_122852.mp4"
    output_dir = f"{project_dir}/trailer_output"
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("🎮 Criando versões para STEAM e WHATSAPP...")
    
    # 1. STEAM OFICIAL - HD com qualidade máxima
    steam_final = f"{output_dir}/STEAM_OFICIAL_{timestamp}.mp4"
    cmd_steam = [
        "ffmpeg", "-i", input_file,
        
        # Melhor qualidade para Steam
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264",
        "-preset", "veryslow",  # Máxima qualidade
        "-crf", "18",           # Qualidade alta
        "-pix_fmt", "yuv420p",
        "-profile:v", "main",
        "-level", "4.0",
        
        # Sem áudio por enquanto
        "-an",
        
        # Otimização para web
        "-movflags", "+faststart",
        
        "-y", steam_final
    ]
    
    # 2. WHATSAPP - Arquivo pequeno, boa qualidade
    whatsapp_file = f"{output_dir}/WHATSAPP_{timestamp}.mp4"
    cmd_whatsapp = [
        "ffmpeg", "-i", input_file,
        
        # Resolução menor para WhatsApp (limite 16MB)
        "-vf", "scale=720:480",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "28",  # Compressão maior
        "-pix_fmt", "yuv420p",
        
        # Reduzir duração para 15s
        "-t", "15",
        
        "-an",
        "-movflags", "+faststart",
        
        "-y", whatsapp_file
    ]
    
    # 3. STEAM CAPSULE - Versão curta para preview
    steam_capsule = f"{output_dir}/STEAM_CAPSULE_{timestamp}.mp4"
    cmd_capsule = [
        "ffmpeg", "-i", input_file,
        
        # Pegar apenas os melhores 10 segundos
        "-ss", "5", "-t", "10",
        
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        
        "-an",
        "-movflags", "+faststart",
        
        "-y", steam_capsule
    ]
    
    commands = [
        ("🎮 STEAM OFICIAL (1920x1080)", cmd_steam, steam_final),
        ("📱 WHATSAPP (720x480)", cmd_whatsapp, whatsapp_file),
        ("🏷️ STEAM CAPSULE (10s)", cmd_capsule, steam_capsule)
    ]
    
    results = []
    
    for name, cmd, output_file in commands:
        print(f"\n{name}...")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"✅ Criado: {os.path.basename(output_file)} ({size_mb:.1f} MB)")
                results.append((name, output_file, size_mb))
            else:
                print(f"❌ Erro: {result.stderr[:200]}...")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    print("\n" + "="*60)
    print("🎯 RESUMO DOS VÍDEOS CRIADOS:")
    print("="*60)
    
    for name, filepath, size in results:
        filename = os.path.basename(filepath)
        print(f"{name}")
        print(f"   📄 Arquivo: {filename}")
        print(f"   💾 Tamanho: {size:.1f} MB")
        
        if "STEAM_OFICIAL" in filename:
            print("   🎮 Uso: Upload principal para Steam Store")
            print("   📐 Resolução: 1920x1080 (Full HD)")
            
        elif "WHATSAPP" in filename:
            print("   📱 Uso: Compartilhar no WhatsApp/Telegram")
            print("   📐 Resolução: 720x480 (otimizado para mobile)")
            print("   ⚡ Limite WhatsApp: <16MB ✓")
            
        elif "CAPSULE" in filename:
            print("   🏷️ Uso: Preview/thumbnail para Steam")
            print("   📐 Resolução: 1920x1080 (10 segundos)")
            
        print()
    
    print("📍 LOCALIZAÇÃO: /home/hendel/Estudos/Pygame/game1/trailer_output/")
    print("\n🚀 PRONTO PARA USAR!")

if __name__ == "__main__":
    create_steam_whatsapp_versions()