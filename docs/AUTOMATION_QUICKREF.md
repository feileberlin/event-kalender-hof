# ⚙️ Automation Config Quick Reference

**TL;DR:** Alle Intervalle in `_config.yml` → Workflows referenzieren diese Config

## 📍 Neue Standorte hinzufügen

### 1. _config.yml
```yaml
locations:
  mein_ort:
    lat: 50.1234
    lng: 11.5678
    name: "Mein Veranstaltungsort"
```

### 2. assets/js/main.js
```javascript
const LOCATIONS = {
    // ... existing locations
    mein_ort: { lat: 50.1234, lng: 11.5678, name: 'Mein Veranstaltungsort' }
};
```

### 3. index.html
```html
<option value="mein_ort" data-icon="📍">Mein Veranstaltungsort</option>
```

## ⏰ Schedules anpassen

**Datei:** `_config.yml`

```yaml
automation:
  scraping:
    schedule: "0 6,18 * * *"  # Täglich 6:00 + 18:00 UTC
  archiving:
    schedule: "0 3 * * *"     # Täglich 3:00 UTC
  date_validation:
    schedule: "0 4 * * *"     # Täglich 4:00 UTC
  documentation:
    schedule: "0 5 * * 0"     # Sonntags 5:00 UTC
  code_validation:
    schedule: "0 3 1 * *"     # Monatlich am 1. um 3:00 UTC
  monthly_tests:
    schedule: "0 2 1 * *"     # Monatlich am 1. um 2:00 UTC
```

**Cron-Cheatsheet:**
```
┌─ Minute (0-59)
│ ┌─ Stunde (0-23)
│ │ ┌─ Tag (1-31)
│ │ │ ┌─ Monat (1-12)
│ │ │ │ ┌─ Wochentag (0-6, 0=So)
* * * * *
```

**Beispiele:**
- `0 6,18 * * *` = Täglich 6:00 + 18:00 UTC
- `0 */6 * * *` = Alle 6 Stunden
- `0 0 * * 0` = Jeden Sonntag Mitternacht
- `*/15 * * * *` = Alle 15 Minuten

**UTC → MEZ/MESZ:**
- MEZ (Winter): UTC +1
- MESZ (Sommer): UTC +2
- Beispiel: 8:00 MEZ = `0 7 * * *` (7:00 UTC)

## 🗂️ Archivierung konfigurieren

```yaml
archiving:
  days_threshold: 30              # Events älter als X Tage
  target_directory: "_events/_history"
```

**Manuell triggern:**
```bash
gh workflow run archive-old-events.yml --field days=60
```

## 🕸️ Scraping konfigurieren

```yaml
scraping:
  max_retries: 3
  timeout_seconds: 30
  user_agent: "Mozilla/5.0 (krawl.ist-Bot)"
```

## 🚀 Manuelles Scraping

```bash
# Scrapt alle Quellen aus sources.csv
./scripts/scrape.sh

# Oder direkt Python-Script
python scripts/editorial/scrape_events.py
```

## 📊 Dokumentation regenerieren

**Automatisch:** Jeden Sonntag 5:00 UTC

**Manuell:**
```bash
# Lokal
python scripts/editorial/regenerate_docs.py

# GitHub Actions
gh workflow run regenerate-docs.yml --field reason="Nach Update"
```

**Aktualisiert:**
- `docs/PROJECT.md` (Statistik-Sektion)
- `README.md` (Event-Count-Badge)

**Statistiken:**
- Events: Gesamt, Veröffentlicht, Entwürfe, Archiviert, Recurring
- Datenquellen: Sources, Venues, Locations
- Code: Python, JS, CSS, HTML, Markdown (Lines of Code)
- Git: Commits, Letzter Commit

## 🔧 Workflow manuell ausführen

```bash
# Web-UI
Actions → Workflow auswählen → Run workflow

# CLI
gh workflow run scrape-events.yml
gh workflow run archive-old-events.yml
gh workflow run regenerate-docs.yml
```

## 🐛 Troubleshooting

**Workflow läuft nicht?**
1. Actions aktiviert? (Repo-Settings)
2. Cron-Syntax korrekt? → https://crontab.guru
3. YAML valide? → `gh workflow view <file>`

**Schedule verzögert?**
- Normal: Bis zu 15 Min. Verzögerung
- Bei hoher Last: Ggf. übersprungen
- Workaround: workflow_dispatch verwenden

**Script-Fehler?**
```bash
# Logs prüfen
gh run list --workflow=<name>.yml
gh run view <run-id> --log

# Lokal testen
python scripts/<script>.py
```

## 📚 Siehe auch

- [AUTOMATION.md](AUTOMATION.md) - Vollständige Dokumentation
- [SOURCES_WATCHER.md](SOURCES_WATCHER.md) - Auto-Scraping Details
- [ARCHIVING.md](ARCHIVING.md) - Archivierungs-Details
- https://crontab.guru - Cron Expression Tester
