#!/usr/bin/env python3
"""
Event-Datums-Verbesserer
Hilft bei der Erkennung und Korrektur von Datums-Fehlern beim Scraping
"""

from datetime import datetime, timedelta
import re

class DateEnhancer:
    """Hilfsmethoden zur Verbesserung der Datumserkennung beim Scraping"""
    
    @staticmethod
    def parse_date_with_context(date_text, context_text="", source_url=""):
        """
        Parst Datum mit Kontext-Informationen zur Vermeidung von Fehlern
        
        Args:
            date_text: Der Datums-Text aus der Quelle
            context_text: Umgebender Text für Kontext
            source_url: URL der Quelle (für Metadaten-Extraktion)
        
        Returns:
            tuple: (event_date, confidence_score, warnings)
        """
        warnings = []
        confidence = 1.0
        
        if not date_text:
            return None, 0.0, ["Kein Datums-Text vorhanden"]
        
        # Verschiedene Datumsformate probieren
        parsed_date = None
        formats = [
            ("%d.%m.%Y %H:%M", "Vollständig mit Uhrzeit"),
            ("%d.%m.%Y", "Vollständig ohne Uhrzeit"),
            ("%d. %B %Y", "Mit Monatsname"),
            ("%d.%m.", "Nur Tag und Monat (aktuelles Jahr)"),
        ]
        
        for fmt, description in formats:
            try:
                parsed_date = datetime.strptime(date_text.strip(), fmt)
                
                # Bei Formaten ohne Jahr: aktuelles oder nächstes Jahr?
                if "%Y" not in fmt:
                    current_year = datetime.now().year
                    parsed_date = parsed_date.replace(year=current_year)
                    
                    # Falls Datum in Vergangenheit, nehme nächstes Jahr
                    if parsed_date.date() < datetime.now().date():
                        parsed_date = parsed_date.replace(year=current_year + 1)
                        warnings.append(f"Datum lag in Vergangenheit, Jahr zu {current_year + 1} geändert")
                
                break
            except ValueError:
                continue
        
        if not parsed_date:
            # Relative Datumsangaben
            text_lower = date_text.lower()
            today = datetime.now()
            
            if "heute" in text_lower:
                parsed_date = today
                warnings.append("Relatives Datum 'heute' verwendet - VORSICHT: Event-Datum = Scraping-Datum!")
                confidence = 0.3  # Niedrige Konfidenz
            elif "morgen" in text_lower:
                parsed_date = today + timedelta(days=1)
                warnings.append("Relatives Datum 'morgen' verwendet")
                confidence = 0.5
            elif "übermorgen" in text_lower:
                parsed_date = today + timedelta(days=2)
                warnings.append("Relatives Datum 'übermorgen' verwendet")
                confidence = 0.5
        
        if not parsed_date:
            return None, 0.0, ["Datum konnte nicht geparst werden"]
        
        # Validierungen
        event_date = parsed_date.date() if isinstance(parsed_date, datetime) else parsed_date
        
        # Check 1: Liegt Datum zu weit in der Zukunft?
        days_future = (event_date - datetime.now().date()).days
        if days_future > 365:
            warnings.append(f"WARNUNG: Event liegt {days_future} Tage in der Zukunft - evtl. Jahresfehler?")
            confidence *= 0.7
        
        # Check 2: Liegt Datum in der Vergangenheit?
        if event_date < datetime.now().date():
            days_past = (datetime.now().date() - event_date).days
            warnings.append(f"WARNUNG: Event liegt {days_past} Tage in der Vergangenheit - evtl. Veröffentlichungsdatum statt Event-Datum?")
            confidence *= 0.3
        
        # Check 3: Kontext-Analyse
        if context_text:
            context_lower = context_text.lower()
            
            # Verdächtige Formulierungen
            if "heute" in context_lower or "ab heute" in context_lower:
                warnings.append("VORSICHT: Text enthält 'heute' - evtl. Veröffentlichungsdatum verwendet?")
                confidence *= 0.5
            
            # Positive Indikatoren
            if "am" in context_lower or "jeden" in context_lower:
                confidence *= 1.2  # Erhöht Konfidenz
        
        return event_date, min(confidence, 1.0), warnings
    
    @staticmethod
    def detect_recurring_pattern(title, description=""):
        """
        Erkennt wiederkehrende Events
        
        Returns:
            dict: {'is_recurring': bool, 'pattern': str, 'by_day': list, 'confidence': float}
        """
        text = f"{title} {description}".lower()
        
        # Wochentags-Mapping
        weekday_patterns = {
            'MO': ['montag', 'monday'],
            'TU': ['dienstag', 'tuesday'],
            'WE': ['mittwoch', 'wednesday'],
            'TH': ['donnerstag', 'thursday'],
            'FR': ['freitag', 'friday'],
            'SA': ['samstag', 'saturday'],
            'SU': ['sonntag', 'sunday']
        }
        
        # Erkenne einzelne Wochentage
        detected_days = []
        for day_code, keywords in weekday_patterns.items():
            for keyword in keywords:
                if f"jeden {keyword}" in text or f"jede {keyword}" in text or f"every {keyword}" in text:
                    detected_days.append(day_code)
                    break
        
        # Mehrere Wochentage (z.B. "mittwoch und samstag")
        if " und " in text or " und " in text:
            for day_code, keywords in weekday_patterns.items():
                for keyword in keywords:
                    if keyword in text:
                        if day_code not in detected_days:
                            detected_days.append(day_code)
        
        # Pattern-Typen
        patterns = {
            'daily': ['täglich', 'jeden tag', 'daily'],
            'weekly': ['wöchentlich', 'jede woche', 'weekly'] + 
                     [f"jeden {kw}" for kws in weekday_patterns.values() for kw in kws],
            'monthly': ['monatlich', 'jeden monat', 'monthly'],
            'yearly': ['jährlich', 'jedes jahr', 'annually'],
        }
        
        for pattern_type, keywords in patterns.items():
            for keyword in keywords:
                if keyword in text:
                    result = {
                        'is_recurring': True,
                        'pattern': pattern_type,
                        'confidence': 0.8,
                        'keyword': keyword
                    }
                    
                    # Füge erkannte Wochentage hinzu
                    if detected_days:
                        result['by_day'] = detected_days
                        result['confidence'] = 0.9  # Höhere Konfidenz bei konkreten Tagen
                    
                    return result
        
        return {'is_recurring': False, 'pattern': None, 'confidence': 0.0}
    
    @staticmethod
    def suggest_date_from_multiple_sources(sources_data):
        """
        Vergleicht Daten aus mehreren Quellen und schlägt wahrscheinlichstes vor
        
        Args:
            sources_data: List[dict] mit {'source': str, 'date': date, 'confidence': float}
        
        Returns:
            dict: {'suggested_date': date, 'confidence': float, 'reason': str}
        """
        if not sources_data:
            return None
        
        # Gewichtete Abstimmung
        date_votes = {}
        for source in sources_data:
            date = source['date']
            confidence = source.get('confidence', 0.5)
            
            if date not in date_votes:
                date_votes[date] = {'count': 0, 'total_confidence': 0, 'sources': []}
            
            date_votes[date]['count'] += 1
            date_votes[date]['total_confidence'] += confidence
            date_votes[date]['sources'].append(source['source'])
        
        # Sortiere nach Konfidenz-Summe
        sorted_dates = sorted(
            date_votes.items(), 
            key=lambda x: (x[1]['count'], x[1]['total_confidence']),
            reverse=True
        )
        
        if not sorted_dates:
            return None
        
        best_date, best_data = sorted_dates[0]
        
        return {
            'suggested_date': best_date,
            'confidence': best_data['total_confidence'] / best_data['count'],
            'votes': best_data['count'],
            'sources': best_data['sources'],
            'reason': f"{best_data['count']} Quelle(n) stimmen überein"
        }
    
    @staticmethod
    def extract_date_from_filename(filename):
        """Extrahiert Datum aus Dateiname (Format: YYYY-MM-DD-title.ext)"""
        match = re.match(r'(\d{4}-\d{2}-\d{2})-', filename)
        if match:
            try:
                return datetime.strptime(match.group(1), '%Y-%m-%d').date()
            except ValueError:
                pass
        return None
    
    @staticmethod
    def validate_date_consistency(event_data):
        """
        Validiert Konsistenz aller Datums-bezogenen Felder
        
        Returns:
            dict: {'is_valid': bool, 'issues': list, 'confidence': float}
        """
        issues = []
        confidence = 1.0
        
        # Prüfe Dateiname vs. event_date
        filename = event_data.get('filename', '')
        event_date = event_data.get('date')
        
        if filename and event_date:
            filename_date = DateEnhancer.extract_date_from_filename(filename)
            if filename_date and filename_date != event_date:
                issues.append(f"Dateiname ({filename_date}) stimmt nicht mit Event-Datum ({event_date}) überein")
                confidence *= 0.6
        
        # Prüfe Start- vs. End-Time
        start_time = event_data.get('start_time')
        end_time = event_data.get('end_time')
        
        if start_time and end_time:
            try:
                start = datetime.strptime(start_time, '%H:%M')
                end = datetime.strptime(end_time, '%H:%M')
                
                # End-Time vor Start-Time (über Mitternacht)
                if end < start:
                    # Das ist ok für Events über Mitternacht
                    pass
            except ValueError:
                issues.append("Ungültiges Zeitformat")
                confidence *= 0.8
        
        # Prüfe Text-Konsistenz
        title = event_data.get('title', '')
        description = event_data.get('description', '')
        text = f"{title} {description}".lower()
        
        if event_date:
            today = datetime.now().date()
            
            if ('heute' in text or 'ab heute' in text) and event_date != today:
                issues.append("Text enthält 'heute' aber Datum ist nicht heute")
                confidence *= 0.3
            
            if event_date < today:
                days_past = (today - event_date).days
                if days_past > 2:
                    issues.append(f"Event liegt {days_past} Tage in der Vergangenheit")
                    confidence *= 0.2
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'confidence': confidence
        }


