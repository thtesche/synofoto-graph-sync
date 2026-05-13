#!/bin/bash

# Load configuration from .env
if [ -f .env ]; then
    export $(grep -v '^[[:space:]]*#' .env | grep -v '^[[:space:]]*$' | xargs)
else
    echo "Error: .env file not found. Please run ./setup_local.sh first."
    exit 1
fi

# Ensure mandatory variables are set
if [ -z "$NAS_USER" ] || [ -z "$NAS_IP" ] || [ -z "$NAS_DEST_PATH" ]; then
    echo "Error: NAS configuration missing in .env."
    exit 1
fi

SSH_OPTS="-o StrictHostKeyChecking=no -o LogLevel=ERROR"

echo "--- Syncing Files to NAS (using tar pipe) ---"
# COPYFILE_DISABLE=1 prevents Mac from adding ._ files to the archive
# We also explicitly exclude ._* files
COPYFILE_DISABLE=1 tar -cz \
    --exclude='venv' \
    --exclude='.git' \
    --exclude='.DS_Store' \
    --exclude='__pycache__' \
    --exclude='._*' \
    --exclude='.github' \
    --exclude='.agents' \
    --exclude='.benchmarks' \
    --exclude='.ruff_cache' \
    --exclude='.pytest_cache' \
    --exclude='docs' \
    --exclude='tests' \
    --exclude='design' \
    --exclude='scratch' \
    --exclude='*.md' \
    --exclude='test.py' \
    --exclude='*.log' \
    --exclude='pyproject.toml' \
    --exclude='setup_*.sh' \
    --exclude='copy_to_nas.sh' \
    --exclude='.env.example' \
    --exclude='.gitignore' \
    -f - . | ssh ${NAS_USER}@${NAS_IP} "tar -xz -C ${NAS_DEST_PATH}"

if [ $? -ne 0 ]; then
    echo "Error: Transfer failed."
    exit 1
fi

# Cleanup existing ._ files and setup scripts on NAS if any were already copied
ssh ${NAS_USER}@${NAS_IP} "find ${NAS_DEST_PATH} -name '._*' -delete; rm -f ${NAS_DEST_PATH}/setup_*.sh ${NAS_DEST_PATH}/copy_to_nas.sh ${NAS_DEST_PATH}/*.md ${NAS_DEST_PATH}/.env.example ${NAS_DEST_PATH}/.gitignore ${NAS_DEST_PATH}/test.py ${NAS_DEST_PATH}/*.log ${NAS_DEST_PATH}/pyproject.toml; rm -rf ${NAS_DEST_PATH}/.github ${NAS_DEST_PATH}/.agents ${NAS_DEST_PATH}/.benchmarks ${NAS_DEST_PATH}/.ruff_cache ${NAS_DEST_PATH}/.pytest_cache ${NAS_DEST_PATH}/docs ${NAS_DEST_PATH}/tests ${NAS_DEST_PATH}/design ${NAS_DEST_PATH}/scratch"

echo "--- Checking NAS Status ---"
ssh $SSH_OPTS ${NAS_USER}@${NAS_IP} << nas_ssh
    if [ ! -d "${NAS_DEST_PATH}/venv" ]; then
        echo "STATUS: Python environment (venv) is missing on NAS."
        echo "ACTION: Run 'python3 -m venv venv' inside ${NAS_DEST_PATH} on the NAS."
    else
        echo "STATUS: Remote environment is ready."
    fi
nas_ssh

echo "--- Finished ---"
