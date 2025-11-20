/**
 * Filter Manager - Event Filtering Logic
 * 
 * Pattern: Stateful class managing filter criteria
 * State: Active filters (category, time, radius, location)
 * Core: filterEvents() applies all filters in pipeline pattern
 * Why: Centralized filter logic, easy to extend with new filters
 */

export class FilterManager {
  
  constructor() {
    // Filter state - all criteria combined
    this.activeFilters = {
      categories: new Set(),      // Multi-select: Set for O(1) lookup
      timeRange: 'sunrise',       // 'sunrise', 'tatort', 'moon' (Default: bis Sonnenaufgang)
      radius: 5,                  // Distance in km from user location
      location: null              // Specific venue filter
    };
    
    // Configured categories (from _config.yml, excluding "Sonstiges")
    // Needed to determine which events belong to "Sonstiges" category
    this.configuredCategories = [];
  }
  
  /**
   * Set list of configured categories (from _config.yml)
   * Needed to determine which events belong to "Sonstiges"
   */
  setConfiguredCategories(categories) {
    this.configuredCategories = categories.filter(c => c !== 'Sonstiges');
  }

  // ========================================
  // CATEGORY FILTER
  // ========================================
  // Multi-select: User can filter by multiple categories at once
  
  toggleCategory(category) {
    if (this.activeFilters.categories.has(category)) {
      this.activeFilters.categories.delete(category);
    } else {
      this.activeFilters.categories.add(category);
    }
    return this.activeFilters.categories;
  }

  clearCategories() {
    this.activeFilters.categories.clear();
  }

  hasCategory(category) {
    return this.activeFilters.categories.has(category);
  }

  // ========================================
  // TIME FILTER
  // ========================================
  
  setTimeRange(range) {
    this.activeFilters.timeRange = range;
  }

  getTimeRange() {
    return this.activeFilters.timeRange;
  }
  
  /**
   * Berechnet n\u00e4chsten Sonnenaufgang (heute oder morgen)
   * Vereinfachte Berechnung: 6:00 Uhr lokale Zeit (TODO: echte astronomische Berechnung)
   */
  getNextSunrise() {
    const now = new Date();
    const sunrise = new Date(now);
    sunrise.setHours(6, 0, 0, 0);
    
    // Wenn Sonnenaufgang heute schon vorbei, nehme morgen
    if (now > sunrise) {
      sunrise.setDate(sunrise.getDate() + 1);
    }
    
    return sunrise;
  }
  
  /**
   * Berechnet nächsten Tatort-Termin
   * Tatort = beliebteste TV-Sendung in Deutschland, läuft Sonntags 20:15 Uhr (ARD)
   */
  getNextTatort() {
    const now = new Date();
    const tatort = new Date(now);
    
    // N\u00e4chster Sonntag
    const daysUntilSunday = (7 - now.getDay()) % 7;
    tatort.setDate(now.getDate() + (daysUntilSunday === 0 ? 7 : daysUntilSunday));
    tatort.setHours(20, 15, 0, 0);
    
    // Wenn heute Sonntag ist und 20:15 schon vorbei, nehme n\u00e4chsten Sonntag
    if (now.getDay() === 0 && now.getHours() >= 20 && now.getMinutes() >= 15) {
      tatort.setDate(tatort.getDate() + 7);
    }
    
    return tatort;
  }
  
