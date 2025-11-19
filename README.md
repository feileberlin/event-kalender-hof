# 🎉 Event-Kalender Hof an der Saale

**hof.ist/jetzt** - Events bis Sonnenaufgang in Hof an der Saale

Ein Jekyll-basierter Event-Kalender für GitHub Pages, der automatisch Events aus verschiedenen Quellen sammelt und auf einer interaktiven Karte darstellt.

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://feileberlin.github.io/event-kalender-hof/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Features

- **📍 Interaktive Karte** mit Leaflet.js, zentriert auf Hof an der Saale
- **🕐 Zeitfilter "Bis Sonnenaufgang"**: Zeigt nur Events bis zur Morgendämmerung (6:30 Uhr)
- **🔍 Intelligente Filter**: Textsuche, Kategorie, Zeitraum, Umkreis (Fuß, Rad, ÖPNV, Taxi)
- **📱 Geolocation**: GPS-basierte Umkreissuche
- **📌 Bookmark-System**: Events merken, drucken oder per E-Mail versenden (Cookie-basiert, DSGVO-konform)
- **🤖 Automatisches Scraping**: Sammelt Events von lokalen Websites
- **⚡ Auto-Scraping**: Startet automatisch bei Änderungen an `sources.csv`
- **📝 Scraping-Logs**: Detaillierte Protokolle aller Scraping-Durchläufe mit Recurring-Detection
- **✅ Datums-Validierung**: Erkennt fehlerhafte Event-Daten (Veröffentlichungsdatum vs. Event-Datum)
- **🔄 Wiederkehrende Events**: Erweiterte Logik mit `by_set_pos`, `additions`, mehrere Wochentage
- **🎛️ Admin-UI**: Vollständiges Interface mit Event-Erstellung, Recurring-Vorschau, Markdown-Generator
- **🖼️ AI-Flyer-Analyse**: Extrahiert Events aus Bildern/PDFs (GitHub Models / DuckDuckGo AI)
- **🎨 Minimalistisch**: Skeleton CSS, Mobile-First, Touch-optimiert
- **🖨️ Druckfreundlich**: Optimierte Print-Styles
- **🏛️ Venue-Management**: Verwaltet Veranstaltungsorte mit Barrierefreiheit & Metadaten
- **📦 Auto-Archivierung**: Events älter als 30 Tage werden automatisch archiviert

## 🚀 Quick Start

### Für Benutzer

