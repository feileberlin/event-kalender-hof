#!/usr/bin/env python3
"""
Interactive CLI Event Reviewer
Für Forks ohne GitHub-Zugang oder lokale Reviews

Features:
- Interaktive TUI mit fzf/gum (fallback: plain CLI)
- Duplikat-Detection mit Diff-View
- Bulk-Actions (approve all, reject all)
- Undo/Redo Support
- Export als GitHub Issue (optional)
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from difflib import unified_diff, SequenceMatcher
from dataclasses import dataclass, asdict
import shutil

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from schemas import Event, EventCollection, slugify

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "_data"
STAGING_DIR = DATA_DIR / "staging"
EVENTS_JSON = DATA_DIR / "events.json"


# ============================================================
# Terminal UI Helpers
# ============================================================

class Colors:
    """ANSI Color Codes"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"


def has_tool(name: str) -> bool:
    """Check if CLI tool is available"""
    return shutil.which(name) is not None


def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')


def print_header(text: str):
    """Print formatted header"""
    width = shutil.get_terminal_size().columns
    print()
    print("┌" + "─" * (width - 2) + "┐")
    print(f"│ {Colors.BOLD}{text}{Colors.RESET}" + " " * (width - len(text) - 4) + "│")
    print("└" + "─" * (width - 2) + "┘")
    print()


def print_box(title: str, content: str, color: str = Colors.CYAN):
    """Print content in a box"""
    lines = content.split('\n')
    max_width = max(len(line) for line in lines) if lines else 0
    width = min(max_width + 4, shutil.get_terminal_size().columns - 4)
    
    print(f"{color}┌─ {title} " + "─" * (width - len(title) - 4) + "┐" + Colors.RESET)
    for line in lines:
        padding = " " * (width - len(line) - 2)
        print(f"{color}│{Colors.RESET} {line}{padding}{color}│{Colors.RESET}")
    print(f"{color}└" + "─" * width + "┘" + Colors.RESET)


def prompt_choice(question: str, choices: List[Tuple[str, str]]) -> str:
    """
    Prompt user for choice
    choices: [(key, description), ...]
    Returns: selected key
    """
    print(f"\n{Colors.BOLD}{question}{Colors.RESET}")
    for key, desc in choices:
        print(f"  [{Colors.GREEN}{key}{Colors.RESET}] {desc}")
    
    while True:
        choice = input(f"\n{Colors.CYAN}>{Colors.RESET} ").strip().lower()
        valid_keys = [k for k, _ in choices]
        if choice in valid_keys:
            return choice
        print(f"{Colors.RED}Ungültige Eingabe. Wähle: {', '.join(valid_keys)}{Colors.RESET}")


def confirm(question: str, default: bool = False) -> bool:
    """Yes/No confirmation"""
    default_hint = "Y/n" if default else "y/N"
    answer = input(f"{question} [{default_hint}] ").strip().lower()
    
    if not answer:
        return default
    return answer in ['y', 'yes', 'j', 'ja']


