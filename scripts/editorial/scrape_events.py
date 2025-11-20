#!/usr/bin/env python3
"""
Event Scraper für Hof an der Saale
Sammelt Events von verschiedenen Quellen und erstellt YAML-Dateien
"""

import os
import re
import json
import csv
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import yaml

# Venue Manager importieren
from venue_manager import VenueManager

# Konfiguration
PROJECT_ROOT = Path(__file__).parent.parent.parent
EVENTS_DIR = PROJECT_ROOT / "_events"
LOGS_DIR = PROJECT_ROOT / "_events" / "_logs"
SOURCES_CSV = PROJECT_ROOT / "_data" / "sources.csv"

def load_sources():
    """Lädt Event-Quellen aus CSV-Datei"""
    sources = []
    if SOURCES_CSV.exists():
        with open(SOURCES_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['active'].lower() == 'true':
                    sources.append({
                        'name': row['name'],
                        'url': row['url'],
                        'type': row['type'],
                        'notes': row.get('notes', '')
                    })
    return sources

SOURCES = load_sources()

# Zentrum Hof (Rathaus)
DEFAULT_COORDINATES = {
    "lat": 50.3197,
    "lng": 11.9168
}


class ScrapingLogger:
    """Logger für detaillierte Scraping-Protokolle"""
    
    def __init__(self):
        # Stelle sicher, dass Log-Verzeichnis existiert
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Timestamp für Dateinamen
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        self.log_file = LOGS_DIR / f"{timestamp}-scraping.log"
        
        # Logging-Daten
        self.logs = []
        self.start_time = datetime.now()
        
        self.log("="*80)
        self.log(f"SCRAPING SESSION GESTARTET: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.log("="*80)
        self.log("")
    
    def log(self, message, level="INFO"):
        """Fügt Log-Eintrag hinzu"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
    
    def log_source(self, source_name, source_url):
        """Loggt Start einer Quelle"""
        self.log("")
        self.log("-"*80)
        self.log(f"📡 QUELLE: {source_name}")
        self.log(f"🔗 URL: {source_url}")
        self.log("-"*80)
    
    def log_event_found(self, title, date, time, location):
        """Loggt ein gefundenes Event"""
        self.log(f"🔍 Event gefunden: '{title}'")
        self.log(f"   📅 Datum: {date} | ⏰ Zeit: {time}")
        self.log(f"   📍 Ort: {location}")
    
    def log_event_duplicate(self, title, event_hash):
        """Loggt ein doppeltes Event"""
        self.log(f"⚠️  Event übersprungen (Duplikat): '{title}' (Hash: {event_hash})", "WARN")
    
    def log_event_created(self, filename, title):
        """Loggt Erstellung einer Event-Datei"""
        self.log(f"✅ Event-Datei erstellt: {filename}")
        self.log(f"   📝 Titel: '{title}'")
    
    def log_venue_enrichment(self, location, venue_found=True, venue_data=None):
        """Loggt Venue-Anreicherung"""
        if venue_found and venue_data:
            self.log(f"🏛️  Venue gefunden für '{location}':")
            self.log(f"   ✓ Kanonischer Name: {venue_data.get('venue_name', 'N/A')}")
            self.log(f"   ✓ Adresse: {venue_data.get('address', 'N/A')}")
            self.log(f"   ✓ Koordinaten: {venue_data.get('latitude', 'N/A')}, {venue_data.get('longitude', 'N/A')}")
            if venue_data.get('wheelchair_accessible'):
                self.log(f"   ✓ Barrierefrei: Ja")
        else:
            self.log(f"⚠️  Keine Venue-Daten für '{location}' gefunden", "WARN")
    
    def log_category_guess(self, title, category):
        """Loggt automatische Kategorie-Zuordnung"""
        self.log(f"🏷️  Kategorie ermittelt: '{category}' (aus Titel: '{title}')")
    
    def log_tags_extracted(self, tags):
        """Loggt extrahierte Tags"""
        if tags:
            self.log(f"🏷️  Tags extrahiert: {', '.join(tags)}")
    
    def log_recurring_detected(self, title, recurring_info):
        """Loggt erkannte wiederkehrende Events"""
        self.log(f"🔄 Wiederkehrendes Event erkannt: '{title}'")
        if recurring_info.get('pattern'):
            pattern = recurring_info['pattern']
            self.log(f"   ✓ Muster: {pattern}")
        if recurring_info.get('frequency'):
            self.log(f"   ✓ Frequenz: {recurring_info['frequency']}")
        if recurring_info.get('by_day'):
            days_map = {'MO': 'Montag', 'TU': 'Dienstag', 'WE': 'Mittwoch', 
                       'TH': 'Donnerstag', 'FR': 'Freitag', 'SA': 'Samstag', 'SU': 'Sonntag'}
            days = [days_map.get(d, d) for d in recurring_info['by_day']]
            self.log(f"   ✓ Wochentage: {', '.join(days)}")
        if recurring_info.get('confidence'):
            self.log(f"   ✓ Konfidenz: {recurring_info['confidence']:.0%}")
        if recurring_info.get('source'):
            self.log(f"   ✓ Quelle: {recurring_info['source']}")
    
    def log_error(self, error_message, context=""):
        """Loggt einen Fehler"""
        self.log(f"❌ FEHLER: {error_message}", "ERROR")
        if context:
            self.log(f"   Kontext: {context}", "ERROR")
    
    def log_summary(self, total_found, total_created, total_duplicates, missing_venues):
        """Loggt Zusammenfassung am Ende"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        self.log("")
        self.log("="*80)
        self.log("📊 SCRAPING SESSION ABGESCHLOSSEN")
        self.log("="*80)
        self.log(f"⏱️  Dauer: {duration.total_seconds():.2f} Sekunden")
        self.log(f"🔍 Events gefunden: {total_found}")
        self.log(f"✅ Events erstellt: {total_created}")
        self.log(f"⚠️  Duplikate übersprungen: {total_duplicates}")
        
        if missing_venues:
            self.log("")
            self.log(f"🏛️  Fehlende Venues ({len(missing_venues)}):")
            for venue in missing_venues:
                self.log(f"   • {venue}")
        else:
            self.log("✅ Alle Venues in venues.csv vorhanden")
        
        self.log("")
        self.log(f"📄 Log gespeichert: {self.log_file}")
        self.log("="*80)
    
    def save(self):
        """Speichert Log-Datei"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.logs))
            return str(self.log_file)
        except Exception as e:
            print(f"Fehler beim Speichern der Log-Datei: {e}")
            return None


class EventScraper:
    def __init__(self):
        self.events = []
        self.existing_hashes = self.load_existing_hashes()
        self.venue_manager = VenueManager()
        self.logger = ScrapingLogger()
        self.duplicates_count = 0
        
        self.logger.log(f"📍 Venue Manager geladen: {len(self.venue_manager.venues)} Venues")
    
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
        self.logger.log_source("Stadt Hof", url)
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Beispiel-Parsing (muss an tatsächliche HTML-Struktur angepasst werden)
            events = soup.find_all('div', class_='event-item')
            self.logger.log(f"📄 HTML geparst: {len(events)} Event-Elemente gefunden")
            
            for event in events[:10]:  # Limitierung auf 10 Events
                try:
                    title = event.find('h3').text.strip() if event.find('h3') else 'Unbekanntes Event'
                    date_text = event.find('span', class_='date').text.strip() if event.find('span', class_='date') else None
                    location = event.find('span', class_='location').text.strip() if event.find('span', class_='location') else 'Hof an der Saale'
                    description = event.find('p').text.strip() if event.find('p') else ''
                    
                    # Datum parsen (anpassen an Format)
                    event_date, event_time = self.parse_date(date_text)
                    
                    if event_date:
                        self.logger.log_event_found(title, event_date, event_time, location)
                        event_hash = self.generate_event_hash(title, str(event_date), event_time, location)
                        
                        if event_hash not in self.existing_hashes:
                            event_data = {
                                'title': title,
                                'date': event_date,
                                'start_time': event_time,
                                'location': location,
                                'description': description,
                                'source': 'Stadt Hof',
                                'source_url': url,
                                'event_hash': event_hash,
                                'status': 'Entwurf'
                            }
                            
                            # Prüfe auf wiederkehrende Events
                            try:
                                from date_enhancer import DateEnhancer
                                enhancer = DateEnhancer()
                                recurring_result = enhancer.detect_recurring_pattern(title, description)
                                
                                if recurring_result.get('is_recurring'):
                                    recurring_info = {
                                        'pattern': recurring_result.get('keyword', ''),
                                        'frequency': recurring_result.get('pattern', ''),
                                        'by_day': recurring_result.get('by_day', []),
                                        'confidence': recurring_result.get('confidence', 0),
                                        'source': 'Automatische Erkennung (Titel/Beschreibung)'
                                    }
                                    self.logger.log_recurring_detected(title, recurring_info)
                                    
                                    # Füge recurring-Config hinzu
                                    event_data['recurring'] = {
                                        'enabled': True,
                                        'frequency': recurring_result.get('pattern', 'weekly'),
                                        'interval': 1,
                                        'by_day': recurring_result.get('by_day', []),
                                        'start_date': str(event_date),
                                        'end_date': None,
                                        'exceptions': []
                                    }
                            except ImportError:
                                pass  # date_enhancer nicht verfügbar
                            except Exception as e:
                                self.logger.log_error(f"Recurring-Detection fehlgeschlagen: {e}", title)
                            
                            # Venue-Daten anreichern
                            enriched_data = self.venue_manager.enrich_event_data(event_data)
                            if enriched_data.get('venue_name'):
                                self.logger.log_venue_enrichment(location, True, enriched_data)
                            else:
                                self.logger.log_venue_enrichment(location, False)
                            
                            self.events.append(enriched_data)
                        else:
                            self.logger.log_event_duplicate(title, event_hash)
                            self.duplicates_count += 1
                except Exception as e:
                    self.logger.log_error(str(e), f"Event: {title if 'title' in locals() else 'unbekannt'}")
                    continue
        
        except Exception as e:
            self.logger.log_error(str(e), f"Scraping von {url}")
    
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
        
        self.logger.log("")
        self.logger.log("-"*80)
        self.logger.log(f"💾 SPEICHERE {len(self.events)} EVENTS")
        self.logger.log("-"*80)
        
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
                'coordinates': event.get('coordinates', self.geocode_location(event['location'])),
                'category': self.guess_category(event['title'], event.get('description', '')),
                'tags': self.extract_tags(event['title'], event.get('description', '')),
                'description': event.get('description', ''),
                'url': event.get('source_url', ''),
                'image': '',
                'status': 'Entwurf',
                'source': event['source'],
                'event_hash': event['event_hash']
            }
            
            # Venue-Metadaten hinzufügen (falls vorhanden)
            if 'venue' in event:
                event_data['venue'] = event['venue']
            
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
                self.logger.log_event_created(filename, event_data['title'])
            except Exception as e:
                self.logger.log_error(f"Fehler beim Speichern von {filename}: {e}")
    
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
                self.logger.log_category_guess(title, category)
                return category
        
        self.logger.log_category_guess(title, 'Sonstiges')
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
        
        tags = tags[:5]  # Maximal 5 Tags
        if tags:
            self.logger.log_tags_extracted(tags)
        return tags
    
    def run(self):
        """Führt den kompletten Scraping-Prozess aus"""
        self.logger.log("🔍 Starte Event-Scraping für Hof an der Saale...")
        self.logger.log(f"📅 Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Beispiel-Events generieren (für Demonstration)
        self.generate_sample_events()
        
        # TODO: Uncomment für echtes Scraping
        # for source in SOURCES:
        #     if source['type'] == 'html':
        #         self.scrape_stadt_hof(source['url'])
        
        self.logger.log("")
        self.logger.log(f"✅ {len(self.events)} neue Events gefunden")
        
        if self.events:
            self.save_events()
            self.logger.log("")
            self.logger.log(f"💾 Events gespeichert in {EVENTS_DIR}")
        else:
            self.logger.log("")
            self.logger.log("ℹ️  Keine neuen Events zum Speichern")
    
    def generate_sample_events(self):
        """Generiert Beispiel-Events für Testzwecke"""
        self.logger.log_source("Beispiel-Generator", "internal://sample-events")
        
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
            self.logger.log_event_found(
                event['title'],
                event['date'],
                event['start_time'],
                event['location']
            )
            
            event_hash = self.generate_event_hash(
                event['title'], 
                str(event['date']), 
                event['start_time'], 
                event['location']
            )
            
            if event_hash not in self.existing_hashes:
                event['event_hash'] = event_hash
                event['status'] = 'Entwurf'
                
                # Prüfe auf wiederkehrende Events
                try:
                    from date_enhancer import DateEnhancer
                    enhancer = DateEnhancer()
                    recurring_result = enhancer.detect_recurring_pattern(event['title'], event['description'])
                    
                    if recurring_result.get('is_recurring'):
                        recurring_info = {
                            'pattern': recurring_result.get('keyword', ''),
                            'frequency': recurring_result.get('pattern', ''),
                            'by_day': recurring_result.get('by_day', []),
                            'confidence': recurring_result.get('confidence', 0),
                            'source': 'Automatische Erkennung (Titel/Beschreibung)'
                        }
                        self.logger.log_recurring_detected(event['title'], recurring_info)
                        
                        # Füge recurring-Config hinzu
                        event['recurring'] = {
                            'enabled': True,
                            'frequency': recurring_result.get('pattern', 'weekly'),
                            'interval': 1,
                            'by_day': recurring_result.get('by_day', []),
                            'start_date': str(event['date']),
                            'end_date': None,
                            'exceptions': []
                        }
                except ImportError:
                    pass  # date_enhancer nicht verfügbar
                except Exception as e:
                    self.logger.log_error(f"Recurring-Detection fehlgeschlagen: {e}", event['title'])
                
                self.events.append(event)
            else:
                self.logger.log_event_duplicate(event['title'], event_hash)
                self.duplicates_count += 1


def main():
    """
    Haupt-Scraping-Workflow:
    1. Bereinigung: Alte Events archivieren (mit Recurring-Scan)
    2. Scraping: Neue Events von Quellen sammeln
    3. Recurring: Fehlende Instanzen generieren
    4. Report: Statistik und fehlende Venues
    """
    
    # SCHRITT 1: BEREINIGUNG & ARCHIVIERUNG
    print("\n" + "="*80)
    print("🧹 SCHRITT 1: BEREINIGUNG & ARCHIVIERUNG")
    print("="*80)
    
    try:
        from archive_old_events import EventArchiver
        archiver = EventArchiver(days_threshold=30, scan_recurring=True)
        # Dry-run um zu sehen was passieren würde
        # Für automatisches Archivieren: dry_run=False setzen
        archiver.run(dry_run=True, interactive=False)
    except ImportError:
        print("⚠️  Archivierung übersprungen (Modul nicht gefunden)")
    except Exception as e:
        print(f"⚠️  Fehler bei Archivierung: {e}")
    
    # SCHRITT 2: SCRAPING
    print("\n" + "="*80)
    print("🔍 SCHRITT 2: EVENT-SCRAPING")
    print("="*80)
    
    scraper = EventScraper()
    scraper.run()
    
    # Report: Fehlende Venues
    missing_venues = scraper.venue_manager.find_missing_venues(scraper.events)
    
    # Log-Zusammenfassung
    scraper.logger.log_summary(
        total_found=len(scraper.events) + scraper.duplicates_count,
        total_created=len(scraper.events),
        total_duplicates=scraper.duplicates_count,
        missing_venues=missing_venues
    )
    
    # Log-Datei speichern
    log_path = scraper.logger.save()
    
    # SCHRITT 3: RECURRING EVENTS EXPANSION
    print("\n" + "="*80)
    print("🔄 SCHRITT 3: RECURRING EVENTS EXPANSION")
    print("="*80)
    
    try:
        from recurring_expander import RecurringExpander
        expander = RecurringExpander(lookahead_months=3)
        expander.run(use_index=True)
    except ImportError:
        print("⚠️  Recurring Expansion übersprungen (Modul nicht gefunden)")
    except Exception as e:
        print(f"⚠️  Fehler bei Recurring Expansion: {e}")
    
    # SCHRITT 4: VENUE REPORT
    if missing_venues:
        print("\n" + "="*60)
        print("📋 VENUE REPORT")
        print("="*60)
        print(f"\n⚠️  Fehlende Venues ({len(missing_venues)}):")
        for venue in missing_venues:
            print(f"  • {venue}")
        
        print("\n📝 Template für _data/venues.csv:")
        print("-" * 60)
        print(scraper.venue_manager.suggest_venue_entries(missing_venues))
        print("-" * 60)
        print("\n💡 Kopiere die Zeilen oben in _data/venues.csv und fülle die Daten aus:")
        print("   - Aliases (kommasepariert)")
        print("   - Adresse")
        print("   - Koordinaten (lat, lng)")
        print("   - Barrierefreiheit (true/false)")
        print("   - Website, Telefon, Kapazität, Notizen")
        print("\n" + "="*60)


if __name__ == "__main__":
    main()
