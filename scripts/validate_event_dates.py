#!/usr/bin/env python3
"""
Event-Datums-Validator
Prüft Events auf häufige Datumsfehler und bietet Korrekturvorschläge
"""

import re
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

EVENTS_DIR = Path("_events")

class EventDateValidator:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.stats = defaultdict(int)
    
    def validate_all_events(self):
        """Validiert alle Events im Events-Verzeichnis"""
        print("🔍 Validiere Event-Daten...\n")
        
        today = datetime.now().date()
        events = []
        
        for file_path in EVENTS_DIR.glob("*.md"):
            if file_path.name.startswith('_'):
                continue
                
            event_data = self.parse_event_file(file_path)
            if event_data:
                events.append({
                    'file': file_path,
                    'data': event_data
                })
        
        # Validierungen
        self.check_past_events(events, today)
        self.check_publication_date_confusion(events)
        self.check_recurring_patterns(events)
        self.check_suspicious_dates(events)
        self.check_filename_mismatch(events)
        
        # Report
        self.print_report()
    
    def parse_event_file(self, file_path):
        """Parst Event-Datei und extrahiert YAML Front Matter"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # YAML Front Matter extrahieren
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if match:
                yaml_content = match.group(1)
                data = yaml.safe_load(yaml_content)
                
                # Datum parsen
                if isinstance(data.get('date'), str):
                    data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
                
                return data
        except Exception as e:
            self.warnings.append(f"⚠️ Fehler beim Parsen von {file_path.name}: {e}")
        
        return None
    
    def check_past_events(self, events, today):
        """Prüft auf Events in der Vergangenheit"""
        past_events = []
        
        for event in events:
            event_date = event['data'].get('date')
            if not event_date:
                continue
            
            days_ago = (today - event_date).days
            
            if days_ago > 0:
                status = event['data'].get('status', 'Unbekannt')
                if status != 'Archiviert':
                    past_events.append({
                        'file': event['file'].name,
                        'title': event['data'].get('title', 'Unbekannt'),
                        'date': event_date,
                        'days_ago': days_ago,
                        'status': status,
                        'source': event['data'].get('source', 'Unbekannt')
                    })
                    self.stats['past_events'] += 1
        
        if past_events:
            self.issues.append({
                'type': '📅 EVENTS IN DER VERGANGENHEIT',
                'severity': 'ERROR',
                'count': len(past_events),
                'events': past_events,
                'recommendation': 'Diese Events sollten archiviert oder gelöscht werden, es sei denn, sie sind wiederkehrend.'
            })
    
    def check_publication_date_confusion(self, events):
        """Prüft auf Events, die alle am gleichen Tag erstellt wurden"""
        date_clusters = defaultdict(list)
        
        for event in events:
            event_date = event['data'].get('date')
            if event_date:
                date_clusters[event_date].append(event)
        
        suspicious_clusters = []
        for date, cluster_events in date_clusters.items():
            if len(cluster_events) >= 5:  # 5+ Events am gleichen Tag
                sources = set(e['data'].get('source', '') for e in cluster_events)
                if len(sources) == 1:  # Alle von der gleichen Quelle
                    suspicious_clusters.append({
                        'date': date,
                        'count': len(cluster_events),
                        'source': list(sources)[0],
                        'titles': [e['data'].get('title', '') for e in cluster_events[:3]]
                    })
                    self.stats['suspicious_clusters'] += 1
        
        if suspicious_clusters:
            self.issues.append({
                'type': '⚠️  VERDACHT: VERÖFFENTLICHUNGSDATUM STATT EVENT-DATUM',
                'severity': 'WARNING',
                'count': len(suspicious_clusters),
                'clusters': suspicious_clusters,
                'recommendation': 'Prüfe, ob diese Events wirklich alle am gleichen Tag stattfinden oder ob das Veröffentlichungsdatum verwendet wurde.'
            })
    
    def check_recurring_patterns(self, events):
        """Erkennt potentiell wiederkehrende Events"""
        title_groups = defaultdict(list)
        
        for event in events:
            title = event['data'].get('title', '').lower()
            # Vereinfache Titel (entferne Datum-Teile)
            simple_title = re.sub(r'\d{1,2}\.\s*\w+|\d{4}', '', title).strip()
            title_groups[simple_title].append(event)
        
        recurring_candidates = []
        for title, title_events in title_groups.items():
            if len(title_events) >= 2:
                # Prüfe ob gleiche Location
                locations = set(e['data'].get('location', '') for e in title_events)
                if len(locations) == 1:
                    recurring_candidates.append({
                        'title': title,
                        'count': len(title_events),
                        'location': list(locations)[0],
                        'dates': sorted([e['data'].get('date') for e in title_events if e['data'].get('date')])
                    })
                    self.stats['recurring_candidates'] += 1
        
        if recurring_candidates:
            self.issues.append({
                'type': '🔄 POTENTIELL WIEDERKEHRENDE EVENTS',
                'severity': 'INFO',
                'count': len(recurring_candidates),
                'events': recurring_candidates,
                'recommendation': 'Diese Events könnten wiederkehrend sein. Erwäge, ein "recurring"-Feld hinzuzufügen.'
            })
    
    def check_suspicious_dates(self, events):
        """Prüft auf verdächtige Datumsmuster"""
        suspicious = []
        
        for event in events:
            event_date = event['data'].get('date')
            title = event['data'].get('title', '')
            description = event['data'].get('description', '')
            
            if not event_date:
                continue
            
            # "heute", "morgen" im Text aber altes Datum
            today = datetime.now().date()
            text = f"{title} {description}".lower()
            
            if ('heute' in text or 'morgen' in text) and event_date < today:
                suspicious.append({
                    'file': event['file'].name,
                    'title': title,
                    'date': event_date,
                    'reason': 'Text enthält "heute/morgen" aber Datum liegt in der Vergangenheit'
                })
                self.stats['suspicious_dates'] += 1
        
        if suspicious:
            self.issues.append({
                'type': '🚨 VERDÄCHTIGE DATUMSANGABEN',
                'severity': 'ERROR',
                'count': len(suspicious),
                'events': suspicious,
                'recommendation': 'Diese Events haben inkonsistente Datums-Referenzen. Prüfe die Quelle erneut.'
            })
    
    def check_filename_mismatch(self, events):
        """Prüft ob Dateiname und Event-Datum übereinstimmen"""
        mismatches = []
        
        for event in events:
            filename = event['file'].name
            event_date = event['data'].get('date')
            
            if not event_date:
                continue
            
            # Extrahiere Datum aus Dateiname (Format: YYYY-MM-DD-title.md)
            filename_match = re.match(r'(\d{4}-\d{2}-\d{2})-', filename)
            if filename_match:
                filename_date = datetime.strptime(filename_match.group(1), '%Y-%m-%d').date()
                
                if filename_date != event_date:
                    mismatches.append({
                        'file': filename,
                        'filename_date': filename_date,
                        'event_date': event_date,
                        'title': event['data'].get('title', '')
                    })
                    self.stats['filename_mismatches'] += 1
        
        if mismatches:
            self.issues.append({
                'type': '📝 DATEINAME STIMMT NICHT MIT EVENT-DATUM ÜBEREIN',
                'severity': 'WARNING',
                'count': len(mismatches),
                'events': mismatches,
                'recommendation': 'Dateiname sollte mit Event-Datum übereinstimmen für bessere Organisation.'
            })
    
    def print_report(self):
        """Gibt Validierungs-Report aus"""
        print("="*80)
        print("📊 EVENT-DATUMS-VALIDIERUNG - REPORT")
        print("="*80)
        print()
        
        if not self.issues and not self.warnings:
            print("✅ Alle Events sind korrekt validiert!")
            print()
            return
        
        # Issues
        for issue in self.issues:
            severity_icon = {
                'ERROR': '🔴',
                'WARNING': '⚠️',
                'INFO': 'ℹ️'
            }.get(issue['severity'], '•')
            
            print(f"{severity_icon} {issue['type']}")
            print(f"   Anzahl: {issue['count']}")
            print()
            
            if issue['type'] == '📅 EVENTS IN DER VERGANGENHEIT':
                print("   Events:")
                for event in issue['events'][:10]:  # Max 10 zeigen
                    print(f"   • {event['title']}")
                    print(f"     Datum: {event['date']} ({event['days_ago']} Tage her)")
                    print(f"     Status: {event['status']} | Quelle: {event['source']}")
                    print(f"     Datei: {event['file']}")
                    print()
                
                if issue['count'] > 10:
                    print(f"   ... und {issue['count'] - 10} weitere")
                    print()
            
            elif issue['type'] == '⚠️  VERDACHT: VERÖFFENTLICHUNGSDATUM STATT EVENT-DATUM':
                print("   Verdächtige Cluster:")
                for cluster in issue['clusters']:
                    print(f"   • Datum: {cluster['date']} - {cluster['count']} Events")
                    print(f"     Quelle: {cluster['source']}")
                    print(f"     Beispiele: {', '.join(cluster['titles'][:3])}")
                    print()
            
            elif issue['type'] == '🔄 POTENTIELL WIEDERKEHRENDE EVENTS':
                print("   Wiederkehrende Events:")
                for event in issue['events'][:5]:
                    print(f"   • {event['title']}")
                    print(f"     Location: {event['location']}")
                    print(f"     {event['count']} Vorkommen an: {', '.join(str(d) for d in event['dates'][:3])}")
                    print()
            
            elif issue['type'] == '🚨 VERDÄCHTIGE DATUMSANGABEN':
                print("   Inkonsistente Events:")
                for event in issue['events']:
                    print(f"   • {event['title']}")
                    print(f"     Datum: {event['date']}")
                    print(f"     Grund: {event['reason']}")
                    print(f"     Datei: {event['file']}")
                    print()
            
            elif issue['type'] == '📝 DATEINAME STIMMT NICHT MIT EVENT-DATUM ÜBEREIN':
                print("   Mismatches:")
                for event in issue['events'][:5]:
                    print(f"   • {event['file']}")
                    print(f"     Dateiname: {event['filename_date']} | Event: {event['event_date']}")
                    print()
            
            print(f"   💡 Empfehlung: {issue['recommendation']}")
            print()
            print("-"*80)
            print()
        
        # Warnings
        if self.warnings:
            print("⚠️  WARNUNGEN:")
            for warning in self.warnings:
                print(f"   {warning}")
            print()
        
        # Statistik
        print("="*80)
        print("📈 STATISTIK")
        print("="*80)
        for key, value in self.stats.items():
            print(f"   {key}: {value}")
        print()


def main():
    validator = EventDateValidator()
    validator.validate_all_events()


if __name__ == "__main__":
    main()
