# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).

## 📅 Entwicklungs-Timeline

**🎬 Projektstart:** 17. November 2025, 21:46 Uhr (Initial Commit: `583f2cf`)

### Meilensteine

| Datum | Version | Milestone | Entwicklungszeit |
|-------|---------|-----------|------------------|
| **17.11.2025** | **v0.1.0** | 🚀 **Pre-Release** | 0 Tage (Projektstart) |
| **17.11.2025** | **v1.0.0** | 🎉 **First Release** | < 1 Tag |
| **18.11.2025** | **v1.1.0** | 🎨 **Design-Refactoring** | +1 Tag |
| **18.11.2025** | **v1.2.0** | 🖼️ **AI-Flyer-Analyse** | +1 Tag |
| **19.11.2025** | **v1.3.0** | 🏛️ **Venue-Management** | +2 Tage |
| **19.11.2025** | **v1.4.0** | ✅ **Datums-Validierung** | +2 Tage |
| **19.11.2025** | **v1.5.0** | 🔄 **Recurring Events** | +2 Tage |
| **19.11.2025** | **v1.6.0** | ⚡ **Auto-Scraping** | +2 Tage |
| **19.11.2025** | **v1.7.0** | 📌 **Bookmark-System** | +2 Tage |
| **19.11.2025** | **v1.8.0** | ⚙️ **Automation & Config** | +2 Tage |

### Entwicklungsgeschwindigkeit

- **Pre-Release → First Release**: < 1 Tag
- **First Release → Heute (v1.8.0)**: 2 Tage
- **Durchschnitt**: 3-4 Major Features pro Tag
- **Total Features**: 25+ Major Features in 3 Tagen

## [Unreleased]

### Geplant
- 📤 **ICS Export**
  - iCalendar-Format mit RRULE
  - Import in Google Calendar, Outlook
- 📱 **PWA-Support**
  - Service Worker
  - Offline-Modus
- 🌙 **Dark Mode**
- 📰 **RSS-Feed für Events**
- 🔄 **LocalStorage Migration**
  - Von Cookies zu LocalStorage (größere Kapazität)

## [1.8.0] - 2025-11-19

### ✨ Hinzugefügt
- **📍 Neue Standorte**
  - 🏰 Oberfranken-Kaserne (GPS: 50.3092, 11.9053)
  - 🎓 Hochschule Hof (GPS: 50.3295, 11.9021)
  - Zentrale Verwaltung in `_config.yml`
  - Icons in Standort-Dropdown

- **📊 Automatische Dokumentations-Regenerierung**
  - Neues Script `scripts/regenerate_docs.py` (330+ Zeilen)
  - GitHub Actions Workflow (wöchentlich + manuell)
  - Statistiken:
    * Event-Counts (Gesamt, Veröffentlicht, Entwürfe, Archiviert, Recurring)
    * Datenquellen (Sources, Venues, Locations)
    * Code-Metriken (Python, JS, CSS, HTML, Markdown)
    * Git-Informationen (Commits, Letzter Commit)
  - Automatische Updates:
    * `docs/PROJECT.md` (Statistik-Sektion)
    * `README.md` (Event-Count-Badge)
  - Intelligente Sektion-Erkennung via Regex

- **⚙️ Zentrale Konfiguration in _config.yml**
  - `automation` Sektion mit Cron-Schedules:
    * `scraping.schedule`: "0 6,18 * * *" (täglich 6:00 + 18:00 UTC)
    * `archiving.schedule`: "0 3 * * *" (täglich 3:00 UTC)
    * `date_validation.schedule`: "0 4 * * *" (täglich 4:00 UTC)
    * `documentation.schedule`: "0 5 * * 0" (wöchentlich Sonntag 5:00 UTC)
    * `sources_watcher.enabled + debounce_seconds`
  - `archiving` Konfiguration:
    * `days_threshold`: 30 (Event-Alter für Archivierung)
    * `target_directory`: "_events/_history" (monatliche Unterordner YYYYMM)
  - `scraping` Konfiguration:
    * `max_retries`: 3
    * `timeout_seconds`: 30
    * `user_agent`: Custom User-Agent String
  - `locations` Sektion (4 Standorte mit GPS-Koordinaten)

