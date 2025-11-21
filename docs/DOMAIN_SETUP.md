# Domain-Setup: krawl.ist → GitHub Pages

**Ziel:** `krawl.ist` und Subdomains (`hof.krawl.ist`, `*.krawl.ist`) auf GitHub Pages zeigen lassen.

---

## 🎯 Übersicht

- **Haupt-Domain:** `krawl.ist` → zeigt auf `feileberlin.github.io/krawl.ist` (GitHub Repository Slug bleibt aus technischen Gründen)
- **Subdomain-Struktur:** `hof.krawl.ist`, `punk-berlin.krawl.ist` etc. (für Forks)
- **DNS-Provider:** Wo auch immer du `krawl.ist` registrierst

---

## 📋 Schritt-für-Schritt-Anleitung

### **1. Domain registrieren**

Registriere `krawl.ist` bei einem Domain-Registrar:
- **Empfohlen:** Namecheap, Porkbun, Cloudflare Registrar
- **Preis:** ~$20-40/Jahr
- **TLD:** `.ist` (Istanbul/Türkei)

---

### **2. DNS-Einträge konfigurieren**

**Bei deinem DNS-Provider (z.B. Namecheap DNS, Cloudflare DNS):**

#### **A) Haupt-Domain: `krawl.ist` → GitHub Pages**

**Für apex domain (`krawl.ist` ohne `www`):**

Füge **4 A-Records** hinzu, die auf GitHub Pages zeigen:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | `@` | `185.199.108.153` | 3600 |
| A | `@` | `185.199.109.153` | 3600 |
| A | `@` | `185.199.110.153` | 3600 |
| A | `@` | `185.199.111.153` | 3600 |

**Hinweis:** `@` steht für die Root-Domain (`krawl.ist`).

---

#### **B) Subdomain: `hof.krawl.ist` → GitHub Pages**

Füge einen **CNAME-Record** hinzu:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| CNAME | `hof` | `feileberlin.github.io.` | 3600 |

**Wichtig:** Der Punkt `.` am Ende von `feileberlin.github.io.` ist wichtig!

---

#### **C) Wildcard-Subdomain: `*.krawl.ist` (optional, für alle Forks)**

Füge einen **Wildcard-CNAME** hinzu:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| CNAME | `*` | `feileberlin.github.io.` | 3600 |

**Was das macht:** Jede Subdomain (`punk-berlin.krawl.ist`, `bamberg.krawl.ist` etc.) zeigt automatisch auf GitHub Pages.

**Problem:** Du brauchst trotzdem pro Fork ein separates GitHub-Repo mit Custom Domain-Konfiguration!

**Alternative (empfohlen):** Manuelle CNAME-Einträge pro Subdomain (siehe Punkt B).

---

### **3. GitHub Pages konfigurieren**

#### **A) CNAME-Datei erstellen**

Im Root des Repos (`/CNAME`) eine Datei erstellen:

```
krawl.ist
```

**Nur die Domain, keine `https://`, kein Slash!**

**Für Subdomain-Forks:**
```
hof.krawl.ist
```

---

#### **B) Repository Settings**

1. Gehe zu **GitHub Repo → Settings → Pages**
2. **Source:** `Deploy from a branch`
3. **Branch:** `main` / `/ (root)`
4. **Custom domain:** Trage `krawl.ist` ein
5. Warte 5-10 Minuten, bis DNS propagiert ist
6. **Enforce HTTPS:** ✅ aktivieren (sobald SSL-Zertifikat ausgestellt ist)

**Wichtig:** GitHub prüft DNS-Einträge und stellt automatisch Let's Encrypt SSL-Zertifikat aus.

---

### **4. Häufige Probleme & Lösungen**

#### **Problem: "Domain is improperly configured"**

**Ursache:** DNS-Einträge sind falsch oder nicht propagiert.

**Lösung:**
1. Warte 10-60 Minuten (DNS-Propagierung dauert)
2. Prüfe DNS mit `dig krawl.ist` (Terminal):
   ```bash
   dig krawl.ist +short
   ```
   Sollte die 4 GitHub-IPs anzeigen: `185.199.108.153` etc.

