#!/bin/bash
# Setup-Skript für krawl.ist

set -e

echo "🎉 krawl.ist - Setup"
echo "================================"
echo ""

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Prüfe Ruby
echo -n "Prüfe Ruby... "
if command -v ruby &> /dev/null; then
    RUBY_VERSION=$(ruby -v | cut -d ' ' -f2)
    echo -e "${GREEN}✓${NC} Ruby $RUBY_VERSION"
else
    echo -e "${RED}✗${NC} Ruby nicht gefunden"
    echo "Installiere Ruby mit: brew install ruby (macOS) oder sudo apt install ruby-full (Linux)"
    exit 1
fi

# Prüfe Python
echo -n "Prüfe Python... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d ' ' -f2)
    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python nicht gefunden"
    echo "Installiere Python mit: brew install python@3.11 (macOS) oder sudo apt install python3 (Linux)"
    exit 1
fi

# Prüfe Git
echo -n "Prüfe Git... "
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | cut -d ' ' -f3)
    echo -e "${GREEN}✓${NC} Git $GIT_VERSION"
else
    echo -e "${RED}✗${NC} Git nicht gefunden"
    exit 1
fi

echo ""
echo "📦 Installiere Dependencies..."
echo ""

# Jekyll Dependencies
echo "→ Ruby Gems..."
if [ -f "Gemfile" ]; then
    bundle install
    echo -e "${GREEN}✓${NC} Ruby Gems installiert"
else
    echo -e "${YELLOW}⚠${NC} Gemfile nicht gefunden"
fi

# Python Dependencies
echo "→ Python Packages..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    echo -e "${GREEN}✓${NC} Python Packages installiert"
else
    echo -e "${YELLOW}⚠${NC} requirements.txt nicht gefunden"
fi

echo ""
echo -e "${GREEN}✅ Setup abgeschlossen!${NC}"
echo ""
echo "🚀 Nächste Schritte:"
echo ""
echo "  1. Jekyll-Server starten:"
echo "     ${YELLOW}bundle exec jekyll serve${NC}"
echo ""
echo "  2. Website öffnen:"
echo "     ${YELLOW}http://localhost:4000${NC}"
echo ""
echo "  3. Event-Scraper testen:"
echo "     ${YELLOW}python3 scripts/editorial/scrape_events.py${NC}"
echo ""
echo "  4. Admin-Bereich öffnen:"
echo "     ${YELLOW}http://localhost:4000/admin.html${NC}"
echo ""
echo "📚 Dokumentation: ${YELLOW}README.md${NC}"
echo ""
