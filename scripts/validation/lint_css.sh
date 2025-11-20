#!/bin/bash
# CSS Linter mit Stylelint

set -e

echo "🎨 Linting CSS files..."

# Prüfe ob stylelint installiert ist
if ! command -v npx &> /dev/null; then
    echo "❌ npx not found. Install Node.js first:"
    echo "   ./scripts/dev/setup.sh"
    exit 1
fi

# Installiere stylelint falls nötig
if ! npx stylelint --version &> /dev/null; then
    echo "📦 Installing stylelint..."
    npm install --save-dev stylelint stylelint-config-standard
fi

# Lint alle CSS-Dateien
npx stylelint "assets/css/**/*.css" "_site/assets/css/**/*.css" --config .stylelintrc.json

echo "✅ CSS linting complete"
