#!/usr/bin/env python3
"""
Deduplication & Enrichment Engine
Erkennt Duplikate, clustert Events und reichert Daten an
"""

import csv
import hashlib
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from difflib import SequenceMatcher
import yaml


class EventCluster:
    """Repräsentiert ein Cluster von ähnlichen/doppelten Events"""
    
    def __init__(self, cluster_id: str):
        self.cluster_id = cluster_id
        self.events = []  # Liste von Event-Dicts
        self.sources = set()  # Quellen, die dieses Event erwähnen
        self.canonical = None  # Das "beste" Event (vollständigste Daten)
        self.confidence = 0.0  # Wie sicher sind wir, dass es Duplikate sind?
    
    def add_event(self, event_data: Dict, source: str):
        """Fügt ein Event zum Cluster hinzu"""
        self.events.append(event_data)
        self.sources.add(source)
        self._update_canonical()
    
    def _update_canonical(self):
        """Bestimmt das kanonische Event (vollständigste Daten)"""
        if not self.events:
            return
        
        # Score-basierte Auswahl
        scored_events = []
        for event in self.events:
            score = 0
            
            # Längere Beschreibung = besser
            if event.get('description'):
                score += min(len(event['description']), 500) / 10
            
            # Hat Bild = besser
            if event.get('image'):
                score += 50
            
            # Hat externe URL = besser
            if event.get('external_url'):
                score += 30
            
            # Hat Preis-Info = besser
            if event.get('price'):
                score += 20
            
            # Hat End-Zeit = besser
            if event.get('end_time'):
                score += 10
            
            # Hat Tags = besser
            if event.get('tags'):
                score += len(event['tags']) * 5
            
            scored_events.append((score, event))
        
        # Bestes Event als kanonisch markieren
        scored_events.sort(key=lambda x: x[0], reverse=True)
        self.canonical = scored_events[0][1]
        
        # Confidence berechnen
        if len(self.events) >= 3:
            self.confidence = 0.95
        elif len(self.events) == 2:
            self.confidence = 0.75
        else:
            self.confidence = 0.5
    
    def merge_data(self) -> Dict:
        """Merged alle Event-Daten intelligent"""
        merged = self.canonical.copy()
        
        # Sammle alle einzigartigen Werte
        all_tags = set(merged.get('tags', []))
        all_sources = list(self.sources)
        descriptions = []
        external_urls = []
        
        for event in self.events:
            # Tags sammeln
            if event.get('tags'):
                all_tags.update(event['tags'])
            
            # Beschreibungen sammeln
            if event.get('description') and event['description'] not in descriptions:
                descriptions.append(event['description'])
            
            # Externe URLs sammeln
            if event.get('external_url') and event['external_url'] not in external_urls:
                external_urls.append(event['external_url'])
            
            # Besseres Bild übernehmen
            if not merged.get('image') and event.get('image'):
                merged['image'] = event['image']
            
            # Preis übernehmen wenn fehlt
            if not merged.get('price') and event.get('price'):
                merged['price'] = event['price']
            
            # End-Zeit übernehmen wenn fehlt
            if not merged.get('end_time') and event.get('end_time'):
                merged['end_time'] = event['end_time']
        
        # Merged-Daten einfügen
        merged['tags'] = sorted(list(all_tags))
        merged['verified_sources'] = all_sources
        merged['duplicate_count'] = len(self.events)
        merged['cluster_id'] = self.cluster_id
        merged['confidence_score'] = self.confidence
        
        # Zusätzliche Quellen als Metadaten
        if len(external_urls) > 1:
            merged['additional_urls'] = external_urls
        
        # Längste/beste Beschreibung
        if descriptions:
            merged['description'] = max(descriptions, key=len)
        
        return merged


