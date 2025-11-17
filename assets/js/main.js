// Event-Kalender Hauptlogik
let map;
let markers = [];
let userLocation = null;
let filteredEvents = [];

// Initialisierung
document.addEventListener('DOMContentLoaded', function() {
    initMap();
    calculateDawnTime();
    filterAndDisplayEvents();
    setupEventListeners();
});

// Karte initialisieren
function initMap() {
    map = L.map('map').setView([config.defaultCenter.lat, config.defaultCenter.lng], config.defaultZoom);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);
    
    // Rathaus-Marker (Zentrum)
    const rathausIcon = L.divIcon({
        className: 'rathaus-marker',
        html: '<div class="marker-icon">🏛️</div>',
        iconSize: [30, 30]
    });
    
    L.marker([config.defaultCenter.lat, config.defaultCenter.lng], {icon: rathausIcon})
        .addTo(map)
        .bindPopup('<strong>Rathaus Hof an der Saale</strong><br>Zentrum des Kalenders');
}

// Morgendämmerung berechnen
function calculateDawnTime() {
    const now = new Date();
    const tomorrow = new Date(now);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    // Vereinfachte Berechnung für ~6:30 Uhr am nächsten Tag
    const dawn = new Date(tomorrow.getFullYear(), tomorrow.getMonth(), tomorrow.getDate(), 6, 30);
    
    const dawnElement = document.getElementById('dawnTime');
    dawnElement.textContent = `⏰ Morgendämmerung: ${dawn.toLocaleDateString('de-DE')} ${dawn.toLocaleTimeString('de-DE', {hour: '2-digit', minute: '2-digit'})} Uhr`;
    
    return dawn;
}

// Events filtern (nur kommende bis Morgendämmerung)
function getUpcomingEvents() {
    const now = new Date();
    const dawn = calculateDawnTime();
    
    return allEvents.filter(event => {
        const eventDateTime = new Date(`${event.date}T${event.startTime || '00:00'}`);
        return eventDateTime >= now && eventDateTime <= dawn;
    }).sort((a, b) => {
        const dateA = new Date(`${a.date}T${a.startTime || '00:00'}`);
        const dateB = new Date(`${b.date}T${b.startTime || '00:00'}`);
        return dateA - dateB;
    });
}

// Events filtern und anzeigen
function filterAndDisplayEvents() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const categoryFilter = document.getElementById('categoryFilter').value;
    const timeFilter = document.getElementById('timeFilter').value;
    const radiusFilter = parseFloat(document.getElementById('radiusFilter').value);
    
    let events = getUpcomingEvents();
    
    // Suchfilter
    if (searchTerm) {
        events = events.filter(event => 
            event.title.toLowerCase().includes(searchTerm) ||
            event.description.toLowerCase().includes(searchTerm) ||
            event.location.toLowerCase().includes(searchTerm)
        );
    }
    
    // Kategorie-Filter
    if (categoryFilter) {
        events = events.filter(event => event.category === categoryFilter);
    }
    
    // Zeit-Filter
    const now = new Date();
    if (timeFilter === 'today') {
        const endOfDay = new Date(now);
        endOfDay.setHours(23, 59, 59);
        events = events.filter(event => {
            const eventDate = new Date(`${event.date}T${event.startTime || '00:00'}`);
            return eventDate <= endOfDay;
        });
    } else if (timeFilter === 'tomorrow') {
        const tomorrow = new Date(now);
        tomorrow.setDate(tomorrow.getDate() + 1);
        const startOfTomorrow = new Date(tomorrow.getFullYear(), tomorrow.getMonth(), tomorrow.getDate(), 0, 0, 0);
        const endOfTomorrow = new Date(tomorrow.getFullYear(), tomorrow.getMonth(), tomorrow.getDate(), 23, 59, 59);
        events = events.filter(event => {
            const eventDate = new Date(`${event.date}T${event.startTime || '00:00'}`);
            return eventDate >= startOfTomorrow && eventDate <= endOfTomorrow;
        });
    } else if (timeFilter === 'next-hours') {
        const sixHoursLater = new Date(now.getTime() + 6 * 60 * 60 * 1000);
        events = events.filter(event => {
            const eventDate = new Date(`${event.date}T${event.startTime || '00:00'}`);
            return eventDate <= sixHoursLater;
        });
    }
    
    // Radius-Filter (wenn Benutzerstandort vorhanden)
    if (userLocation && radiusFilter < 999) {
        events = events.filter(event => {
            const distance = calculateDistance(
                userLocation.lat, userLocation.lng,
                event.coordinates.lat, event.coordinates.lng
            );
            return distance <= radiusFilter;
        });
    }
    
    filteredEvents = events;
    updateEventCount();
    displayEventsOnMap();
    displayEventList();
}

