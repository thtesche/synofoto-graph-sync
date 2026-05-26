# Installation & Deployment

This guide covers how to set up the project locally and deploy it to your Synology NAS.

## Step A: Local Setup

Before deploying to the NAS, initialize your local environment and configuration:

1. Run the local setup script:

   ```bash
   ./scripts/setup_local.sh
   ```

   *This will create a `.env` file and prompt you for your NAS details.*

2. Run the SSH key setup script (Highly Recommended):

   ```bash
   ./scripts/setup_ssh_key.sh
   ```

   *This will generate an SSH key and copy it to your NAS to avoid password prompts.*

3. Open the newly created `.env` file and verify the settings, especially the `GRAPHDB_PASSWORD`.

### 💡 Troubleshooting SSH Key Login

If you are still prompted for a password, Synology's strict folder permissions are likely the cause. To fix this:

1. Log into your NAS via SSH (using your password).
2. Run these commands:

   ```bash
   chmod 711 ~
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys
   ```

*Note: SSH requires that only the owner has write access to these folders. Synology defaults are often too permissive.*

## Step B: Remote Directory Preparation (One-time)

Since system paths like `/volume1/scripts/` are protected, you must manually create the destination folder once and give your user ownership:

1. SSH into your NAS:

   ```bash
   ssh your_user@nas-ip
   ```

2. Create the folder with sudo:

   ```bash
   sudo mkdir -p /volume1/scripts/synofoto-graph-sync
   ```

3. Change ownership to your user:

   ```bash
   sudo chown your_user:users /volume1/scripts/synofoto-graph-sync
   ```

## Step C: Deploy to NAS

Use the `deploy_to_nas.sh` script to synchronize the project files to the NAS.

1. Run the script on your local machine:

   ```bash
   ./scripts/deploy_to_nas.sh
   ```

   *This script uses a `tar` pipe over SSH to copy only the necessary application files to your NAS.*

## Step D: Remote Setup (Python Environment)

If the deployment script indicates that the `venv` is missing on the NAS, perform the following once:

1. SSH into the NAS: `ssh your_user@nas-ip`.
2. Navigate to the project: `cd /volume1/scripts/synofoto-graph-sync`.
3. Create and initialize the environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Step E: Configuration Overview

| Service | Config Variable | Default | Role |
| --- | --- | --- | --- |
| **NAS SSH** | `NAS_USER` / `NAS_IP` | - | Used for deployment and SSH access. |
| **PostgreSQL** | `PG_DB` / `PG_HOST` | `synofoto` | The internal Synology Photos database. |
| **Graph DB** | `GRAPHDB_URI` | `bolt://...` | Connection URI for Memgraph or Neo4j. |
| **Task Scheduler** | - | `root` | Required for socket access to Postgres. |

## Step F: Running the Sync

You can run the synchronization manually at any time using the wrapper script:

```bash
sudo ./scripts/run_sync.sh
```

*Note: `sudo` is required to access the Synology Photos database socket.*
