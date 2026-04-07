"""
NexusSave Backend - Flask API
Download de vídeos de redes sociais e conversão MP4→MP3
"""

import os
import re
import uuid
import zipfile
import subprocess
import threading
import time
import tempfile
import platform
import shutil
from pathlib import Path
from flask import Flask, Response, render_template, request, jsonify, send_file
import urllib.request

app = Flask(__name__)

# Determinar se estamos em ambiente de servidor (Docker/Render)
IS_SERVER = os.environ.get('RENDER') or os.environ.get('DOCKER')

# Configurações - Diretórios
if IS_SERVER:
    DOWNLOADS_DIR = Path('/tmp/nexussave/downloads')
    TEMP_DIR = Path('/tmp/nexussave/temp')
else:
    # Local (Windows/macOS)
    user_downloads = os.path.expanduser('~/Downloads')
    if os.path.exists(user_downloads) and os.access(user_downloads, os.W_OK):
        DOWNLOADS_DIR = Path(user_downloads)
    else:
        DOWNLOADS_DIR = Path(os.path.expanduser('~'))
    TEMP_DIR = Path(tempfile.gettempdir()) / 'nexussave'

# Diretório para jobs de conversão
CONVERT_DIR = TEMP_DIR / 'jobs'

# Criar diretórios se não existirem
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
CONVERT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# FFmpeg paths
if platform.system() == 'Windows':
    FFMPEG_DIR = Path(os.environ.get('APPDATA', os.path.expanduser('~'))) / 'NexusSave' / 'ffmpeg'
    FFMPEG_EXE = FFMPEG_DIR / 'ffmpeg.exe'
else:
    # No Linux/Docker, esperamos que o ffmpeg esteja no PATH do sistema
    FFMPEG_DIR = Path('/usr/bin')
    FFMPEG_EXE = Path('ffmpeg')

# Status de instalação do FFmpeg
ffmpeg_installing = False

# Limite de upload: 2GB (suporta arquivos MP4 de longa duração)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

# Jobs de conversão (armazenados em memória)
# Estrutura: {job_id: {'status': 'pending'|'converting'|'done'|'error', 'output_path': Path, 'error': str, 'progress': int}}
convert_jobs: dict[str, dict] = {}

# Limpeza periódica de jobs antigos
def limpar_jobs_antigos():
    """Remove jobs finalizados com mais de 1 hora do armazenamento."""
    while True:
        time.sleep(3600)
        for job_id in list(convert_jobs.keys()):
            job = convert_jobs[job_id]
            if job['status'] in ('done', 'error') and job.get('created_at', 0) < time.time() - 3600:
                # Remove arquivos temporários
                for key in ('input_path', 'output_path'):
                    p = job.get(key)
                    if p and p.exists():
                        try:
                            p.unlink()
                        except Exception:
                            pass
                del convert_jobs[job_id]
threading.Thread(target=limpar_jobs_antigos, daemon=True).start()

# Padrões de URL por plataforma
PLATFORM_PATTERNS = {
    'tiktok': [
        r'(https?://)?(www\.)?tiktok\.com/@[\w.-]+/video/\d+',
        r'(https?://)?(vm\.)?tiktok\.com/\w+'
    ],
    'twitter': [
        r'(https?://)?(www\.)?(twitter|x)\.com/\w+/status/\d+'
    ],
    'instagram': [
        r'(https?://)?(www\.)?instagram\.com/(p|reel|reels)/[\w-]+'
    ]
}


def detect_platform(url):
    """Detecta a plataforma a partir da URL"""
    for platform, patterns in PLATFORM_PATTERNS.items():
        for pattern in patterns:
            if re.match(pattern, url, re.IGNORECASE):
                return platform
    return None


def check_ffmpeg():
    """Verifica se o FFmpeg está disponível"""
    global ffmpeg_installing

    if ffmpeg_installing:
        return False

    # Verificar se existe no diretório do app
    if FFMPEG_EXE.exists():
        return True

    # Verificar se está no PATH do sistema
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


def get_ffmpeg_path():
    """Retorna o caminho do executável FFmpeg"""
    if FFMPEG_EXE.exists():
        return str(FFMPEG_EXE)
    return 'ffmpeg'


