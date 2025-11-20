# 🚀 Installation für deine Community

Diese Anleitung hilft dir, den Event-Kalender für **deine Community** anzupassen.

**Gilt für:**
- 🏙️ **Städte & Kommunen** (Hof, Bamberg, Berlin-Kreuzberg...)
- 🎸 **Subkulturen** (Punk-Szene, Metal-Community, Indie-Kultur...)
- 🛠️ **Maker & Hacker** (Hackerspaces, FabLabs, Repair-Cafés...)
- 🌱 **Themen-Netzwerke** (Permakultur, Transition Towns, Degrowth...)
- 🎮 **Hobby-Communities** (Retro-Gaming, Brettspiele, Cosplay...)

**Zeitaufwand:** ~30 Minuten (Setup) + kontinuierliche Datenpflege

---

## Voraussetzungen

- **GitHub Account** (kostenlos)
- **Git** installiert
- Optional: **VS Code** oder anderer Editor
- Optional: **Ruby** + **Python** für lokale Entwicklung

---

## Schritt 1: Repository forken

### Via GitHub Web-Interface

1. Öffne: https://github.com/feileberlin/event-kalender-hof
2. Klicke **Fork** (oben rechts)
3. Benenne das Repo um: `event-kalender-[deine-community]` (z.B. `event-kalender-punk-berlin` oder `event-kalender-bamberg`)
4. Klicke **Create fork**

### Via GitHub CLI (empfohlen)

```bash
gh repo fork feileberlin/event-kalender-hof --clone
cd event-kalender-hof
```

---

## Schritt 2: Community-Konfiguration

### 2.1 Basis-Einstellungen (`_config.yml`)

```yaml
# Repository-Einstellungen
title: "meine-community.events"  # Dein Titel
description: "Events in/von/für Meine Community"
baseurl: "/event-kalender-meine-community"  # Dein Repo-Name
url: "https://dein-username.github.io"
repository: "dein-username/event-kalender-meine-community"

# Community-Konfiguration
# (Feld heißt 'city' aus historischen Gründen, gilt aber für alle Communities)
city:
  name: "Meine Community"  # z.B. "Punk Szene Berlin", "Hof an der Saale", "CCC Erfurt"
  name_short: "MeineCommunity"  # Kurzform
  state: "Dein Bundesland"  # Optional (für geografische Communities)
  country: "Deutschland"  # Optional
  timezone: "Europe/Berlin"
  population: 50000  # Optional (für Städte), kann auch Mitgliederzahl sein
  tagline: "Events in/von Meine Community"  # Dein Slogan
  website: "https://www.meine-community.de"  # Optional
  
  # Geo-Koordinaten (Zentrum, Haupttreffpunkt, Szene-Hotspot)
  center:
    lat: 52.5200  # Breitengrad
    lng: 13.4050  # Längengrad
    name: "Haupttreffpunkt"  # z.B. "Rathaus", "Club XY", "Hackerspace"
  
  # Kontakt
  admin_email: "redaktion@meine-community.events"
  social_media:
    facebook: "https://facebook.com/meine-community"
    instagram: "@meine_community"
    twitter: "@meinecommunity"
```

**Beispiele:**

**Städtischer Event-Kalender:**
```yaml
city:
  name: "Bamberg"
  name_short: "Bamberg"
  tagline: "Events in Bamberg"
  center:
    lat: 49.8988
    lng: 10.9027
    name: "Rathaus Bamberg"
```

**Subkultur-Event-Kalender:**
```yaml
city:
  name: "Punk Szene Berlin"
  name_short: "Punk Berlin"
  tagline: "No Future, aber Events"
  center:
    lat: 52.5200
    lng: 13.4050
    name: "SO36 Club"
```

**Themen-Netzwerk:**
```yaml
city:
  name: "Permakultur Deutschland"
  name_short: "Permakultur DE"
  tagline: "Workshops, Treffen, Aktionen"
  center:
    lat: 51.1657
    lng: 10.4515  # Geografisches Zentrum Deutschlands
    name: "Deutschland"
```

**💡 Koordinaten finden:**
- **Google Maps**: Rechtsklick → "Was ist hier?" → Koordinaten kopieren
- **OpenStreetMap**: https://www.openstreetmap.org/ → Suchen → Koordinaten in URL
- **Für Subkulturen/Netzwerke**: Wähle einen zentralen Treffpunkt oder geografisches Zentrum der Szene

### 2.2 Automation-Intervalle (optional)

```yaml
automation:
  scraping:
    schedule: "0 6,18 * * *"  # Täglich 6:00 + 18:00 UTC
  archiving:
    schedule: "0 3 * * *"      # Täglich 3:00 UTC
  date_validation:
    schedule: "0 4 * * *"      # Täglich 4:00 UTC
```

