# Synofoto-Graph-Sync

**Goal:** Synchronize Synology Photos metadata and AI tags into a Graph Database (Memgraph or Neo4j) to enable powerful graph-based discovery and relationship analysis.

---

## 🚀 Quick Start

1. **[Database Setup](docs/setup_database.md)**: Install Neo4j or Memgraph on your NAS via Container Manager.
2. **[Installation](docs/installation.md)**: Run `./setup_local.sh` and deploy to NAS with `./copy_to_nas.sh`.
3. **[Automation](docs/automation.md)**: Schedule the sync task in Synology Task Scheduler.

---

## 📋 Requirements

- **Synology DSM 7.x** with Synology Photos.
- **Python 3.8+** (on NAS).
- **SSH access** & **Container Manager** (recommended).
- **sudo/root privileges** (for database access).

---

## 🛠 Usage

### Connection Test (Doctor Mode)

Verify that both databases are reachable:

```bash
sudo venv/bin/python sync.py --doctor
```

### Run Sync

Execute the main synchronization:

```bash
sudo venv/bin/python sync.py
```

---

## 📂 Detailed Documentation

- [Graph Database Setup Guide](docs/setup_database.md) - Docker configuration & permissions.
- [Installation & Deployment](docs/installation.md) - Local setup, SSH keys, and NAS deployment.
- [Automation Guide](docs/automation.md) - Setting up the Synology Task Scheduler.
- [Graph Model Design (POLE+O)](design/lpg_pole_o_model.md) - Mapping between Postgres and Graph DB.
- [Synology Photos Schema](design/synofoto_schema.md) - Reference for the synofoto database.

---

## 📈 Development Plan (Milestones)

| Phase | Content | Status |
| --- | --- | --- |
| **Milestone 1** | **Metadata Extractor** | ✅ DONE |
| **Milestone 2** | **XMP Parser** | ✅ DONE |
| **Milestone 3** | **Graph Importer** | ✅ DONE |
| **Milestone 4** | **Automation** | ✅ DONE |
