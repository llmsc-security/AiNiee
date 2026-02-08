#!/bin/bash

# AiNiee Docker invocation script
# Note: This is primarily a GUI application, but can be run headless with HTTP API

# Configuration
CONTAINER_NAME="ainiee"
HOST_PORT=11460
CONTAINER_PORT=3388
IMAGE_NAME="ainiee:latest"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Check if container is already running
if docker ps | grep -q "$CONTAINER_NAME"; then
    echo "Container '$CONTAINER_NAME' is already running."
    echo "To restart it, run: docker restart $CONTAINER_NAME"
    exit 0
fi

echo "Starting AiNiee in headless mode..."
echo "Note: To enable the HTTP API, you need to:"
echo "  1. Create a config.json with 'http_server_enable': true"
echo "  2. Set 'http_listen_address' to '0.0.0.0:3388'"
echo "  3. Mount it to Resource/config.json in the container"
echo ""

# Run the container (headless mode - no display)
# The HTTP service needs to be enabled in the config file
docker run -d \
    --name "$CONTAINER_NAME" \
    -p "$HOST_PORT:$CONTAINER_PORT" \
    -e QT_QPA_PLATFORM="offscreen" \
    --restart unless-stopped \
    "$IMAGE_NAME"

echo "AiNiee started successfully!"
echo "Port mapping: ${HOST_PORT}:${CONTAINER_PORT}"
echo "HTTP API will be available at http://localhost:${HOST_PORT} when enabled in config"
echo "To stop the container: docker stop $CONTAINER_NAME"
echo "To view logs: docker logs -f $CONTAINER_NAME"
