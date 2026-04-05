# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies, including ffmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV RENDER=true
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

# Command to run the app using Gunicorn
# Aumentamos o timeout para 120s para permitir downloads de vídeos maiores
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000", "--timeout", "120"]
