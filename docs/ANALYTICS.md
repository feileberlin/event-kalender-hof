# GoatCounter Analytics Setup

## Einrichtung (für Repository-Owner)

1. **Account erstellen:** https://www.goatcounter.com/signup
   - Wähle subdomain: `krawl-ist` (Legacy: `event-kalender-hof` für alte Installationen)
   - Email bestätigen

2. **Dashboard öffentlich machen (optional):**
   - Settings → Make stats public
   - Öffentlicher Link: https://krawl-ist.goatcounter.com (Legacy: https://event-kalender-hof.goatcounter.com)

3. **Code ist bereits integriert:**
   ```html
   <script data-goatcounter="https://krawl-ist.goatcounter.com/count"
           async src="//gc.zgo.at/count.js"></script>
   ```

## Was wird getrackt?

### Automatisch:
- ✅ Seitenaufrufe
- ✅ Referrer (woher kommen Besucher)
- ✅ Browser & Geräte
- ✅ Länder (ohne Stadt-Level)
- ✅ Bildschirmgrößen

### Custom Events:
- ✅ **Event-Klicks:** `/event/{event-name}`
- ✅ **Kategorie-Filter:** `/filter/category/{kategorie}`
- ✅ **Zeit-Filter:** `/filter/time/{sunrise|tatort|all}`
- ✅ **Radius-Filter:** `/filter/radius/{1|3|10|999999}km`
- ✅ **Standort-Wechsel:** `/location/{rathaus|bahnhof|browser}`

## Auswertbare Insights

📊 **Event-Popularität:**
- Welche Events werden am häufigsten angeklickt?
- Gibt es Favoriten-Kategorien?

🕐 **Nutzungszeiten:**
- Wann ist die Peak-Zeit? (Wochentag + Uhrzeit)
- Morgens vs. Abends?

🎯 **Filter-Verhalten:**
- Welche Kategorien sind beliebt?
- Nutzen User Zeitfilter oder "alle Events"?
- Durchschnittlicher Suchradius?

📍 **Standort-Präferenzen:**
- Rathaus vs. Bahnhof vs. Browser-Standort
- Wie oft wird Geolocation genutzt?

📱 **Geräte:**
- Desktop vs. Mobile
- Browser-Verteilung

## Privacy-First

✅ Keine Cookies  
✅ Keine IP-Speicherung  
✅ Keine Fingerprinting  
✅ DSGVO-konform ohne Consent-Banner  
✅ Öffentliches Dashboard (Transparenz)  

## Dashboard-Zugang

**Öffentlich:** https://krawl-ist.goatcounter.com (falls aktiviert)  
**Admin:** Login auf goatcounter.com mit Account-Email

## Support

- Dokumentation: https://www.goatcounter.com/help
- GitHub: https://github.com/arp242/goatcounter
