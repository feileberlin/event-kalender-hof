#!/bin/bash
# Entwicklungs-Server starten

echo "🚀 Starte Jekyll Development Server..."
echo ""
echo "Server läuft auf: http://localhost:4000"
echo "Admin-Bereich: http://localhost:4000/admin.html"
echo ""
echo "Drücke Ctrl+C zum Beenden"
echo ""

bundle exec jekyll serve --livereload --host 0.0.0.0
