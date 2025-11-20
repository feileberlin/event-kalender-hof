# Krawl - Projekt-Historie

**Zeitraum:** 17.-20. November 2025  
**Zusammenarbeit:** User + GitHub Copilot (Claude Sonnet 4.5)

> *"Für mich ist unsere Zusammenarbeit historisch im Sinne von gänzlich neuer Erfahrung und wahrhaft inspirierend, als hätte man ein echt geiles Team um sich, das 100% gibt."*

---

## 🎯 Erreichte Meilensteine

### **Tag 1-2: Technische Fundamente**
- ✅ CSV-System vereinheitlicht (venues.csv + locations.csv gemerged)
- ✅ Deduplication-Engine implementiert (Fuzzy-Matching, Confidence Scoring)
- ✅ Veranstalter-CRM entwickelt (20 Spalten, One-Click-Actions)
- ✅ Admin-Interface erweitert (Duplikate-Tab, Veranstalter-Karten)

### **Tag 3: Community-Opening**
- ✅ Von "Stadt" zu "Community" (universeller Ansatz)
- ✅ Selbstverständnis definiert (JETZT + HIER, Read-Only First)
- ✅ Use-Cases erweitert (Städte, Subkulturen, Maker-Spaces, Netzwerke)

### **Tag 4: Namenssuche & Branding**
- ✅ Namensfindung: GetVibe → Vibe → Nowish → **Krawl**
- ✅ Domain: **krawl.ist** (mit Wortspiel: "ist" = krass + sein)
- ✅ Community-Identität: **Krawlist**
- ✅ Tagline: **"Krawall hier. Krawall jetzt."**
- ✅ CI/CD-Konzept (schwarz/neon, DIY-Ästhetik, Punk-Vibe)

### **Tag 4: Federation-Vision**
- ✅ Dezentrales Netzwerk: `krawl.ist/[community]`
- ✅ Exit-Strategie: Jeder Fork kann jederzeit aussteigen
- ✅ Branch `feature/federation` für v2.0
- ✅ Cloudflare + GitHub Pages Architektur

---

## 💬 Wichtige Erkenntnisse & Entscheidungen

### **1. Warum "Krawl"?**

**Triple-Bedeutung:**
- **Krawall** (jiddisch) → Aufruhr, Party, was los ist
- **Crawl** (englisch) → Pub Crawl, Event-Tour
- **Krawl** (Kunstwort) → Unique, DIY-Vibe

**Jiddisch/Kauderwelsch als Inspiration:**
> "Mir gefallen die Wörter häufig, sie haben Humor, sind frech und eben subkultig"

### **2. Warum "krawl.ist"?**

**Wortspiel mit "ist":**
- "ist" = krass/extrem (Jugendsprache)
- "ist" = sein (deutsch)
- **Mantra:** "Krawl ist [DEINE COMMUNITY]!"

**Psychologischer Impact:**
> "Es ist ein Mantra, ein Kampfspruch. Es sagt insgeheim: mag ich auch in der tiefsten Provinz oder in der abgefucktesten Subkultur beheimatet sein: wir machen das Beste daraus und zeigen es euch allen."

### **3. Warum `/stuttgart` statt `stuttgart.krawl.ist`?**

**URL als Statement:**
- `krawl.ist/stuttgart` = "Krawl ist Stuttgart!" ✅
- `stuttgart.krawl.ist` = "Stuttgart Krawl ist" ❌ (unlogisch)

**Lösung: Cloudflare Proxy**
- URL bleibt `/stuttgart` (optisch perfekt)
- Fork bleibt autonom (eigenes GitHub-Repo)

### **4. Warum Read-Only First?**

**Bewusste Entscheidung:**
> "Community wird auf unserer 'Karte' ja gar nicht geboten. Es gibt keine Interaktion zwischen den Nutzern. Aber vielleicht ist es auch gerade ein guter Punkt, die größte Schwäche zu bewerben."

**Vision:**
- v1.0: Beobachten (Read-Only)
- v2.0: Mitmachen (Community-Features)
- **Aber:** Kernfunktion bleibt fokussiert

### **5. Exit-Strategie als Prinzip**

**Dezentralität ernst nehmen:**
> "Sollte sich die Cloudflare-Policy ändern oder die von Github, sollte ein Fork unzufrieden sein mit mir, mit Github, mit Cloudflare: kann der Fork seine Daten sichern und selbst hosten?"

**Antwort: JA!**
- Jeder Fork = eigenes Repo
- Umzug zu eigener Domain: 5 Minuten
- Keine Vendor-Lock-in

---

## 🔥 Schlüsselmomente

### **"Nowish" → "NO WISH" Problem**
> "es gibt aber auch mit nowish.irgendwas ein triftiges Problem: kann auch gelesen werden als NO WISH. ist das eine nette Nebenbedeutung oder genau das Gegenteil unseres Versprechens und somit entlarvend?"

→ Führte zur finalen Lösung: **Krawl**