3. Prüfe CNAME mit `dig hof.krawl.ist`:
   ```bash
   dig hof.krawl.ist +short
   ```
   Sollte `feileberlin.github.io` anzeigen.

---

#### **Problem: "HTTPS nicht verfügbar"**

**Ursache:** SSL-Zertifikat noch nicht ausgestellt.

**Lösung:**
1. Warte 10-30 Minuten nach DNS-Konfiguration
2. GitHub Pages stellt automatisch Let's Encrypt Zertifikat aus
3. Falls nach 1 Stunde immer noch nicht: Domain aus GitHub Pages entfernen, 5 Minuten warten, neu hinzufügen

---

#### **Problem: "404 auf Subdomain (z.B. hof.krawl.ist)"**

**Ursache:** CNAME-Datei fehlt ODER zeigt auf falsche Domain.

**Lösung:**
1. Im Repo-Root muss `/CNAME` existieren mit Inhalt `hof.krawl.ist`
2. `_config.yml` muss `baseurl: ""` haben (leer!) und `url: "https://hof.krawl.ist"`
3. Neu bauen: `git commit --allow-empty -m "trigger rebuild" && git push`

---

#### **Problem: "CSS/JS laden nicht (404 auf /assets/)"**

**Ursache:** `baseurl` in `_config.yml` falsch gesetzt.

**Lösung:**
- Für Custom Domain (`krawl.ist`): `baseurl: ""`  (LEER!)
- Für GitHub Pages ohne Custom Domain (`feileberlin.github.io/krawl.ist`): `baseurl: "/krawl.ist"`

**Aktuell (`_config.yml`):**
```yaml
baseurl: ""  # Leer für Custom Domain!
url: "https://krawl.ist"
```

---

### **5. Mehrere Domains / Subdomains verwalten**

**Strategie für Forks:**

#### **Option A: Jeder Fork = eigenes Repo + eigene Subdomain**

1. Fork: `https://github.com/username/krawl-bamberg`
2. CNAME-Datei: `bamberg.krawl.ist`
3. DNS: CNAME `bamberg` → `username.github.io.`
4. GitHub Pages: Custom Domain = `bamberg.krawl.ist`

#### **Option B: Alle Forks unter einer Domain mit Path**

**Problem:** GitHub Pages unterstützt kein URL-Rewriting!  
Du kannst nicht `krawl.ist/bamberg` auf `username.github.io/krawl-bamberg` mappen.

**Lösung:** Subdomains nutzen (Option A).

---

### **6. Checkliste (in dieser Reihenfolge!)**

- [ ] Domain `krawl.ist` registriert
- [ ] DNS A-Records für `@` gesetzt (4 IPs)
- [ ] DNS CNAME für `hof` gesetzt → `feileberlin.github.io.`
- [ ] `/CNAME`-Datei im Repo erstellt mit `krawl.ist`
- [ ] `_config.yml`: `baseurl: ""` und `url: "https://krawl.ist"`
- [ ] GitHub Pages Settings: Custom Domain = `krawl.ist`
- [ ] 10-30 Minuten warten (DNS + SSL)
- [ ] `https://krawl.ist` im Browser testen
- [ ] "Enforce HTTPS" in GitHub Pages aktivieren

---

### **7. Testen**

```bash
# DNS-Propagierung prüfen
dig krawl.ist +short
# Sollte anzeigen: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153

dig hof.krawl.ist +short
# Sollte anzeigen: feileberlin.github.io

# HTTP-Test
curl -I https://krawl.ist
# Sollte HTTP 200 zurückgeben

# Browser-Test
open https://krawl.ist  # macOS
xdg-open https://krawl.ist  # Linux
```

---

## 📚 Weitere Ressourcen

- [GitHub Pages Custom Domain Docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [GitHub Pages IP-Adressen](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site#configuring-an-apex-domain)
- [DNS-Checker Tool](https://dnschecker.org/) - Prüfe weltweite DNS-Propagierung

---

## 🆘 Support

Falls Probleme auftreten:
1. Prüfe DNS mit `dig` (siehe oben)
2. Prüfe GitHub Actions Logs (Build-Fehler?)
3. GitHub Issues: https://github.com/feileberlin/krawl.ist/issues

---

**Viel Erfolg mit krawl.ist!** 🚀
