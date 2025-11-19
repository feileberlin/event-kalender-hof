// Event-Kalender Hauptlogik
let map;
let markers = [];
let userLocation = null;
let filteredEvents = [];
let lastSelectedLocation = 'rathaus'; // Track für Browser-Standort Refresh

// Standort-Definitionen
const LOCATIONS = {
    rathaus: { lat: 50.3197, lng: 11.9168, name: 'Rathaus Hof' },
    bahnhof: { lat: 50.3132, lng: 11.9196, name: 'Hauptbahnhof Hof' }
};

// Cookie-Verwaltung
const COOKIE_NAME = 'eventKalenderPrefs';
const COOKIE_DAYS = 365;

function savePrefsToCookie() {
    const prefs = {
        category: document.getElementById('categoryFilter')?.value || '',
        time: document.getElementById('timeFilter')?.value || 'sunrise',
        radius: document.getElementById('radiusFilter')?.value || '3',
        location: document.getElementById('locationSelect')?.value || 'rathaus'
    };
    
    const expires = new Date();
    expires.setTime(expires.getTime() + (COOKIE_DAYS * 24 * 60 * 60 * 1000));
    document.cookie = `${COOKIE_NAME}=${JSON.stringify(prefs)}; expires=${expires.toUTCString()}; path=/; SameSite=Lax`;
    console.log('Präferenzen gespeichert:', prefs);
}

function loadPrefsFromCookie() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === COOKIE_NAME) {
            try {
                const prefs = JSON.parse(decodeURIComponent(value));
                console.log('Präferenzen geladen:', prefs);
                return prefs;
            } catch (e) {
                console.error('Fehler beim Laden der Präferenzen:', e);
            }
        }
    }
    return null;
}

function applyPrefs(prefs) {
    if (!prefs) return;
    
    const categoryFilter = document.getElementById('categoryFilter');
    const timeFilter = document.getElementById('timeFilter');
    const radiusFilter = document.getElementById('radiusFilter');
    const locationSelect = document.getElementById('locationSelect');
    
    if (categoryFilter && prefs.category !== undefined) {
        categoryFilter.value = prefs.category;
    }
    if (timeFilter && prefs.time) {
        timeFilter.value = prefs.time;
    }
    if (radiusFilter && prefs.radius) {
        radiusFilter.value = prefs.radius;
    }
    if (locationSelect && prefs.location) {
        locationSelect.value = prefs.location;
    }
    
    console.log('Präferenzen angewendet');
}

// Initialisierung
document.addEventListener('DOMContentLoaded', function() {
    console.log('Event-Kalender initialisiert');
    console.log('Anzahl aller Events:', allEvents.length);
    console.log('Events:', allEvents);

    // Präferenzen aus Cookie laden
    const savedPrefs = loadPrefsFromCookie();

    initMap();
    calculateDawnTime();

    // Warten bis Karte geladen ist, dann Events anzeigen
    setTimeout(() => {
        // Präferenzen anwenden BEVOR Filter setup
        if (savedPrefs) {
            applyPrefs(savedPrefs);
        }
        
        setupEventListeners();
        
        // Standort setzen (nach Event Listeners!)
        const locationSelect = document.getElementById('locationSelect');
        if (locationSelect) {
            setLocation(locationSelect.value);
        }
        
        filterAndDisplayEvents();
    }, 200);
});

// Karte initialisieren
function initMap() {
    console.log('Initialisiere Karte...');

    // Prüfen, ob das Karten-Element existiert
    const mapElement = document.getElementById('map');
    if (!mapElement) {
        console.error('Karten-Element nicht gefunden!');
        return;
    }

    try {
        map = L.map('map', {
            zoomControl: false,
            attributionControl: false
        }).setView([config.defaultCenter.lat, config.defaultCenter.lng], config.defaultZoom);

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

        // Rathaus-Marker (immer sichtbar)
        const rathausMarker = L.marker([config.defaultCenter.lat, config.defaultCenter.lng], {icon: rathausIcon})
            .addTo(map)
            .bindPopup('<strong>Rathaus Hof an der Saale</strong><br>Zentrum des Kalenders');

        // Öffne Popup standardmäßig wenn keine Events
        if (allEvents.length === 0) {
            rathausMarker.openPopup();
        }

        console.log('Karte erfolgreich initialisiert');

        // Karte nach kurzer Verzögerung neu laden (für korrekte Tile-Darstellung)
        setTimeout(() => {
            map.invalidateSize();
            console.log('Kartengröße aktualisiert');
        }, 100);
    } catch (error) {
        console.error('Fehler beim Initialisieren der Karte:', error);
    }
}

