# Contributing to Event-Kalender Hof

Vielen Dank für dein Interesse, zum Event-Kalender Hof beizutragen! 🎉

## Wie kann ich beitragen?

### Event-Quellen hinzufügen

Wenn du eine neue Event-Quelle kennst:

1. Öffne ein Issue mit dem Label "neue-quelle"
2. Gib die URL und Beschreibung der Quelle an
3. Optional: Erstelle einen Pull Request mit dem Scraper-Code

### Bugs melden

Bugs bitte als GitHub Issue melden mit:
- Beschreibung des Problems
- Schritte zur Reproduktion
- Browser/Environment-Infos

### Feature-Vorschläge

Feature-Requests als Issue mit Label "enhancement" einreichen.

### Code beitragen

1. Fork das Repository
2. Erstelle einen Feature-Branch
3. Committe deine Änderungen mit klaren Commit-Messages
4. Öffne einen Pull Request

## Code-Style

- **Python**: PEP 8
- **JavaScript**: ES6+, 2 Spaces Einrückung
- **CSS**: BEM-Notation wo sinnvoll

## Testing

### Automatische Tests ausführen

**Vor jedem Commit solltest du die Tests ausführen:**

```bash
cd tests
node test_filters.js
```

**Was wird getestet:**
- ✅ HTML `<select>` Optionen stimmen mit erwarteten Werten überein
- ✅ JavaScript Filter-Logik ist konsistent (z.B. `radiusFilter < 999`)
- ✅ Distanzberechnung funktioniert für alle Fortbewegungsarten
- ✅ Edge Cases (mit/ohne Standort, extreme Werte)

**CI/CD Integration:**
- Tests laufen automatisch bei jedem Push zu `index.html` oder `assets/js/main.js`
- Workflow: `.github/workflows/test-filters.yml`
- Verhindert Inkonsistenzen zwischen UI und Logik

### Code Quality Validation

**Lokal ausführen:**

```bash
# HTML validieren
bundle exec jekyll build
npx html-validate _site/index.html

# CSS validieren
npx stylelint "assets/css/*.css"

# JavaScript validieren
npx eslint assets/js/main.js --fix
```

**Automatische Validierung:**
- **Bei jedem Push**: `.github/workflows/validate-code.yml`
- **Monatlich**: `.github/workflows/monthly-tests.yml`

**Was wird geprüft:**
- ✅ HTML: Void elements, button types, accessibility
- ✅ CSS: Duplicates, modern syntax, consistency
- ✅ JavaScript: Linting, trailing spaces, indentation
- ✅ Accessibility: Inline styles, raw characters, semantic HTML

### Monatliche Testbatterie

Jeden 1. des Monats um 2:00 UTC läuft automatisch:

1. **Filter Tests** - HTML ↔ JavaScript Konsistenz
2. **Code Validation** - HTML, CSS, JS Quality
3. **Build Test** - Jekyll Build, Python Scraper
4. **Event Files Check** - Prüfung vorhandener Events

Manuell starten: GitHub → Actions → "Monthly Test Suite" → "Run workflow"

📖 Details: [../tests/README.md](../tests/README.md)

**Test-Konfiguration anpassen:**

Wenn du Filter-Optionen änderst, aktualisiere `tests/test_filters.js`:
```javascript
const EXPECTED_RADIUS_OPTIONS = [
    { value: '999', label: 'Alle', shouldFilter: false },
    { value: '1', label: '10 min zu Fuß', shouldFilter: true },
    { value: '3', label: '10 min Rad', shouldFilter: true },
    // ... weitere Optionen
];
```

📖 Details: [../tests/README.md](../tests/README.md)

### Manuelle Tests

Teste deine Änderungen lokal:

```bash
bundle exec jekyll serve
python scripts/scrape_events.py
```

## Fragen?

Bei Fragen öffne ein Issue oder starte eine Discussion.

Danke! ❤️
