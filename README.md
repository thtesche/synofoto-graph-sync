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

## 2. Installation on Synology

### Step A: Set up Python Environment
Connect to your NAS via SSH and run:

```bash
cd /volume1/scripts/photo-graph-sync
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step B: Configuration
Edit `sync.py` to match your environment:
- Set `NEO4J_CONFIG` password.
- Verify `PG_CONFIG` (default Unix socket is usually `/run/postgresql/`).
- Set `PHOTO_ROOT` to the path where your photos are stored (e.g., `/volume1/photo`).

### Step C: Database Access
The script needs to read the `synofoto` PostgreSQL database. When running via the **Synology Task Scheduler**, it should run as `root` to have direct access to the database socket.

---

## 3. Usage

### Connection Test
Verify that both the Synology DB and Neo4j are reachable:
```bash
python3 scripts/hello_world_check.py
```

### Run Sync
Execute the main synchronization:
```bash
python3 sync.py
```

---

## 4. Development Plan (Milestones)

| Phase | Content | Status |
| --- | --- | --- |
| **Milestone 1** | **Metadata Extractor** | ✅ Done |
| **Milestone 2** | **XMP Parser** | ⏳ Paused |
| **Milestone 3** | **Graph Importer** | ✅ Done |
| **Milestone 4** | **Automation** | ✅ Done |
