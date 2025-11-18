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
- **🤖 Automatisches Scraping**: Sammelt Events von lokalen Websites
- **🎨 Minimalistisch**: Skeleton CSS, Mobile-First, Touch-optimiert
- **🖨️ Druckfreundlich**: Optimierte Print-Styles

## 🚀 Quick Start

### Für Benutzer

➡️ **Website öffnen**: [feileberlin.github.io/event-kalender-hof](https://feileberlin.github.io/event-kalender-hof/)

**Funktionen:**
- Suchmaske für Freitextsuche
- Filter nach Kategorie, Zeitraum, Umkreis
- "Mein Standort" für GPS-basierte Suche
- Klick auf Marker für Event-Details

### Für Admins

➡️ **Admin-Interface**: [admin.html](https://feileberlin.github.io/event-kalender-hof/admin.html)

**Aufgaben:**
- Entwürfe prüfen und publizieren
- Events manuell erstellen
- Scraping-Quellen verwalten

📖 **Vollständige Anleitung**: [docs/ADMIN.md](docs/ADMIN.md)

### Für Entwickler

```bash
# Repository klonen
git clone https://github.com/feileberlin/event-kalender-hof.git
cd event-kalender-hof

# Dependencies installieren
bundle install
pip install -r requirements.txt

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
| **[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)** | Entwickler | Tests, Code-Style, Pull Requests |
| **[docs/PROJECT.md](docs/PROJECT.md)** | Entwickler | Technische Architektur, API-Referenz |
| **[docs/CHANGELOG.md](docs/CHANGELOG.md)** | Alle | Versionshistorie |

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

**Geplant:**
- RSS-Feed für Events
- iCal/Calendar-Export
- PWA-Support
- Dark Mode

Vollständige Roadmap: [docs/PROJECT.md](docs/PROJECT.md#roadmap)

---

**Entwickelt mit ❤️ für Hof an der Saale**
