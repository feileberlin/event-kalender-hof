#!/usr/bin/env python3
"""
Flyer Analyzer - Extract event data from image flyers
Uses OCR + optional LLM for structured data extraction
"""

import sys
import json
import requests
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import subprocess
import tempfile
import re

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.schemas import Event, EventMeta

# Try importing OCR libraries (graceful degradation)
try:
    import pytesseract
    from PIL import Image
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False

try:
    import easyocr
    HAS_EASYOCR = True
except ImportError:
    HAS_EASYOCR = False


class FlyerAnalyzer:
    """Analyze event flyers and extract structured data"""
    
    def __init__(self, ocr_engine='auto'):
        """
        Args:
            ocr_engine: 'tesseract', 'easyocr', 'auto', or 'ollama'
        """
        self.ocr_engine = ocr_engine
        self.reader = None
        
        if ocr_engine == 'auto':
            if HAS_EASYOCR:
                self.ocr_engine = 'easyocr'
                print("🔧 Using EasyOCR engine")
                self.reader = easyocr.Reader(['de', 'en'])
            elif HAS_TESSERACT:
                self.ocr_engine = 'tesseract'
                print("🔧 Using Tesseract OCR engine")
            else:
                print("⚠️  No OCR engine available!")
                print("   Install: pip install pytesseract pillow")
                print("   Or: pip install easyocr")
    
    def analyze_from_url(self, image_url: str) -> Dict:
        """Download and analyze flyer from URL"""
        print(f"📥 Downloading: {image_url[:80]}...")
        
        try:
            response = requests.get(image_url, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; krawl.ist/2.0)'
            })
            response.raise_for_status()
            
            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                tmp.write(response.content)
                tmp_path = tmp.name
            
            result = self.analyze_from_file(tmp_path)
            result['source_url'] = image_url
            
            # Cleanup
            Path(tmp_path).unlink()
            
            return result
            
        except Exception as e:
            return {"error": f"Download failed: {e}"}
    
    def analyze_from_file(self, image_path: str) -> Dict:
        """Analyze flyer from local file"""
        print(f"🔍 Analyzing: {Path(image_path).name}")
        
        if self.ocr_engine == 'tesseract':
            return self._analyze_tesseract(image_path)
        elif self.ocr_engine == 'easyocr':
            return self._analyze_easyocr(image_path)
        elif self.ocr_engine == 'ollama':
            return self._analyze_ollama(image_path)
        else:
            return {"error": "No OCR engine configured"}
    
    def _analyze_tesseract(self, image_path: str) -> Dict:
        """Extract text using Tesseract OCR"""
        try:
            from PIL import Image
            
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img, lang='deu')
            
            return {
                "raw_text": text,
                "structured": self._parse_text_to_event(text),
                "engine": "tesseract"
            }
        except Exception as e:
            return {"error": f"Tesseract failed: {e}"}
    
    def _analyze_easyocr(self, image_path: str) -> Dict:
        """Extract text using EasyOCR"""
        try:
            result = self.reader.readtext(image_path)
            
            # Combine all detected text
            text = "\n".join([item[1] for item in result])
            
            return {
                "raw_text": text,
                "structured": self._parse_text_to_event(text),
                "confidence": sum([item[2] for item in result]) / len(result) if result else 0,
                "engine": "easyocr"
            }
        except Exception as e:
            return {"error": f"EasyOCR failed: {e}"}
    
    def _analyze_ollama(self, image_path: str) -> Dict:
        """Use Ollama multimodal model for structured extraction"""
        try:
            import base64
            
            with open(image_path, 'rb') as f:
                img_data = base64.b64encode(f.read()).decode()
            
            prompt = """Analysiere diesen Veranstaltungsflyer und extrahiere:
- Titel/Name der Veranstaltung
- Datum und Uhrzeit
- Veranstaltungsort/Location
- Beschreibung/Details
- Eintritt/Preis
- Veranstalter

Antworte als JSON."""
            
            # Call Ollama API
            result = subprocess.run([
                'ollama', 'run', 'llava',
                prompt
            ], capture_output=True, text=True, input=img_data, timeout=60)
            
            if result.returncode == 0:
                try:
                    parsed = json.loads(result.stdout)
                    return {
                        "raw_text": result.stdout,
                        "structured": parsed,
                        "engine": "ollama-llava"
                    }
                except json.JSONDecodeError:
                    return {
                        "raw_text": result.stdout,
                        "structured": self._parse_text_to_event(result.stdout),
                        "engine": "ollama-llava"
                    }
            else:
                return {"error": f"Ollama failed: {result.stderr}"}
                
        except Exception as e:
            return {"error": f"Ollama not available: {e}"}
    
    def _parse_text_to_event(self, text: str) -> Dict:
        """Parse raw text into structured event data"""
        structured = {
            "title": None,
            "date": None,
            "time": None,
            "location": None,
            "description": None,
            "price": None
        }
        
        if not text:
            return structured
        
        lines = text.strip().split('\n')
        text_lower = text.lower()
        
        # Extract date patterns
        date_patterns = [
            r'(\d{1,2})\.(\d{1,2})\.(\d{4})',
            r'(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})',
            r'(\d{1,2})\s+(januar|februar|märz|april|mai|juni|juli|august|september|oktober|november|dezember)\s+(\d{4})',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                structured["date"] = match.group(0)
                break
        
        # Extract time
        time_match = re.search(r'(\d{1,2})[:\.](\d{2})\s*(uhr)?', text_lower)
        if time_match:
            structured["time"] = f"{time_match.group(1)}:{time_match.group(2)}"
        
        # Extract price
        price_match = re.search(r'(eintritt|preis)[:\s]*(kostenlos|frei|[\d,]+\s*€)', text_lower)
        if price_match:
            structured["price"] = price_match.group(2)
        
        # Title heuristic: Usually first or largest text
        if lines:
            candidates = [line.strip() for line in lines if len(line.strip()) > 5]
            if candidates:
                structured["title"] = candidates[0]
        
        # Location keywords
        location_keywords = ['hof', 'freiheitshalle', 'theater', 'rathaus', 'altstadt']
        for keyword in location_keywords:
            if keyword in text_lower:
                pattern = rf'(.{{0,30}}{keyword}.{{0,30}})'
                match = re.search(pattern, text_lower)
                if match:
                    structured["location"] = match.group(1).strip()
                    break
        
        return structured
    
    def interactive_review(self, image_path: str, analysis: Dict):
        """Interactive review of extracted data"""
        print("\n" + "=" * 80)
        print("📸 Flyer Analysis Review")
        print("=" * 80)
        print(f"\n🖼️  Image: {image_path}")
        print(f"🔧 Engine: {analysis.get('engine', 'unknown')}")
        
        if 'error' in analysis:
            print(f"\n❌ Error: {analysis['error']}")
            return None
        
        print("\n" + "-" * 80)
        print("RAW TEXT EXTRACTED:")
        print("-" * 80)
        print(analysis.get('raw_text', '')[:500])
        
        if 'structured' in analysis:
            print("\n" + "-" * 80)
            print("STRUCTURED DATA:")
            print("-" * 80)
            for key, value in analysis['structured'].items():
                status = "✓" if value else "✗"
                print(f"  {status} {key:15} : {value}")
        
        print("\n" + "=" * 80)
        print("Interactive Review:")
        print("  [e] Edit extracted data")
        print("  [s] Save as event JSON")
        print("  [c] Copy raw text to clipboard")
        print("  [q] Quit")
        print("=" * 80)
        
        choice = input("\nChoice: ").strip().lower()
        
        if choice == 'e':
            return self._edit_structured_data(analysis.get('structured', {}))
        elif choice == 's':
            return self._save_as_event(analysis.get('structured', {}), analysis.get('source_url'))
        elif choice == 'c':
            self._copy_to_clipboard(analysis.get('raw_text', ''))
            print("✓ Copied to clipboard")
            return None
        else:
            return None
    
    def _edit_structured_data(self, data: Dict) -> Dict:
        """Interactive editing of structured data"""
        print("\n📝 Edit Mode (press Enter to keep current value):\n")
        
        edited = {}
        for key, value in data.items():
            current = f" [{value}]" if value else ""
            new_value = input(f"  {key}{current}: ").strip()
            edited[key] = new_value if new_value else value
        
        return edited
    
    def _save_as_event(self, data: Dict, source_url: str = None) -> str:
        """Save structured data as event JSON for staging"""
        event_data = {
            "title": data.get("title", "Unbekannte Veranstaltung"),
            "date": data.get("date"),
            "time": data.get("time"),
            "location": data.get("location"),
            "description": data.get("description", ""),
            "price": data.get("price"),
            "image_url": source_url,
            "needs_review": True,
            "extracted_from_image": True,
            "extraction_confidence": "manual_review_required"
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"flyer-event-{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(event_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Saved to: {filename}")
        print(f"💡 Copy this to _data/staging/ for review workflow")
        return filename
    
    def _copy_to_clipboard(self, text: str):
        """Copy text to clipboard (platform-specific)"""
        try:
            import pyperclip
            pyperclip.copy(text)
        except ImportError:
            print("\n⚠️  pyperclip not installed, printing instead:")
            print(text)


def main():
    """CLI for flyer analysis"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze event flyer images')
    parser.add_argument('image', help='Image file path or URL')
    parser.add_argument('--engine', choices=['auto', 'tesseract', 'easyocr', 'ollama'],
                       default='auto', help='OCR engine to use')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Interactive review mode')
    parser.add_argument('--json', '-j', action='store_true',
                       help='Output as JSON')
    
    args = parser.parse_args()
    
    analyzer = FlyerAnalyzer(ocr_engine=args.engine)
    
    # Analyze
    if args.image.startswith('http'):
        result = analyzer.analyze_from_url(args.image)
    else:
        result = analyzer.analyze_from_file(args.image)
    
    # Output
    if args.interactive:
        analyzer.interactive_review(args.image, result)
    elif args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Pretty print
        if 'error' in result:
            print(f"❌ {result['error']}")
        else:
            print("\n📄 Extracted Text:")
            print(result.get('raw_text', '')[:300])
            if len(result.get('raw_text', '')) > 300:
                print("... (truncated)")
            print("\n📊 Structured Data:")
            print(json.dumps(result.get('structured', {}), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
