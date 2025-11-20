# 🔄 Deduplication & Enrichment System

## Überblick

Das Deduplication & Enrichment System erkennt automatisch **Duplikate** von Events, die auf **mehreren Quellen** gefunden wurden, und **merged** sie intelligent zu einem kanonischen Event mit den **besten verfügbaren Daten**.

## Konzept

### Problem
- Events werden oft auf mehreren Kanälen veröffentlicht (Facebook, Website, Newsletter)
- Unterschiedliche Quellen haben unterschiedliche Datenqualität
- Manuelles Zusammenführen ist zeitaufwändig und fehleranfällig

### Lösung
1. **Clustering**: Ähnliche Events werden automatisch gruppiert
2. **Confidence Scoring**: System bewertet, wie sicher es ist, dass es Duplikate sind
3. **Data Enrichment**: Beste Daten aus allen Quellen werden kombiniert
4. **Admin Review**: Redakteur entscheidet final über Merge

## Architektur

```
┌─────────────────────────────────────────────────────────────┐
│                     SCRAPING PHASE                          │
│  scrape_events.py sammelt Events von verschiedenen Quellen │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 DEDUPLICATION PHASE                         │
│  deduplication_engine.py erkennt Duplikate                 │
│  - Fuzzy-Matching (Titel, Datum, Ort)                      │
│  - Confidence Scoring (0.0 - 1.0)                          │
│  - Cluster-Bildung                                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  ENRICHMENT PHASE                           │
│  Merge der besten Daten aus allen Quellen:                │
│  - Längste Beschreibung                                    │
│  - Beste Bilder                                            │
│  - Alle Tags kombiniert                                    │
│  - Externe URLs gesammelt                                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   ADMIN REVIEW                              │
│  admin.html zeigt Review-Queue:                            │
│  - Duplikate mit niedrigem Confidence Score                │
│  - Links zu allen Originalquellen                          │
│  - Merge/Split/Ignore Aktionen                             │
└─────────────────────────────────────────────────────────────┘
```

## Dateien

### Datenbanken
- **`_data/organizers.csv`**: Veranstalter-Datenbank (Namen, typische Venues, Quellen)
- **`_data/event_clusters.csv`**: Cluster-Metadaten (Duplikat-IDs, Confidence)
- **`_data/admin_review_queue.json`**: Review-Queue für Admin-Interface

### Scripts
- **`scripts/deduplication_engine.py`**: Hauptengine für Deduplication
- **`admin.html`**: Admin-Interface (Tab "🔄 Duplikate")

## Usage

### 1. Events scrapen
```bash
python3 scripts/scrape_events.py
```

### 2. Duplikate erkennen
```bash
python3 scripts/deduplication_engine.py
```

Output:
```
🔍 Deduplication Engine gestartet...
📊 3 Veranstalter geladen
📄 47 Event-Dateien gefunden
  → 2025-12-15-weihnachtsmarkt-hof.md: Cluster cluster_1_a3f2b8c9
  → 2025-12-15-xmas-market.md: Cluster cluster_1_a3f2b8c9  ← Duplikat!
  
📊 Ergebnis: 42 Cluster gefunden
🔍 Veranstalter-Muster erkannt:
  Stadt Hof: 12 Events auf 3 Quellen
  
✅ 42 Cluster gespeichert in _data/event_clusters.csv
📝 5 Events benötigen Review
✅ Review-Queue gespeichert: _data/admin_review_queue.json
```

### 3. Admin Review
```bash
# Jekyll Server starten
bundle exec jekyll serve

# Browser öffnen
http://localhost:4000/event-kalender-hof/admin.html
```

Im Admin-Interface:
1. Tab **"🔄 Duplikate"** öffnen
2. Cluster mit niedrigem Confidence Score prüfen
3. Links zu Originalquellen öffnen
4. Entscheidung treffen:
   - **✅ Merge**: Duplikate zu kanonischem Event zusammenführen
   - **✂️ Split**: Nicht Duplikat, sondern unterschiedliche Events
   - **🚫 Ignore**: Cluster aus Queue entfernen

## Algorithmus

### Similarity-Matching

```python
def calculate_similarity(event1, event2):
    # Datum muss identisch sein
    if event1['date'] != event2['date']:
        return 0.0
    
    # Titel-Ähnlichkeit (60% Gewichtung)
    title_sim = SequenceMatcher(event1['title'], event2['title']).ratio()
    score = title_sim * 0.6
    
    # Location-Ähnlichkeit (30% Gewichtung)
    loc_sim = SequenceMatcher(event1['location'], event2['location']).ratio()
    score += loc_sim * 0.3
    
    # Zeit-Ähnlichkeit (10% Gewichtung, ±30min Toleranz)
    time_diff = abs(parse_time(event1['start_time']) - parse_time(event2['start_time']))
    if time_diff <= 30:
        score += 0.1
    
    return score  # 0.0 - 1.0
```

**Threshold**: 0.8 = sehr wahrscheinlich dasselbe Event

### Confidence Scoring

