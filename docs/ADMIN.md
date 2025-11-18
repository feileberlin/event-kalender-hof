# 🔧 Admin-Dokumentation

Dokumentation für Administratoren des Event-Kalender Hof.

## 📋 Übersicht

Als Admin bist du verantwortlich für:
- Prüfung automatisch gescrapeter Events
- Publikation von Entwürfen
- Manuelle Event-Erstellung
- Pflege der Event-Quellen

## 🚀 Schnellstart

### Admin-Interface öffnen

→ [https://feileberlin.github.io/event-kalender-hof/admin/](https://feileberlin.github.io/event-kalender-hof/admin/)

## 📅 Event-Verwaltung

### Event-Status

| Status | Bedeutung | Sichtbarkeit | Löschbar |
|--------|-----------|--------------|----------|
| `Entwurf` | Automatisch gescraped oder unveröffentlicht | ❌ Nicht auf Website | ✅ Ja |
| `Öffentlich` | Geprüft und freigegeben | ✅ Auf Website sichtbar | ❌ Nein* |
| `Archiviert` | Vergangene oder stornierte Events | ❌ Nicht auf Website | ❌ Nein* |

**\*Wichtig:** Einmal veröffentlichte Events können **nicht gelöscht** werden, nur archiviert! Dies verhindert defekte Links und bewahrt die Event-Historie.

### Workflow: Entwurf publizieren

1. **Admin-Interface öffnen**: `/admin/`
2. **Event prüfen**: Titel, Datum, Ort, Beschreibung kontrollieren
3. **GitHub Editor öffnen**: Klick auf "Bearbeiten (GitHub)"
4. **Status ändern**: `status: "Entwurf"` → `status: "Öffentlich"`
5. **Speichern**: Commit Message eingeben → "Commit changes"
6. **Deployment**: Automatisch in 1-2 Minuten live

### Workflow: Event archivieren

**Für vergangene oder stornierte Events:**

1. **Admin-Interface öffnen**: `/admin/`
2. **Event auswählen**: Veröffentlichtes Event finden
3. **Archivieren klicken**: Button "📦 Archivieren"
4. **GitHub Editor öffnet sich** automatisch
5. **Status ändern**: `status: "Öffentlich"` → `status: "Archiviert"`
6. **Speichern**: Commit Message: "Event archiviert"
7. **Deployment**: Event verschwindet von der Website

**Archivierte Events:**
- ❌ Nicht mehr auf Website sichtbar
- ✅ Bleiben im Repository erhalten
- ✅ URLs bleiben gültig (404-Seite zeigt Archiv-Hinweis)
- ✅ Git-Historie bleibt vollständig

### Workflow: Entwurf löschen

**Nur für unveröffentlichte Entwürfe:**

1. **Admin-Interface öffnen**: Tab "Entwürfe"
2. **Event auswählen**: Entwurf finden
3. **Löschen klicken**: Button "🗑️ Löschen"
4. **GitHub Repository öffnet sich**
5. **Datei löschen**: `_events/YYYY-MM-DD-titel.md` entfernen
6. **Commit**: "Entwurf gelöscht"

### Flyer-Analyse (AI-powered)

**Automatische Event-Extraktion aus Flyern (Bilder/PDFs)**

#### Verwendung

```bash
python scripts/analyze_flyer.py <URL>
```

**Beispiel:**
```bash
python scripts/analyze_flyer.py https://example.com/event-flyer.jpg
```

#### Unterstützte Formate

- **Bilder**: JPG, PNG, GIF, WebP
- **PDFs**: Mehrseitige Dokumente

#### AI-Provider (automatische Auswahl)

1. **GitHub Models API** (GPT-4o-mini via GITHUB_TOKEN)
   - Beste Qualität
   - Kostenlos für GitHub-User
   - Automatisch verfügbar im Dev Container

2. **DuckDuckGo AI Chat** (Fallback)
   - Kostenlos, keine API-Key nötig
   - Nutzt GPT-3.5-turbo

3. **Lokales OCR** (Tesseract, letzte Option)
   - Reine Texterkennung
   - Regex-basierte Extraktion

#### Workflow

1. **Flyer-URL kopieren** (z.B. von Facebook, Instagram, Website)
2. **Script ausführen**:
   ```bash
   python scripts/analyze_flyer.py https://example.com/flyer.jpg
   ```
3. **Event-Datei wird erstellt** in `_events/` mit `status: "Entwurf"`
4. **Prüfen und korrigieren** im Admin-Interface
5. **Publizieren**: Status auf `"Öffentlich"` ändern

#### Extrahierte Daten

- ✅ Titel
- ✅ Datum & Uhrzeit
- ✅ Veranstaltungsort
- ✅ Adresse (automatisch geocodiert)
- ✅ Kategorie
- ✅ Beschreibung
- ✅ Tags
- ✅ URL
- ✅ Eintrittspreis

#### Geocoding

Adressen werden automatisch in Koordinaten umgewandelt:
- **API**: OpenStreetMap Nominatim
- **Fallback**: Rathaus Hof (50.3197, 11.9168)

#### Wichtig

- ⚠️ **Immer prüfen!** AI kann Fehler machen
- ⚠️ **Status bleibt "Entwurf"** bis manuelle Freigabe
- ✅ Koordinaten werden validiert
- ✅ Datum/Zeit-Format wird normalisiert

### Manuelles Event erstellen

#### Schritt 1: Datei erstellen

Neue Datei in `_events/` mit Format: `YYYY-MM-DD-event-titel.md`

**Beispiel:** `2025-11-25-konzert-freiheitshalle.md`

#### Schritt 2: YAML Front Matter

```yaml
---
title: "Konzert in der Freiheitshalle"
date: 2025-11-25
start_time: "20:00"
end_time: "23:00"
location: "Freiheitshalle Hof"
address: "Kulmbacher Str. 4, 95028 Hof"
coordinates:
  lat: 50.3197
  lng: 11.9168
category: "Musik"
tags:
  - Live-Musik
  - Rock
description: "Ein unvergesslicher Abend mit lokalen Bands"
url: "https://freiheitshalle-hof.de/events/konzert"
status: "Öffentlich"
source: "Manuell"
---
```

#### Schritt 3: Optional - Markdown-Content

Nach dem `---` kannst du ausführliche Beschreibungen hinzufügen:

```markdown
---
# (YAML Front Matter wie oben)
---

## Über das Event

Detaillierte Beschreibung mit **Markdown-Formatierung**.

### Line-Up
- Band 1
- Band 2
- Band 3

### Tickets

Tickets gibt es [hier](https://example.com/tickets).
```

#### Schritt 4: Committen

```bash
git add _events/2025-11-25-konzert-freiheitshalle.md
git commit -m "Event: Konzert Freiheitshalle am 25.11."
git push
```

### Event editieren

1. GitHub → Repository → `_events/`
2. Datei öffnen
3. Pencil-Icon (Edit) klicken
4. Änderungen vornehmen
5. "Commit changes" mit Beschreibung

### Event löschen

1. GitHub → Repository → `_events/`
2. Datei öffnen
3. Trash-Icon (Delete) klicken
4. "Commit changes"

## 🔄 Batch-Operationen

### Alle Entwürfe publizieren

**Linux/macOS:**
```bash
cd _events/
for file in *.md; do
  sed -i 's/status: "Entwurf"/status: "Öffentlich"/' "$file"
done
git add .
git commit -m "Publish all drafts"
git push
```

**Windows (PowerShell):**
```powershell
cd _events
Get-ChildItem *.md | ForEach-Object {
  (Get-Content $_.FullName) -replace 'status: "Entwurf"', 'status: "Öffentlich"' | Set-Content $_.FullName
}
git add .
git commit -m "Publish all drafts"
git push
```

### Alte Events löschen

**Älter als 30 Tage:**
```bash
find _events/ -name "*.md" -mtime +30 -delete
git add .
git commit -m "Remove events older than 30 days"
git push
```

**Älter als bestimmtes Datum:**
```bash
# Alle Events vor 2025-11-01 löschen
find _events/ -name "2025-10-*.md" -delete
find _events/ -name "2025-09-*.md" -delete
git add .
git commit -m "Remove events before November 2025"
git push
```

## 🤖 Scraping-Konfiguration

### Event-Quellen verwalten

**Datei:** `scripts/scrape_events.py`

#### Neue Quelle hinzufügen

```python
SOURCES = [
    {
        "name": "Neue Venue",
        "url": "https://example.com/events",
        "type": "html",
        "selector": ".event-item",  # CSS Selector
        "enabled": True
    },
]
```

#### Quelle deaktivieren

```python
{
    "name": "Alte Venue",
    "url": "https://old-venue.com/events",
    "enabled": False  # Temporär deaktivieren
}
```

### Scraping-Frequenz ändern

**Datei:** `.github/workflows/scrape-events.yml`

```yaml
on:
  schedule:
    - cron: '0 6,18 * * *'  # Aktuell: Täglich 6:00 und 18:00 UTC
```

**Cron-Beispiele:**
| Cron | Frequenz |
|------|----------|
| `0 * * * *` | Jede Stunde |
| `0 */3 * * *` | Alle 3 Stunden |
| `0 0 * * *` | Täglich um Mitternacht |
| `0 0 * * 1` | Jeden Montag um Mitternacht |
| `0 6 * * 1-5` | Werktags um 6:00 UTC |

### Manuelles Scraping auslösen

1. GitHub → Repository → **Actions** Tab
2. Workflow "Event Scraper" auswählen
3. **Run workflow** → Branch "main" → **Run workflow**
4. Warte auf grünen Haken ✅
5. Events erscheinen in `_events/` als Entwürfe

## 📊 Kategorien & Tags

### Verfügbare Kategorien

| Kategorie | Icon | Verwendung |
|-----------|------|------------|
| `Musik` | 🎵 | Konzerte, Festivals, Live-Musik |
| `Theater` | 🎭 | Schauspiel, Kabarett, Comedy |
| `Sport` | ⚽ | Sportveranstaltungen, Turniere |
| `Kultur` | 🎨 | Ausstellungen, Lesungen, Kunst |
| `Markt` | 🛒 | Wochenmärkte, Flohmärkte |
| `Fest` | 🎉 | Stadtfeste, Volksfeste |
| `Sonstiges` | 📅 | Andere Events |

### Tag-Empfehlungen

**Musik:**
- Live-Musik, Rock, Pop, Jazz, Klassik, Electronic, Folk

**Theater:**
- Schauspiel, Kabarett, Comedy, Musical, Improvisation

**Sport:**
- Fußball, Basketball, Handball, Laufen, Radsport

**Kultur:**
- Ausstellung, Lesung, Vortrag, Workshop, Film

## 🗺️ Koordinaten finden

### Option 1: Google Maps

1. Rechtsklick auf Ort in Google Maps
2. Koordinaten anzeigen lassen
3. Format: `50.3197, 11.9168`

### Option 2: OpenStreetMap

1. [openstreetmap.org](https://www.openstreetmap.org/)
2. Ort suchen
3. Rechtsklick → "Adresse anzeigen"
4. Koordinaten kopieren

### Option 3: Online-Tools

- [latlong.net](https://www.latlong.net/)
- [gps-coordinates.net](https://gps-coordinates.net/)

### Hof Standard-Koordinaten

| Ort | Lat | Lng |
|-----|-----|-----|
| Rathaus Hof | 50.3197 | 11.9168 |
| Freiheitshalle | 50.3242 | 11.9156 |
| Theresienstein | 50.3289 | 11.9045 |
| Altstadt | 50.3201 | 11.9175 |

## 🚨 Troubleshooting

### Events werden nicht angezeigt

**Prüfe:**
1. ✅ `status: "Öffentlich"` gesetzt?
2. ✅ Datum in der Zukunft? (Events bis 6:30 Uhr Folgetag)
3. ✅ YAML-Syntax korrekt? (keine Tabs, richtige Einrückung)
4. ✅ Jekyll Build erfolgreich? (GitHub Actions → Grüner Haken)

### Scraper findet keine Events

**Prüfe:**
1. ✅ URL erreichbar? (Browser-Test)
2. ✅ Quell-Website hat Events?
3. ✅ CSS-Selector korrekt? (Browser DevTools)
4. ✅ Workflow läuft? (GitHub Actions)

### Koordinaten falsch

**Symptome:**
- Event erscheint nicht auf Karte
- Marker an falscher Position

**Lösung:**
- Format prüfen: `lat: 50.3197` (Punkt statt Komma)
- Reihenfolge: `lat` zuerst, dann `lng`
- Bereich: Hof liegt bei ca. 50.32° N, 11.92° E

## 📞 Support

Bei Fragen oder Problemen:
- **GitHub Issues**: [github.com/feileberlin/event-kalender-hof/issues](https://github.com/feileberlin/event-kalender-hof/issues)
- **Discussions**: [github.com/feileberlin/event-kalender-hof/discussions](https://github.com/feileberlin/event-kalender-hof/discussions)
