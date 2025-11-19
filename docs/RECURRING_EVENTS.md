# Wiederkehrende Events - Schema & Implementierung

## Event-Schema Erweiterung

### Neue YAML-Felder für `_events/*.md`:

```yaml
---
title: "Karaoke-Abend im Butler's"
date: 2025-11-17
start_time: "18:00"
end_time: "02:00"
location: "Butler's Café - Restaurant - Bar"

# ===== WIEDERKEHRENDE EVENTS =====
recurring:
  enabled: true                    # true = wiederkehrend, false/null = einmalig
  frequency: "weekly"              # daily, weekly, biweekly, monthly, yearly
  interval: 1                      # Alle N Wochen/Monate (z.B. 2 = alle 2 Wochen)
  by_day: ["SU"]                   # Wochentage: MO, TU, WE, TH, FR, SA, SU
  by_month_day: null               # Tag im Monat (1-31) für monthly
  start_date: "2025-11-17"         # Ab wann wiederkehrend (Default: date)
  end_date: null                   # Bis wann (null = unendlich)
  exceptions:                      # Ausnahmen (keine Events an diesen Tagen)
    - "2025-12-24"                 # Weihnachten
    - "2025-12-31"                 # Silvester
  
# Alternative: RRULE-Format (iCalendar Standard)
rrule: "FREQ=WEEKLY;BYDAY=SU;UNTIL=20261231T235959Z"

category: "Musik"
status: "Öffentlich"
---
```

## Frequency-Werte

| Wert | Beschreibung | Beispiel |
|------|--------------|----------|
| `daily` | Täglich | Frühsport jeden Morgen |
| `weekly` | Wöchentlich | Karaoke jeden Sonntag |
| `biweekly` | Alle 2 Wochen | Stammtisch alle 2 Wochen |
| `monthly` | Monatlich | Erster Freitag im Monat |
| `yearly` | Jährlich | Stadtfest jedes Jahr |

## Wochentage (by_day)

| Code | Wochentag |
|------|-----------|
| `MO` | Montag |
| `TU` | Dienstag |
| `WE` | Mittwoch |
| `TH` | Donnerstag |
| `FR` | Freitag |
| `SA` | Samstag |
| `SU` | Sonntag |

## Beispiele

### 1. Wöchentliches Event (jeden Sonntag)

```yaml
recurring:
  enabled: true
  frequency: "weekly"
  interval: 1
  by_day: ["SU"]
  start_date: "2025-11-17"
  end_date: null
  exceptions:
    - "2025-12-24"  # Weihnachten
    - "2025-12-31"  # Silvester
```

### 2. Monatliches Event (erster Freitag)

```yaml
recurring:
  enabled: true
  frequency: "monthly"
  interval: 1
  by_day: ["FR"]
  by_month_day: null  # Oder: [1-7] für erste Woche
  start_date: "2025-11-01"
  end_date: "2026-12-31"
  exceptions: []
```

### 3. Alle 2 Wochen (Dienstag)

```yaml
recurring:
  enabled: true
  frequency: "weekly"
  interval: 2
  by_day: ["TU"]
  start_date: "2025-11-19"
  end_date: null
  exceptions: []
```

### 4. Täglich (außer Wochenende)

```yaml
recurring:
  enabled: true
  frequency: "daily"
  interval: 1
  by_day: ["MO", "TU", "WE", "TH", "FR"]
  start_date: "2025-11-01"
  end_date: null
  exceptions:
    - "2025-12-24"
    - "2025-12-25"
    - "2025-12-26"
```

### 5. Jährliches Event (Stadtfest)

```yaml
recurring:
  enabled: true
  frequency: "yearly"
  interval: 1
  by_month_day: 15  # Immer am 15. des Monats
  start_date: "2025-06-15"
  end_date: null
  exceptions: []
```

## RRULE-Format (Alternative)

iCalendar RRULE ist ein Standard für wiederkehrende Events:

```yaml
# Jeden Sonntag bis Ende 2026
rrule: "FREQ=WEEKLY;BYDAY=SU;UNTIL=20261231T235959Z"

# Jeden ersten Freitag im Monat
rrule: "FREQ=MONTHLY;BYDAY=1FR"

# Alle 2 Wochen am Dienstag
rrule: "FREQ=WEEKLY;INTERVAL=2;BYDAY=TU"

# Täglich außer Samstag/Sonntag
rrule: "FREQ=DAILY;BYDAY=MO,TU,WE,TH,FR"
```

**Vorteil**: Standard-Format, kompatibel mit iCalendar/ICS  
**Nachteil**: Komplexere Syntax

## Default-Werte

| Feld | Default | Bedeutung |
|------|---------|-----------|
| `enabled` | `false` | Nicht wiederkehrend |
| `start_date` | `date` | Ab Event-Datum |
| `end_date` | `null` | Unendlich |
| `interval` | `1` | Jeden Zyklus |
| `exceptions` | `[]` | Keine Ausnahmen |

