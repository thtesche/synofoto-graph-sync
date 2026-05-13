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

* **Tabelle `metadata`:** Speichert neben den EXIF-Daten auch die rohen GPS-Koordinaten (Latitude und Longitude) für die jeweilige `id_unit`.
* **Tabelle `address`:** Beinhaltet die strukturierten und semantischen Geodaten (z.B. Stadt, Land). Über die Bedingung `lang = 0` lassen sich die Standardsprach-Einträge filtern.

## 4. Object (Entity)

Von der KI erkannte Motive und abstrakte Konzepte werden in Synology Photos als Tags behandelt.

* **Tabelle `general_tag`:** Speichert die Namen der erkannten Objekte/Tags (oft mit einer normalisierten, kleingeschriebenen Version des Namens).
* **Verknüpfungstabelle `many_unit_has_many_general_tag`:** Dies ist die relationale n:m-Tabelle. Sie enthält die Kanten (Relationships), die ein Foto (über `id_unit` oder `id_item`) mit der ID des Objekts aus `general_tag` verbinden.

## 5. Owner & Family (Entities - Besonderheiten)

*Hinweis für die Implementierungslogik der KI-IDE:*

* **Owner:** Es gibt in der `synofoto`-Datenbank keine explizite "Besitzer"-Tabelle für einzelne Fotos. Der Besitzer (Tenant) lässt sich jedoch über die **Tabelle `folder**` ableiten. Dort sind die Dateipfade gespeichert. Fotos im Pfad `/home/Photos/` gehören zum persönlichen Speicherplatz eines spezifischen Nutzers, während Fotos unter `/photo/` im freigegebenen Bereich liegen.
* **Family:** Synology Photos hat kein natives Konzept für "Familiennamen". Deine KI muss diese Entity bei der Graph-Erstellung algorithmisch aus den Namens-Strings der Tabelle `person` extrahieren (z. B. durch Splitten von Vor- und Nachnamen) und daraus eigenständige `Family`-Knoten generieren.
