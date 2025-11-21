# 🎨 Theme System - Dokumentation

Zentrales Theme-System für krawl.ist mit austauschbaren, vorkonfigurierten Themes.

## 📁 Struktur

```
assets/themes/
├── default-dark.css    # Standard-Theme (dunkel mit roten Akzenten)
├── light.css           # Heller Modus
├── cyberpunk.css       # Neon & Futuristisch
├── nature.css          # Grüne Erdtöne
└── minimal.css         # Schwarz-Weiß Reduktion
```

## 🔧 Theme aktivieren

### In `_config.yml`:

```yaml
theme:
  active: "cyberpunk"  # Name des Themes (ohne .css)
```

**Verfügbare Themes:**
- `default-dark` - Standard (dunkel, rot)
- `light` - Hell & freundlich
- `cyberpunk` - Neon-Farben, futuristisch
- `nature` - Grün, nachhaltig, organisch
- `minimal` - Schwarz-Weiß, ultra-clean

## 🎨 Eigenes Theme erstellen

### 1. CSS-Datei anlegen

Erstelle `assets/themes/mein-theme.css`:

```css
/* Theme: Mein Theme - Beschreibung */

:root {
    /* Brand Colors */
    --color-primary: #your-color;
    --color-secondary: #your-color;
    --color-accent: #your-color;
    
    /* Background Colors */
    --bg-primary: #your-color;
    --bg-secondary: #your-color;
    --bg-overlay: rgba(0, 0, 0, 0.95);
    --bg-card: #your-color;
    
    /* Text Colors */
    --text-primary: #your-color;
    --text-secondary: #your-color;
    --text-muted: #your-color;
    
    /* UI Colors */
    --border-color: rgba(255, 255, 255, 0.1);
    --shadow-color: rgba(0, 0, 0, 0.3);
    --hover-bg: rgba(255, 255, 255, 0.05);
    
    /* Status Colors */
    --success: #your-color;
    --warning: #your-color;
    --error: #your-color;
    --info: #your-color;
    
    /* Interactive Elements */
    --button-bg: var(--color-primary);
    --button-hover: #your-color;
    --link-color: var(--color-secondary);
    --link-hover: #your-color;
    
    /* Map Specific */
    --map-marker-color: var(--color-primary);
    --map-cluster-color: var(--color-secondary);
    
    /* Typography */
    --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-size-base: 16px;
    --line-height-base: 1.6;
    
    /* Spacing */
    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 16px;
    --spacing-lg: 24px;
    --spacing-xl: 32px;
    
    /* Transitions */
    --transition-fast: 150ms ease;
    --transition-normal: 300ms ease;
    --transition-slow: 500ms ease;
}

/* Theme Specifics */
body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

/* Custom Styles hier */
```

### 2. Theme in Config registrieren

```yaml
theme:
  active: "mein-theme"
  available:
    - name: "mein-theme"
      label: "Mein Theme"
      description: "Beschreibung des Themes"
```

### 3. Commit & Deploy

```bash
git add assets/themes/mein-theme.css _config.yml
git commit -m "Add custom theme: mein-theme"
git push
```

## 🎯 CSS-Variablen Übersicht

### Pflichtfelder (MÜSSEN definiert werden)

| Variable | Zweck | Beispiel |
|----------|-------|----------|
| `--color-primary` | Hauptfarbe (Buttons, Links) | `#ff6b6b` |
| `--bg-primary` | Haupthintergrund | `#1a1a1a` |
| `--text-primary` | Haupttextfarbe | `#ffffff` |
| `--button-bg` | Button-Hintergrund | `var(--color-primary)` |
| `--link-color` | Link-Farbe | `#4ecdc4` |

### Optional (werden von fullscreen.css verwendet)

| Variable | Zweck | Standard |
|----------|-------|----------|
| `--font-family` | Schriftart | System-Font |
| `--transition-normal` | Animationsdauer | `300ms ease` |
| `--spacing-md` | Standard-Abstände | `16px` |
| `--border-color` | Border-Farbe | `rgba(255,255,255,0.1)` |
| `--shadow-color` | Schatten-Farbe | `rgba(0,0,0,0.3)` |

## 🔍 Verwendung in Komponenten

Das Theme-System nutzt CSS-Variablen, die in `fullscreen.css` referenziert werden:

```css
/* fullscreen.css verwendet Theme-Variablen */
.header-content {
    background-color: var(--bg-overlay);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

button {
    background-color: var(--button-bg);
    color: var(--text-primary);
    transition: all var(--transition-normal);
}

button:hover {
    background-color: var(--button-hover);
}
```

