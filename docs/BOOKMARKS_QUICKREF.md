# 📌 Bookmark-System - Quick Reference

## Für Benutzer

### Event merken
```
1. Klicke "☆ Merken" in Event-Card oder Popup
2. Button wird grün: "⭐ Gemerkt"
3. Event erhält grünen Rahmen + ⭐-Symbol
4. Toolbar erscheint am rechten Bildrand
```

### Events exportieren
```
🖨️ Drucken:  Formatierte Liste → Browser-Druckdialog
📧 Mailen:    E-Mail-Programm öffnet sich automatisch
🗑️ Löschen:  Alle Bookmarks entfernen
```

### Toolbar-Position
```
Desktop:  Rechts, vertikal zentriert
Mobile:   Unten rechts, über Footer
```

## Für Entwickler

### JavaScript-API

```javascript
// Event merken/entmerken
toggleBookmark(eventUrl)

// Cookie-Verwaltung
saveBookmarksToCookie()           // Set bookmarkedEvents → Cookie
loadBookmarksFromCookie()         // Cookie → Set bookmarkedEvents

// UI-Updates
updateBookmarkUI()                // Toolbar Sichtbarkeit
updateBookmarkButton(btn, bool)   // Button-Zustand

// Export
getBookmarkedEventData()          // Array gültiger Events
printBookmarks()                  // PDF/Druck
emailBookmarks()                  // Mailto-Link
clearAllBookmarks()               // Alles löschen
```

### Cookie-Struktur

```javascript
Name:     'eventKalenderBookmarks'
Value:    JSON.stringify(['url1', 'url2', ...])
Expires:  +365 Tage
Path:     '/'
SameSite: 'Lax'
```

### CSS-Klassen

```css
/* Toolbar */
.bookmarks-toolbar                /* Container (fixed, rechts) */
.toolbar-btn                      /* Druck/Mail Buttons */
.toolbar-btn-clear                /* Löschen-Button (rot) */

/* Buttons */
.btn-bookmark                     /* Merken-Button */
.btn-bookmark.bookmarked          /* Aktiv (grün) */

/* Highlighting */
.event-card.bookmarked            /* Grüner Rahmen */
.event-card.bookmarked::before    /* ⭐-Symbol (::before) */
```

### Event-Validierung

```javascript
// Nur diese Events werden exportiert:
- status === 'Öffentlich'
- date >= now (zukünftige Events)
- Sortiert nach Datum (aufsteigend)
```

### HTML-Integration

```html
<!-- Toolbar (in index.html) -->
<div id="bookmarks-toolbar" class="bookmarks-toolbar" style="display: none;">
  <div class="toolbar-content">
    <span class="toolbar-label">
      <strong id="bookmark-count">0</strong> Events gemerkt
    </span>
    <button onclick="printBookmarks()">🖨️ Drucken</button>
    <button onclick="emailBookmarks()">📧 Mailen</button>
    <button onclick="clearAllBookmarks()">🗑️ Alle löschen</button>
  </div>
</div>

<!-- Bookmark-Button (in Event-Card) -->
<button class="btn-bookmark" 
        data-event-url="/events/2025-12-09-stammtisch.html"
        onclick="event.stopPropagation(); toggleBookmark('/events/...')">
  ☆ Merken
</button>
```

## Testing

### Quick-Tests

```bash
# 1. Event merken
[Klick "☆ Merken"] → Button wird "⭐ Gemerkt" + Toolbar erscheint

# 2. Persistenz
[Seite neu laden] → Bookmarks noch vorhanden

# 3. Druck
[Klick "🖨️ Drucken"] → Neues Fenster mit formatierter Liste

# 4. E-Mail
[Klick "📧 Mailen"] → E-Mail-Programm öffnet mit Betreff & Body

# 5. Löschen
[Klick "🗑️ Alle löschen"] → Bestätigung → Bookmarks weg
```

### Browser-Console

```javascript
// Bookmarks anzeigen
console.log(bookmarkedEvents);

// Manuell hinzufügen
bookmarkedEvents.add('/events/2025-12-09-stammtisch.html');
saveBookmarksToCookie();

// Cookie auslesen
document.cookie.split(';').find(c => c.includes('Bookmarks'));
```

## Datenschutz

✅ **DSGVO-konform:**
- Nur Event-URLs (öffentliche Daten)
- Lokal im Browser gespeichert
- Kein Server-Transfer
- Kein Cookie-Banner nötig (technisch notwendig)

## Browser-Limits

| Feature | Limit | Lösung |
|---------|-------|--------|
| Cookie-Größe | ~4KB | ~100-150 URLs |
| Mailto-Länge | ~2000 Zeichen | Warnung + Druck-Verweis |

## Mobile Besonderheiten

```css
/* < 768px */
.bookmarks-toolbar {
  bottom: 80px;      /* Über Footer */
  right: 10px;
  border-radius: 12px;
}

.toolbar-content {
  flex-direction: row;  /* Horizontal */
}

.toolbar-btn {
  min-width: 80px;
  font-size: 12px;
}
```

## Bekannte Issues

1. **Private Browsing:** Cookies werden gelöscht beim Schließen
2. **Safari < 14:** Mailto-Links kürzen Body automatisch
3. **IE11:** Nicht unterstützt (ES6 Set, Template Strings)

## Roadmap

### v1.8.0
- LocalStorage statt Cookies
- Bookmark-Kategorien
- Import/Export JSON

### v1.9.0
- ICS-Export (iCalendar)
- Teilen-Funktion
- Sync mit Kalender-Apps

## Support

**Dokumentation:** `docs/BOOKMARKS.md`  
**GitHub Issues:** https://github.com/feileberlin/event-kalender-hof/issues
