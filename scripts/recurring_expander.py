#!/usr/bin/env python3
"""
Recurring Events Expander
Generiert automatisch Instanzen für wiederkehrende Events
"""

import json
import yaml
import re
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Set
from collections import defaultdict

EVENTS_DIR = Path("_events")
HISTORY_DIR = Path("_events/_history")
INDEX_FILE = Path("_data/recurring_index.json")

WEEKDAY_MAP = {
    'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3,
    'FR': 4, 'SA': 5, 'SU': 6
}


class RecurringExpander:
    """
    Verwaltet wiederkehrende Events und generiert fehlende Instanzen
    
    Workflow:
    1. Scannt _events/ und Archive nach recurring-Events
    2. Pflegt Index-Datei mit allen recurring-Events
    3. Generiert fehlende Instanzen für konfigurierten Zeitraum
    """
    
    def __init__(self, lookahead_months: int = 3):
        """
        Args:
            lookahead_months: Wie viele Monate im Voraus generieren (default: 3)
        """
        self.lookahead_months = lookahead_months
        self.recurring_events = {}
        self.existing_hashes = set()
        self.generated_count = 0
        self.stats = {
            'scanned_files': 0,
            'recurring_found': 0,
            'instances_generated': 0,
            'instances_skipped': 0,
            'errors': 0
        }
    
    def load_event_file(self, filepath: Path) -> Optional[Dict]:
        """Lädt Event-YAML aus Datei"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        event_data = yaml.safe_load(parts[1])
                        event_data['_content'] = parts[2].strip()
                        event_data['_filepath'] = str(filepath)
                        event_data['_filename'] = filepath.name
                        return event_data
        except Exception as e:
            print(f"⚠️  Fehler beim Laden von {filepath.name}: {e}")
            self.stats['errors'] += 1
        
        return None
    
    def generate_event_hash(self, title: str, date: str, time: str, location: str) -> str:
        """Generiert Hash für Event (zur Duplikat-Erkennung)"""
        hash_string = f"{title}{date}{time}{location}".lower()
        return hashlib.md5(hash_string.encode()).hexdigest()[:12]
    
    def load_existing_hashes(self):
        """Lädt Hashes aller existierenden Events"""
        self.existing_hashes = set()
        
        # _events/ durchsuchen
        if EVENTS_DIR.exists():
            for filepath in EVENTS_DIR.glob("*.md"):
                event = self.load_event_file(filepath)
                if event:
                    event_hash = event.get('event_hash')
                    if event_hash:
                        self.existing_hashes.add(event_hash)
                    else:
                        # Hash generieren falls nicht vorhanden
                        event_hash = self.generate_event_hash(
                            event.get('title', ''),
                            str(event.get('date', '')),
                            event.get('start_time', ''),
                            event.get('location', '')
                        )
                        self.existing_hashes.add(event_hash)
    
    def scan_for_recurring_events(self):
        """
        Scannt alle Event-Dateien nach recurring-Flag
        Reihenfolge: _events/ → _history/YYYYMM/ (aktuelles Jahr) → _history/YYYYMM/ (Folgejahre)
        """
        print("🔍 Scanne nach wiederkehrenden Events...")
        
        scan_paths = []
        
        # 1. Aktueller Events-Ordner
        scan_paths.append(("_events", EVENTS_DIR))
        
        # 2. Archive (monatlich sortiert, neueste zuerst)
        if HISTORY_DIR.exists():
            archive_dirs = sorted(HISTORY_DIR.glob("*/"), reverse=True)
            for archive_dir in archive_dirs:
                scan_paths.append((f"_history/{archive_dir.name}", archive_dir))
        
        # Scannen
        for location_name, scan_path in scan_paths:
            if not scan_path.exists():
                continue
            
            for filepath in scan_path.glob("*.md"):
                self.stats['scanned_files'] += 1
                event = self.load_event_file(filepath)
                
                if not event:
                    continue
                
                # Prüfe auf recurring-Flag
                recurring_config = event.get('recurring')
                if recurring_config and recurring_config.get('enabled'):
                    event_id = event.get('event_hash') or self.generate_event_hash(
                        event.get('title', ''),
                        str(event.get('date', '')),
                        event.get('start_time', ''),
                        event.get('location', '')
                    )
                    
                    # Nur hinzufügen, wenn noch nicht im Index
                    if event_id not in self.recurring_events:
                        self.recurring_events[event_id] = {
                            'id': event_id,
                            'title': event.get('title'),
                            'location': event.get('location'),
                            'start_time': event.get('start_time'),
                            'end_time': event.get('end_time', ''),
                            'category': event.get('category'),
                            'tags': event.get('tags', []),
                            'description': event.get('description', ''),
                            'url': event.get('url', ''),
                            'coordinates': event.get('coordinates', {}),
                            'address': event.get('address', ''),
                            'status': event.get('status', 'Öffentlich'),
                            'source': event.get('source', ''),
                            'recurring': recurring_config,
                            'template_file': str(filepath),
                            'found_in': location_name
                        }
                        self.stats['recurring_found'] += 1
                        print(f"  ✓ {event.get('title')} ({location_name})")
        
        print(f"\n📊 {self.stats['recurring_found']} wiederkehrende Events gefunden")
    
    def calculate_next_occurrences(self, recurring_event: Dict) -> List[datetime]:
        """
        Berechnet nächste Vorkommnisse eines wiederkehrenden Events
        
        Returns:
            List[datetime]: Datumsangaben für nächste Instanzen
        """
        recurring_config = recurring_event['recurring']
        frequency = recurring_config.get('frequency', 'weekly')
        interval = recurring_config.get('interval', 1)
        by_day = recurring_config.get('by_day', [])
        
        start_date_str = recurring_config.get('start_date')
        end_date_str = recurring_config.get('end_date')
        exceptions = recurring_config.get('exceptions', [])
        
        # Start-Datum ermitteln
        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            except ValueError:
                start_date = datetime.now().date()
        else:
            start_date = datetime.now().date()
        
        # End-Datum ermitteln
        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                end_date = None
        else:
            end_date = None
        
        # Lookahead-Datum berechnen
        lookahead_date = datetime.now().date() + timedelta(days=self.lookahead_months * 30)
        if end_date and end_date < lookahead_date:
            lookahead_date = end_date
        
        occurrences = []
        current_date = max(start_date, datetime.now().date())
        
        # Generiere Instanzen basierend auf Frequenz
        if frequency == 'daily':
            while current_date <= lookahead_date:
                if str(current_date) not in exceptions:
                    occurrences.append(current_date)
                current_date += timedelta(days=interval)
        
        elif frequency == 'weekly':
            # Wöchentlich mit spezifischen Wochentagen
            if by_day:
                target_weekdays = [WEEKDAY_MAP[day] for day in by_day if day in WEEKDAY_MAP]
                
                while current_date <= lookahead_date:
                    if current_date.weekday() in target_weekdays:
                        if str(current_date) not in exceptions:
                            occurrences.append(current_date)
                    current_date += timedelta(days=1)
            else:
                # Wöchentlich ohne spezifische Tage
                while current_date <= lookahead_date:
                    if str(current_date) not in exceptions:
                        occurrences.append(current_date)
                    current_date += timedelta(weeks=interval)
        
        elif frequency == 'biweekly':
            while current_date <= lookahead_date:
                if str(current_date) not in exceptions:
                    occurrences.append(current_date)
                current_date += timedelta(weeks=2 * interval)
        
        elif frequency == 'monthly':
            # Monatlich (gleicher Tag im Monat)
            while current_date <= lookahead_date:
                if str(current_date) not in exceptions:
                    occurrences.append(current_date)
                # Nächster Monat
                month = current_date.month + interval
                year = current_date.year
                while month > 12:
                    month -= 12
                    year += 1
                try:
                    current_date = current_date.replace(year=year, month=month)
                except ValueError:
                    # Tag existiert nicht im Zielmonat (z.B. 31. Februar)
                    break
        
        elif frequency == 'yearly':
            while current_date <= lookahead_date:
                if str(current_date) not in exceptions:
                    occurrences.append(current_date)
                current_date = current_date.replace(year=current_date.year + interval)
        
        return occurrences
    
    def create_event_instance(self, template_event: Dict, occurrence_date: datetime) -> bool:
        """
        Erstellt eine neue Event-Instanz basierend auf Template
        
        Returns:
            bool: True wenn erfolgreich erstellt
        """
        # Dateiname generieren
        date_str = occurrence_date.strftime("%Y-%m-%d")
        title_slug = re.sub(r'[^\w\s-]', '', template_event['title'].lower())
        title_slug = re.sub(r'[-\s]+', '-', title_slug)[:50]
        filename = f"{date_str}-{title_slug}.md"
        filepath = EVENTS_DIR / filename
        
        # Prüfe ob Datei bereits existiert
        if filepath.exists():
            self.stats['instances_skipped'] += 1
            return False
        
        # Hash für neue Instanz generieren
        event_hash = self.generate_event_hash(
            template_event['title'],
            date_str,
            template_event['start_time'],
            template_event['location']
        )
        
        # Prüfe auf Duplikat via Hash
        if event_hash in self.existing_hashes:
            self.stats['instances_skipped'] += 1
            return False
        
        # Event-Daten vorbereiten
        event_data = {
            'title': template_event['title'],
            'date': date_str,
            'start_time': template_event['start_time'],
            'end_time': template_event['end_time'],
            'location': template_event['location'],
            'address': template_event.get('address', ''),
            'coordinates': template_event.get('coordinates', {}),
            'category': template_event.get('category', 'Sonstiges'),
            'tags': template_event.get('tags', []),
            'description': template_event.get('description', ''),
            'url': template_event.get('url', ''),
            'image': '',
            'status': template_event.get('status', 'Öffentlich'),
            'source': f"{template_event.get('source', 'Recurring Expander')} (Auto-generiert)",
            'event_hash': event_hash,
            'recurring_parent': template_event['id']
        }
        
        # YAML Front Matter
        front_matter = yaml.dump(event_data, allow_unicode=True, sort_keys=False)
        
        # Markdown-Inhalt
        content = f"""---
{front_matter}---