# Beispiel-Verwendung
if __name__ == "__main__":
    enhancer = DateEnhancer()
    
    # Test 1: Parse Date
    print("Test 1: Datum parsen")
    date, conf, warnings = enhancer.parse_date_with_context(
        "17.11.2025",
        "Heute Abend im Butler's"
    )
    print(f"  Datum: {date}")
    print(f"  Konfidenz: {conf}")
    print(f"  Warnungen: {warnings}")
    print()
    
    # Test 2: Recurring Detection
    print("Test 2: Wiederkehrende Events")
    result = enhancer.detect_recurring_pattern(
        "Karaoke-Abend",
        "Jeden Sonntag ab 20 Uhr"
    )
    print(f"  Wiederkehrend: {result['is_recurring']}")
    print(f"  Pattern: {result['pattern']}")
    print()
    
    # Test 3: Multiple Sources
    print("Test 3: Mehrere Quellen")
    sources = [
        {'source': 'Website A', 'date': datetime(2025, 11, 25).date(), 'confidence': 0.8},
        {'source': 'Website B', 'date': datetime(2025, 11, 25).date(), 'confidence': 0.9},
        {'source': 'Website C', 'date': datetime(2025, 11, 26).date(), 'confidence': 0.6},
    ]
    suggestion = enhancer.suggest_date_from_multiple_sources(sources)
    print(f"  Vorgeschlagenes Datum: {suggestion['suggested_date']}")
    print(f"  Konfidenz: {suggestion['confidence']}")
    print(f"  Grund: {suggestion['reason']}")
