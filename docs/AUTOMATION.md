# ⚙️ Automatisierungs-Konfiguration

**Letzte Aktualisierung:** 19. November 2025  
**Version:** v1.7.0

## Übersicht

Alle Automatisierungs-Intervalle werden zentral in `_config.yml` konfiguriert. Dies ermöglicht einfache Anpassung der Schedules ohne Workflow-Dateien zu bearbeiten.

## Konfiguration (_config.yml)

### Automation-Sektion

```yaml
automation:
  scraping:
    schedule: "0 6,18 * * *"  # Täglich um 6:00 und 18:00 UTC
    description: "Event-Scraping von konfigurierten Quellen"
  
  archiving:
    schedule: "0 3 * * *"  # Täglich um 3:00 UTC
    description: "Archivierung vergangener Events (älter als 30 Tage)"
  
  date_validation:
    schedule: "0 4 * * *"  # Täglich um 4:00 UTC
    description: "Validierung von Event-Datumsangaben"
  
  documentation:
    schedule: "0 5 * * 0"  # Jeden Sonntag um 5:00 UTC
    description: "Regenerierung der Projekt-Dokumentation"
  
  code_validation:
    schedule: "0 3 1 * *"  # Monatlich am 1. um 3:00 UTC
    description: "HTML/CSS/JS Lint & Validierung"
  
  monthly_tests:
    schedule: "0 2 1 * *"  # Monatlich am 1. um 2:00 UTC
    description: "Komplette Testbatterie (Filter, Python, etc.)"
  
  sources_watcher:
    enabled: true
    debounce_seconds: 2
    description: "File Watcher für sources.csv (läuft lokal)"
```

### Archivierungs-Konfiguration

```yaml
archiving:
  days_threshold: 30  # Events älter als X Tage archivieren
  target_directory: "_events/_history"
```

### Scraping-Konfiguration

```yaml
scraping:
  max_retries: 3
  timeout_seconds: 30
  user_agent: "Mozilla/5.0 (Event-Kalender-Hof-Bot)"
```

### Standorte

```yaml
locations:
  rathaus:
    lat: 50.3197
    lng: 11.9168
    name: "Rathaus Hof"
  bahnhof:
    lat: 50.3132
    lng: 11.9196
    name: "Hauptbahnhof Hof"
  kaserne:
    lat: 50.3092
    lng: 11.9053
    name: "Oberfranken-Kaserne"
  hochschule:
    lat: 50.3295
    lng: 11.9021
    name: "Hochschule Hof"
```

## Cron-Format

```
┌───────────── Minute (0 - 59)
│ ┌───────────── Stunde (0 - 23)
│ │ ┌───────────── Tag des Monats (1 - 31)
│ │ │ ┌───────────── Monat (1 - 12)
│ │ │ │ ┌───────────── Wochentag (0 - 6, 0=Sonntag)
│ │ │ │ │
* * * * *
```

### Beispiele

| Cron | Beschreibung |
|------|--------------|
| `0 6,18 * * *` | Täglich um 6:00 und 18:00 UTC |
| `0 3 * * *` | Täglich um 3:00 UTC |
| `0 5 * * 0` | Jeden Sonntag um 5:00 UTC |
| `*/15 * * * *` | Alle 15 Minuten |
| `0 0 1 * *` | Am 1. jeden Monats um Mitternacht |

## Workflows

### 1. Event-Scraping (scrape-events.yml)

**Trigger:**
- Schedule: `automation.scraping.schedule`
- Manuell: `workflow_dispatch`

**Funktion:**
- Scrapt Events von konfigurierten Quellen
- Erstellt Entwürfe in `_events/`
- Duplikatsprüfung via Hash

**Konfiguration:**
```yaml
scraping:
  max_retries: 3
  timeout_seconds: 30
```

### 2. Event-Archivierung (archive-old-events.yml)

**Trigger:**
- Schedule: `automation.archiving.schedule`
- Manuell: `workflow_dispatch` (mit days Parameter)