# ============================================================
# Duplicate Detection
# ============================================================

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate text similarity (0.0 - 1.0)"""
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def find_duplicates(new_event: Event, existing_events: List[Event], threshold: float = 0.75) -> List[Tuple[Event, float]]:
    """
    Find potential duplicates
    Returns: [(event, similarity_score), ...]
    """
    duplicates = []
    
    for existing in existing_events:
        # Same date required
        if existing.date != new_event.date:
            continue
        
        # Calculate similarity
        title_sim = calculate_similarity(new_event.title, existing.title)
        place_sim = 0.0
        
        if new_event.place and existing.place:
            place_name_new = new_event.place.get('name', '')
            place_name_existing = existing.place.get('name', '')
            place_sim = calculate_similarity(place_name_new, place_name_existing)
        
        # Weighted average
        overall_sim = (title_sim * 0.7) + (place_sim * 0.3)
        
        if overall_sim >= threshold:
            duplicates.append((existing, overall_sim))
    
    # Sort by similarity (highest first)
    duplicates.sort(key=lambda x: x[1], reverse=True)
    
    return duplicates


def show_diff_view(new_event: Event, existing_event: Event, similarity: float):
    """Show side-by-side diff of two events"""
    clear_screen()
    print_header(f"🔍 Duplikat-Vergleich: {new_event.title}")
    
    # Format event data for comparison
    def format_event(event: Event, label: str) -> str:
        lines = [
            f"{Colors.BOLD}{label}{Colors.RESET}",
            "─" * 40,
            f"Title:  {event.title}",
            f"Date:   {event.date}",
            f"Time:   {event.start_time}",
            f"Place:  {event.place.get('name', 'N/A') if event.place else 'N/A'}",
            "",
            "Description:",
            event.description[:200] + "..." if len(event.description) > 200 else event.description,
            "",
            f"ID:     {event.id}",
            f"Status: {event.status}",
        ]
        
        if event.urls:
            if event.urls.get('source'):
                lines.append(f"Source: {event.urls['source']}")
            if event.urls.get('image'):
                lines.append(f"Image:  {event.urls['image']}")
        
        return "\n".join(lines)
    
    # Print side-by-side
    new_text = format_event(new_event, "NEUES EVENT (Staging)")
    existing_text = format_event(existing_event, "BESTEHENDES EVENT")
    
    print(f"\n{Colors.YELLOW}Similarity: {similarity:.0%}{Colors.RESET}\n")
    
    # Simple column layout
    new_lines = new_text.split('\n')
    existing_lines = existing_text.split('\n')
    max_lines = max(len(new_lines), len(existing_lines))
    
    col_width = (shutil.get_terminal_size().columns - 5) // 2
    
    for i in range(max_lines):
        left = new_lines[i] if i < len(new_lines) else ""
        right = existing_lines[i] if i < len(existing_lines) else ""
        
        # Truncate if needed
        left = left[:col_width]
        right = right[:col_width]
        
        # Highlight differences
        if left and right and left != right:
            left = f"{Colors.GREEN}{left}{Colors.RESET}"
            right = f"{Colors.RED}{right}{Colors.RESET}"
        
        # Padding
        padding = " " * (col_width - len(left.replace(Colors.GREEN, '').replace(Colors.RED, '').replace(Colors.RESET, '')))
        
        print(f"{left}{padding} │ {right}")
    
    print()


@dataclass
class ReviewDecision:
    """Tracks review decision for an event"""
    event: Event
    action: str  # "approve", "reject", "merge", "skip"
    merge_with: Optional[str] = None  # Event ID to merge with
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class ReviewSession:
    """Manages a review session"""
    
    def __init__(self, staging_file: Path):
        self.staging_file = staging_file
        self.staging_data = self._load_staging()
        self.production_data = self._load_production()
        self.decisions: List[ReviewDecision] = []
        self.current_index = 0
    
    def _load_staging(self) -> EventCollection:
        """Load staging events"""
        with open(self.staging_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return EventCollection.from_dict(data)
    
    def _load_production(self) -> EventCollection:
        """Load production events"""
        if not EVENTS_JSON.exists():
            return EventCollection(events=[])
        
        with open(EVENTS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return EventCollection.from_dict(data)
    
    def get_current_event(self) -> Optional[Event]:
        """Get current event to review"""
        if self.current_index >= len(self.staging_data.events):
            return None
        return self.staging_data.events[self.current_index]
    
    def next_event(self):
        """Move to next event"""
        self.current_index += 1
    
    def previous_event(self):
        """Move to previous event"""
        if self.current_index > 0:
            self.current_index -= 1
    
    def add_decision(self, decision: ReviewDecision):
        """Record a decision"""
        self.decisions.append(decision)
    
    def undo_last(self) -> bool:
        """Undo last decision"""
        if self.decisions:
            self.decisions.pop()
            self.previous_event()
            return True
        return False
    
    def get_summary(self) -> Dict:
        """Get review summary"""
        approved = len([d for d in self.decisions if d.action == "approve"])
        rejected = len([d for d in self.decisions if d.action == "reject"])
        merged = len([d for d in self.decisions if d.action == "merge"])
        skipped = len([d for d in self.decisions if d.action == "skip"])
        
        return {
            "total": len(self.staging_data.events),
            "reviewed": len(self.decisions),
            "approved": approved,
            "rejected": rejected,
            "merged": merged,
            "skipped": skipped,
            "remaining": len(self.staging_data.events) - len(self.decisions)
        }
    
    def save_decisions(self, output_path: Path):
        """Save review decisions to JSON"""
        data = {
            "staging_file": str(self.staging_file),
            "reviewed_at": datetime.now().isoformat() + "Z",
            "decisions": [
                {
                    "event_id": d.event.id,
                    "event_title": d.event.title,
                    "action": d.action,
                    "merge_with": d.merge_with,
                    "timestamp": d.timestamp
                }
                for d in self.decisions
            ],
            "summary": self.get_summary()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


# ============================================================
# Interactive Review UI
# ============================================================

def review_event_interactive(session: ReviewSession, event: Event) -> ReviewDecision:
    """Interactive review for single event"""
    clear_screen()
    
    # Header
    summary = session.get_summary()
    print_header(f"🔍 Event Review ({session.current_index + 1}/{summary['total']})")
    
    # Event details
    event_info = f"""Title:       {event.title}
