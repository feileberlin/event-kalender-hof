# 👥 Veranstalter-CRM für Event-Redaktion

## Überblick

Das **Veranstalter-CRM** (Customer Relationship Management) ist in das Deduplication-System integriert und unterstützt Redakteure beim **Networking** und der **Recherche** zu Event-Veranstaltern.

## Features

### 📇 Zentrale Kontaktdatenbank
Alle Veranstalter-Informationen in einer CSV-Datei: `_data/organizers.csv`

### 🔍 Automatische Zuordnung
Das System ordnet Events automatisch den passenden Veranstaltern zu:
- **Direkter Match**: Event hat `organizer`-Feld
- **Alias-Match**: Event nutzt einen Alias-Namen
- **Venue-Match**: Event findet am typischen Venue des Veranstalters statt (70% Konfidenz)

### 📊 Pattern Recognition
System lernt, welche Veranstalter typischerweise:
- Welche Kanäle nutzen (Facebook, Website, Newsletter)
- Welche Venues bevorzugen
- Wie oft Events veranstalten

## Datenstruktur

### organizers.csv Spalten

```csv
name,aliases,verified_sources,typical_venues,website,contact_email,contact_phone,
contact_person,contact_role,social_media_facebook,social_media_instagram,
press_contact,press_email,press_phone,best_contact_time,preferred_contact_method,
notes,last_updated,last_contact_date,relationship_status
```

#### Basis-Informationen
- **name**: Offizieller Name des Veranstalters
- **aliases**: Alternative Namen (komma-separiert)
- **website**: Haupt-Website
- **verified_sources**: Bekannte Quellen (z.B. `facebook-stadt-hof,newsletter-hof`)
- **typical_venues**: Häufig genutzte Veranstaltungsorte

#### Kontaktdaten
- **contact_email**: Allgemeine E-Mail-Adresse
- **contact_phone**: Telefonnummer (Format: `+49 9281 815 0`)
- **contact_person**: Name des Ansprechpartners
- **contact_role**: Position (z.B. "Pressereferentin", "Geschäftsführer")

#### Presse-Kontakt
- **press_contact**: Name des Pressekontakts (falls abweichend)
- **press_email**: Presse-E-Mail
- **press_phone**: Presse-Telefon

#### Social Media
- **social_media_facebook**: Facebook-URL (vollständig)
- **social_media_instagram**: Instagram-Handle (mit oder ohne @)

#### CRM-Metadaten
- **best_contact_time**: Empfohlene Kontaktzeit (z.B. "Mo-Fr 9-16 Uhr")
- **preferred_contact_method**: Bevorzugter Kanal (E-Mail, Telefon, Social Media)
- **notes**: Interne Notizen zur Zusammenarbeit
- **last_contact_date**: Datum des letzten Kontakts (YYYY-MM-DD)
- **relationship_status**: Beziehungsstatus
  - `new`: Neu, noch kein Kontakt
  - `active`: Aktive Zusammenarbeit
  - `established`: Etablierte Partnerschaft
  - `inactive`: Kontakt schlief ein

## Beispiel-Eintrag

```csv
Stadt Hof,"Stadtverwaltung Hof,Hof Marketing","stadt-hof,facebook-stadt-hof",
"Freiheitshalle Hof,Altstadt Hof",https://www.hof.de,presse@hof.de,
+49 9281 815 0,Maria Schmidt,Pressereferentin,
https://www.facebook.com/StadtHof,@stadt_hof,Maria Schmidt,
presse@hof.de,+49 9281 815 1234,Mo-Fr 9-16 Uhr,E-Mail,
Offizielle Veranstaltungen - sehr zuverlässig,2025-11-20,
2025-11-15,established
```

## Admin-Interface Integration

### Anzeige im Duplikate-Tab

Wenn das System einen Veranstalter für ein Event identifiziert, wird eine **Veranstalter-Kontakt-Karte** angezeigt:

```
┌─────────────────────────────────────────────────────┐
│ 👤 Veranstalter-Kontakt     [established]          │
├─────────────────────────────────────────────────────┤
│ 👤 Ansprechpartner          📧 E-Mail               │
│ Maria Schmidt               presse@hof.de           │
│ (Pressereferentin)                                  │
│                                                     │
│ 📞 Telefon                  📰 Presse-Kontakt       │
│ +49 9281 815 0              Maria Schmidt           │
│                             presse@hof.de           │
│                                                     │
│ ⏰ Beste Erreichbarkeit     ✉️ Bevorzugter Kanal   │
│ Mo-Fr 9-16 Uhr              E-Mail                  │
│                                                     │
│ 🌐 Website                  📅 Letzter Kontakt      │
│ https://www.hof.de          15.11.2025              │
├─────────────────────────────────────────────────────┤
│ 📝 Notizen: Offizielle Veranstaltungen -           │
│            sehr zuverlässig                         │
├─────────────────────────────────────────────────────┤
│ [📧 E-Mail schreiben] [📞 Anrufen]                 │
│ [📘 Facebook] [📷 Instagram]                        │
└─────────────────────────────────────────────────────┘
```

