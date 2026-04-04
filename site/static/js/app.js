/**
 * NexusSave — Frontend Application
 * Download de vídeos e conversão MP4→MP3
 */

// Current language
let currentLang = localStorage.getItem('nexussave-lang') || 'pt-BR';

// FFmpeg status
let ffmpegInstalled = false;
let ffmpegInstalling = false;

// DOM Elements
const elements = {
    // Language
    langBtns: document.querySelectorAll('.lang-btn'),

    // Tabs
    tabBtns: document.querySelectorAll('.tab-btn'),
    tabContents: document.querySelectorAll('.tab-content'),

    // Downloader
    videoUrl: document.getElementById('video-url'),
    fetchInfoBtn: document.getElementById('fetch-info-btn'),
    videoPreview: document.getElementById('video-preview'),
    previewThumbnail: document.getElementById('preview-thumbnail'),
    previewTitle: document.getElementById('preview-title'),
    previewMeta: document.getElementById('preview-meta'),
    progressContainer: document.getElementById('progress-container'),
    downloadBtn: document.getElementById('download-btn'),
    downloaderMessage: document.getElementById('downloader-message'),
    platformIcons: document.querySelectorAll('.platform-icon'),

    // Converter
    dropzone: document.getElementById('dropzone'),
    fileInput: document.getElementById('file-input'),
    selectedFile: document.getElementById('selected-file'),
    fileName: document.getElementById('file-name'),
    removeFileBtn: document.getElementById('remove-file'),
    convertProgress: document.getElementById('convert-progress'),
    convertBtn: document.getElementById('convert-btn'),
    converterMessage: document.getElementById('converter-message'),

    // FFmpeg Modal
    ffmpegModal: document.getElementById('ffmpeg-modal'),
    ffmpegInstallBtn: document.getElementById('ffmpeg-install-btn'),
    ffmpegCancelBtn: document.getElementById('ffmpeg-cancel-btn'),
    ffmpegProgress: document.getElementById('ffmpeg-progress')
};

// Current video info
let currentVideoInfo = null;

/**
 * Initialize the application
 */
function init() {
    applyLanguage(currentLang);
    setupEventListeners();
    checkFFmpeg();
}

/**
 * Apply language to all elements with data-i18n
 */
function applyLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('nexussave-lang', lang);

    // Update active button
    elements.langBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });

    // Update all i18n elements
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        el.textContent = t(key, lang);
    });

    // Update placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.dataset.i18nPlaceholder;
        el.placeholder = t(key, lang);
    });
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Language switcher
    elements.langBtns.forEach(btn => {
        btn.addEventListener('click', () => applyLanguage(btn.dataset.lang));
    });

    // Tabs
    elements.tabBtns.forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });

    // Downloader
    elements.videoUrl.addEventListener('input', detectPlatform);
    elements.videoUrl.addEventListener('paste', () => setTimeout(detectPlatform, 100));
    elements.fetchInfoBtn.addEventListener('click', fetchVideoInfo);
    elements.downloadBtn.addEventListener('click', downloadVideo);

    // Converter
    elements.dropzone.addEventListener('click', () => elements.fileInput.click());
    elements.dropzone.addEventListener('dragover', handleDragOver);
    elements.dropzone.addEventListener('dragleave', handleDragLeave);
    elements.dropzone.addEventListener('drop', handleDrop);
    elements.fileInput.addEventListener('change', handleFileSelect);
    elements.removeFileBtn.addEventListener('click', removeFile);
    elements.convertBtn.addEventListener('click', convertFile);

    // FFmpeg Modal
    if (elements.ffmpegInstallBtn) {
        elements.ffmpegInstallBtn.addEventListener('click', installFFmpeg);
    }
    if (elements.ffmpegCancelBtn) {
        elements.ffmpegCancelBtn.addEventListener('click', hideFFmpegModal);
    }
}

/**
 * Switch between tabs
 */
function switchTab(tabId) {
    elements.tabBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabId);
    });

    elements.tabContents.forEach(content => {
        content.classList.toggle('active', content.id === tabId);
    });
}

/**
 * Detect platform from URL
 */
function detectPlatform() {
    const url = elements.videoUrl.value.trim();

    // Reset icons
    elements.platformIcons.forEach(icon => icon.classList.remove('active'));

    if (!url) return;

    // Detect platform
    let detected = null;
    if (/tiktok\.com/i.test(url)) detected = 'tiktok';
    else if (/(twitter|x)\.com/i.test(url)) detected = 'twitter';
    else if (/instagram\.com/i.test(url)) detected = 'instagram';

    if (detected) {
        document.querySelector(`.platform-icon[data-platform="${detected}"]`)?.classList.add('active');
    }
}