```python
if len(cluster.events) >= 3:
    confidence = 0.95  # 3+ Quellen = sehr sicher
elif len(cluster.events) == 2:
    confidence = 0.75  # 2 Quellen = ziemlich sicher
else:
    confidence = 0.5   # 1 Quelle = unklar
```

### Data Quality Scoring

```python
score = 0.0
checks = [
    ('title', 10),
    ('description', 15),
    ('image', 10),
    ('external_url', 7),
    ('tags', 10),
    ...
]

for field, weight in checks:
    if event[field]:
        score += weight

quality = score / max_score  # 0.0 - 1.0
```

## Veranstalter-Muster-Erkennung

Das System lernt, welche Veranstalter typischerweise welche Quellen nutzen:

```csv
name,aliases,verified_sources,typical_venues
Stadt Hof,"Stadtverwaltung","stadt-hof,facebook-stadt-hof","Freiheitshalle,Altstadt"
```

**Nutzen**:
- Automatisches Tagging neuer Events
- Plausibilitätschecks (Stadt Hof normalerweise nicht im Theater)
- Bessere Duplikat-Erkennung

## Admin-Interface Features

### Cluster-Karte
```
┌─────────────────────────────────────────────────────┐
│ 🎄 Weihnachtsmarkt Hof                [Hoch: 95%]  │
│ 📅 Fr., 15. Dezember 2025 | 📍 Altstadt Hof        │
├─────────────────────────────────────────────────────┤
│ Duplikate gefunden: 3 Quellen                       │
│ Cluster ID: cluster_1_a3f2b8c9                     │
│ Datenqualität: 85% ████████▌░                       │
│ Review nötig? ✅ Nein                               │
├─────────────────────────────────────────────────────┤
│ 🔗 Gefunden auf folgenden Quellen:                  │
│  • Stadt Hof (2025-11-20) → Quelle öffnen ↗        │
│  • Facebook Stadt Hof (2025-11-19) → Quelle öffnen ↗│
│  • Hofer Anzeiger (2025-11-18) → Quelle öffnen ↗   │
├─────────────────────────────────────────────────────┤
│ Beschreibung (merged):                              │
│ Der traditionelle Weihnachtsmarkt findet auch...    │
├─────────────────────────────────────────────────────┤
│ [✅ Merge] [✂️ Split] [🚫 Ignore] [📝 Details]     │
└─────────────────────────────────────────────────────┘
```

### Farbcodierung
- **Grün**: High Confidence (≥90%) - automatisch mergen möglich
- **Orange**: Medium Confidence (70-89%) - Review empfohlen
- **Rot**: Low Confidence (<70%) - manueller Check erforderlich

## Workflow-Integration

### Automatisierung mit GitHub Actions

```yaml
# .github/workflows/deduplication.yml
name: Event Deduplication

on:
  schedule:
    - cron: '0 2 * * *'  # Täglich 2:00 Uhr
  workflow_dispatch:

jobs:
  deduplicate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install Dependencies
        run: pip install -r requirements.txt
      
      - name: Run Deduplication
        run: python3 scripts/deduplication_engine.py
      
      - name: Commit Results
        run: |
          git config user.name "Deduplication Bot"
          git config user.email "bot@example.com"
          git add _data/event_clusters.csv _data/admin_review_queue.json
          git commit -m "chore: Update deduplication data [skip ci]"
          git push
```

## Erweiterte Features (Zukunft)

### 1. Machine Learning
- **Supervised Learning**: Aus manuellen Review-Entscheidungen lernen
- **Feature Engineering**: Bessere Similarity-Metriken

### 2. NLP-basierte Similarity
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embeddings1 = model.encode(event1['description'])
embeddings2 = model.encode(event2['description'])
similarity = cosine_similarity(embeddings1, embeddings2)
```

### 3. Automatisches Mergen
Bei **High Confidence** (≥95%) automatisch mergen ohne Review.

### 4. Conflict Resolution
```json
{
  "conflicts": [
    {
      "field": "start_time",
      "values": ["18:00", "18:30"],
      "sources": ["Facebook", "Website"],
      "resolution": "manual"
    }
  ]
}
```

## Troubleshooting

### "Review-Queue noch nicht generiert"
```bash
python3 scripts/deduplication_engine.py
```

### "ModuleNotFoundError: No module named 'yaml'"
```bash
pip install -r requirements.txt
```

### Zu viele False Positives
- **Threshold erhöhen**: In `deduplication_engine.py` Zeile 154: `if similarity >= 0.9` (statt 0.8)
- **Strengere Zeit-Toleranz**: Zeile 141: `if time_diff <= 15` (statt 30)

### Zu wenige Duplikate erkannt
- **Threshold senken**: `if similarity >= 0.7`
- **Fuzzy-Matching verbessern**: `from fuzzywuzzy import fuzz`

## Performance

- **47 Events**: ~2 Sekunden
- **500 Events**: ~15 Sekunden
- **5000 Events**: ~3 Minuten

**Optimierung**:
```python
# Caching für wiederholte Normalisierungen
from functools import lru_cache

@lru_cache(maxsize=1000)
def normalize_text(text: str) -> str:
    ...
```

## Lizenz

MIT - siehe [LICENSE](../LICENSE)
