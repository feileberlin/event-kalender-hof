# Event-Datums-Validierung & Qualitätssicherung

## 🚨 Problem: Veröffentlichungsdatum vs. Event-Datum

### Symptome

Bei der Analyse vorhandener Events wurde festgestellt:
- **12 Events** mit Datum in der Vergangenheit (17.-18. November)
- **6 Events** am gleichen Tag (17.11.) von gleicher Quelle
- Text enthält "heute" aber Datum liegt 2 Tage zurück

**Root Cause**: Beim Scraping wurde das **Veröffentlichungsdatum** statt des **tatsächlichen Event-Datums** extrahiert.

## 🛠️ Lösung: Multi-Layer-Validierung

### 1. **Validator-Script** (`scripts/validate_event_dates.py`)

Prüft existierende Events auf häufige Fehler:

```bash
python3 scripts/validate_event_dates.py
```

**Erkennt:**
- ❌ Events in der Vergangenheit (sollten archiviert sein)
- ⚠️ Verdächtige Datums-Cluster (alle am gleichen Tag)
- 🔄 Wiederkehrende Events (gleicher Titel, verschiedene Daten)
- 🚨 Inkonsistente Text-Referenzen ("heute" aber altes Datum)
- 📝 Dateiname-Mismatches (Dateiname ≠ Event-Datum)

**Output-Beispiel:**
```
🔴 EVENTS IN DER VERGANGENHEIT
   Anzahl: 12
   
   • Karaoke-Abend im Butler's
     Datum: 2025-11-17 (2 Tage her)
     Status: Öffentlich | Quelle: Hof Programm
     
⚠️  VERDACHT: VERÖFFENTLICHUNGSDATUM STATT EVENT-DATUM
   • Datum: 2025-11-17 - 6 Events
     Quelle: Hof Programm
```

### 2. **Date Enhancer** (`scripts/editorial/date_enhancer.py`)

Hilfsklasse für intelligente Datumserkennung beim Scraping:

**Features:**
- **Kontext-basiertes Parsing**: Analysiert umgebenden Text
- **Konfidenz-Scoring**: 0.0-1.0 (wie sicher ist das Datum?)
- **Warnung-System**: Liste von Problemen
- **Multi-Source-Vergleich**: Kombiniert Daten aus mehreren Quellen
- **Recurring Detection**: Erkennt wiederkehrende Events

**Verwendung im Scraping:**
```python
from date_enhancer import DateEnhancer

enhancer = DateEnhancer()

# Datum mit Kontext parsen
event_date, confidence, warnings = enhancer.parse_date_with_context(
    date_text="17.11.2025",
    context_text="Heute Abend im Butler's",  # ⚠️ "heute" erkannt!
    source_url="https://example.com/events"
)

# confidence = 0.15 (sehr niedrig!)
# warnings = ["VORSICHT: Text enthält 'heute' - evtl. Veröffentlichungsdatum?"]

# Event nur erstellen wenn Konfidenz > 0.5
if confidence > 0.5:
    create_event(event_date)
else:
    log_low_confidence_event(event_date, warnings)
```

**Recurring Events erkennen:**
```python
result = enhancer.detect_recurring_pattern(
    title="Karaoke-Abend",
    description="Jeden Sonntag ab 20 Uhr"
)
# {'is_recurring': True, 'pattern': 'weekly', 'keyword': 'jeden sonntag'}
```

**Mehrere Quellen vergleichen:**
```python
sources = [
    {'source': 'Stadt Hof', 'date': date(2025, 11, 25), 'confidence': 0.8},
    {'source': 'Facebook', 'date': date(2025, 11, 25), 'confidence': 0.9},
    {'source': 'Flyer', 'date': date(2025, 11, 26), 'confidence': 0.3},
]

suggestion = enhancer.suggest_date_from_multiple_sources(sources)
# Wählt 25.11. (2 Quellen, höhere Konfidenz)
```

### 3. **Scraping-Logging** (bereits implementiert)

Jedes Scraping erstellt detailliertes Log in `_events/_logs/`:

```log
[18:01:01] [INFO] 🔍 Event gefunden: 'Karaoke-Abend'
[18:01:01] [INFO]    📅 Datum: 2025-11-17 | ⏰ Zeit: 18:00
[18:01:01] [WARN] ⚠️  Konfidenz: 0.15 (NIEDRIG)
[18:01:01] [WARN]    Warnung: Text enthält 'heute' - evtl. Veröffentlichungsdatum?
[18:01:01] [INFO] 💾 Event als ENTWURF gespeichert (manuelle Prüfung nötig)
```

## 📋 Best Practices für Scraping

### ✅ DO:

1. **Mehrere Quellen nutzen**
   ```python
   # Datum aus verschiedenen Stellen extrahieren
   date_header = extract_date_from_header()
   date_meta = extract_date_from_meta_tags()
   date_body = extract_date_from_event_description()
   
   # Vergleichen
   suggestion = enhancer.suggest_date_from_multiple_sources([...])
   ```