➡️ **Website öffnen**: [feileberlin.github.io/event-kalender-hof](https://feileberlin.github.io/event-kalender-hof/)

**Funktionen:**
- Suchmaske für Freitextsuche
- Filter nach Kategorie, Zeitraum, Umkreis
- "Mein Standort" für GPS-basierte Suche
- Klick auf Marker für Event-Details
- 📌 **Bookmark-System**: Events merken, drucken (PDF), per E-Mail versenden

### Für Admins

➡️ **Admin-Interface**: [admin/](https://feileberlin.github.io/event-kalender-hof/admin/)

**Aufgaben:**
- Entwürfe prüfen und publizieren
- Events manuell erstellen (mit Recurring-Support & Vorschau)
- Scraping-Quellen verwalten
- Veranstaltungsorte pflegen (Barrierefreiheit, Kontakt, etc.)
- Markdown-Generator für komplexe Event-Konfigurationen

📖 **Vollständige Anleitung**: [docs/ADMIN.md](docs/ADMIN.md)
📍 **Venue-Management**: [docs/VENUES.md](docs/VENUES.md)

### Für Entwickler

```bash
# Repository klonen
git clone https://github.com/feileberlin/event-kalender-hof.git
cd event-kalender-hof

# Dependencies installieren
bundle install
pip install -r requirements.txt

# Scraping starten
python scripts/scrape_events.py

# ⚡ NEU: Auto-Scraping bei sources.csv Änderungen
./scripts/scrape.sh              # Startet Watcher
./scripts/scrape.sh --trigger    # Einmaliges Scraping
./scripts/demo_sources_watcher.sh  # Interaktive Demo

# Datums-Validierung ausführen
python scripts/validate_event_dates.py

# Venue-Verwaltung
python scripts/venue_admin.py      # Interaktives CLI-Tool
python scripts/venue_examples.py   # Beispiel-Code

# Server starten
bundle exec jekyll serve --livereload
```

➡️ Öffne: http://localhost:4000

📖 **Entwickler-Guide**: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

## 🛠️ Tech Stack

| Komponente | Technologie |
|------------|-------------|
| **Frontend** | Jekyll 4.3, Skeleton CSS 2.0.4, Leaflet.js 1.9.4 |
| **JavaScript** | Vanilla ES6+ (keine jQuery) |
| **Scraping** | Python 3.11+, BeautifulSoup4, PyYAML |
| **CI/CD** | GitHub Actions, GitHub Pages |
| **Tests** | Node.js, Custom Test Suite |

## 📚 Dokumentation

| Datei | Zielgruppe | Inhalt |
|-------|------------|--------|
| **[docs/QUICKSTART.md](docs/QUICKSTART.md)** | Alle | Schnelleinstieg in 5 Minuten |
| **[docs/ADMIN.md](docs/ADMIN.md)** | Admins | Event-Verwaltung, Scraping-Konfiguration |
| **[docs/BOOKMARKS.md](docs/BOOKMARKS.md)** | Alle/Devs | Bookmark-System: Merken, Drucken, Mailen |
| **[docs/VENUES.md](docs/VENUES.md)** | Admins | Venue-Management, Barrierefreiheit |
| **[docs/ARCHIVING.md](docs/ARCHIVING.md)** | Admins | Auto-Archivierung vergangener Events |
| **[docs/DATE_VALIDATION.md](docs/DATE_VALIDATION.md)** | Admins/Devs | Datums-Validierung, Qualitätssicherung |
| **[docs/SOURCES_WATCHER.md](docs/SOURCES_WATCHER.md)** | Admins/Devs | Auto-Scraping bei sources.csv Änderungen |
| **[docs/RECURRING_EVENTS.md](docs/RECURRING_EVENTS.md)** | Admins/Devs | Wiederkehrende Events (Basis) |
| **[docs/RECURRING_EVENTS_ADVANCED.md](docs/RECURRING_EVENTS_ADVANCED.md)** | Devs | Erweiterte Recurring-Logik (by_set_pos, additions) |
| **[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)** | Entwickler | Tests, Code-Style, Pull Requests |
| **[docs/PROJECT.md](docs/PROJECT.md)** | Entwickler | Technische Architektur, API-Referenz, Timeline |
| **[docs/CHANGELOG.md](docs/CHANGELOG.md)** | Alle | Versionshistorie (v0.1.0 → v1.7.0) |
| **[docs/ANALYTICS.md](docs/ANALYTICS.md)** | Admins | GoatCounter Analytics-Integration |

### 📖 Quick References

| Datei | Inhalt |
|-------|--------|
| **[docs/BOOKMARKS_QUICKREF.md](docs/BOOKMARKS_QUICKREF.md)** | Bookmark-System API & Testing |
| **[docs/SOURCES_WATCHER_QUICKREF.md](docs/SOURCES_WATCHER_QUICKREF.md)** | Auto-Scraping Commands |
| **[docs/VENUES_QUICKREF.md](docs/VENUES_QUICKREF.md)** | Venue-CLI Befehle |
| **[docs/STATUS_QUICKREF.md](docs/STATUS_QUICKREF.md)** | Event-Status Workflow |

## 📝 Event erstellen

Neue Datei: `_events/2025-11-20-mein-event.md`

```yaml
---
title: "Konzert in der Freiheitshalle"
date: 2025-11-20
start_time: "20:00"
location: "Freiheitshalle Hof"
coordinates:
  lat: 50.3197
  lng: 11.9168
category: "Musik"
status: "Öffentlich"
---
```

Details: [docs/ADMIN.md](docs/ADMIN.md#manuelles-event-erstellen)

## 🧪 Testing

```bash
cd tests
node test_filters.js
```

Die Test Suite validiert HTML ↔ JavaScript Konsistenz automatisch.

Details: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md#testing)

## 🤝 Beitragen

1. Fork das Repository
2. Erstelle Feature-Branch: `git checkout -b feature/AmazingFeature`
3. Committe Änderungen: `git commit -m 'Add AmazingFeature'`
4. Push zum Branch: `git push origin feature/AmazingFeature`
5. Öffne Pull Request

Details: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

## 📄 Lizenz

MIT License - siehe [LICENSE](LICENSE)

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/feileberlin/event-kalender-hof/issues)
- **Diskussionen**: [GitHub Discussions](https://github.com/feileberlin/event-kalender-hof/discussions)

## 🎯 Roadmap

**v1.8.0 (geplant):**
- LocalStorage statt Cookies (größere Kapazität)
- Bookmark-Kategorien/Tags
- iCal/Calendar-Export (.ics)

**v1.9.0 (geplant):**
- RSS-Feed für Events
- PWA-Support (Service Worker, Offline-Modus)
- Sync mit Google Calendar / Outlook

**v2.0.0 (geplant):**
- Dark Mode
- Account-System (optional, für Sync)
- Bookmark-Statistiken & Empfehlungen

Vollständige Roadmap: [docs/PROJECT.md](docs/PROJECT.md#roadmap)

---

**Entwickelt mit ❤️ für Hof an der Saale**
