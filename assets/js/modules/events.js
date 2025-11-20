// Events-Modul - Event-Daten & Logik
export class EventManager {
  constructor() {
    this.events = [];
    this.allEvents = [];
  }

  // Events laden (von Jekyll-generierten Daten)
  async loadFromDOM() {
    const eventCards = document.querySelectorAll('.event-card');
    this.allEvents = Array.from(eventCards).map(card => ({
      url: card.dataset.eventUrlCard || '',
      title: card.querySelector('h3')?.textContent.trim() || '',
      date: card.dataset.eventDate || '',
      dateObj: new Date(card.dataset.eventDate || ''),
      time: card.dataset.eventTime || '',
      location: card.dataset.eventLocation || '',
      venue: card.querySelector('.event-location')?.textContent.trim() || '',
      categories: (card.dataset.eventCategories || '').split(',').map(c => c.trim()).filter(Boolean),
      description: card.querySelector('.event-description')?.textContent.trim() || '',
      lat: parseFloat(card.dataset.eventLat) || null,
      lng: parseFloat(card.dataset.eventLng) || null,
      imageUrl: card.dataset.eventImage || null,
      element: card
    }));

    this.events = [...this.allEvents];
    return this.events;
  }

  // Alle Events zurücksetzen
  resetFilter() {
    this.events = [...this.allEvents];
  }

  // Gefilterte Events setzen
  setFiltered(filteredEvents) {
    this.events = filteredEvents;
  }

  // Upcoming Events (ab jetzt)
  getUpcoming(limit = null) {
    const now = new Date();
    const upcoming = this.events
      .filter(e => e.dateObj >= now)
      .sort((a, b) => a.dateObj - b.dateObj);
    
    return limit ? upcoming.slice(0, limit) : upcoming;
  }

  // Events nach Datum sortieren
  sortByDate(ascending = true) {
    this.events.sort((a, b) => {
      return ascending 
        ? a.dateObj - b.dateObj 
        : b.dateObj - a.dateObj;
    });
    return this.events;
  }

  // Sonnenaufgang berechnen (vereinfacht)
  calculateDawnTime(date, lat = 50.3195, lng = 11.9173) {
    // Vereinfachte Berechnung (ohne Bibliothek)
    // Für genauere Berechnung: SunCalc.js o.ä.
    const dayOfYear = Math.floor((date - new Date(date.getFullYear(), 0, 0)) / 86400000);
    const offset = Math.sin(dayOfYear / 365 * 2 * Math.PI) * 1.5;
    const dawnHour = 6 + offset; // ~6:00 Uhr ± 1.5h je nach Jahreszeit
    
    const dawn = new Date(date);
    dawn.setHours(Math.floor(dawnHour), Math.floor((dawnHour % 1) * 60), 0, 0);
    return dawn;
  }

  // Events für einen bestimmten Tag
  getByDate(date) {
    const targetDate = new Date(date).toDateString();
    return this.events.filter(e => 
      e.dateObj.toDateString() === targetDate
    );
  }

  // Events nach Kategorie
  getByCategory(category) {
    return this.events.filter(e => 
      e.categories.includes(category)
    );
  }

  // Events nach Location
  getByLocation(location) {
    return this.events.filter(e => 
      e.location === location
    );
  }

  // Event-Statistiken
  getStats() {
    const now = new Date();
    return {
      total: this.allEvents.length,
      filtered: this.events.length,
      upcoming: this.events.filter(e => e.dateObj >= now).length,
      past: this.events.filter(e => e.dateObj < now).length,
      categories: [...new Set(this.allEvents.flatMap(e => e.categories))],
      locations: [...new Set(this.allEvents.map(e => e.location).filter(Boolean))]
    };
  }
}