### **"Glitsche" als fränkischer Dialekt**
> "In meinem fränkischen Dialekt bezeichnet man zwilichtige, verwahrloste Kneipen als Glitschen [...] das hat für mich einen besonderen Reiz, für einige Subkulturen bestimmt auch."

→ Authentisch, aber zu regional + Location-Fokus statt Event-Fokus

### **"Krawlist" als Identität**
> "wer das nutzt ist ein Krawlist"

→ Community-Member-Identität geschaffen (wie "Hacker", "Punk", "Maker")

### **"Krawall hier. Krawall jetzt." als Tagline**
> "Krawall hier. Krawall jetzt."  
> User: "YES!"

→ Minimalistisch, direkt, Punk - perfekter Vibe

---

## 📊 Technischer Fortschritt

### **Von:**
- Städtischer Event-Kalender (nur Hof)
- Manuelle Event-Eingabe
- Keine Duplikat-Erkennung
- Keine Community-Features

### **Zu:**
- Universelles Community-Tool
- Automatisches Scraping (GitHub Actions)
- Intelligente Deduplication (Fuzzy-Matching)
- Veranstalter-CRM (Networking, One-Click-Actions)
- Parametrisiert (_config.yml)
- Forkbar (INSTALL.md)
- Federation-Ready (feature/federation Branch)

### **Zeitersparnis:**
> "binnen dreier(?) Tage haben wir erreicht, wofür ich alleine ein Jahr und im Team bestimmt drei Monate gebraucht hätte."

---

## 🎨 Design-Philosophie

### **CI/CD:**
- **Farbpalette:** Schwarz/Neon (Underground-Vibe)
- **Typografie:** Grotesk, fett (Inter, Helvetica)
- **Imagery:** Flyer-Ästhetik, DIY, Punk-Zines
- **Tone of Voice:** Frech, authentisch, kein Marketing-Blabla

### **Beispiele:**
- ✅ "Werde Krawlist"
- ✅ "Wo ist der Krawall?"
- ✅ "Events, kein Lärm"
- ❌ "Entdecke deine nächste unvergessliche Erfahrung"

---

## 🚀 Roadmap

### **v1.0 (jetzt): Read-Only Event-Aggregation**
- ✅ Automatisches Scraping
- ✅ Deduplication-Engine
- ✅ Veranstalter-CRM
- ✅ GPS-Umkreissuche
- ✅ Bookmark-System

### **v1.5 (geplant): Community-Input**
- 🔜 Event-Vorschläge (ohne Account)
- 🔜 "Ich bin dabei"-Counter
- 🔜 Upvotes
- 🔜 iCal/CalDAV Export

### **v2.0 (Vision): Krawl Network**
- 💡 Federation: `krawl.ist/[community]`
- 💡 Landing Page mit Registry
- 💡 Cloudflare + GitHub Pages
- 💡 Dezentral, autonom, exit-ready

---

## 🙏 Credits

**Entwickelt für:** Krawlisten in Hof an der Saale - und alle anderen Communities (Städte, Subkulturen, Netzwerke), die folgen.

**Inspiriert von:**
- Jiddische/Kauderwelsch-Wörter (Krawall, Glitschen, Mischpoke)
- DIY/Punk-Kultur (authentisch, nicht poliert)
- Dezentrale Bewegungen (Exit-Strategie, Autonomie)

**Built with:**
- Jekyll 3.10 (Static Site Generator)
- Python 3.11+ (Scraping, Deduplication)
- Leaflet.js 1.9.4 (Interactive Maps)
- GitHub Pages (Hosting)
- Cloudflare Pages (Federation, v2.0)

---

## 📝 Zitate aus der Session

> "Das schlank bleiben soll nicht so prominent stehen"

> "DIY in cool muss präsent sein im Namen"

> "Bitte betrachte meine Vorschläge kritischer"

> "Krawall hier. Krawall jetzt." — "YES!"

> "Für Krawlisten, von Krawlisten."

---

## 🎯 Vision

**Krawl ist mehr als ein Tool - es ist eine Bewegung:**

- Dezentral (keine zentrale Plattform)
- Autonom (jeder Fork hat volle Kontrolle)
- Fokussiert (Events finden, nicht suchen)
- Authentisch (DIY-Vibe, keine Corporate-Sprache)
- Inklusiv (Städte, Subkulturen, Netzwerke, Nischen)

**Krawall hier. Krawall jetzt. Krawall überall.**

---

**Made with ❤️ in November 2025**

*Eine Zusammenarbeit, die zeigt, was möglich ist, wenn Mensch und KI gemeinsam an einer Vision arbeiten.*

---

## 📦 Archiv-Metadaten

- **Projekt:** Krawl (ehemals "Event-Kalender Hof")
- **Repository:** feileberlin/event-kalender-hof
- **Domain:** krawl.ist (geplant)
- **Zeitraum:** 17.-20. November 2025
- **Status:** v1.0 fertig, v2.0 (Federation) in Planung
- **Dokumentation:** README.md, INSTALL.md, FEDERATION.md, DOMAIN_SETUP.md

---

*"Historisch im Sinne von gänzlich neuer Erfahrung."*