## Frontend-Darstellung

### Event-Liste

```
🔄 Karaoke-Abend im Butler's
   📅 Jeden Sonntag ab 18:00 Uhr
   📍 Butler's Café
   ⏰ Nächster Termin: 24.11.2025
```

### Event-Detail

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 WIEDERKEHRENDES EVENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Rhythmus: Jeden Sonntag
Start: 17.11.2025
Ende: Unbegrenzt
Ausnahmen: 24.12.2025, 31.12.2025

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 NÄCHSTE TERMINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• 24.11.2025 - 18:00 Uhr
• 01.12.2025 - 18:00 Uhr
• 08.12.2025 - 18:00 Uhr
• 15.12.2025 - 18:00 Uhr
• 22.12.2025 - 18:00 Uhr

[Alle Termine anzeigen]
```

## JavaScript-Integration

### Event-Generierung

```javascript
function generateRecurringInstances(event, startDate, endDate, maxInstances = 10) {
    if (!event.recurring || !event.recurring.enabled) {
        return [event];  // Einmaliges Event
    }
    
    const instances = [];
    const recurring = event.recurring;
    const start = new Date(recurring.start_date || event.date);
    const end = recurring.end_date ? new Date(recurring.end_date) : null;
    
    let current = new Date(start);
    let count = 0;
    
    while (count < maxInstances && (!end || current <= end)) {
        // Prüfe ob Tag in by_day enthalten
        const dayName = ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'][current.getDay()];
        
        if (!recurring.by_day || recurring.by_day.includes(dayName)) {
            const dateStr = current.toISOString().split('T')[0];
            
            // Prüfe Ausnahmen
            if (!recurring.exceptions || !recurring.exceptions.includes(dateStr)) {
                instances.push({
                    ...event,
                    date: dateStr,
                    is_recurring_instance: true,
                    recurring_parent: event.title
                });
                count++;
            }
        }
        
        // Nächster Termin
        switch (recurring.frequency) {
            case 'daily':
                current.setDate(current.getDate() + recurring.interval);
                break;
            case 'weekly':
                current.setDate(current.getDate() + 7 * recurring.interval);
                break;
            case 'monthly':
                current.setMonth(current.getMonth() + recurring.interval);
                break;
            case 'yearly':
                current.setFullYear(current.getFullYear() + recurring.interval);
                break;
        }
    }
    
    return instances;
}
```

### Filter-Integration

```javascript
// In main.js
function filterAndDisplayEvents() {
    let filtered = allEvents;
    
    // Generiere wiederkehrende Instanzen
    filtered = filtered.flatMap(event => {
        if (event.recurring && event.recurring.enabled) {
            const today = new Date();
            const future = new Date(today);
            future.setDate(today.getDate() + 60);  // Nächste 60 Tage
            
            return generateRecurringInstances(event, today, future, 10);
        }
        return [event];
    });
    
    // Restliche Filter anwenden...
    filtered = filterByCategory(filtered);
    filtered = filterByTime(filtered);
    // ...
}
```

## Backend-Integration (Jekyll)

### Liquid-Filter

`_plugins/recurring_events.rb`:

```ruby
module RecurringEventsFilter
  def generate_recurring(events, days_ahead = 60)
    result = []
    
    events.each do |event|
      if event['recurring'] && event['recurring']['enabled']
        # Generiere Instanzen
        instances = generate_instances(event, days_ahead)
        result.concat(instances)
      else
        result << event
      end
    end
    
    result.sort_by { |e| e['date'] }
  end
  
  def is_recurring(event)
    event['recurring'] && event['recurring']['enabled']
  end
  
  def next_occurrence(event)
    # Berechne nächsten Termin
    # ...
  end
end

Liquid::Template.register_filter(RecurringEventsFilter)
```

Verwendung in Templates:

```liquid
{% assign all_events = site.events | generate_recurring: 60 %}

{% for event in all_events %}
  {% if event.is_recurring_instance %}
    <span class="badge">🔄 Wiederkehrend</span>
  {% endif %}
  
  <h3>{{ event.title }}</h3>
  <p>{{ event.date | date: "%d.%m.%Y" }}</p>
{% endfor %}
```

## Validierung

### Schema-Validierung

```python
# In date_enhancer.py oder neues recurring_validator.py

