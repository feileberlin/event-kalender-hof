/**
 * Map Manager - Leaflet.js Wrapper
 * 
 * Pattern: Stateful class managing map lifecycle
 * Tech: Leaflet.js (open source, lighter than Google Maps)
 * State: Map instance, markers array, user location
 * Why: Encapsulates all map operations in one place
 */

export class MapManager {
  
  constructor(mapElementId, initialCenter = [50.3195, 11.9173], initialZoom = 13) {
    // State
    this.map = null;                    // Leaflet map instance
    this.markers = [];                  // Track markers for cleanup
    this.userLocation = null;           // GPS coordinates if available
    
    // Config
    this.mapElementId = mapElementId;   // DOM element ID
    this.center = initialCenter;        // Default: Hof, Germany
    this.zoom = initialZoom;            // Default zoom level
  }

  // ========================================
  // LIFECYCLE
  // ========================================
  
  /**
   * Initialize map with OpenStreetMap tiles
   * Pattern: Lazy initialization (only when needed)
   */
  init() {
    const element = document.getElementById(this.mapElementId);
    
    if (!element) {
      console.warn('Map element not found');
      return;
    }

    // Create Leaflet map instance
    this.map = L.map(this.mapElementId).setView(this.center, this.zoom);
    
    // Add OpenStreetMap tile layer (free, open source)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 19
    }).addTo(this.map);

    return this.map;
  }

  // ========================================
  // MARKER MANAGEMENT
  // ========================================
  
  /**
   * Remove all markers from map
   * Use case: Before re-rendering filtered events
   */
  clearMarkers() {
    this.markers.forEach(marker => marker.remove());
    this.markers = [];
  }

  /**
   * Add event marker to map
   * @param {string} iconUrl - Optional custom marker icon
   * @returns {Marker} Leaflet marker instance
   */
  addMarker(lat, lng, popupContent, iconUrl) {
    if (!this.map) return null;

    // Custom icon or default pin
    const icon = iconUrl ? L.icon({
      iconUrl,
      iconSize: [32, 32],
      iconAnchor: [16, 32],        // Point of icon that touches the map
      popupAnchor: [0, -32]        // Where popup opens relative to icon
    }) : undefined;

    const marker = L.marker([lat, lng], icon ? { icon } : {})
      .bindPopup(popupContent)
      .addTo(this.map);

    // Track for cleanup
    this.markers.push(marker);
    
    return marker;
  }

  // ========================================
  // VIEW CONTROL
  // ========================================
  
  setView(lat, lng, zoom) {
    if (this.map) {
      this.map.setView([lat, lng], zoom);
    }
  }

  // ========================================
  // GEOLOCATION
  // ========================================
  
  /**
   * Get user's GPS location
   * Pattern: Callback-based (async operation)
   * Browser API: navigator.geolocation
   */
  getUserLocation(callback) {
    if (!navigator.geolocation) {
      console.warn('Geolocation not available');
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        this.userLocation = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        if (callback) callback(this.userLocation);
      },
      (error) => {
        console.warn('Geolocation error:', error);
      }
    );
  }

  // ========================================
  // DISTANCE CALCULATION
  // ========================================
  
  /**
   * Haversine formula - Calculate distance between two GPS points [1]
   * @returns {number} Distance in kilometers
   * Use case: Radius filter (show events within X km)
   */
  getDistanceKm(lat1, lng1, lat2, lng2) {
    const R = 6371; // Earth radius in km
    
    // Convert degrees to radians
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLng = (lng2 - lng1) * Math.PI / 180;
    
    // Haversine formula [1]
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLng/2) * Math.sin(dLng/2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    
    return R * c;
  }
}

// ========================================
// REFERENCES & INSPIRATIONS
// ========================================

/**
 * [1] Haversine formula for great-circle distance
 * Source: Movable Type Scripts - Calculate distance between lat/lng points
 * https://www.movable-type.co.uk/scripts/latlong.html
 * 
 * Why notable: This is the standard algorithm for calculating distance on a sphere.
 * The implementation is remarkably elegant - just a few trig operations to account
 * for Earth's curvature. The formula dates back to 1805 (Joseph de Mendoza y Ríos)
 * but remains the best balance of accuracy vs. complexity for most use cases.
 * 
 * Accuracy: ±0.5% error for most distances (good enough for "events within 5km")
 * Performance: ~100-200 ops/ms on modern browsers (plenty fast for our use case)
 * 
 * Alternative approaches (not used):
 * - Vincenty formula: More accurate (±0.5mm) but 10x slower and overkill
 * - Equirectangular approximation: Faster but only works for small distances
 * - Turf.js library: 40KB for one function - not KISS
 * 
 * Fun fact: Named after "haversine" (half-versed-sine), an obscure trig function
 * from the pre-calculator era when lookup tables were used for navigation.
 */
