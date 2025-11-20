# 📋 TODO - Feature Backlog

**Aktuelle Wunschliste & Bugfixes für krawl.ist**

**Update:** Diese Datei IMMER vor neuen Features aktualisieren!

---

## 🔥 High Priority (sofort)

### ~~1. GoatCounter Script wiederherstellen~~ ✅ ERLEDIGT
- **Status:** ✅ COMPLETED (2025-11-20)
- **Solution:** Code in `_config.yml` von "krawlist" zu "feileberlin" korrigiert
- **Files:** `_config.yml` Line 233

### ~~2. Radius-Filter KISS-Restrukturierung~~ ✅ ERLEDIGT
- **Status:** ✅ COMPLETED (2025-11-20)
- **Solution:** Radius-Filter von hardcoded zu config-driven migriert
- **Implementation:**
  - ✅ `_config.yml` → `filters.radius_filters` (key, label, km, default)
  - ✅ `index.html` → Jekyll template loop mit `data-km` Attribut
  - ✅ `assets/js/main.js` → Liest `data-km`, handled null für unbegrenzt
  - ✅ `assets/js/modules/filters.js` → null-Handling in setRadius() und Distanzprüfung
- **Files:** `_config.yml`, `index.html`, `assets/js/main.js`, `assets/js/modules/filters.js`

### ~~3. Feature Guard Workflow~~ ✅ ERLEDIGT
- **Status:** ✅ COMPLETED (2025-11-20)
- **Implementation:** `.github/workflows/feature-guard.yml`
- **Checks:**
  - ✅ GoatCounter Script in Layouts + Config
  - ✅ Radius-Filter Config in `_config.yml`
  - ✅ Category & Time Filters
  - ✅ RSS-Feeds existieren
  - ✅ Critical JS modules vorhanden
  - ✅ Admin Panel + GitHub Meta Editor
  - ✅ Documentation (README, FEATURES, TODO)

### ~~4. SEO Optimization~~ ✅ ERLEDIGT
- **Status:** ✅ COMPLETED (2025-11-20)
- **Implementation:**
  - ✅ Meta Description, Open Graph, Twitter Cards in Layouts
  - ✅ Canonical URLs für Duplicate Content Prevention
  - ✅ robots.txt (Crawler-Steuerung, Admin-Ausschluss)
  - ✅ sitemap.xml (automatisch via jekyll-sitemap)
  - ✅ Admin-Bereich: noindex/nofollow
- **Files:** `_layouts/base.html`, `_layouts/map.html`, `_layouts/admin.html`, `robots.txt`, `_config.yml`

### ~~5. PWA Implementation~~ ✅ ERLEDIGT
- **Status:** ✅ COMPLETED (2025-11-20)
- **Implementation:**
  - ✅ manifest.json (App-Metadata, standalone mode)
  - ✅ Service Worker (Network-First Caching, Offline-Support)
  - ✅ Theme Color (Android Status Bar)
  - ✅ Apple Touch Icons (iOS)
  - ✅ Auto-Update Handling
- **Files:** `manifest.json`, `sw.js`, `_layouts/base.html`, `_layouts/map.html`, `assets/js/main.js`

### ~~6. Accessibility (WCAG 2.1 Level AA)~~ ✅ ERLEDIGT
- **Status:** ✅ COMPLETED (2025-11-20)
- **Implementation:**
  - ✅ prefers-reduced-motion Support (Animationen deaktivierbar)
  - ✅ Skip-to-Content Link (Keyboard Navigation)
  - ✅ Focus Styles (outline: 2px solid auf allen interaktiven Elementen)
  - ✅ ARIA Labels (Screen Reader Support)
  - ✅ role="application" für Karte
- **Files:** `assets/css/fullscreen.css`, `index.html`

---

## ⚡ Medium Priority (bald)

### ~~7. Filter-Icon-Bug final fixen~~ ✅ ERLEDIGT
- **Status:** ✅ COMPLETED (2025-11-20)
- **Solution:** Verbesserte Regex für robusteres Icon-Parsing
- **Implementation:**
  - Erweiterte Unicode-Ranges für alle Emoji-Kategorien
  - Kombiniertes Pattern für Zahlen + Emojis in einem Regex
  - Bessere Fehlerbehandlung in updateCategoryCounts()
- **Files:** `assets/js/main.js`

