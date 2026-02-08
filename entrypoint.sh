#!/bin/bash
set -e

# AiNiee entrypoint script
# This is a PyQt5 desktop application with optional HTTP service

echo "Starting AiNiee..."
echo "Arguments: $@"

# If no arguments provided, run the main application
if [ $# -eq 0 ]; then
    exec python3 AiNiee.py
else
    # Execute with provided arguments
    exec python3 AiNiee.py "$@"
fi
