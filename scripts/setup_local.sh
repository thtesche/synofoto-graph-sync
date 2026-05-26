#!/bin/bash

echo "--- Local Setup: Synofoto-Graph-Sync ---"

# Get the directory where this script is located and cd to project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR/.."

if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    
    echo "Please enter your NAS configuration:"
    read -p "NAS Username: " nas_user
    read -p "NAS IP Address: " nas_ip
    read -p "NAS Destination Path [/volume1/scripts/synofoto-graph-sync]: " nas_path
    nas_path=${nas_path:-/volume1/scripts/synofoto-graph-sync}
    
    # Update .env with sed (handling both macOS and Linux sed)
    sed -i.bak "s/NAS_USER=your_user/NAS_USER=$nas_user/" .env
    sed -i.bak "s/NAS_IP=192.168.1.10/NAS_IP=$nas_ip/" .env
    sed -i.bak "s|NAS_DEST_PATH=/volume1/scripts/synofoto-graph-sync|NAS_DEST_PATH=$nas_path|" .env
    rm .env.bak
    
    echo ".env file created. Please open it to configure your database passwords."
else
    echo ".env file already exists."
fi

# Optional: Setup local venv for IDE support
if [ ! -d venv ]; then
    read -p "Do you want to create a local virtual environment for development? (y/n) " create_venv
    if [[ $create_venv == "y" ]]; then
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        echo "Local venv created and dependencies installed."
    fi
fi

echo "--- Setup complete ---"
