# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).

## [Unreleased]

### Geplant
- RSS-Feed für Events
- iCal/Calendar-Export
- PWA-Unterstützung
- Dark Mode

## [1.1.0] - 2025-11-18

### Geändert
- 🎨 **Design-Vereinfachung**: Scherenschnitt/Dürer-Artwork komplett entfernt (240+ Zeilen SVG)
- 🎨 **CSS-Framework**: Auf Skeleton CSS 2.0.4 umgestellt (Mobile-First Grid)
- 📐 **Layout**: Alle display:flex entfernt, ausschließlich Skeleton Grid verwendet
- 🗺️ **Karte**: Rathaus-Marker jetzt immer sichtbar, auch ohne Events
- 📱 **Responsive**: Mobile-First @media queries (550px, 960px Breakpoints)
- 👆 **Touch**: 44px Mindestgröße für Buttons/Inputs auf Touch-Geräten
- 🖨️ **Print**: Optimierte Print-Styles (Karte/Filter ausgeblendet)

### Behoben
- 🐛 **Doppelter Footer**: Duplicate SVG-Footer aus Layout entfernt
- 🐛 **Pfade**: Alle Links auf relative URLs mit baseurl konvertiert
- 🐛 **Karte**: z-index-Konflikte behoben (999-1001 Stacking)
- 🐛 **Event-Anzeige**: Dawn-Time Berechnung korrigiert (6:30 Uhr)
- 🐛 **Skeleton CSS**: Container-Override entfernt (brach Grid-System)

### Hinzugefügt
- ✅ **Baseurl**: Konfiguration für GitHub Pages Subdirectory
- ✅ **Facebook-Quellen**: 3 neue Event-Quellen im Scraper
- ✅ **Popup**: Rathaus-Marker öffnet Popup wenn keine Events
- ✅ **Test-Events**: 2 Events für 18.11. Nacht zum Testen

## [1.0.0] - 2025-11-17

### Hinzugefügt
- 🎉 Initiales Release des Event-Kalender Hof
- 📍 Interaktive Leaflet.js 1.9.4 Karte mit Events
- 🕐 Filter: Nur Events bis Morgendämmerung (6:30 Uhr)
- 🔍 Such- und Filterfunktionen (Text, Kategorie, Zeit, Radius)
- 📱 Browser-Geolocation für Umkreissuche mit Fehlerbehandlung
- 🤖 Automatisches Event-Scraping via GitHub Actions
- ✏️ Admin-Interface zur Event-Verwaltung
- 📚 Umfassende Dokumentation (README, QUICKSTART, CONTRIBUTING)
- 🔧 Jekyll 4.3 mit GitHub Pages Support
- 🐍 Python 3.11+ basierter Event-Scraper
- 📦 GitHub Actions Workflows (Deploy + Scraping)
- 🌐 Event-Detail-Seiten
- 🎯 Kategorien-System mit 7 Kategorien (Musik, Theater, Sport, Kultur, Markt, Fest, Sonstiges)
- 🏷️ Tag-System für Events
- 📝 YAML-basierte Event-Struktur in _events/
- 🔒 Status-System (Entwurf/Öffentlich)
- 🔄 Duplikatsprüfung via MD5-Hash
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
