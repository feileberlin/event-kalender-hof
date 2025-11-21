/**
 * Map Manager - Leaflet.js Wrapper
 * 
 * Pattern: Stateful class managing map lifecycle
 * Tech: Leaflet.js (open source, lighter than Google Maps)
 * State: Map instance, markers array, user location
 * Why: Encapsulates all map operations in one place
 */

export class MapManager {
  
  constructor(mapElementId, initialCenter = [50.3195, 11.9173], initialZoom = 13, options = {}) {
    // State
    this.map = null;                    // Leaflet map instance
    this.markers = [];                  // Track markers for cleanup
    this.userLocation = null;           // GPS coordinates if available
    
    // Config
    this.mapElementId = mapElementId;   // DOM element ID
    this.center = initialCenter;        // Default: Hof, Germany
    this.zoom = initialZoom;            // Default zoom level
    
    // Avatar generator (optional, for papercut theme)
    this.avatarGenerator = options.avatarGenerator || null;
    this.organizersData = options.organizersData || {};
    this.venuesData = options.venuesData || {};
    this.usePapercutMarkers = options.usePapercutMarkers || false;
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
   * @param {Object} eventData - Full event data (for papercut avatars)
   * @returns {Marker} Leaflet marker instance
   */
  addMarker(lat, lng, popupContent, iconUrl, eventData = null) {
    if (!this.map) return null;

    let icon = undefined;
    
    // Papercut theme: Generate SVG avatar
    if (this.usePapercutMarkers && this.avatarGenerator && eventData) {
      const organizerData = this.findOrganizerData(eventData);
      const venueData = this.findVenueData(eventData);
      
      const avatarUrl = this.avatarGenerator.generateAvatar(eventData, organizerData, venueData);
      
      icon = L.icon({
        iconUrl: avatarUrl,
        iconSize: [200, 400],
        iconAnchor: [100, 390],       // Bottom center of venue base
        popupAnchor: [0, -390]       // Popup above top layer
      });
    } 
    // Standard theme: Custom icon or default
    else if (iconUrl) {
      icon = L.icon({
        iconUrl,
        iconSize: [32, 32],
        iconAnchor: [16, 32],        // Point of icon that touches the map
        popupAnchor: [0, -32]        // Where popup opens relative to icon
      });
    }

    const marker = L.marker([lat, lng], icon ? { icon } : {})
      .bindPopup(popupContent)
      .addTo(this.map);

    // Track for cleanup
    this.markers.push(marker);
    
    return marker;
  }
  
  /**
   * Find organizer data by name lookup
   */
  findOrganizerData(event) {
    const organizerName = event.organizer || '';
    
    // Try exact match
    if (this.organizersData[organizerName]) {
      return this.organizersData[organizerName];
    }
    
    // Try case-insensitive match
    const lowerName = organizerName.toLowerCase();
    for (const [key, value] of Object.entries(this.organizersData)) {
      if (key.toLowerCase() === lowerName) {
        return value;
      }
    }
    
    return null;
  }
  
  /**
   * Find venue data by name lookup
   */
  findVenueData(event) {
    const venueName = event.location || event.venue || '';
    
    // Try exact match
    if (this.venuesData[venueName]) {
      return this.venuesData[venueName];
    }
    
    // Try case-insensitive match
    const lowerName = venueName.toLowerCase();
    for (const [key, value] of Object.entries(this.venuesData)) {
      if (key.toLowerCase() === lowerName) {
        return value;
      }
    }
    
    return null;
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
   * Haversine formula - Calculate distance between two GPS points [8]
   * @returns {number} Distance in kilometers
   * Use case: Radius filter (show events within X km)
   */
  getDistanceKm(lat1, lng1, lat2, lng2) {
    const R = 6371; // Earth radius in km
    
    // Convert degrees to radians
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLng = (lng2 - lng1) * Math.PI / 180;
    
    // Haversine formula
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLng/2) * Math.sin(dLng/2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); // [9]
    
    return R * c;
  }
}

// ========================================
// REFERENCES & INSPIRATIONS
// ========================================

/**
 * [8] Haversine Formula for Great-Circle Distance
 * Source: R.W. Sinnott, "Virtues of the Haversine" (1984, Sky & Telescope)
 * https://en.wikipedia.org/wiki/Haversine_formula
 * Also: Movable Type Scripts - Calculate distance between lat/long
 * https://www.movable-type.co.uk/scripts/latlong.html
 * 
 * Insight: The Haversine formula (from 1984!) is still the gold standard for
 * calculating distances on a sphere. More accurate than Pythagoras for GPS coords.
 * Accounts for Earth's curvature. For ultra-high precision, use Vincenty formula,
 * but Haversine is accurate enough (<0.5% error) and way simpler. Classic algorithm.
 * 
 * [9] atan2() vs atan()
 * Source: "Numerical Recipes" (Press et al., 1986)
 * Insight: atan2(y, x) handles quadrants correctly, atan(y/x) doesn't. Subtle
 * but crucial for angle calculations. atan2 knows the signs of both arguments,
 * so it can determine which quadrant the angle is in. Old-school numeric wisdom.
 */