  /**
   * Berechnet n\u00e4chste Mondphase (Vollmond oder Neumond, je nachdem was n\u00e4her)
   * Vereinfachte Berechnung basierend auf Lunation (29.53 Tage)
   */
  getNextMoonPhase() {
    const now = new Date();
    
    // Referenz: Neumond am 1. Januar 2000, 18:14 UTC
    const knownNewMoon = new Date(Date.UTC(2000, 0, 6, 18, 14));
    const lunarCycle = 29.530588853; // Tage
    
    // Tage seit Referenz-Neumond
    const daysSinceNew = (now - knownNewMoon) / (1000 * 60 * 60 * 24);
    const currentPhase = (daysSinceNew % lunarCycle) / lunarCycle;
    
    // N\u00e4chster Vollmond (Phase 0.5) und Neumond (Phase 0.0/1.0)
    let daysToFullMoon, daysToNewMoon;
    
    if (currentPhase < 0.5) {
      daysToFullMoon = (0.5 - currentPhase) * lunarCycle;
      daysToNewMoon = (1.0 - currentPhase) * lunarCycle;
    } else {
      daysToFullMoon = (1.5 - currentPhase) * lunarCycle;
      daysToNewMoon = (1.0 - currentPhase) * lunarCycle;
    }
    
    // N\u00e4here Phase ausw\u00e4hlen
    const daysToNext = Math.min(daysToFullMoon, daysToNewMoon);
    const nextPhase = new Date(now.getTime() + daysToNext * 24 * 60 * 60 * 1000);
    
    // UI-Update: Label im Select anpassen
    if (typeof document !== 'undefined') {
      const moonOption = document.getElementById('moonOption');
      if (moonOption) {
        const isFullMoon = daysToFullMoon < daysToNewMoon;
        moonOption.textContent = isFullMoon ? '\ud83c\udf15 bis Vollmond' : '\ud83c\udf11 bis Neumond';
        moonOption.value = 'moon';
      }
    }
    
    return nextPhase;
  }

  // ========================================
  // RADIUS FILTER
  // ========================================
  // Only applies if user location is available
  // null = unlimited (disable radius filter)
  
  setRadius(radius) {
    // null means "unlimited" - disable radius filtering
    this.activeFilters.radius = radius === null ? null : parseFloat(radius);
  }

  getRadius() {
    return this.activeFilters.radius;
  }

  // ========================================
  // LOCATION FILTER
  // ========================================
  
  setLocation(location) {
    this.activeFilters.location = location;
  }

  getLocation() {
    return this.activeFilters.location;
  }

  // ========================================
  // CORE FILTERING LOGIC
  // ========================================
  
  /**
   * Apply all active filters to event list
   * Pattern: Pipeline - each filter eliminates non-matching events [10]
   * Performance: Early return (continue) avoids checking remaining filters [11]
   * 
   * @param {Array} events - All available events
   * @param {MapManager} mapManager - Needed for distance calculation
   * @returns {Array} Filtered events
   */
  filterEvents(events, mapManager) {
    const now = new Date();
    const filtered = [];

    for (const event of events) { // [12]
      
      // FILTER 1: Categories (if any selected)
      if (this.activeFilters.categories.size > 0) {
        const eventCategories = event.categories || [];
        
        // Special handling for "Sonstiges": show events that DON'T match configured categories
        if (this.activeFilters.categories.has('Sonstiges')) {
          const matchesConfiguredCategory = eventCategories.some(cat => 
            this.configuredCategories.includes(cat)
          );
          // For "Sonstiges": skip if event matches any configured category
          if (matchesConfiguredCategory) continue;
        } else {
          // Normal categories: check if event matches any selected category
          const hasMatch = eventCategories.some(cat => // [13]
            this.activeFilters.categories.has(cat)
          );
          if (!hasMatch) continue; // Skip to next event [11]
        }
      }

      // FILTER 2: Time Range
      const eventDate = new Date(event.date);
      const timeRange = this.activeFilters.timeRange;
      
      // Cutoff-Zeit berechnen (entweder aus Config oder astronomisch)
      let cutoff;
      
      // Prüfe ob im DOM ein data-hours Attribut gesetzt ist (aus _config.yml)
      const timeFilterSelect = document.getElementById('timeFilter');
      const selectedOption = timeFilterSelect?.querySelector(`option[value="${timeRange}"]`);
      const configuredHours = selectedOption?.dataset.hours;
      
      if (configuredHours) {
        // Verwende konfigurierte Stunden aus _config.yml (max. 720h = 1 Monat)
        const hours = Math.min(parseFloat(configuredHours), 720);
        cutoff = new Date(Date.now() + hours * 60 * 60 * 1000);
      } else {
        // Fallback: Spezielle Berechnungen
        if (timeRange === 'sunrise') {
          cutoff = this.getNextSunrise();  // ~6 Uhr heute/morgen
        } else if (timeRange === 'tatort') {
          cutoff = this.getNextTatort();  // Nächster Sonntag 20:15 (TV-Sendezeit)
        } else if (timeRange === 'moon') {
          cutoff = this.getNextMoonPhase();  // Astronomische Mondphasen-Berechnung
        }
      }
      
      if (cutoff && eventDate > cutoff) continue;

      // FILTER 3: Radius (Distance)
      // Only applies if:
      // - User shared their location
      // - Radius is not null (unlimited)
      // - Event has coordinates
      if (this.activeFilters.radius !== null && 
          mapManager?.userLocation && 
          event.lat && 
          event.lng) {
        const distance = mapManager.getDistanceKm(
          mapManager.userLocation.lat,
          mapManager.userLocation.lng,
          event.lat,
          event.lng
        );
        if (distance > this.activeFilters.radius) {
          continue;
        }
      }

      // FILTER 4: Specific Location
      if (this.activeFilters.location && event.location !== this.activeFilters.location) {
        continue;
      }

      // Passed all filters - include in results
      filtered.push(event);
    }

    return filtered;
  }

