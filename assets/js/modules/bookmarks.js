// Bookmark-Modul - Vereinfacht, fokussiert
import { Storage } from './storage.js';

export class BookmarkManager {
  constructor() {
    this.bookmarks = Storage.loadBookmarks();
  }

  toggle(eventUrl) {
    if (this.bookmarks.has(eventUrl)) {
      this.bookmarks.delete(eventUrl);
    } else {
      this.bookmarks.add(eventUrl);
    }
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
    if (confirm('Alle Bookmarks löschen?')) {
      this.bookmarks.clear();
      Storage.saveBookmarks(this.bookmarks);
      return true;
    }
    return false;
  }

  // UI-Update (einfach)
  updateButton(button) {
    const eventUrl = button.dataset.eventUrl;
    const isBookmarked = this.has(eventUrl);
    
    button.textContent = isBookmarked ? '★' : '☆';
    button.title = isBookmarked ? 'Bookmark entfernen' : 'Bookmark setzen';
    button.classList.toggle('bookmarked', isBookmarked);
  }

  // Bookmarked Events extrahieren (für Print/Mail)
  getEventData() {
    const events = [];
    this.bookmarks.forEach(url => {
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