- **📄 Neue Dokumentation**
  - `docs/AUTOMATION.md`: Umfangreiche Dokumentation (300+ Zeilen)
    * Konfigurationsoptionen erklärt
    * Cron-Format mit Beispielen
    * Workflow-Details
    * Standorte hinzufügen (3-Schritt-Anleitung)
    * Best Practices
    * Troubleshooting

### 🔧 Geändert
- **GitHub Actions Workflows aktualisiert**
  - `scrape-events.yml`: Name + Config-Referenz-Kommentare
  - `archive-old-events.yml`: Schedule geändert (täglich statt wöchentlich), Config-Referenzen
  - Alle Workflows dokumentieren jetzt Schedule-Quelle in `_config.yml`

### 📚 Dokumentation
- Workflow-Kommentare verweisen auf zentrale Konfiguration
- AUTOMATION.md mit vollständiger Konfigurations-Referenz
- Beispiele für Intervall-Anpassungen
- UTC-Zeitzone-Hinweise

### 🛠️ Technische Details
- Python-Script mit umfangreichen Statistik-Funktionen
- Regex-Pattern-Matching für intelligente Dokumentations-Updates
- Conditional Commit in Workflows (nur bei Änderungen)
- workflow_dispatch mit reason-Input für manuelle Auslösung

## [1.7.0] - 2025-11-19

### ✨ Hinzugefügt
- **📌 Bookmark-System** (Cookie-basiert, DSGVO-konform)
  - Event-Markierung in Kartenübersicht und Popup-Detailansicht
  - Visuelle Hervorhebung: ⭐-Symbol + grüner Rahmen
  - Toolbar am Bildrand (nur sichtbar wenn Bookmarks vorhanden)
  - 🖨️ **Druck-Funktion**: Formatierte PDF-druckbare Liste
  - 📧 **E-Mail-Funktion**: Vorausgefüllte E-Mail mit Event-Liste
  - 🗑️ **Löschen-Funktion**: Alle Bookmarks auf einmal entfernen
  - Automatische Validierung (nur veröffentlichte + zukünftige Events)
  - Cookie-Speicherung (365 Tage, nur URLs gespeichert)
  - Responsive Design (Desktop: rechts, Mobile: unten rechts)
- **🎛️ Admin-UI Erweiterung**
  - Neuer Tab "➕ Neues Event" mit vollständigem Formular
  - `by_set_pos` Dropdown (Erster/Zweiter/.../Letzter Wochentag)
  - `additions` Editor mit visueller Datumsliste (Pills)
  - `exceptions` Editor mit Remove-Funktion
  - Wochentags-Checkboxen (mehrere gleichzeitig wählbar)
  - 👁️ **Vorschau-Generator**: Zeigt nächste 10 Termine mit Farbcodierung
  - 📄 **Markdown-Generator**: Erstellt kompletten YAML-Frontmatter
  - Event-Listen zeigen Recurring-Info inline (z.B. "🔄 Jeden Zweiten Dienstag")
  - Live-Vorschau in Event-Cards (nächste 10 Termine)

### 📚 Dokumentation
- **BOOKMARKS.md**: Vollständige Bookmark-System Dokumentation
  - Cookie-Struktur und Speicherlogik
  - Export-Funktionen (Druck/Mail) mit Beispielen
  - CSS-Klassen und JavaScript-API-Referenz
  - Browser-Kompatibilität Matrix
  - Datenschutz-Hinweise (DSGVO-konform, kein Cookie-Banner nötig)
  - Testing-Anleitung und bekannte Limitierungen

