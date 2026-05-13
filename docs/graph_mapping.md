# Data Mapping & Graph Structure (POLE+O)

This document describes the mapping between the Synology Photos PostgreSQL database and the Graph Database (Memgraph/Neo4j) structure, following the **POLE+O** (Photo, Owner, Location, Entity + Object) model.

## 1. Node Types (Labels)

### Photo
The central node representing a media unit (image).
- **Source Table**: `unit`, `metadata`, `folder`
- **Properties**:
  - `id`: Internal Synology unit ID (e.g., `55839`)
  - `filename`: Original filename (e.g., `20260227_091142.jpg`)
  - `path`: Folder path relative to photo root (e.g., `/2026/02`)
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
| `:LOCATED_AT` | `Photo` | `City` | Links a photo to its most specific location (City). |
| `:PART_OF` | `City` | `Region` | Hierarchical link from City to Region. |
| `:PART_OF` | `Region` | `Country` | Hierarchical link from Region to Country. |

---

## 3. Transformation Logic

### Location (Hierarchy)
Geographical entities are derived from the `address` table. Due to varying administrative divisions across countries, we use Synology's internal `level` property to assign semantic labels:
- **Level 1**: `:Country`
- **Level 2**: `:State` (e.g., Brandenburg, Bavaria)
- **Level 3**: `:County` (e.g., Barnim, Landkreis Wolfenbüttel)
- **Level 4**: `:City` (e.g., Panketal, St. Lorenz)
- **Level 5**: `:District` (e.g., Schwanebeck)
- **Level 6+**: `:Street` (e.g., Zillertaler Straße, Hirschsteig)

The Importer creates a semantic chain based on available levels:
`Photo -[:LOCATED_AT]-> [Most Specific] -[:PART_OF]-> [Higher Level] -[:PART_OF]-> Country`.

*Note: If a level is missing in the source data, the chain skips it and links directly to the next higher available level.*

### Tag Merging
Tags are gathered from two sources and merged before import:
- **Synology DB**: `general_tag` (AI recognition).
- **XMP Files**: Sidecar or embedded metadata (User-defined tags).

### Family Extraction
The `Family` node is created by splitting the `Person.name` by space. If a surname is detected, a `Family` node is created and linked to the `Person`.
