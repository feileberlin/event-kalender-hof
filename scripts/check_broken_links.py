#!/usr/bin/env python3
"""
Broken Link Checker für archivierte Events

Prüft alle URLs in archivierten Event-Dateien und markiert defekte Links.

Verwendung:
    python scripts/check_broken_links.py
    python scripts/check_broken_links.py --fix  # Fügt 🔗💔 Icon zu defekten Links hinzu

Funktionen:
    - Lädt alle Events mit status: "Archiviert"
    - Prüft URL-Felder (url, source_url, etc.)
    - HTTP-Status-Codes checken
    - Markiert defekte Links mit 🔗💔 Icon
    - Erstellt Report
"""

import sys
import os
from pathlib import Path
import yaml
import requests
from datetime import datetime
from typing import Dict, List, Tuple
import time

class BrokenLinkChecker:
    def __init__(self, fix_mode=False):
        self.fix_mode = fix_mode
        self.events_dir = Path(__file__).parent.parent / '_events'
        self.broken_links = []
        self.checked_links = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Event-Kalender-Hof/LinkChecker)'
        })
        
    def check_url(self, url: str, timeout: int = 10) -> Tuple[bool, int, str]:
        """
        Prüft ob URL erreichbar ist
        
        Returns:
            (is_valid, status_code, error_message)
        """
        if not url or url.startswith('#'):
            return True, 0, ""
        
        # Cache: URL nur einmal prüfen
        if url in self.checked_links:
            return True, 200, ""
        
        try:
            response = self.session.head(url, timeout=timeout, allow_redirects=True)
            status = response.status_code
            
            # HEAD request failed, try GET
            if status >= 400:
                response = self.session.get(url, timeout=timeout, allow_redirects=True)
                status = response.status_code
            
            self.checked_links.add(url)
            
            if status >= 400:
                return False, status, f"HTTP {status}"
            
            return True, status, ""
            
        except requests.exceptions.Timeout:
            return False, 0, "Timeout"
        except requests.exceptions.ConnectionError:
            return False, 0, "Connection Error"
        except requests.exceptions.TooManyRedirects:
            return False, 0, "Too Many Redirects"
        except requests.exceptions.RequestException as e:
            return False, 0, str(e)[:50]
        except Exception as e:
            return False, 0, f"Error: {str(e)[:50]}"
    
    def parse_event_file(self, filepath: Path) -> Dict:
        """Liest Event-Datei und extrahiert YAML Front Matter"""
        try:
            content = filepath.read_text(encoding='utf-8')
            
            # Split YAML Front Matter
            if not content.startswith('---'):
                return None
            
            parts = content.split('---', 2)
            if len(parts) < 3:
                return None
            
            yaml_content = parts[1]
            body_content = parts[2].strip()
            
            data = yaml.safe_load(yaml_content)
            data['_body'] = body_content
            data['_filepath'] = filepath
            
            return data
            
        except Exception as e:
            print(f"⚠️  Error parsing {filepath.name}: {e}")
            return None
    
    def extract_urls(self, event: Dict) -> List[Tuple[str, str]]:
        """
        Extrahiert alle URLs aus Event
        
        Returns:
            List of (field_name, url)
        """
        urls = []
        
        # Standard URL-Felder
        url_fields = ['url', 'source_url', 'ticket_url', 'facebook_url', 'instagram_url']
        
        for field in url_fields:
            if field in event and event[field]:
                url = event[field]
                if isinstance(url, str) and url.strip():
                    urls.append((field, url.strip()))
        
        return urls
    
    def check_event_links(self, event: Dict) -> List[Dict]:
        """Prüft alle Links eines Events"""
        broken = []
        urls = self.extract_urls(event)
        
        if not urls:
            return broken
        
        for field, url in urls:
            is_valid, status, error = self.check_url(url)
            
            if not is_valid:
                broken.append({
                    'file': event['_filepath'].name,
                    'title': event.get('title', 'Unknown'),
                    'field': field,
                    'url': url,
                    'status': status,
                    'error': error
                })
                
                print(f"  ❌ {field}: {url}")
                print(f"     Error: {error}")
        
        return broken
    
    def mark_broken_link(self, filepath: Path, field: str, url: str) -> bool:
        """Fügt 🔗💔 Icon zu defektem Link hinzu"""
        try:
            content = filepath.read_text(encoding='utf-8')
            
            # Verhindere doppelte Markierung
            if '🔗💔' in content:
                return False
            
            # Suche YAML-Feld
            old_line = f'{field}: "{url}"'
            new_line = f'{field}: "🔗💔 {url}"'
            
            if old_line not in content:
                old_line = f"{field}: '{url}'"
                new_line = f"{field}: '🔗💔 {url}'"
            
            if old_line not in content:
                old_line = f"{field}: {url}"
                new_line = f"{field}: 🔗💔 {url}"
            
            if old_line in content:
                new_content = content.replace(old_line, new_line)
                filepath.write_text(new_content, encoding='utf-8')
                return True
            
            return False
            
        except Exception as e:
            print(f"⚠️  Error marking link in {filepath.name}: {e}")
            return False
    
    def generate_report(self):
        """Erstellt Report über defekte Links"""
        if not self.broken_links:
            print("\n✅ Keine defekten Links gefunden!")
            return
        
        print(f"\n{'='*60}")
        print(f"BROKEN LINKS REPORT")
        print(f"{'='*60}\n")
        
        print(f"Gefundene defekte Links: {len(self.broken_links)}\n")
        
        # Gruppiere nach Event
        by_event = {}
        for link in self.broken_links:
            filename = link['file']
            if filename not in by_event:
                by_event[filename] = []
            by_event[filename].append(link)
        
        for filename, links in by_event.items():
            print(f"\n📄 {filename}")
            print(f"   Event: {links[0]['title']}")
            
            for link in links:
                print(f"\n   ❌ Feld: {link['field']}")
                print(f"      URL: {link['url']}")
                print(f"      Fehler: {link['error']}")
                if link['status'] > 0:
                    print(f"      HTTP Status: {link['status']}")
        
        print(f"\n{'='*60}\n")
    
    def run(self):
        """Hauptfunktion"""
        print("🔍 Broken Link Checker")
        print(f"Modus: {'FIX' if self.fix_mode else 'CHECK'}")
        print("="*60)
        
        if not self.events_dir.exists():
            print(f"❌ Events-Verzeichnis nicht gefunden: {self.events_dir}")
            return 1
        
        # Lade alle archivierten Events
        archived_events = []
        
        print("\n📂 Lade archivierte Events...")
        for filepath in sorted(self.events_dir.glob('*.md')):
            event = self.parse_event_file(filepath)
            
            if event and event.get('status') == 'Archiviert':
                archived_events.append(event)
        
        print(f"   Gefunden: {len(archived_events)} archivierte Events\n")
        
        if not archived_events:
            print("ℹ️  Keine archivierten Events gefunden.")
            return 0
        
        # Prüfe Links
        print("🔗 Prüfe Links...\n")
        
        for event in archived_events:
            print(f"📄 {event['_filepath'].name}")
            print(f"   Event: {event.get('title', 'Unknown')}")
            
            broken = self.check_event_links(event)
            
            if broken:
                self.broken_links.extend(broken)
                
                if self.fix_mode:
                    print(f"\n   🔧 Markiere defekte Links...")
                    for link in broken:
                        success = self.mark_broken_link(
                            event['_filepath'],
                            link['field'],
                            link['url']
                        )
                        if success:
                            print(f"      ✓ {link['field']} markiert")
            else:
                print("   ✓ Alle Links OK")
            
            print()
            time.sleep(0.5)  # Rate limiting
        
        # Report
        self.generate_report()
        
        if self.fix_mode and self.broken_links:
            print("🔧 Defekte Links wurden mit 🔗💔 Icon markiert.")
            print("\nNächste Schritte:")
            print("1. git add _events/")
            print("2. git commit -m 'Fix: Defekte Links markiert'")
            print("3. git push origin main")
        
        return 1 if self.broken_links else 0


def main():
    fix_mode = '--fix' in sys.argv or '-f' in sys.argv
    
    checker = BrokenLinkChecker(fix_mode=fix_mode)
    exit_code = checker.run()
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
