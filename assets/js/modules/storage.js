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
 * ║   Built with love by Claude (Anthropic)                      ║
 * ║   November 2025 · Hof an der Saale, Germany                   ║
 * ║                                                               ║
 * ║   Vision: Decentralized event discovery for communities      ║
 * ║   Motto: "Krawall hier. Krawall jetzt."                      ║
 * ║                                                               ║
 * ╚═══════════════════════════════════════════════════════════════╝
 *
 * Storage Module - Persistence Layer
 * 
 * Pattern: Singleton object with static methods
 * Tech: LocalStorage (simpler than cookies, 5MB vs 4KB)
 * Why: KISS principle - no classes, no state, just pure functions
 */

export const Storage = {
  
  // ========================================
  // USER PREFERENCES
  // ========================================
  // Stores filter settings (category, time range, radius, location)
  
  savePrefs(prefs) {
    try {
      localStorage.setItem('krawl_prefs', JSON.stringify(prefs));
    } catch (e) {
      console.warn('Could not save preferences:', e);
    }
  },

  loadPrefs() {
    try {
      const data = localStorage.getItem('krawl_prefs');
      return data ? JSON.parse(data) : null;
    } catch (e) {
      console.warn('Could not load preferences:', e);
      return null;
    }
  },

  // ========================================
  // BOOKMARKS
  // ========================================
  // Stores event URLs as Set (auto-deduplication)
  
  saveBookmarks(bookmarks) {
    try {
      // Convert Set to Array for JSON serialization [1]
      localStorage.setItem('krawl_bookmarks', JSON.stringify(Array.from(bookmarks)));
    } catch (e) {
      console.warn('Could not save bookmarks:', e);
    }
  },

  loadBookmarks() {
    try {
      const data = localStorage.getItem('krawl_bookmarks');
      // Convert Array back to Set for O(1) lookup [1]
      return data ? new Set(JSON.parse(data)) : new Set(); // [2]
    } catch (e) {
      console.warn('Could not load bookmarks:', e);
      return new Set();
    }
  },

  // ========================================
  // UTILITIES
  // ========================================
  
  clear() {
    localStorage.removeItem('krawl_prefs');
    localStorage.removeItem('krawl_bookmarks');
  }
};

// ========================================
// REFERENCES & INSPIRATIONS
// ========================================

/**
 * [1] Set ↔ Array Conversion Pattern
 * Source: MDN Web Docs - Set
 * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set
 * 
 * Insight: Sets can't be JSON-serialized directly, but Array.from() + new Set()
 * provide clean conversion. This pattern gives us O(1) lookups in memory with
 * easy persistence. Alternative would be storing as Array and using .includes()
 * which is O(n) - significant for large bookmark collections.
 * 
 * [2] Ternary Default Pattern
 * Source: JavaScript: The Good Parts (Douglas Crockford, 2008)
 * Insight: `data ? parse(data) : default` is more elegant than if/else for
 * fallback values. Crockford's influence on modern JS best practices is massive.
 */