// Event-Anzahl aktualisieren
function updateEventCount() {
    document.getElementById('eventCount').textContent = `${filteredEvents.length} ${filteredEvents.length === 1 ? 'Event' : 'Events'}`;
}

// Events auf Karte anzeigen
function displayEventsOnMap() {
    // Alte Marker entfernen
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];
    
    // Neue Marker hinzufügen
    filteredEvents.forEach((event, index) => {
        const eventIcon = L.divIcon({
            className: 'event-marker',
            html: `<div class="marker-icon" style="background: ${getCategoryColor(event.category)}">${getCategoryEmoji(event.category)}</div>`,
            iconSize: [35, 35]
        });
        
        const marker = L.marker([event.coordinates.lat, event.coordinates.lng], {icon: eventIcon})
            .addTo(map)
            .bindPopup(`
                <div class="event-popup">
                    <strong>${event.title}</strong><br>
                    <em>${event.category || 'Event'}</em><br>
                    📅 ${new Date(event.date).toLocaleDateString('de-DE')}<br>
                    🕐 ${event.startTime} Uhr<br>
                    📍 ${event.location}<br>
                    <a href="${event.url}" class="popup-link">Details →</a>
                </div>
            `);
        
        marker.on('click', () => highlightEvent(index));
        markers.push(marker);
    });
    
    // Karte an Marker anpassen
    if (markers.length > 0) {
        const group = L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.1));
    }
}

// Event-Liste anzeigen
function displayEventList() {
    const eventList = document.getElementById('eventList');
    
    if (filteredEvents.length === 0) {
        eventList.innerHTML = '<div class="no-events">Keine Events gefunden. 😔</div>';
        return;
    }
    
    eventList.innerHTML = filteredEvents.map((event, index) => `
        <div class="event-card" data-index="${index}" onclick="focusEvent(${index})">
            <div class="event-card-header" style="border-left: 4px solid ${getCategoryColor(event.category)}">
                <h3>${getCategoryEmoji(event.category)} ${event.title}</h3>
                <span class="event-category">${event.category || 'Event'}</span>
            </div>
            <div class="event-card-body">
                <p class="event-datetime">
                    📅 ${new Date(event.date).toLocaleDateString('de-DE', {weekday: 'short', day: '2-digit', month: '2-digit', year: 'numeric'})}
                    &nbsp;|&nbsp;
                    🕐 ${event.startTime}${event.endTime ? ' - ' + event.endTime : ''} Uhr
                </p>
                <p class="event-location">📍 ${event.location}</p>
                <p class="event-description">${event.description || ''}</p>
                ${event.tags && event.tags.length > 0 ? 
                    `<div class="event-tags-inline">${event.tags.map(tag => `<span class="tag-small">${tag}</span>`).join('')}</div>` 
                    : ''}
            </div>
            <div class="event-card-footer">
                <a href="${event.url}" class="btn-small">Details ansehen →</a>
            </div>
        </div>
    `).join('');
}

// Event auf Karte fokussieren
function focusEvent(index) {
    const event = filteredEvents[index];
    map.setView([event.coordinates.lat, event.coordinates.lng], 16);
    markers[index].openPopup();
    highlightEvent(index);
}