{template_event.get('description', '')}

---
*Diese Instanz wurde automatisch aus einem wiederkehrenden Event generiert.*
"""
        
        # Datei schreiben
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.existing_hashes.add(event_hash)
            self.stats['instances_generated'] += 1
            print(f"  ✅ {filename}")
            return True
        except Exception as e:
            print(f"  ❌ Fehler bei {filename}: {e}")
            self.stats['errors'] += 1
            return False
    
    def expand_recurring_events(self):
        """Generiert fehlende Instanzen für alle wiederkehrenden Events"""
        if not self.recurring_events:
            print("\nℹ️  Keine wiederkehrenden Events gefunden")
            return
        
        print(f"\n🔄 Generiere Instanzen für {len(self.recurring_events)} wiederkehrende Events...")
        print(f"   Zeitraum: {self.lookahead_months} Monate im Voraus")
        print("-" * 60)
        
        for event_id, recurring_event in self.recurring_events.items():
            print(f"\n📅 {recurring_event['title']}")
            
            # Berechne nächste Vorkommnisse
            occurrences = self.calculate_next_occurrences(recurring_event)
            
            if not occurrences:
                print(f"  ℹ️  Keine neuen Instanzen zu generieren")
                continue
            
            print(f"  → {len(occurrences)} Termine berechnet")
            
            # Erstelle Instanzen
            for occurrence_date in occurrences:
                self.create_event_instance(recurring_event, occurrence_date)
    
    def save_index(self):
        """Speichert Recurring-Events-Index"""
        INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        index_data = {
            'last_update': datetime.now().isoformat(),
            'recurring_events': list(self.recurring_events.values()),
            'stats': {
                'total_recurring': len(self.recurring_events),
                'last_scan_files': self.stats['scanned_files']
            }
        }
        
        try:
            with open(INDEX_FILE, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Index gespeichert: {INDEX_FILE}")
        except Exception as e:
            print(f"⚠️  Fehler beim Speichern des Index: {e}")
    
    def load_index(self) -> bool:
        """
        Lädt Recurring-Events-Index (falls vorhanden)
        
        Returns:
            bool: True wenn Index erfolgreich geladen
        """
        if not INDEX_FILE.exists():
            return False
        
        try:
            with open(INDEX_FILE, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            for event in index_data.get('recurring_events', []):
                self.recurring_events[event['id']] = event
            
            print(f"📋 Index geladen: {len(self.recurring_events)} wiederkehrende Events")
            return True
        except Exception as e:
            print(f"⚠️  Fehler beim Laden des Index: {e}")
            return False
    
    def run(self, use_index: bool = True):
        """
        Hauptfunktion: Expandiert wiederkehrende Events
        
        Args:
            use_index: Wenn True, versuche Index zu laden (schneller)
        """
        print("\n" + "="*60)
        print("🔄 RECURRING EVENTS EXPANDER")
        print("="*60)
        
        # Lade existierende Event-Hashes
        print("\n📚 Lade existierende Events...")
        self.load_existing_hashes()
        print(f"   {len(self.existing_hashes)} Events gefunden")
        
        # Versuche Index zu laden (optional)
        if use_index and self.load_index():
            print("   ✓ Index verwendet (schneller)")
        else:
            # Vollständiger Scan
            self.scan_for_recurring_events()
            # Index speichern für nächstes Mal
            self.save_index()
        
        # Generiere fehlende Instanzen
        self.expand_recurring_events()
        
        # Statistik
        print("\n" + "="*60)
        print("✅ RECURRING EXPANSION ABGESCHLOSSEN")
        print("="*60)
        print(f"Gescannte Dateien: {self.stats['scanned_files']}")
        print(f"Wiederkehrende Events: {self.stats['recurring_found']}")
        print(f"Instanzen generiert: {self.stats['instances_generated']}")
        print(f"Instanzen übersprungen: {self.stats['instances_skipped']}")
        print(f"Fehler: {self.stats['errors']}")


def main():
    """CLI-Interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generiert Instanzen für wiederkehrende Events'
    )
    parser.add_argument(
        '--months',
        type=int,
        default=3,
        help='Monate im Voraus generieren (default: 3)'
    )
    parser.add_argument(
        '--no-index',
        action='store_true',
        help='Ignoriere Index, führe vollständigen Scan durch'
    )
    parser.add_argument(
        '--rebuild-index',
        action='store_true',
        help='Index neu aufbauen (ohne Instanzen zu generieren)'
    )
    
    args = parser.parse_args()
    
    expander = RecurringExpander(lookahead_months=args.months)
    
    if args.rebuild_index:
        print("\n🔨 Baue Index neu auf...")
        expander.load_existing_hashes()
        expander.scan_for_recurring_events()
        expander.save_index()
    else:
        expander.run(use_index=not args.no_index)


if __name__ == "__main__":
    main()
