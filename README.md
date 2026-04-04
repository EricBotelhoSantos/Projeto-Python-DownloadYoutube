<div align="center">

# ⬇ NexusSave

### **Plataforma Unificada para Download e Conversão de Vídeos de Redes Sociais**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-Engine-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Converter-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)](https://ffmpeg.org)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-Desktop-00E676?style=for-the-badge&logo=windowsterminal&logoColor=white)](https://github.com/TomSchimansky/CustomTkinter)
[![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/Licença-MIT-yellow?style=for-the-badge)](LICENSE)

<br>

> **Baixe vídeos do TikTok, Twitter/X e Instagram com um único clique.**
> Converta MP4 para MP3 instantaneamente. Interface web moderna com Dark Mode premium e suporte bilíngue (PT-BR / EN).

<br>

[Funcionalidades](#-funcionalidades) •
[Instalação](#-instalação) •
[Como Usar](#-como-usar) •
[Tecnologias](#-tecnologias-utilizadas) •
[Contribuição](#-contribuição)

---

</div>

## 📖 Descrição Geral

O **NexusSave** é uma solução completa e de código aberto para download de vídeos de múltiplas redes sociais e conversão de mídia. O projeto oferece duas interfaces distintas, projetadas para atender diferentes necessidades de uso:

| Componente | Descrição |
|:---|:---|
| **NexusSave Web** | Aplicação web com backend Flask e frontend responsivo. Suporte a TikTok, Twitter/X e Instagram com pré-visualização de vídeos, detecção automática de plataforma e conversor MP4→MP3 integrado. |
| **NexusTube Downloader** | Aplicação desktop para Windows (CustomTkinter) focada em download de vídeos do YouTube em qualidade máxima (1080p+), com merge automático de áudio e vídeo. |

Ambas as interfaces compartilham o mesmo motor de extração **yt-dlp** e incluem **autoinstalação inteligente do FFmpeg**, eliminando a necessidade de configuração manual por parte do usuário.

---

## ✨ Funcionalidades

### 🌐 NexusSave — Interface Web

<table>
<tr>
<td width="50%">

#### 🔗 Download Multi-Plataforma
- Suporte a **TikTok**, **Twitter/X** e **Instagram**
- Detecção automática da plataforma via análise de URL
- Pré-visualização com thumbnail, título, autor e duração
- Proxy interno de imagens para contornar bloqueios de CORS

</td>
<td width="50%">

#### 🎵 Conversor MP4 → MP3
- Upload via **drag-and-drop** ou seleção de arquivo
- Conversão de alta qualidade com codec `libmp3lame`
- Limite de upload de 100 MB por arquivo
- Limpeza automática de arquivos temporários (10 min)

</td>
</tr>
<tr>
<td width="50%">

#### 🌍 Interface Bilíngue
- Suporte completo a **Português (BR)** e **Inglês**
- Alternância de idioma em tempo real sem recarregamento
- Persistência de preferência via `localStorage`

</td>
<td width="50%">

#### 🛡️ Instalação Segura do FFmpeg
- Modal informativo com badges de confiança
- Download automático a partir de fonte oficial (gyan.dev)
- Instalação isolada na pasta do NexusSave
- Verificação de status em tempo real via polling

</td>
</tr>
</table>

### 🖥️ NexusTube Downloader — Interface Desktop

<table>
<tr>
<td width="50%">

#### 🎬 Download em Qualidade Máxima
- Vídeos do YouTube em **1080p+**
- Merge automático de streams de vídeo e áudio
- Suporte a links padrão e encurtados (`youtu.be`)
- Salvamento direto na pasta **Downloads** do usuário

</td>
<td width="50%">

#### 🎨 Design Premium
- Interface Dark Mode com tema **verde neon** (#00E676)
- Background **Glassmorphism** gerado programaticamente
- Barra de progresso em tempo real com velocidade (MB/s)
- Feedback visual dinâmico em cada etapa do processo

</td>
</tr>
<tr>
<td width="50%">

#### 🛠️ Autoinstalação FFmpeg
- Detecta automaticamente a presença do FFmpeg
- Download e instalação silenciosa na primeira execução
- Armazenamento em `AppData` (sem conflitos de permissão)
- Limpeza automática de arquivos zip temporários

</td>
<td width="50%">

#### 📦 Distribuição Profissional
- Executável único (.exe) empacotado via **PyInstaller**
- Instalador Windows profissional via **Inno Setup**
- Ícone personalizado na janela e barra de tarefas
- Funciona em qualquer PC com Windows 10/11

</td>
</tr>
</table>

---

## 🏗️ Arquitetura do Sistema

```
📁 NexusSave/
│
├── .gitignore                             # Filtros de versionamento
├── README.md                              # Documentação do projeto
├── requirements.txt                       # Dependências unificadas (todas)
│
├── 📁 desktop/                            # Aplicação Desktop (NexusTube Downloader)
│   ├── 🐍 main.py                        # Entry point e construção da interface
│   ├── 🐍 downloader.py                  # Lógica de download (yt-dlp)
│   ├── 🐍 ffmpeg_manager.py              # Autoinstalação e verificação do FFmpeg
│   └── 📁 assets/
│       ├── 🎯 app_icon.ico               # Ícone do aplicativo
│       └── 🖼️ bg.png                     # Background Glassmorphism (gerado)
│
├── 📁 web/                                # Aplicação Web (NexusSave)
│   ├── 🐍 app.py                         # Backend Flask (API REST + servidor)
│   ├── 📋 requirements.txt               # Dependências Python (flask, yt-dlp)
│   ├── 📋 Procfile                        # Configuração de deploy
│   ├── 📁 templates/
│   │   └── 🌐 index.html                 # Template principal (Jinja2)
│   └── 📁 static/
│       ├── 📁 css/style.css              # Estilos premium (Dark Mode + Glassmorphism)
│       ├── 📁 js/
│       │   ├── ⚙️ app.js                 # Lógica do frontend (download, conversão, i18n)
│       │   └── 🌍 translations.js        # Sistema de tradução (PT-BR / EN)
│       └── 📁 images/                    # Bandeiras SVG (BR / US)
│
├── 📁 scripts/                            # Scripts utilitários
│   ├── 🎨 generate_bg.py                 # Gerador de wallpaper (1920×1080)
│   ├── 🔧 start_server.bat               # Iniciar servidor web
│   └── 🔧 build.bat                      # Build unificado (ambos executáveis)
│
└── 📁 config/                             # Configurações de build
    ├── 📋 nexussave.spec                  # PyInstaller config (web)
    ├── 📋 nexustube_downloader.spec       # PyInstaller config (desktop)
    └── 📋 instalador_nexus.iss            # Script Inno Setup (instalador Windows)
```

### Visão Geral da API REST (NexusSave Web)

| Endpoint | Método | Descrição |
|:---|:---:|:---|
| `/` | `GET` | Serve a página principal da aplicação |
| `/api/detect` | `POST` | Detecta a plataforma de origem a partir da URL |
| `/api/info` | `POST` | Retorna metadados do vídeo (título, thumbnail, duração, autor) |
| `/api/download` | `POST` | Realiza o download do vídeo e retorna o arquivo |
| `/api/convert` | `POST` | Converte arquivo MP4 enviado para MP3 |
| `/api/proxy-image` | `GET` | Proxy para thumbnails com CORS bloqueado (Instagram, Twitter) |
| `/api/ffmpeg/status` | `GET` | Verifica o status de instalação do FFmpeg |
| `/api/ffmpeg/install` | `POST` | Inicia a instalação automática do FFmpeg |

---

## 🚀 Instalação

### Pré-requisitos

- **Python 3.10** ou superior
- **Git** (opcional, para clonar o repositório)
- **pip** (gerenciador de pacotes Python)

### NexusSave Web (Interface Web)

```bash
# 1. Clone o repositório
git clone https://github.com/EricBotelhoSantos/Projeto-Python-DownloadYoutube.git
cd Projeto-Python-DownloadYoutube

# 2. Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie o servidor
cd web
python app.py
```

O servidor será iniciado em **http://localhost:5000**.

> **Alternativa rápida (Windows):** Execute `scripts\start_server.bat`.

### NexusTube Downloader (Interface Desktop)

```bash
# 1. A partir da raiz do projeto (com o ambiente virtual ativo)
pip install -r requirements.txt

# 2. Gere a imagem de background (primeira execução)
python scripts/generate_bg.py

# 3. Execute a aplicação
python desktop/main.py
```

---

## 💡 Como Usar

### Interface Web — Download de Vídeos

1. Acesse **http://localhost:5000** no navegador
2. Cole a URL do vídeo (TikTok, Twitter/X ou Instagram) no campo de entrada
3. Clique em **Buscar** para pré-visualizar as informações do vídeo
4. Clique em **Baixar Vídeo** para realizar o download

### Interface Web — Conversão MP4 → MP3

1. Selecione a aba **Conversor** na interface
2. Arraste um arquivo `.mp4` para a área de upload (ou clique para selecionar)
3. Clique em **Converter para MP3**
4. Na primeira conversão, o sistema solicitará a instalação do FFmpeg (automática)

### Interface Desktop — YouTube

1. Execute `desktop/main.py` ou o executável `NexusTubeDownloader.exe`
2. Cole a URL do vídeo do YouTube no campo de entrada
3. Clique em **BAIXAR VÍDEO**
4. O vídeo será salvo automaticamente na pasta **Downloads** do usuário

---

## 📐 Exemplos de Uso

### URLs Suportadas

```
# TikTok
https://www.tiktok.com/@usuario/video/7123456789012345678
https://vm.tiktok.com/AbCdEfG/

# Twitter / X
https://twitter.com/usuario/status/1234567890123456789
https://x.com/usuario/status/1234567890123456789

# Instagram
https://www.instagram.com/reel/AbCdEfGhIjK/
https://www.instagram.com/p/AbCdEfGhIjK/

# YouTube (Desktop)
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/dQw4w9WgXcQ
```

---

## 📦 Gerar Executável (.exe)

### NexusSave (Web — Executável Standalone)

```bash
.venv\Scripts\pyinstaller config\nexussave.spec --clean -y
```

Gera `dist/NexusSave.exe` — executável autônomo que embarca o servidor Flask, templates e assets estáticos.

### NexusTube Downloader (Desktop)

```bash
.venv\Scripts\pyinstaller config\nexustube_downloader.spec --clean -y
```

Gera `dist/NexusTubeDownloader.exe` com:
- ✅ Ícone personalizado embutido
- ✅ Background Glassmorphism incluído
- ✅ Todas as dependências empacotadas
- ✅ Sem necessidade de Python na máquina de destino

### Gerar Instalador Windows (Inno Setup)

1. Instale o [Inno Setup](https://jrsoftware.org/isinfo.php) (gratuito)
2. Abra o arquivo `instalador_nexus.iss` no Inno Setup
3. Compile com `Ctrl+F9`
4. O instalador será gerado em `Instalador_Final/`

O instalador inclui:
- 🖥️ Atalho no Menu Iniciar
- 🖥️ Atalho opcional na Área de Trabalho
- 🚀 Opção de iniciar o aplicativo após a instalação

---

## 🔌 Tecnologias Utilizadas

| Tecnologia | Versão | Propósito |
|:---:|:---:|:---|
| **Python** | 3.10+ | Linguagem principal do backend e aplicação desktop |
| **Flask** | Latest | Framework web para a API REST e servidor HTTP |
| **yt-dlp** | Latest | Motor de extração e download de vídeos (fork avançado do youtube-dl) |
| **FFmpeg** | Latest | Processamento de mídia: merge de streams e conversão MP4→MP3 |
| **CustomTkinter** | Latest | Framework de UI moderna para Python (versão Desktop) |
| **Pillow** | Latest | Manipulação de imagens (geração de background, ícones) |
| **Jinja2** | Latest | Template engine para renderização HTML no Flask |
| **PyInstaller** | Latest | Empacotamento em executável Windows standalone |
| **Inno Setup** | Latest | Geração de instalador profissional para Windows |

### Frontend (Web)

| Tecnologia | Propósito |
|:---:|:---|
| **HTML5 + CSS3** | Estrutura e estilização da interface web |
| **JavaScript (Vanilla)** | Lógica de interação, requisições assíncronas e i18n |
| **Inter (Google Fonts)** | Tipografia premium para a interface |
| **CSS Custom Properties** | Sistema de design tokens para Dark Mode |
| **Glassmorphism** | Efeitos visuais com `backdrop-filter` e transparências |

---

## ❓ Solução de Problemas

<details>
<summary><b>🔴 Erro ao baixar vídeo de rede social</b></summary>

Causas comuns:
- **Vídeo privado ou removido** — verifique se o link está acessível no navegador
- **Plataforma não suportada** — apenas TikTok, Twitter/X e Instagram são suportados na versão web
- **Sem conexão com a internet** — verifique sua conexão de rede
- **Bloqueio regional** — alguns conteúdos possuem restrição geográfica
</details>

<details>
<summary><b>🔴 FFmpeg não foi encontrado</b></summary>

Na versão web, o sistema solicita a instalação via modal na primeira conversão. Se a instalação automática falhar:
1. Baixe manualmente em [ffmpeg.org](https://ffmpeg.org/download.html)
2. Coloque o `ffmpeg.exe` no diretório `%APPDATA%/NexusSave/ffmpeg/` (Windows)
3. Ou adicione o FFmpeg ao `PATH` do sistema
</details>

<details>
<summary><b>🔴 Thumbnail não carrega (Instagram/Twitter)</b></summary>

Algumas plataformas bloqueiam requisições de imagem via CORS. O NexusSave utiliza um proxy interno (`/api/proxy-image`) para contornar esse problema. Caso persista:
- Verifique se o servidor Flask está rodando corretamente
- Confira o log do console do servidor para mensagens de erro detalhadas
</details>

<details>
<summary><b>🔴 Servidor não inicia na porta 5000</b></summary>

A porta pode estar em uso por outro processo. Defina uma porta alternativa:
```bash
set PORT=8080     # Windows
python app.py
```
</details>

---

## 🤝 Contribuição

Contribuições são bem-vindas e valorizadas. Para contribuir com o projeto:

1. **Fork** o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Realize os commits com mensagens descritivas (`git commit -m 'feat: adiciona suporte a nova plataforma'`)
4. Envie para o repositório remoto (`git push origin feature/nova-funcionalidade`)
5. Abra um **Pull Request** detalhando suas alterações

### Sugestões de Melhorias Futuras

- [ ] Suporte a novas plataformas (Facebook, Pinterest, Threads)
- [ ] Download de playlists completas
- [ ] Seleção de qualidade/resolução antes do download
- [ ] Sistema de fila para múltiplos downloads simultâneos
- [ ] Versão PWA (Progressive Web App) para uso offline
- [ ] Suporte a download de áudio direto (sem conversão)
- [ ] Containerização com Docker para deploy simplificado

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**. Consulte o arquivo [LICENSE](LICENSE) para informações detalhadas.

Você é livre para usar, modificar e distribuir este software, desde que mantenha o aviso de copyright original.

---

## 👤 Autor

**Eric Botelho Santos**

- GitHub: [@EricBotelhoSantos](https://github.com/EricBotelhoSantos)

---

<div align="center">

### Feito com 💚 e Python

*Simplificando o download de conteúdo digital desde 2026*

<br>

**⭐ Se este projeto foi útil para você, considere deixar uma estrela!**

</div>
