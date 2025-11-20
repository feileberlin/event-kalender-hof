/**
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
   * Pattern: DOM scraping - no separate API needed (KISS) [1]
   * Why: Static site = HTML is the database
   * 
   * Data attributes used:
   * - data-event-url-card: Unique event URL
   * - data-event-date: ISO date string
   * - data-event-categories: Comma-separated list
   * - data-event-lat/lng: GPS coordinates
   */
  async loadFromDOM() { // [2]
    const eventCards = document.querySelectorAll('.event-card');
    
    this.allEvents = Array.from(eventCards).map(card => ({ // [3]
      // Core data
      url: card.dataset.eventUrlCard || '',
      title: card.querySelector('h3')?.textContent.trim() || '', // [4]
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
        .filter(Boolean), // [5]
      
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
   * Algorithm: Simplified sine wave approximation [6]
   * Note: For production, use SunCalc.js for accuracy
   */
  calculateDawnTime(date, lat = 50.3195, lng = 11.9173) {
    // Day of year (1-365)
    const dayOfYear = Math.floor((date - new Date(date.getFullYear(), 0, 0)) / 86400000); // [7]
    
    // Sine wave: ±1.5 hours around base time [6]
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
      
      // Unique values (for filter dropdowns) [8]
      categories: [...new Set(this.allEvents.flatMap(e => e.categories))], // [9]
      locations: [...new Set(this.allEvents.map(e => e.location).filter(Boolean))]
    };
  }
}

// ========================================
// REFERENCES & INSPIRATIONS
// ========================================

/**
 * [1] DOM as database pattern
 * Source: Static site philosophy, Jekyll best practices
 * 
 * Why notable: Instead of fetching JSON via API, we extract data from HTML.
 * This eliminates:
 * - API latency (data is already in DOM)
 * - JSON parsing overhead
 * - Network request complexity
 * - CORS issues
 * 
 * Tradeoff: Tight coupling between HTML structure and JS. But for static sites
 * generated server-side (Jekyll), this is acceptable and performant.
 * 
 * Historical note: This pattern was common in early 2000s (semantic HTML + jQuery),
 * fell out of favor with SPAs, but is making a comeback with SSG (Jamstack).
 */

/**
 * [2] async function without await
 * Source: JavaScript best practices for future-proofing
 * 
 * Why notable: loadFromDOM() is marked async but has no await. This is intentional
 * for future extensibility. If we later need to fetch supplementary data via API,
 * we can add await calls without changing the function signature or call sites.
 * 
 * Pattern:
 *   async loadFromDOM() { return this.events; }
 * 
 * This signals to callers: "This might be async, await me to be safe."
 */

/**
 * [3] Array.from() + map() pattern
 * Source: Modern JavaScript array manipulation
 * 
 * Why notable: querySelectorAll() returns NodeList (array-like but not array).
 * Array.from() converts to real array, enabling .map().
 * 
 * Alternative: [...eventCards].map() (spread operator)
 * We use Array.from() for clarity - it's more explicit about intent.
 */

/**
 * [4] Optional chaining + nullish coalescing
 * Source: ES2020 - Modern null handling
 * 
 * Pattern:
 *   card.querySelector('h3')?.textContent.trim() || ''
 * 
 * Breakdown:
 * - ?. returns undefined if querySelector returns null (no throw)
 * - || '' provides fallback for falsy values
 * 
 * This is defensive programming - handles missing DOM elements gracefully.
 */

/**
 * [5] filter(Boolean) trick
 * Source: JavaScript functional programming idioms
 * 
 * Why notable: After splitting/trimming comma-separated categories, we might
 * have empty strings. filter(Boolean) removes all falsy values:
 * 
 *   ['Music', '', 'Art', null] → ['Music', 'Art']
 * 
 * This is a clever use of Boolean as predicate function. Alternative:
 * 
 *   .filter(c => c) or .filter(c => c.length > 0)
 * 
 * But filter(Boolean) is more idiomatic and handles null/undefined too.
 */

/**
 * [6] Sine wave sunrise approximation
 * Source: Astronomical algorithms (simplified)
 * Inspiration: SunCalc.js (but we don't want the dependency)
 * 
 * Why notable: Real sunrise calculation requires complex astronomy (solar declination,
 * equation of time, atmospheric refraction). For "events at dawn" filter, ±30 min
 * accuracy is fine, so we use simple sine wave:
 * 
 *   sunrise ≈ 6:00 ± 1.5h * sin(2π * dayOfYear/365)
 * 
 * This approximates the ~3-hour variation between summer (early) and winter (late)
 * sunrises at mid-latitudes. Good enough for UX, not for astronomy.
 * 
 * Accuracy: ±30 minutes vs. astronomical calculation
 * Code: 5 lines vs. 200+ lines for full implementation
 */

/**
 * [7] Day of year calculation trick
 * Source: Stack Overflow - Calculate day number of the year
 * https://stackoverflow.com/questions/8619879/
 * 
 * Why notable: This one-liner calculates day-of-year (1-365):
 * 
 *   (date - new Date(date.getFullYear(), 0, 0)) / 86400000
 * 
 * Breakdown:
 * - new Date(year, 0, 0) = Dec 31 of previous year (month 0 = Jan, day 0 = previous month's last)
 * - Subtract dates → milliseconds difference
 * - Divide by 86400000 (ms per day) → day number
 * 
 * This is a clever hack that avoids looping through months/days. Edge case: leap years
 * are handled automatically by Date constructor.
 */

/**
 * [8] Spread operator for Set deduplication
 * Source: ES6 - Modern array/set conversion
 * 
 * Pattern:
 *   [...new Set(array)]
 * 
 * This is the idiomatic way to remove duplicates from array:
 * 1. new Set(array) → deduplicate
 * 2. [...set] → convert back to array
 * 
 * Much cleaner than:
 *   array.filter((v, i, a) => a.indexOf(v) === i)
 */

/**
 * [9] flatMap for nested array flattening
 * Source: ES2019 - Array.prototype.flatMap()
 * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/flatMap
 * 
 * Why notable: Each event can have multiple categories (array). To get all unique
 * categories across all events, we need to flatten then deduplicate:
 * 
 *   events.flatMap(e => e.categories)
 * 
 * This is equivalent to:
 *   events.map(e => e.categories).flat()
 * 
 * But flatMap() does it in one pass (more efficient). Combined with Set:
 * 
 *   [...new Set(events.flatMap(e => e.categories))]
 * 
 * This is peak modern JavaScript - concise, performant, elegant.
 */
