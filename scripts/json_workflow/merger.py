#!/usr/bin/env python3
"""
Merger - Applies review decisions and merges approved events
Reads review decision JSON files and updates _data/events.json
"""

import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.schemas import Event, EventCollection

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
STAGING_DIR = PROJECT_ROOT / "_data" / "staging"
EVENTS_JSON = PROJECT_ROOT / "_data" / "events.json"
ARCHIVE_DIR = PROJECT_ROOT / "_data" / "archive"

# Ensure directories exist
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)


class EventMerger:
    """Merges approved events into production events.json"""
    
    def __init__(self):
        self.production_events: EventCollection = self._load_production()
        self.approved_count = 0
        self.rejected_count = 0
        self.merged_count = 0
        self.skipped_count = 0
        
    def _load_production(self) -> EventCollection:
        """Load production events from events.json"""
        if EVENTS_JSON.exists():
            try:
                with open(EVENTS_JSON, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return EventCollection.from_dict(data)
            except Exception as e:
                print(f"⚠️  Error loading events.json: {e}")
                print("   Creating new EventCollection")
        
        # Create new collection if file doesn't exist or is invalid
        return EventCollection(version="2.0", events=[])
    
    def process_review_decisions(self, review_file: Path):
        """Process a single review decision file"""
        print(f"\n📂 Processing: {review_file.name}")
        print("-" * 80)
        
        try:
            with open(review_file, 'r', encoding='utf-8') as f:
                decisions = json.load(f)
            
            # Get the corresponding staging file
            session_id = decisions.get('session_id')
            staging_file = STAGING_DIR / f"events-{session_id}.json"
            
            if not staging_file.exists():
                print(f"❌ Staging file not found: {staging_file.name}")
                return
            
            # Load staged events
            with open(staging_file, 'r', encoding='utf-8') as f:
                staging_data = json.load(f)
            
            staged_events = {
                event['meta']['hash']: Event.from_dict(event)
                for event in staging_data['events']
            }
            
            print(f"📋 Decisions: {len(decisions['decisions'])}")
            print(f"📦 Staged events: {len(staged_events)}")
            print()
            
            # Process each decision
            for decision in decisions['decisions']:
                event_hash = decision['event_hash']
                action = decision['decision']
                
                if event_hash not in staged_events:
                    print(f"⚠️  Event not found: {event_hash}")
                    continue
                
                event = staged_events[event_hash]
                
                if action == 'approved':
                    self._merge_event(event)
                    self.approved_count += 1
                    print(f"✅ Approved: {event.title}")
                    
                elif action == 'rejected':
                    self.rejected_count += 1
                    print(f"❌ Rejected: {event.title}")
                    
                elif action == 'merged':
                    # Already merged into another event (duplicate handling)
                    self.merged_count += 1
                    print(f"🔀 Merged: {event.title}")
                    
                elif action == 'skipped':
                    self.skipped_count += 1
                    print(f"⏭️  Skipped: {event.title}")
            
            # Archive processed files
            self._archive_files(review_file, staging_file)
            
        except Exception as e:
            print(f"❌ Error processing {review_file.name}: {e}")
    
    def _merge_event(self, event: Event):
        """Add event to production collection"""
        # Check if event already exists by ID
        existing_ids = {e.generate_id() for e in self.production_events.events}
        event_id = event.generate_id()
        
        if event_id in existing_ids:
            print(f"   ⚠️  Event already exists (ID: {event_id[:12]})")
            return
        
        # Update meta
        event.meta.needs_review = False
        event.meta.reviewed_at = datetime.now().isoformat()
        event.meta.reviewed_by = "merger.py"
        
        # Add to collection
        self.production_events.events.append(event)
    
    def _archive_files(self, review_file: Path, staging_file: Path):
        """Move processed files to archive"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Archive review decision
        archive_review = ARCHIVE_DIR / f"{review_file.stem}_{timestamp}.json"
        shutil.move(str(review_file), str(archive_review))
        print(f"\n📦 Archived: {archive_review.name}")
        
        # Archive staging file
        archive_staging = ARCHIVE_DIR / f"{staging_file.stem}_{timestamp}.json"
        shutil.move(str(staging_file), str(archive_staging))
        print(f"📦 Archived: {archive_staging.name}")
    
    def save_production(self):
        """Save updated production events to events.json"""
        # Sort events by date (most recent first)
        self.production_events.events.sort(
            key=lambda e: (e.start_date, e.start_time or "00:00"),
            reverse=False
        )
        
        # Update metadata
        self.production_events.meta = {
            "last_updated": datetime.now().isoformat(),
            "total_events": len(self.production_events.events),
            "version": "2.0"
        }
        
        # Create backup
        if EVENTS_JSON.exists():
            backup = EVENTS_JSON.with_suffix('.json.bak')
            shutil.copy2(EVENTS_JSON, backup)
            print(f"\n💾 Backup created: {backup.name}")
        
        # Save to file
        with open(EVENTS_JSON, 'w', encoding='utf-8') as f:
            json.dump(
                self.production_events.to_dict(),
                f,
                ensure_ascii=False,
                indent=2
            )
        
        print(f"✅ Saved: {EVENTS_JSON.name}")
        print(f"   Total events: {len(self.production_events.events)}")
    
    def print_summary(self):
        """Print merge summary"""
        print("\n" + "=" * 80)
        print("📊 Merge Summary")
        print("=" * 80)
        print(f"✅ Approved:  {self.approved_count}")
        print(f"❌ Rejected:  {self.rejected_count}")
        print(f"🔀 Merged:    {self.merged_count}")
        print(f"⏭️  Skipped:   {self.skipped_count}")
        print(f"📚 Total in production: {len(self.production_events.events)}")
        print("=" * 80)


def main():
    """Main merger entry point"""
    print("=" * 80)
    print("🔀 Event Merger - Apply Review Decisions")
    print("=" * 80)
    
    # Find all review decision files
    review_files = list(STAGING_DIR.glob("review-*.json"))
    
    if not review_files:
        print("\n⚠️  No review decision files found in staging/")
        print("   Run reviewer.py first to create review decisions")
        return
    
    print(f"\nFound {len(review_files)} review file(s)")
    
    # Process all reviews
    merger = EventMerger()
    
    for review_file in sorted(review_files):
        merger.process_review_decisions(review_file)
    
    # Save results
    if merger.approved_count > 0:
        merger.save_production()
    else:
        print("\n⚠️  No events approved, events.json unchanged")
    
    # Print summary
    merger.print_summary()
    
    print("\nNext steps:")
    print("  1. Commit changes: git add _data/events.json")
    print("  2. Review diff: git diff _data/events.json")
    print("  3. Push changes: git commit -m 'Add reviewed events' && git push")


if __name__ == '__main__':
    main()
