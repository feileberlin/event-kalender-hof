# Recurring Events - Erweiterte Features

## Allgemeingültige Logik für komplexe Wiederholungsmuster

Das System unterstützt eine flexible, kombinierbare Logik für wiederkehrende Events.

### 🎯 Kern-Konzepte

#### 1. **Base Pattern** (frequency + interval + by_day)
Definiert das Grundmuster der Wiederholung.

#### 2. **Position im Monat** (by_set_pos)
Für monatliche Events: Welcher Wochentag im Monat?

#### 3. **Exceptions** (exceptions)
Entfernt spezifische Termine aus dem Pattern.

#### 4. **Additions** (additions)
Fügt außerordentliche Termine hinzu.

### 📋 Kombinierbare Parameter

```yaml
recurring:
  # BASE PATTERN
  enabled: true                    # Ein/Aus-Schalter
  frequency: "monthly"             # daily, weekly, biweekly, monthly, yearly
  interval: 1                      # Alle N Zyklen
  by_day: ["TU"]                   # Wochentage: MO-SU (mehrere möglich!)
  
  # POSITION (nur bei monthly)
  by_set_pos: 2                    # 1=erster, 2=zweiter, -1=letzter, etc.
  
  # ZEITRAUM
  start_date: "2025-12-09"         # Start
  end_date: null                   # Ende (null = unendlich)
  
  # MODIFIKATOREN
  exceptions:                      # ENTFERNEN: Diese Termine fallen aus
    - "2025-12-24"                 
    - "2026-04-14"
  
  additions:                       # HINZUFÜGEN: Extra-Termine außerhalb Pattern
    - "2025-12-30"
    - "2026-01-05"
```

### 🔄 Logik-Ablauf

```
1. Generiere Base Pattern (frequency + interval + by_day + by_set_pos)
   ↓
2. Filtere Exceptions (entferne diese Termine)
   ↓
3. Füge Additions hinzu (ergänze Extra-Termine)
   ↓
4. Sortiere chronologisch
   ↓
5. Limitiere auf max_instances
```

### 💡 Use Cases & Beispiele

#### Use Case 1: Einfache Wiederholung
**"Jeden Mittwoch"**
```yaml
recurring:
  enabled: true
  frequency: "weekly"
  by_day: ["WE"]
  start_date: "2025-11-20"
```

#### Use Case 2: Mehrere Wochentage
**"Jeden Mittwoch UND Samstag"**
```yaml
recurring:
  enabled: true
  frequency: "weekly"
  by_day: ["WE", "SA"]  # ← Mehrere Tage!
  start_date: "2025-11-19"
  exceptions:
    - "2025-12-25"  # Weihnachten fällt aus
```

#### Use Case 3: N-ter Wochentag im Monat
**"Jeden 2. Dienstag im Monat"**
```yaml
recurring:
  enabled: true
  frequency: "monthly"
  by_day: ["TU"]
  by_set_pos: 2  # ← 2. Dienstag
  start_date: "2025-12-09"
```

#### Use Case 4: Erster/Letzter Wochentag
**"Jeden ersten Freitag im Monat"**
```yaml
recurring:
  enabled: true
  frequency: "monthly"
  by_day: ["FR"]
  by_set_pos: 1  # ← Erster Freitag
  start_date: "2025-12-05"
```

**"Jeden letzten Sonntag im Monat"**
```yaml
recurring:
  enabled: true
  frequency: "monthly"
  by_day: ["SU"]
  by_set_pos: -1  # ← Letzter Sonntag (-1 = von hinten)
  start_date: "2025-11-30"
```

#### Use Case 5: Komplex mit Ausnahmen & Zusatzterminen
**"Jeden 2. Dienstag, außer Feiertage, plus Sondertermine"**
```yaml
recurring:
  enabled: true
  frequency: "monthly"
  by_day: ["TU"]
  by_set_pos: 2
  start_date: "2025-12-09"
  exceptions:
    - "2025-12-24"  # Weihnachten
    - "2026-04-14"  # Ostern
  additions:
    - "2025-12-30"  # Jahresabschluss-Special
    - "2026-01-05"  # Neujahrs-Special
```

**Ergebnis:**
```
✓ 09.12.2025  (regulär: 2. Di im Dez)
✗ 24.12.2025  (exception: Weihnachten)
★ 30.12.2025  (addition: Extra-Termin!)
★ 05.01.2026  (addition: Extra-Termin!)
✓ 13.01.2026  (regulär: 2. Di im Jan)
✓ 10.02.2026  (regulär: 2. Di im Feb)
✗ 14.04.2026  (exception: Ostern)
```

#### Use Case 6: Alle 2 Wochen (biweekly)
**"Alle 2 Wochen am Donnerstag"**
```yaml
recurring:
  enabled: true
  frequency: "weekly"
  interval: 2  # ← Alle 2 Wochen
  by_day: ["TH"]
  start_date: "2025-11-21"
```

#### Use Case 7: Täglich außer Wochenende
**"Täglich Mo-Fr"**
```yaml
recurring:
  enabled: true
  frequency: "daily"
  by_day: ["MO", "TU", "WE", "TH", "FR"]  # ← Nur Werktage
  start_date: "2025-12-01"
  exceptions:
    - "2025-12-24"  # Heiligabend
    - "2025-12-25"  # 1. Weihnachtstag
    - "2025-12-26"  # 2. Weihnachtstag
```

### 🔢 by_set_pos - Position im Monat

| Wert | Bedeutung | Beispiel |
|------|-----------|----------|
| `1` | Erster | Erster Freitag im Monat |
| `2` | Zweiter | Zweiter Dienstag im Monat |
| `3` | Dritter | Dritter Mittwoch im Monat |
| `4` | Vierter | Vierter Donnerstag im Monat |
| `-1` | Letzter | Letzter Sonntag im Monat |
| `-2` | Vorletzter | Vorletzter Montag im Monat |

