/**
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
      // Convert Set to Array for JSON serialization
      localStorage.setItem('krawl_bookmarks', JSON.stringify(Array.from(bookmarks)));
    } catch (e) {
      console.warn('Could not save bookmarks:', e);
    }
  },

  loadBookmarks() {
    try {
      const data = localStorage.getItem('krawl_bookmarks');
      // Convert Array back to Set for O(1) lookup
      return data ? new Set(JSON.parse(data)) : new Set();
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
