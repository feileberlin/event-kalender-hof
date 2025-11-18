# 🎉 Event-Kalender Hof an der Saale

**hof.ist/jetzt** - Events bis Sonnenaufgang in Hof an der Saale

Ein Jekyll-basierter Event-Kalender für GitHub Pages, der automatisch Events aus verschiedenen Quellen sammelt und auf einer interaktiven Karte darstellt.

## 🌟 Features

- **📍 Interaktive Karte** mit Leaflet.js 1.9.4, immer zentriert auf Hof an der Saale
- **🕐 Zeitfilter "Bis Sonnenaufgang"**: Zeigt nur Events bis zur Morgendämmerung (6:30 Uhr)
- **🔍 Such- und Filterfunktionen**
  - Textsuche (Titel, Beschreibung, Ort)
  - Kategorie-Filter (Musik, Theater, Sport, Kultur, Markt, Fest)
  - Zeitraum-Filter (heute, morgen, nächste 6 Stunden)
  - Radius-Filter (1-10 km, basierend auf Standort)
- **📱 Geolocation**: Browser-Standort für personalisierte Umkreissuche mit Fehlerbehandlung
- **🤖 Automatisches Scraping**: Python-Script sammelt Events von lokalen Websites und Facebook
- **✏️ Admin-Interface**: Einfache Verwaltung von Event-Entwürfen (admin.html)
- **🎨 Minimalistisches Design**: Skeleton CSS Framework, Mobile-First, Touch-optimiert
- **📱 Responsive**: Funktioniert auf Desktop, Tablet, Smartphone
- **🖨️ Druckfreundlich**: Optimierte Print-Styles

## 🛠️ Tech Stack

- **Frontend**: Jekyll 4.3, Skeleton CSS 2.0.4, Leaflet.js 1.9.4
- **JavaScript**: Vanilla ES6+, keine jQuery
- **Backend**: Python 3.11+ (Scraping mit BeautifulSoup, PyYAML)
- **Deployment**: GitHub Pages, GitHub Actions
- **CSS**: Mobile-First, keine Flexbox (nur Skeleton Grid)

## 📋 Inhaltsverzeichnis