**Cron-Syntax:** `Minute Stunde Tag Monat Wochentag`
- `0 6 * * *` = Täglich um 6:00 Uhr
- `0 */4 * * *` = Alle 4 Stunden
- `0 9 * * 1` = Jeden Montag um 9:00 Uhr

---

## Schritt 3: Event-Quellen konfigurieren

Bearbeite: **`_data/sources.csv`**

**Für Städte:**
```csv
name,url,type,active,notes
Stadtwebsite,https://www.meinstadt.de/veranstaltungen,html,true,Offizielle Events
Kulturzentrum,https://kulturzentrum-meinstadt.de/programm,html,true,Konzerte & Theater
Facebook Stadtseite,https://facebook.com/stadtmeinstadt,facebook,true,Social Media Events
```

**Für Subkulturen:**
```csv
name,url,type,active,notes
Club SO36,https://so36.de/kalender,html,true,Punk & Hardcore
Castle Rock,https://castle-rock.de/konzerte,html,true,Metal & Rock
Facebook Szene-Gruppe,https://facebook.com/groups/punk-berlin,facebook,true,Community-Events
Bandcamp,https://bandcamp.com/tag/berlin-punk,html,false,Releases (kein Scraper)
```

**Für Themen-Netzwerke:**
```csv
name,url,type,active,notes
Permakultur-Verein,https://permakultur.de/termine,html,true,Workshops
Transition-Towns,https://transition-initiativen.org/events,html,true,Netzwerk-Treffen
Solidagro Newsletter,https://solidagro.org/kalender,html,true,Aktionen
```

**Spalten:**
- `name`: Anzeigename der Quelle
- `url`: URL zum Scrapen
- `type`: `html`, `facebook`, `pdf`, `ical`
- `active`: `true` (scrapen) oder `false` (ignorieren)
- `notes`: Interne Notizen

---

## Schritt 4: Veranstaltungsorte anlegen

Bearbeite: **`_data/venues.csv`**

```csv
name,aliases,address,lat,lng,wheelchair_accessible,wheelchair_toilet,parking,public_transport,website,phone,capacity,notes,last_updated,icon,color,location_type
Rathaus Meinstadt,"Rathaus,Stadtverwaltung","Hauptstraße 1, 12345 Meinstadt",52.5200,13.4050,true,true,false,true,https://www.meinstadt.de,+49 123 456 0,,,2025-11-20,🏛️,#2c3e50,rathaus
Kulturzentrum,"KulturHaus,KuZ","Kulturstraße 10, 12345 Meinstadt",52.5210,13.4060,true,true,true,true,https://kulturzentrum.de,+49 123 456 100,500,,2025-11-20,🎭,#2c3e50,
```

