# 🧪 Tests

Funktionale Tests für die Website-Features.

## 🎯 Test-Übersicht

### `test_filters.js`
**Was wird getestet:**
- Konsistenz zwischen HTML-UI und JavaScript-Logik
- Filter-Optionen: Radius, Time, Category
- Data-Attributes: `data-hours`, `data-singular`, `data-plural`

**Ausführen:**
```bash
node scripts/tests/test_filters.js
```

**Status:** ⚠️ Muss aktualisiert werden nach Module-Refactoring

### `test-filter.html`
**Was wird getestet:**
- Standalone-Seite zum manuellen Testen der Filter-UI
- Nützlich für Browser-basierte Tests

**Ausführen:**
```bash
# Development Server starten
./scripts/dev/dev.sh

# Im Browser öffnen
open http://localhost:4000/scripts/tests/test-filter.html
```

---

## 📝 Neue Tests hinzufügen

### Funktionale Tests

Erstelle eine neue Datei `test_<feature>.js`:

```javascript
// scripts/tests/test_bookmarks.js
import { BookmarkManager } from '../../assets/js/modules/bookmarks.js';

console.log('Testing Bookmark Manager...');

const manager = new BookmarkManager();
manager.addBookmark('test-event-id');

if (manager.hasBookmark('test-event-id')) {
  console.log('✅ Bookmark added successfully');
} else {
  console.error('❌ Bookmark test failed');
  process.exit(1);
}
```

### Test-Konventionen

1. **Dateinamen**: `test_<feature>.js`
2. **Output**: `✅` für Success, `❌` für Failure
3. **Exit Codes**: `0` = Success, `1` = Failure
4. **Import-Pfade**: Relativ zu `scripts/tests/`

---

## 🚀 Test-Automation

Tests werden automatisch ausgeführt:

- **Pre-Commit Hook**: Validation-Tests
- **GitHub Actions**: Alle Tests bei Push
- **Manuell**: `npm test` (wenn konfiguriert)

---

## 🔍 Debugging

### Test lokal ausführen
```bash
# Einzelner Test
node scripts/tests/test_filters.js

# Mit Debugging-Output
node --inspect scripts/tests/test_filters.js
```

### Test-Daten
Verwende echte Event-Dateien aus `_events/`:
```javascript
const testEvent = '_events/2025-12-15-weihnachtsmarkt-hof.md';
```

---

## ⚠️ TODO

- [ ] `test_filters.js` aktualisieren für Module-Architektur
- [ ] Bookmark-Tests hinzufügen
- [ ] Map-Marker-Tests hinzufügen
- [ ] RSS-Feed-Validierung hinzufügen
- [ ] Coverage-Report generieren
