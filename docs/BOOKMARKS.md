# 📌 Bookmark-System

**Letzte Aktualisierung:** 19. November 2025  
**Version:** v1.7.0

## Übersicht

Das Bookmark-System ermöglicht es Besuchern, Events vorzumerken und später zu exportieren. Alle Daten werden **lokal im Browser** gespeichert (Cookie-basiert, datenschutzfreundlich).

## Features

### ✅ Event-Markierung

- **In Kartenübersicht:** Bookmark-Button in jeder Event-Card
- **In Popup-Detailansicht:** Bookmark-Button im Karten-Popup
- **Visuelle Hervorhebung:**
  - Gemerktes Event erhält grünen Rahmen
  - ⭐-Symbol in der rechten oberen Ecke
  - "⭐ Gemerkt" statt "☆ Merken" im Button

### 🍪 Cookie-Speicherung

```javascript
// Cookie-Name
eventKalenderBookmarks

// Speichert nur URLs (nicht vollständige Event-Daten)
["https://example.com/events/event-1", "https://example.com/events/event-2"]

// Gültigkeitsdauer: 365 Tage
```

### 🎯 Toolbar am Bildrand

Die Toolbar erscheint nur, wenn mindestens ein Event gemerkt wurde:

**Position:**
- Desktop: Rechter Bildschirmrand, vertikal zentriert
- Mobile: Unten rechts, über Footer

**Buttons:**
- `🖨️ Drucken` - Generiert druckbare Übersicht
- `📧 Mailen` - Erstellt E-Mail mit Event-Liste
- `🗑️ Alle löschen` - Löscht alle Bookmarks

### 🖨️ Druck-Funktion

**Funktionsweise:**
1. Prüft welche gemerkten Events noch gültig sind:
   - `status: "Öffentlich"`
   - Termin liegt in der Zukunft
2. Öffnet neues Browser-Fenster mit formatierter Liste
3. Browser-Druckdialog oder "Als PDF speichern"

**Generiertes Format:**
```
📌 Meine gemerkten Events

Generiert am: Dienstag, 19. November 2025
Anzahl Events: 3

════════════════════════════════════════════════════════════════

1. Stammtisch Kulturfreunde
📅 Dienstag, 10. Dezember 2025 um 19:00 Uhr
📍 Gaststätte Zum Kronprinz
🏷️ Kultur

Monatliches Treffen für Kulturinteressierte

────────────────────────────────────────────────────────────────

2. Wochenmarkt
📅 Mittwoch, 20. November 2025 um 08:00 Uhr
📍 Altstadt Marktplatz
🏷️ Markt

────────────────────────────────────────────────────────────────
```

### 📧 E-Mail-Funktion

**Funktionsweise:**
1. Generiert Text-Liste aller gültigen Events
2. Erstellt `mailto:`-Link mit vorausgefülltem Betreff & Body
3. Öffnet Standard-E-Mail-Programm

**Einschränkungen:**
- Browser-Limit: ~2000 Zeichen für `mailto:`-Links
- Bei zu vielen Events: Warnung + Verweis auf Druck-Funktion

**E-Mail-Format:**
```
Betreff: Meine gemerkten Events (3 Termine)

Body:
Meine gemerkten Events - Event-Kalender Hof
Generiert am: Dienstag, 19. November 2025

============================================================

1. Stammtisch Kulturfreunde
📅 Dienstag, 10. Dezember 2025 um 19:00 Uhr
📍 Gaststätte Zum Kronprinz
🏷️ Kultur

Monatliches Treffen für Kulturinteressierte

------------------------------------------------------------
```

## Technische Implementierung

### JavaScript-Funktionen

```javascript
// Core Functions
toggleBookmark(eventUrl)          // Event merken/entmerken
saveBookmarksToCookie()           // In Cookie speichern
loadBookmarksFromCookie()         // Aus Cookie laden
updateBookmarkUI()                // Toolbar-Sichtbarkeit

// Export Functions
getBookmarkedEventData()          // Gültige Events filtern
printBookmarks()                  // Druck-Dialog öffnen
emailBookmarks()                  // E-Mail erstellen
clearAllBookmarks()               // Alle löschen
```

### Cookie-Struktur

```javascript
{
  name: 'eventKalenderBookmarks',
  value: JSON.stringify(['url1', 'url2', ...]),
  expires: new Date(+365 Tage),
  path: '/',
  sameSite: 'Lax'
}
```

### Event-Validierung

Beim Export werden Events automatisch gefiltert:

