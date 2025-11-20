#!/usr/bin/env python3
"""
Cleanup Test Events
Löscht alle Test-Events (markiert mit test_event: true)
"""

import os
import yaml
from pathlib import Path


def cleanup_test_events():
    """Löscht alle Events mit test_event: true im Frontmatter"""
    
    # Projekt-Root finden
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    events_dir = project_root / "_events"
    
    print(f"🔍 Suche Test-Events in: {events_dir}")
    
    deleted = 0
    for filepath in events_dir.glob("*.md"):
        # Frontmatter lesen
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Prüfe ob Frontmatter existiert
        if not content.startswith('---'):
            continue
        
        # Parse Frontmatter
        try:
            parts = content.split('---', 2)
            if len(parts) < 3:
                continue
            
            frontmatter = yaml.safe_load(parts[1])
            
            # Lösche wenn test_event: true
            if frontmatter and frontmatter.get('test_event') is True:
                os.remove(filepath)
                deleted += 1
                print(f"🗑️  Gelöscht: {filepath.name}")
        
        except yaml.YAMLError:
            continue
    
    print(f"\n✅ {deleted} Test-Events gelöscht!")


if __name__ == "__main__":
    cleanup_test_events()
