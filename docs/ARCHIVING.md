# Event-Archivierung

## Übersicht

Automatische Archivierung alter Events nach `_events/_history/YYYY/` (organisiert nach Jahr).

## 🎯 Funktionsweise

### Automatisch (empfohlen)
**GitHub Actions Workflow** läuft jeden Montag um 3 Uhr (UTC):
- Events älter als **30 Tage** werden archiviert
- Status → `"Archiviert"`
- Verschoben nach `_events/_history/{JAHR}/`
- Automatischer Commit

### Manuell
```bash
# Dry-Run (zeigt nur was passieren würde)
python scripts/archive_old_events.py --days 30 --dry-run

# Tatsächlich archivieren
python scripts/archive_old_events.py --days 30

# Interaktiv (bei jedem Event nachfragen)
python scripts/archive_old_events.py --days 30 --interactive

# Custom Threshold (z.B. 60 Tage)
python scripts/archive_old_events.py --days 60
```

## 📋 Script-Optionen

```
usage: archive_old_events.py [--days N] [--dry-run] [--interactive] [--force]

options:
  --days N         Events älter als N Tage archivieren (default: 30)
  --dry-run        Zeigt nur was passieren würde, keine Änderungen
  --interactive    Fragt bei jedem Event nach
  --force          Keine Bestätigung erforderlich
```

## 🔄 Workflow

```
1. Event ist älter als Threshold (z.B. 30 Tage)
   ↓
2. Script findet Event in _events/
   ↓
3. Status wird auf "Archiviert" gesetzt
   ↓
4. Datei wird verschoben nach _events/_history/YYYYMM/ (Jahr-Monat aus Event-Datum)
5. Vor Verschieben: Recurring-Flag wird gescannt und ggf. in Index eingetragen
6. Recurring-Index wird aktualisiert (_data/recurring_index.json)
   ↓
5. Original-Datei in _events/ wird gelöscht
   ↓
6. Git Commit + Push (bei Auto-Run)
```

## 📊 Beispiel-Output

```
============================================================
📦 EVENT ARCHIVIERUNG
============================================================
Threshold: Events älter als 30 Tage
Stichtag: 2025-10-20

🔍 Suche Events zum Archivieren...

📊 Statistik:
  • Gesamt Events: 45
  • Zum Archivieren: 12
  • Bereits archiviert: 3
  • Zu neu: 30
  • Fehler: 0

📁 Archiv-Struktur:
  • _history/202509/ (September 2025): 8 Events
  • _history/202510/ (Oktober 2025): 12 Events
  • _history/202511/ (November 2025): 6 Events

❓ 12 Events archivieren? (j/n): j

📦 Archiviere Events...
------------------------------------------------------------
  ✅ 2025-09-15-konzert.md → _history/202509/2025-09-15-konzert.md
  ✅ 2025-09-18-festival.md → _history/202509/2025-09-18-festival.md
  ✅ 2025-10-01-theater.md → _history/202510/2025-10-01-theater.md
  ...

============================================================
✅ ARCHIVIERUNG ABGESCHLOSSEN
============================================================
Archiviert: 12 Events
Fehler: 0

💡 Nächste Schritte:
   1. git add _events/
   2. git commit -m 'Archive: Events älter als 30 Tage'
   3. git push
```

## 🚀 GitHub Actions

### Manuell triggern
1. Gehe zu **Actions** Tab auf GitHub
2. Wähle **"Archive Old Events"**
3. Klicke **"Run workflow"**
4. Konfiguriere:
   - `days`: Threshold (default: 30)
   - `dry_run`: `true` (Test) oder `false` (Live)
5. Klicke **"Run workflow"**

### Workflow-Config
`.github/workflows/archive-old-events.yml`:
```yaml
on:
  schedule:
    - cron: '0 3 * * 1'  # Jeden Montag 3 Uhr UTC
  workflow_dispatch:     # Manueller Trigger
```

**Permissions erforderlich**: `contents: write` (bereits konfiguriert)