  // ========================================
  // PERSISTENCE HELPERS
  // ========================================
  // Export/import for saving to Storage layer
  
  /**
   * Export filter state for persistence
   * Pattern: Plain object (JSON-serializable)
   */
  export() {
    return {
      categories: Array.from(this.activeFilters.categories), // Set → Array [1]
      timeRange: this.activeFilters.timeRange,
      radius: this.activeFilters.radius,
      location: this.activeFilters.location
    };
  }

  /**
   * Restore filter state from saved preferences
   */
  import(state) {
    if (state.categories) {
      this.activeFilters.categories = new Set(state.categories); // Array → Set [1]
    }
    if (state.timeRange) {
      this.activeFilters.timeRange = state.timeRange;
    }
    if (state.radius) {
      this.activeFilters.radius = state.radius;
    }
    if (state.location) {
      this.activeFilters.location = state.location;
    }
  }
}

// ========================================
// REFERENCES & INSPIRATIONS
// ========================================

/**
 * [10] Pipeline Pattern for Filtering
 * Source: Functional Programming concepts (Haskell, Unix pipes)
 * Also: "Eloquent JavaScript" by Marijn Haverbeke (Chapter 5: Higher-Order Functions)
 * https://eloquentjavascript.net/05_higher_order.html
 * 
 * Insight: Each filter acts as a stage in a pipeline. Event passes through all
 * stages or gets eliminated. This is the Unix philosophy applied to data processing:
 * compose small, focused filters. Easier to debug than nested if/else trees.
 * 
 * [11] Early Return / Guard Clauses
 * Source: "Refactoring" by Martin Fowler (1999) - "Replace Nested Conditional with Guard Clauses"
 * https://refactoring.com/catalog/replaceNestedConditionalWithGuardClauses.html
 * 
 * Insight: `continue` is an early return for loops. Reduces nesting, improves
 * readability. Alternative would be deeply nested if-statements. Fowler's book
 * revolutionized how we think about code structure.
 * 
 * [12] for...of Loop (ES6)
 * Source: TC39 ECMAScript 2015 (ES6) Spec
 * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...of
 * 
 * Insight: `for (const x of array)` is cleaner than `for (let i=0; i<array.length; i++)`.
 * No index tracking needed. More readable, less error-prone (off-by-one bugs impossible).
 * 
 * [13] Array.some() for Existence Check
 * Source: Functional programming patterns, popularized by Underscore.js (2009)
 * https://underscorejs.org/#some
 * 
 * Insight: `array.some(predicate)` stops iterating as soon as it finds a match.
 * O(n) worst case but often O(1) in practice. More declarative than for-loop +
 * break. Jeremy Ashkenas (Underscore creator) made FP accessible to JS devs.
 * 
 * [14] Optional Chaining + Nullish Coalescing
 * Source: TC39 Proposal - Optional Chaining (ES2020)
 * https://github.com/tc39/proposal-optional-chaining
 * 
 * Insight: `mapManager?.userLocation` returns undefined if mapManager is null/undefined,
 * avoiding "Cannot read property of null" errors. Replaces verbose checks like
 * `mapManager && mapManager.userLocation`. Massive DX improvement.
 */