**Wichtig**: `by_set_pos` funktioniert nur mit `frequency: "monthly"` + `by_day`!

### 🚫 Exceptions vs 🎉 Additions

#### Exceptions (Ausnahmen)
- **Zweck**: Termine aus dem Pattern entfernen
- **Beispiele**: Feiertage, Betriebsferien, Wartungsarbeiten
- **Logik**: `IF date IN exceptions THEN skip`

```yaml
exceptions:
  - "2025-12-24"  # Heiligabend
  - "2025-12-25"  # 1. Weihnachtstag
  - "2025-12-31"  # Silvester
```

#### Additions (Zusatztermine)
- **Zweck**: Extra-Termine außerhalb des Patterns hinzufügen
- **Beispiele**: Sonder-Events, Jubiläen, spontane Termine
- **Logik**: `ADD date even if not in pattern`

```yaml
additions:
  - "2025-12-30"  # Jahresabschluss-Special
  - "2026-03-15"  # Jubiläums-Event
```

### 🎯 Kombinationsmatrix

| frequency | interval | by_day | by_set_pos | Beispiel |
|-----------|----------|--------|------------|----------|
| `daily` | 1 | - | - | Jeden Tag |
| `daily` | 1 | [MO-FR] | - | Jeden Werktag |
| `weekly` | 1 | [WE] | - | Jeden Mittwoch |
| `weekly` | 1 | [WE, SA] | - | Jeden Mi + Sa |
| `weekly` | 2 | [TU] | - | Alle 2 Wochen Di |
| `monthly` | 1 | - | - | Gleicher Tag jeden Monat |
| `monthly` | 1 | [FR] | 1 | Erster Fr jeden Monat |
| `monthly` | 1 | [TU] | 2 | Zweiter Di jeden Monat |
| `monthly` | 1 | [SU] | -1 | Letzter So jeden Monat |
| `yearly` | 1 | - | - | Jährlich (gleicher Tag) |

### 🔧 Implementierungs-Details

#### Algorithmus

```python
def generate_instances(event, days_ahead, max_instances):
    instances = []
    
    # 1. Durchlaufe alle Tage von start_date bis max_date
    for current_date in date_range(start_date, max_date):
        should_include = False
        
        # 2. Prüfe Frequency-Pattern
        if frequency == 'daily':
            should_include = check_daily(current_date, interval, by_day)
        
        elif frequency == 'weekly':
            should_include = check_weekly(current_date, interval, by_day)
        
        elif frequency == 'monthly':
            if by_set_pos:
                should_include = check_nth_weekday(current_date, by_day, by_set_pos)
            else:
                should_include = check_monthly(current_date, interval)
        
        # 3. Filtere Exceptions
        if should_include and current_date in exceptions:
            should_include = False
        
        # 4. Füge Instanz hinzu
        if should_include:
            instances.append(create_instance(current_date))
    
    # 5. Füge Additions hinzu
    for addition_date in additions:
        if addition_date not in [inst.date for inst in instances]:
            instances.append(create_instance(addition_date, is_addition=True))
    
    # 6. Sortiere & limitiere
    return sorted(instances)[:max_instances]
```

#### N-ter Wochentag Berechnung

```python
def is_nth_weekday_in_month(date, weekday, position):
    """
    Prüft ob date der N-te <weekday> im Monat ist
    
    Args:
        date: Zu prüfendes Datum
        weekday: Wochentag (z.B. "FR")
        position: 1=erster, 2=zweiter, -1=letzter
    """
    # 1. Finde alle <weekday> im Monat
    occurrences = [d for d in month_days(date) if d.weekday == weekday]
    
    # 2. Prüfe Position
    if position > 0:
        return date == occurrences[position - 1]  # 1-indexed
    else:
        return date == occurrences[position]  # -1 = letzter
```

### 📊 Validierung

```python
# by_set_pos nur mit frequency='monthly'
if by_set_pos and frequency != 'monthly':
    error("by_set_pos requires frequency='monthly'")

# by_set_pos erfordert by_day
if by_set_pos and not by_day:
    error("by_set_pos requires by_day")

# Position im gültigen Bereich
if by_set_pos and (by_set_pos < -5 or by_set_pos > 5 or by_set_pos == 0):
    error("by_set_pos must be 1-5 or -1 to -5")
```

### 🚀 Frontend-Integration

```javascript
function generateRecurringInstances(event, daysAhead = 60) {
    if (!event.recurring?.enabled) return [event];
    
    const instances = [];
    const current = new Date(event.recurring.start_date);
    const maxDate = addDays(new Date(), daysAhead);
    
    // Base Pattern
    while (current <= maxDate) {
        if (matchesPattern(current, event.recurring)) {
            if (!event.recurring.exceptions.includes(formatDate(current))) {
                instances.push(createInstance(event, current));
            }
        }
        current = addDays(current, 1);
    }
    
    // Additions
    for (const addDate of event.recurring.additions || []) {
        const date = new Date(addDate);
        if (date <= maxDate && !instances.find(i => i.date === addDate)) {
            instances.push(createInstance(event, date, {isAddition: true}));
        }
    }
    
    return instances.sort((a, b) => a.date.localeCompare(b.date));
}
```

### 📚 Weitere Dokumentation

- **[RECURRING_EVENTS.md](RECURRING_EVENTS.md)** - Vollständige Schema-Referenz
- **[recurring_validator.py](../scripts/recurring_validator.py)** - Python-Implementierung
- **[main.js](../assets/js/main.js)** - JavaScript-Integration (TODO)
