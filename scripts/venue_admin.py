#!/usr/bin/env python3
"""
Venue Admin Tool
Interaktives CLI-Tool für Venue-Verwaltung
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from venue_manager import VenueManager
import csv


def print_menu():
    """Zeigt Hauptmenü"""
    print("\n" + "="*60)
    print("🏛️  VENUE ADMIN TOOL")
    print("="*60)
    print("1. Alle Venues anzeigen")
    print("2. Venue suchen")
    print("3. Neuen Venue hinzufügen")
    print("4. Fehlende Venues aus Events finden")
    print("5. Venue-Details anzeigen")
    print("0. Beenden")
    print("="*60)


def show_all_venues(manager):
    """Zeigt alle Venues"""
    print(f"\n📍 {len(manager.venues)} Venues in venues.csv:\n")
    
    for i, venue in enumerate(manager.venues, 1):
        icons = []
        if venue.get('wheelchair_accessible'):
            icons.append('♿')
        if venue.get('parking'):
            icons.append('🅿️')
        if venue.get('public_transport'):
            icons.append('🚌')
        
        icons_str = ' '.join(icons) if icons else ''
        print(f"{i:2d}. {venue['name']:<30} {icons_str}")
        
        if venue['address']:
            print(f"    📫 {venue['address']}")


def search_venue(manager):
    """Sucht Venue"""
    query = input("\n🔍 Venue-Name eingeben: ").strip()
    
    if not query:
        return
    
    venue = manager.find_venue(query)
    
    if venue:
        print(f"\n✅ Gefunden: {venue['name']}")
        show_venue_details(venue)
    else:
        print(f"\n❌ Kein Venue gefunden für: '{query}'")


def show_venue_details(venue):
    """Zeigt Venue-Details"""
    print("\n" + "-"*60)
    print(f"🏛️  {venue['name']}")
    print("-"*60)
    
    if venue['aliases']:
        print(f"📝 Aliases: {', '.join(venue['aliases'])}")
    
    if venue['address']:
        print(f"📫 Adresse: {venue['address']}")
    
    if venue.get('lat') and venue.get('lng'):
        print(f"📍 Koordinaten: {venue['lat']}, {venue['lng']}")
    
    print(f"\n♿ Rollstuhlgerecht: {'✅ Ja' if venue.get('wheelchair_accessible') else '❌ Nein'}")
    print(f"🚽 Rollstuhl-WC: {'✅ Ja' if venue.get('wheelchair_toilet') else '❌ Nein'}")
    print(f"🅿️  Parkplatz: {'✅ Ja' if venue.get('parking') else '❌ Nein'}")
    print(f"🚌 ÖPNV: {'✅ Ja' if venue.get('public_transport') else '❌ Nein'}")
    
    if venue.get('website'):
        print(f"\n🌐 Website: {venue['website']}")
    
    if venue.get('phone'):
        print(f"📞 Telefon: {venue['phone']}")
    
    if venue.get('capacity'):
        print(f"👥 Kapazität: {venue['capacity']}")
    
    if venue.get('notes'):
        print(f"\n📋 Notizen: {venue['notes']}")
    
    print(f"\n🗓️  Letzte Aktualisierung: {venue.get('last_updated', 'unbekannt')}")
    print("-"*60)


def add_venue(manager):
    """Fügt neuen Venue hinzu"""
    print("\n➕ Neuen Venue hinzufügen")
    print("-"*60)
    
    name = input("Name (Pflicht): ").strip()
    if not name:
        print("❌ Name ist Pflichtfeld!")
        return
    
    # Prüfen ob existiert
    if manager.find_venue(name):
        print(f"⚠️  Venue '{name}' existiert bereits!")
        if input("Details anzeigen? (j/n): ").lower() == 'j':
            show_venue_details(manager.find_venue(name))
        return
    
    venue_data = {'name': name}
    
    # Optional: Aliases
    aliases = input("Aliases (kommasepariert, optional): ").strip()
    if aliases:
        venue_data['aliases'] = aliases
    
    # Optional: Adresse
    address = input("Adresse (optional): ").strip()
    if address:
        venue_data['address'] = address
    
    # Optional: Koordinaten
    lat = input("Latitude (optional): ").strip()
    lng = input("Longitude (optional): ").strip()
    if lat and lng:
        try:
            venue_data['lat'] = float(lat)
            venue_data['lng'] = float(lng)
        except ValueError:
            print("⚠️  Ungültige Koordinaten - übersprungen")
    
    # Boolean-Felder
    def ask_bool(prompt):
        answer = input(f"{prompt} (j/n): ").lower()
        return 'true' if answer == 'j' else 'false'
    
    venue_data['wheelchair_accessible'] = ask_bool("♿ Rollstuhlgerecht?")
    venue_data['wheelchair_toilet'] = ask_bool("🚽 Rollstuhl-WC?")
    venue_data['parking'] = ask_bool("🅿️  Parkplatz?")
    venue_data['public_transport'] = ask_bool("🚌 ÖPNV-Anbindung?")
    
    # Optional: Website
    website = input("🌐 Website (optional): ").strip()
    if website:
        venue_data['website'] = website
    
    # Optional: Telefon
    phone = input("📞 Telefon (optional): ").strip()
    if phone:
        venue_data['phone'] = phone
    
    # Optional: Kapazität
    capacity = input("👥 Kapazität (optional): ").strip()
    if capacity:
        venue_data['capacity'] = capacity
    
    # Optional: Notizen
    notes = input("📋 Notizen (optional): ").strip()
    if notes:
        venue_data['notes'] = notes
    
    # Bestätigung
    print("\n" + "-"*60)
    print("📝 Zusammenfassung:")
    for key, value in venue_data.items():
        print(f"  {key}: {value}")
    print("-"*60)
    
    if input("\nSpeichern? (j/n): ").lower() == 'j':
        if manager.add_venue(venue_data):
            print("✅ Venue erfolgreich hinzugefügt!")
        else:
            print("❌ Fehler beim Hinzufügen!")
    else:
        print("❌ Abgebrochen")


def find_missing_from_events(manager):
    """Findet fehlende Venues aus Event-Dateien"""
    from pathlib import Path
    import yaml
    
    events_dir = Path("_events")
    
    if not events_dir.exists():
        print("❌ Kein _events Verzeichnis gefunden!")
        return
    
    print("\n🔍 Analysiere Event-Dateien...")
    
    events = []
    for event_file in events_dir.glob("*.md"):
        try:
            with open(event_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if '---' in content:
                    parts = content.split('---', 2)
                    if len(parts) >= 2:
                        event_data = yaml.safe_load(parts[1])
                        if event_data and 'location' in event_data:
                            events.append(event_data)
        except Exception as e:
            print(f"⚠️  Fehler bei {event_file.name}: {e}")
    
    if not events:
        print("❌ Keine Events gefunden!")
        return
    
    print(f"📊 {len(events)} Events analysiert")
    
    missing = manager.find_missing_venues(events)
    
    if missing:
        print(f"\n⚠️  {len(missing)} fehlende Venues:\n")
        for i, venue in enumerate(missing, 1):
            print(f"{i:2d}. {venue}")
        
        print("\n" + "-"*60)
        print("📋 CSV-Template zum Kopieren:")
        print("-"*60)
        print(manager.suggest_venue_entries(missing))
        print("-"*60)
        print("\n💡 Kopiere die Zeilen in _data/venues.csv und fülle die Daten aus.")
    else:
        print("\n✅ Alle Venues sind erfasst!")


def main():
    """Hauptprogramm"""
    manager = VenueManager()
    
    while True:
        print_menu()
        choice = input("\nAuswahl: ").strip()
        
        if choice == '0':
            print("\n👋 Auf Wiedersehen!")
            break
        elif choice == '1':
            show_all_venues(manager)
        elif choice == '2':
            search_venue(manager)
        elif choice == '3':
            add_venue(manager)
        elif choice == '4':
            find_missing_from_events(manager)
        elif choice == '5':
            show_all_venues(manager)
            try:
                num = int(input("\nVenue-Nummer: "))
                if 1 <= num <= len(manager.venues):
                    show_venue_details(manager.venues[num-1])
                else:
                    print("❌ Ungültige Nummer!")
            except ValueError:
                print("❌ Bitte Zahl eingeben!")
        else:
            print("❌ Ungültige Auswahl!")
        
        input("\n[Enter drücken zum Fortfahren]")


if __name__ == "__main__":
    main()