// Umkreis-Änderung mit Zoom synchronisieren (Einweg: Radius → Zoom)
function syncZoomWithRadius() {
    if (!map) return;
    
    const radiusFilter = document.getElementById('radiusFilter');
    if (!radiusFilter) return;
    
    const radius = radiusFilter.value;
    const currentZoom = map.getZoom();
    
    // Radius zu Zoom-Level Mapping:
    let targetZoom;
    if (radius === '1') {
        targetZoom = 16;
    } else if (radius === '3') {
        targetZoom = 14; // DEFAULT
    } else if (radius === '10') {
        targetZoom = 12;
    } else {
        targetZoom = 9; // Unbegrenzt: Zeige ~60 km Zoom
    }
    
    // Nur zoomen wenn deutlicher Unterschied
    if (Math.abs(currentZoom - targetZoom) >= 1) {
        const center = userLocation || config.defaultCenter;
        map.setView([center.lat, center.lng], targetZoom, {
            animate: true,
            duration: 0.5
        });
        console.log(`Radius ${radius} km → Zoom ${targetZoom}`);
    }
}

// Morgendämmerung berechnen
function calculateDawnTime() {
    const now = new Date();
    let dawnDate = new Date(now);

    // Wenn es nach 6:30 Uhr ist, nimm morgen früh 6:30
    // Wenn es vor 6:30 Uhr ist, nimm heute 6:30
    if (now.getHours() >= 6 && now.getMinutes() >= 30) {
        dawnDate.setDate(dawnDate.getDate() + 1);
    }

    dawnDate.setHours(6, 30, 0, 0);

    return dawnDate;
}

// Events filtern (nur kommende, Zeitfilter wird in filterAndDisplayEvents angewendet)
function getUpcomingEvents() {
    const now = new Date();

    console.log('Jetzt:', now);

    const upcomingEvents = allEvents.filter(event => {
        const eventDateTime = new Date(`${event.date}T${event.startTime || '00:00'}`);
        console.log(`Event: ${event.title}, Zeit: ${eventDateTime}, Kommend: ${eventDateTime >= now}`);
        return eventDateTime >= now;
    }).sort((a, b) => {
        const dateA = new Date(`${a.date}T${a.startTime || '00:00'}`);
        const dateB = new Date(`${b.date}T${b.startTime || '00:00'}`);
        return dateA - dateB;
    });

    console.log('Gefilterte Events:', upcomingEvents.length);
    return upcomingEvents;
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
    if (timeFilter === 'sunrise') {
        // Bis Sonnenaufgang (6:30 Uhr nächster Tag oder heute wenn vor 6:30)
        const dawn = calculateDawnTime();
        events = events.filter(event => {
            const eventDate = new Date(`${event.date}T${event.startTime || '00:00'}`);
            return eventDate <= dawn;
        });
    } else if (timeFilter === 'tatort') {
        // Bis zum Tatort (Sonntag 20:15 Uhr)
        const tatortTime = new Date(now);
        // Finde nächsten Sonntag
        const daysUntilSunday = (7 - tatortTime.getDay()) % 7;
        if (daysUntilSunday === 0 && (tatortTime.getHours() > 20 || (tatortTime.getHours() === 20 && tatortTime.getMinutes() >= 15))) {
            // Wenn heute Sonntag nach 20:15, nimm nächsten Sonntag
            tatortTime.setDate(tatortTime.getDate() + 7);
        } else if (daysUntilSunday > 0) {
            tatortTime.setDate(tatortTime.getDate() + daysUntilSunday);
        }
        tatortTime.setHours(20, 15, 0, 0);
        events = events.filter(event => {
            const eventDate = new Date(`${event.date}T${event.startTime || '00:00'}`);
            return eventDate <= tatortTime;
        });
    }
    // 'all' = kein Zeitfilter

    // Radius-Filter (nur wenn Benutzerstandort vorhanden UND Filter nicht "Alle" oder "Taxi")
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
    displayEventsOnMap();
    displayEventList();
    updateCategoryFilterDisplay();
}

