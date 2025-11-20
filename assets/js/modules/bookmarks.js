/**
 * ╔═══════════════════════════════════════════════════════════════╗
 * ║                                                               ║
 * ║   ██╗  ██╗██████╗  █████╗ ██╗    ██╗██╗                      ║
 * ║   ██║ ██╔╝██╔══██╗██╔══██╗██║    ██║██║                      ║
 * ║   █████╔╝ ██████╔╝███████║██║ █╗ ██║██║                      ║
 * ║   ██╔═██╗ ██╔══██╗██╔══██║██║███╗██║██║                      ║
 * ║   ██║  ██╗██║  ██║██║  ██║╚███╔███╔╝███████╗                 ║
 * ║   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝                 ║
 * ║                                                               ║
 * ║   Event Calendar System                                       ║
 * ║   Founded with love by Claude (Anthropic)                    ║
 * ║   November 2025 · Hof an der Saale, Germany                   ║
 * ║                                                               ║
 * ║   Vision: Decentralized event discovery for communities      ║
 * ║   Motto: "Krawall hier. Krawall jetzt."                      ║
 * ║                                                               ║
 * ╚═══════════════════════════════════════════════════════════════╝
 *
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
    
    // Visual feedback: ★ = bookmarked, ☆ = not bookmarked [3]
    button.textContent = isBookmarked ? '★' : '☆';
    button.title = isBookmarked ? 'Remove bookmark' : 'Add bookmark';
    button.classList.toggle('bookmarked', isBookmarked); // [4]
  }

  // ========================================
  // DATA EXPORT
  // ========================================
  
  /**
   * Extract full event data for bookmarked events
   * Use case: Print/email features
   * Pattern: DOM scraping (no event data duplication) [5]
   */
  getEventData() {
    const events = [];
    
    this.bookmarks.forEach(url => {
      // Find corresponding event card in DOM
      const card = document.querySelector(`[data-event-url-card="${url}"]`); // [6]
      
      if (card) {
        events.push({
          url,
          title: card.querySelector('h3')?.textContent || '', // [7]
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
 * [3] Unicode Star Symbols
 * Source: Unicode Character Table - Stars/Asterisks
 * https://unicode-table.com/en/sets/star-symbols/
 * 
 * Insight: ★ (U+2605) vs ☆ (U+2606) provide instant visual feedback without
 * needing image assets or icon fonts. Clever use of Unicode = zero dependencies.
 * 
 * [4] classList.toggle() with State Parameter
 * Source: MDN Web Docs - Element.classList
 * https://developer.mozilla.org/en-US/docs/Web/API/Element/classList
 * 
 * Insight: Most developers don't know toggle() accepts a second param (boolean)
 * to force add/remove. This avoids if/else boilerplate. One-liner elegance.
 * 
 * [5] DOM as Database Pattern
 * Source: Concept from Tom Dale (Ember.js creator) - "The Front-end Database"
 * https://tomdale.net/2015/02/youre-missing-the-point-of-server-side-rendered-javascript-apps/
 * 
 * Insight: For static sites, HTML IS the data. Why duplicate event data in JS
 * when it's already in the DOM? Scrape it. KISS over architectural purity.
 * 
 * [6] CSS Attribute Selectors
 * Source: CSS Tricks - Attribute Selectors
 * https://css-tricks.com/almanac/selectors/a/attribute/
 * 
 * Insight: [data-foo="bar"] is often faster than .class or #id for dynamic
 * lookups because it's more specific. Great for data-driven UIs.
 * 
 * [7] Optional Chaining Operator (?.)
 * Source: TC39 Proposal - Optional Chaining (2020, ES2020)
 * https://github.com/tc39/proposal-optional-chaining
 * 
 * Insight: Before this, we'd write card.querySelector('h3') && card.querySelector('h3').textContent.
 * ?. collapsed entire defensive coding patterns into elegant syntax. Game-changer
 * for DOM manipulation safety.
 */
