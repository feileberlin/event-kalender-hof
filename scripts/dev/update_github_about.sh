#!/bin/bash
# Update GitHub Repository About Section
# Setzt Description, Homepage, Topics via GitHub CLI

set -e

REPO="feileberlin/krawl.ist"

# Lese Werte aus _config.yml
DESCRIPTION="Krawall hier. Krawall jetzt. — Events bis Sonnenaufgang in Hof an der Saale"
HOMEPAGE="https://krawl.ist"

# Topics (GitHub Tags)
TOPICS="events,calendar,jekyll,open-source,hof,oberfranken,punk,diy,community"

echo "� Aktualisiere GitHub Repository Metadata..."
echo "Repository: $REPO"
echo "Description: $DESCRIPTION"
echo "Homepage: $HOMEPAGE"
echo "Topics: $TOPICS"
echo ""

# Prüfe ob gh CLI installiert ist
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) nicht gefunden!"
    echo "   Installation: https://cli.github.com/"
    exit 1
fi

# Prüfe ob authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Nicht bei GitHub authentifiziert!"
    echo "   Run: gh auth login"
    exit 1
fi

# Update Repository Metadata
echo "📝 Setze Description..."
gh repo edit "$REPO" --description "$DESCRIPTION"

echo "🌐 Setze Homepage..."
gh repo edit "$REPO" --homepage "$HOMEPAGE"

echo "🏷️  Setze Topics..."
gh repo edit "$REPO" --add-topic "$(echo $TOPICS | tr ',' ' ')"

echo ""
echo "✅ GitHub About Section aktualisiert!"
echo "🔗 Siehe: https://github.com/$REPO"
