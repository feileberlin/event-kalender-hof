#!/usr/bin/env python3
"""
JSON Schema Definitions für krawl.ist
Verwendet Python Dataclasses für Type Safety
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Literal
from datetime import datetime
import json
import hashlib


@dataclass
class Coordinates:
    """GPS-Koordinaten"""
    lat: float
    lng: float
    
    def __post_init__(self):
        # Validiere Deutschland-Bounds (grob)
        if not (47.0 <= self.lat <= 55.0):
            raise ValueError(f"Latitude {self.lat} außerhalb Deutschland")
        if not (5.0 <= self.lng <= 15.0):
            raise ValueError(f"Longitude {self.lng} außerhalb Deutschland")


@dataclass
class Place:
    """Veranstaltungsort (ex-Venue)"""
    name: str
    slug: str
    address: str
    coords: Coordinates
    wheelchair_accessible: bool = False
    public_transport: bool = False
    capacity: Optional[int] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    icon: str = "📍"
    color: str = "#2c3e50"
    
    def to_dict(self) -> Dict:
        return {
            **asdict(self),
            'coords': asdict(self.coords)
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Place':
        coords_data = data.pop('coords')
        coords = Coordinates(**coords_data)
        return Place(**data, coords=coords)


@dataclass
class Organizer:
    """Veranstalter (merged Organizer + Source)"""
    name: str
    slug: str
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    social_facebook: Optional[str] = None
    social_instagram: Optional[str] = None
    typical_places: List[str] = field(default_factory=list)
    verified_sources: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @staticmethod
    def from_dict(data: Dict) -> 'Organizer':
        return Organizer(**data)


@dataclass
class EventMeta:
    """Event-Metadaten"""
    scraped_at: str  # ISO datetime
    scraper_version: str = "2.0"
    confidence: float = 1.0
    needs_review: bool = False
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[str] = None
    hash: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class EventUrls:
    """Event-URLs"""
    source: Optional[str] = None
    tickets: Optional[str] = None
    detail: Optional[str] = None
    image: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Event:
    """
    Event-Schema V2 (JSON-First)
    
    Vereinfacht gegenüber Markdown:
    - Keine Markdown-Frontmatter-Komplexität
    - Direct JSON-Serialization
    - Hash-basierte Deduplication
    - Status-Tracking für Review-Workflow
    """
    id: str  # SHA256 Hash (deterministic)
    status: Literal["pending-review", "approved", "rejected", "published"] = "pending-review"
    title: str = ""
    date: str = ""  # YYYY-MM-DD
    start_time: str = ""  # HH:MM
    end_time: Optional[str] = None
    place: Optional[Dict] = None  # Place.to_dict()
    organizer: Optional[Dict] = None  # Organizer.to_dict()
    category: str = "Sonstiges"
    tags: List[str] = field(default_factory=list)
    description: str = ""
    urls: Optional[Dict] = None  # EventUrls.to_dict()
    meta: Optional[Dict] = None  # EventMeta.to_dict()
    
    def __post_init__(self):
        """Generate ID if not provided"""
        if not self.id:
            self.id = self.generate_id()
        
        # Ensure dicts are properly initialized
        if self.urls is None:
            self.urls = EventUrls().to_dict()
        if self.meta is None:
            self.meta = EventMeta(
                scraped_at=datetime.now().isoformat() + "Z"
            ).to_dict()
    
    def generate_id(self) -> str:
        """
        Generiert deterministische Event-ID (SHA256)
        
        Basiert auf:
        - Datum (exakt)
        - Titel (normalisiert)
        - Ort (normalisiert)
        - Start-Zeit (exakt)
        
        Vorteil gegenüber MD5:
        - Deterministisch (gleiche Eingabe → gleiche ID)
        - Keine Fuzzy-Logic
        - Einfach testbar
        """
        place_name = self.place.get('name', '') if self.place else ''
        
        # Normalisiere Strings
        title_norm = self.title.lower().strip()
        place_norm = place_name.lower().strip()
        
        # Hash-Input
        hash_input = f"{self.date}:{title_norm}:{place_norm}:{self.start_time}"
        
        # SHA256 (erste 16 Zeichen ausreichend für Collision-Resistance)
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
    
    def is_duplicate(self, other: 'Event') -> bool:
        """Prüft ob Event Duplikat ist (Hash-basiert)"""
        return self.id == other.id
    
    def to_dict(self) -> Dict:
        """Konvertiert zu JSON-serialisierbarem Dict"""
        return asdict(self)
    
    @staticmethod
    def from_dict(data: Dict) -> 'Event':
        """Erstellt Event aus Dict"""
        return Event(**data)
    
    def validate(self) -> List[str]:
        """
        Validiert Event-Daten
        Returns: Liste von Validierungs-Fehlern (leer = valid)
        """
        errors = []
        
        # Required Fields
        if not self.title:
            errors.append("title ist erforderlich")
        if not self.date:
            errors.append("date ist erforderlich")
        if not self.start_time:
            errors.append("start_time ist erforderlich")
        
        # Date Format
        if self.date:
            try:
                datetime.strptime(self.date, "%Y-%m-%d")
            except ValueError:
                errors.append(f"date '{self.date}' hat falsches Format (erwartet: YYYY-MM-DD)")
        
        # Time Format
        if self.start_time:
            if not self._is_valid_time(self.start_time):
                errors.append(f"start_time '{self.start_time}' hat falsches Format (erwartet: HH:MM)")
        
        if self.end_time and not self._is_valid_time(self.end_time):
            errors.append(f"end_time '{self.end_time}' hat falsches Format (erwartet: HH:MM)")
        
        # Status
        valid_statuses = ["pending-review", "approved", "rejected", "published"]
        if self.status not in valid_statuses:
            errors.append(f"status '{self.status}' ungültig (erlaubt: {valid_statuses})")
        
        return errors
    
    @staticmethod
    def _is_valid_time(time_str: str) -> bool:
        """Validiert Zeit-Format HH:MM"""
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False


@dataclass
class EventCollection:
    """
    Collection von Events mit Metadaten
    Repräsentiert _data/events.json oder Staging-Files
    """
    version: str = "2.0"
    schema: str = "https://krawl.ist/schema/events-v2.json"
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat() + "Z")
    generator: str = "krawl.ist-scraper-v2"
    meta: Dict = field(default_factory=dict)
    events: List[Event] = field(default_factory=list)
    
    def add_event(self, event: Event) -> bool:
        """
        Fügt Event hinzu (mit Duplikat-Check)
        Returns: True wenn hinzugefügt, False wenn Duplikat
        """
        for existing in self.events:
            if existing.is_duplicate(event):
                return False
        
        self.events.append(event)
        return True
    
    def to_dict(self) -> Dict:
        """Konvertiert zu JSON-serialisierbarem Dict"""
        return {
            'version': self.version,
            'schema': self.schema,
            'generated_at': self.generated_at,
            'generator': self.generator,
            'meta': self.meta,
            'events': [event.to_dict() for event in self.events]
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Konvertiert zu JSON-String"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)
    
    @staticmethod
    def from_dict(data: Dict) -> 'EventCollection':
        """Erstellt EventCollection aus Dict"""
        events_data = data.pop('events', [])
        events = [Event.from_dict(e) for e in events_data]
        return EventCollection(**data, events=events)
    
    @staticmethod
    def from_json(json_str: str) -> 'EventCollection':
        """Erstellt EventCollection aus JSON-String"""
        data = json.loads(json_str)
        return EventCollection.from_dict(data)
    
    def validate_all(self) -> Dict[str, List[str]]:
        """
        Validiert alle Events
        Returns: Dict mit Event-IDs als Keys und Fehler-Listen als Values
        """
        validation_results = {}
        for event in self.events:
            errors = event.validate()
            if errors:
                validation_results[event.id] = errors
        return validation_results


# ============================================================
# Helper Functions
# ============================================================

def slugify(text: str) -> str:
    """
    Konvertiert Text zu URL-safe Slug
    
    Beispiel:
        "Freiheitshalle Hof" → "freiheitshalle-hof"
        "Stadt Hof (Saale)" → "stadt-hof-saale"
    """
    import re
    
    # Lowercase
    text = text.lower()
    
    # Umlaute ersetzen
    text = text.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    
    # Nur Alphanumerisch + Spaces
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    
    # Multiple Spaces → Single Dash
    text = re.sub(r'[\s-]+', '-', text)
    
    # Trim Dashes
    text = text.strip('-')
    
    return text


def validate_json_file(filepath: str) -> List[str]:
    """
    Validiert JSON-Datei gegen Schema
    Returns: Liste von Fehlern (leer = valid)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate Structure
        collection = EventCollection.from_dict(data)
        
        # Validate Events
        validation_results = collection.validate_all()
        
        if validation_results:
            errors = []
            for event_id, event_errors in validation_results.items():
                for error in event_errors:
                    errors.append(f"Event {event_id}: {error}")
            return errors
        
        return []  # No errors
        
    except json.JSONDecodeError as e:
        return [f"JSON Parse Error: {e}"]
    except Exception as e:
        return [f"Validation Error: {e}"]


# ============================================================
# CLI Helper (für Testing)
# ============================================================

if __name__ == "__main__":
    # Test Event Creation
    test_event = Event(
        id="",  # Will be auto-generated
        title="Test Event",
        date="2025-12-01",
        start_time="20:00",
        place={
            'name': 'Test Venue',
            'slug': 'test-venue',
            'address': 'Test Str. 1, 95028 Hof',
            'coords': {'lat': 50.32, 'lng': 11.92}
        },
        category="Test",
        description="Dies ist ein Test-Event"
    )
    
    print("📋 Test Event:")
    print(f"ID: {test_event.id}")
    print(f"Valid: {len(test_event.validate()) == 0}")
    print()
    
    # Test Collection
    collection = EventCollection()
    added = collection.add_event(test_event)
    print(f"Event added: {added}")
    
    # Try to add duplicate
    duplicate = Event.from_dict(test_event.to_dict())
    added_duplicate = collection.add_event(duplicate)
    print(f"Duplicate added: {added_duplicate}")
    
    print()
    print("📄 JSON Output:")
    print(collection.to_json())
