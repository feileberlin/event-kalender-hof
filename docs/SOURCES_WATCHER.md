# Sources CSV Watcher & Auto-Scraper

Automatisches Scraping-System, das bei Änderungen an `_data/sources.csv` sofort ein Event-Scraping startet.

## 🎯 Zweck

Nach dem Bearbeiten der `sources.csv` (Quellen hinzufügen/entfernen/aktivieren) wird automatisch:
1. Die Änderung erkannt
2. Die aktualisierten Quellen geladen
3. Ein kompletter Scraping-Durchlauf gestartet
4. Eine Zusammenfassung angezeigt

## 🚀 Verwendung

### Option 1: Watcher-Modus (empfohlen)

Startet einen Hintergrund-Prozess, der `sources.csv` überwacht:

```bash
# Bash-Script (prüft Abhängigkeiten automatisch)
./scripts/scrape.sh

# Oder direkt Python
python3 scripts/sources_watcher.py --watch
```

**Output:**
```
================================================================================
🔍 SOURCES.CSV WATCHER
================================================================================
Überwache: _data/sources.csv
Scraper:   scripts/editorial/scrape_events.py
Logs:      _events/_logs
================================================================================

💡 Bearbeite sources.csv um automatisch Scraping zu starten
🛑 Drücke Ctrl+C zum Beenden
```

Sobald du `sources.csv` speicherst:
```
[18:45:12] [INFO] 📝 sources.csv wurde geändert!
[18:45:12] [INFO] 📊 Aktive Quellen: 6
[18:45:12] [INFO]    1. Stadt Hof (html)
[18:45:12] [INFO]    2. Freiheitshalle Hof (html)
[18:45:12] [INFO]    3. Galeriehaus Hof (facebook)
[18:45:12] [INFO] 🚀 Starte Scraping mit aktualisierten Quellen...
[18:45:15] [SUCCESS] ✅ Scraping erfolgreich abgeschlossen!
[18:45:15] [INFO] 📄 Log-Datei: 20251119-184512-scraping.log

================================================================================
SCRAPING-ZUSAMMENFASSUNG
================================================================================
📊 ZUSAMMENFASSUNG
   ✓ Quellen gescannt: 2
   ✓ Events gefunden: 5
   ✓ Neue Events: 3
   ✓ Duplikate: 2
   ✓ Fehler: 0
================================================================================
```

### Option 2: Manuelles Triggern

Einmaliges Scraping ohne Watcher:

```bash
./scripts/scrape.sh --trigger

# Oder
python3 scripts/sources_watcher.py --trigger
```

### Option 3: Klassisches Scraping (ohne Watcher)

```bash
python3 scripts/editorial/scrape_events.py
```

## 📋 Voraussetzungen

### Python-Paket: watchdog

```bash
# Installation
pip install watchdog

# Oder aus requirements.txt
pip install -r requirements.txt
```

Das Bash-Script `scripts/scrape.sh` prüft automatisch ob `watchdog` installiert ist und bietet Installation an.

## 🔧 Funktionsweise

### 1. File Watcher (Watchdog)
```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SourcesChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('sources.csv'):
            # Hash prüfen (nur echte Änderungen)
            # Debounce (max. 1x alle 2 Sekunden)
            # Scraping triggern
```

### 2. Änderungs-Erkennung
- **Hash-Vergleich**: MD5-Hash von `sources.csv` wird verglichen
- **Debounce**: Mehrfache Saves innerhalb 2 Sekunden = 1x Scraping
- **Nur echte Änderungen**: Speichern ohne Änderung triggert nichts

### 3. Auto-Scraping
```python
subprocess.run([sys.executable, "scripts/editorial/scrape_events.py"])
```

- Führt `scrape_events.py` aus
- Timeout: 5 Minuten
- Zeigt Zusammenfassung aus Log-Datei

## 📁 Dateien

```
scripts/
  sources_watcher.py    # Python Watcher & Auto-Scraper
  scrape_events.py      # Haupt-Scraping-Script

scripts/scrape.sh        # Bash Convenience-Script

_data/
  sources.csv           # Event-Quellen (überwacht)

_events/
  _logs/
    YYYYMMDD-HHMMSS-scraping.log  # Scraping-Logs
```

## 🎛️ Konfiguration