### 🐛 Bugfixes
- Event-Card `onClick` propagiert nicht mehr bei Button/Link-Clicks
- Popup-Bookmark-Button aktualisiert sich synchron mit Card-Button
- Mobile Toolbar positioniert sich korrekt über Footer

### 🎨 UI/UX
- Bookmark-Toolbar mit Hover-Effekten und Icons
- Pulse-Animation bei Bookmark-Hinzufügung
- Responsive Toolbar-Layout für Mobile (horizontal statt vertikal)
- Event-Cards mit Bookmark-Highlight (grüner Glow-Effekt)

## [1.6.0] - 2025-11-19

### Hinzugefügt
- ⚡ **Auto-Scraping bei sources.csv Änderungen**
  - File Watcher (watchdog) überwacht _data/sources.csv
  - Automatisches Scraping bei Speichern der Datei
  - Debounce-Mechanismus (max. 1x alle 2 Sekunden)
  - Hash-Vergleich (nur echte Änderungen triggern Scraping)
  - Live-Feedback im Terminal mit Scraping-Zusammenfassung
  - Bash-Script: `./scripts/scrape.sh`
  - Manuelles Triggern: `./scripts/scrape.sh --trigger`
  - Demo-Script: `./scripts/demo_sources_watcher.sh`
- 🔄 **Recurring Events - Erweiterte Logik**
  - `by_set_pos`: Position im Monat (1=erster, 2=zweiter, -1=letzter)
  - `additions`: Liste außerordentlicher Zusatztermine
  - Mehrere Wochentage kombinierbar in `by_day` (z.B. ["WE", "SA"])
  - Komplexe Kombinationen: Base Pattern + Exceptions + Additions
  - Allgemeingültige Logik deckt praktisch alle Use Cases ab
- 📝 **Scraping-Log Recurring Detection**
  - Automatische Erkennung von "jeden Mittwoch", "wöchentlich", etc.
  - Logging der erkannten Patterns mit Konfidenz
  - Integration in scrape_events.py und date_enhancer.py

### Dokumentation
- 📖 **SOURCES_WATCHER.md**: Auto-Scraping Vollständige Dokumentation
- 📖 **SOURCES_WATCHER_QUICKREF.md**: Quick Reference
- 📖 **RECURRING_EVENTS_ADVANCED.md**: Erweiterte Logik-Dokumentation
- 📖 **RECURRING_EVENTS.md**: 9 Beispiele inkl. by_set_pos und additions

### Beispiel-Events
- ✅ **Hofer Wochenmarkt**: Jeden Mi + Sa (mehrere Wochentage)
- ✅ **Stammtisch Kulturfreunde**: Jeden 2. Dienstag (by_set_pos=2) mit additions
- ✅ **Museumsabend**: Jeden 1. Freitag (by_set_pos=1)

## [1.5.0] - 2025-11-19

### Hinzugefügt
- 🔄 **Wiederkehrende Events (Recurring Events)**
  - Vollständiges Schema für wiederkehrende Events
  - Frequencies: daily, weekly, biweekly, monthly, yearly
  - Wochentage: MO, TU, WE, TH, FR, SA, SU
  - Interval-Support (z.B. alle 2 Wochen)
  - Ausnahmen (exceptions) für Feiertage
  - Start/End-Date Konfiguration
  - Alternative: RRULE-Format (iCalendar Standard)
- 🛠️ **recurring_validator.py**
  - Validiert recurring-Konfigurationen
  - Generiert Event-Instanzen (nächste X Tage)
  - Erkennt automatisch wiederkehrende Patterns
  - Report mit Beispiel-Instanzen
- 📖 **RECURRING_EVENTS.md**
  - Schema-Referenz mit 5 Beispielen
  - JavaScript-Integration (Code-Beispiele)
  - Jekyll/Liquid-Filter
  - Admin-UI Erweiterung (HTML-Beispiele)

### Beispiel-Events
- ✅ **Butler's Karaoke**: Jeden Mittwoch ab 20 Uhr (korrigiert von Sonntag)

## [1.4.0] - 2025-11-19

