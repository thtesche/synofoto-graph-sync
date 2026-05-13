# Data Mapping & Graph Structure (POLE+O)

This document describes the mapping between the Synology Photos PostgreSQL database and the Graph Database (Memgraph/Neo4j) structure, following the **POLE+O** (Photo, Owner, Location, Entity + Object) model.

## 1. Node Types (Labels)

### Photo
The central node representing a media unit (image).
- **Source Table**: `unit`, `metadata`, `folder`
- **Properties**:
  - `id`: Internal Synology unit ID (e.g., `55839`)
  - `filename`: Original filename (e.g., `20260227_091142.jpg`)
  - `path`: Absolute folder path on the NAS (e.g., `/volume1/photo/2026/02`)
  - `latitude`: GPS Latitude (if available)
  - `longitude`: GPS Longitude (if available)

### Owner
The user who owns the photo.
- **Source Table**: `user_info` (via `unit.id_user`)
- **Properties**:
  - `name`: Synology username (e.g., `thtesche`)

### Person
A recognized face in a photo.
- **Source Table**: `person` (via `face` bridge table)
- **Properties**:
  - `name`: Full name of the person.

### Family
A grouping of persons based on their surname.
- **Source**: Algorithmically derived from `Person.name`.
- **Properties**:
  - `name`: Surname (e.g., `Tesche`)

### Object
AI-recognized tags or objects.
- **Source Table**: `general_tag` and XMP Metadata.
- **Properties**:
  - `name`: Tag name (e.g., `Vineyard`, `Landscape`)

### Location (Hierarchy)
Geographical entities derived from the address table.
- **Source Table**: `address` (levels 1-5)
- **Labels**: `Country`, `Region`, `City`
- **Properties**:
  - `name`: Name of the location part (e.g., `Germany`, `Baden-Württemberg`)

---

## 2. Relationships

| Relationship | Source Node | Target Node | Description |
| --- | --- | --- | --- |
| `:OWNED_BY` | `Photo` | `Owner` | Links a photo to its owner. |
| `:HAS_PERSON` | `Photo` | `Person` | Links a photo to the recognized persons. |
| `:BELONGS_TO_FAMILY` | `Person` | `Family` | Groups persons into families. |
| `:HAS_OBJECT` | `Photo` | `Object` | Links a photo to AI tags and objects. |
| `:LOCATED_AT` | `Photo` | `Location` | Links a photo to its most specific location. |
| `:PART_OF` | `Location` | `Location` | Hierarchical link (e.g., Street -> City -> Country). |

---

## 3. Transformation Logic

### Location Hierarchy (POLE+O: Location)

Geodata is extracted from the `address` table. Due to inconsistent level numbering in Synology Photos, we use a **Poly-Labeling Strategy**:

- **Labels**:
    - Every node: `:Location`
    - First node (Index 0): `:Country`
    - Last node: `:Street` (only if more than 1 node exists)
- **Properties**:
    - `name`: The address component string (e.g., "Deutschland").
    - `type`: Guessed semantic type based on position (`Country`, `State`, `County`, `City`, `District`, `Street`).
    - `index`: Relative position (0-based).
    - `level`: The original Synology DB level ID.
- **Relationships**:
    - `(Photo)-[:LOCATED_AT]->(Location)` (to the most specific location).
    - `(Location)-[:PART_OF]->(Location)` (to the parent in the hierarchy).

This strategy ensures that nodes like "Berlin" remain unique even if they appear at different levels in different photo metadata records.

---

## 5. Implementation Notes

### Tag Merging
Tags are gathered from two sources and merged before import:
- **Synology DB**: `general_tag` (AI recognition).
- **XMP Files**: Sidecar or embedded metadata (User-defined tags).

### Family Extraction
The `Family` node is created by splitting the `Person.name` by space. If a surname is detected, a `Family` node is created and linked to the `Person`.

---

## 6. Useful Cypher Queries

For a detailed list of useful queries, see [useful_queries.md](useful_queries.md).

### Quick Status Check
```cypher
MATCH (n) RETURN labels(n) as labels, count(n) as count;
```

### Find Photos by Country
```cypher
MATCH (l:Location {name: 'Deutschland'})<-[:PART_OF*0..]-(loc)<-[:LOCATED_AT]-(p:Photo) 
RETURN p.filename, loc.name;
```
