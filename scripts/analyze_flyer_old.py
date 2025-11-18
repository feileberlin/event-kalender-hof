#!/usr/bin/env python3
"""
Event Flyer Analyzer - Extrahiert Event-Daten aus Flyern (Bilder/PDFs)

Verwendung:
    python scripts/analyze_flyer.py <URL>
    python scripts/analyze_flyer.py https://example.com/flyer.pdf
    python scripts/analyze_flyer.py https://example.com/flyer.jpg

Benötigt:
    - GITHUB_TOKEN (automatisch in Dev Container verfügbar)
    - pip install requests pillow pypdf2 pytesseract duckduckgo-search
    - Optional: tesseract-ocr für bessere Texterkennung

AI-Provider (in Reihenfolge):
    1. GitHub Models API (GPT-4o-mini via GitHub Token)
    2. DuckDuckGo AI (kostenlos, keine API-Key nötig)
    3. Lokales OCR (Tesseract als Fallback)
"""

import sys
import os
import re
import hashlib
import json
from datetime import datetime
from pathlib import Path
import requests
from urllib.parse import urlparse
import base64

try:
    from PIL import Image
    import io
except ImportError:
    print("❌ Error: 'pillow' package not installed")
    print("Install: pip install pillow")
    sys.exit(1)

try:
    import PyPDF2
except ImportError:
    print("⚠️  Warning: 'PyPDF2' not installed - PDF support disabled")
    print("Install: pip install pypdf2")
    PyPDF2 = None


