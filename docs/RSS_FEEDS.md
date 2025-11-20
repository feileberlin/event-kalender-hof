# RSS Feeds

## Verfügbare Feeds

### Standard-Feed
- **URL**: `https://krawl.ist/feed.xml`
- **Filter**: Events bis Sonnenaufgang
- **Aktualisierung**: Täglich bei jedem Jekyll-Build

### Thematische Feeds
- **Musik**: `https://krawl.ist/feeds/musik.xml` (Musik-Events diese Woche)

## Eigene Feeds konfigurieren

Feeds werden in `_config.yml` unter `filters.rss_feeds` definiert:

```yaml
filters:
  rss_feeds:
    - name: "Feed-Name"
      filename: "custom-feed.xml"  # Oder "feed.xml" für Standard-Feed
      time: "sunrise"                # Time-Filter-Key (optional)
      category: "Musik"              # Kategorie-Filter (optional)
      radius: ""                     # Radius-Filter (optional, im RSS nicht umgesetzt)
```

## Feed generieren

Nach Änderungen an der Config:

```bash
python scripts/generate_rss_feeds.py
```

Dies erstellt automatisch die Feed-Dateien im Root oder `feeds/` Verzeichnis.

## Beispiele

### Alle Events bis Sonnenaufgang
```yaml
- name: "Alle Events bis Sonnenaufgang"
  filename: "feed.xml"
  time: "sunrise"
  category: ""
  radius: ""
```

### Kultur-Events die nächsten 3 Tage
```yaml
- name: "Kultur-Events (3 Tage)"
  filename: "kultur-3days.xml"
  time: "3days"  # Erfordert entsprechenden time_filter
  category: "Kultur"
  radius: ""
```

### Sport-Events diese Woche
```yaml
- name: "Sport diese Woche"
  filename: "sport-weekly.xml"
  time: "week"
  category: "Sport"
  radius: ""
```

## Hinweise

- **Radius-Filter** werden im RSS nicht umgesetzt (benötigt User-Location)
- **Time-Filter-Keys** müssen in `filters.time_filters` definiert sein
- **Kategorie-Keys** müssen in `filters.categories` existieren
- Feeds werden bei jedem Jekyll-Build aktualisiert
- Format: RSS 2.0 mit Atom-Namespace

## Integration in anderen Apps

### Feed-Reader
Kopiere die Feed-URL in deinen RSS-Reader (z.B. Feedly, Inoreader, NetNewsWire)

### Kalender-Apps
Einige Kalender-Apps können RSS-Feeds als Ereignisquelle nutzen

### Automation
Nutze RSS-zu-X-Dienste wie IFTTT oder Zapier für Notifications
