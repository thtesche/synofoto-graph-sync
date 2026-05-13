# Synology Photos to LPG Mapping

Um deine KI-IDE optimal für die Extraktion und den Aufbau des Labeled Property Graphs (LPG) in Memgraph vorzubereiten, habe ich die relevanten Tabellen und Beziehungsstrukturen aus der internen PostgreSQL-Datenbank (`synofoto`) von Synology Photos analysiert.

Hier ist das Mapping, das du deiner KI-IDE übergeben kannst, damit sie die SQL-Tabellen in das POLE+O Graph-Modell übersetzt:

## 1. Photo (Entity - Anker-Knoten)

Die Kerninformationen der Bilder sind auf mehrere Tabellen aufgeteilt, die über IDs verknüpft sind.

* **Tabelle `unit`:** Repräsentiert das eigentliche Foto. Wichtige Spalten sind `id` (Primärschlüssel), `filename` und `id_folder`.
* **Tabelle `item`:** Speichert grundlegende Datei-Metadaten wie den Pfad, den Typ (Foto/Video) und Zeitstempel.
* **Tabelle `metadata`:** Enthält technische EXIF-Daten (z.B. ISO, Brennweite, Kameramodell). Diese Tabelle ist über die Spalte `id_unit` direkt mit der Tabelle `unit` verknüpft.

## 2. Person (Entity)

Für die Gesichtserkennung nutzt Synology zwei Tabellen, die die Person mit dem Foto verbinden.

* **Tabelle `person`:** Verwaltet die eindeutig identifizierten Personen und deren Namen.
* **Tabelle `face`:** Enthält die eigentlichen Gesichtserkennungsdaten (Bounding Boxes / Koordinaten des Gesichts auf dem Bild). Sie fungiert als Brücke und verknüpft die identifizierte Person mit dem jeweiligen Foto.

## 3. Location (Entity)

Geografische Daten liegen sowohl als Rohkoordinaten als auch als aufgelöste Adressen vor.

* **Tabelle `metadata`:** Speichert die rohen GPS-Koordinaten (`latitude` und `longitude`) für die jeweilige `id_unit`.
* **Tabelle `address`:** Beinhaltet die detaillierten, hierarchischen Adressdaten (z. B. Stadt, Bundesland, Land). Über die Spalte `level` lässt sich die Granularität steuern und über `lang = 0` werden die Standardsprach-Einträge gefiltert.

## 4. Object (Entity)

Von der KI erkannte Motive und abstrakte Konzepte werden in Synology Photos als Tags behandelt.

* **Tabelle `general_tag`:** Speichert die Namen der erkannten Objekte/Tags.
* **Verknüpfungstabelle `many_unit_has_many_general_tag`:** Verknüpft ein Foto (`id_unit`) mit den IDs der Tags aus `general_tag`.

## 5. Owner & Family (Entities - Besonderheiten)

* **Owner:** Der Besitzer eines Fotos wird direkt über die Tabelle `user_info` identifiziert. Die Verknüpfung erfolgt von `unit.id_user` auf `user_info.id`. Der Name des Owners wird für die Erstellung der `Owner`-Knoten im Graphen verwendet.
* **Family:** Synology Photos hat kein natives Konzept für "Familiennamen". Die KI extrahiert diese Entity algorithmisch aus den Namen der Tabelle `person` (z. B. durch Splitten von Vor- und Nachnamen) und generiert daraus eigenständige `Family`-Knoten.
