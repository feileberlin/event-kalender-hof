#!/usr/bin/env python3
"""
Event Scraper für Hof an der Saale
Sammelt Events von verschiedenen Quellen und erstellt YAML-Dateien
"""

import os
import re
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import yaml

# Konfiguration
EVENTS_DIR = Path("_events")
SOURCES = [
    {
        "name": "Stadt Hof",
        "url": "https://www.hof.de/hof/hof_deu/leben/veranstaltungen.html",
        "type": "html"
    },
    {
        "name": "Freiheitshalle Hof",
        "url": "https://www.freiheitshalle-hof.de/veranstaltungen/",
        "type": "html"
    },
    {
        "name": "Galeriehaus Hof (Fb)",
        "url": "https://www.facebook.com/GaleriehausHof/",
        "type": "html"
    },
      {
        "name": "Vanishing Walls (Fb)",
        "url": "https://www.facebook.com/people/Vanishing-Walls/100093518893300/#",
        "type": "html"
    },
    {
        "name": "Punkrock in Hof (Fb)",
        "url": "https://www.facebook.com/people/Punk-in-Hof/100090512583516/",
        "type": "html"
    },
    # Weitere Quellen können hier hinzugefügt werden
]

# Zentrum Hof (Rathaus)
DEFAULT_COORDINATES = {
    "lat": 50.3197,
    "lng": 11.9168
}


