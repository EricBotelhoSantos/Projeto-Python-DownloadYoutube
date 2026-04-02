<div align="center">

# 🌀 NexusTube Pro Downloader

### *Sistema de Extração em Nível Quântico*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-Latest-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-UI-00E676?style=for-the-badge&logo=windowsterminal&logoColor=white)](https://github.com/TomSchimansky/CustomTkinter)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Auto--Install-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)](https://ffmpeg.org)
[![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/Licença-MIT-yellow?style=for-the-badge)](LICENSE)

<br>

> **Baixe vídeos do YouTube em qualidade máxima (1080p+) com apenas um clique.**
> Interface premium Dark Mode, autoinstalação inteligente de dependências e empacotamento profissional para Windows.

<br>

---

</div>

## 📸 Preview

<div align="center">

| Interface Principal |
|:---:|
| *Painel flutuante com design Glassmorphism, barra de progresso em tempo real e feedback visual dinâmico* |

</div>

---

## ✨ Funcionalidades

<table>
<tr>
<td width="50%">

### 🎬 Download Inteligente
- Baixa vídeos em **qualidade máxima** (1080p+)
- Merge automático de **vídeo + áudio** separados
- Suporte a links padrão e encurtados (`youtu.be`)
- Salva automaticamente na pasta **Downloads** do usuário

</td>
<td width="50%">

### 🛠️ Autoinstalação FFmpeg
- Detecta automaticamente se o FFmpeg está presente
- Baixa e instala o FFmpeg **silenciosamente** na primeira execução
- Armazena em `AppData` (sem problemas de permissão)
- Limpeza automática de arquivos temporários

</td>
</tr>
<tr>
<td width="50%">

### 🎨 Interface Premium
- Design **Dark Mode** elegante com tema verde neon
- Background **Glassmorphism** com efeitos visuais
- Barra de progresso em **tempo real** com velocidade (MB/s)
- Feedback dinâmico em cada etapa do processo

</td>
<td width="50%">

### 📦 Distribuição Profissional
- Empacotado como **executável único** (.exe) via PyInstaller
- Instalador Windows profissional via **Inno Setup**
- Ícone personalizado na janela e barra de tarefas
- Pronto para distribuição — funciona em qualquer PC Windows

</td>
</tr>
</table>

---

## 🚀 Início Rápido

### Pré-requisitos

- **Python 3.10+** instalado
- **Git** (opcional, para clonar o repositório)

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/EricBotelhoSantos/Projeto-Python-DownloadYoutube.git
cd Projeto-Python-DownloadYoutube

# 2. Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows

# 3. Instale as dependências
pip install customtkinter yt-dlp Pillow pyinstaller

# 4. Gere a imagem de background
python generate_bg.py

# 5. Execute o aplicativo
python main.py
```

---

## 🏗️ Estrutura do Projeto

```
📁 NexusTube-Pro-Downloader/
│
├── 🐍 main.py                      # Aplicação principal (interface + lógica)
├── 🎨 generate_bg.py                # Gerador de wallpaper Glassmorphism
├── 🖼️ bg.png                        # Imagem de fundo gerada
├── 🎯 app_icon.ico                  # Ícone do aplicativo
├── 📋 NexusTubeDownloader.spec      # Configuração do PyInstaller
├── 📋 instalador_nexus.iss          # Script do instalador (Inno Setup)
│
├── 📁 dist/                         # Executável compilado (.exe)
├── 📁 build/                        # Arquivos temporários de build
├── 📁 Instalador_Final/             # Instalador gerado pelo Inno Setup
└── 📁 .venv/                        # Ambiente virtual Python
```

---

## 📦 Gerar o Executável (.exe)

Para compilar o aplicativo em um executável Windows independente:

```bash
# Compilar o executável (dentro do ambiente virtual)
.venv\Scripts\pyinstaller NexusTubeDownloader.spec --clean -y
```

O executável será gerado em `dist/NexusTubeDownloader.exe` com:
- ✅ Ícone personalizado embutido
- ✅ Background Glassmorphism incluído
- ✅ Todas as dependências empacotadas
- ✅ Sem necessidade de Python instalado na máquina de destino

---

## 🔧 Gerar o Instalador Windows

Para criar um instalador profissional (wizard de instalação):

1. **Baixe e instale** o [Inno Setup](https://jrsoftware.org/isinfo.php) (gratuito)
2. Abra o arquivo `instalador_nexus.iss` no Inno Setup
3. Clique em **Compile** (ou pressione `Ctrl+F9`)
4. O instalador será gerado em `Instalador_Final/`

O instalador inclui:
- 🖥️ Atalho no Menu Iniciar
- 🖥️ Atalho opcional na Área de Trabalho
- 🚀 Opção de iniciar o app após a instalação

---

## 🎨 Personalização do Background

O projeto inclui um gerador de wallpaper programático. Para gerar um novo background:

```bash
python generate_bg.py
```

O script cria uma imagem **1920x1080** com:
- Grade sutil estilo cyberpunk
- Orbe central com brilho Gaussiano no tom verde neon `#00E676`
- Partículas de rede interconectadas
- Linhas oblíquas fluídas

---

## 🔌 Tecnologias Utilizadas

| Tecnologia | Propósito |
|:---:|:---|
| **CustomTkinter** | Framework de UI moderno para Python com suporte a Dark Mode |
| **yt-dlp** | Motor de download de vídeos (fork avançado do youtube-dl) |
| **Pillow** | Manipulação de imagens (background, ícones) |
| **FFmpeg** | Merge de streams de vídeo e áudio para qualidade 1080p+ |
| **PyInstaller** | Empacotamento em executável Windows standalone |
| **Inno Setup** | Geração de instalador profissional Windows |

---

## ❓ Solução de Problemas

<details>
<summary><b>🔴 "A Anomalia impediu o download!"</b></summary>

A partir da versão atual, o erro real é exibido na interface. Causas comuns:
- **Vídeo privado ou removido** — verifique se o link está acessível no navegador
- **Sem conexão com a internet** — verifique sua rede
- **`No space left on device`** — libere espaço no disco rígido
</details>

<details>
<summary><b>🔴 FFmpeg não foi encontrado</b></summary>

O app tenta baixar o FFmpeg automaticamente na primeira execução. Se falhar:
1. Baixe manualmente em [ffmpeg.org](https://ffmpeg.org/download.html)
2. Coloque o `ffmpeg.exe` na mesma pasta do executável
</details>

<details>
<summary><b>🔴 Ícone não aparece na barra de tarefas</b></summary>

Certifique-se de que o arquivo `app_icon.ico` está na mesma pasta do `main.py` ou foi incluído corretamente no `.spec` do PyInstaller.
</details>

---

## 📄 Licença

Este projeto está sob a licença **MIT**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">

### Feito com 💚 e Python

*"Extraindo conteúdo em nível quântico desde 2026"*

<br>

**⭐ Se este projeto te ajudou, deixe uma estrela!**

</div>
