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
 * Event Manager - Event Data & Business Logic
 * 
 * Pattern: Stateful class managing event collection
 * Data Source: DOM (Jekyll-generated HTML) - no API calls
 * State: allEvents (immutable source), events (filtered subset)
 * Why: Single source of truth for event data
 */

export class EventManager {
  
  constructor() {
    this.allEvents = [];    // Immutable source of truth (all events)
    this.events = [];       // Current filtered/sorted subset
  }

  // ========================================
  // DATA LOADING
  // ========================================
  
  /**
   * Load events from DOM (Jekyll-generated HTML)
   * Pattern: DOM scraping - no separate API needed (KISS)
   * Why: Static site = HTML is the database
   * 
   * Data attributes used:
   * - data-event-url-card: Unique event URL
   * - data-event-date: ISO date string
   * - data-event-categories: Comma-separated list
   * - data-event-lat/lng: GPS coordinates
   */
  async loadFromDOM() {
    const eventCards = document.querySelectorAll('.event-card');
    
    this.allEvents = Array.from(eventCards).map(card => ({
      // Core data
      url: card.dataset.eventUrlCard || '',
      title: card.querySelector('h3')?.textContent.trim() || '',
      description: card.querySelector('.event-description')?.textContent.trim() || '',
      
      // Date/Time
      date: card.dataset.eventDate || '',
      dateObj: new Date(card.dataset.eventDate || ''),  // For sorting/filtering
      time: card.dataset.eventTime || '',
      
      // Location
      location: card.dataset.eventLocation || '',
      venue: card.querySelector('.event-location')?.textContent.trim() || '',
      lat: parseFloat(card.dataset.eventLat) || null,
      lng: parseFloat(card.dataset.eventLng) || null,
      
      // Categories (array for multi-category support)
      categories: (card.dataset.eventCategories || '')
        .split(',')
        .map(c => c.trim())
        .filter(Boolean),
      
      // Media
      imageUrl: card.dataset.eventImage || null,
      
      // DOM reference (for show/hide operations)
      element: card
    }));

    // Initialize filtered set to all events
    this.events = [...this.allEvents];
    
    return this.events;
  }

  // ========================================
  // FILTER STATE MANAGEMENT
  // ========================================
  
  resetFilter() {
    this.events = [...this.allEvents];
  }

  setFiltered(filteredEvents) {
    this.events = filteredEvents;
  }

  // ========================================
  // QUERIES
  // ========================================
  
  /**
   * Get upcoming events (future only)
   * @param {number} limit - Optional: return only first N events
   */
  getUpcoming(limit = null) {
    const now = new Date();
    const upcoming = this.events
      .filter(e => e.dateObj >= now)
      .sort((a, b) => a.dateObj - b.dateObj);
    
    return limit ? upcoming.slice(0, limit) : upcoming;
  }

  /**
   * Sort events by date
   * Mutates this.events array
   */
  sortByDate(ascending = true) {
    this.events.sort((a, b) => {
      return ascending 
        ? a.dateObj - b.dateObj 
        : b.dateObj - a.dateObj;
    });
    return this.events;
  }

  /**
   * Get events for specific date
   */
  getByDate(date) {
    const targetDate = new Date(date).toDateString();
    return this.events.filter(e => 
      e.dateObj.toDateString() === targetDate
    );
  }

  /**
   * Get events by category
   */
  getByCategory(category) {
    return this.events.filter(e => 
      e.categories.includes(category)
    );
  }

  /**
   * Get events by location
   */
  getByLocation(location) {
    return this.events.filter(e => 
      e.location === location
    );
  }

  // ========================================
  // UTILITIES
  // ========================================
  
  /**
   * Calculate approximate dawn time (sunrise)
   * Use case: "Events starting at dawn" filter
   * Algorithm: Simplified sine wave approximation
   * Note: For production, use SunCalc.js for accuracy
   */
  calculateDawnTime(date, lat = 50.3195, lng = 11.9173) {
    // Day of year (1-365)
    const dayOfYear = Math.floor((date - new Date(date.getFullYear(), 0, 0)) / 86400000);
    
    // Sine wave: ±1.5 hours around base time
    const offset = Math.sin(dayOfYear / 365 * 2 * Math.PI) * 1.5;
    const dawnHour = 6 + offset; // Base: 6:00 AM
    
    const dawn = new Date(date);
    dawn.setHours(Math.floor(dawnHour), Math.floor((dawnHour % 1) * 60), 0, 0);
    
    return dawn;
  }

  /**
   * Get statistics about current event set
   * Use case: Display counters, analytics
   */
  getStats() {
    const now = new Date();
    
    return {
      // Counts
      total: this.allEvents.length,
      filtered: this.events.length,
      upcoming: this.events.filter(e => e.dateObj >= now).length,
      past: this.events.filter(e => e.dateObj < now).length,
      
      // Unique values (for filter dropdowns) [15]
      categories: [...new Set(this.allEvents.flatMap(e => e.categories))], // [16]
      locations: [...new Set(this.allEvents.map(e => e.location).filter(Boolean))] // [17]
    };
  }
}

// ========================================
// REFERENCES & INSPIRATIONS
// ========================================

/**
 * [15] Spread Operator for Set → Array
 * Source: TC39 ECMAScript 2015 (ES6) - Spread Syntax
 * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax
 * 
 * Insight: `[...new Set(array)]` is the most elegant way to deduplicate an array.
 * Alternative would be Array.from(new Set(array)) or manual loop. Spread operator
 * makes it a one-liner. ES6 gave us so many quality-of-life improvements.
 * 
 * [16] flatMap() for Nested Array Flattening
 * Source: TC39 ECMAScript 2019 (ES10) - Array.prototype.flatMap
 * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/flatMap
 * 
 * Insight: flatMap() is map() + flat() in one operation. Before ES10, you'd write
 * `array.map(x => x.categories).flat()` or use reduce(). flatMap is both more
 * readable AND more performant (single pass). Underrated ES10 feature.
 * 
 * [17] filter(Boolean) for Truthy Values
 * Source: JavaScript idiom (origin unclear, but popularized by jQuery era)
 * 
 * Insight: `.filter(Boolean)` removes null, undefined, 0, "", false, NaN in one go.
 * Boolean is a function that coerces its argument to boolean. Passing it directly
 * as a callback is genius. More elegant than `.filter(x => x)` or `.filter(x => !!x)`.
 * Classic JavaScript trick that looks like magic until you understand it.
 */