### ~~8. Performance Optimization~~ ✅ PARTIALLY COMPLETED
- **Status:** 🟡 IN PROGRESS
- **Completed:**
  - ✅ Resource Hints (dns-prefetch, preconnect für CDNs)
    - cdnjs.cloudflare.com (Normalize CSS)
    - unpkg.com (Leaflet.js)
    - gc.zgo.at (GoatCounter Analytics)
    - tile.openstreetmap.org (Map Tiles)
  - ✅ Preconnect mit crossorigin für kritische Resources
- **Remaining:**
  - 🔴 Lazy Loading für Event-Marker (nur sichtbare laden)
  - 🔴 Image Optimization (WebP für Venue-Fotos)
  - 🔴 Code Splitting (separate Bundles für Map/Admin)
- **Impact:** MEDIUM (Ladezeit-Verbesserung, DNS-Lookup gespart)
- **Test:** Lighthouse Performance Score > 90
- **Files:** `_layouts/base.html`, `_layouts/map.html`

### ~~9. Debug-Switch für Test-Events~~ ✅ ERLEDIGT
- **Status:** ✅ COMPLETED (2025-11-20)
- **Solution:** Jekyll Template filtert Test-Events basierend auf Config
- **Implementation:**
  - Prüfung auf `event.test_event` Flag in index.html
  - Conditional Rendering basierend auf `site.debug.show_test_events`
  - Test-Events erhalten zusätzlich `testEvent: true` Property in JS
  - Normale Events erhalten `testEvent: false` Property
- **Usage:** In `_config.yml` setze `debug.show_test_events: false` um Test-Events zu verstecken
- **Files:** `index.html`

### 10. Responsive Filter-Counter
- **Status:** 🟢 WORKING, needs UX polish
- **Issue:** Counter manchmal zu lang auf Mobile ("123 🎉 Konzerte")
- **Idea:** Kürzere Labels auf Mobile (nur Icon + Zahl?)
- **Impact:** LOW (nur UX)

### 11. Event-Validierung verbessern
- **Status:** 🔴 TODO
- **Problem:** Scraper erzeugt manchmal inkonsistente Daten
- **TODO:**
  - Schema-Validierung (JSON Schema für Events)
  - Required Fields Check (title, date, venue)
  - Date Format Validation (ISO 8601)
  - URL Validation (source links)
- **Location:** `scripts/validation/validate_events.py`
- **Impact:** HIGH (Datenqualität)

---

## 🌟 Nice-to-Have (später)

### 12. Event-Export (iCal/CSV)
- **Purpose:** Events in Kalender-App importieren
- **Format:** iCalendar (.ics)
- **Location:** Bookmark-Toolbar → "📅 Exportieren" Button
- **Impact:** MEDIUM (Feature-Request)

### 13. Dark Mode
- **Status:** 🔴 TODO
- **Implementation:**
  - CSS: `@media (prefers-color-scheme: dark)`
  - Toggle in Header (optional)
  - LocalStorage für Persistenz
  - Karte: Dark Tiles (OpenStreetMap Dark Mode)
- **Impact:** MEDIUM (UX-Verbesserung)

### 14. Social Sharing
- **Status:** 🔴 TODO
- **Features:**
  - Share-Button in Event-Popups
  - Web Share API (Mobile)
  - Fallback: Copy-to-Clipboard
  - Pre-filled Text mit Event-Details
- **Impact:** LOW (Social-Feature)

### 15. Recurring Events UI verbessern
- **Current:** Admin-Panel hat Preview, aber schwer zu editieren
- **Idea:** Visual Recurring Editor (Drag & Drop für Exceptions?)
- **Impact:** LOW (Admin-only)

### 16. Multi-Language Support
- **Current:** Nur Deutsch
- **Target:** Englisch als zweite Sprache
- **Approach:** i18n mit Jekyll Liquid
- **Impact:** HIGH (große Änderung)

### 17. Event-Kommentare / Ratings
- **Purpose:** Community-Feedback zu Events
- **Tech:** GitHub Discussions API oder Disqus
- **Privacy:** GDPR-Considerations
- **Impact:** HIGH (Social-Feature)

### 18. Venue-Fotos
- **Purpose:** Bilder von Veranstaltungsorten
- **Source:** Wikimedia Commons oder User-Upload?
- **Location:** Marker-Popups, Event-Cards
- **Impact:** MEDIUM (Visual Enhancement)