### Quick Actions

Die Kontakt-Karte bietet **One-Click-Aktionen**:

1. **📧 E-Mail schreiben**: Öffnet E-Mail-Client mit vorausgefülltem Betreff
2. **📞 Anrufen**: tel:-Link für direkte Anwahl
3. **📘 Facebook**: Öffnet Facebook-Seite
4. **📷 Instagram**: Öffnet Instagram-Profil

## Workflow

### 1. Veranstalter erfassen

```bash
# Manuell in _data/organizers.csv editieren
# ODER via Python-Script (TODO)
python3 scripts/organizer_manager.py add \
  --name "Stadt Hof" \
  --contact-email "presse@hof.de" \
  --contact-person "Maria Schmidt"
```

### 2. Events scrapen

```bash
python3 scripts/editorial/scrape_events.py
```

### 3. Deduplication mit Veranstalter-Matching

```bash
python3 scripts/editorial/deduplication_engine.py
```

Output:
```
🔍 Deduplication Engine gestartet...
📊 5 Veranstalter geladen
📄 47 Event-Dateien gefunden
  → 2025-12-15-weihnachtsmarkt-hof.md: Cluster cluster_1_a3f2b8c9
    👤 Veranstalter: Stadt Hof (direct match)
  
📊 Ergebnis: 42 Cluster gefunden
✅ 5 Events mit Veranstalter-Kontakten verknüpft
```

### 4. Admin-Review mit Kontakten

```bash
bundle exec jekyll serve
# http://localhost:4000/event-kalender-hof/admin.html
```

Im Admin-Interface:
1. Tab **"🔄 Duplikate"** öffnen
2. Event mit Veranstalter-Kontakt sehen
3. **📧 E-Mail schreiben** klicken → E-Mail-Client öffnet sich
4. Nachfrage beim Veranstalter zur Verifizierung

### 5. Kontakt dokumentieren

Nach Kontakt zurück zu `organizers.csv`:
```csv
...,last_contact_date,relationship_status
...,2025-11-20,active
```

## Automatisierung

### GitHub Actions: Kontakt-Reminder

```yaml
# .github/workflows/contact-reminder.yml
name: Contact Reminder

on:
  schedule:
    - cron: '0 9 * * 1'  # Jeden Montag 9:00 Uhr

jobs:
  remind:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check stale contacts
        run: |
          python3 scripts/check_stale_contacts.py
      
      - name: Create Issue
        if: env.STALE_CONTACTS > 0
        uses: actions/create-issue@v2
        with:
          title: "📞 Kontakt-Reminder: ${{ env.STALE_CONTACTS }} Veranstalter"
          body: |
            Folgende Veranstalter wurden länger nicht kontaktiert:
            
            ${{ env.STALE_LIST }}
```

### Python-Script: check_stale_contacts.py

```python
#!/usr/bin/env python3
import csv
from datetime import datetime, timedelta
from pathlib import Path

ORGANIZERS_CSV = Path("_data/organizers.csv")
STALE_THRESHOLD_DAYS = 90  # 3 Monate

with open(ORGANIZERS_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    stale_contacts = []
    
    for row in reader:
        last_contact = row.get('last_contact_date')
        if last_contact:
            days_ago = (datetime.now() - datetime.fromisoformat(last_contact)).days
            if days_ago > STALE_THRESHOLD_DAYS:
                stale_contacts.append({
                    'name': row['name'],
                    'days_ago': days_ago,
                    'contact': row.get('contact_person', 'N/A')
                })

if stale_contacts:
    print(f"::set-env name=STALE_CONTACTS::{len(stale_contacts)}")
    stale_list = "\n".join([
        f"- **{c['name']}** ({c['contact']}): {c['days_ago']} Tage"
        for c in stale_contacts
    ])
    print(f"::set-env name=STALE_LIST::{stale_list}")
```

## Erweiterte Features (Zukunft)

### 1. Vollständiges CRM-Interface

Separates Admin-Tab für Veranstalter-Verwaltung:

```html
Tab: 👥 Veranstalter
- Liste aller Veranstalter
- Filterung nach relationship_status
- Sortierung nach last_contact_date
- CRUD-Operationen (Create, Read, Update, Delete)
- Export als vCard
```

