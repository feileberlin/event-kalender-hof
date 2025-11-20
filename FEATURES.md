# 🎯 Feature Registry

**Single Source of Truth** für alle aktiven Features im Event-Kalender.

**Zweck:** Verhindert versehentliches Löschen/Überschreiben von Features bei Änderungen.

**Update:** Bei jeder Feature-Addition/Removal diese Datei aktualisieren!

---

## 📊 Analytics & Tracking

### GoatCounter Analytics
- **Status:** 🟢 ACTIVE
- **Location:** 
  - `_layouts/map.html` (vor `</body>`)
  - `_layouts/base.html` (vor `</body>`)
- **Code:**
  ```html
  <script data-goatcounter="https://feileberlin.goatcounter.com/count"
          async src="//gc.zgo.at/count.js"></script>
  ```
- **Purpose:** Privacy-friendly Analytics (kein Cookies, GDPR-konform)
- **Test:** `grep -r "goatcounter" _layouts/`
- **Added:** 2025-11-19
- **Dependencies:** Keine

---

## 🔍 Filter-System

### Kategorien-Filter
- **Status:** 🟢 ACTIVE
- **Location:**
  - Config: `_config.yml` → `filters.categories`
  - HTML: `index.html` → `#categoryFilter`
  - JS: `assets/js/modules/filters.js` → `FilterManager.toggleCategory()`
- **Features:**
  - Dynamische Kategorien aus Config
  - Multi-select (mehrere gleichzeitig)
  - "Sonstiges"-Kategorie für nicht-konfigurierte Events
  - Icons + Pluralisierung
- **Test:** Dropdown hat Kategorien aus `_config.yml`
- **Dependencies:** `_config.yml`, Jekyll Liquid

### Zeit-Filter (Time Filters)
- **Status:** 🟢 ACTIVE
- **Location:**
  - Config: `_config.yml` → `filters.time_filters`
  - HTML: `index.html` → `#timeFilter`
  - JS: `assets/js/modules/filters.js` → `getNextSunrise()`, `getNextTatort()`, `getNextMoonPhase()`
- **Features:**
  - 🌅 Bis Sonnenaufgang (astronomisch oder override mit hours)
  - 📺 Bis nächster Tatort (Sonntag 20:15)
  - 🌕 Bis Vollmond/Neumond (Mondphasen-Berechnung)
  - Konfigurierbare Stunden-Override
- **Test:** 3 Time-Filter-Optionen im Dropdown
- **Dependencies:** `_config.yml`, Astronomische Berechnungen

### Radius-Filter
- **Status:** 🟡 HARDCODED (TODO: Config-Migration)
- **Location:**
  - HTML: `index.html` → `#radiusFilter` (hardcoded options)
  - JS: `assets/js/modules/filters.js` → `setRadius()`, `getDistanceKm()`
- **Current Implementation:**
  - Hardcoded: 1km, 3km, 10km, 999999km ("weit entfernt")
  - Magische Zahl: 999999 = unbegrenzt
