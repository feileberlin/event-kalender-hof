# 📜 Scripts

Alle Automatisierungs- und Verwaltungs-Scripts für den Event-Kalender.

## 🚀 Schnellstart-Scripts

### Development
```bash
./scripts/dev.sh              # Startet Jekyll Development Server
```

### Setup
```bash
./scripts/setup.sh            # Installiert alle Dependencies
```

### Scraping
```bash
./scripts/scrape.sh           # Scrapt alle Quellen aus sources.csv
```

## 🐍 Python-Scripts

### Event-Management
- **`scrape_events.py`** - Event-Scraping von konfigurierten Quellen
- **`archive_old_events.py`** - Archiviert vergangene Events
- **`validate_event_dates.py`** - Validiert Event-Datumsangaben

### Flyer-Analyse
- **`analyze_flyer.py`** - Extrahiert Events aus Bildern/PDFs (AI)

### Venue-Management
- **`venue_manager.py`** - Programmatisches Venue-API
- **`venue_admin.py`** - CLI für Venue-Verwaltung

### Utilities
- **`date_enhancer.py`** - Erweitert Event-Daten um Datumsfelder
- **`recurring_validator.py`** - Validiert Recurring-Events-Syntax
- **`regenerate_docs.py`** - Aktualisiert Projekt-Dokumentation
- **`check_broken_links.py`** - Prüft auf defekte Links

## 📋 Verwendung

### Scraping manuell starten
```bash
./scripts/scrape.sh
# Oder direkt:
python scripts/scrape_events.py
```

### Events archivieren
```bash
# Standard: 30 Tage
python scripts/archive_old_events.py

# Custom: 60 Tage
python scripts/archive_old_events.py --days 60

# Dry-Run (ohne Änderungen)
python scripts/archive_old_events.py --dry-run
```

### Flyer analysieren
```bash
python scripts/analyze_flyer.py https://example.com/flyer.pdf
```

### Venue hinzufügen
```bash
python scripts/venue_admin.py add "Kulturzentrum" \
  --address "Hauptstraße 1, 95028 Hof" \
  --website "https://example.com" \
  --wheelchair-accessible
```

### Dokumentation regenerieren
```bash
python scripts/regenerate_docs.py
```

## 🔧 Dependencies

**Ruby:**
```bash
bundle install
```

**Python:**
```bash
pip install -r requirements.txt
```

## 📚 Siehe auch

- [AUTOMATION.md](../docs/AUTOMATION.md) - Automatisierungs-Konfiguration
- [ADMIN.md](../docs/ADMIN.md) - Admin-Workflows
- [VENUES.md](../docs/VENUES.md) - Venue-Management
