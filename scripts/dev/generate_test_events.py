#!/usr/bin/env python3
"""
Generate Lorem Ipsum Test Events
Erstellt Test-Events für lokale Entwicklung und Filter-Tests
"""

import os
import yaml
from datetime import datetime, timedelta
import random
from pathlib import Path

# Lorem Ipsum für Event-Titel (Punk-inspiriert 🤘)
TITLES = [
    "Konzert im Keller",
    "Jam Session",
    "Open Mic Night",
    "Karaoke Krawall",
    "Poetry Slam",
    "Film & Diskussion",
    "Workshop: Siebdruck",
    "Maker Monday",
    "Repair Café",
    "Soli-Party",
    "Flohmarkt",
    "Lesung & Musik",
    "Theater-Impro",
    "Ausstellung: Neue Kunst",
    "Techno im Bahnhof",
    "Punk Rock Matinee",
    "Quiz Night",
    "Yoga am Morgen",
    "Brunch & Beats",
    "Nachtwanderung",
]

# Lorem Ipsum für Venues
VENUES = [
    "Kulturzentrum",
    "Alte Fabrik",
    "Stadtbibliothek",
    "Jugendzentrum",
    "Gemeindezentrum",
    "Club Untergrund",
    "Café am Markt",
    "Werkstatt 23",
    "Mehrzweckhalle",
    "Galerie Zwischenraum",
]

# Kategorien (aus _config.yml)
CATEGORIES = [
    "Musik",
    "Kunst",
    "Theater",
    "Film",
    "Workshop",
    "Sport",
    "Politik",
    "Essen",
]

# Veranstalter
ORGANIZERS = [
    "Kulturverein Hof",
    "DIY Kollektiv",
    "Stadtjugendring",
    "Autonomes Zentrum",
    "Nachbarschaftstreff",
    "Kunst AG",
    "Open Source Stammtisch",
]

# Koordinaten (Hof Innenstadt-Nähe)
COORDS = [
    (50.3197, 11.9168),  # Rathaus
    (50.3210, 11.9185),
    (50.3180, 11.9150),
    (50.3220, 11.9200),
    (50.3160, 11.9140),
]

# Lorem Ipsum Beschreibungen
DESCRIPTIONS = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.",
]


def generate_test_events(count=10):
    """Generiert Test-Events für die nächsten 14 Tage"""
    
    # Projekt-Root finden
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    events_dir = project_root / "_events"
    
    print(f"📁 Events-Verzeichnis: {events_dir}")
    
    # Erstelle Events
    created = 0
    for i in range(count):
        # Zufälliger Zeitpunkt in den nächsten 14 Tagen
        days_ahead = random.randint(0, 14)
        hours = random.randint(10, 23)
        minutes = random.choice([0, 15, 30, 45])
        
        event_date = datetime.now() + timedelta(days=days_ahead)
        event_time = f"{hours:02d}:{minutes:02d}"
        event_datetime = event_date.replace(hour=hours, minute=minutes, second=0, microsecond=0)
        
        # Zufällige Event-Daten
        title = random.choice(TITLES)
        venue = random.choice(VENUES)
        categories = random.sample(CATEGORIES, k=random.randint(1, 3))
        organizer = random.choice(ORGANIZERS)
        lat, lng = random.choice(COORDS)
        description = random.choice(DESCRIPTIONS)
        
        # Dateiname: YYYY-MM-DD-lorem-ipsum-N.md
        filename = f"{event_date.strftime('%Y-%m-%d')}-lorem-ipsum-{i+1:02d}.md"
        filepath = events_dir / filename
        
        # Skip wenn schon existiert
        if filepath.exists():
            print(f"⏭️  Skip: {filename} (existiert bereits)")
            continue
        
        # Frontmatter erstellen
        frontmatter = {
            "layout": "event",
            "title": f"{title} #{i+1}",
            "date": event_datetime.strftime("%Y-%m-%d %H:%M:%S %z"),
            "categories": categories,
            "venue": venue,
            "venue_address": f"{venue}, 95028 Hof",
            "organizer": organizer,
            "lat": lat,
            "lng": lng,
            "status": "Bestätigt",
            "access": "Kostenlos",
            "test_event": True,  # Markierung für Cleanup
        }
        
        # Event-Datei schreiben
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("---\n")
            yaml.dump(frontmatter, f, allow_unicode=True, sort_keys=False)
            f.write("---\n\n")
            f.write(f"# {title} #{i+1}\n\n")
            f.write(f"{description}\n\n")
            f.write("**Dies ist ein Test-Event für Entwicklungszwecke.**\n")
        
        created += 1
        print(f"✅ Erstellt: {filename}")
    
    print(f"\n🎉 {created} Test-Events erstellt!")
    print(f"💡 Tipp: Aktiviere in _config.yml → debug.show_test_events: true")
    print(f"🧹 Cleanup: scripts/dev/cleanup_test_events.py")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generiere Lorem Ipsum Test-Events")
    parser.add_argument('--count', type=int, default=10, help='Anzahl Test-Events (default: 10)')
    args = parser.parse_args()
    
    generate_test_events(args.count)


if __name__ == "__main__":
    main()
