#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR/.."

# Log start time
echo "--- Sync started at $(date) ---" | tee -a sync.log

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "ERROR: virtual environment (venv) not found in $SCRIPT_DIR" >> sync.log
    exit 1
fi

# Run the sync script using the venv python
# We use tee -a to show output on console AND write to log
./venv/bin/python sync.py "$@" 2>&1 | tee -a sync.log

# Log end time
echo "--- Sync finished at $(date) ---" | tee -a sync.log
echo "" >> sync.log
