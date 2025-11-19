# Event-Status Quick Reference

## 📊 Status-Übersicht

| Status | Frontend | Admin | Location | Farbe |
|--------|----------|-------|----------|-------|
| **Entwurf** | ❌ Nicht sichtbar | ✅ Tab "Entwürfe" | `_events/` | 🟡 Gelb |
| **Öffentlich** | ✅ Sichtbar | ✅ Tab "Veröffentlicht" | `_events/` | 🟢 Grün |
| **Archiviert** | ❌ Nicht sichtbar | ✅ Tab "Archiviert" | `_events/_history/{JAHR}/` | ⚪ Grau |

## 🔄 Status-Workflow

```
┌─────────────┐
│  Scraping   │
│   (Auto)    │
└──────┬──────┘
       │
       ↓ status: "Entwurf"
┌─────────────┐
│   Entwurf   │ ← Manuelle Überprüfung erforderlich
│  (Review)   │    Location: _events/
└──────┬──────┘
       │
       ↓ Admin ändert: status → "Öffentlich"
┌─────────────┐
│ Öffentlich  │ ← Auf Website sichtbar
│  (Live)     │    Location: _events/
└──────┬──────┘
       │
       ↓ Auto-Archivierung (> 30 Tage)
┌─────────────┐
│ Archiviert  │ ← Nicht mehr sichtbar
│  (Hidden)   │    Location: _events/_history/{JAHR}/
└─────────────┘
```

## 🎯 Status ändern

### Entwurf → Öffentlich
```yaml
# _events/2025-11-25-jazz-night.md
---
title: Jazz-Night
status: "Entwurf"  # ← Ändern zu: "Öffentlich"
---
```

**Via Script (Bash):**
```bash
# Einzelnes Event
sed -i 's/status: "Entwurf"/status: "Öffentlich"/' _events/2025-11-25*.md

# Alle Entwürfe vom 25. November
for file in _events/2025-11-25*.md; do
  sed -i 's/status: "Entwurf"/status: "Öffentlich"/' "$file"
done
```

**Via Script (PowerShell):**
```powershell
# Einzelnes Event
(Get-Content _events/2025-11-25-jazz-night.md) -replace 'status: "Entwurf"', 'status: "Öffentlich"' | Set-Content _events/2025-11-25-jazz-night.md

# Alle Entwürfe vom 25. November
Get-ChildItem _events/2025-11-25*.md | ForEach-Object {
  (Get-Content $_.FullName) -replace 'status: "Entwurf"', 'status: "Öffentlich"' | Set-Content $_.FullName
}
```

### Öffentlich → Archiviert

**Automatisch** (empfohlen):
- Geschieht automatisch nach 30 Tagen
- Jeden Montag 3 Uhr (UTC)
- Via GitHub Actions

**Manuell** (Script):
```bash
python scripts/archive_old_events.py --days 30
```

**Manuell** (YAML + Verschieben):
```bash
# 1. Status ändern
sed -i 's/status: "Öffentlich"/status: "Archiviert"/' _events/2025-01-15-event.md

# 2. Verschieben
mkdir -p _events/_history/2025
mv _events/2025-01-15-event.md _events/_history/2025/
```

### Archiviert → Öffentlich (Restore)

```bash
# 1. Zurück verschieben
mv _events/_history/2025/2025-01-15-event.md _events/

# 2. Status ändern
sed -i 's/status: "Archiviert"/status: "Öffentlich"/' _events/2025-01-15-event.md
```

## 🔍 Status prüfen

### Via grep
```bash
# Alle Entwürfe
grep -r 'status: "Entwurf"' _events/*.md

# Alle Öffentlichen
grep -r 'status: "Öffentlich"' _events/*.md

# Alle Archivierten
grep -r 'status: "Archiviert"' _events/_history/
```

### Via Python
```python
from pathlib import Path
import yaml

for file in Path('_events').glob('*.md'):
    with open(file) as f:
        content = f.read()
        parts = content.split('---', 2)
        event = yaml.safe_load(parts[1])
        print(f"{event['status']:12} {file.name}")
```

### Via Admin-Interface
1. Öffne `/admin.html`
2. Statistik zeigt:
   - Entwürfe: 📝 Tab
   - Veröffentlicht: ✓ Tab
   - Archiviert: 📦 Tab

## 📦 Auto-Archivierung

### Konfiguration
- **Threshold**: 30 Tage (default)
- **Schedule**: Montags 3 Uhr UTC
- **Workflow**: `.github/workflows/archive-old-events.yml`

### Manuell triggern
1. GitHub → **Actions** Tab
2. **"Archive Old Events"**
3. **"Run workflow"**
4. Konfiguriere:
   - `days`: 30 (oder custom)
   - `dry_run`: `false` (Live) oder `true` (Test)

### Lokal testen
```bash
# Dry-Run (keine Änderungen)
python scripts/archive_old_events.py --days 30 --dry-run

# Live
python scripts/archive_old_events.py --days 30

# Interactive
python scripts/archive_old_events.py --days 30 --interactive
```

## 🎨 Frontend-Filter

### index.html (Hauptseite)
```liquid
{% for event in site.events %}
{% if event.status == "Öffentlich" %}
  <!-- Nur Öffentliche Events anzeigen -->
{% endif %}
{% endfor %}
```

### admin.html (Admin-Interface)
```javascript
// Alle Events laden (inkl. Archivierte)
const allEvents = [
  {% for event in site.events %}
    { ..., status: {{ event.status | jsonify }} }
  {% endfor %}
];

// Filter nach Status
if (tab === 'drafts') {
    events = events.filter(e => e.status === 'Entwurf');
} else if (tab === 'published') {
    events = events.filter(e => e.status === 'Öffentlich');
} else if (tab === 'archived') {
    events = events.filter(e => e.status === 'Archiviert');
}
```

## 🛠️ Implementierungs-Details

### _config.yml (Default-Status)
```yaml
defaults:
  - scope:
      type: "events"
    values:
      status: "Entwurf"  # Neue Events sind Entwurf
```

### scripts/scrape_events.py
```python
event_data = {
    'title': event['title'],
    ...
    'status': 'Entwurf',  # Gescrapte Events immer Entwurf
}
```

### .github/workflows/archive-old-events.yml
```yaml
on:
  schedule:
    - cron: '0 3 * * 1'  # Montags 3 Uhr UTC
  workflow_dispatch:     # Manueller Trigger
```

## ⚠️ Wichtig

### Status-Werte
- ✅ **Exakte Strings**: `"Entwurf"`, `"Öffentlich"`, `"Archiviert"`
- ❌ **NICHT**: `Entwurf` (ohne Quotes), `entwurf` (Kleinschreibung)
- ✅ **In YAML**: `status: "Öffentlich"` ODER `status: Öffentlich`
- ✅ **In Liquid**: `{% if event.status == "Öffentlich" %}`

### Jekyll Collection
```yaml
# _config.yml
collections:
  events:
    output: true  # Generiert HTML-Seiten
    permalink: /events/:name.html
```

Alle Events (auch Archivierte) sind Teil von `site.events`!

### Git Workflow
```bash
# Nach Status-Änderung
git add _events/
git commit -m "Publish: Events vom 25. November"
git push

# Nach Auto-Archivierung
# → GitHub Actions committed automatisch
```

## 📚 Weitere Infos

- **Archivierungs-Guide**: `docs/ARCHIVING.md`
- **Admin-Guide**: `docs/ADMIN.md`
- **Script-Hilfe**: `python scripts/archive_old_events.py --help`
- **Archiv-README**: `_events/_history/README.md`