### 19. Event-Empfehlungen (ML)
- **Status:** 🔴 TODO (experimentell)
- **Approach:**
  - User-History (Bookmarks, geklickte Events)
  - Collaborative Filtering (ähnliche User)
  - Content-Based (Kategorie, Veranstaltungsort)
- **Privacy:** Client-side ML (kein Tracking)
- **Impact:** HIGH (Feature-Addition)

### 20. Desktop-Notifications
- **Status:** 🔴 TODO
- **Trigger:** Neue Events in Bookmark-Kategorien
- **Tech:** Web Notifications API + Service Worker
- **Opt-in:** Permission Request
- **Impact:** MEDIUM (Engagement)

---

## 🐛 Known Bugs

### Bug 1: Filter-Icons duplizieren
- **Status:** 🟡 PARTIALLY FIXED (data-original-label)
- **Reproduce:** Schnell zwischen Kategorien wechseln
- **Priority:** MEDIUM

### Bug 2: Mobile Safari - Map Rendering
- **Status:** 🔴 OPEN
- **Issue:** Karte lädt manchmal nicht auf iOS Safari
- **Workaround:** Seite neu laden
- **Priority:** HIGH

---
- **Impact:** MEDIUM (UX-Enhancement)

---

## 🐛 Known Bugs

### Bug #1: Cache-Issues auf GitHub Pages
- **Symptom:** Änderungen nicht sofort sichtbar
- **Workaround:** Cache-Invalidation-Timestamp in `_config.yml`
- **Proper Fix:** Service Worker mit Cache-Strategie?
- **Priority:** LOW (Workaround funktioniert)

### Bug #2: Map-Zoom manchmal falsch
- **Symptom:** Karte zoomt zu weit rein/raus bei Location-Wechsel
- **Location:** `assets/js/modules/map.js`
- **Priority:** LOW (selten)

### Bug #3: Bookmark-Toolbar flackert
- **Symptom:** Toolbar blinkt kurz beim Laden
- **Cause:** CSS-Transition + JS show/hide race condition
- **Priority:** LOW (nur visuell)

---

## ✅ Completed (aus Backlog)

### ✅ Event-Liste Sidebar (2025-11-19)
- Ausklappbare Sidebar mit Event-Cards
- Bookmark-Buttons in Cards
- Responsive Design

### ✅ Test-Events-Generator (2025-11-20)
- `scripts/dev/generate_test_events.py`
- Lorem-Ipsum Events für Tests
- Cleanup-Script

### ✅ GitHub Meta Editor (2025-11-20)
- Admin-Panel Tab für Repository-Metadaten
- Description, Homepage, Topics editierbar
- GitHub API Integration

### ✅ Scripts-Reorganisation (2025-11-20)
- Neue Struktur: dev/, editorial/, tests/, validation/
- maintenance/ → editorial/ umbenannt
- README.md komplett neu

### ✅ Filter-Icon-Bug (2025-11-20)
- Icons duplizierten sich bei jedem Update
- Fix: data-original-label bereinigen mit Regex

---

## 🔄 Change Management Workflow

**Für neue Features/Bugs:**


5. Security Headers (LOW Priority für GH Pages)

Content Security Policy
Aber: GitHub Pages setzt bereits viele Header automatisch
6. Performance (LOW Priority)

Lazy Loading für Bilder
Resource Hints (preconnect, dns-prefetch)

**Bei Änderungen an bestehenden Features:**

1. SEO & Metadata (HIGH Priority)

Meta Description fehlt
Open Graph Tags (Facebook, LinkedIn)
Twitter Card Tags
Canonical URLs

2. PWA Features (MEDIUM Priority)

manifest.json (App-Installation auf Mobile)
Service Worker (Offline-Funktionalität)
Theme Color

3. SEO Infrastructure (HIGH Priority)

robots.txt (Crawler-Steuerung)
sitemap.xml (Search Engine Discovery)

4. Accessibility (MEDIUM Priority)

lang Attribut ist da ✓, aber:
prefers-reduced-motion für Animationen
Skip-to-Content Links
ARIA Labels für Filter

---

**Last Updated:** 2025-11-20  
**Next Review:** Bei jedem neuen Feature-Request  
**Maintainer:** GitHub Copilot + User
