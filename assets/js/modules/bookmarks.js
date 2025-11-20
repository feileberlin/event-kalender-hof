/**
 * Bookmark Manager - User's Saved Events
 * 
 * Pattern: Class with instance state
 * State: Set of event URLs (auto-deduplication)
 * Persistence: Syncs to Storage layer on every mutation
 * Why: Encapsulates bookmark logic + UI updates
 */

import { Storage } from './storage.js';

export class BookmarkManager {
  
  constructor() {
    // Load bookmarks from persistent storage
    // Set data structure: O(1) lookups, auto-dedup
    this.bookmarks = Storage.loadBookmarks();
  }

  // ========================================
  // CORE OPERATIONS (CRUD)
  // ========================================
  
  /**
   * Toggle bookmark on/off
   * @returns {boolean} New bookmark state (true = bookmarked)
   */
  toggle(eventUrl) {
    if (this.bookmarks.has(eventUrl)) {
      this.bookmarks.delete(eventUrl);
    } else {
      this.bookmarks.add(eventUrl);
    }
    
    // Persist immediately (no batch saves - KISS)
    Storage.saveBookmarks(this.bookmarks);
    
    return this.bookmarks.has(eventUrl);
  }

  has(eventUrl) {
    return this.bookmarks.has(eventUrl);
  }

  getAll() {
    return Array.from(this.bookmarks);
  }

  count() {
    return this.bookmarks.size;
  }

  clear() {
    if (confirm('Delete all bookmarks?')) {
      this.bookmarks.clear();
      Storage.saveBookmarks(this.bookmarks);
      return true;
    }
    return false;
  }

  // ========================================
  // UI INTEGRATION
  // ========================================
  
  /**
   * Update bookmark button appearance
   * Pattern: Direct DOM manipulation (no virtual DOM - KISS)
   */
  updateButton(button) {
    const eventUrl = button.dataset.eventUrl;
    const isBookmarked = this.has(eventUrl);
    
    // Visual feedback: ★ = bookmarked, ☆ = not bookmarked [1]
    button.textContent = isBookmarked ? '★' : '☆';
    button.title = isBookmarked ? 'Remove bookmark' : 'Add bookmark';
    button.classList.toggle('bookmarked', isBookmarked); // [2]
  }

  // ========================================
  // DATA EXPORT
  // ========================================
  
  /**
   * Extract full event data for bookmarked events
   * Use case: Print/email features
   * Pattern: DOM scraping (no event data duplication)
   */
  getEventData() {
    const events = [];
    
    this.bookmarks.forEach(url => {
      // Find corresponding event card in DOM
      const card = document.querySelector(`[data-event-url-card="${url}"]`);
      
      if (card) {
        events.push({
          url,
          title: card.querySelector('h3')?.textContent || '',
          date: card.querySelector('.event-date')?.textContent || '',
          location: card.querySelector('.event-location')?.textContent || ''
        });
      }
    });
    
    return events;
  }
}

// ========================================
// REFERENCES & INSPIRATIONS
// ========================================

/**
 * [1] Unicode star characters for bookmark UI
 * Source: Unicode.org - Miscellaneous Symbols
 * https://unicode.org/charts/PDF/U2600.pdf
 * 
 * Why notable: Using ★ (U+2605 BLACK STAR) and ☆ (U+2606 WHITE STAR) instead of
 * icon fonts or SVGs eliminates dependencies and reduces file size. The symbols
 * render consistently across all modern browsers and are screen-reader friendly.
 * This is peak KISS - no Font Awesome, no webpack, just UTF-8.
 * 
 * Alternative approaches (not used):
 * - Font Awesome (5KB+ overhead for 2 icons)
 * - Custom SVG (overkill for simple toggle)
 * - CSS ::before with content (less flexible)
 */

/**
 * [2] classList.toggle() with boolean parameter
 * Source: DOM Living Standard
 * https://dom.spec.whatwg.org/#dom-domtokenlist-toggle
 * 
 * Why notable: Many developers don't know classList.toggle() accepts a second
 * parameter to force add/remove. Common pattern is:
 * 
 *   if (condition) el.classList.add('class');
 *   else el.classList.remove('class');
 * 
 * But toggle with boolean is cleaner:
 * 
 *   el.classList.toggle('class', condition);
 * 
 * This is a hidden gem in the DOM API that eliminates if/else verbosity.
 * Supported since IE11, so no polyfill needed.
 */
