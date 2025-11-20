#!/bin/bash
# HTML Validator mit HTMLHint

set -e

echo "📄 Linting HTML files..."

# Prüfe ob htmlhint installiert ist
if ! command -v npx &> /dev/null; then
    echo "❌ npx not found. Install Node.js first:"
    echo "   ./scripts/dev/setup.sh"
    exit 1
fi

# Installiere htmlhint falls nötig
if ! npx htmlhint --version &> /dev/null; then
    echo "📦 Installing htmlhint..."
    npm install --save-dev htmlhint
fi

# Lint alle HTML-Dateien (außer _site da generiert)
npx htmlhint "*.html" "_layouts/*.html" --config .htmlhintrc

echo "✅ HTML linting complete"
