/**
 * NexusSave — Translations (i18n)
 * Suporte a Português (BR) e Inglês
 */

const translations = {
    "pt-BR": {
        // Hero
        heroTitle: "NexusSave",
        heroSubtitle: "Baixe vídeos de qualquer rede social",

        // Tabs
        tabDownloader: "Downloader",
        tabConverter: "Conversor",

        // Downloader
        platformLabel: "Plataforma detectada:",
        inputPlaceholder: "Cole o link do vídeo aqui...",
        fetchBtn: "Buscar",
        downloading: "Baixando...",
        downloadBtn: "Baixar Vídeo",

        // Video Preview
        duration: "Duração",
        seconds: "s",

        // Converter
        dropzoneText: "Arraste seu arquivo MP4 aqui",
        dropzoneSubtext: "ou clique para selecionar",
        converting: "Convertendo...",
        convertBtn: "Converter para MP3",

        // Supported
        supportedTitle: "Plataformas Suportadas",

        // Footer
        footerText: "Feito com 💚 por NexusSave",
        footerDisclaimer: "Use apenas para baixar vídeos que você tem permissão.",

        // Messages
        errorEmptyUrl: "Por favor, insira uma URL.",
        errorInvalidUrl: "URL inválida. Verifique o link.",
        errorUnsupported: "Plataforma não suportada. Use TikTok, Twitter ou Instagram.",
        errorDownload: "Erro ao baixar o vídeo. Tente novamente.",
        errorConvert: "Erro ao converter o arquivo. Tente novamente.",
        errorServerTimeout:
            "O servidor demorou demais ou ficou indisponível (limite de tempo). Tente um arquivo MP4 menor ou novamente mais tarde.",
        errorServerUnexpected: "O servidor enviou uma resposta inesperada. Tente novamente.",
        errorNoFile: "Selecione um arquivo MP4.",
        successDownload: "Download concluído!",
        successConvert: "Conversão concluída!",

        // FFmpeg
        ffmpegTitle: "Componente Necessário para Conversão",
        ffmpegDescription: "Para converter vídeos em MP3, o NexusSave utiliza o FFmpeg — a ferramenta de processamento de áudio e vídeo mais utilizada do mundo, presente em softwares como VLC, OBS Studio, Chrome e até no WhatsApp.",
        ffmpegInfo: "O FFmpeg não é um vírus, não coleta dados e não acessa a internet. Ele apenas processa arquivos locais no seu computador. Milhões de desenvolvedores e empresas confiam nele diariamente.",
        ffmpegInstallBtn: "Instalar com Segurança",
        ffmpegCancelBtn: "Agora Não",
        ffmpegInstalling: "Baixando e instalando FFmpeg...",
        ffmpegBadge1Title: "100% Open Source",
        ffmpegBadge1Desc: "Código aberto, que qualquer pessoa pode verificar",
        ffmpegBadge2Title: "Fonte Oficial Verificada",
        ffmpegBadge2Desc: "Download direto de gyan.dev (distribuidor oficial)",
        ffmpegBadge3Title: "Instalação Isolada",
        ffmpegBadge3Desc: "Salvo apenas na pasta do NexusSave — nada é alterado no seu sistema",

        // Platform Names
        platformTiktok: "TikTok",
        platformTwitter: "Twitter/X",
        platformInstagram: "Instagram"
    },

    "en": {
        // Hero
        heroTitle: "NexusSave",
        heroSubtitle: "Download videos from any social network",

        // Tabs
        tabDownloader: "Downloader",
        tabConverter: "Converter",

        // Downloader
        platformLabel: "Detected platform:",
        inputPlaceholder: "Paste the video link here...",
        fetchBtn: "Fetch",
        downloading: "Downloading...",
        downloadBtn: "Download Video",

        // Video Preview
        duration: "Duration",
        seconds: "s",

        // Converter
        dropzoneText: "Drag your MP4 file here",
        dropzoneSubtext: "or click to select",
        converting: "Converting...",
        convertBtn: "Convert to MP3",

        // Supported
        supportedTitle: "Supported Platforms",

        // Footer
        footerText: "Made with 💚 by NexusSave",
        footerDisclaimer: "Only download videos you have permission to use.",

        // Messages
        errorEmptyUrl: "Please enter a URL.",
        errorInvalidUrl: "Invalid URL. Please check the link.",
        errorUnsupported: "Unsupported platform. Use TikTok, Twitter or Instagram.",
        errorDownload: "Error downloading video. Please try again.",
        errorConvert: "Error converting file. Please try again.",
        errorServerTimeout:
            "The server took too long or was unavailable (time limit). Try a smaller MP4 or again later.",
        errorServerUnexpected: "The server returned an unexpected response. Please try again.",
        errorNoFile: "Please select an MP4 file.",
        successDownload: "Download complete!",
        successConvert: "Conversion complete!",

        // FFmpeg
        ffmpegTitle: "Required Component for Conversion",
        ffmpegDescription: "To convert videos to MP3, NexusSave uses FFmpeg — the world's most widely used audio and video processing tool, built into software like VLC, OBS Studio, Chrome, and even WhatsApp.",
        ffmpegInfo: "FFmpeg is not a virus, does not collect data, and does not access the internet. It only processes local files on your computer. Millions of developers and companies rely on it every day.",
        ffmpegInstallBtn: "Install Safely",
        ffmpegCancelBtn: "Not Now",
        ffmpegInstalling: "Downloading and installing FFmpeg...",
        ffmpegBadge1Title: "100% Open Source",
        ffmpegBadge1Desc: "Open code, auditable by anyone",
        ffmpegBadge2Title: "Verified Official Source",
        ffmpegBadge2Desc: "Downloaded directly from gyan.dev (official distributor)",
        ffmpegBadge3Title: "Isolated Installation",
        ffmpegBadge3Desc: "Saved only in the NexusSave folder — nothing else on your system is changed",

        // Platform Names
        platformTiktok: "TikTok",
        platformTwitter: "Twitter/X",
        platformInstagram: "Instagram"
    }
};

/**
 * Get translation for a key
 * @param {string} key - Translation key
 * @param {string} lang - Language code (pt-BR or en)
 * @returns {string} - Translated text
 */
function t(key, lang = currentLang) {
    return translations[lang]?.[key] || translations["en"][key] || key;
}

// Export for use in app.js
window.translations = translations;
window.t = t;