class EventScraper:
    def __init__(self):
        self.events = []
        self.existing_hashes = self.load_existing_hashes()
    
    def load_existing_hashes(self):
        """Lädt bereits vorhandene Event-Hashes um Duplikate zu vermeiden"""
        hashes = set()
        if EVENTS_DIR.exists():
            for file_path in EVENTS_DIR.glob("*.md"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'event_hash:' in content:
                            hash_match = re.search(r'event_hash:\s*(\w+)', content)
                            if hash_match:
                                hashes.add(hash_match.group(1))
                except Exception as e:
                    print(f"Fehler beim Lesen von {file_path}: {e}")
        return hashes
    
    def generate_event_hash(self, title, date, time, location):
        """Generiert einen eindeutigen Hash für ein Event"""
        hash_string = f"{title}{date}{time}{location}".lower()
        return hashlib.md5(hash_string.encode()).hexdigest()[:12]
    
    def scrape_stadt_hof(self, url):
        """Scrapt Events von der Stadt Hof Website"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Beispiel-Parsing (muss an tatsächliche HTML-Struktur angepasst werden)
            events = soup.find_all('div', class_='event-item')
            
            for event in events[:10]:  # Limitierung auf 10 Events
                try:
                    title = event.find('h3').text.strip() if event.find('h3') else 'Unbekanntes Event'
                    date_text = event.find('span', class_='date').text.strip() if event.find('span', class_='date') else None
                    location = event.find('span', class_='location').text.strip() if event.find('span', class_='location') else 'Hof an der Saale'
                    description = event.find('p').text.strip() if event.find('p') else ''
                    
                    # Datum parsen (anpassen an Format)
                    event_date, event_time = self.parse_date(date_text)
                    
                    if event_date:
                        event_hash = self.generate_event_hash(title, str(event_date), event_time, location)
                        
                        if event_hash not in self.existing_hashes:
                            self.events.append({
                                'title': title,
                                'date': event_date,
                                'start_time': event_time,
                                'location': location,
                                'description': description,
                                'source': 'Stadt Hof',
                                'source_url': url,
                                'event_hash': event_hash,
                                'status': 'Entwurf'
                            })
                except Exception as e:
                    print(f"Fehler beim Parsen eines Events: {e}")
                    continue
        
        except Exception as e:
            print(f"Fehler beim Scrapen von {url}: {e}")
    
    def parse_date(self, date_text):
        """Versucht, Datum und Zeit aus Text zu extrahieren"""
        if not date_text:
            return None, "20:00"
        
        # Verschiedene Datumsformate probieren
        formats = [
            "%d.%m.%Y %H:%M",
            "%d.%m.%Y",
            "%d. %B %Y",
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_text, fmt)
                return dt.date(), dt.strftime("%H:%M") if "%H:%M" in fmt else "20:00"
            except ValueError:
                continue
        
        # Relative Datumsangaben
        if "heute" in date_text.lower():
            return datetime.now().date(), "20:00"
        elif "morgen" in date_text.lower():
            return (datetime.now() + timedelta(days=1)).date(), "20:00"
        
        return None, "20:00"
    
    def geocode_location(self, location):
        """Versucht, Koordinaten für einen Ort zu finden (vereinfacht)"""
        # In einer echten Implementierung würde hier eine Geocoding-API verwendet
        # Für Hof an der Saale verwenden wir vorläufig Standard-Koordinaten
        return DEFAULT_COORDINATES
    
    def create_ai_enhanced_description(self, event_data):
        """
        Placeholder für KI-gestützte Beschreibungserweiterung
        Könnte OpenAI API, Claude API oder lokales LLM nutzen
        """
        # TODO: Integration mit KI-Service
        return event_data.get('description', 'Keine Beschreibung verfügbar.')
    
    def save_events(self):
        """Speichert gescrapte Events als Markdown-Dateien"""
        EVENTS_DIR.mkdir(exist_ok=True)
        
        for event in self.events:
            # Dateiname generieren
            date_str = event['date'].strftime("%Y-%m-%d")
            title_slug = re.sub(r'[^\w\s-]', '', event['title'].lower())
            title_slug = re.sub(r'[-\s]+', '-', title_slug)[:50]
            filename = f"{date_str}-{title_slug}.md"
            filepath = EVENTS_DIR / filename
            
            # Event-Daten vorbereiten
            event_data = {
                'title': event['title'],
                'date': event['date'].strftime("%Y-%m-%d"),
                'start_time': event['start_time'],
                'end_time': '',
                'location': event['location'],
                'address': event.get('address', ''),
                'coordinates': self.geocode_location(event['location']),
                'category': self.guess_category(event['title'], event.get('description', '')),
                'tags': self.extract_tags(event['title'], event.get('description', '')),
                'description': event.get('description', ''),
                'url': event.get('source_url', ''),
                'image': '',
                'status': 'Entwurf',
                'source': event['source'],
                'event_hash': event['event_hash']
            }
            
            # KI-gestützte Beschreibung (optional)
            # event_data['description'] = self.create_ai_enhanced_description(event_data)
            
            # YAML Front Matter
            front_matter = yaml.dump(event_data, allow_unicode=True, sort_keys=False)
            
            # Markdown-Inhalt
            content = f"""---
{front_matter}---

{event_data['description']}

## Details

Dieses Event wurde automatisch erfasst und wartet auf Überprüfung durch einen Administrator.

**Quelle:** {event['source']}
"""
            
            # Datei schreiben
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ Erstellt: {filename}")
            except Exception as e:
                print(f"✗ Fehler beim Speichern von {filename}: {e}")
    
    def guess_category(self, title, description):
        """Rät die Event-Kategorie basierend auf Keywords"""
        text = f"{title} {description}".lower()
        
        categories = {
            'Musik': ['konzert', 'musik', 'band', 'festival', 'sänger', 'orchester'],
            'Theater': ['theater', 'schauspiel', 'bühne', 'drama', 'komödie'],
            'Sport': ['sport', 'fußball', 'lauf', 'turnier', 'wettkampf'],
            'Kultur': ['ausstellung', 'museum', 'kunst', 'kultur', 'lesung'],
            'Markt': ['markt', 'flohmarkt', 'wochenmarkt', 'verkauf'],
            'Fest': ['fest', 'feier', 'party', 'volksfest', 'stadtfest']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'Sonstiges'
    
    def extract_tags(self, title, description):
        """Extrahiert relevante Tags"""
        text = f"{title} {description}".lower()
        tags = []
        
        tag_keywords = {
            'Live-Musik': ['live', 'konzert', 'auftritt'],
            'Outdoor': ['outdoor', 'draußen', 'freien', 'open air'],
            'Indoor': ['indoor', 'halle', 'saal'],
            'Familie': ['familie', 'kinder', 'familienfreundlich'],
            'Kostenlos': ['kostenlos', 'frei', 'gratis', 'eintritt frei']
        }
        
        for tag, keywords in tag_keywords.items():
            if any(keyword in text for keyword in keywords):
                tags.append(tag)
        
        return tags[:5]  # Maximal 5 Tags
    
    def run(self):
        """Führt den kompletten Scraping-Prozess aus"""
        print("🔍 Starte Event-Scraping für Hof an der Saale...")
        print(f"📅 Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Beispiel-Events generieren (für Demonstration)
        self.generate_sample_events()
        
        # TODO: Uncomment für echtes Scraping
        # for source in SOURCES:
        #     print(f"Scraping: {source['name']}...")
        #     if source['type'] == 'html':
        #         self.scrape_stadt_hof(source['url'])
        
        print(f"\n✅ {len(self.events)} neue Events gefunden")
        
        if self.events:
            self.save_events()
            print(f"\n💾 Events gespeichert in {EVENTS_DIR}")
        else:
            print("\nℹ️ Keine neuen Events zum Speichern")
    
    def generate_sample_events(self):
        """Generiert Beispiel-Events für Testzwecke"""
        sample_events = [
            {
                'title': 'Weihnachtsmarkt Hof',
                'date': datetime(2025, 12, 15).date(),
                'start_time': '14:00',
                'location': 'Altstadt Hof',
                'description': 'Traditioneller Weihnachtsmarkt mit Glühwein, Bratwurst und Kunsthandwerk.',
                'source': 'Beispiel-Generator',
                'source_url': 'https://www.hof.de',
            },
            {
                'title': 'Jazz-Night in der Freiheitshalle',
                'date': datetime(2025, 11, 25).date(),
                'start_time': '20:00',
                'location': 'Freiheitshalle Hof',
                'description': 'Ein Abend voller Jazz mit regionalen und internationalen Künstlern.',
                'source': 'Beispiel-Generator',
                'source_url': 'https://www.freiheitshalle-hof.de',
            }
        ]
        
        for event in sample_events:
            event_hash = self.generate_event_hash(
                event['title'], 
                str(event['date']), 
                event['start_time'], 
                event['location']
            )
            
            if event_hash not in self.existing_hashes:
                event['event_hash'] = event_hash
                event['status'] = 'Entwurf'
                self.events.append(event)


def main():
    scraper = EventScraper()
    scraper.run()


if __name__ == "__main__":
    main()
