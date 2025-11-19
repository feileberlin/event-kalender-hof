# GoatCounter Setup Anleitung

## 1. Account erstellen

1. Gehe zu https://www.goatcounter.com/signup
2. Wähle: **Non-commercial** (kostenlos)
3. Code: `event-kalender-hof` (oder dein Wunsch-Name)
4. Email-Adresse angeben
5. Bestätige per Email

## 2. Dashboard konfigurieren

Nach Anmeldung unter https://event-kalender-hof.goatcounter.com/settings:

### Öffentliches Dashboard aktivieren (optional aber empfohlen!)
- Settings → Make stats public ✅
- URL: https://event-kalender-hof.goatcounter.com

### Data Retention
- Standard: 180 Tage (anpassbar)

## 3. Integration (bereits erledigt ✅)

Das Script ist bereits in `_layouts/popart.html` eingefügt:
```html
<script data-goatcounter="https://event-kalender-hof.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
```

## 4. Custom Events (bereits erledigt ✅)

Events werden getrackt:
- **Event-Klicks:** `/event/{category}/{event-name}`
- **Filter-Änderungen:**
  - `/filter/category/{category}`
  - `/filter/time/{timespan}`
  - `/filter/radius/{km}km`
  - `/filter/location/{location}`

## 5. Dashboard nutzen

### Echtzeit-Statistiken
- Unique Visitors (täglich, wöchentlich, monatlich)
- Top-Seiten
- Referrer (woher kommen Besucher)
- Browser & OS
- Bildschirmgrößen
- Länder

### Event-Statistiken
Unter "Pages" siehst du:
- Welche Events am meisten geklickt werden
- Welche Kategorien beliebt sind
- Welche Filter-Einstellungen bevorzugt werden

### Export
- CSV/JSON Export möglich
- API-Zugriff verfügbar

## 6. Wichtig: Domain verifizieren

Nach dem ersten Deploy:
1. Gehe zu https://event-kalender-hof.goatcounter.com
2. Warte ~5 Minuten
3. Erste Daten sollten erscheinen

Falls keine Daten:
- Browser-Console prüfen (F12)
- Network-Tab: Suche nach `gc.zgo.at/count`
- Sollte Status 200 sein

## 7. Widerrufsrecht für User

User können GoatCounter blockieren mit:
- uBlock Origin
- Privacy Badger
- Browser DNS-Block: `gc.zgo.at`

Dies wird in `docs/PRIVACY.md` dokumentiert.

## 8. Kosten

**Non-Commercial (unser Fall):**
- ✅ Komplett kostenlos
- ✅ Unbegrenzte Pageviews
- ✅ Alle Features inklusive

**Commercial:**
- Ab 5€/Monat für bis zu 100.000 Pageviews/Monat

## Fertig! 🎉

Nach dem nächsten Deploy läuft das Tracking automatisch.

Dashboard: https://event-kalender-hof.goatcounter.com (nach Setup öffentlich)
