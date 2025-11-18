# Test Suite für Event-Kalender Hof

## Übersicht

Diese Test Suite validiert die Konsistenz zwischen HTML-Formularen und JavaScript-Logik.

## Tests

### `test_filters.js`

Testet die Event-Filter-Funktionalität:

1. **HTML Validierung**: Prüft alle `<select>` Optionen im radiusFilter
2. **JavaScript Logik**: Validiert die Filter-Schwellwerte in `main.js`
3. **Distanzberechnung**: Simuliert Event-Filterung für alle Radius-Optionen
4. **Edge Cases**: Testet Grenzfälle (mit/ohne Standort, extreme Werte)

## Lokal ausführen

```bash
cd tests
node test_filters.js
```

## CI/CD Integration

Die Tests laufen automatisch via GitHub Actions bei jedem Push der Dateien:
- `index.html`
- `assets/js/main.js`
- `tests/**`

## Test-Konfiguration anpassen

In `test_filters.js` die Konstante `EXPECTED_RADIUS_OPTIONS` anpassen:

```javascript
const EXPECTED_RADIUS_OPTIONS = [
    { value: '999', label: 'Alle', shouldFilter: false },
    { value: '1', label: '10 min zu Fuß', shouldFilter: true },
    // ... weitere Optionen
];
```

## Was wird getestet?

### ✅ Konsistenz-Checks
- HTML `<option>` Werte stimmen mit erwarteten Werten überein
- JavaScript Filter-Schwellwert (`radiusFilter < 999`) ist korrekt
- "Alle" und "Taxi" Optionen werden nie gefiltert
- Distanz-Optionen (Fuß, Rad, ÖPNV) werden korrekt gefiltert

### ✅ Logik-Validierung
- Filter greift nur wenn `userLocation` gesetzt UND `radiusFilter < 999`
- Ohne Standort wird nie nach Distanz gefiltert
- Extreme Werte (999, 999999) werden korrekt behandelt

## Bei Fehlern

Tests schlagen fehl wenn:
- HTML Optionen nicht mit erwarteten Werten übereinstimmen
- JavaScript Filter-Logik inkonsistent ist
- Distanzberechnung falsche Events herausfiltert

**Fix:** Passen Sie entweder `index.html` oder `assets/js/main.js` an, sodass beide synchron sind.
