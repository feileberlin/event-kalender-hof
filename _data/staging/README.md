# Staging Area - Event Review Queue

Dieser Ordner enthält neu gescrapte Events, die noch nicht veröffentlicht wurden.

## Workflow

1. **Scraper** schreibt Events hierher: `events-{timestamp}.json`
2. **GitHub Action** erstellt automatisch ein Review-Issue
3. **Editor** approved/rejected via Issue-Comment
4. **Merger** published approved Events nach `_data/events.json`

## Dateiformat

```json
{
  "scraped_at": "2025-11-21T15:00:00Z",
  "source": "stadt-hof",
  "events": [
    {
      "id": "sha256-hash",
      "status": "pending-review",
      "title": "...",
      "date": "2025-12-01",
      "start_time": "20:00",
      "end_time": "23:00",
      "place": {
        "name": "Freiheitshalle Hof",
        "slug": "freiheitshalle-hof",
        "address": "Kulmbacher Str. 4, 95030 Hof",
        "coords": {"lat": 50.3197, "lng": 11.9168}
      },
      "organizer": {
        "name": "Stadt Hof",
        "slug": "stadt-hof"
      },
      "category": "Kultur",
      "tags": ["Konzert", "Jazz"],
      "description": "...",
      "urls": {
        "source": "https://...",
        "tickets": null,
        "detail": null
      },
      "meta": {
        "scraped_at": "2025-11-21T15:00:00Z",
        "scraper_version": "2.0",
        "confidence": 0.95,
        "needs_review": false
      }
    }
  ]
}
```

## Manual Cleanup

```bash
# Lösche alte Staging-Files (nach Merge)
find _data/staging -name "events-*.json" -mtime +7 -delete
```
