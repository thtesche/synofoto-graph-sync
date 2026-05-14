#!/bin/bash

# Load configuration from .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: .env file not found. Please run ./setup_local.sh first."
    exit 1
fi

echo "--- SSH Key Setup for ${NAS_USER}@${NAS_IP} ---"

# 1. Check if local key exists, if not generate one
if [ ! -f ~/.ssh/id_ed25519.pub ] && [ ! -f ~/.ssh/id_rsa.pub ]; then
    echo "No SSH key found. Generating a new Ed25519 key..."
    ssh-keygen -t ed25519 -C "synofoto-graph-sync" -f ~/.ssh/id_ed25519 -N ""
fi

# 2. Copy key to NAS
echo "Copying your public key to the NAS. You will be asked for your password ONE LAST TIME."
ssh-copy-id -o StrictHostKeyChecking=no ${NAS_USER}@${NAS_IP}

if [ $? -eq 0 ]; then
    echo "--- Success! ---"
    echo "You should now be able to run ./deploy_to_nas.sh without a password."
else
    echo "--- Failed to copy key ---"
    echo "Make sure SSH is enabled on your Synology (Control Panel -> Terminal & SNMP)."
fi