// Kategorie-Filter mit Event-Counts aktualisieren
function updateCategoryFilterDisplay() {
    const categoryFilter = document.getElementById('categoryFilter');
    if (!categoryFilter) return;
    
    const selectedCategory = categoryFilter.value;
    const upcomingEvents = getUpcomingEvents();
    
    // Counts pro Kategorie berechnen
    const categoryCounts = {
        '': upcomingEvents.length,
        'Musik': 0,
        'Theater': 0,
        'Sport': 0,
        'Kultur': 0,
        'Markt': 0,
        'Fest': 0,
        'Sonstiges': 0
    };
    
    // Aktuell gefilterte Events nach Radius/Zeit zählen
    const radiusFilter = document.getElementById('radiusFilter');
    const timeFilter = document.getElementById('timeFilter');
    const radius = radiusFilter ? radiusFilter.value : '3';
    const timeValue = timeFilter ? timeFilter.value : 'sunrise';
    
    upcomingEvents.forEach(event => {
        // Radius-Filter anwenden
        if (userLocation && radius !== '999999') {
            const distance = calculateDistance(
                userLocation.lat, userLocation.lng,
                event.coordinates.lat, event.coordinates.lng
            );
            if (distance > parseFloat(radius)) return;
        }
        
        // Zeit-Filter anwenden
        const eventDateTime = new Date(`${event.date}T${event.startTime || '00:00'}`);
        if (timeValue === 'sunrise') {
            const dawnTime = calculateDawnTime();
            if (eventDateTime > dawnTime) return;
        } else if (timeValue === 'tatort') {
            const tatortTime = new Date();
            tatortTime.setHours(20, 15, 0, 0);
            if (eventDateTime > tatortTime) return;
        }
        
        // Count für spezifische Kategorie erhöhen
        if (event.category && categoryCounts.hasOwnProperty(event.category)) {
            categoryCounts[event.category]++;
        }
    });
    
    // "Alle Kategorien" Count = Summe aller gefilterten Events
    categoryCounts[''] = Object.values(categoryCounts).reduce((sum, count, index) => {
        // Ersten Wert (alte '') überspringen
        return index === 0 ? 0 : sum + count;
    }, 0);
    
    // Options aktualisieren
    Array.from(categoryFilter.options).forEach(option => {
        const category = option.value;
        const icon = option.getAttribute('data-icon') || '';
        const count = categoryCounts[category] || 0;
        
        if (category === selectedCategory) {
            // Aktuell ausgewählte Kategorie - zeige im Footer
            if (category === '') {
                option.textContent = `${count} Events in allen Kategorien`;
            } else {
                const eventWord = count === 1 ? 'Event' : 'Events';
                option.textContent = `${count} ${icon}${category}-${eventWord}`;
            }
        } else {
            // Andere Kategorien - zeige im Dropdown mit Count
            if (category === '') {
                option.textContent = `${count} Events in allen Kategorien`;
            } else {
                option.textContent = `${count} ${icon} ${category}`;
            }
        }
    });
}

// Events auf Karte anzeigen
function displayEventsOnMap() {
    if (!map) {
        console.error('Karte noch nicht initialisiert');
        return;
    }

    console.log('Zeige', filteredEvents.length, 'Events auf Karte');

    // Alte Marker entfernen
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];

    // Neue Marker hinzufügen
    filteredEvents.forEach((event, index) => {
        console.log(`Marker für Event: ${event.title} bei [${event.coordinates.lat}, ${event.coordinates.lng}]`);

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

    // Karte an Marker anpassen oder auf Standard-Zentrum setzen
    if (markers.length > 0) {
        const group = L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.1));
        console.log('Karte an', markers.length, 'Marker angepasst');
    } else {
        // Wenn keine Marker, zeige Standard-Ansicht
        map.setView([config.defaultCenter.lat, config.defaultCenter.lng], config.defaultZoom);
        console.log('Keine Marker - Standard-Ansicht');
    }
}

