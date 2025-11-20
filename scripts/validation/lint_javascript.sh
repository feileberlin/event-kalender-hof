#!/bin/bash
# JavaScript Linter mit ESLint

set -e

echo "⚡ Linting JavaScript files..."

# Prüfe ob eslint installiert ist
if ! command -v npx &> /dev/null; then
    echo "❌ npx not found. Install Node.js first:"
    echo "   ./scripts/dev/setup.sh"
    exit 1
fi

# ESLint sollte bereits konfiguriert sein (eslint.config.js existiert)
if ! npx eslint --version &> /dev/null; then
    echo "❌ ESLint not found. Run:"
    echo "   npm install"
    exit 1
fi

# Lint alle JavaScript-Dateien
npx eslint "assets/js/**/*.js" "scripts/**/*.js" --config eslint.config.js

echo "✅ JavaScript linting complete"