def download_ffmpeg():
    """Baixa e instala o FFmpeg automaticamente (Apenas Windows)"""
    global ffmpeg_installing

    if platform.system() != 'Windows':
        print("Instalação automática do FFmpeg só é necessária no Windows.")
        return False

    ffmpeg_installing = True

    try:
        FFMPEG_DIR.mkdir(parents=True, exist_ok=True)

        # URL do FFmpeg para Windows (build essencial)
        ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

        zip_path = FFMPEG_DIR / 'ffmpeg.zip'

        # Baixar FFmpeg
        print("Baixando FFmpeg...")
        urllib.request.urlretrieve(ffmpeg_url, zip_path)

        # Extrair
        print("Extraindo FFmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Encontrar a pasta dentro do zip
            for member in zip_ref.namelist():
                if member.endswith('ffmpeg.exe'):
                    # Extrair ffmpeg.exe
                    source = member
                    target = FFMPEG_DIR / 'ffmpeg.exe'
                    with zip_ref.open(source) as source_file:
                        with open(target, 'wb') as target_file:
                            target_file.write(source_file.read())
                elif member.endswith('ffprobe.exe'):
                    # Extrair ffprobe.exe também
                    source = member
                    target = FFMPEG_DIR / 'ffprobe.exe'
                    with zip_ref.open(source) as source_file:
                        with open(target, 'wb') as target_file:
                            target_file.write(source_file.read())

        # Limpar zip
        if zip_path.exists():
            zip_path.unlink()

        print("FFmpeg instalado com sucesso!")
        ffmpeg_installing = False
        return True

    except Exception as e:
        print(f"Erro ao instalar FFmpeg: {e}")
        ffmpeg_installing = False
        return False


def cleanup_file(filepath, delay=600):
    """Remove arquivo após delay (10 minutos por padrão)"""
    def remove():
        time.sleep(delay)
        try:
            if filepath.exists():
                filepath.unlink()
        except Exception:
            pass
    threading.Thread(target=remove, daemon=True).start()


@app.route('/')
def index():
    """Serve a página principal"""
    return render_template('index.html')


@app.route('/api/ffmpeg/status', methods=['GET'])
def ffmpeg_status():
    """Retorna o status do FFmpeg"""
    return jsonify({
        'installed': check_ffmpeg(),
        'installing': ffmpeg_installing
    })


@app.route('/api/ffmpeg/install', methods=['POST'])
def ffmpeg_install():
    """Instala o FFmpeg automaticamente"""
    global ffmpeg_installing

    if ffmpeg_installing:
        return jsonify({'error': 'Instalação já em andamento'}), 400

    if check_ffmpeg():
        return jsonify({'message': 'FFmpeg já está instalado'})

    # Executar instalação em background
    def install():
        download_ffmpeg()

    thread = threading.Thread(target=install, daemon=True)
    thread.start()

    return jsonify({'message': 'Instalação iniciada', 'installing': True})


@app.route('/api/detect', methods=['POST'])
def detect():
    """Detecta a plataforma da URL"""
    data = request.get_json()
    url = data.get('url', '').strip()

    if not url:
        return jsonify({'error': 'URL não fornecida'}), 400

    platform = detect_platform(url)

    if not platform:
        return jsonify({'error': 'Plataforma não suportada', 'supported': ['tiktok', 'twitter', 'instagram']}), 400

    return jsonify({'platform': platform})


@app.route('/api/info', methods=['POST'])
def get_info():
    """Retorna informações do vídeo sem baixar"""
    data = request.get_json()
    url = data.get('url', '').strip()

    if not url:
        return jsonify({'error': 'URL não fornecida'}), 400

    platform = detect_platform(url)
    if not platform:
        return jsonify({'error': 'Plataforma não suportada'}), 400

    try:
        import yt_dlp

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # Extrair título (Instagram as vezes retorna "Video by username")
            title = info.get('title', '')
            if not title or title.lower().startswith('video by'):
                # Tentar pegar da descrição
                description = info.get('description', '')
                if description:
                    # Pegar primeira linha da descrição (geralmente é o título/caption)
                    first_line = description.split('\n')[0][:100]
                    if first_line and not first_line.lower().startswith('video by'):
                        title = first_line
                    else:
                        title = 'Video do Instagram'
                else:
                    title = 'Video do Instagram'

            # Extrair thumbnail (Instagram pode ter em campos diferentes)
            thumbnail = info.get('thumbnail', '')

            if not thumbnail:
                # Tentar pegar de thumbnails
                if 'thumbnails' in info and info['thumbnails']:
                    # Pegar a maior qualidade (geralmente a última)
                    for t in reversed(info['thumbnails']):
                        if 'url' in t and t['url']:
                            thumbnail = t['url']
                            break
                # Tentar outros campos
                if not thumbnail:
                    thumbnail = info.get('display_url', '') or info.get('full_display_url', '')

            # Debug: imprimir thumbnail no console do servidor
            print(f"[DEBUG] Thumbnail para {platform}: {thumbnail}")

            # Extrair duração (arredondar para segundos inteiros)
            duration = info.get('duration', 0)
            if duration:
                duration = int(duration)

            # Extrair uploader (Instagram usa uploader_id ou channel)
            uploader = info.get('uploader', '')
            if not uploader or uploader.lower().startswith('video by'):
                uploader = info.get('uploader_id', '') or info.get('channel', '') or ''
                # Limpar @ se existir
                if uploader and uploader.startswith('@'):
                    uploader = uploader[1:]

            return jsonify({
                'title': title,
                'thumbnail': thumbnail,
                'duration': duration,
                'uploader': uploader,
                'platform': platform
            })

    except Exception as e:
        print(f"[ERROR] get_info: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/proxy-image')
def proxy_image():
    """Proxy para imagens com CORS bloqueado (ex: Instagram)"""
    image_url = request.args.get('url', '')
    if not image_url:
        return jsonify({'error': 'URL não fornecida'}), 400

    try:
        req = urllib.request.Request(image_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response = urllib.request.urlopen(req, timeout=10)

        # Ler a imagem
        image_data = response.read()
        content_type = response.headers.get('Content-Type', 'image/jpeg')

        return Response(image_data, mimetype=content_type)

    except Exception as e:
        print(f"[ERROR] Proxy image: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/download', methods=['POST'])
def download_video():
    """Baixa o vídeo da rede social"""
    data = request.get_json()
    url = data.get('url', '').strip()

    if not url:
        return jsonify({'error': 'URL não fornecida'}), 400

    platform = detect_platform(url)
    if not platform:
        return jsonify({'error': 'Plataforma não suportada'}), 400

    try:
        import yt_dlp

        # Nome único para o arquivo
        file_id = str(uuid.uuid4())[:8]

        # Opções do yt-dlp
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'outtmpl': str(DOWNLOADS_DIR / f'{file_id}_%(title).50s.%(ext)s'),
            'format': 'best',
            'extractor_args': {
                'youtube': {
                    'player_client': ['web', 'android', 'ios']
                }
            },
            'http_timeout': 60,
        }

        # TikTok sem marca d'água
        if platform == 'tiktok':
            ydl_opts['format'] = 'best'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            if not info:
                return jsonify({'error': 'Não foi possível processar o vídeo'}), 500

            # Obter título do info (mais confiável)
            video_title = info.get('title') or ''

            if not video_title or video_title.lower().startswith('video by'):
                description = info.get('description', '')
                if description:
                    video_title = description.split('\n')[0][:100]
                if not video_title or video_title.lower().startswith('video by'):
                    video_title = f'video_{platform}_{file_id}'

            # Sanitizar título para nome de arquivo
            safe_title = re.sub(r'[^\w\s-]', '', video_title)[:50].strip()
            if not safe_title:
                safe_title = f'video_{platform}_{file_id}'

            # Encontrar o arquivo baixado
            filename = ydl.prepare_filename(info)
            filepath = Path(filename)

            if not filepath.exists():
                # Procurar arquivo com o ID
                files = list(DOWNLOADS_DIR.glob(f'{file_id}_*'))
                if files:
                    filepath = files[0]
                else:
                    return jsonify({'error': 'Arquivo não encontrado'}), 500

            # Agendar limpeza
            cleanup_file(filepath)

            print(f"[DEBUG] Filename: {filepath.name}, safe_title: {safe_title}")
            ext = filepath.suffix

            response = send_file(
                filepath,
                as_attachment=True,
                download_name=f'{safe_title}{ext}'
            )

            return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/convert', methods=['POST'])
def convert_video():
    """Inicia conversão MP4→MP3 em background (modelo assíncrono)."""
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

    # Verificar extensão
    filename = file.filename
    if not filename or not filename.lower().endswith('.mp4'):
        return jsonify({'error': 'Apenas arquivos MP4 são aceitos'}), 400

    # Verificar FFmpeg
    if not check_ffmpeg():
        return jsonify({'error': 'FFmpeg não encontrado', 'need_ffmpeg': True}), 400

    try:
        # Criar job
        job_id = str(uuid.uuid4())
        input_path = CONVERT_DIR / f'{job_id}_input.mp4'
        output_path = CONVERT_DIR / f'{job_id}_output.mp3'

        file.save(input_path)

        # Registrar job
        convert_jobs[job_id] = {
            'status': 'pending',
            'progress': 0,
            'input_path': input_path,
            'output_path': output_path,
            'original_name': filename,
            'error': None,
            'created_at': time.time(),
        }

        def run_conversion():
            job = convert_jobs[job_id]
            ffmpeg_cmd = get_ffmpeg_path()
            try:
                job['status'] = 'converting'
                job['progress'] = 1

                result = subprocess.run(
                    [ffmpeg_cmd, '-i', str(input_path), '-vn', '-acodec', 'libmp3lame', '-q:a', '2', str(output_path)],
                    capture_output=True,
                    text=True,
                    timeout=3600  # 1 hora max
                )

                # Limpar input
                if input_path.exists():
                    try:
                        input_path.unlink()
                    except Exception:
                        pass

                if result.returncode != 0:
                    error_detail = result.stderr.strip()[:200] if result.stderr else 'Erro desconhecido'
                    print(f'[ERROR] FFmpeg convert ({job_id}): {error_detail}')
                    job['status'] = 'error'
                    job['error'] = error_detail
                    return

                if not output_path.exists() or output_path.stat().st_size == 0:
                    job['status'] = 'error'
                    job['error'] = 'Falha na conversão: arquivo vazio'
                    return

                job['status'] = 'done'
                job['progress'] = 100

            except subprocess.TimeoutExpired:
                job['status'] = 'error'
                job['error'] = 'Tempo de conversão excedido (1h)'
            except Exception as e:
                job['status'] = 'error'
                job['error'] = str(e)

        threading.Thread(target=run_conversion, daemon=True).start()

        return jsonify({'job_id': job_id, 'status': 'pending'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/convert/status/<job_id>', methods=['GET'])
def convert_status(job_id):
    """Retorna o status de um job de conversão."""
    job = convert_jobs.get(job_id)
    if not job:
        return jsonify({'error': 'Job não encontrado'}), 404

    response = {
        'status': job['status'],
        'progress': job['progress'],
    }
    if job['status'] == 'error':
        response['error'] = job['error']
    if job['status'] == 'done':
        response['filename'] = re.sub(r'[^\w\s-]', '', job['original_name'][:-4])[:50] if job.get('original_name') else 'audio'
    return jsonify(response)


@app.route('/api/convert/download/<job_id>', methods=['GET'])
def convert_download(job_id):
    """Baixa o arquivo MP3 convertido."""
    job = convert_jobs.get(job_id)
    if not job:
        return jsonify({'error': 'Job não encontrado'}), 404

    if job['status'] != 'done':
        return jsonify({'error': 'Conversão ainda não está pronta'}), 400

    output_path = job['output_path']
    if not output_path.exists():
        return jsonify({'error': 'Arquivo MP3 não encontrado'}), 500

    safe_name = re.sub(r'[^\w\s-]', '', job['original_name'][:-4])[:50] if job.get('original_name') else 'audio'

    # Agendar limpeza
    cleanup_file(output_path)

    # Remover job após download (com delay para evitar race condition)
    def remove_job():
        time.sleep(60)
        if job_id in convert_jobs:
            job = convert_jobs.pop(job_id, None)

    threading.Thread(target=remove_job, daemon=True).start()

    return send_file(
        output_path,
        as_attachment=True,
        download_name=f'{safe_name}.mp3',
        mimetype='audio/mpeg',
    )


port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    print("NexusSave Backend iniciando...")
    print("Downloads:", DOWNLOADS_DIR)
    app.run(debug=False, host='0.0.0.0', port=port, use_reloader=False)