# Krawl JavaScript Modules

Modulare Architektur nach KISS-Prinzip.

## Struktur

```
assets/js/
├── main.js                    (Orchestrator, 267 Zeilen)
└── modules/
    ├── storage.js             (LocalStorage-Abstraktion, 48 Zeilen)
    ├── bookmarks.js           (Bookmark-System, 66 Zeilen)
    ├── map.js                 (Leaflet-Integration, 87 Zeilen)
    ├── filters.js             (Event-Filterung, 129 Zeilen)
    └── events.js              (Event-Verwaltung, 108 Zeilen)
```

**Vorher:** 1127 Zeilen monolithisch  
**Nachher:** 267 + 438 = 705 Zeilen modular (76% Reduktion in main.js)

## Module

### `storage.js`
- **Purpose:** Persistierung von Präferenzen & Bookmarks
- **API:** `savePrefs()`, `loadPrefs()`, `saveBookmarks()`, `loadBookmarks()`, `clear()`
- **Tech:** LocalStorage (statt Cookies - einfacher, mehr Platz)

### `bookmarks.js`
- **Purpose:** Bookmark-Management
- **API:** `toggle()`, `has()`, `getAll()`, `clear()`, `updateButton()`, `getEventData()`
- **Features:** UI-Updates, Print/Mail-Export

### `map.js`
- **Purpose:** Leaflet-Karte
- **API:** `init()`, `addMarker()`, `clearMarkers()`, `setView()`, `getUserLocation()`, `getDistanceKm()`
- **Tech:** Leaflet.js Integration

### `filters.js`
- **Purpose:** Event-Filterung (Category, Time, Radius, Location)
- **API:** `toggleCategory()`, `setTimeRange()`, `setRadius()`, `setLocation()`, `filterEvents()`
- **State:** `export()`, `import()` für Präferenzen

### `events.js`
- **Purpose:** Event-Daten & Logik
- **API:** `loadFromDOM()`, `getUpcoming()`, `sortByDate()`, `getByCategory()`, `getByLocation()`, `getStats()`
- **Features:** Sonnenaufgang-Berechnung, Event-Statistiken

## KISS-Prinzipien

### Cookies → LocalStorage
```javascript
// VORHER: Cookie-Handling (80+ Zeilen)
document.cookie = `${COOKIE_NAME}=${JSON.stringify(prefs)}; expires=${expires.toUTCString()}; path=/; SameSite=Lax`;

// NACHHER: LocalStorage (1 Zeile)
localStorage.setItem('krawl_prefs', JSON.stringify(prefs));
```

### ES6 Modules statt globale Variablen
```javascript
// VORHER: Alles global
let map;
let markers = [];
let bookmarks = new Set();

// NACHHER: Gekapselt
import { MapManager } from './modules/map.js';
const mapManager = new MapManager('map');
```

### Error-Handling: Minimal
```javascript
// Nur console.warn für Debugging
// Keine Over-Engineering mit try/catch überall
```

## Verwendung

### Import in HTML
```html
<script type="module" src="/assets/js/main.js"></script>
```

### Debugging
```javascript
// Browser-Console:
window.krawl.bookmarks.getAll()
window.krawl.map.markers
window.krawl.filters.export()
window.krawl.events.getStats()
window.krawl.refresh() // Display neu rendern
```

## Migration

### Alte main.js
- Backup: `assets/js/main.js.backup` (1127 Zeilen)
- Funktioniert nicht mehr (ES6 Imports fehlen)

### Kompatibilität
- Browser-Anforderung: ES6 Modules (Chrome 61+, Firefox 60+, Safari 11+)
- Kein Babel/Webpack nötig (moderne Browser only)

## Tradeoffs

### ✅ Gewonnen
- **Wartbarkeit:** Klare Trennung, leicht zu finden
- **Testbarkeit:** Module einzeln testbar
- **Größe:** 76% weniger Code in main.js
- **Performance:** LocalStorage ist schneller als Cookies

### ❌ Verloren
- **Legacy-Support:** IE11 funktioniert nicht (aber wer nutzt das noch?)
- **Build-Step:** Kein Bundling/Minification (aber GitHub Pages = statisch)

### 🤷 Ignoriert (Kill your darlings)
- Komplexe Error-Recovery
- Fallbacks für alles
- Excessive Validation
- Over-Engineering

## Nächste Schritte

Optional:
- [ ] Tests schreiben (Jest/Vitest)
- [ ] TypeScript-Definitionen
- [ ] Minification (Terser)
- [ ] Bundle für Produktion (esbuild)

Aber: **KISS > Perfektion**
