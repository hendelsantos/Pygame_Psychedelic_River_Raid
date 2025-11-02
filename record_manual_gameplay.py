#!/usr/bin/env python3
"""
Gravar gameplay - Você joga, eu gravo!
"""

import subprocess
import time
import os
from datetime import datetime

def record_gameplay():
    print("🎮 GRAVADOR DE GAMEPLAY")
    print("="*50)
    print("📋 INSTRUÇÕES:")
    print("1. Vou abrir o jogo")
    print("2. Você começa a jogar")
    print("3. Quando estiver pronto, aperte ENTER aqui no terminal")
    print("4. Vou gravar 30 segundos do seu gameplay")
    print("5. Continue jogando normalmente!")
    print("="*50)
    
    # Iniciar o jogo
    print("🚀 Iniciando o jogo...")
    game_process = subprocess.Popen(["python", "game.py"])
    
    # Aguardar confirmação do usuário
    print("\n⏳ Jogo iniciado! Comece a jogar...")
    print("⚡ Quando estiver pronto para gravar, pressione ENTER")
    input("   [Pressione ENTER para iniciar gravação]")
    
    # Criar arquivo de saída
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"trailer_output/GAMEPLAY_MANUAL_{timestamp}.mp4"
    
    # Comando de gravação
    ffmpeg_cmd = [
        "ffmpeg",
        "-f", "x11grab",
        "-r", "30",                    # 30 FPS
        "-s", "800x600",               # Tamanho da janela do jogo
        "-i", ":0.0",                  # Display principal
        "-t", "30",                    # Gravar por 30 segundos
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",                  # Boa qualidade
        "-pix_fmt", "yuv420p",
        "-y",                          # Sobrescrever se existir
        output_file
    ]
    
    print("\n🔴 GRAVANDO AGORA! (30 segundos)")
    print("🎯 Continue jogando - mostre suas habilidades!")
    
    # Countdown visual
    for i in range(30, 0, -5):
        print(f"⏰ {i} segundos restantes...")
        time.sleep(5)
    
    try:
        # Iniciar gravação
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"\n✅ GRAVAÇÃO CONCLUÍDA!")
            print(f"📁 Arquivo: {output_file}")
            print(f"📊 Tamanho: {size_mb:.1f} MB")
            return output_file
        else:
            print(f"\n❌ Erro na gravação: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        return None
    
    finally:
        # Fechar o jogo
        print("\n🛑 Fechando o jogo...")
        game_process.terminate()
        game_process.wait()

def create_final_videos(gameplay_file):
    """Criar versões finais para Steam e WhatsApp"""
    if not gameplay_file or not os.path.exists(gameplay_file):
        print("❌ Arquivo de gameplay não encontrado!")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("\n🎬 Criando versões finais...")
    
    # Steam - Full HD, 20 segundos dos melhores momentos
    steam_file = f"trailer_output/STEAM_READY_{timestamp}.mp4"
    cmd_steam = [
        "ffmpeg", "-i", gameplay_file,
        "-ss", "5", "-t", "20",  # Pular primeiros 5s
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-y", steam_file
    ]
    
    # WhatsApp - Compacto, 15 segundos
    whatsapp_file = f"trailer_output/WHATSAPP_READY_{timestamp}.mp4"
    cmd_whatsapp = [
        "ffmpeg", "-i", gameplay_file,
        "-ss", "8", "-t", "15",  # Melhores 15 segundos
        "-vf", "scale=720:480",
        "-c:v", "libx264", "-preset", "fast", "-crf", "25",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-y", whatsapp_file
    ]
    
    # Executar conversões
    conversions = [
        ("🎮 STEAM", cmd_steam, steam_file),
        ("📱 WHATSAPP", cmd_whatsapp, whatsapp_file)
    ]
    
    results = []
    
    for name, cmd, output in conversions:
        print(f"{name}...")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                size_mb = os.path.getsize(output) / (1024 * 1024)
                print(f"✅ {name}: {os.path.basename(output)} ({size_mb:.1f} MB)")
                results.append((name, output, size_mb))
            else:
                print(f"❌ Erro {name}: {result.stderr[:100]}...")
        except Exception as e:
            print(f"❌ Erro {name}: {e}")
    
    return results

def main():
    # Criar pasta se não existir
    os.makedirs("trailer_output", exist_ok=True)
    
    # Gravar gameplay
    gameplay_file = record_gameplay()
    
    if gameplay_file:
        # Criar versões finais
        results = create_final_videos(gameplay_file)
        
        print("\n" + "="*60)
        print("🎉 PROCESSO COMPLETO!")
        print("="*60)
        
        if results:
            print("📁 ARQUIVOS PRONTOS:")
            for name, filepath, size in results:
                filename = os.path.basename(filepath)
                print(f"   {name}: {filename} ({size:.1f} MB)")
        
        print(f"\n📍 Localização: {os.path.abspath('trailer_output')}")
        print("🚀 Seus vídeos estão prontos para usar!")
    else:
        print("\n❌ Falha na gravação. Tente novamente.")

if __name__ == "__main__":
    main()