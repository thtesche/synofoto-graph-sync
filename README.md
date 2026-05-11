# Synofoto-Graph-Sync

**Goal:** Synchronize Synology Photos metadata and AI tags into a Neo4j Graph Database to enable powerful graph-based discovery and relationship analysis.

---

## Requirements

- **Synology DSM 7.x** with Synology Photos installed.
- **SSH access** to the NAS.
- **Python 3.10+** (Included in DSM 7.x or available via Package Center).
- **Container Manager** (formerly Docker) installed on the NAS.
- **sudo privileges** for database access.

---

## 1. Preparation: Neo4j Docker Setup

To host the graph database on your Synology NAS, follow these steps in the **Container Manager**:

### A. Install Container Manager

If not already installed, open the **Package Center**, search for "Container Manager", and click **Install**.

### B. Download Neo4j Image

1. Open **Container Manager**.
2. Go to **Registry** on the left sidebar.
3. Search for `neo4j`.
4. Select the official `neo4j` image and click **Download**.
5. Choose the `latest` tag.

### C. Create Folder Structure & Permissions

Before running the container, create persistent storage folders and set appropriate permissions:

1. Open **File Station**.
2. Navigate to your `docker` share (or create it).
3. Create a folder named `neo4j`.
4. Inside `neo4j`, create two subfolders: `data` and `logs`.
5. **Set Permissions**: Right-click the `neo4j` folder, select **Properties** -> **Permission**.
   - Click **Create** (or **Edit**).
   - Select `Everyone` as the User/Group.
   - Check **Read** and **Write** permissions.
   - Check the box **Apply to this folder, sub-folders and files**.
   - Click **Done** and **Save**.

### D. Configure and Run the Container

1. In **Container Manager**, go to **Image** and select the downloaded `neo4j:latest`, then click **Run**.
2. **General Settings**: Give it a name (e.g., `neo4j-sync`).
3. **Port Settings**:
   - `7474` -> `7474` (HTTP interface)
   - `7687` -> `7687` (Bolt protocol for Python)
   - *Optional:* `7473` -> `7473` (HTTPS interface)
4. **Volume Settings**:
   - Map `/docker/neo4j/data` to `/data` (Read/Write)
   - Map `/docker/neo4j/logs` to `/logs` (Read/Write)
5. **Environment Variables**:
   - Add `NEO4J_AUTH` with value `neo4j/your_password`.
6. **Network**: Use the default `bridge` network.
7. Click **Next**, review the settings, and click **Done** to start the container.

---

---

## 2. Installation & Deployment

### Step A: Local Setup

Before deploying to the NAS, initialize your local environment and configuration:

1. Run the local setup script:

   ```bash
   ./setup_local.sh
   ```

   *This will create a `.env` file and prompt you for your NAS details.*

2. Run the SSH key setup script (Highly Recommended):

   ```bash
   ./setup_ssh_key.sh
   ```

   *This will generate an SSH key and copy it to your NAS to avoid password prompts.*

3. Open the newly created `.env` file and verify the settings, especially the `NEO4J_PASSWORD`.

#### 💡 Troubleshooting SSH Key Login

If you are still prompted for a password, Synology's strict folder permissions are likely the cause. To fix this:

1. Log into your NAS via SSH (using your password).
2. Run these commands:

   ```bash
   chmod 711 ~
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys
   ```

*Note: SSH requires that only the owner has write access to these folders. Synology defaults are often too permissive.*

### Step B: Remote Directory Preparation (One-time)

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

### Step C: Deploy to NAS

Use the `copy_to_nas.sh` script to synchronize the project files to the NAS.

1. Run the script on your local machine:

   ```bash
   ./copy_to_nas.sh
   ```

   *This script uses a `tar` pipe over SSH to copy only the necessary application files to your NAS.*

### Step D: Remote Setup (Python Environment)

If the deployment script indicates that the `venv` is missing on the NAS, perform the following once:

1. SSH into the NAS: `ssh your_user@nas-ip`.
2. Navigate to the project: `cd /volume1/scripts/synofoto-graph-sync`.
3. Create and initialize the environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Step E: User & Database Configuration

| Service | Config Variable | Default | Role |
| --- | --- | --- | --- |
| **NAS SSH** | `NAS_USER` / `NAS_IP` | - | Used for deployment and SSH access. |
| **PostgreSQL** | `PG_DB` / `PG_HOST` | `synofoto` | The internal Synology Photos database. |
| **Neo4j** | `NEO4J_PASSWORD` | `your_password` | The graph database administrator account. |
| **Task Scheduler** | - | `root` | Required for socket access to Postgres. |

---

## 3. Usage

### Connection Test (Doctor Mode)

Before running a full sync, verify that both databases are reachable using the built-in diagnostic tool:

```bash
# Must be run as root or via sudo for Postgres socket access
sudo venv/bin/python sync.py --doctor
```

*This checks both the PostgreSQL Unix socket and the Neo4j Bolt connection.*

### Run Sync

Execute the main synchronization:

```bash
sudo venv/bin/python sync.py
```

---

## 4. Automation (Task Scheduler)

To keep your graph database up-to-date, set up a task in the **Synology Task Scheduler**:

1. Open **Control Panel** -> **Task Scheduler**.
2. Click **Create** -> **Scheduled Task** -> **User-defined script**.
3. **General**: Task name `Photo-Graph-Sync`, User `root`.
4. **Schedule**: Set to Daily or hourly as desired.
5. **Task Settings**: Run command:

   ```bash
   cd /volume1/scripts/synofoto-graph-sync && ./venv/bin/python sync.py >> sync.log 2>&1
   ```

---

## 5. Development Plan (Milestones)

| Phase | Content | Status |
| --- | --- | --- |
| **Milestone 1** | **Metadata Extractor** | ✅ Done |
| **Milestone 2** | **XMP Parser** | ⏳ Paused |
| **Milestone 3** | **Graph Importer** | ✅ Done |
| **Milestone 4** | **Automation** | ✅ Done |
