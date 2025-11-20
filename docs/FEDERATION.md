# Krawl Federation (v2.0)

**Vision:** Ein Netzwerk von autonomen Krawl-Instanzen unter einer Domain: `krawl.ist`

---

## 🎯 Ziel

**Mantra:** "Krawl ist [DEINE COMMUNITY]!"

- `krawl.ist/hof` → "Krawl ist Hof!"
- `krawl.ist/stuttgart` → "Krawl ist Stuttgart!"
- `krawl.ist/punk-berlin` → "Krawl ist Punk Berlin!"

**Psychologischer Impact:**
- Statement: "Der Krawall IST hier!"
- Zugehörigkeit: Teil einer Bewegung
- Power: Nicht "Community hat Events", sondern "KRAWALL IST COMMUNITY"

---

## 🏗️ Architektur

### **Dezentral + Autonom:**

```
krawl.ist (Cloudflare Pages)
    ↓ Proxy
    ├── /hof → hof.krawl.ist (GitHub Pages)
    ├── /stuttgart → stuttgart.krawl.ist (GitHub Pages)
    └── /heidelberg → heidelberg.krawl.ist (GitHub Pages)
```

**Jeder Fork:**
- Eigenes GitHub-Repo (`username/krawl-stuttgart`)
- Eigene GitHub Actions (Scraping, Archivierung)
- Eigene Daten (vollständige Kontrolle)
- Eigene Subdomain (`stuttgart.krawl.ist`)

**Cloudflare:**
- Hostet nur Landing Page (`krawl.ist/`)
- Proxied Requests zu Subdomains
- **URL bleibt** `krawl.ist/stuttgart` (kein Redirect!)

---

## ✅ Exit-Strategie (WICHTIG!)

**Jeder Fork kann JEDERZEIT aussteigen:**

### **Warum das funktioniert:**

1. **Alle Daten gehören dem Fork-Owner**
   - Repo: `username/krawl-stuttgart`
   - GitHub Pages: `username.github.io/krawl-stuttgart`
   - → Volle Kontrolle!

2. **Umzug zu eigener Domain (5 Minuten):**
   ```bash
   # 1. CNAME-Datei ändern
   echo "stuttgart-events.de" > CNAME
   
   # 2. DNS konfigurieren
   # stuttgart-events.de → GitHub Pages IPs
   
   # 3. Fertig! Fork läuft unter eigener Domain
   ```

3. **Was bei Exit passiert:**
   - Fork läuft weiter unter neuer Domain
   - Cloudflare-Regel wird gelöscht (`/stuttgart` → 404)
   - Kein Datenverlust, keine Abhängigkeit

**→ Volle Autonomie! Keine Vendor-Lock-in!** ✅

---

## 🛠️ Technische Umsetzung

### **1. Landing Page (Cloudflare Pages)**

**Repo-Struktur:**
```
krawl-network/
├── index.html          # Landing Page mit Registry
├── _registry.json      # Liste aller Forks
├── _redirects          # Cloudflare Proxy Rules
└── assets/
    ├── css/
    └── js/
```

**`_registry.json`:**
```json
{
  "instances": [
    {
      "slug": "hof",
      "name": "Hof an der Saale",
      "subdomain": "hof.krawl.ist",
      "type": "stadt",
      "maintainer": "feileberlin",
      "repo": "feileberlin/event-kalender-hof",
      "status": "active"
    },
    {
      "slug": "stuttgart",
      "name": "Stuttgart",
      "subdomain": "stuttgart.krawl.ist",
      "type": "stadt",
      "maintainer": "username",
      "repo": "username/krawl-stuttgart",
      "status": "active"
    }
  ]
}
```

**`_redirects` (Cloudflare Pages):**
```
/              /index.html                 200
/hof           https://hof.krawl.ist       200!
/stuttgart     https://stuttgart.krawl.ist 200!
/heidelberg    https://heidelberg.krawl.ist 200!
/*             /404.html                   404
```

**Wichtig:** `200!` = Proxy (URL bleibt), nicht `301` (Redirect)

---

### **2. Fork-Workflow**

**Für neue Krawl-Instanz (z.B. Stuttgart):**

#### **Schritt 1: Repo forken**
```bash
gh repo fork feileberlin/event-kalender-hof --clone
cd event-kalender-hof
```

#### **Schritt 2: Anpassen**
```yaml
# _config.yml
title: "krawl.ist/stuttgart"
url: "https://stuttgart.krawl.ist"
baseurl: ""

city:
  name: "Stuttgart"
  name_short: "Stuttgart"
  center:
    lat: 48.7758
    lng: 9.1829
```

#### **Schritt 3: CNAME erstellen**
```bash
echo "stuttgart.krawl.ist" > CNAME
git add CNAME
git commit -m "chore: Set custom domain to stuttgart.krawl.ist"
git push
```

#### **Schritt 4: GitHub Pages aktivieren**
- Repo Settings → Pages
- Custom Domain: `stuttgart.krawl.ist`
- Enforce HTTPS

