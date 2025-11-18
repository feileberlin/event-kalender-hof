# 🚀 Quick Start Guide

Event-Kalender Hof in 5 Minuten starten!

## Option 1: GitHub Pages (Empfohlen)

### Schritt 1: Repository forken
1. Besuche: https://github.com/feileberlin/event-kalender-hof
2. Klicke auf "Fork"
3. Wähle deinen Account

### Schritt 2: Baseurl anpassen
1. Öffne `_config.yml` in deinem Fork
2. Ändere `baseurl: "/event-kalender-hof"` zu `baseurl: "/DEIN-REPO-NAME"`
3. Commit & Push

### Schritt 3: GitHub Pages aktivieren
1. Gehe zu deinem Fork → Settings → Pages
2. Source: "GitHub Actions"
3. Warte ~2 Minuten auf Deployment

### Schritt 4: Website öffnen
→ `https://DEIN-USERNAME.github.io/DEIN-REPO-NAME`

**Fertig!** 🎉

---

## Option 2: Lokal entwickeln

### Voraussetzungen installieren

**macOS/Linux:**
```bash
# Ruby
brew install ruby

# Python
brew install python@3.11

# Git
brew install git
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ruby-full python3 python3-pip git
```

### Projekt einrichten

```bash
# 1. Repository klonen
git clone https://github.com/feileberlin/event-kalender-hof.git
cd event-kalender-hof

# 2. Dependencies installieren
bundle install
pip install -r requirements.txt

# 3. Server starten (baseurl wird automatisch leer für lokale Entwicklung)
bundle exec jekyll serve --livereload
```

→ Öffne: http://localhost:4000

---

## Erste Schritte

### 1. Erstes Event erstellen

Erstelle: `_events/2025-11-20-mein-event.md`

```yaml
---
title: "Mein erstes Event"
date: 2025-11-20
start_time: "19:00"
location: "Rathaus Hof"
coordinates:
  lat: 50.3197
  lng: 11.9168
category: "Musik"
description: "Ein tolles Event"
status: "Öffentlich"
---

Hier kommt die Beschreibung...
```

### 2. Event-Scraper testen

```bash
python scripts/scrape_events.py
```

### 3. Flyer analysieren (AI-powered) 🆕

**Automatische Event-Extraktion aus Flyern:**

```bash
# Beispiel: Event-Flyer von URL analysieren
python scripts/analyze_flyer.py https://example.com/flyer.jpg

# Oder PDF-Flyer
python scripts/analyze_flyer.py https://example.com/programm.pdf
```

**Was passiert:**
- 🤖 AI analysiert Bild/PDF (GitHub Models oder DuckDuckGo AI)
- 📝 Extrahiert Titel, Datum, Ort, Zeit, Beschreibung
- 🗺️ Geocodiert Adresse automatisch
- 💾 Erstellt Event-Datei mit `status: "Entwurf"`
- ⚠️ Manuelle Prüfung erforderlich!

**Benötigt:**
- PIL/Pillow, PyPDF2 (automatisch installiert)
- Optional: Tesseract für OCR-Fallback

### 4. Admin-Bereich nutzen

Öffne: `/admin/`

---

## Häufige Probleme

### Jekyll startet nicht
```bash
# Dependencies neu installieren
bundle install
gem cleanup
```

### Python-Fehler
```bash
# Virtual Environment nutzen
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### GitHub Actions schlägt fehl
- Prüfe: Settings → Actions → General → Workflow permissions
- Setze auf: "Read and write permissions"

---

## Nächste Schritte

1. ✅ [Vollständige Dokumentation lesen](README.md)
2. ✅ [Eigene Event-Quellen hinzufügen](README.md#scraping-konfiguration)
3. ✅ [Design anpassen](README.md#css-anpassungen)
4. ✅ [Zur Community beitragen](CONTRIBUTING.md)

---

**Braucht du Hilfe?** → [GitHub Issues](https://github.com/feileberlin/event-kalender-hof/issues)
