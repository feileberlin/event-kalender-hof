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
    
    // Visual feedback: ★ = bookmarked, ☆ = not bookmarked
    button.textContent = isBookmarked ? '★' : '☆';
    button.title = isBookmarked ? 'Remove bookmark' : 'Add bookmark';
    button.classList.toggle('bookmarked', isBookmarked);
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
