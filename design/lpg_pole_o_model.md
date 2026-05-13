# Synology Photos to LPG Mapping

To optimally prepare your AI IDE for the extraction and construction of the Labeled Property Graph (LPG) in Memgraph, I have analyzed the relevant tables and relationship structures from the internal PostgreSQL database (`synofoto`) of Synology Photos.

Here is the mapping you can provide to your AI IDE so it can translate the SQL tables into the POLE+O graph model:

## 1. Photo (Entity - Anchor Node)

The core information of the images is split across several tables linked by IDs.

* **Table `unit`:** Represents the actual photo. Important columns are `id` (primary key), `filename`, and `id_folder`.
* **Table `item`:** Stores basic file metadata such as path, type (photo/video), and timestamps.
* **Table `metadata`:** Contains technical EXIF data (e.g., ISO, focal length, camera model). This table is directly linked to the `unit` table via the `id_unit` column.

## 2. Person (Entity)

For facial recognition, Synology uses two tables that connect the person to the photo.

* **Table `person`:** Manages uniquely identified persons and their names.
* **Table `face`:** Contains the actual facial recognition data (bounding boxes / coordinates of the face on the image). It acts as a bridge, linking the identified person to the respective photo.

## 3. Location (Entity)

Geographical data is available both as raw coordinates and as resolved addresses.

* **Table `metadata`:** Stores the raw GPS coordinates (`latitude` and `longitude`) for the respective `id_unit`.
* **Table `address`:** Contains detailed, hierarchical address data (e.g., city, state, country). The granularity can be controlled via the `level` column, and default language entries are filtered via `lang = 0`.

## 4. Object (Entity)

Motifs recognized by AI and abstract concepts are treated as tags in Synology Photos.

* **Table `general_tag`:** Stores the names of the recognized objects/tags.
* **Linking Table `many_unit_has_many_general_tag`:** Links a photo (`id_unit`) with the IDs of the tags from `general_tag`.

## 5. Owner & Family (Entities - Special Cases)

* **Owner:** The owner of a photo is identified directly via the `user_info` table. The link is from `unit.id_user` to `user_info.id`. The name of the owner is used to create `Owner` nodes in the graph.
* **Family:** Synology Photos does not have a native concept for "surnames". The AI algorithmically extracts this entity from the names in the `person` table (e.g., by splitting first and last names) and generates independent `Family` nodes from them.
