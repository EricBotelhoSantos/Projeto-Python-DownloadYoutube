# NexusSave — Site Multi-Ferramentas

Transformar o aplicativo desktop NexusTube em um site web premium chamado **NexusSave**, com download de vídeos de redes sociais (TikTok, Twitter/X, Instagram) e conversor de arquivos MP4→MP3. O site será **bilíngue** (Português BR + Inglês) com seletor de idioma por bandeiras.

## User Review Required

> [!NOTE]
> **Nome do site**: ✅ Definido como **NexusSave**

> [!NOTE]
> **Idioma do site**: ✅ **Bilíngue** — Português (BR) e Inglês, com seletor de idioma usando **bandeiras dos países** (🇧🇷 Brasil / 🇺🇸 EUA) posicionado no canto superior direito do header.

> [!IMPORTANT]
> **Hospedagem**: Para rodar localmente durante o desenvolvimento, usaremos Flask. Para produção futura, será necessário uma VPS (DigitalOcean, Hostinger, etc). A parte de deploy será feita depois.

---

## Arquitetura Geral

```
┌─────────────────────────────────────────┐
│         FRONTEND (Browser)              │
│   HTML + CSS + JavaScript               │
│   ┌──────────────────────────────────┐  │
│   │  🇧🇷/🇺🇸 Seletor de Idioma (header) │  │
│   ├───────────┬──────────────────────┤  │
│   │ Downloader│   Conversor          │  │
│   │ TikTok    │   MP4 → MP3         │  │
│   │ Twitter   │   (upload local)     │  │
│   │ Instagram │                      │  │
│   └───────────┴──────────────────────┘  │
│   i18n: translations.js (pt-BR / en)    │
└──────────────┬──────────────────────────┘
               │ API REST (JSON)
┌──────────────▼──────────────────────────┐
│         BACKEND (Python/Flask)           │
│   ┌───────────┬──────────────────────┐  │
│   │  yt-dlp   │   FFmpeg             │  │
│   │ (download)│  (conversão)         │  │
│   └───────────┴──────────────────────┘  │
└──────────────────────────────────────────┘
```

---

## Proposed Changes

### Estrutura do Projeto

```
c:\projetos\Projeto-Python-DownloadYoutube\
├── main.py                    (app desktop — mantido intacto)
├── site/                      (NOVO — projeto web NexusSave)
│   ├── app.py                 (Backend Flask — rotas API)
│   ├── requirements.txt       (Dependências Python)
│   ├── templates/
│   │   └── index.html         (Página principal)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css      (Design premium completo)
│   │   ├── js/
│   │   │   ├── app.js         (Lógica frontend)
│   │   │   └── translations.js (Textos PT-BR e EN)
│   │   ├── images/
│   │   │   ├── flag-br.svg    (Bandeira do Brasil)
│   │   │   └── flag-us.svg    (Bandeira dos EUA)
│   │   └── fonts/             (Fontes locais se necessário)
│   └── downloads/             (Pasta temporária de arquivos)
```

---

### Backend — Flask API

#### [NEW] [app.py](file:///c:/projetos/Projeto-Python-DownloadYoutube/site/app.py) — NexusSave Backend

Servidor Flask com as seguintes rotas:

| Rota | Método | Função |
|---|---|---|
| `/` | GET | Serve a página principal |
| `/api/download` | POST | Recebe URL da rede social, usa `yt-dlp` para baixar e retorna o arquivo |
| `/api/info` | POST | Retorna info do vídeo (título, thumbnail, duração) antes de baixar |
| `/api/convert` | POST | Recebe upload MP4, converte para MP3 com FFmpeg, retorna arquivo |

**Lógica de download por plataforma:**
- **TikTok**: `yt-dlp` suporta nativamente, opção sem marca d'água
- **Twitter/X**: `yt-dlp` suporta nativamente
- **Instagram**: `yt-dlp` suporta Reels e Posts públicos

**Lógica de conversão:**
- Usuário faz upload de MP4
- Backend usa FFmpeg para extrair áudio → MP3
- Arquivo convertido é servido para download
- Arquivos temporários são limpos automaticamente

**Segurança:**
- Limite de tamanho de upload (100MB)
- Limpeza automática de arquivos temporários após 10 minutos
- Rate limiting básico para evitar abuso

#### [NEW] [requirements.txt](file:///c:/projetos/Projeto-Python-DownloadYoutube/site/requirements.txt)

```
flask
yt-dlp
```

---

### Frontend — Interface Premium

#### [NEW] [index.html](file:///c:/projetos/Projeto-Python-DownloadYoutube/site/templates/index.html) — NexusSave

Página única (SPA-like) com navegação por abas:

**Seções do site:**
1. **Hero/Header** — Logo **NexusSave** + tagline + navegação + **seletor de idioma com bandeiras** (canto superior direito)
2. **Aba Downloader** — Campo de URL + detecção automática de plataforma + botão download
3. **Aba Conversor** — Área de drag & drop para upload MP4 + botão converter
4. **Footer** — Links, créditos, disclaimer legal

