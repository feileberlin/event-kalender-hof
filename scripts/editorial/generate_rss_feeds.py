#!/usr/bin/env python3
"""
RSS Feed Generator
Generiert RSS-Feed-Dateien basierend auf _config.yml Konfiguration
"""

import yaml
from pathlib import Path

def generate_rss_feeds():
    """Generiert RSS-Feed-Dateien aus _config.yml"""
    
    # Config laden
    with open('_config.yml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    rss_feeds = config.get('filters', {}).get('rss_feeds', [])
    
    if not rss_feeds:
        print("⚠️  Keine RSS-Feeds in _config.yml definiert")
        return
    
    # Feeds erstellen
    for feed in rss_feeds:
        name = feed.get('name', 'Unnamed Feed')
        filename = feed.get('filename', 'feed.xml')
        time_filter = feed.get('time', '')
        category_filter = feed.get('category', '')
        radius_filter = feed.get('radius', '')
        
        # Pfad bestimmen
        if filename == 'feed.xml':
            filepath = Path(filename)
        else:
            filepath = Path('feeds') / filename
            filepath.parent.mkdir(exist_ok=True)
        
        # Permalink generieren
        if filename == 'feed.xml':
            permalink = '/feed.xml'
        else:
            permalink = f'/feeds/{filename}'
        
        # Front Matter generieren
        content = f"""---
layout: rss
permalink: {permalink}
feed_name: "{name}"
time_filter: "{time_filter}"
category_filter: "{category_filter}"
radius_filter: "{radius_filter}"
---
"""
        
        # Datei schreiben
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {filepath} erstellt ({name})")
    
    print(f"\n🎉 {len(rss_feeds)} RSS-Feeds generiert!")
    print("\nFeeds sind erreichbar unter:")
    for feed in rss_feeds:
        filename = feed.get('filename', 'feed.xml')
        if filename == 'feed.xml':
            print(f"  - https://krawl.ist/feed.xml")
        else:
            print(f"  - https://krawl.ist/feeds/{filename}")

if __name__ == '__main__':
    generate_rss_feeds()