/**
 * Fetch video info
 */
async function fetchVideoInfo() {
    const url = elements.videoUrl.value.trim();

    if (!url) {
        showMessage('downloader', t('errorEmptyUrl'), 'error');
        return;
    }

    // Detect platform first
    detectPlatform();

    try {
        elements.fetchInfoBtn.disabled = true;
        elements.fetchInfoBtn.textContent = '...';

        const response = await fetch('/api/info', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || t('errorInvalidUrl'));
        }

        // Store video info
        currentVideoInfo = { ...data, url };

        // Show preview
        let thumbnailUrl = data.thumbnail || '';
        
        // Debug: logging para verificar thumbnail
        console.log('Platform:', data.platform);
        console.log('Thumbnail URL:', thumbnailUrl);
        
        // Para Instagram e Twitter, sempre usar proxy para evitar CORS
        if (thumbnailUrl && (data.platform === 'instagram' || data.platform === 'twitter' || thumbnailUrl.includes('instagram') || thumbnailUrl.includes('cdninstagram') || thumbnailUrl.includes('fbcdn'))) {
            thumbnailUrl = '/api/proxy-image?url=' + encodeURIComponent(thumbnailUrl);
            console.log('Using proxy URL:', thumbnailUrl);
        }

        elements.previewThumbnail.src = thumbnailUrl;
        
        elements.previewThumbnail.onerror = function() {
            // Se falhar, tentar URL direta como fallback
            if (data.thumbnail && this.src !== data.thumbnail) {
                this.src = data.thumbnail;
            } else {
                this.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 68"><rect fill="%23111" width="120" height="68"/><text x="60" y="38" text-anchor="middle" fill="%23666" font-size="12">Preview</text></svg>';
            }
        };
        elements.previewTitle.textContent = data.title || t('downloading');

        // Montar meta com uploader e duração
        const metaParts = [];
        if (data.uploader) metaParts.push(data.uploader);
        if (data.duration) metaParts.push(formatDuration(data.duration));
        elements.previewMeta.textContent = metaParts.join(' • ') || 'Pronto para download';

        elements.videoPreview.classList.remove('hidden');
        elements.downloadBtn.classList.remove('hidden');

    } catch (error) {
        showMessage('downloader', error.message, 'error');
    } finally {
        elements.fetchInfoBtn.disabled = false;
        elements.fetchInfoBtn.textContent = t('fetchBtn');
    }
}

/**
 * Download video
 */
async function downloadVideo() {
    if (!currentVideoInfo) return;

    try {
        elements.downloadBtn.disabled = true;
        elements.progressContainer.classList.remove('hidden');
        elements.videoPreview.classList.add('hidden');

        const response = await fetch('/api/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: currentVideoInfo.url })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || t('errorDownload'));
        }

        // Get the blob
        const blob = await response.blob();

        // Extract filename from Content-Disposition header
        const disposition = response.headers.get('Content-Disposition');
        let filename = 'video.mp4';
        if (disposition) {
            const match = disposition.match(/filename\*?=['"]?(?:UTF-\d['"]*)?([^'";\s]+)/i);
            if (match) filename = decodeURIComponent(match[1]);
        }

        // Download file
        const downloadUrl = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(downloadUrl);

        showMessage('downloader', t('successDownload'), 'success');

    } catch (error) {
        showMessage('downloader', error.message, 'error');
    } finally {
        elements.downloadBtn.disabled = false;
        elements.progressContainer.classList.add('hidden');
    }
}

/**
 * Handle drag over
 */
function handleDragOver(e) {
    e.preventDefault();
    elements.dropzone.classList.add('dragover');
}

/**
 * Handle drag leave
 */
function handleDragLeave(e) {
    e.preventDefault();
    elements.dropzone.classList.remove('dragover');
}

/**
 * Handle drop
 */