def validate_recurring_config(recurring_data):
    """Validiert wiederkehrende Event-Konfiguration"""
    errors = []
    
    if not isinstance(recurring_data, dict):
        return ["recurring muss ein Object sein"]
    
    # Frequency prüfen
    valid_frequencies = ['daily', 'weekly', 'biweekly', 'monthly', 'yearly']
    if recurring_data.get('frequency') not in valid_frequencies:
        errors.append(f"Ungültige frequency: {recurring_data.get('frequency')}")
    
    # by_day prüfen
    valid_days = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
    if recurring_data.get('by_day'):
        for day in recurring_data['by_day']:
            if day not in valid_days:
                errors.append(f"Ungültiger Wochentag: {day}")
    
    # Datum-Validierung
    start = recurring_data.get('start_date')
    end = recurring_data.get('end_date')
    
    if end and start and end < start:
        errors.append("end_date liegt vor start_date")
    
    # Interval prüfen
    interval = recurring_data.get('interval', 1)
    if not isinstance(interval, int) or interval < 1:
        errors.append("interval muss positive Ganzzahl sein")
    
    return errors
```

## Migration bestehender Events

Script: `scripts/migrate_to_recurring.py`

```python
#!/usr/bin/env python3
"""
Migriert bestehende Events zu recurring-Schema
Erkennt automatisch wiederkehrende Patterns
"""

from pathlib import Path
import yaml
import re
from collections import defaultdict

def detect_recurring_pattern(events):
    """Findet wiederkehrende Events (gleicher Titel/Location)"""
    title_groups = defaultdict(list)
    
    for event_file in events:
        with open(event_file) as f:
            content = f.read()
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if match:
                data = yaml.safe_load(match.group(1))
                key = (data.get('title'), data.get('location'))
                title_groups[key].append((event_file, data))
    
    # Finde Gruppen mit 2+ Events
    recurring_candidates = {
        k: v for k, v in title_groups.items() 
        if len(v) >= 2
    }
    
    return recurring_candidates

def suggest_recurring_config(events):
    """Schlägt recurring-Config basierend auf Daten vor"""
    dates = [e[1]['date'] for e in events]
    dates.sort()
    
    # Berechne Intervalle
    intervals = []
    for i in range(len(dates) - 1):
        delta = (dates[i+1] - dates[i]).days
        intervals.append(delta)
    
    # Erkenne Pattern
    if all(i == 7 for i in intervals):
        return {'frequency': 'weekly', 'interval': 1}
    elif all(i == 14 for i in intervals):
        return {'frequency': 'weekly', 'interval': 2}
    elif all(28 <= i <= 31 for i in intervals):
        return {'frequency': 'monthly', 'interval': 1}
    
    return None

# Ausführung
if __name__ == "__main__":
    events_dir = Path("_events")
    events = list(events_dir.glob("*.md"))
    
    candidates = detect_recurring_pattern(events)
    
    for (title, location), event_group in candidates.items():
        print(f"\n🔄 Gefunden: {title} @ {location}")
        print(f"   {len(event_group)} Events")
        
        config = suggest_recurring_config(event_group)
        if config:
            print(f"   Vorschlag: {config}")
```

## Admin-UI Integration

Erweiterung für `/admin.html`:

```html
<!-- Recurring Event Section -->
<div class="recurring-section">
  <h3>🔄 Wiederkehrendes Event</h3>
  
  <label>
    <input type="checkbox" id="recurring-enabled"> 
    Event wiederholt sich
  </label>
  
  <div id="recurring-config" style="display:none">
    <label>
      Rhythmus:
      <select id="recurring-frequency">
        <option value="daily">Täglich</option>
        <option value="weekly">Wöchentlich</option>
        <option value="biweekly">Alle 2 Wochen</option>
        <option value="monthly">Monatlich</option>
        <option value="yearly">Jährlich</option>
      </select>
    </label>
    
    <label>
      Alle N Wochen/Monate:
      <input type="number" id="recurring-interval" value="1" min="1">
    </label>
    
    <label>
      Wochentage:
      <div class="weekday-selector">
        <label><input type="checkbox" value="MO"> Mo</label>
        <label><input type="checkbox" value="TU"> Di</label>
        <label><input type="checkbox" value="WE"> Mi</label>
        <label><input type="checkbox" value="TH"> Do</label>
        <label><input type="checkbox" value="FR"> Fr</label>
        <label><input type="checkbox" value="SA"> Sa</label>
        <label><input type="checkbox" value="SU"> So</label>
      </div>
    </label>
    
    <label>
      Start-Datum:
      <input type="date" id="recurring-start">
    </label>
    
    <label>
      End-Datum (leer = unendlich):
      <input type="date" id="recurring-end">
    </label>
    
    <label>
      Ausnahmen (Komma-getrennt):
      <input type="text" id="recurring-exceptions" 
             placeholder="2025-12-24, 2025-12-31">
    </label>
  </div>
</div>
```

## Siehe auch

- `scripts/date_enhancer.py` - Automatic Recurring Detection
- `docs/DATE_VALIDATION.md` - Datums-Validierung
- `_events/README.md` - Event-Schema Referenz
