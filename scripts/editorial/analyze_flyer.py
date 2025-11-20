#!/usr/bin/env python3
"""
Event Flyer Analyzer - Extrahiert Event-Daten aus Flyern (Bilder/PDFs)

Verwendung:
    python scripts/analyze_flyer.py <URL>
    python scripts/analyze_flyer.py https://example.com/flyer.pdf
    python scripts/analyze_flyer.py https://example.com/flyer.jpg

Benötigt:
    - GITHUB_TOKEN (automatisch in Dev Container verfügbar)
    - pip install requests pillow pypdf2 pytesseract

AI-Provider (in Reihenfolge):
    1. GitHub Models API (GPT-4o-mini via GitHub Token)
    2. DuckDuckGo AI Chat (kostenlos, keine API-Key nötig)
    3. Lokales OCR (Tesseract als Fallback)
"""

import sys
import os
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
import requests
from urllib.parse import urlparse
import base64
import tempfile
import subprocess

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
    PyPDF2 = None


class FlyerAnalyzer:
    def __init__(self):
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.default_coordinates = {
            'lat': 50.3197,
            'lng': 11.9168
        }
        
        # GitHub Models API Endpoint
        self.github_models_endpoint = "https://models.inference.ai.azure.com/chat/completions"
        self.github_model = "gpt-4o-mini"
    
    def download_file(self, url):
        """Lädt Datei von URL herunter"""
        print(f"📥 Downloading: {url}")
        try:
            response = requests.get(url, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0 (Event-Kalender-Hof/1.0)'
            })
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
    
    def extract_text_from_image_ocr(self, image_content):
        """Extrahiert Text aus Bild via Tesseract OCR"""
        print("🔍 Using local OCR (Tesseract)...")
        try:
            # Tesseract verfügbar?
            result = subprocess.run(['which', 'tesseract'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception("Tesseract not installed")
            
            # Bild speichern
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                tmp.write(image_content)
                tmp_path = tmp.name
            
            try:
                # OCR ausführen
                result = subprocess.run(
                    ['tesseract', tmp_path, 'stdout', '-l', 'deu'],
                    capture_output=True, text=True, timeout=30
                )
                
                if result.returncode == 0:
                    return result.stdout.strip()
                else:
                    raise Exception(f"Tesseract failed: {result.stderr}")
            finally:
                os.unlink(tmp_path)
                
        except Exception as e:
            print(f"⚠️  OCR failed: {e}")
            return None
    
    def image_to_base64(self, image_content, max_size=1024):
        """Konvertiert Bild zu Base64"""
        try:
            img = Image.open(io.BytesIO(image_content))
            
            # Resize wenn zu groß
            if img.width > max_size or img.height > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Zu Base64
            buffer = io.BytesIO()
            img_format = 'JPEG' if img.mode == 'RGB' else 'PNG'
            img.save(buffer, format=img_format, quality=85)
            img_bytes = buffer.getvalue()
            
            return base64.b64encode(img_bytes).decode('utf-8')
        except Exception as e:
            raise Exception(f"Image processing failed: {e}")
    
    def analyze_with_github_models(self, text, image_base64=None):
        """Analysiert mit GitHub Models API (GPT-4o-mini)"""
        if not self.github_token:
            print("⚠️  GITHUB_TOKEN not available")
            return None
        
        print("🤖 Analyzing with GitHub Models API (GPT-4o-mini)...")
        
        prompt = """Analysiere diesen Event-Flyer und extrahiere folgende Informationen im JSON-Format:

{
  "title": "Event-Titel",
  "date": "YYYY-MM-DD",
  "start_time": "HH:MM",
  "end_time": "HH:MM oder null",
  "location": "Veranstaltungsort",
  "address": "Vollständige Adresse in Hof, Saale",
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
- Stadt ist Hof (Saale), Deutschland

Antworte NUR mit dem JSON, ohne zusätzlichen Text."""

        try:
            messages = [{"role": "user", "content": prompt}]
            
            if text:
                messages.append({"role": "user", "content": f"Text vom Flyer:\n\n{text}"})
            
            if image_base64:
                messages.append({
                    "role": "user", 
                    "content": f"[Bild als Base64: {image_base64[:50]}...]"
                })
            
            response = requests.post(
                self.github_models_endpoint,
                headers={
                    "Authorization": f"Bearer {self.github_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.github_model,
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 1000
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Extrahiere JSON aus Antwort
                json_match = re.search(r'\{[\s\S]*\}', content)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    print("⚠️  No JSON found in response")
                    return None
            else:
                print(f"⚠️  GitHub Models API error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"⚠️  GitHub Models API failed: {e}")
            return None
    
    def analyze_with_duckduckgo(self, text):
        """Analysiert mit DuckDuckGo AI Chat (kostenlos)"""
        print("🦆 Analyzing with DuckDuckGo AI Chat...")
        
        prompt = f"""Analysiere diesen Event-Flyer und extrahiere Informationen im JSON-Format.

Text vom Flyer:
{text}

Extrahiere:
{{
  "title": "Event-Titel",
  "date": "YYYY-MM-DD",
  "start_time": "HH:MM",
  "end_time": "HH:MM oder null",
  "location": "Veranstaltungsort",
  "address": "Vollständige Adresse",
  "category": "Musik|Theater|Sport|Kultur|Markt|Fest|Sonstiges",
  "description": "Kurzbeschreibung",
  "tags": ["Tag1", "Tag2"],
  "url": "URL oder null",
  "price": "Preis oder null"
}}

Antworte NUR mit JSON."""

        try:
            # DuckDuckGo Chat API (kostenlos, kein API-Key)
            response = requests.post(
                "https://duckduckgo.com/duckchat/v1/chat",
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0"
                },
                json={
                    "model": "gpt-3.5-turbo-0125",
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('message', '')
                
                # Extrahiere JSON
                json_match = re.search(r'\{[\s\S]*\}', content)
                if json_match:
                    return json.loads(json_match.group())
            
            print(f"⚠️  DuckDuckGo AI failed: {response.status_code}")
            return None
            
        except Exception as e:
            print(f"⚠️  DuckDuckGo AI failed: {e}")
            return None
    
    def analyze_with_fallback(self, text):
        """Fallback: Einfache Regex-Extraktion"""
        print("📝 Using fallback extraction (regex patterns)...")
        
        data = {
            "title": None,
            "date": None,
            "start_time": None,
            "end_time": None,
            "location": None,
            "address": None,
            "category": "Sonstiges",
            "description": text[:200] if text else None,
            "tags": [],
            "url": None,
            "price": None
        }
        
        if not text:
            return data
        
        # Datum finden
        date_patterns = [
            r'(\d{1,2})\.(\d{1,2})\.(\d{4})',
            r'(\d{4})-(\d{1,2})-(\d{1,2})'
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                if '.' in pattern:
                    day, month, year = match.groups()
                    data['date'] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                else:
                    data['date'] = match.group()
                break
        
        # Uhrzeit finden
        time_match = re.search(r'(\d{1,2}):(\d{2})', text)
        if time_match:
            data['start_time'] = f"{time_match.group(1).zfill(2)}:{time_match.group(2)}"
        
        # URL finden
        url_match = re.search(r'https?://[^\s]+', text)
        if url_match:
            data['url'] = url_match.group()
        
        # Preis finden
        price_match = re.search(r'(\d+[,.]?\d*)\s*€', text)
        if price_match:
            data['price'] = price_match.group()
        
        return data
    
    def geocode_address(self, address):
        """Geocodiert Adresse zu Koordinaten"""
        if not address:
            return self.default_coordinates
        
        print(f"🗺️  Geocoding: {address}")
        
        try:
            # Nominatim (OpenStreetMap)
            response = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={
                    'q': f"{address}, Hof, Saale, Deutschland",
                    'format': 'json',
                    'limit': 1
                },
                headers={'User-Agent': 'Event-Kalender-Hof/1.0'},
                timeout=10
            )
            
            if response.status_code == 200:
                results = response.json()
                if results:
                    return {
                        'lat': float(results[0]['lat']),
                        'lng': float(results[0]['lon'])
                    }
        except Exception as e:
            print(f"⚠️  Geocoding failed: {e}")
        
        return self.default_coordinates
    
    def generate_event_file(self, data):
        """Generiert Event Markdown Datei"""
        if not data.get('title'):
            raise Exception("No title extracted - cannot create event")
        
        # Dateiname generieren
        date_str = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        title_slug = re.sub(r'[^a-z0-9]+', '-', data['title'].lower()).strip('-')
        filename = f"{date_str}-{title_slug}.md"
        
        # Pfad
        events_dir = Path(__file__).parent.parent.parent / '_events'
        events_dir.mkdir(exist_ok=True)
        filepath = events_dir / filename
        
        # Koordinaten
        coords = self.geocode_address(data.get('address'))
        
        # Markdown generieren
        frontmatter = {
            'layout': 'event',
            'title': data['title'],
            'date': date_str,
            'start_time': data.get('start_time', '00:00'),
            'end_time': data.get('end_time'),
            'location': data.get('location', 'Hof'),
            'address': data.get('address'),
            'category': data.get('category', 'Sonstiges'),
            'tags': data.get('tags', []),
            'coordinates': coords,
            'url': data.get('url'),
            'price': data.get('price'),
            'status': 'Entwurf'
        }
        
        # YAML schreiben
        content = "---\n"
        for key, value in frontmatter.items():
            if value is None:
                continue
            if isinstance(value, list):
                content += f"{key}:\n"
                for item in value:
                    content += f"  - {item}\n"
            elif isinstance(value, dict):
                content += f"{key}:\n"
                for k, v in value.items():
                    content += f"  {k}: {v}\n"
            else:
                # String escapen
                if isinstance(value, str) and any(c in value for c in ':#[]{}'):
                    value = f'"{value}"'
                content += f"{key}: {value}\n"
        content += "---\n\n"
        
        # Description
        if data.get('description'):
            content += f"{data['description']}\n"
        
        # Datei schreiben
        filepath.write_text(content, encoding='utf-8')
        
        print(f"✅ Event created: {filepath}")
        print(f"📍 Coordinates: {coords['lat']}, {coords['lng']}")
        print(f"⚠️  Status: Entwurf (bitte überprüfen und anpassen)")
        
        return filepath
    
    def analyze(self, url):
        """Hauptfunktion: Analysiert Flyer von URL"""
        # Datei herunterladen
        content = self.download_file(url)
        
        # Dateityp erkennen
        parsed_url = urlparse(url)
        extension = Path(parsed_url.path).suffix.lower()
        
        text = None
        image_base64 = None
        
        if extension == '.pdf':
            print("📄 Processing PDF...")
            text = self.extract_text_from_pdf(content)
            file_type = 'pdf'
        elif extension in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            print("🖼️  Processing Image...")
            image_base64 = self.image_to_base64(content)
            text = self.extract_text_from_image_ocr(content)
            file_type = 'image'
        else:
            raise Exception(f"Unsupported file type: {extension}")
        
        # AI-Analyse (mehrere Provider probieren)
        event_data = None
        
        # 1. Versuch: GitHub Models API
        if self.github_token:
            event_data = self.analyze_with_github_models(text, image_base64)
        
        # 2. Versuch: DuckDuckGo AI
        if not event_data and text:
            event_data = self.analyze_with_duckduckgo(text)
        
        # 3. Versuch: Fallback Regex
        if not event_data:
            event_data = self.analyze_with_fallback(text)
        
        if not event_data or not event_data.get('title'):
            raise Exception("Could not extract event data from flyer")
        
        # Event-Datei generieren
        return self.generate_event_file(event_data)


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/analyze_flyer.py <URL>")
        print("\nExample:")
        print("  python scripts/analyze_flyer.py https://example.com/flyer.jpg")
        sys.exit(1)
    
    url = sys.argv[1]
    
    print("=" * 60)
    print("Event Flyer Analyzer")
    print("=" * 60)
    
    try:
        analyzer = FlyerAnalyzer()
        filepath = analyzer.analyze(url)
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS")
        print("=" * 60)
        print(f"\nEvent file created: {filepath}")
        print("\nNext steps:")
        print("1. Review the generated file")
        print("2. Update status from 'Entwurf' to 'Veröffentlicht'")
        print("3. git add _events/")
        print("4. git commit -m 'Event: <title>'")
        print("5. git push origin main")
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR")
        print("=" * 60)
        print(f"\n{e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
