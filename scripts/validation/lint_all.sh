#!/bin/bash
# Alle Lint-Tests auf einmal ausführen

set -e

echo "🔍 Running all linters..."
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# JavaScript
echo "================================"
bash "$SCRIPT_DIR/lint_javascript.sh"
echo ""

# CSS
echo "================================"
bash "$SCRIPT_DIR/lint_css.sh"
echo ""

# HTML
echo "================================"
bash "$SCRIPT_DIR/lint_html.sh"
echo ""

# Markdown
echo "================================"
bash "$SCRIPT_DIR/lint_markdown.sh"
echo ""

echo "================================"
echo "✅ All linters passed!"
