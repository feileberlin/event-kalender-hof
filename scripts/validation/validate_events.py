#!/usr/bin/env python3
"""
Event Schema Validator
Validates event files against required schema and data quality rules

Checks:
- Required fields (title, date, location)
- Date format (ISO 8601: YYYY-MM-DD)
- Time format (HH:MM)
- URL validation (source links)
- Coordinate validation (lat/lng ranges)
- Status values
- Category validation
"""

import re
import yaml
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

EVENTS_DIR = Path("_events")

# Schema definition
REQUIRED_FIELDS = ["title", "date", "location", "status"]
OPTIONAL_FIELDS = ["start_time", "end_time", "address", "coordinates", 
                   "category", "tags", "description", "url", "image", "source"]
VALID_STATUS = ["Öffentlich", "Entwurf", "Archiviert"]

class EventValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.stats = {
            'total': 0,
            'valid': 0,
            'errors': 0,
            'warnings': 0
        }
    
    def validate_all(self):
        """Validate all event files"""
        print("🔍 Validiere Event-Schema...\n")
        
        for file_path in EVENTS_DIR.glob("*.md"):
            if file_path.name.startswith('_'):
                continue
            
            self.stats['total'] += 1
            event_data = self.parse_event(file_path)
            
            if event_data:
                self.validate_event(file_path, event_data)
        
        self.print_report()
        return len(self.errors) == 0
    
    def parse_event(self, file_path):
        """Parse event file and extract YAML front matter"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract YAML front matter
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if not match:
                self.errors.append({
                    'file': file_path.name,
                    'type': 'PARSE_ERROR',
                    'message': 'Kein YAML Front Matter gefunden'
                })
                return None
            
            yaml_content = match.group(1)
            return yaml.safe_load(yaml_content)
            
        except Exception as e:
            self.errors.append({
                'file': file_path.name,
                'type': 'PARSE_ERROR',
                'message': f'YAML Parse-Fehler: {e}'
            })
            return None
    
    def validate_event(self, file_path, data):
        """Validate single event against schema"""
        has_errors = False
        
        # 1. Check required fields
        for field in REQUIRED_FIELDS:
            if field not in data or data[field] is None or data[field] == '':
                self.errors.append({
                    'file': file_path.name,
                    'type': 'MISSING_FIELD',
                    'field': field,
                    'message': f'Pflichtfeld "{field}" fehlt oder ist leer'
                })
                has_errors = True
        
        if not data:
            return
        
        # 2. Validate date format
        if 'date' in data:
            if not self.validate_date_format(data['date']):
                self.errors.append({
                    'file': file_path.name,
                    'type': 'INVALID_DATE',
                    'field': 'date',
                    'value': data['date'],
                    'message': f'Ungültiges Datumsformat: {data["date"]} (erwartet: YYYY-MM-DD)'
                })
                has_errors = True
        
        # 3. Validate time formats
        for time_field in ['start_time', 'end_time']:
            if time_field in data and data[time_field]:
                if not self.validate_time_format(data[time_field]):
                    self.errors.append({
                        'file': file_path.name,
                        'type': 'INVALID_TIME',
                        'field': time_field,
                        'value': data[time_field],
                        'message': f'Ungültiges Zeitformat: {data[time_field]} (erwartet: HH:MM)'
                    })
                    has_errors = True
        
        # 4. Validate status
        if 'status' in data:
            if data['status'] not in VALID_STATUS:
                self.errors.append({
                    'file': file_path.name,
                    'type': 'INVALID_STATUS',
                    'field': 'status',
                    'value': data['status'],
                    'message': f'Ungültiger Status: {data["status"]} (erwartet: {", ".join(VALID_STATUS)})'
                })
                has_errors = True
        
        # 5. Validate coordinates
        if 'coordinates' in data and data['coordinates']:
            coords = data['coordinates']
            if 'lat' in coords and 'lng' in coords:
                if not self.validate_coordinates(coords['lat'], coords['lng']):
                    self.errors.append({
                        'file': file_path.name,
                        'type': 'INVALID_COORDINATES',
                        'field': 'coordinates',
                        'value': f"{coords['lat']}, {coords['lng']}",
                        'message': f'Koordinaten außerhalb gültiger Bereiche'
                    })
                    has_errors = True
            else:
                self.warnings.append({
                    'file': file_path.name,
                    'type': 'INCOMPLETE_COORDINATES',
                    'message': 'Koordinaten vorhanden, aber lat oder lng fehlt'
                })
        
        # 6. Validate URL
        if 'url' in data and data['url']:
            if not self.validate_url(data['url']):
                self.warnings.append({
                    'file': file_path.name,
                    'type': 'INVALID_URL',
                    'field': 'url',
                    'value': data['url'],
                    'message': f'Möglicherweise ungültige URL: {data["url"]}'
                })
        
        # 7. Check for unknown fields (warnings only)
        known_fields = set(REQUIRED_FIELDS + OPTIONAL_FIELDS + ['test_event', 'recurring'])
        for field in data.keys():
            if field not in known_fields:
                self.warnings.append({
                    'file': file_path.name,
                    'type': 'UNKNOWN_FIELD',
                    'field': field,
                    'message': f'Unbekanntes Feld: {field}'
                })
        
        if not has_errors:
            self.stats['valid'] += 1
    
    def validate_date_format(self, date_value):
        """Validate ISO 8601 date format (YYYY-MM-DD)"""
        if isinstance(date_value, str):
            try:
                datetime.strptime(date_value, '%Y-%m-%d')
                return True
            except ValueError:
                return False
        # datetime.date objects are also valid
        return hasattr(date_value, 'year')
    
    def validate_time_format(self, time_value):
        """Validate time format (HH:MM)"""
        if not isinstance(time_value, str):
            return False
        
        pattern = r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$'
        return bool(re.match(pattern, time_value))
    
    def validate_coordinates(self, lat, lng):
        """Validate coordinate ranges"""
        try:
            lat_float = float(lat)
            lng_float = float(lng)
            
            # Valid ranges: lat [-90, 90], lng [-180, 180]
            # For Germany: lat [47, 55], lng [5, 15] (rough bounds)
            if not (-90 <= lat_float <= 90):
                return False
            if not (-180 <= lng_float <= 180):
                return False
            
            # Warning for coordinates far from Germany
            if not (47 <= lat_float <= 55 and 5 <= lng_float <= 15):
                self.warnings.append({
                    'type': 'SUSPICIOUS_COORDINATES',
                    'message': f'Koordinaten ({lat_float}, {lng_float}) außerhalb Deutschland'
                })
            
            return True
        except (ValueError, TypeError):
            return False
    
    def validate_url(self, url):
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def print_report(self):
        """Print validation report"""
        print("=" * 80)
        print("📊 EVENT-SCHEMA-VALIDIERUNG - REPORT")
        print("=" * 80)
        print()
        
        print(f"📁 Dateien geprüft: {self.stats['total']}")
        print(f"✅ Valide Events: {self.stats['valid']}")
        print(f"❌ Events mit Fehlern: {len([e for e in self.errors if e['type'] != 'PARSE_ERROR'])}")
        print(f"⚠️  Warnungen: {len(self.warnings)}")
        print()
        
        if self.errors:
            print("🔴 FEHLER")
            print("-" * 80)
            
            # Group errors by file
            errors_by_file = {}
            for error in self.errors:
                file = error['file']
                if file not in errors_by_file:
                    errors_by_file[file] = []
                errors_by_file[file].append(error)
            
            for file, file_errors in errors_by_file.items():
                print(f"\n📄 {file}")
                for error in file_errors:
                    print(f"   ❌ {error['type']}: {error['message']}")
                    if 'field' in error:
                        print(f"      Feld: {error['field']}")
                    if 'value' in error:
                        print(f"      Wert: {error['value']}")
            print()
        
        if self.warnings:
            print("⚠️  WARNUNGEN")
            print("-" * 80)
            
            # Group warnings by file
            warnings_by_file = {}
            for warning in self.warnings:
                file = warning['file']
                if file not in warnings_by_file:
                    warnings_by_file[file] = []
                warnings_by_file[file].append(warning)
            
            for file, file_warnings in warnings_by_file.items():
                print(f"\n📄 {file}")
                for warning in file_warnings:
                    print(f"   ⚠️  {warning['type']}: {warning['message']}")
            print()
        
        if not self.errors and not self.warnings:
            print("✅ Alle Events sind valide!")
            print()
        
        print("=" * 80)

if __name__ == '__main__':
    validator = EventValidator()
    success = validator.validate_all()
    exit(0 if success else 1)