class FlyerAnalyzer:
    def __init__(self):
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.github_models_endpoint = "https://models.inference.ai.azure.com/chat/completions"
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=self.api_key)
        self.default_coordinates = {
            'lat': 50.3197,
            'lng': 11.9168
        }
    
    def download_file(self, url):
        """Lädt Datei von URL herunter"""
        print(f"📥 Downloading: {url}")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.content
        except Exception as e:
            raise Exception(f"Download failed: {e}")
    
    def extract_text_from_pdf(self, pdf_content):
        """Extrahiert Text aus PDF"""
        if not PyPDF2:
            raise Exception("PyPDF2 not installed - cannot process PDF")
        
        try:
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"PDF extraction failed: {e}")
    
    def image_to_base64(self, image_content):
        """Konvertiert Bild zu Base64 für Vision API"""
        try:
            # Bild optimieren (max 2000px)
            img = Image.open(io.BytesIO(image_content))
            
            # Resize wenn zu groß
            max_size = 2000
            if img.width > max_size or img.height > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Zu Base64
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            img_bytes = buffer.getvalue()
            
            return base64.b64encode(img_bytes).decode('utf-8')
        except Exception as e:
            raise Exception(f"Image processing failed: {e}")
    
    def analyze_with_ai(self, content, file_type):
        """Analysiert Flyer mit OpenAI Vision/GPT"""
        print("🤖 Analyzing with AI...")
        
        prompt = """Analysiere diesen Event-Flyer und extrahiere folgende Informationen im JSON-Format:

{
  "title": "Event-Titel",
  "date": "YYYY-MM-DD",
  "start_time": "HH:MM",
  "end_time": "HH:MM oder null",
  "location": "Veranstaltungsort",
  "address": "Vollständige Adresse",
  "category": "Musik|Theater|Sport|Kultur|Markt|Fest|Sonstiges",
  "description": "Kurzbeschreibung (2-3 Sätze)",
  "tags": ["Tag1", "Tag2"],
  "url": "Event-URL oder null",
  "price": "Eintrittspreis oder null"
}

Wichtig:
- Datum im Format YYYY-MM-DD
- Zeiten im Format HH:MM (24h)
- Kategorie aus der Liste wählen
- Tags: relevante Schlagwörter
- description: prägnant und informativ
- Wenn Info fehlt: null

Antworte NUR mit dem JSON, ohne zusätzlichen Text."""

        try:
            if file_type == 'image':
                # Vision API für Bilder
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{content}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=1000,
                    temperature=0.3
                )
            else:
                # GPT-4 für Text/PDF
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Du bist ein Experte für Event-Daten-Extraktion."},
                        {"role": "user", "content": f"{prompt}\n\nFlyer-Text:\n{content}"}
                    ],
                    max_tokens=1000,
                    temperature=0.3
                )
            
            result = response.choices[0].message.content.strip()
            
            # JSON extrahieren (falls Markdown Code-Block)
            if '```json' in result:
                result = result.split('```json')[1].split('```')[0].strip()
            elif '```' in result:
                result = result.split('```')[1].split('```')[0].strip()
            
            import json
            event_data = json.loads(result)
            return event_data
            
        except Exception as e:
            raise Exception(f"AI analysis failed: {e}")
    
    def create_event_file(self, event_data, source_url):
        """Erstellt Event Markdown File"""
        print("📝 Creating event file...")
        
        # Dateiname generieren
        date = event_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        title_slug = re.sub(r'[^a-z0-9]+', '-', event_data.get('title', 'event').lower())
        filename = f"{date}-{title_slug}.md"
        filepath = Path('_events') / filename
        
        # Prüfe ob Datei existiert
        if filepath.exists():
            counter = 1
            while True:
                filename = f"{date}-{title_slug}-{counter}.md"
                filepath = Path('_events') / filename
                if not filepath.exists():
                    break
                counter += 1
        
        # YAML Front Matter
        yaml_content = f"""---
title: "{event_data.get('title', 'Unbekanntes Event')}"
date: {event_data.get('date', datetime.now().strftime('%Y-%m-%d'))}
start_time: "{event_data.get('start_time', '20:00')}"
"""
        
        if event_data.get('end_time'):
            yaml_content += f'end_time: "{event_data["end_time"]}"\n'
        
        yaml_content += f"""location: "{event_data.get('location', 'Hof an der Saale')}"
"""
        
        if event_data.get('address'):
            yaml_content += f'address: "{event_data["address"]}"\n'
        
        yaml_content += f"""coordinates:
  lat: {self.default_coordinates['lat']}
  lng: {self.default_coordinates['lng']}
category: "{event_data.get('category', 'Sonstiges')}"
"""
        
        if event_data.get('tags'):
            yaml_content += "tags:\n"
            for tag in event_data['tags']:
                yaml_content += f"  - {tag}\n"
        
        yaml_content += f"""description: "{event_data.get('description', '')}"
"""
        
        if event_data.get('url'):
            yaml_content += f'url: "{event_data["url"]}"\n'
        
        if event_data.get('price'):
            yaml_content += f'price: "{event_data["price"]}"\n'
        
        # Hash generieren
        hash_string = f"{event_data.get('title', '')}{date}{event_data.get('start_time', '')}{event_data.get('location', '')}"
        event_hash = hashlib.md5(hash_string.encode()).hexdigest()
        
        yaml_content += f"""status: "Entwurf"
source: "AI-Flyer-Analyse"
source_url: "{source_url}"
event_hash: "{event_hash}"
---

## Über das Event

{event_data.get('description', 'Keine Beschreibung verfügbar.')}

"""
        
        if event_data.get('price'):
            yaml_content += f"\n### Eintritt\n\n{event_data['price']}\n"
        
        yaml_content += f"""
---

*Automatisch erstellt aus Flyer-Analyse. Bitte Daten prüfen und bei Bedarf korrigieren.*

*Quelle: {source_url}*
"""
        
        # Datei schreiben
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        
        return filepath
    
    def analyze_flyer(self, url):
        """Haupt-Funktion: Analysiert Flyer von URL"""
        print(f"\n{'='*60}")
        print("🎨 Event Flyer Analyzer")
        print(f"{'='*60}\n")
        
        # Dateitype ermitteln
        parsed = urlparse(url)
        path_lower = parsed.path.lower()
        
        if path_lower.endswith('.pdf'):
            file_type = 'pdf'
        elif any(path_lower.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
            file_type = 'image'
        else:
            # Versuche von Content-Type zu ermitteln
            try:
                head = requests.head(url, timeout=10)
                content_type = head.headers.get('Content-Type', '').lower()
                if 'pdf' in content_type:
                    file_type = 'pdf'
                elif 'image' in content_type:
                    file_type = 'image'
                else:
                    raise Exception(f"Unsupported file type: {content_type}")
            except:
                raise Exception("Could not determine file type. Use .pdf, .jpg, .png extension.")
        
        print(f"📄 File type: {file_type.upper()}")
        
        # Datei herunterladen
        content = self.download_file(url)
        print(f"✅ Downloaded {len(content)} bytes")
        
        # Verarbeiten je nach Typ
        if file_type == 'pdf':
            text = self.extract_text_from_pdf(content)
            print(f"✅ Extracted {len(text)} characters from PDF")
            processed_content = text
        else:  # image
            base64_image = self.image_to_base64(content)
            print(f"✅ Processed image ({len(base64_image)} chars base64)")
            processed_content = base64_image
        
        # Mit AI analysieren
        event_data = self.analyze_with_ai(processed_content, file_type)
        print(f"✅ Extracted event data")
        
        # Event File erstellen
        filepath = self.create_event_file(event_data, url)
        
        print(f"\n{'='*60}")
        print(f"✅ SUCCESS! Event created:")
        print(f"{'='*60}")
        print(f"📁 File: {filepath}")
        print(f"📅 Event: {event_data.get('title')}")
        print(f"📍 Ort: {event_data.get('location')}")
        print(f"🗓️  Datum: {event_data.get('date')} {event_data.get('start_time')}")
        print(f"🏷️  Kategorie: {event_data.get('category')}")
        print(f"📝 Status: Entwurf")
        print(f"\n💡 Next steps:")
        print(f"   1. Öffne: {filepath}")
        print(f"   2. Prüfe Daten (Datum, Uhrzeit, Koordinaten)")
        print(f"   3. Ändere Status: 'Entwurf' → 'Öffentlich'")
        print(f"   4. Commit & Push")
        print(f"{'='*60}\n")
        
        return filepath


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/analyze_flyer.py <URL>")
        print("\nExamples:")
        print("  python scripts/analyze_flyer.py https://example.com/flyer.pdf")
        print("  python scripts/analyze_flyer.py https://example.com/poster.jpg")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Validiere URL
    if not url.startswith(('http://', 'https://')):
        print("❌ Error: URL must start with http:// or https://")
        sys.exit(1)
    
    try:
        analyzer = FlyerAnalyzer()
        analyzer.analyze_flyer(url)
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nSetup:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
