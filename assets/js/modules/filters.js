// Filter-Modul - Event-Filterung
export class FilterManager {
  constructor() {
    this.activeFilters = {
      categories: new Set(),
      timeRange: 'upcoming',
      radius: 5,
      location: null
    };
  }

  // Category Filter
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

  // Time Filter
  setTimeRange(range) {
    this.activeFilters.timeRange = range;
  }

  getTimeRange() {
    return this.activeFilters.timeRange;
  }

  // Radius Filter
  setRadius(radius) {
    this.activeFilters.radius = parseFloat(radius);
  }

  getRadius() {
    return this.activeFilters.radius;
  }

  // Location Filter
  setLocation(location) {
    this.activeFilters.location = location;
  }

  getLocation() {
    return this.activeFilters.location;
  }

  // Event filtern (Haupt-Logik)
  filterEvents(events, mapManager) {
    const now = new Date();
    const filtered = [];

    for (const event of events) {
      // Category Filter
      if (this.activeFilters.categories.size > 0) {
        const eventCategories = event.categories || [];
        const hasMatch = eventCategories.some(cat => 
          this.activeFilters.categories.has(cat)
        );
        if (!hasMatch) continue;
      }

      // Time Filter
      const eventDate = new Date(event.date);
      if (this.activeFilters.timeRange === 'upcoming' && eventDate < now) {
        continue;
      } else if (this.activeFilters.timeRange === 'past' && eventDate >= now) {
        continue;
      }

      // Radius Filter (wenn userLocation vorhanden)
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

      // Location Filter
      if (this.activeFilters.location && event.location !== this.activeFilters.location) {
        continue;
      }

      filtered.push(event);
    }

    return filtered;
  }

  // State exportieren (für Prefs)
  export() {
    return {
      categories: Array.from(this.activeFilters.categories),
      timeRange: this.activeFilters.timeRange,
      radius: this.activeFilters.radius,
      location: this.activeFilters.location
    };
  }

  // State importieren (von Prefs)
  import(state) {
    if (state.categories) {
      this.activeFilters.categories = new Set(state.categories);
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
