#!/usr/bin/env python3
"""
CSV to JSON Migration Script
Migrates venues.csv, organizers.csv, and sources.csv to JSON format
"""

import csv
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.schemas import Place, Organizer, Coordinates

def load_csv(filepath):
    """Load CSV file and return list of dicts"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def slugify(text):
    """Generate URL-safe slug from text"""
    slug = text.lower().replace(' ', '-').replace('/', '-')
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')
    return slug

def migrate_venues_to_places():
    """Migrate venues.csv to individual JSON files in _data/places/"""
    venues_csv = Path('_data/venues.csv')
    places_dir = Path('_data/places')
    places_dir.mkdir(exist_ok=True)
    
    if not venues_csv.exists():
        print(f"⚠️  {venues_csv} not found, skipping venues migration")
        return
    
    venues = load_csv(venues_csv)
    print(f"📍 Migrating {len(venues)} venues to places...")
    
    migrated = 0
    for venue in venues:
        try:
            name = venue.get('name', '').strip()
            if not name:
                continue
            
            # Parse coordinates
            coords = None
            if venue.get('lat') and venue.get('lon'):
                try:
                    coords = Coordinates(
                        lat=float(venue['lat']),
                        lng=float(venue['lon'])
                    )
                except (ValueError, KeyError):
                    coords = None
            
            # Map CSV columns to Place schema
            place = Place(
                name=name,
                slug=slugify(name),
                address=venue.get('address', '').strip() or 'Unbekannt',
                coords=coords or Coordinates(lat=50.3197, lng=11.9175),  # Hof center fallback
                wheelchair_accessible=venue.get('wheelchair_accessible', '').lower() in ['true', 'yes', '1'],
                public_transport=venue.get('public_transport', '').lower() in ['true', 'yes', '1'],
                capacity=int(venue['capacity']) if venue.get('capacity', '').strip() else None,
                website=venue.get('url', '').strip() or None,
                phone=venue.get('phone', '').strip() or None
            )
            
            # Generate filename from slug
            filepath = places_dir / f"{place.slug}.json"
            
            # Write JSON file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(place.to_dict(), f, ensure_ascii=False, indent=2)
            
            migrated += 1
            print(f"  ✓ {place.name} → {filepath.name}")
            
        except Exception as e:
            print(f"  ✗ Error migrating venue {venue.get('name', 'unknown')}: {e}")
    
    print(f"✅ Migrated {migrated}/{len(venues)} venues\n")

def migrate_organizers_and_sources():
    """Migrate organizers.csv and sources.csv to individual JSON files in _data/organizers/"""
    organizers_csv = Path('_data/organizers.csv')
    sources_csv = Path('_data/sources.csv')
    organizers_dir = Path('_data/organizers')
    organizers_dir.mkdir(exist_ok=True)
    
    migrated = 0
    
    # Migrate organizers.csv
    if organizers_csv.exists():
        organizers = load_csv(organizers_csv)
        print(f"👥 Migrating {len(organizers)} organizers...")
        
        for org in organizers:
            try:
                name = org.get('name', '').strip()
                if not name:
                    continue
                
                organizer = Organizer(
                    name=name,
                    slug=slugify(name),
                    website=org.get('url', '').strip() or None,
                    email=org.get('email', '').strip() or None,
                    phone=org.get('phone', '').strip() or None
                )
                
                filepath = organizers_dir / f"{organizer.slug}.json"
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(organizer.to_dict(), f, ensure_ascii=False, indent=2)
                
                migrated += 1
                print(f"  ✓ {organizer.name} → {filepath.name}")
                
            except Exception as e:
                print(f"  ✗ Error migrating organizer {org.get('name', 'unknown')}: {e}")
        
        print(f"✅ Migrated {migrated}/{len(organizers)} organizers\n")
    else:
        print(f"⚠️  {organizers_csv} not found, skipping organizers migration\n")
    
    # Migrate sources.csv (treated as organizers/scrapers)
    if sources_csv.exists():
        sources = load_csv(sources_csv)
        print(f"🔍 Migrating {len(sources)} sources as organizers...")
        
        source_count = 0
        for source in sources:
            try:
                name = source.get('name', '').strip()
                if not name:
                    continue
                
                # Sources are essentially organizers that provide event data
                organizer = Organizer(
                    name=name,
                    slug=f"source-{slugify(name)}",
                    website=source.get('url', '').strip() or None,
                    email=source.get('contact_email', '').strip() or None,
                    verified_sources=[source.get('url', '').strip()] if source.get('url', '').strip() else []
                )
                
                filepath = organizers_dir / f"{organizer.slug}.json"
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(organizer.to_dict(), f, ensure_ascii=False, indent=2)
                
                source_count += 1
                print(f"  ✓ {organizer.name} → {filepath.name}")
                
            except Exception as e:
                print(f"  ✗ Error migrating source {source.get('name', 'unknown')}: {e}")
        
        print(f"✅ Migrated {source_count}/{len(sources)} sources\n")
    else:
        print(f"⚠️  {sources_csv} not found, skipping sources migration\n")

def create_backup():
    """Create backup of CSV files before migration"""
    backup_dir = Path('_data/csv_backup')
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for csv_file in ['venues.csv', 'organizers.csv', 'sources.csv']:
        source = Path('_data') / csv_file
        if source.exists():
            dest = backup_dir / f"{csv_file}.{timestamp}.bak"
            dest.write_bytes(source.read_bytes())
            print(f"📦 Backed up {csv_file} → {dest.name}")

def main():
    """Main migration function"""
    print("=" * 60)
    print("CSV to JSON Migration")
    print("=" * 60)
    print()
    
    # Create backup
    print("Creating backups...")
    create_backup()
    print()
    
    # Run migrations
    migrate_venues_to_places()
    migrate_organizers_and_sources()
    
    print("=" * 60)
    print("Migration Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review generated JSON files in _data/places/ and _data/organizers/")
    print("2. Run scraper V2 to populate _data/staging/")
    print("3. Use reviewer.py to review staged events")
    print("4. Use merger.py to apply approved events to _data/events.json")

if __name__ == '__main__':
    main()
