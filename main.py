import customtkinter as ctk
import yt_dlp
import os
import glob
import time
import threading
import sys
import zipfile
import urllib.request
from PIL import Image

# --- CONFIGURAÇÃO VISUAL PREMIUM ---
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("green") 

# --- CAMINHOS SEGUROS PARA EXECUTÁVEL (MEIPASS) ---
def resource_path(relative_path):
    """Pega o caminho absoluto escondido no _MEIPASS do executável PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# --- ROTINA DE AUTOINSTALAÇÃO DO FFMPEG ---
def get_ffmpeg_dir():
    # Usa a pasta de AppData livre de restrições de permissão do Windows
    import os
    app_data = os.path.join(os.getenv('APPDATA', os.path.expanduser('~')), 'NexusTube')
    os.makedirs(app_data, exist_ok=True)
    return app_data

def checar_ffmpeg_e_instalar():
    # Verifica onde estamos rodando. Se for executável, vamos injetar do lado dele
    exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.abspath(".")
    ffmpeg_cmd = "ffmpeg.exe"
    
    # Se ffmpeg normal estiver do lado do executável:
    if os.path.exists(os.path.join(exe_dir, ffmpeg_cmd)):
        return exe_dir
        
    # Se não está do lado, verifica na pasta oculta do usuário AppData
    app_data_dir = get_ffmpeg_dir()
    if os.path.exists(os.path.join(app_data_dir, ffmpeg_cmd)):
        return app_data_dir
        
    return None # não achou

def baixar_ffmpeg(status_label, progress_bar, download_btn):
    # Força o Autodownload a jogar o ffmpeg.exe na pasta livre de bloqueios
    exe_dir = get_ffmpeg_dir()
    
    status_label.configure(text="Iniciando Autoinstalador Oculto...\nBaixando motores gráficos nativos FFMPEG (1080p)...", text_color="#FF9800")
    download_btn.configure(state="disabled", text="Instalando...")
    progress_bar.set(0)
    
    # Baixando pacote mais enxuto oficial do Windows FFMPEG da Github release BtbN
    url_ffmpeg = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    zip_path = os.path.join(exe_dir, "ffmpeg.zip")
    
    try:
        def reporthook(count, block_size, total_size):
            if total_size > 0:
                calc = (count * block_size) / total_size
                if calc <= 1:
                    progress_bar.set(calc)
                    status_label.configure(text=f"Ajustando Motores de Renderização... {calc*100:.1f}%")

        urllib.request.urlretrieve(url_ffmpeg, zip_path, reporthook)
        
        status_label.configure(text="Extraindo componentes vitais do Zip...", text_color="#00BCD4")
        progress_bar.set(0.5)
        
        # Descompactar apenas o exe super rápido para a raiz do disco (apenas o que importa)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for membro in zip_ref.namelist():
                if membro.endswith('ffmpeg.exe'):
                    fonte = zip_ref.open(membro)
                    target = open(os.path.join(exe_dir, 'ffmpeg.exe'), 'wb')
                    with fonte, target:
                        target.write(fonte.read())
                    break
        
        progress_bar.set(1.0)
        status_label.configure(text="Motores instalados com sucesso!\nO Sistema está pronto para a ação.", text_color="#00E676")
        time.sleep(2)
        
    except Exception as e:
        status_label.configure(text="Erro ao baixar pacotes vitais. Certifique conexão ou instale FFMPEG manualmente.", text_color="red")
        print(f"Erro Autoinstalador: {e}")
    finally:
        # Destruir provas (zip lixo)
        if os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except:
                pass
            
        progress_bar.set(0)
        status_label.configure(text="")
        download_btn.configure(state="normal", text="B A I X A R   V Í D E O")
    
    return exe_dir

# --- LÓGICA DE FEEDBACK (BARRA DE PROGRESSO) ---
def atualizar_progresso(d):
    """Lê os dados ao vivo do yt_dlp e envia para a barra gráfica da interface."""
    if d['status'] == 'downloading':
        try:
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            baixado = d.get('downloaded_bytes', 0)
            
            if total and total > 0:
                percentual = baixado / total
                progress_bar.set(percentual)
                
                velocidade = d.get('speed')
                vel_str = f"{(velocidade / 1024 / 1024):.1f} MB/s" if velocidade else "..."
                
                texto = f"Baixando... {percentual * 100:.1f}%  (Velocidade: {vel_str})"
                status_label.configure(text=texto, text_color="#00E676")
        except:
            pass

    elif d['status'] == 'finished':
        progress_bar.set(1.0)
        status_label.configure(text="Download 100%! Finalizando renderização do processo...", text_color="#FF9800")


# --- LÓGICA DE DOWNLOAD ---
def executar_script(url):
    caminho_downloads = os.path.join(os.path.expanduser('~'), 'Downloads')

    # 1. VERIFICAÇÃO INTELIGENTE DO MOTOR GRÁFICO (AUTOMAÇÃO FFMPEG)
    ffmpeg_dir = checar_ffmpeg_e_instalar()
    if not ffmpeg_dir:
        # Entra na rotina de Auto-download na Tela. Ele tranca a thread até salvar o executavel.
        ffmpeg_dir = baixar_ffmpeg(status_label, progress_bar, download_btn)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(caminho_downloads, '%(title)s.%(ext)s'),
        'nopart': True,
        'progress_hooks': [atualizar_progresso],
        'ffmpeg_location': ffmpeg_dir
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            status_label.configure(text="Conectando aos servidores do Nexus...", text_color="#2196F3")
            info = ydl.extract_info(url, download=True)
            titulo = info.get('title', 'Vídeo concluído!')
            
            status_label.configure(text="Aplicando polimento final e limpando buffers...", text_color="#FF9800")
            time.sleep(2)
            caminho_limpeza = os.path.join(caminho_downloads, "*.m4a")
            for temp_audio in glob.glob(caminho_limpeza):
                try:
                    os.remove(temp_audio)
                except:
                    pass
            
            mensagem = f"Missão Cumprida!\n« {titulo} »\nAcesso liberado na sua pasta Downloads!"
            status_label.configure(text=mensagem, text_color="#00E676")
            
    except Exception as e:
        error_msg = str(e).split('\n')[0] # Pega a primeira linha
        status_label.configure(text=f"A Anomalia impediu o download!\nErro Real: {error_msg[:80]}", text_color="#FF5252")
        print(f"Erro detalhado: {e}")
        
    finally:
        download_btn.configure(state="normal", text="B A I X A R   V Í D E O")
        progress_bar.set(0)

def iniciar_download():
    url = url_entry.get()
    
    if not url.strip():
        status_label.configure(text="⚠️ Por favor, insira um link de coordenadas válido do YouTube!", text_color="#FF5252")
        return
        
    status_label.configure(text="Iniciando cálculos da matriz, por favor aguarde...", text_color="#B0BEC5")
    download_btn.configure(state="disabled", text="Construindo...")
    progress_bar.set(0)

    # Roda em background
    threading.Thread(target=executar_script, args=(url,), daemon=True).start()

# --- CONSTRUÇÃO DA JANELA ESTILIZADA ---
app = ctk.CTk()
app.title("NexusTube Downloader")

# --- CONFIGURAÇÃO DE ÍCONES (Janela e Barra de Tarefas) ---
icon_path = resource_path("app_icon.ico")
if os.path.exists(icon_path):
    # Aplica na janela (CTk e Tkinter nativo)
    try:
        app.wm_iconbitmap(icon_path)
    except:
        pass
    try:
        app.iconbitmap(icon_path)
    except:
        pass
    
    # Taskbar icon fix on Windows
    try:
        import ctypes
        myappid = 'nexustube.downloader.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception as e:
        print(f"Erro ao definir ícone da barra de tarefas: {e}")
else:
    print(f"ATENÇÃO: Ícone não encontrado no caminho -> {icon_path}")

# Faz a janela abrir ocupando a tela toda agressivamente
largura = app.winfo_screenwidth()
altura = app.winfo_screenheight()
app.geometry(f"{largura}x{altura}+0+0")
app.after(100, lambda: app.state('zoomed'))

# --- BACKGROUND IMAGEM DE ALTA DEFINIÇÃO SEVERA ---
# Usa a rota do executável blindado para puxar a imagem empacotada
bg_path = resource_path("bg.png")

if os.path.exists(bg_path):
    try:
        img_original = Image.open(bg_path)
        img_fundo = ctk.CTkImage(light_image=img_original, dark_image=img_original, size=(largura, altura))
        bg_label = ctk.CTkLabel(app, text="", image=img_fundo)
        bg_label.place(relx=0.5, rely=0.5, anchor="center")
    except Exception as e:
        print(f"Não foi possível carregar a imagem de fundo blindada: {e}")

# Container Principal (Painel central flutuante para a tela grande)
frame = ctk.CTkFrame(app, corner_radius=25, fg_color="#1E1E1E", border_width=1, border_color="#333333", width=800, height=580)
frame.place(relx=0.5, rely=0.5, anchor="center")
frame.pack_propagate(False) 

# Títulos (Proporções Maiores para Desktop) - Nome Novo
title_label = ctk.CTkLabel(frame, text="N E X U S   T U B E", font=ctk.CTkFont(family="Inter", size=32, weight="bold"), text_color="#00E676")
title_label.pack(pady=(55, 10))

subtitle = ctk.CTkLabel(frame, text="Sistema de Extração em Nível Quântico (1080p+)", font=ctk.CTkFont(size=14, slant="italic"), text_color="#9E9E9E")
subtitle.pack(pady=(0, 40))

# Campo de Input (Largo e Expandido)
url_entry = ctk.CTkEntry(
    frame, 
    placeholder_text="Cole as coordenadas web aqui... (ex: https://youtu.be/...)", 
    width=600, 
    height=60, 
    font=ctk.CTkFont(size=16),
    corner_radius=12,
    border_color="#424242",
    fg_color="#121212"
)
url_entry.pack(pady=15)

# Botão Baixar (Destacão e Encorpado)
download_btn = ctk.CTkButton(
    frame, 
    text="B A I X A R   V Í D E O", 
    height=60, 
    width=350, 
    font=ctk.CTkFont(size=18, weight="bold"), 
    corner_radius=12,
    fg_color="#00C853",
    hover_color="#00E676",
    text_color="#000000",
    command=iniciar_download
)
download_btn.pack(pady=30)

# Barra de Progresso Visível
progress_bar = ctk.CTkProgressBar(frame, width=600, height=18, corner_radius=8, progress_color="#00E676", fg_color="#1A1A1A")
progress_bar.set(0)
progress_bar.pack(pady=20)

# Letreiro de Feedback e de Velocidade
status_label = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=16, weight="bold"))
status_label.pack(pady=(10, 20))

if __name__ == "__main__":
    app.mainloop()