### Debounce-Zeit anpassen

In `sources_watcher.py`:
```python
self.debounce_seconds = 2  # Standard: 2 Sekunden
```

### Timeout anpassen

In `sources_watcher.py`:
```python
result = subprocess.run(
    ...,
    timeout=300  # Standard: 5 Minuten
)
```

## 🧪 Beispiel-Workflow

### 1. Watcher starten
```bash
./scripts/scrape.sh
```

### 2. Sources bearbeiten
Öffne `_data/sources.csv`:
```csv
name,url,type,active,notes
Stadt Hof,https://www.hof.de/...,html,true,Offizielle Seite
Neue Quelle,https://example.com,html,true,Neue Event-Quelle  # ← NEU
```

### 3. Speichern → Automatisches Scraping
```
[18:50:00] [INFO] 📝 sources.csv wurde geändert!
[18:50:00] [INFO] 📊 Aktive Quellen: 7
[18:50:00] [INFO]    7. Neue Quelle (html)
[18:50:00] [INFO] 🚀 Starte Scraping mit aktualisierten Quellen...
```

### 4. Ergebnis prüfen
```bash
# Neueste Log-Datei
ls -t _events/_logs/*-scraping.log | head -1

# Neue Events
ls -t _events/*.md | head -5
```

## 🔍 Troubleshooting

### "watchdog nicht installiert"
```bash
pip install watchdog
```

### "Scraping-Timeout"
- Scraper läuft länger als 5 Minuten
- Erhöhe `timeout` in `sources_watcher.py`
- Oder prüfe warum Scraper hängt

### "Keine Änderung erkannt"
- Hash ist identisch (keine echte Änderung)
- Debounce aktiv (zu schnell gespeichert)
- Datei nicht in `_data/` (Watcher überwacht nur diesen Ordner)

### "Scraping schlägt fehl"
```bash
# Direkter Test ohne Watcher
python3 scripts/editorial/scrape_events.py

# Log-Datei prüfen
cat _events/_logs/$(ls -t _events/_logs/*-scraping.log | head -1)
```

## 🎯 Use Cases

### 1. Neue Event-Quelle hinzufügen
```csv
Neue Venue,https://venue.com/events,html,true,Beschreibung
```
→ Speichern → Automatisches Scraping → Events in `_events/`

### 2. Quelle temporär deaktivieren
```csv
Alte Quelle,https://...,html,false,Inaktiv
```
→ Speichern → Scraping ohne diese Quelle

### 3. Mehrere Quellen gleichzeitig ändern
- Alle Änderungen machen
- Einmal speichern
- Ein Scraping-Durchlauf mit allen Änderungen

## 🚀 Integration in Workflow

### VS Code Tasks (tasks.json)
```json
{
  "label": "Watch Sources & Auto-Scrape",
  "type": "shell",
  "command": "./scripts/scrape.sh",
  "isBackground": true,
  "problemMatcher": []
}
```

### Development Script
```bash
# In dev.sh
echo "Starte Sources Watcher..."
./scripts/scrape.sh &
WATCHER_PID=$!

# Jekyll starten
bundle exec jekyll serve

# Cleanup
kill $WATCHER_PID
```

## 📊 Features

✅ **Automatische Erkennung**: Speichern von `sources.csv` triggert Scraping  
✅ **Debounce**: Verhindert mehrfaches Scraping bei schnellen Edits  
✅ **Hash-Vergleich**: Nur echte Änderungen triggern Scraping  
✅ **Live-Feedback**: Zeigt Scraping-Progress in Echtzeit  
✅ **Zusammenfassung**: Log-Output direkt in Console  
✅ **Timeout-Protection**: Max. 5 Minuten pro Scraping  
✅ **Error-Handling**: Fehler werden sauber geloggt  
✅ **Manueller Modus**: Auch einmaliges Triggern möglich  

## 🔄 Nächste Schritte

1. **VS Code Extension**: Sources-Editor mit Live-Preview
2. **Web-UI**: Browser-basierter Sources-Manager
3. **Scheduled Scraping**: Cron-Job + Watcher kombinieren
4. **Multi-Source-Scraping**: Paralleles Scraping mehrerer Quellen
5. **Scraping-Queue**: Änderungen sammeln, batch-verarbeiten
