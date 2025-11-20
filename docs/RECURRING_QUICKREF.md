# Recurring Events - Schnellreferenz

Automatische Verwaltung wiederkehrender Events (z.B. Wochenmärkte, regelmäßige Stammtische).

## 🔄 Konzept

1. **Recurring-Flag**: Events mit `recurring.enabled: true` im YAML werden als Vorlagen erkannt
2. **Index**: `_data/recurring_index.json` speichert alle wiederkehrenden Events für schnellen Zugriff
3. **Auto-Expansion**: Generiert automatisch fehlende Instanzen für konfigurierten Zeitraum
4. **Monatliche Archivierung**: Alte Events werden nach `_events/_history/YYYYMM/` verschoben

## 📝 Recurring-Konfiguration

### Beispiel: Wöchentlicher Event

```yaml
---
title: "Hofer Wochenmarkt"
date: 2025-11-19
start_time: "08:00"
location: "Maxplatz"
recurring:
  enabled: true
  frequency: weekly    # daily, weekly, biweekly, monthly, yearly
  interval: 1          # Alle X Wochen/Monate/Jahre
  by_day:              # Wochentage (optional)
    - WE               # Mittwoch
    - SA               # Samstag
  start_date: "2025-11-19"
  end_date: null       # null = kein Ende
  exceptions:          # Ausnahmen (z.B. Feiertage)
    - "2025-12-25"
---
```

### Wochentags-Codes

- `MO` = Montag
- `TU` = Dienstag
- `WE` = Mittwoch
- `TH` = Donnerstag
- `FR` = Freitag
- `SA` = Samstag
- `SU` = Sonntag

### Frequenzen

- `daily`: Täglich
- `weekly`: Wöchentlich
- `biweekly`: Zweiwöchentlich
- `monthly`: Monatlich (gleicher Tag im Monat)
- `yearly`: Jährlich

## 🛠️ Befehle

### Index aufbauen

Scannt alle Events und erstellt/aktualisiert den Index:

```bash
python3 scripts/recurring_expander.py --rebuild-index
```

**Wann ausführen:**
- Nach manueller Bearbeitung von recurring-Events
- Beim ersten Setup
- Wenn Index beschädigt ist

### Instanzen generieren

Generiert fehlende Event-Instanzen für die nächsten X Monate:

```bash
# Standard: 3 Monate im Voraus
python3 scripts/recurring_expander.py

# Nur 1 Monat
python3 scripts/recurring_expander.py --months 1

# 6 Monate
python3 scripts/recurring_expander.py --months 6

# Ohne Index (vollständiger Scan)
python3 scripts/recurring_expander.py --no-index
```

**Wann ausführen:**
- Regelmäßig (z.B. wöchentlich via Cron/GitHub Actions)
- Nach Anlegen eines neuen recurring-Events
- Manuell bei Bedarf

### Integration ins Scraping

Das Recurring-System ist bereits ins Scraping integriert:

```bash
bash scripts/scrape.sh
```

Workflow:
1. **Bereinigung**: Alte Events archivieren (mit Recurring-Scan)
2. **Scraping**: Neue Events von Quellen sammeln
3. **Recurring**: Fehlende Instanzen generieren
4. **Report**: Statistik und fehlende Venues

## 📁 Archivierung

### Monatliche Struktur

```
_events/
  _history/
    202509/           # September 2025
    202510/           # Oktober 2025
    202511/           # November 2025
```

### Archivierungs-Workflow

```bash
# Dry-Run (zeigt nur was passieren würde)
python3 scripts/archive_old_events.py --dry-run

# Archiviere Events älter als 30 Tage
python3 scripts/archive_old_events.py --days 30

# Interaktiv (fragt bei jedem Event)
python3 scripts/archive_old_events.py --interactive

# Events älter als 60 Tage
python3 scripts/archive_old_events.py --days 60
```

**Vor Archivierung:**
- Recurring-Flag wird gescannt
- Events werden zum Index hinzugefügt
- Index wird aktualisiert

## 🔍 Index-Struktur

`_data/recurring_index.json`:

```json
{
  "last_update": "2025-11-20T12:15:30",
  "recurring_events": [
    {
      "id": "eb7febc457d2",
      "title": "Hofer Wochenmarkt",
      "location": "Maxplatz",
      "start_time": "08:00",
      "recurring": {
        "enabled": true,
        "frequency": "weekly",
        "by_day": ["WE", "SA"]
      },
      "template_file": "_events/2025-11-19-wochenmarkt.md"
    }
  ],
  "stats": {
    "total_recurring": 4
  }
}
```

## ⚙️ Automatisierung (Optional)

### GitHub Actions

Füge zu `.github/workflows/recurring.yml` hinzu:

```yaml
name: Generate Recurring Events

on:
  schedule:
    - cron: '0 2 * * 1'  # Jeden Montag um 2 Uhr
  workflow_dispatch:     # Manueller Trigger

jobs:
  expand:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Generate recurring events
        run: python3 scripts/recurring_expander.py --months 3
      
      - name: Commit changes
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add _events/ _data/recurring_index.json
          git commit -m "Auto-generate recurring events" || echo "No changes"
          git push
```

### Cron (Server)

```bash
# Crontab-Eintrag
0 2 * * 1 cd /pfad/zum/projekt && python3 scripts/recurring_expander.py --months 3
```

## 🐛 Troubleshooting

### Problem: Duplikate werden generiert

**Lösung:**
```bash
# Index neu aufbauen
python3 scripts/recurring_expander.py --rebuild-index
```

### Problem: Instanzen fehlen

**Prüfung:**
1. Ist `recurring.enabled: true`?
2. Ist `start_date` korrekt?
3. Liegt Event im konfigurierten Zeitraum?

```bash
# Vollständiger Scan ohne Index
python3 scripts/recurring_expander.py --no-index --months 6
```

### Problem: Alte Instanzen nicht archiviert

```bash
# Archivierung manuell ausführen
python3 scripts/archive_old_events.py --days 30
```

## 📊 Statistik

### Wie viele recurring Events?

```bash
cat _data/recurring_index.json | grep '"total_recurring"'
```

### Wie viele Instanzen generiert?

```bash
grep -r "recurring_parent:" _events/*.md | wc -l
```

### Welche Events sind recurring?

```bash
grep -r "recurring:" _events/*.md -l | xargs basename -a
```

## 💡 Best Practices

1. **Regelmäßige Expansion**: Führe `recurring_expander.py` wöchentlich aus
2. **Index pflegen**: Bei manuellen Änderungen Index neu aufbauen
3. **Zeitraum begrenzen**: Nicht mehr als 6 Monate im Voraus generieren
4. **Exceptions nutzen**: Feiertage und Sondertermine als Exceptions eintragen
5. **Archivierung**: Alte Events regelmäßig archivieren (monatlich)

## 🔗 Siehe auch

- [RECURRING_EVENTS.md](RECURRING_EVENTS.md) - Detaillierte Dokumentation
- [ARCHIVING.md](ARCHIVING.md) - Archivierungs-System
- [AUTOMATION.md](AUTOMATION.md) - Automatisierung
