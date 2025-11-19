# Scraping Logs

Dieses Verzeichnis enthält detaillierte Logfiles von allen Scraping-Durchläufen.

## Dateiformat

`YYYYMMDD-HHMMSS-scraping.log`

Beispiel: `20251119-180101-scraping.log`

## Inhalt der Logs

Jedes Logfile dokumentiert einen kompletten Scraping-Durchlauf und enthält:

### 1. **Session-Start**
- Timestamp
- Anzahl geladener Venues

### 2. **Quellen-Processing**
- Für jede gescrapte Quelle (Website, API, etc.):
  - Quellname und URL
  - Anzahl gefundener Event-Elemente
  - Parsing-Ergebnisse

### 3. **Event-Discovery**
Für jedes gefundene Event:
- 🔍 **Event gefunden**: Titel, Datum, Zeit, Ort
- **Hash-Prüfung**: Ist das Event neu oder ein Duplikat?
- ⚠️ **Duplikate**: Werden mit Hash geloggt und übersprungen

### 4. **Event-Processing**
Für jedes neue Event:
- 🏛️ **Venue-Enrichment**: 
  - Venue-Name aus venues.csv
  - Adresse
  - Koordinaten
  - Barrierefreiheit
- 🏷️ **Kategorie-Ermittlung**: Automatisch aus Titel/Beschreibung
- 🏷️ **Tag-Extraktion**: Live-Musik, Outdoor, Familie, Kostenlos, etc.

### 5. **Event-Speicherung**
- ✅ **Event-Datei erstellt**: Dateiname und Titel
- ❌ **Fehler**: Falls beim Speichern Probleme auftreten

### 6. **Session-Zusammenfassung**
- ⏱️ Dauer des Scraping-Laufs
- 🔍 Anzahl gefundener Events (gesamt)
- ✅ Anzahl erstellter Events
- ⚠️ Anzahl übersprungener Duplikate
- 🏛️ Liste fehlender Venues (falls vorhanden)

## Verwendung

### Logs prüfen
```bash
# Neuestes Log ansehen
cat _events/_logs/$(ls -t _events/_logs/*.log | head -1)

# Alle Logs auflisten
ls -lh _events/_logs/

# Nach Fehlern suchen
grep ERROR _events/_logs/*.log

# Duplikate finden
grep "Duplikat" _events/_logs/*.log
```

### Logs bereinigen
```bash
# Alte Logs löschen (älter als 30 Tage)
find _events/_logs -name "*.log" -mtime +30 -delete

# Alle Logs löschen
rm -f _events/_logs/*.log
```

## Git-Verhalten

Logfiles werden **nicht in Git committet** (.gitignore), bleiben aber lokal für Debugging verfügbar.

## Automatisierung

Bei automatisierten Scraping-Läufen (z.B. GitHub Actions) werden die Logs:
- Während des Runs erstellt
- Im Workflow-Output angezeigt
- Nach Workflow-Ende verworfen (da nicht committet)

## Beispiel-Log

```log
[18:01:01] [INFO] ================================================================================
[18:01:01] [INFO] SCRAPING SESSION GESTARTET: 2025-11-19 18:01:01
[18:01:01] [INFO] ================================================================================
[18:01:01] [INFO] 
[18:01:01] [INFO] 📍 Venue Manager geladen: 5 Venues
[18:01:01] [INFO] 🔍 Starte Event-Scraping für Hof an der Saale...
[18:01:01] [INFO] 📅 Datum: 2025-11-19 18:01:01
[18:01:01] [INFO] 
[18:01:01] [INFO] --------------------------------------------------------------------------------
[18:01:01] [INFO] 📡 QUELLE: Stadt Hof
[18:01:01] [INFO] 🔗 URL: https://www.hof.de/events
[18:01:01] [INFO] --------------------------------------------------------------------------------
[18:01:01] [INFO] 📄 HTML geparst: 12 Event-Elemente gefunden
[18:01:01] [INFO] 🔍 Event gefunden: 'Weihnachtsmarkt 2025'
[18:01:01] [INFO]    📅 Datum: 2025-12-15 | ⏰ Zeit: 14:00
[18:01:01] [INFO]    📍 Ort: Altstadt Hof
[18:01:01] [INFO] 🏛️  Venue gefunden für 'Altstadt Hof':
[18:01:01] [INFO]    ✓ Kanonischer Name: Altstadt Hof
[18:01:01] [INFO]    ✓ Adresse: Altstadt, 95028 Hof
[18:01:01] [INFO]    ✓ Koordinaten: 50.3200, 11.9180
[18:01:01] [INFO] 🏷️  Kategorie ermittelt: 'Kultur' (aus Titel: 'Weihnachtsmarkt 2025')
[18:01:01] [INFO] ✅ Event-Datei erstellt: 2025-12-15-weihnachtsmarkt-2025.md
[18:01:01] [INFO]    📝 Titel: 'Weihnachtsmarkt 2025'
```

## Support

Bei Fragen zum Logging-System siehe `docs/SCRAPING.md` oder `scripts/scrape_events.py`.
