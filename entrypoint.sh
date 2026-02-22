#!/bin/bash
set -e

cd /app

# Enable HTTP service in config if it doesn't exist or if the setting is missing
python3 << 'EOF'
import json
import os

config_file = "Resource/config.json"

# Try to load existing config or create new one
try:
    with open(config_file, 'r') as f:
        config = json.load(f)
except:
    config = {}

# Enable HTTP server
config['http_server_enable'] = True
config['http_listen_address'] = '0.0.0.0:3388'

# Save config
with open(config_file, 'w') as f:
    json.dump(config, f, indent=4, ensure_ascii=False)

print("HTTP service enabled on 0.0.0.0:3388")
EOF

# Run the application in headless mode
export QT_QPA_PLATFORM=offscreen
exec python AiNiee.py
