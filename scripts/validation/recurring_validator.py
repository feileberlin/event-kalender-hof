#!/usr/bin/env python3
"""
Recurring Events Validator & Generator
Validiert wiederkehrende Event-Konfigurationen und generiert Instanzen
"""

import re
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

EVENTS_DIR = Path("_events")

VALID_FREQUENCIES = ['daily', 'weekly', 'biweekly', 'monthly', 'yearly']
VALID_WEEKDAYS = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
WEEKDAY_MAP = {
    'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 
    'FR': 4, 'SA': 5, 'SU': 6
}


class RecurringValidator:
    """Validiert wiederkehrende Event-Konfigurationen"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_recurring_config(self, recurring_data, event_date=None):
        """
        Validiert recurring-Konfiguration
        
        Returns:
            dict: {'is_valid': bool, 'errors': list, 'warnings': list}
        """
        self.errors = []
        self.warnings = []
        
        if not recurring_data:
            return {'is_valid': True, 'errors': [], 'warnings': []}
        
        if not isinstance(recurring_data, dict):
            self.errors.append("recurring muss ein Object sein")
            return self._result()
        
        # Enabled prüfen
        if not recurring_data.get('enabled'):
            return {'is_valid': True, 'errors': [], 'warnings': ['recurring.enabled ist false']}
        
        # Frequency prüfen
        frequency = recurring_data.get('frequency')
        if not frequency:
            self.errors.append("recurring.frequency fehlt")
        elif frequency not in VALID_FREQUENCIES:
            self.errors.append(f"Ungültige frequency: '{frequency}'. Erlaubt: {', '.join(VALID_FREQUENCIES)}")
        
        # Interval prüfen
        interval = recurring_data.get('interval', 1)
        if not isinstance(interval, int) or interval < 1:
            self.errors.append(f"interval muss positive Ganzzahl sein (ist: {interval})")
        
        # by_day prüfen
        by_day = recurring_data.get('by_day')
        if by_day:
            if not isinstance(by_day, list):
                self.errors.append("by_day muss Array sein")
            else:
                for day in by_day:
                    if day not in VALID_WEEKDAYS:
                        self.errors.append(f"Ungültiger Wochentag: '{day}'. Erlaubt: {', '.join(VALID_WEEKDAYS)}")
        
        # Datum-Validierung
        start_date = recurring_data.get('start_date')
        end_date = recurring_data.get('end_date')
        
        if start_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                self.errors.append(f"Ungültiges start_date: '{start_date}' (Format: YYYY-MM-DD)")
                start = None
        else:
            if event_date:
                self.warnings.append(f"start_date fehlt, verwende event.date: {event_date}")
            start = None
        
        if end_date:
            try:
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                self.errors.append(f"Ungültiges end_date: '{end_date}' (Format: YYYY-MM-DD)")
                end = None
            
            if start and end and end < start:
                self.errors.append(f"end_date ({end_date}) liegt vor start_date ({start_date})")
        
        # Exceptions prüfen
        exceptions = recurring_data.get('exceptions', [])
        if exceptions:
            if not isinstance(exceptions, list):
                self.errors.append("exceptions muss Array sein")
            else:
                for exc in exceptions:
                    try:
                        datetime.strptime(exc, '%Y-%m-%d')
                    except ValueError:
                        self.errors.append(f"Ungültige Exception: '{exc}' (Format: YYYY-MM-DD)")
        
        return self._result()
    
    def _result(self):
        return {
            'is_valid': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings
        }


class RecurringGenerator:
    """Generiert Instanzen wiederkehrender Events"""
    
    def generate_instances(self, event_data, days_ahead=60, max_instances=50):
        """
        Generiert Event-Instanzen für wiederkehrende Events
        
        Args:
            event_data: Event mit recurring-Konfiguration
            days_ahead: Wie viele Tage in die Zukunft
            max_instances: Maximale Anzahl Instanzen
        
        Returns:
            list: Liste von Event-Instanzen
        """
        recurring = event_data.get('recurring')
        
        if not recurring or not recurring.get('enabled'):
            return [event_data]  # Einmaliges Event
        
        instances = []
        
        # Start- und End-Datum
        start_date = recurring.get('start_date') or event_data.get('date')
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        
        end_date = recurring.get('end_date')
        if end_date and isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Maximales Datum
        max_date = datetime.now().date() + timedelta(days=days_ahead)
        if end_date:
            max_date = min(max_date, end_date)
        
        # Exceptions und Additions
        exceptions = set(recurring.get('exceptions', []))
        additions = recurring.get('additions', [])
        
        # Generiere reguläre Instanzen
        frequency = recurring.get('frequency')
        interval = recurring.get('interval', 1)
        by_day = recurring.get('by_day')
        by_set_pos = recurring.get('by_set_pos')  # NEU: Position im Monat
        
        # Tägliches Durchlaufen aller Tage von start bis max_date
        current = start_date
        count = 0
        
        while current <= max_date and count < max_instances:
            should_include = False
            weekday = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'][current.weekday()]
            
            # Frequenz-basierte Logik
            if frequency == 'daily':
                # Täglich: Jeder Tag ist gültig (mit interval)
                days_diff = (current - start_date).days
                should_include = (days_diff % interval == 0)
                
                # by_day Filter (optional bei daily)
                if should_include and by_day:
                    should_include = weekday in by_day
            
            elif frequency in ['weekly', 'biweekly']:
                # Wöchentlich: Nur bestimmte Wochentage
                if by_day and weekday in by_day:
                    # Prüfe ob die Woche passt (interval)
                    weeks_diff = (current - start_date).days // 7
                    multiplier = 2 if frequency == 'biweekly' else 1
                    should_include = (weeks_diff % (interval * multiplier) == 0)
            
            elif frequency == 'monthly':
                # Monatlich: Verschiedene Modi
                if by_set_pos is not None and by_day:
                    # Position im Monat (z.B. "erster Freitag", "letzter Sonntag")
                    should_include = self._is_nth_weekday_in_month(current, by_day, by_set_pos)
                    
                    # Prüfe Monats-Interval
                    if should_include:
                        months_diff = (current.year - start_date.year) * 12 + (current.month - start_date.month)
                        should_include = (months_diff % interval == 0)
                
                else:
                    # Fester Tag im Monat (z.B. "15. jeden Monats")
                    if current.day == start_date.day:
                        months_diff = (current.year - start_date.year) * 12 + (current.month - start_date.month)
                        should_include = (months_diff % interval == 0)
                        
                        # by_day Filter (optional)
                        if should_include and by_day:
                            should_include = weekday in by_day
            
            elif frequency == 'yearly':
                # Jährlich: Gleicher Tag und Monat
                if current.month == start_date.month and current.day == start_date.day:
                    years_diff = current.year - start_date.year
                    should_include = (years_diff % interval == 0)
            
            # Instanz hinzufügen
            if should_include:
                date_str = current.strftime('%Y-%m-%d')
                
                # Prüfe Ausnahmen
                if date_str not in exceptions:
                    instance = event_data.copy()
                    instance['date'] = date_str
                    instance['is_recurring_instance'] = True
                    instance['recurring_parent'] = event_data.get('title')
                    instances.append(instance)
                    count += 1
            
            # Nächster Tag
            current = current + timedelta(days=1)
        
        # Additions hinzufügen (außerordentliche Termine)
        for addition_date in additions:
            if isinstance(addition_date, str):
                try:
                    add_date = datetime.strptime(addition_date, '%Y-%m-%d').date()
                    
                    # Nur wenn im gültigen Zeitraum
                    if start_date <= add_date <= max_date:
                        # Prüfe ob schon vorhanden
                        if not any(inst['date'] == addition_date for inst in instances):
                            instance = event_data.copy()
                            instance['date'] = addition_date
                            instance['is_recurring_instance'] = True
                            instance['is_addition'] = True  # Markierung als Zusatztermin
                            instance['recurring_parent'] = event_data.get('title')
                            instances.append(instance)
                except ValueError:
                    pass  # Ungültiges Datum ignorieren
        
        # Sortiere nach Datum
        instances.sort(key=lambda x: x['date'] if isinstance(x['date'], str) else str(x['date']))
        
        return instances[:max_instances]
    
    def _is_nth_weekday_in_month(self, date, by_day, by_set_pos):
        """
        Prüft ob ein Datum der N-te Wochentag im Monat ist
        
        Args:
            date: Zu prüfendes Datum
            by_day: Liste der erlaubten Wochentage (z.B. ["FR"])
            by_set_pos: Position (1=erster, 2=zweiter, -1=letzter)
        
        Returns:
            bool: True wenn Datum passt
        """
        weekday = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'][date.weekday()]
        
        # Prüfe ob richtiger Wochentag
        if weekday not in by_day:
            return False
        
        # Finde alle Vorkommen dieses Wochentags im Monat
        import calendar
        month_start = date.replace(day=1)
        month_days = calendar.monthrange(date.year, date.month)[1]
        
        occurrences = []
        for day in range(1, month_days + 1):
            check_date = date.replace(day=day)
            check_weekday = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'][check_date.weekday()]
            if check_weekday == weekday:
                occurrences.append(day)
        
        # Prüfe Position
        if by_set_pos > 0:
            # Positiv: 1=erster, 2=zweiter, etc.
            if by_set_pos <= len(occurrences):
                return date.day == occurrences[by_set_pos - 1]
        else:
            # Negativ: -1=letzter, -2=vorletzter, etc.
            pos = by_set_pos
            if abs(pos) <= len(occurrences):
                return date.day == occurrences[pos]
        
        return False
        
        return instances
    
    def _next_occurrence(self, current, frequency, interval):
        """Berechnet nächsten Termin"""
        if frequency == 'daily':
            return current + timedelta(days=interval)
        elif frequency == 'weekly' or frequency == 'biweekly':
            weeks = 2 if frequency == 'biweekly' else 1
            return current + timedelta(days=7 * interval * weeks)
        elif frequency == 'monthly':
            # Monat erhöhen
            month = current.month + interval
            year = current.year
            while month > 12:
                month -= 12
                year += 1
            # Gleicher Tag im nächsten Monat (oder letzter Tag des Monats)
            try:
                return current.replace(year=year, month=month)
            except ValueError:
                # Tag existiert nicht (z.B. 31. Februar)
                import calendar
                last_day = calendar.monthrange(year, month)[1]
                return current.replace(year=year, month=month, day=last_day)
        elif frequency == 'yearly':
            return current.replace(year=current.year + interval)
        
        return current
    
    def get_next_occurrence_after(self, event_data, after_date=None):
        """Findet nächsten Termin nach einem Datum"""
        if after_date is None:
            after_date = datetime.now().date()
        
        instances = self.generate_instances(event_data, days_ahead=365, max_instances=1)
        
        for instance in instances:
            inst_date = instance['date']
            if isinstance(inst_date, str):
                inst_date = datetime.strptime(inst_date, '%Y-%m-%d').date()
            
            if inst_date > after_date:
                return instance
        
        return None


class RecurringDetector:
    """Erkennt automatisch wiederkehrende Patterns in Events"""
    
    def detect_recurring_patterns(self, events_dir=EVENTS_DIR):
        """
        Findet potentiell wiederkehrende Events
        
        Returns:
            dict: Gruppen von Events die wiederkehrend sein könnten
        """
        events = []
        
        for file_path in events_dir.glob("*.md"):
            if file_path.name.startswith('_'):
                continue
            
            event_data = self._parse_event_file(file_path)
            if event_data:
                events.append({
                    'file': file_path,
                    'data': event_data
                })
        
        # Gruppiere nach Titel + Location
        title_groups = defaultdict(list)
        
        for event in events:
            # Vereinfachter Titel (ohne Datum)
            title = event['data'].get('title', '')
            title_simple = re.sub(r'\d{1,2}\.\s*\w+|\d{4}', '', title).strip()
            
            location = event['data'].get('location', '')
            key = (title_simple.lower(), location.lower())
            
            title_groups[key].append(event)
        
        # Finde Gruppen mit 2+ Events
        recurring_candidates = {}
        
        for key, group in title_groups.items():
            if len(group) >= 2:
                # Analysiere Pattern
                pattern = self._analyze_pattern(group)
                if pattern:
                    recurring_candidates[key] = {
                        'events': group,
                        'pattern': pattern,
                        'count': len(group)
                    }
        
        return recurring_candidates
    
    def _parse_event_file(self, file_path):
        """Parst Event-Datei"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if match:
                data = yaml.safe_load(match.group(1))
                
                if isinstance(data.get('date'), str):
                    data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
                
                return data
        except Exception:
            pass
        
        return None
    
    def _analyze_pattern(self, events):
        """Analysiert Datums-Pattern einer Event-Gruppe"""
        dates = [e['data']['date'] for e in events if e['data'].get('date')]
        dates.sort()
        
        if len(dates) < 2:
            return None
        
        # Berechne Intervalle
        intervals = []
        for i in range(len(dates) - 1):
            delta = (dates[i+1] - dates[i]).days
            intervals.append(delta)
        
        # Erkenne Pattern
        if all(i == 7 for i in intervals):
            return {
                'frequency': 'weekly',
                'interval': 1,
                'by_day': [['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'][dates[0].weekday()]],
                'confidence': 1.0
            }
        elif all(i == 14 for i in intervals):
            return {
                'frequency': 'weekly',
                'interval': 2,
                'by_day': [['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'][dates[0].weekday()]],
                'confidence': 1.0
            }
        elif all(28 <= i <= 31 for i in intervals):
            return {
                'frequency': 'monthly',
                'interval': 1,
                'by_month_day': dates[0].day,
                'confidence': 0.9
            }
        elif len(set(intervals)) == 1:
            # Einheitliches Intervall (aber nicht standard)
            return {
                'frequency': 'custom',
                'interval_days': intervals[0],
                'confidence': 0.7
            }
        
        return None


