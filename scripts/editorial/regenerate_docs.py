#!/usr/bin/env python3
"""
Dokumentations-Regenerierungs-Script
Aktualisiert automatisch Projekt-Dokumentation basierend auf aktuellem Stand.
"""

import os
import sys
import yaml
import json
from datetime import datetime
from pathlib import Path

# Projekt-Root
PROJECT_ROOT = Path(__file__).parent.parent.parent

def load_config():
    """Lädt _config.yml"""
    config_path = PROJECT_ROOT / '_config.yml'
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def count_events():
    """Zählt Events nach Status"""
    events_dir = PROJECT_ROOT / '_events'
    stats = {
        'total': 0,
        'published': 0,
        'draft': 0,
        'archived': 0,
        'recurring': 0
    }
    
    for event_file in events_dir.glob('*.md'):
        if event_file.name.startswith('_'):
            continue
            
        with open(event_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if '---' in content:
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        frontmatter = yaml.safe_load(parts[1])
                        stats['total'] += 1
                        
                        status = frontmatter.get('status', 'Entwurf')
                        if status == 'Öffentlich':
                            stats['published'] += 1
                        elif status == 'Archiviert':
                            stats['archived'] += 1
                        else:
                            stats['draft'] += 1
                        
                        if frontmatter.get('recurring', {}).get('enabled'):
                            stats['recurring'] += 1
                    except:
                        pass
    
    return stats

def count_sources():
    """Zählt konfigurierte Scraping-Quellen"""
    sources_file = PROJECT_ROOT / '_data' / 'sources.csv'
    if not sources_file.exists():
        return 0
    
    with open(sources_file, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
        return len(lines) - 1  # Header abziehen

def count_venues():
    """Zählt registrierte Veranstaltungsorte"""
    venues_file = PROJECT_ROOT / '_data' / 'venues.csv'
    if not venues_file.exists():
        return 0
    
    with open(venues_file, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
        return len(lines) - 1  # Header abziehen

def count_code_lines():
    """Zählt Code-Zeilen"""
    stats = {
        'python': 0,
        'javascript': 0,
        'css': 0,
        'html': 0,
        'markdown': 0
    }
    
    # Python
    for py_file in (PROJECT_ROOT / 'scripts').glob('*.py'):
        with open(py_file, 'r', encoding='utf-8') as f:
            stats['python'] += len([l for l in f if l.strip() and not l.strip().startswith('#')])
    
    # JavaScript
    js_file = PROJECT_ROOT / 'assets' / 'js' / 'main.js'
    if js_file.exists():
        with open(js_file, 'r', encoding='utf-8') as f:
            stats['javascript'] = len([l for l in f if l.strip() and not l.strip().startswith('//')])
    
    # CSS
    css_file = PROJECT_ROOT / 'assets' / 'css' / 'style.css'
    if css_file.exists():
        with open(css_file, 'r', encoding='utf-8') as f:
            stats['css'] = len([l for l in f if l.strip() and not l.strip().startswith('/*')])
    
    # HTML (Layouts)
    for html_file in (PROJECT_ROOT / '_layouts').glob('*.html'):
        with open(html_file, 'r', encoding='utf-8') as f:
            stats['html'] += len([l for l in f if l.strip()])
    
    # Markdown (Docs)
    for md_file in (PROJECT_ROOT / 'docs').glob('*.md'):
        with open(md_file, 'r', encoding='utf-8') as f:
            stats['markdown'] += len([l for l in f if l.strip()])
    
    return stats

def get_git_info():
    """Holt Git-Informationen"""
    import subprocess
    
    try:
        # Letzter Commit
        last_commit = subprocess.check_output(
            ['git', 'log', '-1', '--format=%H %ai %s'],
            cwd=PROJECT_ROOT
        ).decode('utf-8').strip()
        
        # Commit-Count
        commit_count = subprocess.check_output(
            ['git', 'rev-list', '--count', 'HEAD'],
            cwd=PROJECT_ROOT
        ).decode('utf-8').strip()
        
        return {
            'last_commit': last_commit,
            'commit_count': int(commit_count)
        }
    except:
        return None

def update_project_stats():
    """Aktualisiert PROJECT.md mit aktuellen Statistiken"""
    project_md = PROJECT_ROOT / 'docs' / 'PROJECT.md'
    
    if not project_md.exists():
        print(f"⚠️  {project_md} nicht gefunden")
        return
    
    # Statistiken sammeln
    config = load_config()
    event_stats = count_events()
    source_count = count_sources()
    venue_count = count_venues()
    code_stats = count_code_lines()
    git_info = get_git_info()
    
    # Neue Statistik-Sektion erstellen
    stats_section = f"""
## 📊 Projekt-Statistiken

**Stand:** {datetime.now().strftime('%d. %B %Y, %H:%M Uhr')}

### Events
- **Gesamt:** {event_stats['total']} Events
- **Veröffentlicht:** {event_stats['published']}
- **Entwürfe:** {event_stats['draft']}
- **Archiviert:** {event_stats['archived']}
- **Wiederkehrend:** {event_stats['recurring']}

### Datenquellen
- **Scraping-Quellen:** {source_count}
- **Veranstaltungsorte:** {venue_count}
- **Standorte:** {len(config.get('locations', {}))}

### Code-Metriken
- **Python:** {code_stats['python']:,} Zeilen
- **JavaScript:** {code_stats['javascript']:,} Zeilen
- **CSS:** {code_stats['css']:,} Zeilen
- **HTML:** {code_stats['html']:,} Zeilen
- **Markdown (Docs):** {code_stats['markdown']:,} Zeilen
- **Gesamt:** {sum(code_stats.values()):,} Zeilen

### Repository
- **Commits:** {git_info['commit_count'] if git_info else 'N/A'}
- **Letzter Commit:** `{git_info['last_commit'].split()[0][:7] if git_info else 'N/A'}`
"""
    
    # Datei lesen und Statistik-Sektion ersetzen/einfügen
    with open(project_md, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Prüfen ob Statistik-Sektion existiert
    if '## 📊 Projekt-Statistiken' in content:
        # Ersetzen (von ## 📊 bis zum nächsten ##)
        import re
        pattern = r'## 📊 Projekt-Statistiken.*?(?=\n## |\Z)'
        content = re.sub(pattern, stats_section.strip(), content, flags=re.DOTALL)
    else:
        # Nach "Zusammenfassung" einfügen
        if '## Zusammenfassung' in content:
            parts = content.split('## Zusammenfassung', 1)
            content = parts[0] + '## Zusammenfassung' + parts[1].split('\n\n', 1)[0] + '\n\n' + stats_section.strip() + '\n\n' + parts[1].split('\n\n', 1)[1]
    
    # Schreiben
    with open(project_md, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {project_md.name} aktualisiert")
    print(f"   - Events: {event_stats['total']} ({event_stats['published']} veröffentlicht)")
    print(f"   - Code: {sum(code_stats.values()):,} Zeilen")
    print(f"   - Commits: {git_info['commit_count'] if git_info else 'N/A'}")

def update_readme_badges():
    """Aktualisiert README.md Badges"""
    readme = PROJECT_ROOT / 'README.md'
    
    if not readme.exists():
        print(f"⚠️  {readme} nicht gefunden")
        return
    
    event_stats = count_events()
    
    # Badge-Zeile erstellen
    badges = f"""[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://krawl.ist/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Events](https://img.shields.io/badge/Events-{event_stats['published']}-blue)](https://krawl.ist/)
[![Version](https://img.shields.io/badge/Version-v1.7.0-orange)](docs/CHANGELOG.md)"""
    
    with open(readme, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Badges ersetzen
    import re
    pattern = r'\[!\[Live Demo\].*?\n\[!\[License.*?\]\(LICENSE\)\]'
    content = re.sub(pattern, badges, content, flags=re.DOTALL)
    
    with open(readme, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {readme.name} Badges aktualisiert")

def main():
    """Hauptfunktion"""
    print("📚 Dokumentations-Regenerierung")
    print("=" * 60)
    
    try:
        update_project_stats()
        update_readme_badges()
        
        print("=" * 60)
        print("✅ Dokumentation erfolgreich regeneriert")
        print(f"   Zeitstempel: {datetime.now().isoformat()}")
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