```javascript
function getBookmarkedEventData() {
    const now = new Date();
    return bookmarkedEvents
        .map(url => allEvents.find(e => e.url === url))
        .filter(event => {
            // Nur veröffentlichte Events
            if (event.status !== 'Öffentlich') return false;
            
            // Nur zukünftige Events
            const eventDate = new Date(event.date + 'T' + event.start_time);
            return eventDate >= now;
        })
        .sort((a, b) => new Date(a.date) - new Date(b.date));
}
```

## CSS-Klassen

```css
/* Toolbar */
.bookmarks-toolbar              /* Hauptcontainer */
.toolbar-content                /* Flex-Layout für Buttons */
.toolbar-label                  /* "X Events gemerkt" */
.toolbar-btn                    /* Druck/Mail Buttons */
.toolbar-btn-clear              /* Löschen-Button (rot) */

/* Bookmark-Buttons */
.btn-bookmark                   /* Standard-Button */
.btn-bookmark.bookmarked        /* Aktiver Zustand (grün) */

/* Event-Card Highlighting */
.event-card.bookmarked          /* Grüner Rahmen */
.event-card.bookmarked::before  /* ⭐-Symbol */

/* Popup */
.popup-bookmark-btn             /* Button im Karten-Popup */
```

## Responsive Design

### Desktop
- Toolbar: Rechter Bildschirmrand, vertikal zentriert
- Buttons: Vertikal gestapelt
- Event-Cards: Volle Bookmark-Hervorhebung

### Mobile (< 768px)
- Toolbar: Unten rechts, horizontal Layout
- Buttons: Nebeneinander, kleinere Schrift
- ⭐-Symbol: Kleiner (22px statt 28px)

## Datenschutz

✅ **DSGVO-konform:**
- Keine persönlichen Daten gespeichert
- Nur Event-URLs (öffentliche Daten)
- Lokal im Browser (kein Server)
- Keine Third-Party-Cookies
- Cookie-Banner nicht erforderlich (technisch notwendig)

## Browser-Kompatibilität

| Browser | Version | Unterstützt |
|---------|---------|-------------|
| Chrome | 90+ | ✅ |
| Firefox | 88+ | ✅ |
| Safari | 14+ | ✅ |
| Edge | 90+ | ✅ |

## Bekannte Limitierungen

1. **E-Mail-Länge:** Mailto-Links haben Browser-Limit (~2000 Zeichen)
   - **Lösung:** Warnung + Verweis auf Druck-Funktion

2. **Cookie-Speicher:** Browser-Limit für Cookies (~4KB)
   - **Kapazität:** ~100-150 Event-URLs
   - **Bei Überschreitung:** Warnung + älteste Bookmarks entfernen

3. **Private Browsing:** Cookies werden beim Schließen gelöscht
   - **Hinweis:** Automatisch anzeigen bei Private Mode

## Zukünftige Erweiterungen

### v1.8.0 (geplant)
- [ ] LocalStorage statt Cookies (größere Kapazität)
- [ ] Bookmark-Kategorien/Tags
- [ ] Sortieroptionen (Datum, Kategorie, Alphabet)

### v1.9.0 (geplant)
- [ ] ICS-Export (iCalendar-Format)
- [ ] Sync mit Google Calendar / Outlook
- [ ] Teilen-Funktion (Link zu Bookmark-Liste)

### v2.0.0 (geplant)
- [ ] Account-System (optional, für Sync)
- [ ] Bookmark-Statistiken
- [ ] Empfehlungen basierend auf Bookmarks

## Testing

### Manuelle Tests

```bash
# 1. Event merken
- Klicke "☆ Merken" → Button wird grün "⭐ Gemerkt"
- Event-Card erhält grünen Rahmen + ⭐-Symbol
- Toolbar erscheint am Bildrand

# 2. Mehrere Events merken
- Merke 3-5 Events
- Toolbar zeigt korrekte Anzahl

# 3. Druck-Funktion
- Klicke "🖨️ Drucken"
- Neues Fenster öffnet sich
- Formatierte Liste wird angezeigt
- Browser-Druckdialog öffnet sich

# 4. E-Mail-Funktion
- Klicke "📧 Mailen"
- E-Mail-Programm öffnet sich
- Betreff & Body sind vorausgefüllt

# 5. Persistenz
- Merke Events
- Seite neu laden
- Bookmarks sind noch vorhanden

# 6. Validierung
- Merke Event
- Ändere Event-Status auf "Archiviert"
- Export zeigt Event nicht mehr an
```

## Support

Bei Fragen oder Problemen:
- GitHub Issues: https://github.com/feileberlin/event-kalender-hof/issues
- Diskussionen: https://github.com/feileberlin/event-kalender-hof/discussions