- **TODO:** Migrieren zu `_config.yml` (siehe TODO.md #5)
- **Test:** Radius-Filter hat 4 Optionen
- **Dependencies:** MapManager (GPS)

### Standort-Filter (Location Select)
- **Status:** 🟢 ACTIVE
- **Location:**
  - Config: `_data/venues.csv` (location_type != null)
  - HTML: `index.html` → `#locationSelect`
  - JS: `assets/js/modules/filters.js` → `setLocation()`
- **Features:**
  - Vordefinierte Standorte (Rathaus, Bahnhof, etc.)
  - Browser-Geolocation (Mein Standort)
  - Icons aus venues.csv
- **Test:** Dropdown hat Venues mit location_type + "Mein Standort"
- **Dependencies:** `_data/venues.csv`

---

## 📡 RSS-Feeds

### Dynamische RSS-Feeds
- **Status:** 🟢 ACTIVE
- **Location:**
  - Config: `_config.yml` → `filters.rss_feeds`
  - Template: `_layouts/rss.xml`
  - Generator: `scripts/editorial/generate_rss_feeds.py`
  - Output: `feed.xml`, `feeds/*.xml`
- **Features:**
  - Filter-Kombinationen (time + category + radius)
  - Automatische Generierung via Script
  - RSS 2.0 Standard
- **Test:** 
  ```bash
  ls -la feed.xml feeds/
  curl https://krawl.ist/feed.xml | head
  ```
- **Dependencies:** `_config.yml`, Jekyll

---

## 🗺️ Karte & Geolocation

### Leaflet.js Integration
- **Status:** 🟢 ACTIVE
- **Location:**
  - JS: `assets/js/modules/map.js` → `MapManager`
  - HTML: `index.html` → `#map`
  - CSS: `assets/css/main.css` → `.fullscreen-map`
- **Features:**
  - Fullscreen-Karte (OpenStreetMap)
  - Event-Marker mit Popups
  - User-Location (Browser Geolocation API)
  - Distanz-Berechnung (Haversine-Formel)
- **Test:** Karte lädt, Marker sichtbar
- **Dependencies:** Leaflet.js CDN

---

## 🔖 Bookmarks

### Event-Bookmarks (LocalStorage)
- **Status:** 🟢 ACTIVE
- **Location:**
  - JS: `assets/js/modules/bookmarks.js` → `BookmarkManager`
  - Storage: `assets/js/modules/storage.js` → `Storage.save/load()`
  - UI: `index.html` → `#bookmarks-toolbar`
- **Features:**
  - Events merken (LocalStorage)
  - Bookmark-Toolbar (nur sichtbar wenn Bookmarks)
  - Drucken (window.print())
  - E-Mail (mailto:-Link)
  - Alle löschen
- **Test:** Event merken, Toolbar erscheint
- **Dependencies:** LocalStorage API

---

## 🎨 UI/UX

### 3-Seiten-Architektur
- **Status:** 🟢 ACTIVE
- **Pages:**
  - `index.html` → Map (Fullscreen-Karte + Filter)
  - `info.html` → Info-Seite (Über, Services, Impressum)
  - `404.html` → Error-Seite (Auto-Redirect nach 3s)
- **Test:** Alle 3 Seiten erreichbar
- **Dependencies:** Jekyll Layouts

### Responsive Filter (Inline Selects)
- **Status:** 🟢 ACTIVE
- **Location:** `index.html` → `.inline-select`
- **CSS:** `assets/css/main.css`
- **Features:**
  - Mobile-First Design
  - Emojis als Icons
  - Inline im Header
- **Test:** Filter auf Mobile/Desktop responsiv

### Dark Mode / Punk-Style
- **Status:** 🟢 ACTIVE (Admin-Panel)
- **Location:** `assets/css/admin.css`
- **Features:**
  - Neon-Grün Akzente
  - Dunkler Hintergrund
  - Glitch-Effekte
- **Test:** `/admin.html` hat Punk-Ästhetik

---

## 🛠️ Admin-Panel

### Event-Verwaltung
- **Status:** 🟢 ACTIVE
- **Location:** `admin.html`
- **Features:**
  - Tabs: Entwürfe, Duplikate, Veröffentlicht, Archiviert, Recurring, Alle, Neues Event
  - Event-Editor (via GitHub Issues)
  - Dedup-Button (triggert GitHub Action)
  - Recurring Events Preview
- **Test:** `/admin.html` lädt, Tabs funktionieren
- **Dependencies:** Jekyll Liquid, GitHub API

### GitHub Meta Editor
- **Status:** 🟢 ACTIVE
- **Location:** `admin.html` → Tab "GitHub Meta"
- **Features:**
  - Repository Description editieren
  - Homepage URL setzen
  - Topics verwalten
  - GitHub Personal Access Token Auth
- **Test:** Tab "GitHub Meta" existiert, Formular vorhanden
- **Dependencies:** GitHub REST API

---

## 📝 Content-Management

### Event-Scraping
- **Status:** 🟢 ACTIVE
- **Location:**
  - Script: `scripts/editorial/scrape_events.py`
  - Config: `_data/sources.csv`
  - Output: `_events/*.md`
  - Workflow: `.github/workflows/scrape-events.yml`
- **Features:**
  - Automatisches Scraping (täglich 6:00, 18:00 UTC)
  - Manuell via `scripts/editorial/scrape.sh`
  - Duplikats-Erkennung (Hash)
  - Logging in `_events/_logs/`
- **Test:**
  ```bash
  python scripts/editorial/scrape_events.py --dry-run
  ```
- **Dependencies:** Python, BeautifulSoup, requests

### Event-Archivierung
- **Status:** 🟢 ACTIVE
- **Location:**
  - Script: `scripts/editorial/archive_old_events.py`
  - Workflow: `.github/workflows/archive-old-events.yml`
  - Archive: `_events/_history/`
- **Features:**
  - Automatisch täglich 3:00 UTC
  - Threshold: 30 Tage (konfigurierbar)
  - Dry-run Mode
- **Test:**
  ```bash
  python scripts/editorial/archive_old_events.py --dry-run
  ```
- **Dependencies:** Python, PyYAML

### Deduplication
- **Status:** 🟢 ACTIVE
- **Location:**
  - Script: `scripts/editorial/deduplication_engine.py`
  - Button: `admin.html` → "Duplikate finden"
- **Features:**
  - Fuzzy-Matching (Titel, Datum, Venue)
  - Interaktive Merge-Vorschläge
  - Hash-basierte Duplikats-Erkennung
- **Test:**
  ```bash
  python scripts/editorial/deduplication_engine.py
  ```
- **Dependencies:** Python, difflib

---

## 🧪 Testing & Validation

### Test-Events-Generator
- **Status:** 🟢 ACTIVE
- **Location:**
  - Generator: `scripts/dev/generate_test_events.py`
  - Cleanup: `scripts/dev/cleanup_test_events.py`
  - Config: `_config.yml` → `debug.show_test_events`
- **Features:**
  - Lorem-Ipsum Events für Filter-Tests
  - Markiert mit `test_event: true`
  - Zufällige Kategorien, Venues, Zeiten
- **Test:**
  ```bash
  python scripts/dev/generate_test_events.py --count 10
  ```
- **Dependencies:** Python, PyYAML

### Filter Tests
- **Status:** 🟢 ACTIVE
- **Location:** `scripts/tests/test_filters.js`
- **Test:**
  ```bash
  node scripts/tests/test_filters.js
  ```
- **Dependencies:** Node.js

### Linting & Validation
- **Status:** 🟢 ACTIVE
- **Location:** `scripts/validation/`
- **Scripts:**
  - `lint_css.sh` (stylelint)
  - `lint_html.sh` (html-validate)
  - `lint_javascript.sh` (eslint)
  - `lint_markdown.sh` (markdownlint)
  - `lint_all.sh` (alle zusammen)
- **Test:**
  ```bash
  ./scripts/validation/lint_all.sh
  ```
- **Dependencies:** Node.js, npm packages

---

## 🔄 GitHub Actions Workflows

### Jekyll Build & Deploy
- **Status:** 🟢 ACTIVE
- **File:** `.github/workflows/jekyll.yml`
- **Trigger:** Push to main
- **Purpose:** Build Site, Deploy zu GitHub Pages

### Event Scraper
- **Status:** 🟢 ACTIVE
- **File:** `.github/workflows/scrape-events.yml`
- **Trigger:** Cron (6:00, 18:00 UTC), manual
- **Purpose:** Auto-scrape events von sources.csv

### Archive Old Events
- **Status:** 🟢 ACTIVE
- **File:** `.github/workflows/archive-old-events.yml`
- **Trigger:** Cron (3:00 UTC), manual
- **Purpose:** Archive events älter als 30 Tage

### Monthly Tests
- **Status:** 🟢 ACTIVE
- **File:** `.github/workflows/monthly-tests.yml`
- **Trigger:** Cron (1. des Monats, 2:00 UTC)
- **Purpose:** Filter-Tests, Code-Validation, Build-Test

### Docs Regeneration
- **Status:** 🟢 ACTIVE
- **File:** `.github/workflows/regenerate-docs.yml`
- **Trigger:** Cron (Sonntag 5:00 UTC), manual
- **Purpose:** Update PROJECT.md, README.md

---

## 🔐 Security & Privacy

### GDPR-Konformität
- **Status:** 🟢 ACTIVE
- **Measures:**
  - GoatCounter (Cookie-frei)
  - Kein Google Analytics
  - LocalStorage (nur Client-seitig)
  - Keine User-Accounts
  - Kein Tracking ohne Consent

### Content Security
- **Status:** 🟢 ACTIVE
- **Measures:**
  - Static Site (kein Server-Side Code)
  - GitHub Actions (trusted Workflows)
  - Dependencies via CDN (Leaflet.js)

---

## 📚 Dokumentation

### User-Facing Docs
- **Status:** 🟢 ACTIVE
- **Files:**
  - `README.md` → Projekt-Overview
  - `INSTALL.md` → Setup-Anleitung
  - `info.html` → User-Info-Seite

### Developer Docs
- **Status:** 🟢 ACTIVE
- **Files:**
  - `docs/AUTOMATION.md` → Workflows
  - `docs/ADMIN.md` → Admin-Panel
  - `docs/VENUES.md` → Venue-Management
  - `docs/DEDUPLICATION.md` → Dedup-Engine
  - `docs/RSS_FEEDS.md` → RSS-System
  - `scripts/README.md` → Scripts-Overview

### Code Documentation
- **Status:** 🟢 ACTIVE
- **Location:**
  - JSDoc-Comments in allen JS-Modulen
  - Docstrings in Python-Scripts
  - Inline-Comments für komplexe Logik

---

## 🚀 Deployment

### GitHub Pages
- **Status:** 🟢 ACTIVE
- **URL:** https://feileberlin.github.io/krawl.ist/
- **Custom Domain:** https://krawl.ist (via CNAME)
- **Build:** Automatisch via GitHub Actions
- **Branch:** main

### Cache Management
- **Status:** 🟢 ACTIVE
- **Method:** Cache-Invalidation-Timestamp in `_config.yml`
- **Purpose:** Force Browser-Refresh bei Deployments

---

## 📊 Statistiken

- **Total Features:** 30+ aktive Features
- **Lines of Code:** ~15,000 (JS, Python, HTML, CSS)
- **Events:** ~50+ live Events
- **GitHub Actions:** 7 automatisierte Workflows
- **Scripts:** 25+ Python/Bash Scripts
- **Tests:** Filter-Tests, Lint-Tests

---

## ⚠️ Deprecated / Removed Features

### Alte Tests-Directory
- **Status:** 🔴 REMOVED (2025-11-20)
- **Reason:** Duplikat, verschoben nach `scripts/tests/`

### Maintenance-Scripts-Directory
- **Status:** 🔴 RENAMED → `scripts/editorial/` (2025-11-20)
- **Reason:** Besserer Name für Content-Management

---

## 🔄 Pending Migrations (siehe TODO.md)

1. **Radius-Filter Config-Migration** → `_config.yml` (wie Time-Filter)
2. **Feature Guard Workflow** → Automatische Feature-Checks

---

**Last Updated:** 2025-11-20  
**Maintained by:** GitHub Copilot + User  
**Update Trigger:** Bei jedem Feature-Add/Remove/Change
