# Synofoto-Graph-Sync

**Goal:** Synchronize Synology Photos metadata and AI tags into a Neo4j GraphDB.

---

## 📂 Project Structure

- `hello_world_check.py`: Connection test for PostgreSQL and Neo4j.
- `README.md`: This documentation.
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
pip install psycopg2-binary py2neo
```

### Step B: Allow Database Access

To allow the script to read the `synofoto` DB, the `root` user or an authorized user must be used. Since the script runs as `root` via the Task Scheduler, access to the Unix socket is usually directly possible.

---

## 3. Development Plan (Milestones)

| Phase | Content | Goal |
| --- | --- | --- |
| **Milestone 1** | **Metadata Extractor** | Read `unit_id`, `path`, and `person_name` from Postgres. |
| **Milestone 2** | **XMP Parser** | Open image file from path and extract AI keywords/tags. |
| **Milestone 3** | **Graph Importer** | Write `MERGE` statements in Cypher to avoid duplicates. |
| **Milestone 4** | **Automation** | Set up cronjob in Synology Task Scheduler. |
