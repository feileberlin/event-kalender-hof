# Venue-Management Quick Reference

## 🚀 Schnellstart

### Event-Scraping mit Venue-Enrichment
```bash
python scripts/scrape_events.py
```

**Output:**
```
📍 Venue Manager geladen: 5 Venues
✓ Venue Match: 'Freiheitshalle Hof' → 'Freiheitshalle Hof'
⚠ Venue nicht gefunden: 'Neue Location'

============================================================
📋 VENUE REPORT
============================================================
⚠️  Fehlende Venues (1):
  • Neue Location

📝 Template für _data/venues.csv:
------------------------------------------------------------
"Neue Location","","",,,,false,false,false,false,,,,2025-11-19
------------------------------------------------------------
```

### Fehlende Venues hinzufügen

**Option 1: Interaktives Tool**
```bash
python scripts/venue_admin.py
# → Menü: 3. Neuen Venue hinzufügen
```

**Option 2: Direkt in CSV**
```bash
# venues.csv öffnen, Zeile einfügen:
Neue Location,Alias1,Alias2,"Straße 1, Hof",50.320,11.917,true,true,false,true,https://...,+49...,500,Notizen,2025-11-19
```

### Venues verwalten

**Alle anzeigen:**
```bash
python scripts/venue_admin.py
# → Menü: 1. Alle Venues anzeigen
```

**Venue suchen:**
```bash
python scripts/venue_admin.py
# → Menü: 2. Venue suchen
```

**Details anzeigen:**
```bash
python scripts/venue_admin.py
# → Menü: 5. Venue-Details anzeigen
```

## 📊 Venue-Felder

| Feld | Typ | Beschreibung | Pflicht |
|------|-----|--------------|---------|
| `name` | String | Offizieller Name | ✅ Ja |
| `aliases` | String | Alternative Namen (kommasepariert) | Nein |
| `address` | String | Vollständige Adresse | Empfohlen |
| `lat` | Float | Breitengrad (Dezimal) | Empfohlen |
| `lng` | Float | Längengrad (Dezimal) | Empfohlen |
| `wheelchair_accessible` | Boolean | Rollstuhlgerecht | Ja (true/false) |
| `wheelchair_toilet` | Boolean | Rollstuhl-WC | Ja (true/false) |
| `parking` | Boolean | Parkplatz | Ja (true/false) |
| `public_transport` | Boolean | ÖPNV-Anbindung | Ja (true/false) |
| `website` | String | Website-URL | Nein |
| `phone` | String | Telefonnummer | Nein |
| `capacity` | Integer | Max. Besucheranzahl | Nein |
| `notes` | String | Zusatzinfos | Nein |
| `last_updated` | Date | Letzte Änderung | Auto |

## 🎯 Häufige Aufgaben

### Koordinaten finden
1. Google Maps öffnen
2. Rechtsklick auf Ort
3. "Was ist hier?" → Koordinaten kopieren
4. Format: `50.3197, 11.9168`

### Venue mit mehreren Schreibweisen
```csv
Theater Hof,"Stadttheater Hof,Theater,Hof Theater",...
```
→ Findet: "Theater Hof", "Stadttheater", "theater", etc.

### Barrierefreiheit prüfen
- Venue-Website checken (Oft unter "Besucherinfo")
- Vor Ort prüfen
- Kontakt aufnehmen: `phone` aus CSV

### Events ohne Venue
```bash
# Alle Events analysieren
python scripts/venue_admin.py
# → Menü: 4. Fehlende Venues aus Events finden
```

### Venue-Daten aktualisieren
```csv
# Vor Update:
Theater Hof,...,false,false,...,2024-01-15

# Nach Update (z.B. jetzt rollstuhlgerecht):
Theater Hof,...,true,true,...,2025-11-19
```

## 🐍 Python-Integration

```python
from venue_manager import VenueManager

manager = VenueManager()

# Venue finden
venue = manager.find_venue("Freiheitshalle")
print(venue['wheelchair_accessible'])  # True

# Event anreichern
event = {'location': 'Freiheitshalle Hof', ...}
enriched = manager.enrich_event_data(event)
print(enriched['venue']['capacity'])  # 1500

# Fehlende finden
missing = manager.find_missing_venues(events)
```

## 📋 Checkliste: Neuen Venue anlegen

- [ ] Name + Aliases festlegen
- [ ] Adresse recherchieren
- [ ] Koordinaten ermitteln (Google Maps)
- [ ] Barrierefreiheit prüfen:
  - [ ] Rollstuhlgerecht?
  - [ ] Rollstuhl-WC?
  - [ ] Parkplatz?
  - [ ] ÖPNV-Anbindung?
- [ ] Website + Telefon hinzufügen
- [ ] Kapazität recherchieren
- [ ] In venues.csv eintragen
- [ ] `last_updated` auf heute setzen
- [ ] Events re-scrapen → Venue-Match testen

## ⚠️ Troubleshooting

**Venue wird nicht gefunden:**
```bash
# Test:
python scripts/venue_examples.py
# → Prüfe BEISPIEL 1 Output

# Fix: Alias hinzufügen in venues.csv
```

**CSV-Fehler beim Speichern:**
```
Fehler: "mapping values are not allowed"
```
→ Kommas in Feldern mit `"..."` escapen:
```csv
"Adresse mit, Komma"
```

**Koordinaten falsch:**
```
Event wird nicht auf Karte angezeigt
```
→ Dezimalgrad nutzen: `50.3197` (NICHT `50°19'10.9"N`)

## 🔗 Links

- 📖 **Vollständige Doku**: [docs/VENUES.md](VENUES.md)
- 🛠️ **Admin-Guide**: [docs/ADMIN.md](ADMIN.md)
- 📝 **Beispiel-Code**: `scripts/venue_examples.py`
- 🎯 **Admin-Tool**: `scripts/venue_admin.py`
