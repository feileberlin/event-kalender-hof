// Storage-Modul - KISS: Nur das Nötigste
// Verwendet LocalStorage statt Cookies (einfacher, mehr Platz)

export const Storage = {
  // Preferences
  savePrefs(prefs) {
    try {
      localStorage.setItem('krawl_prefs', JSON.stringify(prefs));
    } catch (e) {
      console.warn('Konnte Präferenzen nicht speichern:', e);
    }
  },

  loadPrefs() {
    try {
      const data = localStorage.getItem('krawl_prefs');
      return data ? JSON.parse(data) : null;
    } catch (e) {
      console.warn('Konnte Präferenzen nicht laden:', e);
      return null;
    }
  },

  // Bookmarks
  saveBookmarks(bookmarks) {
    try {
      localStorage.setItem('krawl_bookmarks', JSON.stringify(Array.from(bookmarks)));
    } catch (e) {
      console.warn('Konnte Bookmarks nicht speichern:', e);
    }
  },

  loadBookmarks() {
    try {
      const data = localStorage.getItem('krawl_bookmarks');
      return data ? new Set(JSON.parse(data)) : new Set();
    } catch (e) {
      console.warn('Konnte Bookmarks nicht laden:', e);
      return new Set();
    }
  },

  // Clear all
  clear() {
    localStorage.removeItem('krawl_prefs');
    localStorage.removeItem('krawl_bookmarks');
  }
};
