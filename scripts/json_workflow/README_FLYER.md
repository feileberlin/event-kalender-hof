# 📸 Flyer Analyzer - Event Data Extraction from Images

OCR-basiertes Tool zum Extrahieren strukturierter Event-Daten aus Veranstaltungs-Flyern (Bilder).

## 🎯 Use Case

Oftmals werden bei Facebook, Instagram & Co. Veranstaltungen als **Bild-Flyer** gepostet statt strukturiert als Text. Dieses Tool extrahiert automatisch:

- 📝 **Titel** der Veranstaltung
- 📅 **Datum** und **Uhrzeit**
- 📍 **Veranstaltungsort**
- 💰 **Eintritt/Preis**
- 📄 **Beschreibung**

## 🔧 Installation

### Minimal (Tesseract OCR)

```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-deu
pip install pytesseract pillow requests beautifulsoup4

# macOS
brew install tesseract tesseract-lang
pip install pytesseract pillow requests beautifulsoup4
```

### Empfohlen (EasyOCR - bessere Genauigkeit)

```bash
pip install easyocr requests beautifulsoup4
```

**Hinweis:** Erster Start lädt ML-Modelle (~50MB)

### Optional (Ollama für LLM-basierte Extraktion)

```bash
# Ollama installieren
curl https://ollama.ai/install.sh | sh

# Vision Model laden
ollama pull llava

# Nutzen
python flyer_analyzer.py image.jpg --engine ollama
```

## 📖 Usage

### Kommandozeile

```bash
# URL analysieren (z.B. Facebook-Bild)
python scripts/json_workflow/flyer_analyzer.py "https://example.com/flyer.jpg"

# Lokale Datei
python scripts/json_workflow/flyer_analyzer.py /path/to/flyer.png

# Interaktiver Review-Modus
python scripts/json_workflow/flyer_analyzer.py image.jpg -i

# JSON-Output
python scripts/json_workflow/flyer_analyzer.py image.jpg --json

# Spezifische OCR-Engine
python scripts/json_workflow/flyer_analyzer.py image.jpg --engine easyocr
```

### Python API

```python
from flyer_analyzer import FlyerAnalyzer

analyzer = FlyerAnalyzer(ocr_engine='auto')

# Von URL
result = analyzer.analyze_from_url('https://example.com/event-flyer.jpg')

# Von Datei
result = analyzer.analyze_from_file('local-flyer.png')

# Ausgabe
print(result['raw_text'])  # Vollständiger OCR-Text
print(result['structured'])  # Strukturierte Daten (Dict)
```

### Integration in Scraper V2

```python
# In scraper_v2.py erweitern:

from flyer_analyzer import FlyerAnalyzer

class ScraperV2:
    def __init__(self):
        # ...existing code...
        self.flyer_analyzer = FlyerAnalyzer()
    
    def scrape_from_social_media_image(self, image_url: str, organizer_slug: str):
        """Scrape event from image flyer (Facebook, Instagram, etc.)"""
        result = self.flyer_analyzer.analyze_from_url(image_url)
        
        if 'structured' in result:
            data = result['structured']
            
            # Create event from extracted data
            event = self._parse_event(
                title=data.get('title', 'Unknown Event'),
                date_str=f"{data.get('date')} {data.get('time', '')}",
                place_slug=self._match_place_from_text(data.get('location', '')),
                organizer_slug=organizer_slug,
                source_url=image_url,
                description=data.get('description'),
                price=data.get('price'),
                image_url=image_url
            )
            
            if event:
                event.meta.confidence = 0.6  # Lower for image-extracted
                event.meta.raw_data = {"ocr_result": result}
                self.scraped_events.append(event)
```

## 🎨 Output-Beispiel

### JSON-Output

```json
{
  "raw_text": "JAZZ NIGHT\n25.12.2025 um 20:00 Uhr\nFreiheitshalle Hof\nEintritt: 15€",
  "structured": {
    "title": "JAZZ NIGHT",
    "date": "25.12.2025",
    "time": "20:00",
    "location": "Freiheitshalle Hof",
    "price": "15€",
    "description": null
  },
  "engine": "easyocr",
  "confidence": 0.92
}
```