def main():
    """Hauptprogramm - Validiert alle Events"""
    print("🔄 Recurring Events Validator\n")
    
    validator = RecurringValidator()
    generator = RecurringGenerator()
    detector = RecurringDetector()
    
    # 1. Validiere alle Events mit recurring-Config
    print("="*80)
    print("📋 VALIDIERUNG BESTEHENDER RECURRING-CONFIGS")
    print("="*80)
    print()
    
    events_with_recurring = []
    validation_errors = []
    
    for file_path in EVENTS_DIR.glob("*.md"):
        if file_path.name.startswith('_'):
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if match:
                data = yaml.safe_load(match.group(1))
                
                if data.get('recurring'):
                    events_with_recurring.append(file_path.name)
                    
                    result = validator.validate_recurring_config(
                        data['recurring'],
                        data.get('date')
                    )
                    
                    if not result['is_valid']:
                        validation_errors.append({
                            'file': file_path.name,
                            'errors': result['errors'],
                            'warnings': result['warnings']
                        })
                        
                        print(f"❌ {file_path.name}")
                        for error in result['errors']:
                            print(f"   ERROR: {error}")
                        for warning in result['warnings']:
                            print(f"   WARNING: {warning}")
                        print()
                    else:
                        print(f"✅ {file_path.name}")
                        if result['warnings']:
                            for warning in result['warnings']:
                                print(f"   WARNING: {warning}")
                        print()
        except Exception as e:
            print(f"⚠️  Fehler beim Lesen von {file_path.name}: {e}\n")
    
    if not events_with_recurring:
        print("ℹ️  Keine Events mit recurring-Config gefunden\n")
    
    # 2. Erkenne potentielle wiederkehrende Events
    print("="*80)
    print("🔍 ERKENNUNG WIEDERKEHRENDER PATTERNS")
    print("="*80)
    print()
    
    candidates = detector.detect_recurring_patterns()
    
    if candidates:
        print(f"Gefunden: {len(candidates)} potentiell wiederkehrende Event-Gruppen\n")
        
        for (title, location), data in candidates.items():
            print(f"🔄 \"{title}\" @ {location}")
            print(f"   Events: {data['count']}")
            print(f"   Pattern: {data['pattern']['frequency']}")
            if data['pattern'].get('by_day'):
                print(f"   Wochentage: {', '.join(data['pattern']['by_day'])}")
            print(f"   Konfidenz: {data['pattern']['confidence']:.0%}")
            print()
    else:
        print("ℹ️  Keine wiederkehrenden Patterns gefunden\n")
    
    # 3. Generiere Beispiel-Instanzen
    if events_with_recurring:
        print("="*80)
        print("📅 BEISPIEL: GENERIERTE INSTANZEN (nächste 30 Tage)")
        print("="*80)
        print()
        
        for file_path in EVENTS_DIR.glob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
                if match:
                    data = yaml.safe_load(match.group(1))
                    
                    if data.get('recurring', {}).get('enabled'):
                        print(f"📌 {data.get('title')}")
                        
                        instances = generator.generate_instances(data, days_ahead=30, max_instances=5)
                        
                        for i, inst in enumerate(instances[:5], 1):
                            print(f"   {i}. {inst['date']} - {data.get('start_time', 'N/A')}")
                        
                        if len(instances) > 5:
                            print(f"   ... und {len(instances) - 5} weitere")
                        
                        print()
            except Exception:
                pass
    
    # Zusammenfassung
    print("="*80)
    print("📊 ZUSAMMENFASSUNG")
    print("="*80)
    print(f"Events mit recurring-Config: {len(events_with_recurring)}")
    print(f"Validierungs-Fehler: {len(validation_errors)}")
    print(f"Erkannte Patterns: {len(candidates)}")
    print()


if __name__ == "__main__":
    main()
