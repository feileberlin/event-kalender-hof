#!/usr/bin/env python3
"""
Beispiel: Venue-System nutzen
Zeigt verschiedene Use-Cases
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from venue_manager import VenueManager


def example_1_find_venue():
    """Beispiel 1: Venue finden"""
    print("\n" + "="*60)
    print("BEISPIEL 1: Venue finden")
    print("="*60)
    
    manager = VenueManager()
    
    # Verschiedene Suchanfragen
    searches = [
        "Freiheitshalle Hof",      # Exakt
        "freiheitshalle",          # Kleinschreibung
        "Kulturzentrum",           # Alias
        "Theater",                  # Teil des Namens
        "Unbekannter Ort"          # Nicht vorhanden
    ]
    
    for search in searches:
        venue = manager.find_venue(search)
        if venue:
            print(f"✅ '{search}' → {venue['name']}")
        else:
            print(f"❌ '{search}' → nicht gefunden")


def example_2_enrich_event():
    """Beispiel 2: Event-Daten anreichern"""
    print("\n" + "="*60)
    print("BEISPIEL 2: Event-Daten anreichern")
    print("="*60)
    
    manager = VenueManager()
    
    # Event ohne Venue-Metadaten
    event = {
        'title': 'Jazz-Konzert',
        'date': '2025-11-25',
        'location': 'Freiheitshalle Hof',
        'description': 'Ein toller Abend'
    }
    
    print("\n📋 Vorher:")
    print(f"  Location: {event['location']}")
    print(f"  Koordinaten: {event.get('coordinates', 'Keine')}")
    print(f"  Venue-Info: {event.get('venue', 'Keine')}")
    
    # Anreichern
    enriched = manager.enrich_event_data(event)
    
    print("\n📋 Nachher:")
    print(f"  Location: {enriched['location']}")
    print(f"  Koordinaten: {enriched.get('coordinates', 'Keine')}")
    print(f"  Adresse: {enriched.get('address', 'Keine')}")
    
    if 'venue' in enriched:
        venue = enriched['venue']
        print(f"\n🏛️  Venue-Metadaten:")
        print(f"  • Rollstuhlgerecht: {venue['wheelchair_accessible']}")
        print(f"  • Rollstuhl-WC: {venue['wheelchair_toilet']}")
        print(f"  • Parkplatz: {venue['parking']}")
        print(f"  • ÖPNV: {venue['public_transport']}")
        print(f"  • Website: {venue['website']}")
        print(f"  • Kapazität: {venue['capacity']}")


def example_3_missing_venues():
    """Beispiel 3: Fehlende Venues finden"""
    print("\n" + "="*60)
    print("BEISPIEL 3: Fehlende Venues finden")
    print("="*60)
    
    manager = VenueManager()
    
    # Beispiel-Events
    events = [
        {'location': 'Freiheitshalle Hof'},
        {'location': 'Theater Hof'},
        {'location': 'Neuer Club XYZ'},  # Nicht in venues.csv
        {'location': 'Sportplatz ABC'},   # Nicht in venues.csv
        {'location': 'Rathaus'},          # Vorhanden
    ]
    
    missing = manager.find_missing_venues(events)
    
    print(f"\n📊 {len(events)} Events analysiert")
    print(f"⚠️  {len(missing)} fehlende Venues:")
    
    for venue in missing:
        print(f"  • {venue}")
    
    if missing:
        print("\n📝 CSV-Template:")
        print("-"*60)
        print(manager.suggest_venue_entries(missing))
        print("-"*60)


def example_4_add_venue():
    """Beispiel 4: Venue programmtisch hinzufügen"""
    print("\n" + "="*60)
    print("BEISPIEL 4: Venue programmatisch hinzufügen (DEMO)")
    print("="*60)
    
    manager = VenueManager()
    
    new_venue = {
        'name': 'Test-Venue (bitte löschen)',
        'aliases': 'Test,Demo-Venue',
        'address': 'Teststraße 1, 95028 Hof',
        'lat': '50.320',
        'lng': '11.917',
        'wheelchair_accessible': 'true',
        'wheelchair_toilet': 'false',
        'parking': 'true',
        'public_transport': 'true',
        'website': 'https://example.com',
        'phone': '+49 123 456789',
        'capacity': '100',
        'notes': 'Nur für Tests'
    }
    
    print("\n⚠️  DEMO-Modus: Venue wird NICHT gespeichert!")
    print("\nVenue-Daten:")
    for key, value in new_venue.items():
        print(f"  {key}: {value}")
    
    print("\n💡 In echter Anwendung:")
    print("   manager.add_venue(new_venue)")


def example_5_venue_details():
    """Beispiel 5: Alle Venue-Details"""
    print("\n" + "="*60)
    print("BEISPIEL 5: Alle Venue-Details")
    print("="*60)
    
    manager = VenueManager()
    
    for venue in manager.venues[:2]:  # Nur erste 2
        print(f"\n🏛️  {venue['name']}")
        print("-"*60)
        
        # Alle Felder ausgeben
        fields = [
            ('📝 Aliases', ', '.join(venue['aliases']) if venue['aliases'] else '-'),
            ('📫 Adresse', venue.get('address', '-')),
            ('📍 Koordinaten', f"{venue.get('lat', '-')}, {venue.get('lng', '-')}"),
            ('♿ Rollstuhlgerecht', '✅ Ja' if venue.get('wheelchair_accessible') else '❌ Nein'),
            ('🚽 Rollstuhl-WC', '✅ Ja' if venue.get('wheelchair_toilet') else '❌ Nein'),
            ('🅿️  Parkplatz', '✅ Ja' if venue.get('parking') else '❌ Nein'),
            ('🚌 ÖPNV', '✅ Ja' if venue.get('public_transport') else '❌ Nein'),
            ('🌐 Website', venue.get('website', '-')),
            ('📞 Telefon', venue.get('phone', '-')),
            ('👥 Kapazität', venue.get('capacity', '-')),
            ('📋 Notizen', venue.get('notes', '-')),
            ('🗓️  Update', venue.get('last_updated', '-')),
        ]
        
        for label, value in fields:
            print(f"  {label:<20} {value}")


def main():
    """Alle Beispiele ausführen"""
    print("\n" + "="*60)
    print("🎯 VENUE-SYSTEM BEISPIELE")
    print("="*60)
    
    example_1_find_venue()
    example_2_enrich_event()
    example_3_missing_venues()
    example_4_add_venue()
    example_5_venue_details()
    
    print("\n" + "="*60)
    print("✅ Alle Beispiele abgeschlossen!")
    print("="*60)
    print("\n💡 Mehr Infos: docs/VENUES.md")
    print("📋 Admin-Tool: python scripts/venue_admin.py")
    print("\n")


if __name__ == "__main__":
    main()
