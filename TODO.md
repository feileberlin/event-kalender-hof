# 📋 TODO - Feature Backlog

**Aktuelle Wunschliste & Bugfixes für krawl.ist**

**Update:** Diese Datei IMMER vor neuen Features aktualisieren!

---

## 🔥 High Priority (sofort)

### 1. GoatCounter Script wiederherstellen
- **Status:** 🔴 TODO
- **Problem:** Script wurde versehentlich entfernt
- **Location:** `_layouts/map.html`, `_layouts/base.html`
- **Action:** Script vor `</body>` einfügen
- **Code:**
  ```html
  <script data-goatcounter="https://feileberlin.goatcounter.com/count"
          async src="//gc.zgo.at/count.js"></script>
  ```
- **Test:** `grep -r "goatcounter" _layouts/`
- **Impact:** LOW (nur Analytics)

### 2. Radius-Filter KISS-Restrukturierung
- **Status:** 🔴 TODO
- **Problem:** Radius-Filter ist hardcoded, bricht bei HTML-Änderungen
- **Current:** Hardcoded `<option value="1">` in `index.html`
- **Target:** Config in `_config.yml` → `filters.radius_filters` (wie time_filters)
- **Changes:**
  - Add `radius_filters` zu `_config.yml`
  - Convert `index.html` radiusFilter zu Jekyll-Template
  - Update `assets/js/modules/filters.js` → lese `data-km` statt `value`
  - Handle `km: null` = unbegrenzt
- **Impact:** MEDIUM (betrifft Filter-System)
- **Files:** `_config.yml`, `index.html`, `assets/js/modules/filters.js`
- **Test:** Radius-Filter funktioniert, "weit entfernt" = kein Radius-Limit

### 3. Feature Guard Workflow
- **Status:** 🔴 TODO
- **Purpose:** Automatisch prüfen ob kritische Features noch da sind
- **Implementation:** `.github/workflows/feature-guard.yml`
- **Checks:**
  - GoatCounter Script in Layouts
  - Radius-Filter Config in `_config.yml`
  - RSS-Feeds existieren
  - Critical JS modules vorhanden
- **Impact:** LOW (nur CI)
- **Benefits:** Verhindert versehentliche Feature-Löschungen

---

## ⚡ Medium Priority (bald)

### 4. Filter-Icon-Bug final fixen
- **Status:** 🟡 PARTIALLY FIXED
- **Problem:** Icons duplizieren sich manchmal noch
- **Current Fix:** `data-original-label` Attribut
- **Remaining Issue:** Edge Cases bei schnellen Filter-Wechseln?
- **Test:** Mehrfach Filter wechseln, Icons prüfen

### 5. Debug-Switch für Test-Events
- **Status:** 🟡 CONFIG ADDED, NOT WIRED
- **Config:** `_config.yml` → `debug.show_test_events: false`
- **TODO:** Jekyll Template liest Config, filtert test_event: true
- **Location:** `index.html` → Event-Loop
- **Impact:** LOW (nur Development)

### 6. Responsive Filter-Counter
- **Status:** 🟢 WORKING, needs UX polish
- **Issue:** Counter manchmal zu lang auf Mobile ("123 🎉 Konzerte")
- **Idea:** Kürzere Labels auf Mobile (nur Icon + Zahl?)
- **Impact:** LOW (nur UX)

---

## 🌟 Nice-to-Have (später)

### 7. Event-Export (iCal/CSV)
- **Purpose:** Events in Kalender-App importieren
- **Format:** iCalendar (.ics)
- **Location:** Bookmark-Toolbar → "📅 Exportieren" Button
- **Impact:** MEDIUM (Feature-Request)

### 8. Recurring Events UI verbessern
- **Current:** Admin-Panel hat Preview, aber schwer zu editieren
- **Idea:** Visual Recurring Editor (Drag & Drop für Exceptions?)
- **Impact:** LOW (Admin-only)

### 9. Multi-Language Support
- **Current:** Nur Deutsch
- **Target:** Englisch als zweite Sprache
- **Approach:** i18n mit Jekyll Liquid
- **Impact:** HIGH (große Änderung)

### 10. Progressive Web App (PWA)
- **Features:**
  - Offline-Modus
  - App-Install-Prompt
  - Push-Notifications für neue Events
- **Tech:** Service Worker, Web App Manifest
- **Impact:** HIGH (große Feature-Addition)

### 11. Event-Kommentare / Ratings
- **Purpose:** Community-Feedback zu Events
- **Tech:** GitHub Discussions API oder Disqus
- **Privacy:** GDPR-Considerations
- **Impact:** HIGH (Social-Feature)

### 12. Venue-Fotos
- **Purpose:** Bilder von Veranstaltungsorten
- **Source:** Wikimedia Commons oder User-Upload?
- **Location:** Marker-Popups, Event-Cards
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

1. **Erst hierher eintragen** (oder Copilot sagt Bescheid)
2. **Impact-Analyse** → Welche Files betroffen?
3. **Konflikte?** → Überschneidung mit anderen Features?
4. **User bestätigt** → "OK, implementiere #X"
5. **Implementation** → Code-Changes
6. **Update FEATURES.md** → Feature dokumentieren
7. **Update TODO.md** → In "Completed" verschieben
8. **Test** → Manuell + CI
9. **Commit** → Mit Referenz auf TODO #X

**Bei Änderungen an bestehenden Features:**

1. **Check FEATURES.md** → Welche Features betroffen?
2. **Impact warnen** → "Achtung: Betrifft GoatCounter, RSS, etc."
3. **User bestätigt** → "OK, GoatCounter wird angepasst"
4. **Implementation** → Mit extra Vorsicht
5. **Test critical Features** → Feature Guard CI
6. **Update FEATURES.md** → Änderungen dokumentieren

---

**Last Updated:** 2025-11-20  
**Next Review:** Bei jedem neuen Feature-Request  
**Maintainer:** GitHub Copilot + User
