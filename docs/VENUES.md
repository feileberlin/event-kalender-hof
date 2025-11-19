# Venue Management System

## Überblick

Das Venue Management System verwaltet Veranstaltungsorte mit Metadaten, die nicht bei jedem Event-Scraping verfügbar sind (z.B. Barrierefreiheit, Kontaktdaten, Kapazität).

## Komponenten

### 1. `_data/venues.csv`
Zentrale Venue-Datenbank mit folgenden Feldern:

| Feld | Typ | Beschreibung | Beispiel |
|------|-----|--------------|----------|
| `name` | String | Offizieller Name | `Freiheitshalle Hof` |
| `aliases` | String | Alternative Namen (kommasepariert) | `Freiheitshalle,Kulturzentrum Hof` |
| `address` | String | Vollständige Adresse | `Kulmbacher Str. 4, 95030 Hof` |
| `lat` | Float | Breitengrad | `50.3197` |
| `lng` | Float | Längengrad | `11.9168` |
| `wheelchair_accessible` | Boolean | Rollstuhlgerecht | `true` |
| `wheelchair_toilet` | Boolean | Rollstuhl-WC vorhanden | `true` |
| `parking` | Boolean | Parkplatz verfügbar | `true` |
| `public_transport` | Boolean | ÖPNV-Anbindung | `true` |
| `website` | String | Website-URL | `https://www.freiheitshalle-hof.de` |
| `phone` | String | Telefonnummer | `+49 9281 8150` |
| `capacity` | Integer | Maximale Besucheranzahl | `1500` |
| `notes` | String | Zusätzliche Informationen | `Hauptkulturzentrum der Stadt` |
| `last_updated` | Date | Letzte Aktualisierung | `2025-11-19` |

### 2. `scripts/venue_manager.py`
Python-Modul für Venue-Verwaltung:

```python
from venue_manager import VenueManager

manager = VenueManager()

# Venue finden (exakt oder fuzzy)
venue = manager.find_venue("Freiheitshalle")
# → Findet auch "freiheitshalle", "Kulturzentrum Hof" etc.

# Event-Daten anreichern
event_data = {
    'location': 'Freiheitshalle Hof',
    'date': '2025-11-25'
}
enriched = manager.enrich_event_data(event_data)
# → Fügt coordinates, address, venue-Metadaten hinzu

# Fehlende Venues finden
missing = manager.find_missing_venues(events)
# → Liste von Locations ohne Venue-Eintrag
```

**Features:**
- **Fuzzy Matching**: Findet Venues auch bei Schreibvarianten (Ähnlichkeit > 80%)
- **Alias-System**: Mehrere Namen pro Venue (z.B. "Freiheitshalle" + "Kulturzentrum Hof")
- **Auto-Enrichment**: Koordinaten, Adresse und Metadaten werden automatisch zu Events hinzugefügt
- **Missing-Report**: Zeigt Locations, die noch nicht in venues.csv sind

### 3. `scripts/venue_admin.py`
Interaktives CLI-Tool für Admin-Aufgaben:

```bash
python scripts/venue_admin.py
```