### Interaktiver Modus

```
================================================================================
📸 Flyer Analysis Review
================================================================================

🖼️  Image: event-flyer.jpg
🔧 Engine: easyocr

--------------------------------------------------------------------------------
RAW TEXT EXTRACTED:
--------------------------------------------------------------------------------
JAZZ NIGHT
25. Dezember 2025
20:00 Uhr
Freiheitshalle Hof
Mit der Jazz Band "Blue Notes"
Eintritt: 15€

--------------------------------------------------------------------------------
STRUCTURED DATA:
--------------------------------------------------------------------------------
  ✓ title          : JAZZ NIGHT
  ✓ date           : 25.12.2025
  ✓ time           : 20:00
  ✓ location       : Freiheitshalle Hof
  ✓ price          : 15€
  ✗ description    : None

================================================================================
Interactive Review:
  [e] Edit extracted data
  [s] Save as event JSON
  [c] Copy raw text to clipboard
  [q] Quit
================================================================================

Choice:
```

## 🔍 OCR Engines Vergleich

| Engine      | Geschwindigkeit | Genauigkeit | Deutsch-Support | Installation |
|-------------|----------------|-------------|-----------------|--------------|
| Tesseract   | ⚡⚡⚡           | ⭐⭐          | ✅ Gut          | Einfach      |
| EasyOCR     | ⚡⚡            | ⭐⭐⭐⭐       | ✅ Sehr gut     | Mittel       |
| Ollama LLaVA| ⚡             | ⭐⭐⭐⭐⭐      | ✅ Exzellent    | Komplex      |

**Empfehlung:** EasyOCR für Production, Ollama für experimentelle Nutzung

## 🐛 Bekannte Einschränkungen

- **Handschrift:** Wird nicht erkannt (nur gedruckter Text)
- **Stark designte Flyer:** Schwierig bei Text-in-Kurven oder extremen Fonts
- **Niedrige Auflösung:** Bilder sollten mindestens 800x600px haben
- **Mehrsprachig:** Optimiert für Deutsch, funktioniert aber auch für Englisch

## 💡 Tipps für bessere Ergebnisse

1. **Hohe Auflösung:** Je größer das Bild, desto besser die OCR-Genauigkeit
2. **Guter Kontrast:** Schwarzer Text auf hellem Hintergrund funktioniert am besten
3. **Gerade Ausrichtung:** Schräge Bilder rotieren vorher
4. **Review immer manuell:** OCR ist nie 100% perfekt - nutze `-i` Modus

## 🔗 Integration mit krawl.ist Workflow

```bash
# 1. Flyer analysieren
python scripts/json_workflow/flyer_analyzer.py "https://facebook.com/photo.jpg" -i

# 2. Daten editieren im Interactive Mode
#    [e] drücken und Felder korrigieren

# 3. Als Event speichern
#    [s] drücken → erstellt flyer-event-TIMESTAMP.json

# 4. In Staging verschieben
mv flyer-event-*.json _data/staging/

# 5. Review mit Standard-Workflow
python scripts/json_workflow/reviewer.py
python scripts/json_workflow/merger.py
```

## 📚 Dependencies

```
# requirements.txt
pytesseract>=0.3.10  # Tesseract wrapper
Pillow>=10.0.0       # Image processing
easyocr>=1.7.0       # OCR engine (optional)
requests>=2.31.0     # HTTP client
beautifulsoup4>=4.12.0  # HTML parsing
```

## 🆘 Troubleshooting

### "No OCR engine available"

```bash
# Installiere mindestens eins:
pip install pytesseract pillow  # Tesseract
# oder
pip install easyocr  # EasyOCR
```

### "Tesseract not found"

```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Windows
# Download: https://github.com/UB-Mannheim/tesseract/wiki
```

### Schlechte Erkennung

1. Versuche andere Engine: `--engine easyocr`
2. Erhöhe Bildqualität
3. Pre-process Bild (Kontrast erhöhen, Drehen)
4. Nutze Ollama für "intelligentere" Extraktion

## 📄 License

Teil von krawl.ist - Open Source Event-Platform für Hof an der Saale

---

**Feedback & Contributions:** GitHub Issues willkommen!
