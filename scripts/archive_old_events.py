#!/usr/bin/env python3
"""
Event Archivierungs-Tool
Verschiebt alte Events automatisch nach _events/_history/{YEAR}/
"""

import os
import shutil
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

EVENTS_DIR = Path("_events")
HISTORY_DIR = Path("_events/_history")


class EventArchiver:
    """Verwaltet Archivierung alter Events"""
    
    def __init__(self, days_threshold: int = 30):
        """
        Args:
            days_threshold: Events älter als X Tage werden archiviert (default: 30)
        """
        self.days_threshold = days_threshold
        self.threshold_date = datetime.now() - timedelta(days=days_threshold)
        self.stats = {
            'total': 0,
            'archived': 0,
            'already_archived': 0,
            'skipped': 0,
            'errors': 0
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
        """Bestimmt Ziel-Pfad für archiviertes Event"""
        try:
            event_date_str = event.get('date')
            if isinstance(event_date_str, datetime):
                year = event_date_str.year
            else:
                year = datetime.strptime(str(event_date_str), '%Y-%m-%d').year
            
            archive_year_dir = HISTORY_DIR / str(year)
            return archive_year_dir / filepath.name
        except Exception:
            # Fallback: Aktuelles Jahr
            return HISTORY_DIR / str(datetime.now().year) / filepath.name
    
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
        
        # Events nach Jahr gruppieren
        events_by_year = {}
        for event in events:
            year = self.get_archive_path(event, event['_filepath']).parent.name
            if year not in events_by_year:
                events_by_year[year] = []
            events_by_year[year].append(event)
        
        print(f"\n📁 Archiv-Struktur:")
        for year, year_events in sorted(events_by_year.items()):
            print(f"  • _history/{year}/: {len(year_events)} Events")
        
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
        
        # Abschluss-Statistik
        print("\n" + "="*60)
        print("✅ ARCHIVIERUNG ABGESCHLOSSEN")
        print("="*60)
        print(f"Archiviert: {self.stats['archived']} Events")
        print(f"Fehler: {self.stats['errors']}")
        
        if not dry_run:
            print("\n💡 Nächste Schritte:")
            print("   1. git add _events/")
            print("   2. git commit -m 'Archive: Events älter als " + 
                  f"{self.days_threshold} Tage'")
            print("   3. git push")


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