**Funktionen:**
1. **Alle Venues anzeigen** - Listet alle Venues mit Icons (♿ 🅿️ 🚌)
2. **Venue suchen** - Fuzzy-Suche nach Name
3. **Neuen Venue hinzufügen** - Interaktives Formular
4. **Fehlende Venues aus Events finden** - Analysiert _events/*.md
5. **Venue-Details anzeigen** - Vollständige Informationen

### 4. Integration in `scrape_events.py`
Der Event-Scraper nutzt VenueManager automatisch:

```python
# In EventScraper.__init__()
self.venue_manager = VenueManager()

# Nach Event-Scraping
event_data = self.venue_manager.enrich_event_data(event_data)
# → Event hat jetzt venue-Feld mit allen Metadaten

# Am Ende: Report
missing_venues = self.venue_manager.find_missing_venues(self.events)
# → Zeigt fehlende Venues + CSV-Template
```

## Workflow

### 1. Events scrapen
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

### 2. Fehlende Venues hinzufügen

**Option A: Manuell in CSV**
```bash
# venues.csv öffnen und Zeile einfügen:
Neue Location,Alternative Namen,"Straße 1, 95028 Hof",50.320,11.917,true,true,false,true,https://example.com,+49 123,500,Notizen,2025-11-19
```

**Option B: Admin-Tool**
```bash
python scripts/venue_admin.py
# → Menü: 3. Neuen Venue hinzufügen
# → Interaktives Formular ausfüllen
```

### 3. Venues verwalten

**Alle Venues anzeigen:**
```bash
python scripts/venue_admin.py
# → Menü: 1. Alle Venues anzeigen
```

**Venue-Details:**
```bash
python scripts/venue_admin.py
# → Menü: 5. Venue-Details anzeigen
```

**Fehlende Venues checken:**
```bash
python scripts/venue_admin.py
# → Menü: 4. Fehlende Venues aus Events finden
```

## Event-YAML mit Venue-Daten

Wenn ein Venue gefunden wird, enthält das Event-YAML zusätzliche Felder:

```yaml
---
title: Jazz-Night in der Freiheitshalle
date: '2025-11-25'
location: Freiheitshalle Hof
address: Kulmbacher Str. 4, 95030 Hof
coordinates:
  lat: 50.3197
  lng: 11.9168
venue:
  name: Freiheitshalle Hof
  wheelchair_accessible: true
  wheelchair_toilet: true
  parking: true
  public_transport: true
  website: https://www.freiheitshalle-hof.de
  phone: +49 9281 8150
  capacity: 1500
---
```

## Frontend-Integration

Im JavaScript kann auf Venue-Metadaten zugegriffen werden:

```javascript
// In main.js
function displayEventDetails(event) {
    let html = `<h3>${event.title}</h3>`;
    
    // Venue-Metadaten anzeigen
    if (event.venue) {
        html += `<div class="venue-info">`;
        
        if (event.venue.wheelchair_accessible) {
            html += `<span title="Rollstuhlgerecht">♿</span> `;
        }
        
        if (event.venue.parking) {
            html += `<span title="Parkplatz">🅿️</span> `;
        }
        
        if (event.venue.public_transport) {
            html += `<span title="ÖPNV">🚌</span> `;
        }
        
        html += `</div>`;
    }
    
    return html;
}
```

## Best Practices

### 1. Aliases pflegen
Füge alle Schreibvarianten als Aliases hinzu:
```csv
Theater Hof,"Stadttheater Hof,Theater,Hof Theater",...
```

### 2. Koordinaten genau erfassen
Nutze z.B. Google Maps für exakte lat/lng:
1. Rechtsklick auf Ort in Google Maps
2. "Was ist hier?" → Koordinaten kopieren
3. In venues.csv eintragen

### 3. Barrierefreiheit dokumentieren
Checke vor Ort oder kontaktiere Venue:
- Rampen/Aufzug vorhanden?
- Rollstuhl-WC verfügbar?
- Induktionsschleife für Hörgeräte?

### 4. Regelmäßig updaten
Setze `last_updated` auf aktuelles Datum bei Änderungen:
```bash
# Alle Venues älter als 6 Monate überprüfen
grep '2024-' _data/venues.csv
```

### 5. Kapazität pflegen
Wichtig für Event-Plannung:
- Theater: Sitzplatzanzahl
- Hallen: Maximalkapazität (stehend)
- Outdoor: Geschätzte Kapazität

## Troubleshooting

**Venue wird nicht gefunden:**
```python
# Test-Script:
from venue_manager import VenueManager
manager = VenueManager()

# Debug:
print(manager.find_venue("Dein Venue"))
# None → Füge Alias hinzu oder prüfe Schreibweise
```

**CSV-Fehler:**
- Achte auf Anführungszeichen bei Kommas in Feldern: `"Straße 1, Hof"`
- UTF-8 Encoding nutzen
- Keine Leerzeilen am Ende

**Koordinaten falsch:**
- Format: Dezimalgrad (nicht Grad/Minuten/Sekunden)
- Beispiel Hof: `50.3197, 11.9168`
- Nicht: `50°19'10.9"N 11°55'06.6"E`

## Erweiterungen

### Custom Fields hinzufügen
1. Spalte in venues.csv hinzufügen
2. In `venue_manager.py` → `load_venues()` verarbeiten
3. In Event-YAML ausgeben

Beispiel: `outdoor` Field:
```python
# venue_manager.py
if row.get('outdoor'):
    row['outdoor'] = row['outdoor'].lower() == 'true'

# Event-Enrichment
event_data['venue']['outdoor'] = venue.get('outdoor', False)
```

### Geocoding-API integrieren
Für automatische Koordinaten-Lookup:
```python
def geocode_address(address):
    # Nominatim, Google Maps API, etc.
    response = requests.get(f"https://nominatim.openstreetmap.org/search?q={address}&format=json")
    data = response.json()[0]
    return float(data['lat']), float(data['lon'])
```

### Venue-Bilder
Füge `image_url` Field hinzu:
```csv
name,...,image_url
Freiheitshalle Hof,...,/assets/images/venues/freiheitshalle.jpg
```

## Support

Bei Problemen oder Fragen:
1. Logs prüfen: `python scripts/venue_admin.py`
2. CSV validieren: `csvlint _data/venues.csv`
3. Test-Script: `python scripts/venue_manager.py`