**Funcionalidades UI:**
- Detecção automática da plataforma pelo URL (ícone muda: TikTok/Twitter/Instagram)
- Preview do vídeo antes do download (thumbnail + título + duração)
- Barra de progresso animada durante download/conversão
- Feedback visual de sucesso/erro

**Seletor de Idioma (Language Switcher):**
- Posicionado no **canto superior direito do header**, área estratégica de fácil acesso
- Exibe a **bandeira do país** correspondente ao idioma ativo (🇧🇷 para PT-BR, 🇺🇸 para Inglês)
- Ao clicar, abre um mini-dropdown com as duas opções de bandeira
- A bandeira ativa fica destacada (borda verde neon ou leve glow)
- O idioma selecionado é salvo no `localStorage` para persistir entre visitas
- Transição suave ao trocar idioma (sem reload da página)

#### [NEW] [style.css](file:///c:/projetos/Projeto-Python-DownloadYoutube/site/static/css/style.css)

Design **dark mode premium** inspirado no app desktop:

- **Cores principais**: Fundo escuro (#0a0a0a), verde neon (#00E676) como accent
- **Glassmorphism**: Cards com backdrop-filter blur
- **Gradientes**: Header e botões com gradientes suaves
- **Tipografia**: Google Fonts (Inter)
- **Responsivo**: Mobile-first, funciona em celular e desktop
- **Animações**: Hover effects, transições suaves, loading spinners
- **Ícones**: Ícones SVG das redes sociais (TikTok, Twitter, Instagram)
- **Seletor de idioma**: Estilização do switcher com bandeiras SVG (hover glow, borda ativa verde neon, dropdown com backdrop-filter blur)

#### [NEW] [app.js](file:///c:/projetos/Projeto-Python-DownloadYoutube/site/static/js/app.js)

- Navegação entre abas (Downloader / Conversor)
- Detecção automática de plataforma a partir da URL colada
- Chamadas fetch() para a API do backend
- Gerenciamento de upload drag & drop para o conversor
- Barra de progresso e feedback visual
- Validação de URL no frontend
- **Sistema de internacionalização (i18n)** — carrega textos de `translations.js` e aplica no DOM
- Salva preferência de idioma no `localStorage`

#### [NEW] [translations.js](file:///c:/projetos/Projeto-Python-DownloadYoutube/site/static/js/translations.js)

Arquivo com todas as strings do site em dois idiomas:

```js
const translations = {
  "pt-BR": {
    heroTitle: "NexusSave",
    heroSubtitle: "Baixe vídeos de qualquer rede social",
    tabDownloader: "Downloader",
    tabConverter: "Conversor",
    inputPlaceholder: "Cole o link do vídeo aqui...",
    downloadBtn: "Baixar Vídeo",
    convertBtn: "Converter para MP3",
    dropzoneText: "Arraste seu arquivo MP4 aqui",
    // ... demais strings
  },
  "en": {
    heroTitle: "NexusSave",
    heroSubtitle: "Download videos from any social network",
    tabDownloader: "Downloader",
    tabConverter: "Converter",
    inputPlaceholder: "Paste the video link here...",
    downloadBtn: "Download Video",
    convertBtn: "Convert to MP3",
    dropzoneText: "Drag your MP4 file here",
    // ... demais strings
  }
};
```

#### [NEW] Bandeiras SVG

- [flag-br.svg](file:///c:/projetos/Projeto-Python-DownloadYoutube/site/static/images/flag-br.svg) — Bandeira do Brasil (SVG otimizado)
- [flag-us.svg](file:///c:/projetos/Projeto-Python-DownloadYoutube/site/static/images/flag-us.svg) — Bandeira dos EUA (SVG otimizado)

---

## Open Questions

> [!NOTE]
> ~~**1. Nome do site**~~ — ✅ Resolvido: **NexusSave**

> [!NOTE]
> ~~**2. Idioma**~~ — ✅ Resolvido: **Bilíngue** (PT-BR + EN) com seletor por bandeiras

Nenhuma questão pendente no momento.

---

## Verification Plan

### Testes Automatizados
- Rodar o servidor Flask localmente (`python app.py`)
- Testar download de vídeo do TikTok via interface
- Testar download de vídeo do Twitter via interface
- Testar conversão MP4→MP3 via upload
- Verificar responsividade em tela mobile (redimensionar browser)

### Testes Manuais
- Verificar que o design está bonito e premium
- Testar em diferentes browsers (Chrome, Firefox, Edge)
- Verificar limpeza automática de arquivos temporários
- **Testar seletor de idioma**: clicar nas bandeiras e verificar que todos os textos mudam
- **Testar persistência**: recarregar a página e verificar que o idioma escolhido é mantido
- **Testar visual das bandeiras**: verificar que a bandeira ativa tem destaque visual (glow/borda verde)
