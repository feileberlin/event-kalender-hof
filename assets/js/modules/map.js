// Map-Modul - Leaflet Integration
export class MapManager {
  constructor(mapElementId, initialCenter = [50.3195, 11.9173], initialZoom = 13) {
    this.map = null;
    this.markers = [];
    this.mapElementId = mapElementId;
    this.center = initialCenter;
    this.zoom = initialZoom;
    this.userLocation = null;
  }

  init() {
    if (!document.getElementById(this.mapElementId)) {
      console.warn('Map element not found');
      return;
    }

    this.map = L.map(this.mapElementId).setView(this.center, this.zoom);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 19
    }).addTo(this.map);

    return this.map;
  }

  clearMarkers() {
    this.markers.forEach(marker => marker.remove());
    this.markers = [];
  }

  addMarker(lat, lng, popupContent, iconUrl) {
    if (!this.map) return null;

    const icon = iconUrl ? L.icon({
      iconUrl,
      iconSize: [32, 32],
      iconAnchor: [16, 32],
      popupAnchor: [0, -32]
    }) : undefined;

    const marker = L.marker([lat, lng], icon ? { icon } : {})
      .bindPopup(popupContent)
      .addTo(this.map);

    this.markers.push(marker);
    return marker;
  }

  setView(lat, lng, zoom) {
    if (this.map) {
      this.map.setView([lat, lng], zoom);
    }
  }

  getUserLocation(callback) {
    if (!navigator.geolocation) {
      console.warn('Geolocation nicht verfügbar');
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

  getDistanceKm(lat1, lng1, lat2, lng2) {
    const R = 6371; // Erdradius in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLng = (lng2 - lng1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLng/2) * Math.sin(dLng/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  }
}