// Event in Liste hervorheben
function highlightEvent(index) {
    document.querySelectorAll('.event-card').forEach((card, i) => {
        if (i === index) {
            card.classList.add('highlighted');
            card.scrollIntoView({behavior: 'smooth', block: 'nearest'});
        } else {
            card.classList.remove('highlighted');
        }
    });
}

// Benutzerstandort verwenden
function useUserLocation() {
    if (!navigator.geolocation) {
        alert('Geolocation wird von Ihrem Browser nicht unterstützt.');
        return;
    }
    
    const locationButton = document.getElementById('useLocation');
    locationButton.textContent = '📍 Lade Position...';
    locationButton.disabled = true;
    
    navigator.geolocation.getCurrentPosition(
        (position) => {
            userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            
            // Benutzerpunkt auf Karte
            const userIcon = L.divIcon({
                className: 'user-marker',
                html: '<div class="marker-icon" style="background: #4CAF50">👤</div>',
                iconSize: [30, 30]
            });
            
            L.marker([userLocation.lat, userLocation.lng], {icon: userIcon})
                .addTo(map)
                .bindPopup('<strong>Ihr Standort</strong>')
                .openPopup();
            
            map.setView([userLocation.lat, userLocation.lng], 14);
            locationButton.textContent = '✓ Standort aktiv';
            locationButton.disabled = false;
            locationButton.style.background = '#4CAF50';
            
            filterAndDisplayEvents();
        },
        (error) => {
            let errorMessage = 'Standort konnte nicht ermittelt werden.';
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    errorMessage = 'Standortzugriff wurde verweigert. Bitte erlaube den Zugriff in deinen Browser-Einstellungen.';
                    break;
                case error.POSITION_UNAVAILABLE:
                    errorMessage = 'Standortinformationen sind nicht verfügbar.';
                    break;
                case error.TIMEOUT:
                    errorMessage = 'Zeitüberschreitung bei der Standortabfrage.';
                    break;
            }
            alert(errorMessage);
            locationButton.textContent = '📍 Mein Standort';
            locationButton.disabled = false;
        },
        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }
    );
}

// Distanz berechnen (Haversine-Formel)
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Erdradius in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

// Kategorie-Farbe
function getCategoryColor(category) {
    const colors = {
        'Musik': '#e91e63',
        'Theater': '#9c27b0',
        'Sport': '#2196f3',
        'Kultur': '#ff9800',
        'Markt': '#4caf50',
        'Fest': '#f44336',
        'Sonstiges': '#607d8b'
    };
    return colors[category] || '#757575';
}

// Kategorie-Emoji
function getCategoryEmoji(category) {
    const emojis = {
        'Musik': '🎵',
        'Theater': '🎭',
        'Sport': '⚽',
        'Kultur': '🎨',
        'Markt': '🛒',
        'Fest': '🎉',
        'Sonstiges': '📅'
    };
    return emojis[category] || '📅';
}

// Event-Listener einrichten
function setupEventListeners() {
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const timeFilter = document.getElementById('timeFilter');
    const radiusFilter = document.getElementById('radiusFilter');
    const resetFilters = document.getElementById('resetFilters');
    const useLocation = document.getElementById('useLocation');
    
    if (searchInput) {
        searchInput.addEventListener('input', filterAndDisplayEvents);
    }
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterAndDisplayEvents);
    }
    
    if (timeFilter) {
        timeFilter.addEventListener('change', filterAndDisplayEvents);
    }
    
    if (radiusFilter) {
        radiusFilter.addEventListener('change', filterAndDisplayEvents);
    }
    
    if (resetFilters) {
        resetFilters.addEventListener('click', () => {
            if (searchInput) searchInput.value = '';
            if (categoryFilter) categoryFilter.value = '';
            if (timeFilter) timeFilter.value = 'all';
            if (radiusFilter) radiusFilter.value = '999';
            filterAndDisplayEvents();
        });
    }
    
    if (useLocation) {
        useLocation.addEventListener('click', (e) => {
            e.preventDefault();
            useUserLocation();
        });
    }
    
    console.log('Event-Listener erfolgreich eingerichtet');
}