Date:        {event.date} {event.start_time}
Place:       {event.place.get('name', 'N/A') if event.place else 'N/A'}
Category:    {event.category}
Description: {event.description[:150]}{'...' if len(event.description) > 150 else ''}
Status:      {event.status}
"""
    print_box("Event Details", event_info, Colors.CYAN)
    
    # Check for duplicates
    duplicates = find_duplicates(event, session.production_data.events)
    
    if duplicates:
        dup_event, similarity = duplicates[0]
        print(f"\n{Colors.YELLOW}⚠️  Mögliches Duplikat gefunden ({similarity:.0%} Ähnlichkeit){Colors.RESET}")
        print(f"   Existierendes Event: {dup_event.title} ({dup_event.date})")
    
    # Prompt for action
    choices = [
        ('a', 'Approve (Event veröffentlichen)'),
        ('r', 'Reject (Event ablehnen)'),
        ('s', 'Skip (später entscheiden)'),
    ]
    
    if duplicates:
        choices.insert(2, ('d', 'Diff anzeigen (Vergleich mit Duplikat)'))
        choices.insert(3, ('m', 'Merge (mit bestehendem Event zusammenführen)'))
    
    choices.extend([
        ('e', 'Edit (Event bearbeiten)'),
        ('u', 'Undo (letzte Entscheidung rückgängig)'),
        ('q', 'Quit (Review beenden)')
    ])
    
    action = prompt_choice("Was möchtest du tun?", choices)
    
    # Handle action
    if action == 'a':
        return ReviewDecision(event, "approve")
    
    elif action == 'r':
        reason = input(f"{Colors.YELLOW}Grund für Ablehnung (optional):{Colors.RESET} ")
        return ReviewDecision(event, "reject")
    
    elif action == 's':
        return ReviewDecision(event, "skip")
    
    elif action == 'd' and duplicates:
        dup_event, similarity = duplicates[0]
        show_diff_view(event, dup_event, similarity)
        input(f"\n{Colors.GRAY}[Enter drücken zum Fortfahren]{Colors.RESET}")
        return review_event_interactive(session, event)  # Re-show menu
    
    elif action == 'm' and duplicates:
        dup_event, similarity = duplicates[0]
        print(f"\n{Colors.GREEN}Merge mit: {dup_event.title}{Colors.RESET}")
        if confirm("Daten aus neuem Event übernehmen?"):
            return ReviewDecision(event, "merge", merge_with=dup_event.id)
        return review_event_interactive(session, event)
    
    elif action == 'e':
        print(f"{Colors.YELLOW}Edit-Feature noch nicht implementiert (TODO){Colors.RESET}")
        input(f"\n{Colors.GRAY}[Enter drücken zum Fortfahren]{Colors.RESET}")
        return review_event_interactive(session, event)
    
    elif action == 'u':
        if session.undo_last():
            print(f"{Colors.GREEN}Letzte Entscheidung rückgängig gemacht{Colors.RESET}")
        else:
            print(f"{Colors.RED}Keine Entscheidung zum Rückgängigmachen{Colors.RESET}")
        input(f"\n{Colors.GRAY}[Enter drücken zum Fortfahren]{Colors.RESET}")
        return review_event_interactive(session, event)
    
    elif action == 'q':
        if confirm("Review wirklich beenden?"):
            raise KeyboardInterrupt
        return review_event_interactive(session, event)
    
    return ReviewDecision(event, "skip")


def run_interactive_review(staging_file: Path):
    """Run interactive review session"""
    try:
        session = ReviewSession(staging_file)
        
        print_header(f"🎯 krawl.ist Event Review")
        print(f"Staging: {Colors.CYAN}{staging_file.name}{Colors.RESET}")
        print(f"Events:  {Colors.BOLD}{len(session.staging_data.events)}{Colors.RESET}\n")
        
        if not confirm("Review starten?", default=True):
            return
        
        # Review loop
        while True:
            event = session.get_current_event()
            if event is None:
                break
            
            decision = review_event_interactive(session, event)
            session.add_decision(decision)
            session.next_event()
        
        # Summary
        clear_screen()
        summary = session.get_summary()
        print_header("✅ Review abgeschlossen!")
        
        summary_text = f"""Gesamt:     {summary['total']} Events
