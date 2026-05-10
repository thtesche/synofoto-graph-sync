# Synofoto-Graph-Sync

**Goal:** Synchronize Synology Photos metadata and AI tags into a Neo4j GraphDB.

---

## 📂 Project Structure

- `sync.py`: Main entry point for the synchronization process.
- `src/synofoto_graph_sync/`: Core logic modules.
  - `extractor.py`: Handles PostgreSQL data extraction.
  - `parser.py`: Extracts XMP/EXIF tags from image files.
  - `importer.py`: Handles Neo4j data ingestion.
- `requirements.txt`: Python dependencies.

---

## 1. Preparation: Neo4j Docker Container

Before the script can run, we need the Graph Database. On the Synology, it's best to use the **Container Manager** (Docker).

**Docker Run Command (or via Compose):**
Create a new instance with the following parameters:

- **Image:** `neo4j:latest`
- **Ports:**
  - `7474` (HTTP for the browser interface)
  - `7687` (Bolt protocol for the Python script)
- **Volumes:** Create a folder `/docker/neo4j/data` to store data persistently.
- **Environment Variables:**
  - `NEO4J_AUTH=neo4j/your_password`

---

## 2. Installation on Synology

### Step A: Set up Python Environment

1. Connect to the Synology via SSH: `ssh user@nas-ip`.
2. Create directory: `mkdir -p /volume1/scripts/photo-graph-sync`.
3. Create virtual environment:

```bash
cd /volume1/scripts/photo-graph-sync
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step B: Configuration

Edit `sync.py` to set your Neo4j password and database paths if they differ from the defaults.

### Step C: Allow Database Access

To allow the script to read the `synofoto` DB, the `root` user or an authorized user must be used. Since the script runs as `root` via the Task Scheduler, access to the Unix socket is usually directly possible.

---

## 3. Usage

### Connection Test

Run the check script to verify both databases are reachable:

```bash
python3 scripts/hello_world_check.py
```

### Run Sync

Run the main synchronization script:

```bash
python3 sync.py
```

---

## 4. Development Plan (Milestones)

| Phase | Content | Status |
| --- | --- | --- |
| **Milestone 1** | **Metadata Extractor** | ✅ Done |
| **Milestone 2** | **XMP Parser** | ✅ Done |
| **Milestone 3** | **Graph Importer** | ✅ Done |
| **Milestone 4** | **Automation** | ✅ Done |