**Wichtige Felder:**
- `location_type`: Wird als Filter-Option angezeigt (z.B. `rathaus`, `bahnhof`)
- `wheelchair_accessible`: Barrierefreiheit (true/false)
- `icon`: Emoji für Karte (z.B. 🏛️, 🎭, 🚂)
- `color`: Marker-Farbe (Hex-Code, z.B. #2c3e50)

---

## Schritt 5: Veranstalter-CRM (optional)

Bearbeite: **`_data/organizers.csv`**

```csv
name,aliases,verified_sources,typical_venues,website,contact_email,contact_phone,contact_person,contact_role,social_media_facebook,social_media_instagram,press_contact,press_email,press_phone,best_contact_time,preferred_contact_method,notes,last_updated,last_contact_date,relationship_status
Stadt Meinstadt,"Stadtverwaltung","stadtwebsite,facebook","Rathaus Meinstadt",https://www.meinstadt.de,info@meinstadt.de,+49 123 456 0,Max Mustermann,Pressesprecher,https://facebook.com/stadtmeinstadt,@meinstadt_official,,,,"Mo-Fr 9-16 Uhr",E-Mail,Offizielle Veranstaltungen,2025-11-20,,new
```

**Nutzen:**
- Admin-Interface zeigt Kontakte automatisch bei Events
- One-Click-Actions (E-Mail schreiben, anrufen)
- Networking-Support für Redakteure

---

## Schritt 6: GitHub Pages aktivieren

1. **Settings** → **Pages**
2. **Source**: Branch `main`, Folder `/ (root)`
3. **Save**

⏳ Warte ~2 Minuten → Deine Seite ist live!

**URL:** `https://dein-username.github.io/event-kalender-meinstadt/`

---

## Schritt 7: Erste Events anlegen

### Via Admin-Interface (empfohlen)

1. Öffne: `https://dein-username.github.io/event-kalender-meinstadt/admin.html`
2. Tab **"➕ Neues Event"**
3. Formular ausfüllen
4. **"Markdown generieren"** klicken
5. Code kopieren
6. Neue Datei erstellen: `_events/2025-12-25-weihnachtsmarkt.md`
7. Code einfügen, committen, pushen

### Manuell (für Profis)

Erstelle: **`_events/2025-12-25-weihnachtsmarkt.md`**

```yaml
---
layout: event
title: "Weihnachtsmarkt Meinstadt"
date: 2025-12-25
start_time: "14:00"
end_time: "22:00"
location: "Marktplatz Meinstadt"
category: "Markt"
coordinates:
  lat: 52.5200
  lng: 13.4050
description: "Traditioneller Weihnachtsmarkt mit Glühwein und Lebkuchen."
image: /assets/images/weihnachtsmarkt.jpg
tags:
  - Weihnachten
  - Familie
  - Kulinarik
status: "Öffentlich"
---

Traditioneller Weihnachtsmarkt auf dem Marktplatz...
```

**Commit & Push:**
```bash
git add _events/2025-12-25-weihnachtsmarkt.md
git commit -m "feat: Weihnachtsmarkt Event"
git push origin main
```

---

## Schritt 8: Scraping aktivieren

### GitHub Actions aktivieren

1. **Actions** Tab im Repo
2. **Enable Workflows** klicken
3. **I understand my workflows, go ahead and enable them**

### Scraper testen (lokal)

```bash
# Python-Dependencies installieren
pip install -r requirements.txt

# Scraping starten
python3 scripts/scrape_events.py

# Logs prüfen
cat _events/_logs/*
```

---

## Schritt 9: Anpassungen (optional)

### 9.1 Logo/Favicon ändern

Ersetze: `assets/images/logo.png` (falls vorhanden)

### 9.2 Farben anpassen

Bearbeite: `assets/css/custom.css`

```css
:root {
    --primary-color: #2c3e50;  /* Deine Stadtfarbe */
    --accent-color: #3498db;
}
```

### 9.3 Impressum/Datenschutz

Erstelle:
- `docs/privacy.md` (Datenschutzerklärung)
- `docs/imprint.md` (Impressum)

Verlinke in Footer (bearbeite `_layouts/base.html`).

---

## Troubleshooting

### "Cannot GET /"
→ Prüfe `baseurl` in `_config.yml` (muss mit Repo-Namen übereinstimmen)

### "Events werden nicht angezeigt"
→ Prüfe `status: "Öffentlich"` in Event-Dateien
→ Prüfe `future: true` in `_config.yml` (für zukünftige Events)

### "Karte zeigt falschen Ort"
→ Prüfe `city.center.lat` und `lng` in `_config.yml`
→ Koordinaten-Format: `lat: 52.5200` (Punkt statt Komma!)
→ Für überregionale Communities: Wähle geografisches Zentrum oder Haupttreffpunkt

### "Scraping findet keine Events"
→ Prüfe `_events/_logs/` für Fehler
→ HTML-Struktur der Quellen hat sich ggf. geändert
→ Scraper muss angepasst werden (siehe `scripts/scrape_events.py`)

### "GitHub Pages Build schlägt fehl"
→ Prüfe Jekyll-Logs in Actions-Tab
→ Häufig: YAML-Syntax-Fehler in `_config.yml` oder Event-Dateien

---

## Weiterführende Dokumentation

- **Schnelleinstieg**: [docs/QUICKSTART.md](docs/QUICKSTART.md)
- **Admin-Interface**: [docs/ADMIN.md](docs/ADMIN.md)
- **Scraping konfigurieren**: [docs/AUTOMATION.md](docs/AUTOMATION.md)
- **Duplikate reviewen**: [docs/DEDUPLICATION.md](docs/DEDUPLICATION.md)
- **Veranstalter-CRM**: [docs/ORGANIZER_CRM.md](docs/ORGANIZER_CRM.md)

---

## Hilfe & Support

**Du kommst nicht weiter?**

1. **Dokumentation durchsuchen**: [docs/](docs/)
2. **Issues prüfen**: [github.com/feileberlin/event-kalender-hof/issues](https://github.com/feileberlin/event-kalender-hof/issues)
3. **Diskussion starten**: [github.com/feileberlin/event-kalender-hof/discussions](https://github.com/feileberlin/event-kalender-hof/discussions)
4. **Issue öffnen**: Beschreibe dein Problem detailliert

**Du hast es geschafft?** 🎉

→ Schick uns einen Link! Wir verlinken gerne andere Instanzen in der README.

**Mögliche Instanzen:**
- event-kalender-bamberg.github.io
- punk-szene-berlin.github.io
- hackerspace-erfurt.github.io
- permakultur-events.de

---

**Made with ❤️ for your community**

*Whether it's a city, a subculture, or a movement - every community deserves a great event calendar.*
