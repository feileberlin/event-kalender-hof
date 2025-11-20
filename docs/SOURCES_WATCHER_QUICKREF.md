# Sources CSV Watcher - Quick Reference

## 🚀 Schnellstart

### Watcher starten (überwacht sources.csv)
```bash
./scripts/scrape.sh
```

### Einmaliges Scraping
```bash
./scripts/scrape.sh --trigger
```

### Demo ansehen
```bash
./scripts/demo_sources_watcher.sh
```

## 📋 Was passiert?

1. **sources.csv bearbeiten** → Quelle hinzufügen/ändern/deaktivieren
2. **Speichern** → Automatische Änderungs-Erkennung
3. **Scraping startet** → Lädt neue/geänderte Quellen
4. **Events erstellt** → Neue Markdown-Dateien in `_events/`
5. **Log anzeigen** → Zusammenfassung in Console

## 🔧 Installation

```bash
# Watchdog installieren
pip install watchdog

# Oder alle Dependencies
pip install -r requirements.txt
```

## 📊 Beispiel

**Terminal 1: Watcher starten**
```bash
$ ./scripts/scrape.sh

================================================================================
🔍 SOURCES.CSV WATCHER
================================================================================
Überwache: _data/sources.csv
💡 Bearbeite die Datei um automatisch Scraping zu starten
🛑 Drücke Ctrl+C zum Beenden
```

**Terminal 2: sources.csv bearbeiten**
```csv
Neue Venue,https://venue.com/events,html,true,Neue Quelle
```

**Terminal 1: Automatisches Feedback**
```
[18:50:00] [INFO] 📝 sources.csv wurde geändert!
[18:50:00] [INFO] 📊 Aktive Quellen: 9
[18:50:00] [INFO]    9. Neue Venue (html)
[18:50:00] [INFO] 🚀 Starte Scraping mit aktualisierten Quellen...
[18:50:03] [SUCCESS] ✅ Scraping erfolgreich abgeschlossen!

================================================================================
SCRAPING-ZUSAMMENFASSUNG
================================================================================
📊 Events gefunden: 5
✅ Events erstellt: 2
⚠️  Duplikate: 3
================================================================================
```

## 📁 Dateien

- `scripts/scrape.sh` - Bash-Script (empfohlen)
- `scripts/sources_watcher.py` - Python-Implementierung
- `scripts/demo_sources_watcher.sh` - Interaktive Demo
- `docs/SOURCES_WATCHER.md` - Vollständige Dokumentation

## 🎯 Workflow

```
sources.csv editieren
        ↓
Datei speichern
        ↓
Watcher erkennt Änderung
        ↓
Hash vergleichen (echte Änderung?)
        ↓
Debounce (max. 1x/2s)
        ↓
scrape_events.py ausführen
        ↓
Events in _events/ speichern
        ↓
Log anzeigen
```

## 💡 Tipps

- **VS Code**: Öffne `sources.csv` und `scripts/scrape.sh` Terminal parallel
- **Mehrere Änderungen**: Alle Änderungen machen → 1x speichern → 1x Scraping
- **Test-Modus**: `--trigger` für einmaliges Scraping ohne Watcher
- **Logs prüfen**: `_events/_logs/` für detaillierte Scraping-Protokolle

## 🔍 Troubleshooting

```bash
# Watchdog fehlt?
pip install watchdog

# Scraping testen (ohne Watcher)
python3 scripts/editorial/scrape_events.py

# Neueste Log-Datei
cat _events/_logs/$(ls -t _events/_logs/*-scraping.log | head -1)
```
