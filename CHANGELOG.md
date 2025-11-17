# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).

## [Unreleased]

### Geplant
- RSS-Feed für Events
- iCal/Calendar-Export
- PWA-Unterstützung
- Dark Mode

## [1.0.0] - 2025-11-17

### Hinzugefügt
- 🎉 Initiales Release des Event-Kalender Hof
- 📍 Interaktive Leaflet.js Karte mit Events
- 🕐 Filter: Nur Events bis Morgendämmerung
- 🔍 Such- und Filterfunktionen (Text, Kategorie, Zeit, Radius)
- 📱 Browser-Geolocation für Umkreissuche
- 🤖 Automatisches Event-Scraping via GitHub Actions
- ✏️ Admin-Interface zur Event-Verwaltung
- 🎨 Scherenschnitt-Design im Stil Albrecht Dürers
- 📚 Umfassende Dokumentation (README, QUICKSTART, CONTRIBUTING)
- 🔧 Jekyll 4.3 mit GitHub Pages Support
- 🐍 Python-basierter Event-Scraper
- 📦 GitHub Actions Workflows (Deploy + Scraping)
- 🌐 Event-Detail-Seiten
- 🎯 Kategorien-System mit 7 Kategorien
- 🏷️ Tag-System für Events
- 📝 YAML-basierte Event-Struktur
- 🔒 Status-System (Entwurf/Öffentlich)
- 🔄 Duplikatsprüfung via Hash
- 🗺️ Standardkoordinaten: Rathaus Hof (50.3197, 11.9168)

### Dateien
- `_config.yml` - Jekyll-Konfiguration
- `_layouts/default.html` - Haupt-Layout mit Scherenschnitt
- `_layouts/event.html` - Event-Detail-Layout
- `index.html` - Hauptseite mit Karte
- `admin.html` - Admin-Interface
- `assets/js/main.js` - JavaScript-Logik
- `assets/css/style.css` - Stylesheet
- `scripts/scrape_events.py` - Event-Scraper
- `.github/workflows/jekyll.yml` - Jekyll Deploy
- `.github/workflows/scrape-events.yml` - Automatisches Scraping
- `Gemfile` - Ruby-Dependencies
- `requirements.txt` - Python-Dependencies
- `README.md` - Hauptdokumentation
- `QUICKSTART.md` - Schnellstart-Anleitung
- `CONTRIBUTING.md` - Contribution Guidelines
- `LICENSE` - MIT Lizenz
- `CODE_OF_CONDUCT.md` - Code of Conduct
- `.gitignore` - Git-Ignore-Regeln

### Technische Details
- Jekyll 4.3.4
- Leaflet.js 1.9.4
- Python 3.11+
- BeautifulSoup4
- GitHub Actions
- OpenStreetMap Tiles

---

## Format

### Arten von Änderungen
- `Hinzugefügt` für neue Features
- `Geändert` für Änderungen an bestehender Funktionalität
- `Veraltet` für bald zu entfernende Features
- `Entfernt` für entfernte Features
- `Behoben` für Bugfixes
- `Sicherheit` für Sicherheitsupdates