#### **Schritt 5: Registry-Eintrag (Pull Request)**
```bash
# Im feileberlin/event-kalender-hof Repo
git checkout feature/federation

# _registry.json erweitern
# Pull Request öffnen mit:
# - Registry-Eintrag
# - Cloudflare _redirects Update
```

#### **Schritt 6: Nach Merge → LIVE!**
- Cloudflare deployed automatisch
- Fork ist erreichbar unter `krawl.ist/stuttgart`
- Subdomain `stuttgart.krawl.ist` funktioniert auch

---

### **3. DNS-Konfiguration**

**Bei Domain-Provider (für `krawl.ist`):**

```
# Cloudflare Pages (Landing Page)
Type: CNAME, Name: @, Value: [cloudflare-pages-url]

# GitHub Pages (Forks)
Type: CNAME, Name: *, Value: feileberlin.github.io.
```

**Wildcard ermöglicht:**
- `hof.krawl.ist` → GitHub Pages
- `stuttgart.krawl.ist` → GitHub Pages
- etc.

---

## 🔄 Merge-Strategie: `main` ↔️ `feature/federation`

### **Was in `main` bleibt:**
- Standalone Hof-Instanz
- Core-Features (Scraping, Deduplication, CRM)
- Dokumentation

### **Was in `feature/federation` kommt:**
- Landing Page (`krawl-network/`)
- Registry (`_registry.json`)
- Cloudflare-Integration
- Federation-Dokumentation

### **Merge-Flow:**

**Von `main` → `feature/federation`:**
```bash
git checkout feature/federation
git merge main
# → Neue Features aus main werden in Federation übernommen
```

**Von `feature/federation` → `main`:**
```bash
git checkout main
git merge feature/federation
# → Nur wenn Federation-Features auch standalone sinnvoll sind
```

**Cherry-Pick einzelne Features:**
```bash
git checkout main
git cherry-pick <commit-hash>
# → Spezifische Commits aus federation in main übernehmen
```

---

## 📋 Roadmap

### **Phase 1: Vorbereitung (JETZT)**
- [x] Branch `feature/federation` erstellen
- [ ] Repo-Struktur refactoren:
  - [ ] `krawl-hof/` (Hof-Instanz)
  - [ ] `krawl-core/` (Shared Code)
  - [ ] `krawl-network/` (Federation)
- [ ] Dokumentation schreiben

### **Phase 2: Landing Page (v2.0 Alpha)**
- [ ] `index.html` mit Registry-Liste
- [ ] Karte mit allen Instanzen
- [ ] Design: Krawl-Ästhetik (schwarz/neon)

### **Phase 3: Cloudflare Setup**
- [ ] Cloudflare Pages Account
- [ ] Repo connecten
- [ ] `_redirects` konfigurieren
- [ ] DNS umstellen

### **Phase 4: Beta-Test**
- [ ] Test-Fork erstellen (`krawl.ist/test`)
- [ ] Proxy testen (URL bleibt `/test`)
- [ ] Exit-Strategie testen (Fork zu eigener Domain)

### **Phase 5: Launch v2.0**
- [ ] Merge `feature/federation` → `main`
- [ ] Dokumentation finalisieren
- [ ] Erste externe Forks onboarden

---

## 🎨 Landing Page Design (Mockup)

```
╔═══════════════════════════════════════════╗
║                                           ║
║              🔥 KRAWL.IST                 ║
║                                           ║
║         Krawall hier. Krawall jetzt.      ║
║                                           ║
║  ┌─────────────────────────────────────┐ ║
║  │  Finde deine Community:              │ ║
║  │                                      │ ║
║  │  🏙️ Städte:                          │ ║
║  │  → krawl.ist/hof                     │ ║
║  │  → krawl.ist/stuttgart               │ ║
║  │  → krawl.ist/heidelberg              │ ║
║  │                                      │ ║
║  │  🎸 Subkulturen:                     │ ║
║  │  → krawl.ist/punk-berlin             │ ║
║  │  → krawl.ist/metal-bayern            │ ║
║  │                                      │ ║
║  │  🛠️ Maker & Hacker:                  │ ║
║  │  → krawl.ist/ccc-erfurt              │ ║
║  │                                      │ ║
║  │  [+ Deine Community hinzufügen]      │ ║
║  └─────────────────────────────────────┘ ║
║                                           ║
║  [🗺️ Karte mit allen Krawls]             ║
║                                           ║
║  Für Krawlisten, von Krawlisten.         ║
║  Open Source, kein Bullshit.             ║
║                                           ║
╚═══════════════════════════════════════════╝
```

---

## 🆘 Support & Ressourcen

**Für Fork-Maintainer:**
- [INSTALL.md](INSTALL.md) - Komplette Fork-Anleitung
- [DOMAIN_SETUP.md](DOMAIN_SETUP.md) - DNS & GitHub Pages
- [FEDERATION.md](FEDERATION.md) - Dieses Dokument

**GitHub:**
- Issues: https://github.com/feileberlin/event-kalender-hof/issues
- Discussions: https://github.com/feileberlin/event-kalender-hof/discussions

---

**Made with ❤️ for the Krawl Network**

*Krawall hier. Krawall jetzt. Krawall überall.*