## 🎨 Theme-Beispiele

### Dark Mode (Standard)
```yaml
theme:
  active: "default-dark"
```
- Dunkler Hintergrund (#1a1a1a)
- Rote Akzente (#ff6b6b)
- Gute Lesbarkeit

### Light Mode
```yaml
theme:
  active: "light"
```
- Heller Hintergrund (#ffffff)
- Freundlich, zugänglich
- Tageslicht-optimiert

### Cyberpunk
```yaml
theme:
  active: "cyberpunk"
```
- Neon-Farben (Magenta, Cyan)
- Monospace-Font
- Glow-Effekte

### Nature
```yaml
theme:
  active: "nature"
```
- Grüne Erdtöne
- Serif-Font (Georgia)
- Runde Ecken

### Minimal
```yaml
theme:
  active: "minimal"
```
- Schwarz-Weiß
- Kein Shadow
- Scharfe Kanten
- Grayscale-Map

## 🚀 Advanced: Theme-Switcher (optional)

Falls du einen Theme-Switcher im UI möchtest:

```javascript
// assets/js/theme-switcher.js
function switchTheme(themeName) {
    // Entferne altes Theme
    document.querySelectorAll('link[href*="/themes/"]').forEach(link => {
        link.remove();
    });
    
    // Lade neues Theme
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = `/assets/themes/${themeName}.css`;
    document.head.appendChild(link);
    
    // Speichere Präferenz
    localStorage.setItem('theme', themeName);
}

// Theme aus LocalStorage laden (überschreibt config)
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    switchTheme(savedTheme);
}
```

## 📱 Responsive Design

Themes sollten responsive sein:

```css
@media (max-width: 768px) {
    :root {
        --font-size-base: 14px;
        --spacing-md: 12px;
    }
}
```

## 🌓 Dark Mode Support

Auto-Detection für System-Präferenz:

```css
@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary: #1a1a1a;
        --text-primary: #ffffff;
    }
}

@media (prefers-color-scheme: light) {
    :root {
        --bg-primary: #ffffff;
        --text-primary: #2d3436;
    }
}
```

## 🐛 Troubleshooting

### Theme wird nicht geladen

1. **Prüfe Dateinamen:** `_config.yml` muss exakt mit Dateiname übereinstimmen
   ```yaml
   # ✅ Richtig
   theme:
     active: "cyberpunk"  # → assets/themes/cyberpunk.css
   
   # ❌ Falsch
   theme:
     active: "cyberpunk.css"  # .css NICHT angeben!
   ```

2. **Cache leeren:** Browser-Cache kann alte Styles laden
   - `Ctrl+Shift+R` (Hard Reload)
   - Oder: `Ctrl+Shift+Del` → Cache löschen

3. **Build-Fehler:** Jekyll muss neu builden nach Config-Änderung
   ```bash
   bundle exec jekyll clean
   bundle exec jekyll build
   ```

### Farben werden nicht übernommen

1. **CSS-Variablen prüfen:** Alle Pflichtfelder definiert?
2. **Syntax-Check:** Keine Tippfehler in Variable-Namen?
3. **Browser-Support:** IE11 unterstützt keine CSS-Variablen (aber egal 😊)

### Map sieht komisch aus

Manche Themes haben Map-Filter:

```css
/* Grayscale-Map für Minimal-Theme */
.leaflet-tile-pane {
    filter: grayscale(100%);
}

/* Hell für Light-Theme */
.leaflet-tile-pane {
    filter: brightness(1.1);
}
```

## 📚 Best Practices

1. **Variablen statt Hardcoded Colors:**
   ```css
   /* ✅ Gut */
   background-color: var(--bg-primary);
   
   /* ❌ Schlecht */
   background-color: #1a1a1a;
   ```

2. **Konsistente Namenskonvention:**
   - `--color-*` für Markenfarben
   - `--bg-*` für Hintergründe
   - `--text-*` für Textfarben

3. **Accessibility beachten:**
   - Kontrast-Ratio mind. 4.5:1 (WCAG AA)
   - Teste mit: https://webaim.org/resources/contrastchecker/

4. **Mobile-First:** Teste auf verschiedenen Geräten

## 🔗 Links

- [CSS Custom Properties (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)
- [Color Picker Tool](https://coolors.co/)
- [Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Theme Generator](https://mycolor.space/)

## 📄 License

Themes sind Open Source (Teil von krawl.ist) - frei verwendbar für eigene Forks!

---

**Fragen? Issues? → GitHub Discussions!**
