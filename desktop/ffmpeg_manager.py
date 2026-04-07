"""
NexusTube Downloader — Gerenciador FFmpeg
Autoinstalação e verificação do FFmpeg para merge de áudio/vídeo.
"""

import os
import sys
import time
import zipfile
import urllib.request


def resource_path(relative_path):
    """Retorna o caminho absoluto para recursos empacotados pelo PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def get_ffmpeg_dir():
    """Retorna o diretório do FFmpeg em AppData (livre de restrições de permissão)."""
    app_data = os.path.join(
        os.getenv('APPDATA', os.path.expanduser('~')),
        'NexusTube'
    )
    os.makedirs(app_data, exist_ok=True)
    return app_data


def checar_ffmpeg_e_instalar():
    """
    Verifica se o FFmpeg está disponível.
    Retorna o diretório do ffmpeg.exe ou None se não encontrado.
    """
    exe_dir = (
        os.path.dirname(sys.executable)
        if getattr(sys, 'frozen', False)
        else os.path.abspath(".")
    )
    ffmpeg_cmd = "ffmpeg.exe"

    # Verificar ao lado do executável
    if os.path.exists(os.path.join(exe_dir, ffmpeg_cmd)):
        return exe_dir

    # Verificar no AppData do usuário
    app_data_dir = get_ffmpeg_dir()
    if os.path.exists(os.path.join(app_data_dir, ffmpeg_cmd)):
        return app_data_dir

    return None


def baixar_ffmpeg(status_label, progress_bar, download_btn):
    """
    Baixa e instala o FFmpeg automaticamente.
    Recebe widgets da UI para feedback visual em tempo real.
    """
    exe_dir = get_ffmpeg_dir()

    status_label.configure(
        text="Iniciando Autoinstalador Oculto...\nBaixando motores gráficos nativos FFMPEG (1080p)...",
        text_color="#FF9800"
    )
    download_btn.configure(state="disabled", text="Instalando...")
    progress_bar.set(0)

    url_ffmpeg = (
        "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    )
    zip_path = os.path.join(exe_dir, "ffmpeg.zip")

    try:
        def reporthook(count, block_size, total_size):
            if total_size > 0:
                calc = (count * block_size) / total_size
                if calc <= 1:
                    progress_bar.set(calc)
                    status_label.configure(
                        text=f"Ajustando Motores de Renderização... {calc * 100:.1f}%"
                    )

        urllib.request.urlretrieve(url_ffmpeg, zip_path, reporthook)

        status_label.configure(
            text="Extraindo componentes vitais do Zip...",
            text_color="#00BCD4"
        )
        progress_bar.set(0.5)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for membro in zip_ref.namelist():
                if membro.endswith('ffmpeg.exe'):
                    fonte = zip_ref.open(membro)
                    target = open(os.path.join(exe_dir, 'ffmpeg.exe'), 'wb')
                    with fonte, target:
                        target.write(fonte.read())
                    # Extraia também ffprobe.exe para diagnóstico
                    break

            # Tentar extrair ffprobe.exe também
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for membro in zip_ref.namelist():
                if membro.endswith('ffprobe.exe'):
                    fonte = zip_ref.open(membro)
                    target = open(os.path.join(exe_dir, 'ffprobe.exe'), 'wb')
                    with fonte, target:
                        target.write(fonte.read())
                    break

        progress_bar.set(1.0)
        status_label.configure(
            text="Motores instalados com sucesso!\nO Sistema está pronto para a ação.",
            text_color="#00E676"
        )
        time.sleep(2)

    except Exception as e:
        status_label.configure(
            text="Erro ao baixar pacotes vitais. Certifique conexão ou instale FFMPEG manualmente.",
            text_color="red"
        )
        print(f"Erro Autoinstalador: {e}")

    finally:
        if os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except OSError:
                pass

        progress_bar.set(0)
        status_label.configure(text="")
        download_btn.configure(state="normal", text="B A I X A R   V Í D E O")

    return exe_dir
