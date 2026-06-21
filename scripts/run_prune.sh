#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR/.."

# Log start time
echo "--- Prune started at $(date) ---" | tee -a prune.log

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "ERROR: virtual environment (venv) not found in $SCRIPT_DIR" >> prune.log
    exit 1
fi

# Run the cleanup script using the venv python
./venv/bin/python src/synofoto_graph_sync/cleanup.py "$@" 2>&1 | tee -a prune.log

# Log end time
echo "--- Prune finished at $(date) ---" | tee -a prune.log
echo "" >> prune.log
