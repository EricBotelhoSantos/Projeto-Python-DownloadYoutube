# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies, including ffmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV DEPLOYED=true
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY web/requirements.txt .

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire web folder
COPY web/ ./web/

# Set working directory to the web folder for execution
WORKDIR /app/web

# Render (e outros PaaS) definem a variável PORT — não fixar 10000
# Aumentamos o timeout para 120s para permitir downloads de vídeos maiores
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-10000} --timeout 1200 --workers 2"]
