# 🗺️ Karten-Styling für Forks

**Ziel:** Die Karte soll **Events betonen**, nicht die Stadt dokumentieren.

---

## 🎨 Aktuelles Design (Krawl.ist Default)

**Prinzip:** Karte wird visuell zurückgedrängt, Events leuchten hervor.

```css
/* assets/css/fullscreen.css */
.fullscreen-map .leaflet-tile-pane {
    filter: grayscale(80%) contrast(0.9) brightness(1.1);
    opacity: 0.7;
}
```

**Effekt:**
- 🗺️ Karte: Grau, dezent, verschwommen
- 📍 Events: Farbig, scharf, prominent
- 🏙️ Straßennamen: Kaum sichtbar (opacity 0.4)

---

## 🛠️ Anpassungen für Forks

### **1. Minimalistische Schwarz-Weiß-Karte (Punk/Indie-Ästhetik)**

Perfekt für: Underground-Szenen, Kunst-Communities, politische Gruppen

```css
.fullscreen-map .leaflet-tile-pane {
    filter: grayscale(100%) contrast(1.3) brightness(0.9);
    opacity: 0.5;
}
```

**Variante "Inverted":**
```css
.fullscreen-map .leaflet-tile-pane {
    filter: invert(1) grayscale(100%) contrast(1.2);
    opacity: 0.6;
}
```

---

### **2. Subtile Farb-Akzente (Moderne Stadt-Apps)**

Perfekt für: Städte-Kalender, Family-Events, Mainstream-Communities

```css
.fullscreen-map .leaflet-tile-pane {
    filter: saturate(0.3) contrast(0.8) brightness(1.2);
    opacity: 0.8;
}
```

**Effekt:** Karte bleibt farbig, aber sehr dezent.

---

### **3. Retro-Sepia (Vintage/Nostalgie-Vibe)**

Perfekt für: Historische Events, Oldtimer-Clubs, Retro-Gaming

```css
.fullscreen-map .leaflet-tile-pane {
    filter: sepia(60%) contrast(0.9) brightness(1.1);
    opacity: 0.75;
}
```

---

### **4. Hochkontrast (Accessibility-First)**

Perfekt für: Barrierefreie Events, Senior-Communities

```css
.fullscreen-map .leaflet-tile-pane {
    filter: contrast(1.5) brightness(1.2);
    opacity: 1;
}

.fullscreen-map .leaflet-overlay-pane {
    opacity: 1; /* Labels gut lesbar */
}
```

---

## 🌍 Alternative Tile-Provider

Statt Standard-OpenStreetMap kannst du in `assets/js/modules/map.js` den Tile-Provider ändern:

### **Stamen Toner (Minimalistisch, Schwarz-Weiß)**

```javascript
// In map.js, Zeile ~30
const tileLayer = L.tileLayer('https://tiles.stadiamaps.com/tiles/stamen_toner/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; Stamen Design',
  maxZoom: 18
});
```

**Effekt:** Ultra-minimalistisch, nur Straßen, keine Farben.

### **Carto Positron (Hell & Clean)**

```javascript
const tileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; CartoDB',
  maxZoom: 19
});
```

**Effekt:** Sehr helle, neutrale Karte - perfekt für bunte Event-Marker.

### **Carto Dark Matter (Dunkel & Modern)**

```javascript
const tileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; CartoDB',
  maxZoom: 19
});
```

**Effekt:** Dunkler Hintergrund - Events leuchten hervor (Nightlife, Clubs).

---

## 🎯 Quick-Start: Deine Stadt in 3 Schritten stylen

### **Schritt 1: Teste CSS-Filter**

Öffne Browser-DevTools (F12), füge temporär ein:

```css
#map .leaflet-tile-pane {
  filter: grayscale(100%) contrast(1.5);
}
```

Experimentiere mit Werten, bis es passt!

### **Schritt 2: Werte in `fullscreen.css` übernehmen**

Ersetze den `.fullscreen-map .leaflet-tile-pane` Block mit deinen Werten.

### **Schritt 3: Optional - Tile-Provider wechseln**

Bearbeite `assets/js/modules/map.js`, Zeile ~30:

```javascript
const tileLayer = L.tileLayer('DEINE_TILE_URL_HIER', {
  attribution: 'Deine Attribution',
  maxZoom: 18
});
```

---

## 🔧 Profi-Tools für Custom-Karten

### **1. Mapbox Studio (Kostenlos bis 50k Views/Monat)**

1. Gehe zu: [mapbox.com/mapbox-studio](https://www.mapbox.com/mapbox-studio/)
2. Erstelle einen Account
3. Wähle "New Style" → "Monochrome" oder "Blank"
4. Passe Farben, Layer-Visibility an
5. Publishe und kopiere die Tile-URL
6. Füge in `map.js` ein:

```javascript
const tileLayer = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
  id: 'DEIN_STYLE_ID',
  accessToken: 'DEIN_ACCESS_TOKEN',
  tileSize: 512,
  zoomOffset: -1
});
```

### **2. Maputnik (Open Source, Self-Hosted)**

1. Gehe zu: [maputnik.github.io](https://maputnik.github.io/)
2. Lade einen Basis-Style (z.B. OSM Liberty)
3. Editiere Layer, Farben, Fonts
4. Exportiere JSON
5. Hoste selbst oder nutze mit Maptiler/Mapbox

---

## 📐 Best Practices

### **DO:**
✅ Karte visuell zurückdrängen (Events sind der Star)  
✅ Hoher Kontrast zwischen Karte und Event-Markern  
✅ Testen auf Mobile & Desktop  
✅ Accessibility beachten (Kontrast, Lesbarkeit)

### **DON'T:**
❌ Karte komplett schwarz/unsichtbar machen  
❌ Zu viele CSS-Filter stapeln (Performance!)  
❌ Event-Marker mit filter: grayscale() treffen  
❌ Labels komplett ausblenden (Orientierung!)

---

## 🧪 Filter-Kombinationen (Cheatsheet)

```css
/* Ultra-Minimal (Punk) */
filter: grayscale(100%) contrast(1.5) brightness(0.8);
opacity: 0.4;

/* Soft & Subtle (Mainstream) */
filter: saturate(0.2) contrast(0.8) brightness(1.3);
opacity: 0.9;

/* High-Contrast (Accessibility) */
filter: contrast(1.8) brightness(1.1);
opacity: 1;

/* Vintage Sepia */
filter: sepia(70%) contrast(0.9) saturate(0.5);
opacity: 0.7;

/* Inverted Dark Mode */
filter: invert(1) hue-rotate(180deg) contrast(1.1);
opacity: 0.6;
```

---

## 🎨 Beispiel-Screenshots

_(In einer zukünftigen Version könnte hier eine Galerie mit Vorher/Nachher-Vergleichen stehen)_

---

## 🆘 Support

- **GitHub Discussions:** [krawl.ist/discussions](https://github.com/feileberlin/krawl.ist/discussions)
- **CSS-Filter-Referenz:** [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/filter)
- **Leaflet Tile-Provider-Übersicht:** [leaflet-extras.github.io/leaflet-providers](https://leaflet-extras.github.io/leaflet-providers/preview/)

---

**Krawall hier. Krawall jetzt. - Aber mit Style.** 🎸