function handleDrop(e) {
    e.preventDefault();
    elements.dropzone.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

/**
 * Handle file select
 */
function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

/**
 * Handle file
 */
function handleFile(file) {
    if (!file.name.toLowerCase().endsWith('.mp4')) {
        showMessage('converter', t('errorNoFile'), 'error');
        return;
    }

    elements.fileName.textContent = file.name;
    elements.dropzone.classList.add('hidden');
    elements.selectedFile.classList.remove('hidden');
    elements.convertBtn.classList.remove('hidden');
}

/**
 * Remove file
 */
function removeFile() {
    elements.fileInput.value = '';
    elements.selectedFile.classList.add('hidden');
    elements.dropzone.classList.remove('hidden');
    elements.convertBtn.classList.add('hidden');
    elements.converterMessage.classList.add('hidden');
}

/**
 * Convert file
 */
async function convertFile() {
    const file = elements.fileInput.files[0];
    if (!file) {
        showMessage('converter', t('errorNoFile'), 'error');
        return;
    }

    // Verificar FFmpeg antes de converter
    if (!ffmpegInstalled) {
        showFFmpegModal();
        return;
    }

    try {
        elements.convertBtn.disabled = true;
        elements.convertProgress.classList.remove('hidden');

        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/convert', {
            method: 'POST',
            body: formData
        });

        // Se houver erro, tentar parsear como JSON
        if (!response.ok) {
            const data = await response.json();

            // Verificar se precisa instalar FFmpeg
            if (data.need_ffmpeg) {
                showFFmpegModal();
                return;
            }

            throw new Error(data.error || t('errorConvert'));
        }

        // Sucesso - processar como blob
        const blob = await response.blob();

        // Extrair nome do arquivo
        const disposition = response.headers.get('Content-Disposition');
        let filename = 'audio.mp3';
        if (disposition) {
            const match = disposition.match(/filename\*?=['"]?(?:UTF-\d['"]*)?([^'";\s]+)/i);
            if (match) filename = decodeURIComponent(match[1]);
        }

        // Download do arquivo
        const downloadUrl = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(downloadUrl);

        showMessage('converter', t('successConvert'), 'success');

    } catch (error) {
        showMessage('converter', error.message, 'error');
    } finally {
        elements.convertBtn.disabled = false;
        elements.convertProgress.classList.add('hidden');
    }
}

/**
 * Show message
 */
function showMessage(type, text, status) {
    const messageEl = type === 'downloader' ? elements.downloaderMessage : elements.converterMessage;

    messageEl.textContent = text;
    messageEl.className = `message ${status}`;
    messageEl.classList.remove('hidden');

    // Auto-hide after 5 seconds
    setTimeout(() => {
        messageEl.classList.add('hidden');
    }, 5000);
}

/**
 * Format duration
 */
function formatDuration(seconds) {
    if (!seconds) return '0:00';
    // Garantir que seja um número inteiro
    seconds = Math.floor(Number(seconds));
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

/**
 * Check FFmpeg status
 */
async function checkFFmpeg() {
    try {
        const response = await fetch('/api/ffmpeg/status');
        const data = await response.json();
        ffmpegInstalled = data.installed;
        ffmpegInstalling = data.installing;
    } catch (error) {
        console.error('Error checking FFmpeg:', error);
    }
}

/**
 * Show FFmpeg installation modal
 */
function showFFmpegModal() {
    if (elements.ffmpegModal) {
        elements.ffmpegModal.classList.add('active');
    }
}

/**
 * Hide FFmpeg modal
 */
function hideFFmpegModal() {
    if (elements.ffmpegModal) {
        elements.ffmpegModal.classList.remove('active');
    }
}

/**
 * Install FFmpeg
 */
async function installFFmpeg() {
    if (ffmpegInstalling) return;

    try {
        ffmpegInstalling = true;

        // Mostrar progresso
        if (elements.ffmpegProgress) {
            elements.ffmpegProgress.classList.remove('hidden');
        }
        if (elements.ffmpegInstallBtn) {
            elements.ffmpegInstallBtn.disabled = true;
        }

        const response = await fetch('/api/ffmpeg/install', { method: 'POST' });
        const data = await response.json();

        // Poll para verificar se terminou
        const checkInterval = setInterval(async () => {
            try {
                const statusResponse = await fetch('/api/ffmpeg/status');
                const statusData = await statusResponse.json();

                if (statusData.installed) {
                    clearInterval(checkInterval);
                    ffmpegInstalled = true;
                    ffmpegInstalling = false;
                    hideFFmpegModal();

                    // Tentar converter novamente
                    convertFile();
                }
            } catch (error) {
                console.error('Error checking FFmpeg status:', error);
            }
        }, 2000);

        // Timeout após 2 minutos
        setTimeout(() => {
            clearInterval(checkInterval);
            ffmpegInstalling = false;
            if (elements.ffmpegInstallBtn) {
                elements.ffmpegInstallBtn.disabled = false;
            }
        }, 120000);

    } catch (error) {
        console.error('Error installing FFmpeg:', error);
        ffmpegInstalling = false;
        if (elements.ffmpegInstallBtn) {
            elements.ffmpegInstallBtn.disabled = false;
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', init);