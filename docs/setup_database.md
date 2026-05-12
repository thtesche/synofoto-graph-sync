# Graph Database Setup

To host the graph database on your Synology NAS, you can choose between **Neo4j** (the industry standard) and **Memgraph** (a high-performance, in-memory graph database). Both are Bolt-compatible and work seamlessly with the sync scripts.

## 📦 Container Manager Installation

If not already installed, open the **Package Center**, search for **Container Manager**, and click **Install**.

---

## 🔵 Option 1: Memgraph (Recommended for Performance)

Memgraph is optimized for speed and works exceptionally well on NAS systems with limited resources.

### 1. Folder & Permission Setup

To correctly set permissions for the container user, you need to execute commands via the terminal:

1. **Enable SSH**: Ensure SSH is enabled in DSM (**Control Panel** -> **Terminal & SNMP**).
2. **Connect via SSH**: Open your terminal (macOS/Linux) or PuTTY (Windows) and connect:

   ```bash
   ssh your_username@NAS_IP_ADDRESS
   ```

3. **Create & Fix Permissions**: Run the following commands to ensure Memgraph has write access to the persistent storage:

   ```bash
   # Create directories if they don't exist
   mkdir -p /volume1/docker/memgraph/data /volume1/docker/memgraph/log

   # Change ownership to the container user (1026:100)
   sudo chown -R 1026:100 /volume1/docker/memgraph/data
   sudo chown -R 1026:100 /volume1/docker/memgraph/log
   ```

### 2. Create the Project

1. Open **Container Manager** -> **Project** -> **Create**.
2. **Project Name**: `memgraph-sync`.
3. **Path**: Select `/docker/memgraph`.
4. **Source**: Select "Create docker-compose.yaml" and paste the following configuration:

```yaml
version: "3"
services:
  memgraph:
    image: memgraph/memgraph:latest
    container_name: memgraph-server
    user: "1026:100"
    ports:
      - "7687:7687"
      - "7444:7444"
    environment:
      - MEMGRAPH_USER=admin
      - MEMGRAPH_PASSWORD=admin
    volumes:
      - /volume1/docker/memgraph/data:/var/lib/memgraph
      - /volume1/docker/memgraph/log:/var/log/memgraph
    # Memory limit for 2GB NAS systems
    deploy:
      resources:
        limits:
          memory: 1G
```

1. Click **Next** and follow the wizard to start the project.

---

## 🟢 Option 2: Neo4j (Classic Setup)

Neo4j provides a robust environment and a powerful web interface for exploring your photo graph.

### 1. Download Image

1. Go to **Registry** in Container Manager.
2. Search for `neo4j` and download the `latest` tag.

### 2. Configure persistent storage

1. Open **File Station** and create `/docker/neo4j/data` and `/docker/neo4j/logs`.
2. Set permissions for the `neo4j` folder:
   - Properties -> Permission -> Create.
   - User: `Everyone`, Permissions: `Read & Write`.
   - Check **Apply to this folder, sub-folders and files**.

### 3. Run the Container

1. Go to **Image**, select `neo4j`, and click **Run**.
2. **Port Settings**:
   - `7474` -> `7474` (HTTP UI)
   - `7687` -> `7687` (Bolt protocol)
3. **Volume Settings**:
   - `/docker/neo4j/data` -> `/data`
   - `/docker/neo4j/logs` -> `/logs`
4. **Environment Variables**:
   - `NEO4J_AUTH` = `neo4j/your_password`

---

**💡 Tipp:** Nach der Einrichtung kannst du die Verbindung prüfen, indem du `http://[NAS-IP]:7474` (Neo4j) öffnest oder einen Bolt-Client (Memgraph) verwendest, um sicherzustellen, dass der Dienst läuft.
