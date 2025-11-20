# Event-Archiv

Dieses Verzeichnis enthält archivierte Events, organisiert nach Jahr.

## 📁 Struktur

Events werden **nach Jahr organisiert**:

```
_events/_history/
├── 2024/                         ← Events aus 2024
│   ├── 2024-01-15-konzert.md
│   └── 2024-12-31-silvester.md
├── 2025/                         ← Events aus 2025
│   ├── 2025-01-01-neujahr.md
│   └── ...
└── README.md (diese Datei)
```

**Wichtig**: Die Jahreszahl wird automatisch aus dem Event-Datum extrahiert!

## 🔄 Automatische Archivierung

Events werden **automatisch archiviert**:
- **Wann**: Jeden Montag um 3 Uhr (UTC)
- **Regel**: Events älter als 30 Tage
- **Aktion**: 
  1. Status → `"Archiviert"`
  2. Verschoben nach `_history/YYYY/` (Jahr aus Event-Datum)
  3. Commit via GitHub Actions

**GitHub Workflow**: `.github/workflows/archive-old-events.yml`

## 🛠️ Manuelle Archivierung

### Via Script
```bash
# Dry-Run (zeigt was passieren würde)
python scripts/editorial/archive_old_events.py --days 30 --dry-run

# Tatsächlich archivieren
python scripts/editorial/archive_old_events.py --days 30

# Interaktiv (bei jedem Event nachfragen)
python scripts/editorial/archive_old_events.py --days 30 --interactive
```

### Via GitHub Actions
1. Gehe zu **Actions** Tab
2. Wähle **"Archive Old Events"**
3. Klicke **"Run workflow"**
4. Konfiguriere:
   - `days`: Threshold (default: 30)
   - `dry_run`: true/false

### Manuell
```yaml
# Datei öffnen: _events/2025-01-15-event.md
status: "Öffentlich"  # → Ändern zu:
status: "Archiviert"

# Datei verschieben:
mv _events/2025-01-15-event.md _events/_history/2025/
```

## 📊 Status-System

| Status | Sichtbarkeit | Location |
|--------|--------------|----------|
| **Entwurf** | ❌ Nicht auf Website | `_events/` |
| **Öffentlich** | ✅ Auf Website | `_events/` |
| **Archiviert** | ❌ Nicht auf Website | `_events/_history/YYYY/` (Jahr automatisch) |

## 🔍 Archivierte Events anzeigen

### Admin-Interface
- URL: `/admin.html`
- Tab: **📦 Archiviert**
- Zeigt alle archivierten Events

### Jekyll-Query
```liquid
{% for event in site.events %}
  {% if event.status == "Archiviert" %}
    <!-- Event ist archiviert -->
  {% endif %}
{% endfor %}
```

### Lokale Suche
```bash
# Alle archivierten Events finden
grep -r 'status: "Archiviert"' _events/_history/

# Events aus 2024
ls _events/_history/2024/

# Nach Titel suchen
grep -r "Jazz" _events/_history/
```

## 🔧 Wartung

### Alte Archive löschen
```bash
# Alle Events älter als 2 Jahre löschen
find _events/_history/ -type f -mtime +730 -delete

# Bestimmtes Jahr löschen
rm -rf _events/_history/2020/
```

### Archive wiederherstellen
```bash
# Event zurück zu _events/ verschieben
mv _events/_history/2025/2025-01-15-event.md _events/

# Status ändern
sed -i 's/status: "Archiviert"/status: "Öffentlich"/' _events/2025-01-15-event.md
```

## 📝 Hinweise

- **Jekyll erkennt archivierte Events**: Sie sind Teil von `site.events`, aber werden nicht auf der Hauptseite angezeigt (Frontend-Filter)
- **Broken Link Checker**: `scripts/check_broken_links.py` prüft auch archivierte Events
- **Backup**: Archive sind Teil des Git-Repository und werden bei jedem Commit gesichert
- **Speicherplatz**: Alte Archive können gelöscht werden, wenn nicht mehr benötigt

## 🆘 Probleme

**"Archivierte Events werden noch angezeigt"**
→ Prüfe `status` in YAML Front Matter: Muss exakt `"Archiviert"` sein

**"Script findet keine Events"**
→ Prüfe Threshold: `--days 30` (Events müssen älter als 30 Tage sein)

**"Workflow schlägt fehl"**
→ Prüfe Actions-Log auf GitHub → Permissions: `contents: write` erforderlich

## 📚 Weitere Infos

- **Script-Doku**: `scripts/editorial/archive_old_events.py --help`
- **Workflow-Config**: `.github/workflows/archive-old-events.yml`
- **Admin-Guide**: `docs/ADMIN.md`
