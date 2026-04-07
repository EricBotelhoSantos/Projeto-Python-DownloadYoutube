"""
NexusTube Downloader — Lógica de Download
Gerencia o download de vídeos do YouTube via yt-dlp com feedback em tempo real.
"""

import os
import glob
import time
import threading

import yt_dlp

from ffmpeg_manager import checar_ffmpeg_e_instalar, baixar_ffmpeg


def _criar_hook_progresso(progress_bar, status_label):
    """Cria o hook de progresso configurado com os widgets da UI."""

    def atualizar_progresso(d):
        """Lê os dados ao vivo do yt-dlp e atualiza a barra de progresso."""
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                baixado = d.get('downloaded_bytes', 0)

                if total and total > 0:
                    percentual = baixado / total
                    progress_bar.set(percentual)

                    velocidade = d.get('speed')
                    vel_str = (
                        f"{(velocidade / 1024 / 1024):.1f} MB/s"
                        if velocidade else "..."
                    )

                    texto = f"Baixando... {percentual * 100:.1f}%  (Velocidade: {vel_str})"
                    status_label.configure(text=texto, text_color="#00E676")
            except Exception:
                pass

        elif d['status'] == 'finished':
            progress_bar.set(1.0)
            status_label.configure(
                text="Download 100%! Finalizando renderização do processo...",
                text_color="#FF9800"
            )

    return atualizar_progresso


def _listar_arquivos_extensao(diretorio, extensao):
    """Lista arquivos com uma determinada extensão no diretório."""
    padrao = os.path.join(diretorio, extensao)
    return set(glob.glob(padrao))


def executar_script(url, status_label, progress_bar, download_btn):
    """Executa o download do vídeo do YouTube com qualidade máxima."""
    caminho_downloads = os.path.join(os.path.expanduser('~'), 'Downloads')

    # Verificação e autoinstalação do FFmpeg
    ffmpeg_dir = checar_ffmpeg_e_instalar()
    if not ffmpeg_dir:
        ffmpeg_dir = baixar_ffmpeg(status_label, progress_bar, download_btn)

    hook = _criar_hook_progresso(progress_bar, status_label)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(caminho_downloads, '%(title)s.%(ext)s'),
        'nopart': True,
        'progress_hooks': [hook],
        'ffmpeg_location': ffmpeg_dir,
        'extractor_args': {
            'youtube': {
                'player_client': ['web', 'android', 'ios']
            }
        }
    }

    try:
        # Snapshot de arquivos .m4a antes do download
        m4a_antes = _listar_arquivos_extensao(caminho_downloads, '*.m4a')

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            status_label.configure(
                text="Conectando aos servidores do Nexus...",
                text_color="#2196F3"
            )
            info = ydl.extract_info(url, download=True)
            titulo = info.get('title', 'Vídeo concluído!')

            status_label.configure(
                text="Aplicando polimento final e limpando buffers...",
                text_color="#FF9800"
            )
            time.sleep(2)

            # Limpar apenas arquivos temporários de audio criados NESTE download
            m4a_depois = _listar_arquivos_extensao(caminho_downloads, '*.m4a')
            m4a_novos = m4a_depois - m4a_antes
            for temp_audio in m4a_novos:
                try:
                    os.remove(temp_audio)
                except OSError:
                    pass

            mensagem = (
                f"Missão Cumprida!\n"
                f"« {titulo} »\n"
                f"Acesso liberado na sua pasta Downloads!"
            )
            status_label.configure(text=mensagem, text_color="#00E676")

    except Exception as e:
        error_msg = str(e).split('\n')[0]
        status_label.configure(
            text=f"A Anomalia impediu o download!\nErro Real: {error_msg[:80]}",
            text_color="#FF5252"
        )
        print(f"Erro detalhado: {e}")

    finally:
        download_btn.configure(state="normal", text="B A I X A R   V Í D E O")
        progress_bar.set(0)


def iniciar_download(url_entry, status_label, progress_bar, download_btn):
    """Valida a URL e inicia o download em uma thread separada."""
    url = url_entry.get()

    if not url.strip():
        status_label.configure(
            text="⚠️ Por favor, insira um link de coordenadas válido do YouTube!",
            text_color="#FF5252"
        )
        return

    status_label.configure(
        text="Iniciando cálculos da matriz, por favor aguarde...",
        text_color="#B0BEC5"
    )
    download_btn.configure(state="disabled", text="Construindo...")
    progress_bar.set(0)

    threading.Thread(
        target=executar_script,
        args=(url, status_label, progress_bar, download_btn),
        daemon=True
    ).start()