- [Installation](#installation)
- [Verwendung](#verwendung)
- [Admin-Dokumentation](#admin-dokumentation)
- [Entwickler-Dokumentation](#entwickler-dokumentation)
- [Event-Struktur](#event-struktur)
- [Chat-Befehle Historie](#chat-befehle-historie)

---

## 🚀 Installation

### Voraussetzungen

- Ruby 3.2+ (für Jekyll)
- Python 3.11+ (für Scraping)
- Git

### Lokale Entwicklung

1. **Repository klonen**
   ```bash
   git clone https://github.com/feileberlin/event-kalender-hof.git
   cd event-kalender-hof
   ```

2. **Jekyll-Dependencies installieren**
   ```bash
   bundle install
   ```

3. **Python-Dependencies installieren**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lokalen Server starten**
   ```bash
   bundle exec jekyll serve
   ```
   
   → Website ist verfügbar unter `http://localhost:4000`

5. **Live-Reload während Entwicklung**
   ```bash
   bundle exec jekyll serve --livereload
   ```

---

## 📖 Verwendung

### Für Benutzer

1. **Website öffnen**: [https://feileberlin.github.io/event-kalender-hof](https://feileberlin.github.io/event-kalender-hof)

2. **Events durchsuchen**:
   - Nutze die Suchleiste für Freitextsuche
   - Filtere nach Kategorie, Zeitraum oder Umkreis
   - Klicke auf "Mein Standort" für GPS-basierte Umkreissuche

3. **Karten-Interaktion**:
   - Klicke auf Marker für Event-Details
   - Event-Karten in der Liste anklicken fokussiert diese auf der Karte

4. **Event-Details**:
   - Klicke auf "Details ansehen" für vollständige Event-Informationen

### Für Admins

1. **Admin-Bereich öffnen**: [/admin.html](https://feileberlin.github.io/event-kalender-hof/admin.html)

2. **Entwürfe prüfen**:
   - Automatisch gescrapte Events erscheinen als "Entwurf"
   - Prüfe Titel, Datum, Ort und Beschreibung

3. **Event publizieren**:
   - Klicke auf "Bearbeiten (GitHub)"
   - Ändere `status: "Entwurf"` zu `status: "Öffentlich"`
   - Committe die Änderung

4. **Event editieren**:
   - Öffne Datei im GitHub Editor
   - Bearbeite YAML Front Matter oder Markdown-Inhalt
   - Speichern und committen

---

## 🔧 Admin-Dokumentation

### Event-Verwaltung

#### Event-Status

- **`Entwurf`**: Automatisch gescrapte oder unveröffentlichte Events (nicht auf Website sichtbar)
- **`Öffentlich`**: Veröffentlichte Events (auf Website sichtbar)

#### Manuelles Event erstellen

1. Neue Datei in `_events/` erstellen: `YYYY-MM-DD-event-titel.md`

2. YAML Front Matter hinzufügen:
   ```yaml
   ---
   title: "Event-Titel"
   date: 2025-11-20
   start_time: "20:00"
   end_time: "23:00"
   location: "Veranstaltungsort"
   address: "Straße 1, 95028 Hof"
   coordinates:
     lat: 50.3197
     lng: 11.9168
   category: "Musik"
   tags:
     - Live-Musik
     - Outdoor
   description: "Kurzbeschreibung"
   url: "https://example.com/event"
   status: "Öffentlich"
   source: "Manuell"
   ---
   ```

3. Optional: Markdown-Inhalt für Details hinzufügen

4. Datei committen und pushen

#### Batch-Operationen

**Alle Entwürfe publizieren** (Linux/Mac):
```bash
cd _events/
for file in *.md; do
  sed -i 's/status: "Entwurf"/status: "Öffentlich"/' "$file"
done
git add .
git commit -m "Publish all drafts"
git push
```

**Alte Events löschen** (älter als 30 Tage):
```bash
find _events/ -name "*.md" -mtime +30 -delete
git add .
git commit -m "Remove old events"
git push
```

### Scraping-Konfiguration

#### Event-Quellen hinzufügen

Datei: `scripts/scrape_events.py`

```python
SOURCES = [
    {
        "name": "Neue Quelle",
        "url": "https://example.com/events",
        "type": "html"
    },
]
```

#### Scraping-Frequenz ändern

Datei: `.github/workflows/scrape-events.yml`

```yaml
on:
  schedule:
    - cron: '0 6,18 * * *'  # Täglich 6:00 und 18:00 UTC
```

Cron-Beispiele:
- `0 * * * *` - Jede Stunde
- `0 0 * * *` - Täglich um Mitternacht
- `0 0 * * 0` - Jeden Sonntag um Mitternacht

#### Manuelles Scraping auslösen

1. GitHub → Actions → "Event Scraper"
2. "Run workflow" → "Run workflow"

---

## 💻 Entwickler-Dokumentation

### Projekt-Struktur

```
event-kalender-hof/
├── _config.yml              # Jekyll-Konfiguration
├── _events/                 # Event-Dateien (YAML + Markdown)
│   └── YYYY-MM-DD-*.md
├── _layouts/                # Jekyll-Layouts
│   ├── default.html         # Haupt-Layout mit Header/Footer
│   └── event.html           # Event-Detail-Seite
├── assets/
│   ├── css/
│   │   └── style.css        # Haupt-Stylesheet
│   └── js/
│       └── main.js          # JavaScript-Logik
├── scripts/
│   └── scrape_events.py     # Event-Scraper
├── .github/
│   └── workflows/
│       ├── jekyll.yml       # Jekyll Build & Deploy
│       └── scrape-events.yml # Automatisches Scraping
├── index.html               # Hauptseite
├── admin.html               # Admin-Interface
├── Gemfile                  # Ruby-Dependencies
└── requirements.txt         # Python-Dependencies
```

### Technologie-Stack

- **Frontend**:
  - Jekyll 4.3 (Static Site Generator)
  - Leaflet.js 1.9.4 (Karten)
  - Vanilla JavaScript (ES6+)
  - CSS3 (Flexbox, Grid)

- **Backend/Automation**:
  - Python 3.11
  - BeautifulSoup4 (HTML-Parsing)
  - Requests (HTTP)
  - PyYAML (YAML-Verarbeitung)

- **CI/CD**:
  - GitHub Actions
  - GitHub Pages

### JavaScript-Funktionen

#### Hauptfunktionen (`assets/js/main.js`)

```javascript
// Karte initialisieren
initMap()

// Events filtern
getUpcomingEvents()           // Nur bis Morgendämmerung
filterAndDisplayEvents()      // Mit Such-/Filter-Optionen

// Benutzerinteraktion
useUserLocation()             // GPS-Standort nutzen
focusEvent(index)             // Event auf Karte fokussieren

// Hilfsfunktionen
calculateDistance(lat1, lon1, lat2, lon2)  // Haversine-Formel
getCategoryColor(category)    // Kategorie → Farbe
getCategoryEmoji(category)    // Kategorie → Emoji
```

#### Event-Datenstruktur (JavaScript)

```javascript
{
  title: "Event-Titel",
  date: "2025-11-20",
  startTime: "20:00",
  endTime: "23:00",
  location: "Veranstaltungsort",
  address: "Straße 1, 95028 Hof",
  coordinates: {lat: 50.3197, lng: 11.9168},
  category: "Musik",
  description: "Beschreibung",
  url: "/events/event-titel/",
  tags: ["Tag1", "Tag2"]
}
```

### Python-Scraper

#### Hauptklasse (`scripts/scrape_events.py`)

```python
class EventScraper:
    def __init__(self)
    def load_existing_hashes(self)
    def generate_event_hash(title, date, time, location)
    def scrape_stadt_hof(url)
    def parse_date(date_text)
    def geocode_location(location)
    def save_events(self)
    def guess_category(title, description)
    def extract_tags(title, description)
    def run()
```

#### Eigenen Scraper implementieren

```python
def scrape_custom_source(self, url):
    """Scrape events from custom website"""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Parse HTML structure
        events = soup.find_all('div', class_='event')
        
        for event in events:
            title = event.find('h2').text.strip()
            # ... extract data ...
            
            self.events.append({
                'title': title,
                'date': event_date,
                # ...
            })
    except Exception as e:
        print(f"Error: {e}")
```

### CSS-Anpassungen

#### Farben ändern

`assets/css/style.css`:

```css
:root {
    --primary-color: #2c3e50;      /* Hauptfarbe */
    --secondary-color: #8b4513;    /* Akzentfarbe */
    --accent-color: #ffaa33;       /* Highlight-Farbe */
}
```

#### Scherenschnitt-Grafiken anpassen

Datei: `_layouts/default.html`

SVG-Elemente in `<svg viewBox="0 0 1200 150">` bearbeiten.

### API-Integration (optional)

#### Geocoding-API

Für präzise Koordinaten kann eine Geocoding-API integriert werden:

```python
import requests

def geocode_location(self, location):
    api_key = os.environ.get('GEOCODING_API_KEY')
    url = f"https://api.opencagedata.com/geocode/v1/json"
    params = {
        'q': f"{location}, Hof an der Saale, Germany",
        'key': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['results']:
        coords = data['results'][0]['geometry']
        return {'lat': coords['lat'], 'lng': coords['lng']}
    return DEFAULT_COORDINATES
```

Dann in GitHub Secrets: `GEOCODING_API_KEY` hinzufügen.

#### KI-gestützte Beschreibungen

Integration mit OpenAI API:

```python
import openai

def create_ai_enhanced_description(self, event_data):
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    
    prompt = f"""
    Erstelle eine ansprechende Event-Beschreibung für:
    
    Titel: {event_data['title']}
    Ort: {event_data['location']}
    Datum: {event_data['date']}
    Original-Beschreibung: {event_data.get('description', 'Keine')}
    
    Die Beschreibung sollte einladend und informativ sein (2-3 Sätze).
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content
```

---

## 📝 Event-Struktur

### YAML Front Matter

| Feld | Typ | Pflicht | Beschreibung |
|------|-----|---------|--------------|
| `title` | String | ✓ | Event-Titel |
| `date` | Date | ✓ | Datum (YYYY-MM-DD) |
| `start_time` | String | ✓ | Startzeit (HH:MM) |
| `end_time` | String | ○ | Endzeit (HH:MM) |
| `location` | String | ✓ | Veranstaltungsort |
| `address` | String | ○ | Vollständige Adresse |
| `coordinates` | Object | ✓ | GPS-Koordinaten |
| `coordinates.lat` | Float | ✓ | Breitengrad |
| `coordinates.lng` | Float | ✓ | Längengrad |
| `category` | String | ○ | Kategorie (siehe unten) |
| `tags` | Array | ○ | Tags/Schlagwörter |
| `description` | String | ○ | Kurzbeschreibung |
| `url` | String | ○ | Externe Event-URL |
| `image` | String | ○ | Bild-URL |
| `status` | String | ✓ | "Entwurf" oder "Öffentlich" |
| `source` | String | ○ | Datenquelle |
| `event_hash` | String | ○ | Hash für Duplikatsprüfung |

### Kategorien

- **Musik** 🎵 - Konzerte, Festivals, Live-Musik
- **Theater** 🎭 - Schauspiel, Kabarett, Comedy
- **Sport** ⚽ - Sportveranstaltungen, Turniere
- **Kultur** 🎨 - Ausstellungen, Lesungen, Kunst
- **Markt** 🛒 - Wochenmärkte, Flohmärkte
- **Fest** 🎉 - Stadtfeste, Volksfeste
- **Sonstiges** 📅 - Andere Events

---

## 📜 Chat-Befehle Historie

### Sitzung vom 17.11.2025

#### Befehl 1: Projekt-Initialisierung
```
erstelle mir einen ghpages-kompatiblen jekyll event-kalender, der stets nur 
die kommenden stunden bis morgendämmerung anzeigt, nicht als tabelle sondern 
als karte mit zentrum rathaus "hof an der saale" oder falls verfügbar mit 
zentrum "koordinaten des Browsers/ Users. Oberhalb dieser Karte finden sich 
eine Suchmaske und weiteren Filtern zur Eingrenzung des Suchergebnisses.
```

**Aktion**: 
- Jekyll-Projekt mit `_config.yml` erstellt
- Leaflet.js-Integration für interaktive Karte
- Suchmaske und Filter implementiert
- Geolocation-Unterstützung hinzugefügt

**Dateien**: `_config.yml`, `index.html`, `assets/js/main.js`, `assets/css/style.css`

---

#### Befehl 2: Automatisches Scraping
```
bitte erstelle cronjobs oder ghpages-alternativen, mit denen man automatisiert 
scraping auf webseiten mit bezug hof an der saale betreiben kann und so Events 
(von Duplikaten befreit) anlegen kann. Diese KI-gestützte Recherche kann dann 
vom Admin editiert und durch Änderung Yaml-Kennzeichnung von "Entwurf" auf 
"Öffentlich" publiziert werden.
```

**Aktion**:
- Python-Scraper mit BeautifulSoup erstellt
- Duplikatsprüfung über Hash-Generierung
- GitHub Actions Workflow für automatisches Scraping (täglich 6:00 & 18:00 UTC)
- Status-System: "Entwurf" → "Öffentlich"

**Dateien**: `scripts/scrape_events.py`, `.github/workflows/scrape-events.yml`, `requirements.txt`

---

#### Befehl 3: Design mit Scherenschnitt
```
zeige in kopf- und fußleiste scherenschnittartig das frivole nachtleben im 
kerzenschein hinter butzenglasscheiben fiktiver wirtshäuser in der altstadt 
von hof an der saale im stile albrecht dürers.
```

**Aktion**:
- SVG-Scherenschnitt-Grafiken im Header erstellt
- Altstadt-Silhouette mit Wirtshäusern und Butzenfenstern
- Footer mit tanzenden Figuren und fröhlichem Nachtleben
- Historisches Flair im Stil der Renaissance

**Dateien**: `_layouts/default.html`, `assets/css/style.css`

---

#### Befehl 4: Dokumentation
```
dokumentiere sämtliche chat-befehle und aktualisiere diese wie auch die 
Dokumentation für Entwickler, Admins und User nach jedem Commit
```

**Aktion**:
- Umfassende README.md erstellt mit:
  - User-Dokumentation (Verwendung)
  - Admin-Dokumentation (Event-Verwaltung)
  - Entwickler-Dokumentation (Code-Struktur, API)
  - Chat-Befehle-Historie (dieser Abschnitt)
- Admin-Interface (`admin.html`) erstellt

**Dateien**: `README.md`, `admin.html`

---

### Weitere Befehle

*Hier werden zukünftige Chat-Befehle und deren Auswirkungen dokumentiert.*

---

## 🔒 Sicherheit & Datenschutz

- **Keine Nutzer-Authentifizierung**: Admin-Bereich ist öffentlich (über GitHub-Login geschützt)
- **Geolocation**: Nur auf Benutzeranfrage, keine Speicherung
- **Externe Ressourcen**: Leaflet.js und OpenStreetMap über CDN
- **Keine Cookies**: Rein statische Website ohne Tracking

---

## 🤝 Beitragen

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Committe deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

---

## 📄 Lizenz

Dieses Projekt ist Open Source. Lizenz: MIT

---

## 🆘 Support & Kontakt

- **Issues**: [GitHub Issues](https://github.com/feileberlin/event-kalender-hof/issues)
- **Diskussionen**: [GitHub Discussions](https://github.com/feileberlin/event-kalender-hof/discussions)

---

## 🎯 Roadmap

### Geplante Features

- [ ] RSS-Feed für Events
- [ ] iCal/Calendar-Export
- [ ] Mehrsprachigkeit (Englisch)
- [ ] Event-Kategorien erweitern
- [ ] Bilder-Upload für Events
- [ ] Social Media Integration
- [ ] PWA (Progressive Web App) Support
- [ ] Dark Mode

### Verbesserungen

- [ ] Erweiterte Geocoding-Unterstützung
- [ ] KI-gestützte Event-Beschreibungen (OpenAI/Claude)
- [ ] Mehr Event-Quellen integrieren
- [ ] Performance-Optimierungen
- [ ] Accessibility-Verbesserungen (WCAG 2.1)

---

## 📊 Statistiken

Aktuelle Projekt-Metriken werden hier automatisch aktualisiert:

- **Events gesamt**: Wird dynamisch berechnet
- **Aktive Quellen**: 2+ (erweiterbar)
- **Letzte Aktualisierung**: Via GitHub Actions

---

**Entwickelt mit ❤️ für Hof an der Saale**
