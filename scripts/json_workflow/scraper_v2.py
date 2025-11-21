#!/usr/bin/env python3
"""
Scraper V2 - JSON-first Event Scraper
Schreibt Events direkt als JSON nach _data/staging/ statt Markdown nach _events/
"""

import sys
import json
import hashlib
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from bs4 import BeautifulSoup

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.schemas import Event, EventMeta, Place, Organizer, Coordinates

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
STAGING_DIR = PROJECT_ROOT / "_data" / "staging"
PLACES_DIR = PROJECT_ROOT / "_data" / "places"
ORGANIZERS_DIR = PROJECT_ROOT / "_data" / "organizers"

# Ensure directories exist
STAGING_DIR.mkdir(parents=True, exist_ok=True)


class ScraperV2:
    """JSON-first event scraper"""
    
    def __init__(self):
        self.scraped_events: List[Event] = []
        self.places_cache: Dict[str, Place] = self._load_places()
        self.organizers_cache: Dict[str, Organizer] = self._load_organizers()
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def _load_places(self) -> Dict[str, Place]:
        """Load all places from _data/places/"""
        places = {}
        if PLACES_DIR.exists():
            for json_file in PLACES_DIR.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        place = Place.from_dict(data)
                        places[place.slug] = place
                except Exception as e:
                    print(f"⚠️  Error loading place {json_file}: {e}")
        return places
    
    def _load_organizers(self) -> Dict[str, Organizer]:
        """Load all organizers from _data/organizers/"""
        organizers = {}
        if ORGANIZERS_DIR.exists():
            for json_file in ORGANIZERS_DIR.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        organizer = Organizer.from_dict(data)
                        organizers[organizer.slug] = organizer
                except Exception as e:
                    print(f"⚠️  Error loading organizer {json_file}: {e}")
        return organizers
    
    def scrape_all_sources(self):
        """Scrape all configured sources"""
        print("=" * 80)
        print("🔍 Scraper V2 - JSON-first Event Collection")
        print("=" * 80)
        print(f"Session ID: {self.session_id}")
        print(f"Places loaded: {len(self.places_cache)}")
        print(f"Organizers loaded: {len(self.organizers_cache)}")
        print()
        
        # Example scrapers - adapt to actual sources
        self.scrape_freiheitshalle()
        self.scrape_stadt_hof()
        
        # Save results
        self._save_to_staging()
        
        print()
        print("=" * 80)
        print(f"✅ Scraping complete: {len(self.scraped_events)} events collected")
        print(f"📁 Saved to: {STAGING_DIR}/events-{self.session_id}.json")
        print("=" * 80)
        print()
        print("Next steps:")
        print("  1. Review events: python scripts/json_workflow/reviewer.py")
        print("  2. Apply decisions: python scripts/json_workflow/merger.py")
    
    def scrape_freiheitshalle(self):
        """Scrape Freiheitshalle Hof events"""
        print("-" * 80)
        print("📡 Source: Freiheitshalle Hof")
        print("-" * 80)
        
        url = "https://www.freiheitshalle-hof.de/veranstaltungen"
        
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; krawl.ist/2.0; +https://krawl.ist)'
            })
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Example parsing - adapt to actual HTML structure
            event_elements = soup.find_all('div', class_='event-item')
            print(f"  Found {len(event_elements)} event elements")
            
            for elem in event_elements[:5]:  # Limit for testing
                try:
                    title = elem.find('h3', class_='event-title')
                    date_elem = elem.find('span', class_='event-date')
                    
                    if not title or not date_elem:
                        continue
                    
                    event = self._parse_event(
                        title=title.text.strip(),
                        date_str=date_elem.text.strip(),
                        place_slug='freiheitshalle-hof',
                        organizer_slug='freiheitshalle',
                        source_url=url,
                        raw_html=str(elem)
                    )
                    
                    if event:
                        self.scraped_events.append(event)
                        print(f"  ✓ {event.title} ({event.start_date})")
                    
                except Exception as e:
                    print(f"  ✗ Error parsing event: {e}")
            
        except Exception as e:
            print(f"  ✗ Error scraping Freiheitshalle: {e}")
    
    def scrape_stadt_hof(self):
        """Scrape Stadt Hof events"""
        print("-" * 80)
        print("📡 Source: Stadt Hof")
        print("-" * 80)
        
        # Placeholder - implement actual scraping logic
        print("  ⚠️  Not implemented yet")
    
    def _parse_event(
        self,
        title: str,
        date_str: str,
        place_slug: str,
        organizer_slug: str,
        source_url: str,
        raw_html: str = None,
        description: str = None,
        price: str = None,
        image_url: str = None
    ) -> Optional[Event]:
        """Parse and create Event object"""
        
        try:
            # Parse date (adapt to actual format)
            start_date, start_time = self._parse_datetime(date_str)
            
            if not start_date:
                return None
            
            # Create event
            event = Event(
                title=title,
                start_date=start_date,
                start_time=start_time,
                end_date=None,  # Could be parsed if available
                end_time=None,
                place=place_slug,
                organizers=[organizer_slug] if organizer_slug else [],
                categories=[],  # Could be extracted from content
                tags=[],
                description=description or "",
                price=price,
                ticket_url=None,
                registration_required=False,
                registration_url=None,
                image_url=image_url,
                accessibility_notes=None,
                language="de",
                status="scheduled",
                meta=EventMeta(
                    scraped_at=datetime.now().isoformat(),
                    scraper_version="2.0",
                    confidence=0.8,  # Adjust based on data completeness
                    needs_review=True,  # Always review scraped events
                    source_url=source_url,
                    raw_data={"html": raw_html} if raw_html else None
                )
            )
            
            # Generate ID
            event_id = event.generate_id()
            
            return event
            
        except Exception as e:
            print(f"  ✗ Error creating event: {e}")
            return None
    
    def _parse_datetime(self, date_str: str) -> tuple[str, Optional[str]]:
        """Parse date string to ISO date and optional time
        
        Returns: (date_str, time_str or None)
        """
        # Example patterns - adapt to actual formats
        patterns = [
            (r'(\d{1,2})\.(\d{1,2})\.(\d{4})\s+(\d{1,2}):(\d{2})', '%d.%m.%Y %H:%M'),
            (r'(\d{1,2})\.(\d{1,2})\.(\d{4})', '%d.%m.%Y'),
            (r'(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2})', '%Y-%m-%d %H:%M'),
            (r'(\d{4})-(\d{2})-(\d{2})', '%Y-%m-%d'),
        ]
        
        import re
        for pattern, fmt in patterns:
            match = re.search(pattern, date_str)
            if match:
                try:
                    dt = datetime.strptime(match.group(0), fmt)
                    date = dt.date().isoformat()
                    time = dt.time().strftime('%H:%M') if '%H' in fmt else None
                    return date, time
                except ValueError:
                    continue
        
        return None, None
    
    def _save_to_staging(self):
        """Save scraped events to staging directory"""
        if not self.scraped_events:
            print("⚠️  No events to save")
            return
        
        # Create staging file
        staging_file = STAGING_DIR / f"events-{self.session_id}.json"
        
        data = {
            "version": "2.0",
            "scraped_at": datetime.now().isoformat(),
            "session_id": self.session_id,
            "events": [event.to_dict() for event in self.scraped_events],
            "meta": {
                "total_events": len(self.scraped_events),
                "scraper_version": "2.0",
                "places_available": list(self.places_cache.keys()),
                "organizers_available": list(self.organizers_cache.keys())
            }
        }
        
        with open(staging_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n📝 Saved {len(self.scraped_events)} events to {staging_file.name}")


def main():
    """Main scraper entry point"""
    scraper = ScraperV2()
    scraper.scrape_all_sources()


if __name__ == '__main__':
    main()
