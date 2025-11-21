# 🎨 Theme-System Implementation

## ✅ Was wurde implementiert

### 1. **Zentrale Theme-Verwaltung**
- Alle Themes in `/assets/themes/`
- Konfiguration über `_config.yml`
- Automatisches Laden via Jekyll Template

### 2. **5 Vorkonfigurierte Themes**

| Theme | Beschreibung | Use Case |
|-------|--------------|----------|
| **default-dark** | Dunkel mit roten Akzenten | Standard, Party-Events |
| **light** | Hell & freundlich | Tageslicht, Accessibility |
| **cyberpunk** | Neon-Farben, futuristisch | Tech-Events, Underground |
| **nature** | Grüne Erdtöne, organisch | Nachhaltigkeits-Events, Öko |
| **minimal** | Schwarz-Weiß, ultra-clean | Minimalismus, Professionalität |

### 3. **CSS-Variablen System**
- Alle Farben als `--variable`
- Konsistente Namenskonvention
- Einfach erweiterbar

### 4. **Integration in Layouts**
```html
<!-- In _layouts/map.html und _layouts/base.html -->
<link rel="stylesheet" href="{{ '/assets/themes/' | append: site.theme.active | append: '.css' | relative_url }}">
```

## 🔧 Theme wechseln

### In `_config.yml`:

```yaml
theme:
  active: "cyberpunk"  # Einfach Theme-Namen ändern!
```

### Verfügbare Optionen:
- `default-dark`
- `light`
- `cyberpunk`
- `nature`
- `minimal`

## 📁 Ordnerstruktur

```
krawl.ist/
├── _config.yml                    # Theme-Konfiguration
├── _layouts/
│   ├── base.html                  # Theme-Loading
│   └── map.html                   # Theme-Loading
└── assets/
    ├── css/
    │   └── fullscreen.css         # Nutzt Theme-Variablen
    └── themes/                    # ← NEU: Zentrale Theme-Verwaltung
        ├── README.md              # Vollständige Dokumentation
        ├── default-dark.css       # Standard-Theme
        ├── light.css              # Helles Theme
        ├── cyberpunk.css          # Neon-Theme
        ├── nature.css             # Grünes Theme
        └── minimal.css            # Minimalistisches Theme
```

## 🎨 Eigenes Theme erstellen

### 1. CSS-Datei anlegen

```bash
# Kopiere ein existierendes Theme als Vorlage
cp assets/themes/default-dark.css assets/themes/mein-theme.css
```

### 2. CSS anpassen

```css
/* Theme: Mein Theme */
:root {
    --color-primary: #your-color;
    --bg-primary: #your-bg;
    /* ... weitere Variablen ... */
}
```

### 3. In Config aktivieren

```yaml
# _config.yml
theme:
  active: "mein-theme"
  available:
    - name: "mein-theme"
      label: "Mein Theme"
      description: "Custom Theme"
```

## 🔍 CSS-Variablen Übersicht

### Pflicht-Variablen (in jedem Theme):
```css
:root {
    /* Brand Colors */
    --color-primary: #main-color;
    --color-secondary: #second-color;
    --color-accent: #accent-color;
    
    /* Backgrounds */
    --bg-primary: #main-bg;
    --bg-secondary: #second-bg;
    --bg-overlay: rgba(...);
    --bg-card: #card-bg;
    
    /* Text */
    --text-primary: #main-text;
    --text-secondary: #second-text;
    --text-muted: #muted-text;
    
    /* UI */
    --border-color: rgba(...);
    --shadow-color: rgba(...);
    --hover-bg: rgba(...);
    
    /* Status */
    --success: #green;
    --warning: #orange;
    --error: #red;
    --info: #blue;
    
    /* Interactive */
    --button-bg: var(--color-primary);
    --button-hover: #hover-color;
    --link-color: var(--color-secondary);
    --link-hover: #hover-link;
    
    /* Map */
    --map-marker-color: var(--color-primary);
    --map-cluster-color: var(--color-secondary);
}
```

## 📱 Verwendung in Components

Alle CSS-Komponenten nutzen jetzt Theme-Variablen:

```css
/* In fullscreen.css */
.header-content {
    background-color: var(--bg-overlay);  /* ← Theme-Variable */
    color: var(--text-primary);           /* ← Theme-Variable */
}

button {
    background-color: var(--button-bg);   /* ← Theme-Variable */
    transition: all var(--transition-normal);  /* ← Theme-Variable */
}
```

## 🚀 Deployment

```bash
# 1. Theme wählen in _config.yml
# 2. Commit & Push
git add _config.yml assets/themes/
git commit -m "Switch to cyberpunk theme"
git push

# 3. GitHub Pages baut automatisch neu
# 4. Nach ~2 Minuten ist neues Theme live
```

## 🎯 Migration alter Styles

### Vorher (hardcoded):
```css
.header {
    background-color: #1a1a1a;  /* ← Hardcoded */
    color: #ffffff;             /* ← Hardcoded */
}
```

### Nachher (Theme-System):
```css
.header {
    background-color: var(--bg-primary);  /* ← Theme-Variable */
    color: var(--text-primary);           /* ← Theme-Variable */
}
```

## 🔗 Workflow für Forks

Andere Communities können einfach eigene Themes erstellen:

```bash
# 1. Fork klonen
git clone https://github.com/YOUR-USERNAME/krawl.ist

# 2. Eigenes Theme erstellen
cp assets/themes/default-dark.css assets/themes/my-community.css

# 3. Farben anpassen (z.B. für Stadtfarben)
# Bearbeite my-community.css

# 4. In Config aktivieren
# Bearbeite _config.yml:
#   theme:
#     active: "my-community"

# 5. Commit & Push
git add .
git commit -m "Add custom theme for my community"
git push
```

## 📊 Theme-Eigenschaften

| Theme | Dark/Light | Font | Special Features |
|-------|-----------|------|------------------|
| default-dark | Dark | Sans-serif | Standard, rote Akzente |
| light | Light | Sans-serif | Hoher Kontrast, WCAG AA |
| cyberpunk | Dark | Monospace | Neon-Glow, Text-Shadow |
| nature | Dark | Serif | Runde Ecken, Erdtöne |
| minimal | Light | Sans-serif | No shadows, Sharp edges, Grayscale map |

## 🛠️ Troubleshooting

### Theme wird nicht geladen?

1. **Cache leeren:** `Ctrl+Shift+R` im Browser
2. **Config prüfen:** Theme-Name ohne `.css`
3. **Jekyll neu builden:** `bundle exec jekyll build`

### Farben falsch?

1. **Browser Developer Tools:** `F12` → Computed Styles
2. **CSS-Variablen prüfen:** Sind alle definiert?
3. **Fallback testen:** Hardcode eine Farbe temporär

### Custom Theme funktioniert nicht?

1. **Dateiname = Config-Name?** Exakte Übereinstimmung!
2. **Syntax-Fehler?** CSS-Validator nutzen
3. **Alle Pflicht-Variablen?** Siehe Übersicht oben

## 💡 Best Practices

1. **Immer von vorhandenem Theme kopieren** (nicht von Null anfangen)
2. **Testen auf verschiedenen Geräten** (Mobile, Desktop, Tablet)
3. **Accessibility prüfen** (Kontrast-Ratio, WCAG)
4. **Theme committen** bevor du es aktivierst
5. **Dokumentieren** welche Community welches Theme nutzt

## 🎓 Erweiterte Features (optional)

### Theme-Switcher im UI (für später)

```javascript
// Theme-Switcher Button
function switchTheme(themeName) {
    localStorage.setItem('theme', themeName);
    location.reload();
}

// Theme aus LocalStorage laden
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    // Override config theme
}
```

### Dark Mode Auto-Detection

```css
@media (prefers-color-scheme: dark) {
    /* Auto dark mode */
}

@media (prefers-color-scheme: light) {
    /* Auto light mode */
}
```

## ✅ Next Steps

1. **Theme wählen** in `_config.yml`
2. **Testen** auf localhost: `bundle exec jekyll serve`
3. **Committen** und pushen
4. **Live prüfen** nach GitHub Pages Deployment

---

**Vollständige Dokumentation:** `assets/themes/README.md`

**Beispiel-Themes anschauen:** `assets/themes/*.css`
