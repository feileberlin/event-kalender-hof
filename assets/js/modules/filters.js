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
   * Pattern: Pipeline - each filter eliminates non-matching events
   * Performance: Early return (continue) avoids checking remaining filters
   * 
   * @param {Array} events - All available events
   * @param {MapManager} mapManager - Needed for distance calculation
   * @returns {Array} Filtered events
   */
  filterEvents(events, mapManager) {
    const now = new Date();
    const filtered = [];

    for (const event of events) {
      
      // FILTER 1: Categories (if any selected)
      if (this.activeFilters.categories.size > 0) {
        const eventCategories = event.categories || [];
        const hasMatch = eventCategories.some(cat => 
          this.activeFilters.categories.has(cat)
        );
        if (!hasMatch) continue; // Skip to next event
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
      if (mapManager?.userLocation && event.lat && event.lng) {
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
      categories: Array.from(this.activeFilters.categories), // Set → Array
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
      this.activeFilters.categories = new Set(state.categories); // Array → Set
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