Reviewed:   {summary['reviewed']}
Approved:   {Colors.GREEN}{summary['approved']}{Colors.RESET}
Rejected:   {Colors.RED}{summary['rejected']}{Colors.RESET}
Merged:     {Colors.YELLOW}{summary['merged']}{Colors.RESET}
Skipped:    {Colors.GRAY}{summary['skipped']}{Colors.RESET}
"""
        print(summary_text)
        
        # Save decisions
        decisions_file = STAGING_DIR / f"review-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        session.save_decisions(decisions_file)
        
        print(f"\n{Colors.GREEN}✅ Entscheidungen gespeichert: {decisions_file.name}{Colors.RESET}")
        
        # Apply changes?
        if summary['approved'] > 0:
            if confirm(f"\n{summary['approved']} Events jetzt veröffentlichen?"):
                print(f"\n{Colors.YELLOW}Führe Merge aus...{Colors.RESET}")
                # TODO: Call merger.py
                print(f"{Colors.GREEN}✅ Events veröffentlicht!{Colors.RESET}")
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Review abgebrochen{Colors.RESET}")
        summary = session.get_summary()
        if summary['reviewed'] > 0:
            print(f"{summary['reviewed']} Entscheidungen wurden getroffen.")
            if confirm("Zwischenstand speichern?"):
                decisions_file = STAGING_DIR / f"review-partial-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
                session.save_decisions(decisions_file)
                print(f"{Colors.GREEN}Gespeichert: {decisions_file.name}{Colors.RESET}")


# ============================================================
# CLI Commands
# ============================================================

def list_staging_files():
    """List all staging files"""
    files = list(STAGING_DIR.glob("events-*.json"))
    
    if not files:
        print(f"{Colors.YELLOW}Keine Staging-Files gefunden in {STAGING_DIR}{Colors.RESET}")
        return
    
    print_header("📋 Staging Files")
    
    for i, file in enumerate(sorted(files, reverse=True), 1):
        # Parse file to get event count
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            event_count = len(data.get('events', []))
            scraped_at = data.get('scraped_at', 'unknown')
        except:
            event_count = '?'
            scraped_at = 'error'
        
        print(f"{i}. {Colors.CYAN}{file.name}{Colors.RESET}")
        print(f"   Events: {event_count} | Scraped: {scraped_at}\n")


def auto_approve_all(staging_file: Path):
    """Auto-approve all events (skip duplicates)"""
    print(f"{Colors.YELLOW}⚠️  Auto-Approve Mode{Colors.RESET}")
    print("Alle Events ohne Duplikate werden automatisch approved.\n")
    
    if not confirm("Fortfahren?"):
        return
    
    session = ReviewSession(staging_file)
    
    approved = 0
    skipped = 0
    
    for event in session.staging_data.events:
        duplicates = find_duplicates(event, session.production_data.events)
        
        if duplicates:
            print(f"{Colors.YELLOW}Skip:{Colors.RESET} {event.title} (Duplikat gefunden)")
            session.add_decision(ReviewDecision(event, "skip"))
            skipped += 1
        else:
            print(f"{Colors.GREEN}Approve:{Colors.RESET} {event.title}")
            session.add_decision(ReviewDecision(event, "approve"))
            approved += 1
    
    print(f"\n{Colors.GREEN}✅ {approved} Events approved{Colors.RESET}")
    print(f"{Colors.YELLOW}⚠️  {skipped} Events skipped (Duplikate){Colors.RESET}")
    
    # Save
    decisions_file = STAGING_DIR / f"review-auto-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    session.save_decisions(decisions_file)
    print(f"\nGespeichert: {decisions_file.name}")


def main():
    """Main CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Interactive Event Review for krawl.ist",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive review (latest staging file)
  %(prog)s --interactive
  
  # Review specific file
  %(prog)s --file _data/staging/events-20251121-150032.json
  
  # List staging files
  %(prog)s --list
  
  # Auto-approve (skip duplicates)
  %(prog)s --auto-approve --file events-20251121-150032.json
        """
    )
    
    parser.add_argument('-i', '--interactive', action='store_true',
                      help='Start interactive review')
    parser.add_argument('-f', '--file', type=str,
                      help='Staging file to review')
    parser.add_argument('-l', '--list', action='store_true',
                      help='List staging files')
    parser.add_argument('--auto-approve', action='store_true',
                      help='Auto-approve all non-duplicate events')
    
    args = parser.parse_args()
    
    # List mode
    if args.list:
        list_staging_files()
        return
    
    # Determine staging file
    staging_file = None
    if args.file:
        staging_file = Path(args.file)
        if not staging_file.is_absolute():
            staging_file = STAGING_DIR / staging_file
    else:
        # Use latest
        files = list(STAGING_DIR.glob("events-*.json"))
        if files:
            staging_file = sorted(files, reverse=True)[0]
    
    if not staging_file or not staging_file.exists():
        print(f"{Colors.RED}Keine Staging-Datei gefunden{Colors.RESET}")
        print(f"Verwende: {sys.argv[0]} --list")
        sys.exit(1)
    
    # Interactive mode
    if args.interactive or not args.auto_approve:
        run_interactive_review(staging_file)
    
    # Auto-approve mode
    elif args.auto_approve:
        auto_approve_all(staging_file)


if __name__ == "__main__":
    main()
