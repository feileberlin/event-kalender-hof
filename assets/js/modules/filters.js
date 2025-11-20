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
      timeRange: 'upcoming',      // 'upcoming', 'past', or 'all'
      radius: 5,                  // Distance in km from user location
      location: null              // Specific venue filter
    };
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

  // ========================================
  // RADIUS FILTER
  // ========================================
  // Only applies if user location is available
  
  setRadius(radius) {
    this.activeFilters.radius = parseFloat(radius);
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
        const hasMatch = eventCategories.some(cat => // [13]
          this.activeFilters.categories.has(cat)
        );
        if (!hasMatch) continue; // Skip to next event [11]
      }

      // FILTER 2: Time Range
      const eventDate = new Date(event.date);
      
      if (this.activeFilters.timeRange === 'upcoming' && eventDate < now) {
        continue;
      } else if (this.activeFilters.timeRange === 'past' && eventDate >= now) {
        continue;
      }
      // 'all' = no time filtering

      // FILTER 3: Radius (GPS distance)
      // Only applies if user shared their location
      if (mapManager?.userLocation && event.lat && event.lng) { // [14]
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
