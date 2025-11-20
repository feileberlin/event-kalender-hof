#!/usr/bin/env python3
"""
Event Archivierungs-Tool
Verschiebt alte Events automatisch nach _events/_history/{YYYYMM}/
Monatliche Archivierung für bessere Übersicht
"""

import os
import shutil
import yaml
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Set

EVENTS_DIR = Path("_events")
HISTORY_DIR = Path("_events/_history")
RECURRING_INDEX = Path("_data/recurring_index.json")


class EventArchiver:
    """Verwaltet Archivierung alter Events mit monatlicher Struktur"""
    
    def __init__(self, days_threshold: int = 30, scan_recurring: bool = True):
        """
        Args:
            days_threshold: Events älter als X Tage werden archiviert (default: 30)
            scan_recurring: Scanne vor Archivierung nach recurring-Events (default: True)
        """
        self.days_threshold = days_threshold
        self.threshold_date = datetime.now() - timedelta(days=days_threshold)
        self.scan_recurring = scan_recurring
        self.recurring_events = {}
        self.stats = {
            'total': 0,
            'archived': 0,
            'already_archived': 0,
            'skipped': 0,
            'errors': 0,
            'recurring_found': 0
        }
    
    def load_event_file(self, filepath: Path) -> Dict:
        """Lädt Event-YAML aus Datei"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # YAML Front Matter extrahieren
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        event_data = yaml.safe_load(parts[1])
                        event_data['_content'] = parts[2].strip()
                        event_data['_filepath'] = filepath
                        return event_data
        except Exception as e:
            print(f"⚠️  Fehler beim Laden von {filepath.name}: {e}")
        
        return None
    
    def is_event_old(self, event: Dict) -> bool:
        """Prüft ob Event älter als Threshold ist"""
        try:
            event_date_str = event.get('date')
            if isinstance(event_date_str, datetime):
                event_date = event_date_str
            else:
                event_date = datetime.strptime(str(event_date_str), '%Y-%m-%d')
            
            return event_date < self.threshold_date
        except Exception as e:
            print(f"⚠️  Fehler beim Datum-Parsing: {e}")
            return False
    
    def get_archive_path(self, event: Dict, filepath: Path) -> Path:
        """Bestimmt Ziel-Pfad für archiviertes Event (monatliche Struktur)"""
        try:
            event_date_str = event.get('date')
            if isinstance(event_date_str, datetime):
                year_month = event_date_str.strftime('%Y%m')
            else:
                dt = datetime.strptime(str(event_date_str), '%Y-%m-%d')
                year_month = dt.strftime('%Y%m')
            
            archive_month_dir = HISTORY_DIR / year_month
            return archive_month_dir / filepath.name
        except Exception:
            # Fallback: Aktueller Monat
            year_month = datetime.now().strftime('%Y%m')
            return HISTORY_DIR / year_month / filepath.name
    
    def check_recurring(self, event: Dict) -> bool:
        """Prüft ob Event recurring ist und fügt es zum Index hinzu"""
        recurring_config = event.get('recurring')
        if recurring_config and recurring_config.get('enabled'):
            event_id = event.get('event_hash', '')
            if not event_id:
                # Generiere ID falls nicht vorhanden
                import hashlib
                hash_string = f"{event.get('title', '')}{event.get('date', '')}{event.get('start_time', '')}{event.get('location', '')}".lower()
                event_id = hashlib.md5(hash_string.encode()).hexdigest()[:12]
            
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
                'template_file': str(event['_filepath']),
                'archived_from': '_events'
            }
            self.stats['recurring_found'] += 1
            return True
        return False
    
    def archive_event(self, event: Dict, dry_run: bool = False) -> bool:
        """
        Archiviert ein Event
        
        Args:
            event: Event-Dict mit _filepath
            dry_run: Wenn True, keine tatsächlichen Änderungen
            
        Returns:
            True bei Erfolg
        """
        filepath = event['_filepath']
        
        # Vor Archivierung: Prüfe auf recurring
        if self.scan_recurring:
            self.check_recurring(event)
        
        archive_path = self.get_archive_path(event, filepath)
        
        # Archive-Verzeichnis erstellen
        if not dry_run:
            archive_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Status auf "Archiviert" setzen
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Status ändern im YAML
            if 'status:' in content:
                # Verschiedene Status-Formate behandeln
                content = content.replace('status: "Öffentlich"', 'status: "Archiviert"')
                content = content.replace("status: 'Öffentlich'", "status: 'Archiviert'")
                content = content.replace('status: Öffentlich', 'status: Archiviert')
                content = content.replace('status: "Entwurf"', 'status: "Archiviert"')
                content = content.replace("status: 'Entwurf'", "status: 'Archiviert'")
                content = content.replace('status: Entwurf', 'status: Archiviert')
            else:
                # Status hinzufügen wenn nicht vorhanden
                content = content.replace('---\n', '---\nstatus: "Archiviert"\n', 1)
            
            if not dry_run:
                # Aktualisierte Datei ins Archiv schreiben
                with open(archive_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Original-Datei löschen
                filepath.unlink()
            
            print(f"  ✅ {filepath.name} → {archive_path.relative_to(EVENTS_DIR)}")
            return True
            
        except Exception as e:
            print(f"  ❌ Fehler bei {filepath.name}: {e}")
            return False
    
    def find_events_to_archive(self) -> List[Dict]:
        """Findet alle Events die archiviert werden sollen"""
        events_to_archive = []
        
        if not EVENTS_DIR.exists():
            print("❌ _events Verzeichnis nicht gefunden!")
            return []
        
        # Alle Event-Dateien durchgehen
        for filepath in EVENTS_DIR.glob("*.md"):
            self.stats['total'] += 1
            
            event = self.load_event_file(filepath)
            if not event:
                self.stats['errors'] += 1
                continue
            
            # Prüfen ob Event alt genug ist
            if not self.is_event_old(event):
                self.stats['skipped'] += 1
                continue
            
            # Prüfen ob bereits archiviert
            if event.get('status') == 'Archiviert':
                self.stats['already_archived'] += 1
                continue
            
            events_to_archive.append(event)
        
        return events_to_archive
    
    def run(self, dry_run: bool = False, interactive: bool = False):
        """
        Hauptfunktion: Archiviert alte Events
        
        Args:
            dry_run: Zeigt nur was passieren würde, ohne Änderungen
            interactive: Fragt bei jedem Event nach
        """
        print("\n" + "="*60)
        print("📦 EVENT ARCHIVIERUNG")
        print("="*60)
        print(f"Threshold: Events älter als {self.days_threshold} Tage")
        print(f"Stichtag: {self.threshold_date.strftime('%Y-%m-%d')}")
        
        if dry_run:
            print("⚠️  DRY-RUN Modus: Keine Änderungen!")
        
        print("\n🔍 Suche Events zum Archivieren...")
        
        events = self.find_events_to_archive()
        
        print(f"\n📊 Statistik:")
        print(f"  • Gesamt Events: {self.stats['total']}")
        print(f"  • Zum Archivieren: {len(events)}")
        print(f"  • Bereits archiviert: {self.stats['already_archived']}")
        print(f"  • Zu neu: {self.stats['skipped']}")
        print(f"  • Fehler: {self.stats['errors']}")
        
        if not events:
            print("\n✅ Keine Events zum Archivieren!")
            return
        
        # Events nach Monat gruppieren
        events_by_month = {}
        for event in events:
            month = self.get_archive_path(event, event['_filepath']).parent.name
            if month not in events_by_month:
                events_by_month[month] = []
            events_by_month[month].append(event)
        
        print(f"\n📁 Archiv-Struktur (monatlich):")
        for month, month_events in sorted(events_by_month.items()):
            # Format: 202511 → November 2025
            try:
                year = month[:4]
                month_num = month[4:]
                month_name = datetime.strptime(month_num, '%m').strftime('%B')
                print(f"  • _history/{month}/ ({month_name} {year}): {len(month_events)} Events")
            except:
                print(f"  • _history/{month}/: {len(month_events)} Events")
        
        # Bestätigung einholen (wenn nicht dry_run)
        if not dry_run and not interactive:
            print("\n" + "-"*60)
            response = input(f"❓ {len(events)} Events archivieren? (j/n): ")
            if response.lower() != 'j':
                print("❌ Abgebrochen")
                return
        
        # Events archivieren
        print("\n📦 Archiviere Events...")
        print("-"*60)
        
        for event in events:
            if interactive and not dry_run:
                print(f"\n📄 {event['_filepath'].name}")
                print(f"   Titel: {event.get('title', 'N/A')}")
                print(f"   Datum: {event.get('date', 'N/A')}")
                response = input("   Archivieren? (j/n): ")
                if response.lower() != 'j':
                    print("   ⏭️  Übersprungen")
                    continue
            
            if self.archive_event(event, dry_run=dry_run):
                self.stats['archived'] += 1
            else:
                self.stats['errors'] += 1
        
        # Recurring-Index aktualisieren
        if self.recurring_events and not dry_run:
            self.update_recurring_index()
        
        # Abschluss-Statistik
        print("\n" + "="*60)
        print("✅ ARCHIVIERUNG ABGESCHLOSSEN")
        print("="*60)
        print(f"Archiviert: {self.stats['archived']} Events")
        print(f"Wiederkehrende Events gefunden: {self.stats['recurring_found']}")
        print(f"Fehler: {self.stats['errors']}")
        
        if not dry_run:
            print("\n💡 Nächste Schritte:")
            print("   1. git add _events/ _data/recurring_index.json")
            print("   2. git commit -m 'Archive: Events älter als " + 
                  f"{self.days_threshold} Tage (monatlich)'")
            print("   3. git push")
            
            if self.recurring_events:
                print("\n🔄 Tipp: Führe 'python3 scripts/recurring_expander.py' aus,")
                print("   um neue Instanzen für wiederkehrende Events zu generieren.")
    
    def update_recurring_index(self):
        """Aktualisiert Recurring-Events-Index"""
        if not self.recurring_events:
            return
        
        # Lade existierenden Index
        existing_index = {}
        if RECURRING_INDEX.exists():
            try:
                with open(RECURRING_INDEX, 'r', encoding='utf-8') as f:
                    index_data = json.load(f)
                    for event in index_data.get('recurring_events', []):
                        existing_index[event['id']] = event
            except Exception as e:
                print(f"⚠️  Fehler beim Laden des Index: {e}")
        
        # Merge mit neuen recurring events
        existing_index.update(self.recurring_events)
        
        # Speichere aktualisierten Index
        RECURRING_INDEX.parent.mkdir(parents=True, exist_ok=True)
        index_data = {
            'last_update': datetime.now().isoformat(),
            'recurring_events': list(existing_index.values()),
            'stats': {
                'total_recurring': len(existing_index),
                'last_archive_scan': self.stats['recurring_found']
            }
        }
        
        try:
            with open(RECURRING_INDEX, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Recurring-Index aktualisiert: {RECURRING_INDEX}")
            print(f"   {len(self.recurring_events)} neue recurring events hinzugefügt")
        except Exception as e:
            print(f"⚠️  Fehler beim Speichern des Index: {e}")


def main():
    """CLI-Interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Archiviert alte Events nach _events/_history/{YEAR}/'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Events älter als X Tage archivieren (default: 30)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Zeigt nur was passieren würde, ohne Änderungen'
    )
    parser.add_argument(
        '--interactive',
        '-i',
        action='store_true',
        help='Fragt bei jedem Event nach'
    )
    parser.add_argument(
        '--force',
        '-f',
        action='store_true',
        help='Keine Bestätigung erforderlich'
    )
    
    args = parser.parse_args()
    
    archiver = EventArchiver(days_threshold=args.days)
    archiver.run(
        dry_run=args.dry_run,
        interactive=args.interactive
    )


if __name__ == "__main__":
    main()