// Event-Liste anzeigen
function displayEventList() {
    const eventList = document.getElementById('eventList');

    console.log('Anzeige von', filteredEvents.length, 'Events');

    // Loading Spinner ausblenden
    const loadingSpinner = document.getElementById('loadingSpinner');
    if (loadingSpinner) {
        loadingSpinner.style.display = 'none';
    }

    if (filteredEvents.length === 0) {
        eventList.innerHTML = '<div class="no-events">Keine Events gefunden. 😔<br><small>Tipp: Ändere den Zeitfilter oder prüfe ob Events für die kommenden Stunden eingetragen sind.</small></div>';
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
function setLocation(locationType) {
    console.log('Setze Standort:', locationType);
    
    // Browser-Standort
    if (locationType === 'browser') {
        if (!navigator.geolocation) {
            alert('Geolocation wird von Ihrem Browser nicht unterstützt.');
            return;
        }
        
        const locationSelect = document.getElementById('locationSelect');
        locationSelect.disabled = true;

        
        navigator.geolocation.getCurrentPosition(
            (position) => {
                userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                console.log('Browser-Standort ermittelt:', userLocation);

                // Entferne alten Standort-Marker
                markers.forEach(marker => {
                    if (marker.options.className === 'user-location-marker') {
                        map.removeLayer(marker);
                    }
                });

            // Benutzerpunkt auf Karte
            const userIcon = L.divIcon({
                className: 'user-location-marker',
                html: '<div class="marker-icon" style="background: #4CAF50; box-shadow: 0 0 10px rgba(76, 175, 80, 0.8);">👤</div>',
                iconSize: [30, 30]
            });

            const userMarker = L.marker([userLocation.lat, userLocation.lng], {icon: userIcon})
                .addTo(map)
                .bindPopup('<strong>📍 Dein Standort</strong>')
                .openPopup();

                // Karte zentrieren
                map.setView([userLocation.lat, userLocation.lng], 14);

                // Select wieder aktivieren
                locationSelect.disabled = false;
                lastSelectedLocation = 'browser';

                // Radius-Filter automatisch auf 3 km setzen, wenn unbegrenzt
                const radiusFilterElement = document.getElementById('radiusFilter');
                if (radiusFilterElement && radiusFilterElement.value === '999999') {
                    radiusFilterElement.value = '3';
                    console.log('Radius-Filter automatisch auf 3 km gesetzt');
                }

                // Events neu filtern und anzeigen
                filterAndDisplayEvents();

                console.log('Browser-Standort aktiv');
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
                locationSelect.disabled = false;
                // Fallback zu Rathaus
                locationSelect.value = 'rathaus';
                setLocation('rathaus');
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
        return;
    }
    
    // Rathaus oder Bahnhof
    const location = LOCATIONS[locationType];
    if (!location) {
        console.error('Unbekannter Standort:', locationType);
        return;
    }
    
    userLocation = {
        lat: location.lat,
        lng: location.lng
    };
    
    console.log(`Standort gesetzt: ${location.name}`, userLocation);
    
    // Entferne alten Standort-Marker
    markers.forEach(marker => {
        if (marker.options.className === 'user-location-marker') {
            map.removeLayer(marker);
        }
    });
    
    // Marker für feste Standorte
    const icon = locationType === 'rathaus' ? '🏛️' : '🚂';
    const locationIcon = L.divIcon({
        className: 'user-location-marker',
        html: `<div class="marker-icon" style="background: #2c3e50;">${icon}</div>`,
        iconSize: [30, 30]
    });
    
    const locationMarker = L.marker([userLocation.lat, userLocation.lng], {icon: locationIcon})
        .addTo(map)
        .bindPopup(`<strong>${location.name}</strong>`)
        .openPopup();
    
    // Karte zentrieren
    map.setView([userLocation.lat, userLocation.lng], 14);
    
    // Radius-Filter automatisch auf 3 km setzen, wenn unbegrenzt
    const radiusFilterElement = document.getElementById('radiusFilter');
    if (radiusFilterElement && radiusFilterElement.value === '999999') {
        radiusFilterElement.value = '3';
    }
    
    // Events neu filtern
    filterAndDisplayEvents();
    lastSelectedLocation = locationType;
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
    const useLocation = document.getElementById('useLocation');
    const searchToggle = document.getElementById('searchToggle');
    const searchPanel = document.getElementById('searchPanel');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const eventSidebar = document.getElementById('eventSidebar');

    if (searchInput) {
        searchInput.addEventListener('input', filterAndDisplayEvents);
    }

    if (categoryFilter) {
        categoryFilter.addEventListener('change', () => {
            filterAndDisplayEvents();
            savePrefsToCookie();
        });
    }

    if (timeFilter) {
        timeFilter.addEventListener('change', () => {
            filterAndDisplayEvents();
            savePrefsToCookie();
        });
    }

    if (radiusFilter) {
        radiusFilter.addEventListener('change', () => {
            syncZoomWithRadius();
            filterAndDisplayEvents();
            savePrefsToCookie();
        });
    }

    // Standort-Select
    const locationSelect = document.getElementById('locationSelect');
    if (locationSelect) {
        locationSelect.addEventListener('change', (e) => {
            const selectedLocation = e.target.value;
            
            // Wenn "Mein Standort" erneut gewählt wird, Standort neu abfragen
            if (selectedLocation === 'browser' && lastSelectedLocation === 'browser') {
                console.log('Standort wird neu abgefragt...');
            }
            
            setLocation(selectedLocation);
            savePrefsToCookie();
        });
        
        // Initial: NICHT setzen, wird in DOMContentLoaded gemacht
    }

    // Such-Toggle
    if (searchToggle && searchPanel) {
        searchToggle.addEventListener('click', () => {
            searchPanel.classList.toggle('collapsed');
            searchPanel.classList.toggle('expanded');
            if (searchPanel.classList.contains('expanded')) {
                searchInput.focus();
            }
        });
    }

    // Sidebar-Toggle
    if (sidebarToggle && eventSidebar) {
        sidebarToggle.addEventListener('click', () => {
            eventSidebar.classList.toggle('collapsed');
        });
    }

    console.log('Event-Listener erfolgreich eingerichtet');
}
