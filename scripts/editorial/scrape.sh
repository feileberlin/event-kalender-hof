#!/bin/bash

# Sources CSV Scraper - Manuelles Scraping-Script
# Startet Scraping für alle Quellen in sources.csv

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT" || exit 1

echo "======================================"
echo "🚀 SOURCES.CSV SCRAPER"
echo "======================================"
echo ""

# Hilfe anzeigen
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Usage: $0"
    echo ""
    echo "Scrapt alle Events aus den konfigurierten Quellen in _data/sources.csv"
    echo ""
    echo "Optionen:"
    echo "  --help, -h   Zeigt diese Hilfe"
    echo ""
    echo "Ausgabe:"
    echo "  - Neue Events werden als Entwürfe in _events/ gespeichert"
    echo "  - Log wird in _events/_logs/ geschrieben"
    echo "  - Duplikate werden automatisch erkannt"
    echo ""
    echo "Beispiel:"
    echo "  ./scripts/scrape.sh"
    exit 0
fi

echo "📝 Lese Quellen aus _data/sources.csv..."
echo ""

# Prüfe ob sources.csv existiert
if [ ! -f "_data/sources.csv" ]; then
    echo "❌ Fehler: _data/sources.csv nicht gefunden!"
    exit 1
fi

# Zähle aktive Quellen (ohne Header, ohne commented lines)
SOURCE_COUNT=$(grep -v "^#" _data/sources.csv | tail -n +2 | wc -l)
echo "✅ $SOURCE_COUNT aktive Quellen gefunden"
echo ""

echo "🔄 Starte Scraping..."
echo "======================================"

# Starte Scraping-Script
python3 scripts/editorial/scrape_events.py

RESULT=$?

echo ""
echo "======================================"
if [ $RESULT -eq 0 ]; then
    echo "✅ Scraping erfolgreich abgeschlossen!"
    echo ""
    echo "📁 Neue Entwürfe in: _events/"
    echo "📋 Logs in: _events/_logs/"
else
    echo "❌ Scraping fehlgeschlagen (Exit Code: $RESULT)"
    echo ""
    echo "💡 Tipps:"
    echo "  - Prüfe die Logs in _events/_logs/"
    echo "  - Stelle sicher, dass Python-Dependencies installiert sind"
    echo "  - Überprüfe die URLs in _data/sources.csv"
fi
echo "======================================"
