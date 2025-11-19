#!/bin/bash
# Entwicklungs-Server starten

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT" || exit 1

echo "🚀 Starte Jekyll Development Server..."
echo ""
echo "Server läuft auf: http://localhost:4000"
echo "Admin-Bereich: http://localhost:4000/admin.html"
echo ""
echo "Drücke Ctrl+C zum Beenden"
echo ""

bundle exec jekyll serve --livereload --host 0.0.0.0