### 2. Kontakt-Historie

```csv
# _data/contact_history.csv
date,organizer,type,notes,next_action
2025-11-20,Stadt Hof,email,Event-Anfrage Weihnachtsmarkt,Antwort abwarten
2025-11-15,Freiheitshalle,phone,Spielplan Q1 2026 besprochen,Follow-up in 2 Wochen
```

### 3. Automatische E-Mail-Vorlagen

```javascript
function sendEventInquiry(organizer, event) {
    const template = `
Hallo ${organizer.contact_person},

wir haben Ihr Event "${event.title}" am ${event.date} auf ${event.source} gefunden.

Könnten Sie uns folgende Informationen bestätigen:
- Startzeit: ${event.start_time || 'noch nicht bekannt'}
- Eintrittspreise: ${event.price || 'noch nicht bekannt'}
- Barrierefreiheit: ${event.wheelchair_accessible || 'noch nicht bekannt'}

Vielen Dank!

Mit freundlichen Grüßen,
[Ihr Name]
Event-Kalender Hof
`;
    
    window.location.href = `mailto:${organizer.contact_email}?subject=Event-Anfrage: ${event.title}&body=${encodeURIComponent(template)}`;
}
```

### 4. Integration mit externen Tools

#### Google Contacts Sync
```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

def sync_to_google_contacts():
    """Synchronisiert organizers.csv mit Google Contacts"""
    service = build('people', 'v1', credentials=creds)
    
    for org in load_organizers():
        contact = {
            'names': [{'displayName': org['name']}],
            'emailAddresses': [{'value': org['contact_email']}],
            'phoneNumbers': [{'value': org['contact_phone']}],
            'organizations': [{'name': org['name'], 'title': org['contact_role']}]
        }
        service.people().createContact(body=contact).execute()
```

#### Slack-Benachrichtigungen
```yaml
# Bei neuem Event: Slack-Message mit Veranstalter-Kontakt
- name: Notify Slack
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Neues Event gefunden!",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*${{ event.title }}*\n📅 ${{ event.date }}\n👤 Veranstalter: ${{ organizer.name }}"
            }
          },
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": "📧 Kontaktieren",
                "url": "mailto:${{ organizer.contact_email }}"
              }
            ]
          }
        ]
      }
```

## Best Practices

### Datenpflege
1. **Regelmäßig aktualisieren**: `last_contact_date` nach jedem Kontakt updaten
2. **Relationship Status pflegen**: `new` → `active` → `established`
3. **Notizen führen**: Wichtige Infos in `notes` eintragen

### Datenschutz
- **DSGVO-konform**: Nur öffentlich verfügbare oder mit Einwilligung erhaltene Daten
- **Kein Public Repo**: `organizers.csv` mit sensiblen Daten NICHT committen
- **Alternative**: Private Submodule oder verschlüsselte Datei

```bash
# .gitignore
_data/organizers.csv  # Sensible Kontaktdaten nicht committen
_data/organizers.example.csv  # Beispiel-Template committen
```

### Datensicherheit
```bash
# Verschlüsselung mit GPG
gpg --encrypt --recipient your-email@example.com _data/organizers.csv

# Im Repo nur verschlüsselt
git add _data/organizers.csv.gpg

# Lokal entschlüsseln
gpg --decrypt _data/organizers.csv.gpg > _data/organizers.csv
```

## Troubleshooting

### "Veranstalter nicht gefunden"
→ Prüfe, ob Event `organizer`-Feld hat oder Location in `typical_venues` eingetragen ist

### "Match-Type: venue_based (70% Konfidenz)"
→ System vermutet Veranstalter aufgrund des Venues, aber nicht 100% sicher
→ Manuell prüfen und ggf. `organizer`-Feld im Event setzen

### "Quick Actions funktionieren nicht"
→ Browser blockiert `mailto:` oder `tel:` Links
→ In Browser-Einstellungen erlauben

## Export & Import

### CSV-Export für Excel/Google Sheets
```bash
# Direkt editierbar in Excel
open _data/organizers.csv
```

### vCard-Export (für Outlook/Thunderbird)
```python
#!/usr/bin/env python3
import csv
import vobject

with open('_data/organizers.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        vcard = vobject.vCard()
        vcard.add('fn').value = row['name']
        vcard.add('email').value = row['contact_email']
        vcard.add('tel').value = row['contact_phone']
        
        with open(f"contacts/{row['name']}.vcf", 'w') as vcf:
            vcf.write(vcard.serialize())
```

## Lizenz

MIT - siehe [LICENSE](../LICENSE)
