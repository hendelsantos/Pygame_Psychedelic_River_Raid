#!/usr/bin/env python3
"""
Captura gameplay real - inicia jogo e grava ao mesmo tempo
"""

import subprocess
import time
import os
from datetime import datetime

def capture_real_gameplay():
    project_dir = "/home/hendel/Estudos/Pygame/game1"
    output_dir = f"{project_dir}/trailer_output"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{output_dir}/GAMEPLAY_REAL_{timestamp}.mp4"
    
    print("🎮 Iniciando captura de gameplay REAL...")
    print("⚠️  ATENÇÃO: O jogo vai abrir, jogue por 30 segundos!")
    print("🎯 Mova a nave, atire nos inimigos, mostre o jogo!")
    print()
    
    # Countdown
    for i in range(3, 0, -1):
        print(f"⏰ Iniciando em {i}...")
        time.sleep(1)
    
    print("🚀 INICIANDO AGORA!")
    
    # Comando FFmpeg para capturar
    ffmpeg_cmd = [
        "ffmpeg",
        "-f", "x11grab",
        "-r", "30",                    # 30 FPS
        "-s", "800x600",               # Tamanho da tela do jogo
        "-i", ":0.0",                  # Display
        "-t", "30",                    # 30 segundos
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",                  # Boa qualidade
        "-pix_fmt", "yuv420p",
        "-y",
        output_file
    ]
    
    # Comando para iniciar o jogo
    game_cmd = ["python", "game.py"]
    
    try:
        print("🎬 Iniciando captura...")
        
        # Iniciar jogo
        game_process = subprocess.Popen(game_cmd, cwd=project_dir)
        
        # Esperar um pouco para o jogo abrir
        time.sleep(2)
        
        # Iniciar captura
        capture_process = subprocess.run(ffmpeg_cmd, 
                                       capture_output=True, 
                                       text=True,
                                       cwd=project_dir)
        
        # Terminar o jogo
        game_process.terminate()
        game_process.wait()
        
        if capture_process.returncode == 0:
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"✅ Gameplay capturado: {output_file}")
            print(f"📊 Tamanho: {size_mb:.1f} MB")
            return output_file
        else:
            print(f"❌ Erro na captura: {capture_process.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def create_final_trailers(gameplay_file):
    """Criar trailers finais usando o gameplay real"""
    if not gameplay_file:
        return
        
    output_dir = "/home/hendel/Estudos/Pygame/game1/trailer_output"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("\n🎬 Criando trailers finais...")
    
    # Steam trailer (20 segundos, melhores momentos)
    steam_file = f"{output_dir}/STEAM_FINAL_{timestamp}.mp4"
    cmd_steam = [
        "ffmpeg", "-i", gameplay_file,
        "-ss", "5", "-t", "20",  # Pular primeiros 5s, pegar 20s
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart",
        "-y", steam_file
    ]
    
    # WhatsApp trailer (15 segundos, compacto)
    whatsapp_file = f"{output_dir}/WHATSAPP_FINAL_{timestamp}.mp4"
    cmd_whatsapp = [
        "ffmpeg", "-i", gameplay_file,
        "-ss", "8", "-t", "15",  # Melhores 15 segundos
        "-vf", "scale=720:480",
        "-c:v", "libx264", "-preset", "fast", "-crf", "25",
        "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart",
        "-y", whatsapp_file
    ]
    
    trailers = [
        ("🎮 STEAM FINAL", cmd_steam, steam_file),
        ("📱 WHATSAPP FINAL", cmd_whatsapp, whatsapp_file)
    ]
    
    for name, cmd, output in trailers:
        print(f"{name}...")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                size_mb = os.path.getsize(output) / (1024 * 1024)
                print(f"✅ {name}: {os.path.basename(output)} ({size_mb:.1f} MB)")
            else:
                print(f"❌ Erro {name}: {result.stderr[:200]}...")
        except Exception as e:
            print(f"❌ Erro {name}: {e}")

if __name__ == "__main__":
    print("🎯 CAPTURA DE GAMEPLAY REAL")
    print("="*50)
    
    gameplay_file = capture_real_gameplay()
    
    if gameplay_file:
        create_final_trailers(gameplay_file)
        print("\n🎉 PROCESSO COMPLETO!")
        print("📁 Verifique a pasta trailer_output/")
    else:
        print("\n❌ Falha na captura. Tente novamente.")