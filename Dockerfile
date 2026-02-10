# Use Python 3.11 slim as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -g 1000 appuser && useradd -u 1000 -g appuser -m appuser

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY AiNiee.py .
COPY ModuleFolders ./ModuleFolders
COPY PluginScripts ./PluginScripts
COPY Resource ./Resource
COPY UserInterface ./UserInterface

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Note: This is a PyQt5 desktop application (not a web app by default).
# The app has an optional HTTP service (default port 3388) that can be enabled
# in the config file (Resource/config.json) by setting:
#   "http_server_enable": true
#   "http_listen_address": "0.0.0.0:3388"
# For Docker, we disable the GUI and run headless, or use VNC for GUI access.
# This image is designed for headless operation with HTTP API access.

# The HTTP service is disabled by default in the config.
# To enable it, mount a custom config or modify the config.json file.

# Working directory
WORKDIR /app

# Enable HTTP service by modifying the config at runtime
# Run the app with Python (headless mode with HTTP API)
CMD ["python", "AiNiee.py"]
