#!/usr/bin/env python3
"""
Venue Manager für Event-Kalender Hof
Verwaltet Veranstaltungsorte mit zusätzlichen Metadaten
"""

import csv
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher

PROJECT_ROOT = Path(__file__).parent.parent.parent
VENUES_CSV = PROJECT_ROOT / "_data" / "venues.csv"


class VenueManager:
    """Verwaltet Veranstaltungsorte und deren Metadaten"""
    
    def __init__(self):
        self.venues = self.load_venues()
        self.name_index = self._build_name_index()
    
    def load_venues(self) -> List[Dict]:
        """Lädt alle Venues aus CSV"""
        venues = []
        if VENUES_CSV.exists():
            with open(VENUES_CSV, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Boolean-Werte konvertieren
                    for bool_field in ['wheelchair_accessible', 'wheelchair_toilet', 'parking', 'public_transport']:
                        if row.get(bool_field):
                            row[bool_field] = row[bool_field].lower() == 'true'
                    
                    # Aliases als Liste
                    if row.get('aliases'):
                        row['aliases'] = [a.strip() for a in row['aliases'].split(',')]
                    else:
                        row['aliases'] = []
                    
                    venues.append(row)
        return venues
    
    def _build_name_index(self) -> Dict[str, Dict]:
        """Erstellt Index für schnelle Name-Lookups (inkl. Aliases)"""
        index = {}
        for venue in self.venues:
            # Hauptname
            normalized_name = self._normalize_name(venue['name'])
            index[normalized_name] = venue
            
            # Aliases
            for alias in venue['aliases']:
                normalized_alias = self._normalize_name(alias)
                index[normalized_alias] = venue
        
        return index
    
    def _normalize_name(self, name: str) -> str:
        """Normalisiert Namen für Vergleiche"""
        if not name:
            return ""
        # Kleinschreibung, Leerzeichen entfernen, Sonderzeichen normalisieren
        name = name.lower().strip()
        name = re.sub(r'\s+', ' ', name)
        name = re.sub(r'[^\w\s]', '', name)
        return name
    
    def find_venue(self, location_name: str) -> Optional[Dict]:
        """
        Findet Venue anhand des Namens (exakt oder fuzzy)
        
        Args:
            location_name: Name des Veranstaltungsortes aus Event-Daten
            
        Returns:
            Venue-Dict oder None
        """
        if not location_name:
            return None
        
        normalized = self._normalize_name(location_name)
        
        # 1. Exakter Match (inkl. Aliases)
        if normalized in self.name_index:
            return self.name_index[normalized]
        
        # 2. Fuzzy-Matching (Ähnlichkeit > 0.8)
        best_match = None
        best_score = 0.0
        
        for indexed_name, venue in self.name_index.items():
            score = SequenceMatcher(None, normalized, indexed_name).ratio()
            if score > best_score and score > 0.8:
                best_score = score
                best_match = venue
        
        return best_match
    
    def enrich_event_data(self, event_data: Dict) -> Dict:
        """
        Reichert Event-Daten mit Venue-Metadaten an
        
        Args:
            event_data: Event-Dict mit 'location' field
            
        Returns:
            Angereichertes Event-Dict
        """
        location_name = event_data.get('location', '')
        venue = self.find_venue(location_name)
        
        if venue:
            # Koordinaten überschreiben (wenn Venue bessere hat)
            if venue.get('lat') and venue.get('lng'):
                event_data['coordinates'] = {
                    'lat': float(venue['lat']),
                    'lng': float(venue['lng'])
                }
            
            # Adresse hinzufügen
            if venue.get('address') and not event_data.get('address'):
                event_data['address'] = venue['address']
            
            # Venue-Metadaten hinzufügen
            event_data['venue'] = {
                'name': venue['name'],
                'wheelchair_accessible': venue.get('wheelchair_accessible', False),
                'wheelchair_toilet': venue.get('wheelchair_toilet', False),
                'parking': venue.get('parking', False),
                'public_transport': venue.get('public_transport', False),
                'website': venue.get('website', ''),
                'phone': venue.get('phone', ''),
                'capacity': venue.get('capacity', '')
            }
            
            print(f"  ✓ Venue Match: '{location_name}' → '{venue['name']}'")
        else:
            print(f"  ⚠ Venue nicht gefunden: '{location_name}'")
        
        return event_data
    
    def add_venue(self, venue_data: Dict) -> bool:
        """
        Fügt neuen Venue zur CSV hinzu
        
        Args:
            venue_data: Dict mit Venue-Feldern
            
        Returns:
            True bei Erfolg
        """
        # Prüfen ob Venue bereits existiert
        if self.find_venue(venue_data['name']):
            print(f"Venue '{venue_data['name']}' existiert bereits")
            return False
        
        # Defaults setzen
        defaults = {
            'aliases': '',
            'address': '',
            'lat': '',
            'lng': '',
            'wheelchair_accessible': 'false',
            'wheelchair_toilet': 'false',
            'parking': 'false',
            'public_transport': 'false',
            'website': '',
            'phone': '',
            'capacity': '',
            'notes': '',
            'last_updated': datetime.now().strftime('%Y-%m-%d')
        }
        
        for key, default in defaults.items():
            if key not in venue_data:
                venue_data[key] = default
        
        # CSV aktualisieren
        with open(VENUES_CSV, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=venue_data.keys())
            writer.writerow(venue_data)
        
        # Index neu laden
        self.venues = self.load_venues()
        self.name_index = self._build_name_index()
        
        print(f"✓ Venue '{venue_data['name']}' hinzugefügt")
        return True
    
    def find_missing_venues(self, events: List[Dict]) -> List[str]:
        """
        Findet Locations aus Events, die nicht in venues.csv sind
        
        Args:
            events: Liste von Event-Dicts
            
        Returns:
            Liste von unbekannten Location-Namen
        """
        missing = set()
        
        for event in events:
            location = event.get('location', '').strip()
            if location and not self.find_venue(location):
                missing.add(location)
        
        return sorted(missing)
    
    def suggest_venue_entries(self, missing_locations: List[str]) -> str:
        """
        Generiert CSV-Zeilen für fehlende Venues (als Template)
        
        Args:
            missing_locations: Liste unbekannter Locations
            
        Returns:
            CSV-formatierter String
        """
        lines = []
        today = datetime.now().strftime('%Y-%m-%d')
        
        for location in missing_locations:
            # Basis-Template (Admin muss ausfüllen)
            line = f'"{location}","","",,,,false,false,false,false,,,,"{today}"'
            lines.append(line)
        
        return '\n'.join(lines)


def main():
    """Test-Funktion"""
    manager = VenueManager()
    
    print(f"\n📍 Geladene Venues: {len(manager.venues)}")
    for venue in manager.venues:
        print(f"  • {venue['name']}")
        if venue['aliases']:
            print(f"    Aliases: {', '.join(venue['aliases'])}")
    
    # Test: Venue-Suche
    print("\n🔍 Test: Venue-Suche")
    test_names = [
        "Freiheitshalle Hof",
        "Kulturzentrum Hof",  # Alias
        "freiheitshalle",  # Fuzzy
        "Theater",
        "Unbekannter Ort"
    ]
    
    for name in test_names:
        venue = manager.find_venue(name)
        if venue:
            print(f"  ✓ '{name}' → {venue['name']}")
        else:
            print(f"  ✗ '{name}' → nicht gefunden")


if __name__ == "__main__":
    main()
