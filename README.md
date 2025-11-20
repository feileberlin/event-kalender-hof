# 🔥 Krawl

> **Live-Beispiel:** [krawl.ist/hof](https://feileberlin.github.io/krawl.ist/hof/) - Krawl für Hof an der Saale

**Krawall hier. Krawall jetzt.**

Krawl zeigt dir Events in deiner unmittelbaren Nähe - ohne Instagram-Scrollen, ohne verpasste Flyer.  
Nur eine Frage: **Was läuft heute?**

Entwickelt aus der Frustration heraus, dass gute Events oft untergehen, weil sie auf zig verschiedenen Kanälen verstreut sind.

---

## 💭 Selbstverständnis

### Was ist Krawl?

**JETZT + HIER**  
Krawl beantwortet eine einzige Frage: *"Was kann ich in den nächsten Stunden in meiner unmittelbaren Nähe erleben?"* Nicht nächste Woche, nicht irgendwo in der Stadt - sondern jetzt und hier.

**Read-Only First**  
Krawl ist bewusst **kein soziales Netzwerk**. Keine Kommentare, keine User-Profile, kein Dopamin-Hack. Du siehst Events - fertig. Community-Features (Event-Vorschläge, Reviews) kommen später (v2.0), aber die Kernfunktion bleibt fokussiert.

**Krawall + Crawl**  
Der Name kommt aus zwei Welten:
- **Krawall** (jiddisch) = Aufruhr, Party, wo was los ist
- **Crawl** (englisch) = Pub Crawl, Event-Tour

**Krawl** = deine Tour durch den Krawall deiner Community.

**Für Krawlisten, von Krawlisten**  
Wer Krawl nutzt, ist ein **Krawlist**. Krawlisten sind nicht passiv. Sie scrollen nicht Instagram, sie erleben Events. Sie sind Teil der Szene, nicht Zuschauer.

**Open Source & Forkbar**  
Jede Community kann Krawl nutzen - ob Stadt, Subkultur, Maker-Space oder Themen-Netzwerk. Keine zentrale Plattform, keine Abhängigkeit. Fork es, pass es an, betreibe es selbst.

### Was Krawl zeigt

Die **nächsten Events** in **relativer Nähe** zu deinem Kontext:
- **Stadt:** Umkreis 1-10 km
- **Subkultur:** nächstes Event deutschlandweit
- **Netzwerk:** geografisches Zentrum ±100 km

"Nähe" ist relativ - für eine Punk-Szene sind 200 km akzeptabel, für eine Stadt-Community nicht.

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://feileberlin.github.io/event-kalender-hof/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Jekyll](https://img.shields.io/badge/Jekyll-3.10-red)](https://jekyllrb.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)

---

## 🚀 Usage

1. **Öffne die Karte:** [hof.krawl.ist](https://feileberlin.github.io/event-kalender-hof/)
2. **Filter anpassen:** Zeitraum, Umkreis (🚶 1km, 🚴 3km, 🚌 10km), Kategorie
3. **Event anklicken:** Details, Beschreibung, Link zum Veranstalter
4. **Bookmark setzen:** Event merken und später als PDF exportieren

**Admin?** Siehe [INSTALL.md](INSTALL.md) für Setup-Anleitung.

---

## 🎯 Warum dieses Projekt?

**Das Problem:**
- Events sind auf 20+ Websites/Social Media verstreut
- Kulturschaffende haben keine Zeit für Marketing
- Bestehende Event-Plattformen sind zu komplex oder kommerziell
- Gute lokale Events gehen unter
- Communities (Städte, Subkulturen, Netzwerke) haben keine einfache Event-Übersicht

**Die Lösung:**
- **Automatisches Scraping** aus beliebigen Quellen
- **Deduplication-Engine** erkennt Duplikate über Plattformen hinweg
- **Veranstalter-CRM** für Networking und Recherche
- **Zero-Config**: Läuft auf GitHub Pages, keine Server nötig
- **Open Source**: Jede Community kann es nutzen (Städte, Subkulturen, Netzwerke)

---

## ✨ Features (die wirklich was bringen)

### 🗺️ Für Besucher
- **Interaktive Karte** mit Leaflet.js - touch-optimiert
- **Intelligente Filter**: Zeitraum, Umkreis (🚶 1km, 🚴 3km, 🚌 10km), Kategorie
- **"Bis Sonnenaufgang"-Filter**: Zeigt nur Events bis 6:30 Uhr (für Nachteulen)
- **GPS-basierte Umkreissuche**: "Mein Standort" nutzt Browser-Geolocation
- **Bookmark-System**: Events merken, als PDF drucken, per E-Mail teilen (Cookie-basiert, DSGVO-konform)
- **Mobile-First**: Funktioniert auf jedem Device

### 🤖 Für Admins/Redakteure
- **Auto-Scraping**: Sammelt Events von konfigurierten Websites (läuft als GitHub Action)
- **Deduplication-Engine**: Erkennt Duplikate via Fuzzy-Matching (Titel, Datum, Ort, Zeit ±30min)
- **Data Enrichment**: Merged beste Daten aus allen Quellen (längste Beschreibung, beste Bilder)
- **Veranstalter-CRM**: 
  - Kontaktdaten (E-Mail, Telefon, Ansprechpartner)
  - One-Click-Actions (E-Mail schreiben, anrufen, Social Media)
  - Relationship-Tracking (neu → active → established)
  - Pattern Recognition (welcher Veranstalter nutzt welche Kanäle?)
- **AI-Flyer-Analyse**: Extrahiert Events aus Bildern/PDFs via GitHub Models oder DuckDuckGo AI
- **Admin-Interface**: 
  - Entwürfe prüfen & publizieren
  - Events manuell erstellen mit Recurring-Support
  - Duplikate reviewen mit Confidence Scores
  - Venue-Management (Barrierefreiheit, Kapazität, Kontakt)
- **Auto-Archivierung**: Events älter als 30 Tage wandern nach `_history/`

### 🛠️ Für Entwickler
- **Modular**: Scraping, Deduplication, Venue-Management als separate Python-Scripts
- **Jekyll + GitHub Pages**: Zero hosting costs
- **CSV-basiert**: Einfach zu editieren (Excel, Google Sheets)
- **Parametrisiert**: Stadt-Name, Koordinaten, etc. in `_config.yml`
- **Gut dokumentiert**: `docs/` mit ausführlichen Guides
- **GitHub Actions**: CI/CD für Scraping, Archivierung, Validation

---

## ✨ Features

Krawl kombiniert **Read-Only Simplicity** mit **intelligenter Automatisierung**:

### 🗺️ Für Besucher
- **Interaktive Karte** - touch-optimiert, schnell
- **Intelligente Filter**: Zeitraum, Umkreis, Kategorie
- **GPS-Umkreissuche**: "Was ist in meiner Nähe - jetzt?"
- **"Bis Sonnenaufgang"-Filter**: Für Nachteulen (Events bis 6:30 Uhr)
- **Bookmark-System**: Events merken, drucken, teilen (Cookie-basiert, DSGVO-konform)

### 🤖 Für Admins (hinter den Kulissen)
- **Auto-Scraping**: Sammelt Events automatisch
- **Deduplication-Engine**: Erkennt Duplikate intelligent (Fuzzy-Matching)
- **Data Enrichment**: Merged beste Daten aus allen Quellen
- **Veranstalter-CRM**: Kontakte, Networking, One-Click-Actions
- **AI-Flyer-Analyse**: Extrahiert Events aus PDFs/Bildern
- **Auto-Archivierung**: Alte Events wandern automatisch ins Archiv

### 🛠️ Für Entwickler
- **Jekyll + GitHub Pages**: Zero hosting costs
- **CSV-basiert**: Einfach zu editieren (Excel, Google Sheets)
- **Parametrisiert**: Anpassbar für jede Community
- **GitHub Actions**: CI/CD für Scraping, Archivierung, Validation

---

## 🚀 Für deine Community anpassen

### 1. Repository forken

```bash
gh repo fork feileberlin/event-kalender-hof --clone
cd event-kalender-hof
```

### 2. Community-Konfiguration anpassen

**`_config.yml`:**
```yaml
title: "meine-community.events"  # Dein Titel
description: "Events in/für Meine-Community"

city:  # Wird auch für Communities genutzt (Name historisch)
  name: "Meine Community"  # z.B. "Punk Szene Berlin" oder "Hof an der Saale"
  name_short: "MeineCommunity"  # Kurzform
  state: "Dein Bundesland"  # Optional, für geografische Communities
  center:
    lat: 52.5200  # Zentrum (z.B. Stadtzentrum oder Szene-Hotspot)
    lng: 13.4050
    name: "Haupttreffpunkt"  # z.B. "Rathaus" oder "Club XY"
  admin_email: "redaktion@meine-community.events"
```

### 3. Event-Quellen konfigurieren

**`_data/sources.csv`:**
```csv
name,url,type,active,notes
Stadtwebsite,https://www.meinstadt.de/events,html,true,Offizielle Events
Kulturzentrum,https://kulturzentrum.de/programm,html,true,
Facebook Stadtseite,https://facebook.com/stadtmeinstadt,facebook,true,
```

### 4. Veranstaltungsorte anlegen

**`_data/venues.csv`:**
```csv
name,aliases,address,lat,lng,wheelchair_accessible,website,phone,capacity,icon,color,location_type
Haupttreffpunkt,Main Spot,"Hauptstr. 1",52.5200,13.4050,true,https://...,+49...,200,🎸,#2c3e50,hauptort
Club Underground,Club UG,"Kellerstr. 5",52.5210,13.4060,false,https://...,+49...,150,🎭,#2c3e50,
```

### 5. GitHub Pages aktivieren

Settings → Pages → Source: `main` branch

**Done!** Deine Community hat jetzt einen Event-Kalender.

> **💡 Migration von v0.x:** Falls du von einer älteren Version upgradest, nutze `site.city.center` statt `site.default_center` (deprecated, aber noch kompatibel).
> 
> **💡 Hinweis:** Das Feld heißt `city` aus historischen Gründen, funktioniert aber genauso für Subkulturen, Netzwerke oder thematische Communities.

---

## 📦 Installation (lokal entwickeln)

```bash
# 1. Ruby + Jekyll
bundle install

# 2. Python-Dependencies
pip install -r requirements.txt

# 3. Jekyll Server starten
bundle exec jekyll serve

# 4. Browser öffnen
open http://localhost:4000/event-kalender-hof/
```

**Scripts testen:**
```bash
# Events scrapen
python3 scripts/editorial/scrape_events.py

# Duplikate finden
python3 scripts/editorial/deduplication_engine.py

# Alte Events archivieren
python3 scripts/editorial/archive_old_events.py

# Flyer analysieren
python3 scripts/editorial/analyze_flyer.py path/to/flyer.pdf
```

---

## 🤝 Mitmachen & Weiterentwickeln

**Das Projekt lebt von der Community!** Jede Stadt, die es nutzt, macht es besser.

### 🐛 Bugs gefunden?
→ [Issue aufmachen](https://github.com/feileberlin/event-kalender-hof/issues)

### 💡 Feature-Ideen?
→ [Discussion starten](https://github.com/feileberlin/event-kalender-hof/discussions)

### 🔧 Code beitragen?

1. **Fork** das Repo
2. **Branch** erstellen: `git checkout -b feature/mein-feature`
3. **Commit** mit klarer Message: `feat: Neue Scraping-Quelle für XY`
4. **Push** und **Pull Request** öffnen

**Besonders willkommen:**
- Neue Scraper für häufige Plattformen (Eventbrite, Meetup, etc.)
- Verbesserungen der Deduplication-Engine
- UI/UX-Optimierungen
- Barrierefreiheit (a11y)
- Performance-Optimierungen
- Übersetzungen (i18n)

### 📝 Dokumentation verbessern?

Die `docs/`-Ordner sind mit [Obsidian](https://obsidian.md/) optimiert. Einfach Markdown editieren und PR öffnen.

---

## 🏗️ Architektur (Überblick)

```
┌─────────────────────────────────────────────────────────┐
│                     DATENQUELLEN                        │
│  Websites · Facebook · PDFs · Manuelle Eingabe         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│               SCRAPING & PROCESSING                     │
│  scrape_events.py → _events/*.md (YAML Front Matter)   │
│  analyze_flyer.py → AI-basierte PDF/Bild-Extraktion    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│            DEDUPLICATION & ENRICHMENT                   │
│  deduplication_engine.py:                              │
│  - Fuzzy-Matching (Titel/Ort/Zeit)                     │
│  - Confidence Scoring                                   │
│  - Data Merging (beste Daten aus allen Quellen)        │
│  - Veranstalter-Matching (CRM-Integration)             │
│  → _data/event_clusters.csv                            │
│  → _data/admin_review_queue.json                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  ADMIN REVIEW                           │
│  admin.html:                                            │
│  - Tab: Entwürfe → Publizieren                         │
│  - Tab: Duplikate → Merge/Split/Ignore                 │
│  - Tab: Neue Events → Recurring-Support                │
│  - Veranstalter-Kontakte (One-Click-Actions)           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 JEKYLL BUILD                            │
│  _events/*.md → JSON für JavaScript                    │
│  _data/venues.csv → Locations mit Icons                │
│  _layouts/event.html → Event-Detailseiten              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                GITHUB PAGES                             │
│  index.html: Interaktive Karte (Leaflet.js)           │
│  assets/js/main.js: Filter, Suche, Bookmarks          │
│  → Live auf https://deineststadt.github.io/            │
└─────────────────────────────────────────────────────────┘
```

**CSV-basierte Konfiguration:**
- `_data/sources.csv` → Scraping-Quellen
- `_data/venues.csv` → Veranstaltungsorte (mit Icons, Farben, Barrierefreiheit)
- `_data/organizers.csv` → Veranstalter-CRM (Kontakte, Social Media, Notizen)
- `_data/event_clusters.csv` → Duplikat-Tracking

**Automatisierung via GitHub Actions:**
- Scraping: Täglich 6:00 + 18:00 UTC
- Archivierung: Täglich 3:00 UTC
- Validation: Täglich 4:00 UTC
- → Konfigurierbar in `_config.yml` (Cron-Format)

---

## 📚 Dokumentation

| Datei | Zielgruppe | Inhalt |
|-------|------------|--------|
| **[docs/QUICKSTART.md](docs/QUICKSTART.md)** | Alle | Schnelleinstieg in 5 Minuten |
| **[INSTALL.md](INSTALL.md)** | Admins | Installation, Konfiguration, erste Schritte |
| **[docs/ADMIN.md](docs/ADMIN.md)** | Admins | Event-Verwaltung, Scraping (erweitert) |
| **[docs/DEDUPLICATION.md](docs/DEDUPLICATION.md)** | Admins/Devs | Duplikat-Erkennung & Enrichment |
| **[docs/ORGANIZER_CRM.md](docs/ORGANIZER_CRM.md)** | Admins | Veranstalter-CRM, Networking, Kontakte |
| **[docs/BOOKMARKS.md](docs/BOOKMARKS.md)** | Alle/Devs | Bookmark-System: Merken, Drucken, Mailen |
| **[docs/VENUES.md](docs/VENUES.md)** | Admins | Venue-Management, Barrierefreiheit |
| **[docs/ARCHIVING.md](docs/ARCHIVING.md)** | Admins | Auto-Archivierung vergangener Events |
| **[docs/DATE_VALIDATION.md](docs/DATE_VALIDATION.md)** | Admins/Devs | Datums-Validierung, Qualitätssicherung |
| **[docs/SOURCES_WATCHER.md](docs/SOURCES_WATCHER.md)** | Admins/Devs | Auto-Scraping bei sources.csv Änderungen |
| **[docs/RECURRING_EVENTS.md](docs/RECURRING_EVENTS.md)** | Admins/Devs | Wiederkehrende Events (Basis) |
| **[docs/RECURRING_EVENTS_ADVANCED.md](docs/RECURRING_EVENTS_ADVANCED.md)** | Devs | Erweiterte Recurring-Logik |
| **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** | Entwickler | Tests, Code-Style, Pull Requests |

---

## 🛠️ Tech Stack

| Komponente | Technologie | Warum? |
|------------|-------------|--------|
| **Frontend** | Jekyll 3.10 | Statische Seiten, GitHub Pages native |
| **CSS** | Skeleton 2.0.4 | Minimal, responsive, <5KB |
| **Karte** | Leaflet.js 1.9.4 | Open-Source, touch-optimiert |
| **JavaScript** | Vanilla ES6+ | Keine Dependencies, schnell |
| **Scraping** | Python 3.11+, BeautifulSoup | Flexibel, gut dokumentiert |
| **AI** | GitHub Models / DuckDuckGo | Kostenlos, keine API-Keys |
| **Hosting** | GitHub Pages | Gratis, CDN, SSL, CI/CD |
| **Daten** | CSV + YAML | Human-readable, Excel-kompatibel |

---

## 🎯 Roadmap

**v1.0 (jetzt): Read-Only Event-Aggregation**
- ✅ Automatisches Scraping
- ✅ Deduplication-Engine
- ✅ Veranstalter-CRM
- ✅ Admin-Interface
- ✅ Bookmark-System
- ✅ GPS-Umkreissuche
- ✅ Geografische Filter

**v1.5 (geplant): Community-Input**
- 🔜 Event-Vorschläge (ohne Account)
- 🔜 Upvotes/Downvotes (zeigt Community-Präferenzen)
- 🔜 "Ich bin dabei"-Counter (ohne Social-Media-Lärm)
- 🔜 iCal/CalDAV Export
- 🔜 PWA (Progressive Web App)
- 🔜 Notification-System (E-Mail/Telegram bei neuen Events)

**v2.0 (Vision): Full Community**
- 💡 User-Profile (optional)
- 💡 Kommentare & Reviews
- 💡 Event-Sharing
- 💡 Federation: Community-übergreifende Event-Suche
- 💡 Moderation-Queue: Community-basierte Qualitätssicherung
- 💡 Mobile Apps (React Native)

**Krawl bleibt fokussiert:** Auch mit Community-Features steht die Kernfunktion im Mittelpunkt - **Events finden, nicht suchen.**

---

## 🙏 Credits & Inspiration

**Gebaut mit:**
- [Jekyll](https://jekyllrb.com/) - Static Site Generator
- [Leaflet.js](https://leafletjs.com/) - Interactive Maps
- [Skeleton CSS](http://getskeleton.com/) - Minimalist CSS Framework
- [OpenStreetMap](https://www.openstreetmap.org/) - Kartendaten

**Inspiriert von:**
- [Graz Advent](https://grazadvent.at/) - Minimalistische Event-Übersicht
- [berlin.digital](https://berlin.digital/) - Tech-Events Berlin
- Lokalen Kulturschaffenden, die jeden Tag großartige Events auf die Beine stellen

**Entwickelt für:** Krawlisten in Hof an der Saale - und alle anderen Communities (Städte, Subkulturen, Netzwerke), die folgen.

---

## 🌍 Use-Cases

Krawl funktioniert für jede Community, die Events hat:

- 🏙️ **Städte**: Lokale Event-Kalender (Hof, Bamberg, Freiburg...)
- 🎸 **Subkulturen**: Punk-Szene Berlin, Metal-Events Bayern, Indie-Kultur Hamburg
- 🛠️ **Maker-Spaces**: Hackerspace-Events, FabLab-Workshops, Repair-Cafés
- 🌱 **Themen-Netzwerke**: Permakultur-Treffen, Degrowth-Events, Transition Towns
- 🎮 **Nischen**: Retro-Gaming-Meetups, Brettspiel-Stammtische, Cosplay-Conventions

**"Nähe" ist relativ:** Für eine Stadt = 10 km, für eine Subkultur = 200 km.

---

## 📄 Lizenz

**MIT License** - siehe [LICENSE](LICENSE)

**TL;DR:** Du kannst dieses Projekt für alles nutzen (privat, kommerziell, modifiziert) - solange du den Copyright-Hinweis beibehältst. Keine Garantie, keine Haftung.

---

## 💬 Kontakt & Community

- **Issues/Bugs:** [GitHub Issues](https://github.com/feileberlin/event-kalender-hof/issues)
- **Diskussionen:** [GitHub Discussions](https://github.com/feileberlin/event-kalender-hof/discussions)
- **Pull Requests:** Immer willkommen!

**Du nutzt Krawl für deine Community?** → Schreib uns! Wir verlinken gerne andere Krawl-Instanzen.

---

**Made with ❤️ in Hof an der Saale**

*"Krawl — events finden, nicht suchen."*  
*Für Krawlisten, von Krawlisten.*
| **[PROJECT.md](docs/PROJECT.md)** | Entwickler | Technische Architektur, API-Referenz, Timeline |
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

Details: [docs/ADMIN.md](docs/ADMIN.md)

## 🧪 Testing

```bash
cd tests
node test_filters.js
```

Die Test Suite validiert HTML ↔ JavaScript Konsistenz automatisch.

Details: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

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

Vollständige Roadmap: [docs/PROJECT.md](docs/PROJECT.md)

---

**Entwickelt mit ❤️ für Hof an der Saale**