### Hinzugefügt
- ✅ **Datums-Validierung & Qualitätssicherung**
  - validate_event_dates.py: Prüft Events auf Datumsfehler
  - Erkennt Veröffentlichungsdatum vs. Event-Datum Problem
  - Prüft Events in der Vergangenheit
  - Warnt bei verdächtigen Datumsangaben ("heute", "ab heute")
  - date_enhancer.py: Intelligente Datumserkennung mit Kontext-Analyse
  - Recurring Pattern Detection ("jeden Mittwoch", "wöchentlich")
  - Konfidenz-Bewertung für extrahierte Daten
- 📝 **Detaillierte Scraping-Logs**
  - Timestamp-basierte Log-Dateien in _events/_logs/
  - Strukturiertes Logging aller Scraping-Entscheidungen
  - Venue-Enrichment-Logging
  - Kategorie-Guessing-Logging
  - Tag-Extraktion-Logging
  - Fehler-Logging mit Kontext
  - Session-Zusammenfassung mit Statistiken

### Dokumentation
- 📖 **DATE_VALIDATION.md**: Datums-Validierung Dokumentation
- 📖 **ARCHIVING.md**: Auto-Archivierung vergangener Events
- 📖 README.md erweitert um Datums-Validierung

### Behoben
- 🐛 **12 Events in Vergangenheit**: Veröffentlichungsdatum statt Event-Datum verwendet

## [1.3.0] - 2025-11-19

### Hinzugefügt
- 🏛️ **Venue-Management-System**
  - venues.csv mit strukturierten Venue-Daten
  - Barrierefreiheit-Tracking (wheelchair, hearing_loop, braille)
  - Kapazitäts-Informationen
  - Kontaktdaten (Telefon, E-Mail, Website)
  - Öffnungszeiten
  - Metadaten (Betreiber, Typ, Baujahr)
  - venue_manager.py: Automatisches Venue-Matching und Enrichment
  - venue_admin.py: Interaktives CLI-Tool zur Venue-Verwaltung
  - venue_examples.py: Code-Beispiele für Entwickler
- 📖 **VENUES.md**: Vollständige Venue-Management-Dokumentation
- 📖 **VENUES_QUICKREF.md**: Quick Reference für Admins

### Geändert
- 🗺️ Events werden jetzt mit Venue-Daten angereichert
- 📍 Automatisches Geocoding über venue_manager

## [1.2.0] - 2025-11-18

### Hinzugefügt
- 🖼️ **AI-Flyer-Analyse**: Automatische Event-Extraktion aus Bildern/PDFs
  - GitHub Models API (GPT-4o-mini, kostenlos für GitHub-User)
  - DuckDuckGo AI Chat als Fallback (kostenlos, kein API-Key)
  - Lokales OCR (Tesseract) als letzte Option
  - Automatisches Geocoding (OpenStreetMap Nominatim)
  - Erstellt Events mit `status: "Entwurf"` für manuelle Prüfung
  - Script: `python scripts/analyze_flyer.py <URL>`

### Dokumentation
- 📖 **ADMIN.md**: Sektion "Flyer-Analyse" mit Workflow und Beispielen
- 📖 **QUICKSTART.md**: AI-Flyer-Analyse in Erste Schritte integriert
- 📖 **README.md**: Feature-Liste um AI-Analyse erweitert

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
- ✅ **Test Suite**: Automatische Validierung HTML ↔ JS Konsistenz (tests/test_filters.js)
- ✅ **CI/CD Tests**: GitHub Actions Workflow für Filter-Tests
- ✅ **UX Verbesserung**: Umkreis-Filter mit Fortbewegungsarten (Fuß, Rad, ÖPNV, Taxi)
- ✅ **KISS Prinzip**: Nur noch ein Layout (popart.html), default.html entfernt
- ✅ **Dokumentations-Workflow**: Automatische Prüfung auf veraltete Docs (täglich 3:00 UTC)

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