## 📁 Verzeichnis-Struktur

```
_events/
├── 2025-11-25-jazz-night.md         ← Aktuelle Events (Öffentlich/Entwurf)
├── 2025-12-15-weihnachtsmarkt.md
└── _history/                         ← Archivierte Events
    ├── 2024/
    │   ├── 2024-01-15-konzert.md    ← Status: "Archiviert"
    │   └── 2024-12-31-silvester.md
    ├── 2025/
    │   ├── 2025-09-15-festival.md
    │   └── 2025-10-01-markt.md
    └── README.md
```

## 🎯 Status-Übersicht

| Status | Frontend | Admin | Location |
|--------|----------|-------|----------|
| **Entwurf** | ❌ | ✅ Tab "Entwürfe" | `_events/` |
| **Öffentlich** | ✅ | ✅ Tab "Veröffentlicht" | `_events/` |
| **Archiviert** | ❌ | ✅ Tab "Archiviert" | `_events/_history/YYYYMM/` (automatisch) |

## 🔧 Integration

### Admin-Interface
- **Tab "📦 Archiviert"** zeigt alle archivierten Events
- **Statistik** zeigt Anzahl archivierter Events
- **Badge** grau für archivierte Events

### Frontend-Filter
`index.html` filtert automatisch:
```liquid
{% if event.status == "Öffentlich" %}
  <!-- Nur Öffentliche Events auf Hauptseite -->
{% endif %}
```

### Broken Link Checker
`scripts/check_broken_links.py` prüft auch archivierte Events

## ⚙️ Konfiguration

### Threshold anpassen
Standard ist **30 Tage**, ändern in:

**GitHub Workflow** (`.github/workflows/archive-old-events.yml`):
```yaml
workflow_dispatch:
  inputs:
    days:
      default: '30'  # ← Hier ändern
```

**Lokal**:
```bash
python scripts/archive_old_events.py --days 60
```

### Schedule anpassen
Workflow läuft Standard **Montags 3 Uhr UTC**, ändern in:

```yaml
schedule:
  - cron: '0 3 * * 1'  # Min Std Tag Mon Wochentag
  
# Beispiele:
# '0 2 * * *'     # Jeden Tag 2 Uhr
# '0 3 * * 0'     # Jeden Sonntag 3 Uhr
# '0 0 1 * *'     # Jeden 1. des Monats Mitternacht
```

## 🐛 Troubleshooting

### "Keine Events gefunden"
**Problem**: Script findet keine Events älter als Threshold

**Lösung**:
```bash
# Prüfe Datum der Events
ls -lh _events/*.md

# Reduziere Threshold
python scripts/archive_old_events.py --days 7 --dry-run
```

### "Permission denied"
**Problem**: Script kann Dateien nicht verschieben

**Lösung**:
```bash
# Prüfe Berechtigungen
ls -la _events/

# Make script executable
chmod +x scripts/archive_old_events.py
```

### "YAML parsing error"
**Problem**: Event-Datei hat ungültiges YAML

**Lösung**:
```bash
# Finde fehlerhafte Dateien
python -c "
import yaml
from pathlib import Path
for f in Path('_events').glob('*.md'):
    try:
        content = f.read_text()
        parts = content.split('---', 2)
        yaml.safe_load(parts[1])
    except Exception as e:
        print(f'{f.name}: {e}')
"
```

### "Workflow schlägt fehl"
**Problem**: GitHub Actions Fehler

**Lösung**:
1. Prüfe Actions-Log auf GitHub
2. Stelle sicher: `permissions: contents: write` ist gesetzt
3. Teste lokal: `python scripts/archive_old_events.py --dry-run`

## 📚 Weitere Infos

- **Archiv-README**: `_events/_history/README.md`
- **Script-Hilfe**: `python scripts/archive_old_events.py --help`
- **Admin-Guide**: `docs/ADMIN.md`
- **Workflow-Logs**: GitHub → Actions → "Archive Old Events"