2. **Kontext analysieren**
   ```python
   # Nicht nur Datum parsen, sondern Kontext prüfen
   date, conf, warnings = enhancer.parse_date_with_context(
       date_text=date_str,
       context_text=full_description  # WICHTIG!
   )
   ```

3. **Konfidenz prüfen**
   ```python
   if confidence < 0.5:
       # Als Entwurf mit Warnung speichern
       event_data['status'] = 'Entwurf'
       event_data['warnings'] = warnings
   ```

4. **Wiederkehrende Events markieren**
   ```python
   recurring = enhancer.detect_recurring_pattern(title, description)
   if recurring['is_recurring']:
       event_data['recurring'] = recurring['pattern']
       event_data['recurring_note'] = f"Automatisch erkannt: {recurring['keyword']}"
   ```

5. **Validierung vor dem Speichern**
   ```python
   validation = enhancer.validate_date_consistency(event_data)
   if not validation['is_valid']:
       logger.log_error(f"Validierung fehlgeschlagen: {validation['issues']}")
   ```

### ❌ DON'T:

1. **Relative Daten blind verwenden**
   ```python
   # ❌ FALSCH
   if "heute" in text:
       event_date = datetime.now().date()  # = Scraping-Datum!
   
   # ✅ RICHTIG
   date, conf, warnings = enhancer.parse_date_with_context(date_text, context_text)
   if "heute" in warnings:
       logger.log_warning("Relatives Datum 'heute' gefunden - Prüfung nötig")
       event_data['status'] = 'Entwurf'
   ```

2. **Erste gefundene Datum nehmen**
   ```python
   # ❌ FALSCH
   date = soup.find('time')['datetime']  # Könnte Veröffentlichungsdatum sein!
   
   # ✅ RICHTIG
   dates = []
   dates.append(('header', extract_from_header()))
   dates.append(('meta', extract_from_meta()))
   dates.append(('body', extract_from_body()))
   
   suggestion = enhancer.suggest_date_from_multiple_sources(dates)
   ```

3. **Ohne Validierung speichern**
   ```python
   # ❌ FALSCH
   save_event(event_data)  # Status sofort "Öffentlich"
   
   # ✅ RICHTIG
   validation = enhancer.validate_date_consistency(event_data)
   if validation['confidence'] < 0.7:
       event_data['status'] = 'Entwurf'  # Manuelle Prüfung
   save_event(event_data)
   ```

## 🔄 Workflow

### Automatisches Scraping

1. **Scraping läuft** (manuell oder GitHub Actions)
2. **Date Enhancer** validiert jedes Datum
3. **Konfidenz-Check**:
   - `>= 0.7`: Event mit Status "Öffentlich"
   - `0.5-0.7`: Event mit Status "Entwurf" + Warnung
   - `< 0.5`: Event übersprungen + Logfile-Eintrag
4. **Logging**: Alle Entscheidungen in `_events/_logs/TIMESTAMP-scraping.log`

### Manuelle Prüfung

1. **Validator ausführen**:
   ```bash
   python3 scripts/validate_event_dates.py
   ```

2. **Report prüfen**:
   - Events in Vergangenheit → Archivieren?
   - Verdächtige Cluster → Quelle nochmal checken
   - Wiederkehrende Events → `recurring`-Feld hinzufügen

3. **Admin-Bereich nutzen**: `/admin/`
   - Filter: `status:Entwurf`
   - Events mit Warnungen prüfen
   - Datum korrigieren falls nötig
   - Status auf "Öffentlich" ändern

## 📊 Metriken

Der Validator zeigt Statistiken:
- Anzahl vergangener Events
- Anzahl verdächtiger Cluster
- Anzahl wiederkehrender Events
- Anzahl Dateiname-Mismatches

**Ziel**: Alle Metriken bei 0!

## 🚀 Zukünftige Verbesserungen

1. **AI-basierte Datumserkennung**
   - GPT-4 Vision für Flyer-Analyse
   - Vergleich extrahiertes Datum vs. AI-Vorschlag

2. **Cross-Reference mit offiziellen Quellen**
   - Stadt Hof Website API
   - Freiheitshalle Kalender
   - Facebook Events

3. **Automatic Fixing**
   - Bei hoher Konfidenz: Auto-Korrektur
   - Bei niedriger Konfidenz: Entwurf mit Vorschlag

4. **Recurring Events System**
   - RRULE-Format (iCalendar)
   - Automatische Instanz-Generierung
   - "Nächstes Event" Feature

## 📚 Weitere Dokumentation

- `scripts/validate_event_dates.py` - Validator-Script
- `scripts/editorial/date_enhancer.py` - Date Enhancer Klasse
- `scripts/editorial/scrape_events.py` - Scraping mit Logging
- `_events/_logs/README.md` - Logging-System