**Funktion:**
- Verschiebt Events älter als X Tage nach `_events/_history/JAHR/`
- Standard: 30 Tage (konfigurierbar)

**Konfiguration:**
```yaml
archiving:
  days_threshold: 30
  target_directory: "_events/_history"
```

### 3. Datums-Validierung (validate-code.yml)

**Trigger:**
- Schedule: `automation.date_validation.schedule`
- Bei Push (nur relevante Dateien)

**Funktion:**
- Prüft Event-Daten auf Plausibilität
- Erkennt fehlerhafte Datumsangaben
- Erstellt GitHub Issues bei Fehlern

### 4. Dokumentations-Regenerierung (regenerate-docs.yml)

**Trigger:**
- Schedule: `automation.documentation.schedule`
- Manuell: `workflow_dispatch`

**Funktion:**
- Aktualisiert `docs/PROJECT.md` mit aktuellen Statistiken
- Aktualisiert README.md Badges
- Committed Änderungen automatisch

**Script:** `scripts/regenerate_docs.py`

**Statistiken:**
- Event-Counts (Gesamt, Veröffentlicht, Entwürfe, Archiviert, Recurring)
- Datenquellen (Sources, Venues, Locations)
- Code-Metriken (Python, JavaScript, CSS, HTML, Markdown)
- Git-Informationen (Commits, Letzter Commit)

### 5. Code-Validierung (validate-code.yml)

**Trigger:**
- Schedule: `automation.code_validation.schedule`
- Bei Push (HTML/CSS/JS Dateien)
- Manuell: `workflow_dispatch`

**Funktion:**
- HTML-Validierung (W3C Nu Validator)
- CSS-Linting (stylelint)
- JavaScript-Linting (ESLint)
- Erstellt GitHub Issues bei Fehlern

**Läuft:** Monatlich am 1. um 3:00 UTC

### 6. Monatliche Tests (monthly-tests.yml)

**Trigger:**
- Schedule: `automation.monthly_tests.schedule`
- Manuell: `workflow_dispatch`

**Funktion:**
- Filter-Tests (JavaScript)
- Python-Script-Tests
- Venue-Validierung
- Recurring-Events-Validierung
- Komplette Testbatterie

**Läuft:** Monatlich am 1. um 2:00 UTC

### 7. Manuelles Scraping (scripts/scrape.sh)

**Trigger:** Manuell ausführen

**Funktion:**
- Scrapt alle Events aus `_data/sources.csv`
- Erstellt Entwürfe in `_events/`
- Schreibt Logs in `_events/_logs/`
- Duplikatsprüfung via Hash

**Ausführung:**
```bash
./scripts/scrape.sh
```

**Hinweis:** Das Script ruft `scripts/scrape_events.py` auf.

## Standorte hinzufügen

### 1. In _config.yml definieren

```yaml
locations:
  mein_ort:
    lat: 50.1234
    lng: 11.5678
    name: "Mein Veranstaltungsort"
```

### 2. In JavaScript verfügbar machen

Die Standorte werden automatisch aus `_config.yml` gelesen. In `assets/js/main.js`:

```javascript
const LOCATIONS = {
    rathaus: { lat: 50.3197, lng: 11.9168, name: 'Rathaus Hof' },
    bahnhof: { lat: 50.3132, lng: 11.9196, name: 'Hauptbahnhof Hof' },
    kaserne: { lat: 50.3092, lng: 11.9053, name: 'Oberfranken-Kaserne' },
    hochschule: { lat: 50.3295, lng: 11.9021, name: 'Hochschule Hof' },
    mein_ort: { lat: 50.1234, lng: 11.5678, name: 'Mein Veranstaltungsort' }
};
```

### 3. In HTML dropdown hinzufügen

In `index.html`:

```html
<select id="locationSelect" class="inline-select">
    <option value="rathaus" selected data-icon="🏛️">Rathaus</option>
    <option value="bahnhof" data-icon="🚂">Hauptbahnhof</option>
    <option value="kaserne" data-icon="🏰">Oberfranken-Kaserne</option>
    <option value="hochschule" data-icon="🎓">Hochschule Hof</option>
    <option value="mein_ort" data-icon="📍">Mein Veranstaltungsort</option>
    <option value="browser" data-icon="🎯">Mein Standort</option>
</select>
```

## Manuelle Ausführung

Alle Workflows können manuell über GitHub Actions ausgeführt werden:

```bash
# Via GitHub Web-UI:
Actions → Workflow auswählen → Run workflow

# Via GitHub CLI:
gh workflow run scrape-events.yml
gh workflow run archive-old-events.yml --field days=60
gh workflow run regenerate-docs.yml --field reason="Nach großem Update"
```

## Lokale Entwicklung

### Dokumentation regenerieren

```bash
python scripts/regenerate_docs.py
```

### Sources-Watcher starten

```bash
./scripts/scrape.sh
```

### Archivierung testen

```bash
python scripts/archive_old_events.py --days 30 --dry-run
```

## Best Practices

### 1. Intervalle anpassen

**Überlegungen:**
- Rate Limits beachten (GitHub Actions: 20 concurrent jobs)
- Kosten bei privaten Repos (2000 Minuten/Monat kostenlos)
- Sinnvolle Zeitpunkte (z.B. Scraping morgens/abends)

**Beispiel - Häufigeres Scraping:**
```yaml
automation:
  scraping:
    schedule: "0 */6 * * *"  # Alle 6 Stunden
```

### 2. Zeitzone berücksichtigen

Alle Cron-Schedules laufen in **UTC**!

**Umrechnung UTC → MEZ/MESZ:**
- MEZ (Winter): UTC + 1 Stunde
- MESZ (Sommer): UTC + 2 Stunden

**Beispiel:**
- Gewünscht: 8:00 MEZ (Winter)
- Cron: `0 7 * * *` (7:00 UTC)

### 3. Monitoring

**GitHub Actions Status:**
- Actions-Tab im Repository
- E-Mail-Benachrichtigungen bei Fehlern
- Badge im README

**Logs prüfen:**
```bash
gh run list --workflow=scrape-events.yml
gh run view <run-id> --log
```

### 4. Fehlerbehandlung

Alle Scripts loggen Fehler und erstellen bei Bedarf GitHub Issues:

- Scraping-Fehler → Issue mit Label `scraping-error`
- Validierungs-Fehler → Issue mit Label `validation-error`
- Dokumentations-Fehler → Workflow-Log, kein Issue

## Troubleshooting

### Workflow läuft nicht

**Prüfen:**
1. Actions in Repository-Settings aktiviert?
2. Cron-Syntax korrekt? → https://crontab.guru
3. Workflow-Datei in `.github/workflows/`?
4. YAML-Syntax valide?

**Debugging:**
```bash
# Workflow-Syntax prüfen
gh workflow view scrape-events.yml

# Letzten Run anzeigen
gh run list --workflow=scrape-events.yml --limit 1
```

### Schedule wird ignoriert

GitHub Actions Schedule-Events haben Einschränkungen:
- Können bis zu 15 Minuten verzögert sein
- Bei hoher Last ggf. übersprungen
- Nur in default branch (main)

**Workaround:**
- Manuelle Ausführung via `workflow_dispatch`
- Externen Cron-Job einrichten (cron-job.org)

### Script-Fehler

**Logs prüfen:**
```bash
gh run view <run-id> --log
```

**Lokal testen:**
```bash
python scripts/regenerate_docs.py
# Oder
python scripts/archive_old_events.py --dry-run
```

## Siehe auch

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Cron Syntax](https://crontab.guru)
- [SOURCES_WATCHER.md](SOURCES_WATCHER.md) - Auto-Scraping Details
- [ARCHIVING.md](ARCHIVING.md) - Archivierungs-Details
- [ADMIN.md](ADMIN.md) - Admin-Tasks
