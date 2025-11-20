# 📜 Scripts Directory

Organisierte Skript-Sammlung für Entwicklung, Redaktion und Wartung.

## 📁 Struktur

```
scripts/
├── README.md              # Diese Datei
├── dev/                   # Development & Setup
├── editorial/             # Content-Management & Redaktion
├── tests/                 # Funktionale Tests
└── validation/            # Code Quality & Linting
```

---

## 🛠️ dev/ - Development & Setup

**Zweck:** Entwicklungs-Tools und Setup-Skripte

### Verfügbare Skripte
- `dev.sh` - Development-Server starten (Jekyll)
- `setup.sh` - Projekt-Setup (Dependencies, Config)
- `generate_test_events.py` - Lorem Ipsum Test-Events generieren
- `cleanup_test_events.py` - Test-Events löschen

### Verwendung
```bash
# Development-Server
./scripts/dev/dev.sh

# Projekt-Setup
./scripts/dev/setup.sh

# Test-Events generieren (für Filter-Tests)
python scripts/dev/generate_test_events.py --count 15

# Test-Events wieder löschen
python scripts/dev/cleanup_test_events.py
```

---

## ✏️ editorial/ - Content-Management & Redaktion

**Zweck:** Event-Verwaltung, Deduplication, Content-Generierung

### Event-Management
- `deduplication_engine.py` - Duplikate erkennen und zusammenführen
- `archive_old_events.py` - Vergangene Events archivieren
- `recurring_expander.py` - Wiederkehrende Events generieren
- `date_enhancer.py` - Event-Datumsfelder erweitern

### Content-Generierung
- `analyze_flyer.py` - Events aus Flyern extrahieren (AI)
- `generate_rss_feeds.py` - RSS-Feeds aus Config generieren
- `regenerate_docs.py` - Projekt-Dokumentation aktualisieren

### Venue-Verwaltung
- `venue_manager.py` - Programmatische Venue-API
- `venue_admin.py` - CLI für Venue-Verwaltung

### Verwendung
```bash
# Duplikate finden
python scripts/editorial/deduplication_engine.py

# Alte Events archivieren
python scripts/editorial/archive_old_events.py

# Recurring Events expandieren (3 Monate)
python scripts/editorial/recurring_expander.py --months 3

# RSS-Feeds aus Config generieren
python scripts/editorial/generate_rss_feeds.py
```

---

## 🧪 tests/ - Funktionale Tests

**Zweck:** JavaScript-Tests für Filter, Events, Bookmarks

### Verfügbare Tests
- `test_filters.html` - Filter-Logik (Kategorien, Zeit, Radius)
- `test_events.html` - Event-Manager und Event-Rendering
- `test_bookmarks.html` - Bookmark-System (Speichern, Laden, Löschen)

### Verwendung
```bash
# Tests im Browser öffnen
open scripts/tests/test_filters.html
open scripts/tests/test_events.html
open scripts/tests/test_bookmarks.html

# Oder: Development-Server starten
./scripts/dev/dev.sh
# Dann: http://localhost:4000/scripts/tests/
```

### Test-Struktur
Jeder Test lädt die Module und testet:
- ✅ Initialisierung
- ✅ Kern-Funktionalität
- ✅ Edge Cases
- ✅ Fehlerbehandlung

---

## ✅ validation/ - Code Quality & Linting

**Zweck:** Code-Qualität, Syntax-Checks, Lint-Tests

### Verfügbare Validatoren
- `lint_css.sh` - CSS-Linting (stylelint)
- `lint_html.sh` - HTML-Validierung (html-validate)
- `lint_js.sh` - JavaScript-Linting (eslint)
- `lint_markdown.sh` - Markdown-Linting (markdownlint)
- `lint_all.sh` - Alle Linter auf einmal

### Verwendung
```bash
# Einzelne Linter
./scripts/validation/lint_css.sh
./scripts/validation/lint_js.sh
./scripts/validation/lint_html.sh

# Alle Linter
./scripts/validation/lint_all.sh
```

### Setup
```bash
# Node.js-basierte Linter installieren
npm install -g stylelint stylelint-config-standard
npm install -g eslint @eslint/js
npm install -g html-validate
npm install -g markdownlint-cli
```

---

## 🔄 Typische Workflows

### 1. Neue Events hinzufügen
```bash
# Scrapen
./scripts/dev/scrape.sh

# Duplikate prüfen
python scripts/editorial/deduplication_engine.py

# Preview
./scripts/dev/dev.sh
```

### 2. Vor einem Commit
```bash
# Code-Qualität prüfen
./scripts/validation/lint_all.sh

# Funktionale Tests
open scripts/tests/test_filters.html

# Alles OK? Commit!
git add -A && git commit
```

### 3. Monatliche Wartung
```bash
# Alte Events archivieren
python scripts/editorial/archive_old_events.py

# Recurring Events expandieren
python scripts/editorial/recurring_expander.py --months 3

# RSS-Feeds neu generieren
python scripts/editorial/generate_rss_feeds.py
```

---

## 📚 Weitere Dokumentation

- **[INSTALL.md](../INSTALL.md)** - Setup-Anleitung
- **[docs/AUTOMATION.md](../docs/AUTOMATION.md)** - GitHub Actions Workflows
- **[docs/ADMIN.md](../docs/ADMIN.md)** - Admin-Panel Dokumentation
