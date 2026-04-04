"""
NexusTube Downloader — Interface Desktop
Aplicação principal com interface gráfica CustomTkinter (Dark Mode Premium).
"""

import os
import customtkinter as ctk
from PIL import Image

from ffmpeg_manager import resource_path
from downloader import iniciar_download

# --- CONFIGURAÇÃO VISUAL PREMIUM ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")


def construir_interface():
    """Constrói e exibe a janela principal da aplicação."""

    # --- JANELA PRINCIPAL ---
    app = ctk.CTk()
    app.title("NexusTube Downloader")

    # --- ÍCONE DA JANELA E BARRA DE TAREFAS ---
    icon_path = resource_path("assets/app_icon.ico")
    if os.path.exists(icon_path):
        try:
            app.wm_iconbitmap(icon_path)
        except Exception:
            pass
        try:
            app.iconbitmap(icon_path)
        except Exception:
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

    # --- DIMENSÕES E POSIÇÃO (TELA CHEIA) ---
    largura = app.winfo_screenwidth()
    altura = app.winfo_screenheight()
    app.geometry(f"{largura}x{altura}+0+0")
    app.after(100, lambda: app.state('zoomed'))

    # --- BACKGROUND GLASSMORPHISM ---
    bg_path = resource_path("assets/bg.png")
    if os.path.exists(bg_path):
        try:
            img_original = Image.open(bg_path)
            img_fundo = ctk.CTkImage(
                light_image=img_original,
                dark_image=img_original,
                size=(largura, altura)
            )
            bg_label = ctk.CTkLabel(app, text="", image=img_fundo)
            bg_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print(f"Não foi possível carregar a imagem de fundo: {e}")

    # --- PAINEL CENTRAL FLUTUANTE ---
    frame = ctk.CTkFrame(
        app,
        corner_radius=25,
        fg_color="#1E1E1E",
        border_width=1,
        border_color="#333333",
        width=800,
        height=580
    )
    frame.place(relx=0.5, rely=0.5, anchor="center")
    frame.pack_propagate(False)

    # --- TÍTULO ---
    title_label = ctk.CTkLabel(
        frame,
        text="N E X U S   T U B E",
        font=ctk.CTkFont(family="Inter", size=32, weight="bold"),
        text_color="#00E676"
    )
    title_label.pack(pady=(55, 10))

    # --- SUBTÍTULO ---
    subtitle = ctk.CTkLabel(
        frame,
        text="Sistema de Extração em Nível Quântico (1080p+)",
        font=ctk.CTkFont(size=14, slant="italic"),
        text_color="#9E9E9E"
    )
    subtitle.pack(pady=(0, 40))

    # --- CAMPO DE INPUT ---
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

    # --- BOTÃO BAIXAR ---
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
        command=None  # Configurado abaixo após criar todos os widgets
    )
    download_btn.pack(pady=30)

    # --- BARRA DE PROGRESSO ---
    progress_bar = ctk.CTkProgressBar(
        frame,
        width=600,
        height=18,
        corner_radius=8,
        progress_color="#00E676",
        fg_color="#1A1A1A"
    )
    progress_bar.set(0)
    progress_bar.pack(pady=20)

    # --- LABEL DE STATUS ---
    status_label = ctk.CTkLabel(
        frame,
        text="",
        font=ctk.CTkFont(size=16, weight="bold")
    )
    status_label.pack(pady=(10, 20))

    # --- CONECTAR O BOTÃO AOS WIDGETS ---
    download_btn.configure(
        command=lambda: iniciar_download(
            url_entry, status_label, progress_bar, download_btn
        )
    )

    return app


if __name__ == "__main__":
    app = construir_interface()
    app.mainloop()
