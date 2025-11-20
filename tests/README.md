# Test Suite für Event-Kalender Hof

## Übersicht

Diese Test Suite validiert die Konsistenz und Qualität des Event-Kalender-Codes.

## Tests

### 1. Filter Tests (`test_filters.js`)

Testet die Event-Filter-Funktionalität:

1. **HTML Validierung**: Prüft alle `<select>` Optionen im radiusFilter
2. **JavaScript Logik**: Validiert die Filter-Schwellwerte in `main.js`
3. **Distanzberechnung**: Simuliert Event-Filterung für alle Radius-Optionen
4. **Edge Cases**: Testet Grenzfälle (mit/ohne Standort, extreme Werte)

**Lokal ausführen:**
```bash
cd tests
node test_filters.js
```

### 2. Code Quality Validation

**HTML Validation:**
- Void elements korrekt (keine self-closing `/>`)
- Button `type` Attribute vorhanden
- Keine inline styles
- Raw `&` als `&amp;` encoded
- Semantic HTML structure

**CSS Validation:**
- Keine Duplikate
- Moderne Syntax (RGB ohne comma)
- Konsistente Struktur

**JavaScript Validation:**
- ESLint Standards
- Keine trailing spaces
- Konsistente Einrückung (4 spaces)
- Keine ungenutzten Variablen (außer onclick-Funktionen)

**Lokal ausführen:**
```bash
# HTML
bundle exec jekyll build
npx html-validate _site/index.html

# CSS
npx stylelint "assets/css/*.css"

# JavaScript
npx eslint assets/js/main.js
```

## CI/CD Integration

### Bei jedem Push

**Filter Tests** (`.github/workflows/test-filters.yml`):
- Trigger: Push zu `index.html` oder `assets/js/main.js`
- Läuft: Filter-Konsistenz Tests
- Dauer: ~30 Sekunden

**Code Validation** (`.github/workflows/validate-code.yml`):
- Trigger: Push zu `**.html`, `**.css`, `**.js`
- Läuft: HTML, CSS, JS Validation + Accessibility Checks
- Dauer: ~2 Minuten

### Monatlich

**Komplette Testbatterie** (`.github/workflows/monthly-tests.yml`):
- Trigger: 1. des Monats, 2:00 UTC
- Läuft: Alle Tests + Build Test + Event Files Check
- Dauer: ~5 Minuten

**Jobs:**
1. Filter Tests
2. Code Quality Validation
3. Build & Deploy Test
4. Summary Report

**Manuell starten:**
GitHub → Actions → "Monthly Test Suite" → "Run workflow"

## Test-Konfiguration anpassen

### Filter Tests

In `test_filters.js` die Konstante `EXPECTED_RADIUS_OPTIONS` anpassen:

```javascript
const EXPECTED_RADIUS_OPTIONS = [
    { value: '999', label: 'Alle', shouldFilter: false },
    { value: '1', label: '10 min zu Fuß', shouldFilter: true },
    // ... weitere Optionen
];
```

### Linting Rules

**ESLint** (`eslint.config.js`):
```javascript
rules: {
    'semi': ['error', 'always'],
    'indent': ['error', 4]
}
```

**Stylelint** (`.stylelintrc.json`):
```json
{
  "extends": "stylelint-config-standard"
}
```

## Was wird getestet?

### ✅ Konsistenz-Checks
- HTML `<option>` Werte stimmen mit erwarteten Werten überein
- JavaScript Filter-Schwellwert (`radiusFilter < 999`) ist korrekt
- "Alle" und "Taxi" Optionen werden nie gefiltert
- Distanz-Optionen (Fuß, Rad, ÖPNV) werden korrekt gefiltert

### ✅ Code Quality
- HTML: Semantic markup, accessibility attributes
- CSS: No duplicates, modern syntax
- JavaScript: Clean code, no trailing spaces
- KISS: Simplified, maintainable code

### ✅ Build Tests
- Jekyll baut ohne Fehler
- Python Scraper läuft
- Event Files vorhanden
- Deployment-ready

## Bei Fehlern

### Filter Tests schlagen fehl
- HTML Optionen nicht mit erwarteten Werten übereinstimmen → `index.html` anpassen
- JavaScript Filter-Logik inkonsistent → `assets/js/main.js` prüfen
- Distanzberechnung falsch → Logik in `main.js` korrigieren

### Code Validation schlägt fehl
- HTML: `npx html-validate _site/index.html` zeigt Fehler
- CSS: `npx stylelint "assets/css/*.css" --fix` automatisch korrigieren
- JS: `npx eslint assets/js/main.js --fix` automatisch korrigieren

### Build Test schlägt fehl
- Jekyll: `bundle exec jekyll build --verbose` für Details
- Python: `python scripts/editorial/scrape_events.py` testen
- Dependencies: `bundle install && pip install -r requirements.txt`

## Workflow Status

Alle Workflows haben Badges im README:
- 🟢 Grün: Alle Tests bestanden
- 🔴 Rot: Tests fehlgeschlagen → GitHub Actions für Details
- ⚪ Grau: Noch nicht gelaufen

**Status prüfen:**
GitHub → Actions → Workflow auswählen → Letzte Runs
