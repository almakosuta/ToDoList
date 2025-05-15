# Todo List API

Dieses Projekt ist eine einfache REST-API zum Verwalten von Todo Listen und deren Einträgen entwickelt mit Python und Flask.

Die API unterstützt CRUD-Operationen (Create, Read, Update, Delete) für:
- Todo Listen
- Einträge innerhalb dieser Listen

---

## Features

- Erstellung und Verwaltung von mehreren Todo-Listen
- Erstellung, Aktualisierung und Löschung von Todo-Einträgen
- Zugriff auf alle Listen und zugehörige Aufgaben
- Statuscodes und Fehlerbehandlung gemäß REST-Standard
- Vorbereitete Beispiel-Daten mit festen Listen-IDs und zufällig generierten Einträgen

---

## Setup

### Voraussetzungen

- Python 3.7 oder höher
- Flask (Installiere mit pip)

### Installation

```bash
pip install flask
```

### Starten

```bash
python app.py
```

API ist dann verfügbar unter:

```
http://localhost:5000
```

---

## Beispiel-Daten

Beim Start enthält das Projekt automatisch:

- **4 Todo-Listen:**
  - `Einkaufsliste`
  - `Arbeit`
  - `Reisen`
  - `Fitness`

- **Jeweils zwei Aufgaben pro Liste**, z. B.:
  - `Milch kaufen` (Einkaufsliste)
  - `Code Review` (Arbeit)
  - `Hotel buchen` (Reisen)
  - `Joggen gehen` (Fitness)

Die Aufgaben erhalten bei jedem Neustart automatisch neue `UUIDs`.

---

## API-Endpunkte

### Alle Listen abrufen

```http
GET /todo-lists
```

**Antwort:** Liste aller vorhandenen Todo-Listen

---

### Neue Liste erstellen

```http
POST /todo-list
```

**Body:**

```json
{
  "name": "Neue Liste"
}
```

**Antwort:** Neue Liste mit generierter ID

---

### Einzelne Liste abrufen oder löschen

```http
GET    /todo-list/<list_id>
DELETE /todo-list/<list_id>
```

- **Antwort (GET):** Details der Liste (`id`, `name`)
- **Antwort (DELETE):** `{ "msg": "success" }`

---

### Aufgaben einer Liste abrufen

```http
GET /todo-list/<list_id>/entries
```

**Antwort:**

```json
[
  {
    "id": "uuid",
    "name": "Joggen gehen",
    "description": "5km im Park"
  }
]
```

---

### Neue Aufgabe zu Liste hinzufügen

```http
POST /todo-list/<list_id>/entry
```

**Body:**

```json
{
  "name": "Hotel buchen",
  "description": "3 Nächte in Berlin"
}
```

**Antwort:** Neuer Eintrag mit generierter `id`

---

### Aufgabe aktualisieren oder löschen

```http
PUT    /todo-list/<list_id>/entry/<entry_id>
DELETE /todo-list/<list_id>/entry/<entry_id>
```

**Body (PUT):**

```json
{
  "name": "Hotel buchen",
  "description": "3 Nächte in Berlin"
}
```

- **Antwort (PUT):** Aktualisierter Eintrag
- **Antwort (DELETE):** `{ "msg": "success" }`

---

## Projektstruktur

```
todo-api/
├── ToDoListServer.py           # Hauptcode mit API und Beispieldaten
├── README.md        # Dokumentation (diese Datei)
```

---

## Lizenz
Dieses Projekt steht under der MIT-Lizenz.