class DeduplicationEngine:
    """Engine für Event-Deduplication und Enrichment"""
    
    def __init__(self):
        self.events_dir = Path("_events")
        self.clusters_csv = Path("_data/event_clusters.csv")
        self.organizers_csv = Path("_data/organizers.csv")
        
        self.clusters = {}  # cluster_id -> EventCluster
        self.event_signatures = {}  # signature -> cluster_id
        self.organizers = self.load_organizers()
    
    def load_organizers(self) -> Dict[str, Dict]:
        """Lädt Veranstalter-Datenbank"""
        organizers = {}
        if self.organizers_csv.exists():
            with open(self.organizers_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    organizers[row['name']] = {
                        'aliases': [a.strip() for a in row['aliases'].split(',') if a],
                        'verified_sources': [s.strip() for s in row['verified_sources'].split(',') if s],
                        'typical_venues': [v.strip() for v in row['typical_venues'].split(',') if v],
                        'website': row['website'],
                        'contact': row['contact']
                    }
        return organizers
    
    def generate_signature(self, event_data: Dict) -> str:
        """Generiert Signature für Similarity-Matching"""
        # Fuzzy-Matching basiert auf:
        # - Datum (exakt)
        # - Titel (normalisiert)
        # - Location (normalisiert)
        # - Zeit (±30min Toleranz)
        
        date = event_data.get('date', '')
        title = self.normalize_text(event_data.get('title', ''))
        location = self.normalize_text(event_data.get('location', ''))
        
        # Signature ohne Zeit (Zeit hat Fuzzy-Matching)
        signature = f"{date}:{title[:50]}:{location[:30]}"
        return hashlib.md5(signature.encode()).hexdigest()[:16]
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalisiert Text für Vergleich"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)  # Sonderzeichen entfernen
        text = re.sub(r'\s+', ' ', text)  # Multiple Spaces
        return text.strip()
    
    def calculate_similarity(self, event1: Dict, event2: Dict) -> float:
        """Berechnet Ähnlichkeit zwischen zwei Events (0.0 - 1.0)"""
        score = 0.0
        
        # Datum muss identisch sein (sonst 0.0)
        if event1.get('date') != event2.get('date'):
            return 0.0
        
        # Titel-Ähnlichkeit (60% Gewichtung)
        title1 = self.normalize_text(event1.get('title', ''))
        title2 = self.normalize_text(event2.get('title', ''))
        title_sim = SequenceMatcher(None, title1, title2).ratio()
        score += title_sim * 0.6
        
        # Location-Ähnlichkeit (30% Gewichtung)
        loc1 = self.normalize_text(event1.get('location', ''))
        loc2 = self.normalize_text(event2.get('location', ''))
        loc_sim = SequenceMatcher(None, loc1, loc2).ratio()
        score += loc_sim * 0.3
        
        # Zeit-Ähnlichkeit (10% Gewichtung)
        time1 = event1.get('start_time', '')
        time2 = event2.get('start_time', '')
        if time1 and time2:
            # Toleranz ±30min
            time_diff = abs(self.parse_time_to_minutes(time1) - self.parse_time_to_minutes(time2))
            if time_diff <= 30:
                score += 0.1
        
        return score
    
    @staticmethod
    def parse_time_to_minutes(time_str: str) -> int:
        """Konvertiert Zeit zu Minuten seit Mitternacht"""
        try:
            parts = time_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1]) if len(parts) > 1 else 0
            return hours * 60 + minutes
        except:
            return 0
    
    def find_or_create_cluster(self, event_data: Dict, source: str) -> str:
        """Findet existierendes Cluster oder erstellt neues"""
        signature = self.generate_signature(event_data)
        
        # Prüfe ob ähnliches Event bereits existiert
        best_match_cluster = None
        best_similarity = 0.0
        
        for cluster_id, cluster in self.clusters.items():
            similarity = self.calculate_similarity(event_data, cluster.canonical)
            
            # Threshold: 0.8 = sehr wahrscheinlich dasselbe Event
            if similarity >= 0.8 and similarity > best_similarity:
                best_similarity = similarity
                best_match_cluster = cluster_id
        
        if best_match_cluster:
            # Event zu existierendem Cluster hinzufügen
            self.clusters[best_match_cluster].add_event(event_data, source)
            return best_match_cluster
        else:
            # Neues Cluster erstellen
            cluster_id = f"cluster_{len(self.clusters) + 1}_{signature[:8]}"
            cluster = EventCluster(cluster_id)
            cluster.add_event(event_data, source)
            self.clusters[cluster_id] = cluster
            self.event_signatures[signature] = cluster_id
            return cluster_id
    
    def detect_organizer_patterns(self):
        """Erkennt Muster: Welcher Veranstalter nutzt welche Quellen?"""
        patterns = {}
        
        for cluster in self.clusters.values():
            # Extrahiere möglichen Veranstalter aus Event
            organizer = cluster.canonical.get('organizer', '')
            
            if organizer:
                if organizer not in patterns:
                    patterns[organizer] = {
                        'sources': set(),
                        'venues': set(),
                        'event_count': 0
                    }
                
                patterns[organizer]['sources'].update(cluster.sources)
                patterns[organizer]['venues'].add(cluster.canonical.get('location', ''))
                patterns[organizer]['event_count'] += 1
        
        return patterns
    
    def save_clusters(self):
        """Speichert Cluster-Informationen"""
        with open(self.clusters_csv, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['cluster_id', 'canonical_event_hash', 'duplicate_hashes', 
                         'sources_found', 'confidence_score', 'created_at', 'reviewed']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for cluster in self.clusters.values():
                duplicate_hashes = [e.get('event_hash', '') for e in cluster.events]
                
                writer.writerow({
                    'cluster_id': cluster.cluster_id,
                    'canonical_event_hash': cluster.canonical.get('event_hash', ''),
                    'duplicate_hashes': '|'.join(duplicate_hashes),
                    'sources_found': '|'.join(sorted(cluster.sources)),
                    'confidence_score': f"{cluster.confidence:.2f}",
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'reviewed': 'false'
                })
        
        print(f"✅ {len(self.clusters)} Cluster gespeichert in {self.clusters_csv}")
    
    def generate_admin_review_data(self) -> List[Dict]:
        """Generiert Daten für Admin-Review (Backend)"""
        review_data = []
        
        for cluster in self.clusters.values():
            if len(cluster.events) > 1:  # Nur Cluster mit Duplikaten
                merged = cluster.merge_data()
                
                # Sammle alle Quellen mit URLs
                source_links = []
                for event in cluster.events:
                    if event.get('source_url'):
                        source_links.append({
                            'source': event.get('source', 'Unbekannt'),
                            'url': event['source_url'],
                            'scraped_at': event.get('scraped_at', '')
                        })
                
                review_data.append({
                    'cluster_id': cluster.cluster_id,
                    'title': merged['title'],
                    'date': merged['date'],
                    'location': merged['location'],
                    'canonical_data': merged,
                    'duplicate_count': len(cluster.events),
                    'confidence': cluster.confidence,
                    'source_links': source_links,
                    'requires_review': cluster.confidence < 0.9,
                    'data_quality_score': self.calculate_data_quality(merged)
                })
        
        return review_data
    
    @staticmethod
    def calculate_data_quality(event_data: Dict) -> float:
        """Berechnet Datenqualität (0.0 - 1.0)"""
        score = 0.0
        max_score = 0.0
        
        checks = [
            ('title', 10),
            ('date', 10),
            ('start_time', 8),
            ('end_time', 5),
            ('location', 10),
            ('description', 15),
            ('image', 10),
            ('price', 5),
            ('external_url', 7),
            ('tags', 10),
            ('organizer', 10)
        ]
        
        for field, weight in checks:
            max_score += weight
            if event_data.get(field):
                score += weight
        
        return score / max_score if max_score > 0 else 0.0


def main():
    """Hauptfunktion für Testing"""
    engine = DeduplicationEngine()
    
    # Beispiel: Events laden und clustern
    print("🔍 Deduplication Engine gestartet...")
    print(f"📊 {len(engine.organizers)} Veranstalter geladen")
    
    # Demo: Events aus _events/ Verzeichnis laden und analysieren
    event_files = list(Path("_events").glob("*.md"))
    print(f"📄 {len(event_files)} Event-Dateien gefunden")
    
    for event_file in event_files[:20]:  # Test mit ersten 20
        try:
            with open(event_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Parse YAML Front Matter
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        event_data = yaml.safe_load(parts[1])
                        source = event_data.get('source', 'unknown')
                        
                        cluster_id = engine.find_or_create_cluster(event_data, source)
                        print(f"  → {event_file.name}: Cluster {cluster_id}")
        except Exception as e:
            print(f"  ❌ Fehler bei {event_file.name}: {e}")
    
    print(f"\n📊 Ergebnis: {len(engine.clusters)} Cluster gefunden")
    
    # Muster erkennen
    patterns = engine.detect_organizer_patterns()
    print(f"\n🔍 Veranstalter-Muster erkannt:")
    for org, data in patterns.items():
        print(f"  {org}: {data['event_count']} Events auf {len(data['sources'])} Quellen")
    
    # Clusters speichern
    engine.save_clusters()
    
    # Admin-Review-Daten generieren
    review_data = engine.generate_admin_review_data()
    print(f"\n📝 {len(review_data)} Events benötigen Review")
    
    # JSON für Admin-Interface
    import json
    review_json = Path("_data/admin_review_queue.json")
    with open(review_json, 'w', encoding='utf-8') as f:
        json.dump(review_data, f, indent=2, ensure_ascii=False, default=str)
    print(f"✅ Review-Queue gespeichert: {review_json}")


if __name__ == "__main__":
    main()
