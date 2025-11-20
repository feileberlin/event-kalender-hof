#!/bin/bash
# Markdown Linter mit markdownlint

set -e

echo "📝 Linting Markdown files..."

# Prüfe ob markdownlint installiert ist
if ! command -v npx &> /dev/null; then
    echo "❌ npx not found. Install Node.js first:"
    echo "   ./scripts/dev/setup.sh"
    exit 1
fi

# Installiere markdownlint falls nötig
if ! npx markdownlint --version &> /dev/null; then
    echo "📦 Installing markdownlint..."
    npm install --save-dev markdownlint-cli
fi

# Lint alle Markdown-Dateien
npx markdownlint "*.md" "docs/**/*.md" "_events/**/*.md" --config .markdownlint.json --ignore node_modules --ignore _site

echo "✅ Markdown linting complete"
