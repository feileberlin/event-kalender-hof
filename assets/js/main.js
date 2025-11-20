// Krawl Event-Kalender - Modulare Version
import { Storage } from './modules/storage.js';
import { BookmarkManager } from './modules/bookmarks.js';
import { MapManager } from './modules/map.js';
import { FilterManager } from './modules/filters.js';
import { EventManager } from './modules/events.js';

// Globale Manager-Instanzen
let bookmarkManager;
let mapManager;
let filterManager;
let eventManager;

// DOM Ready
document.addEventListener('DOMContentLoaded', async () => {
  console.log('🎪 Krawl initialisiert...');

  // Manager initialisieren
  bookmarkManager = new BookmarkManager();
  mapManager = new MapManager('map', [50.3195, 11.9173], 13);
  filterManager = new FilterManager();
  eventManager = new EventManager();

  // Events aus DOM laden
  await eventManager.loadFromDOM();

  // Karte initialisieren
  mapManager.init();
  mapManager.getUserLocation((location) => {
    console.log('📍 Standort:', location);
  });

  // Präferenzen laden
  const savedPrefs = Storage.loadPrefs();
  if (savedPrefs) {
    filterManager.import(savedPrefs);
    applyFiltersToUI();
  }

  // Event-Listener registrieren
  setupEventListeners();

  // Initial: Events anzeigen
  updateDisplay();

  console.log('✅ Krawl bereit!');
});

// Event-Listener Setup
function setupEventListeners() {
  // Filter-Events
  const categoryFilter = document.getElementById('categoryFilter');
  const timeFilter = document.getElementById('timeFilter');
  const radiusFilter = document.getElementById('radiusFilter');
  const locationSelect = document.getElementById('locationSelect');

  if (categoryFilter) {
    categoryFilter.addEventListener('change', () => {
      const selected = categoryFilter.value;
      if (selected) {
        filterManager.toggleCategory(selected);
        categoryFilter.value = ''; // Reset dropdown
      }
      updateDisplay();
      savePrefs();
    });
  }

  if (timeFilter) {
    timeFilter.addEventListener('change', () => {
      filterManager.setTimeRange(timeFilter.value);
      updateDisplay();
      savePrefs();
    });
  }

  if (radiusFilter) {
    radiusFilter.addEventListener('change', () => {
      filterManager.setRadius(radiusFilter.value);
      updateDisplay();
      savePrefs();
    });
  }

  if (locationSelect) {
    locationSelect.addEventListener('change', () => {
      filterManager.setLocation(locationSelect.value);
      updateDisplay();
      savePrefs();
    });
  }

  // Bookmark-Events (Event-Delegation)
  document.addEventListener('click', (e) => {
    // Bookmark-Button
    if (e.target.matches('.bookmark-btn')) {
      const eventUrl = e.target.dataset.eventUrl;
      bookmarkManager.toggle(eventUrl);
      bookmarkManager.updateButton(e.target);
      updateBookmarkCount();
    }

    // Bookmark-Actions
    if (e.target.matches('#clearBookmarksBtn')) {
      if (bookmarkManager.clear()) {
        updateDisplay();
      }
    }

    if (e.target.matches('#printBookmarksBtn')) {
      printBookmarks();
    }

    if (e.target.matches('#emailBookmarksBtn')) {
      emailBookmarks();
    }
  });

  // Such-Panel Toggle
  const searchToggle = document.getElementById('searchToggle');
  const searchPanel = document.getElementById('searchPanel');
  if (searchToggle && searchPanel) {
    searchToggle.addEventListener('click', () => {
      searchPanel.classList.toggle('collapsed');
      searchPanel.classList.toggle('expanded');
    });
  }

  // Sidebar Toggle
  const sidebarToggle = document.getElementById('sidebarToggle');
  const eventSidebar = document.getElementById('eventSidebar');
  if (sidebarToggle && eventSidebar) {
    sidebarToggle.addEventListener('click', () => {
      eventSidebar.classList.toggle('collapsed');
    });
  }
}

// Display aktualisieren
function updateDisplay() {
  // Events filtern
  const filtered = filterManager.filterEvents(eventManager.allEvents, mapManager);
  eventManager.setFiltered(filtered);

  // Event-Cards im DOM zeigen/verstecken
  eventManager.allEvents.forEach(event => {
    const isVisible = filtered.includes(event);
    event.element.style.display = isVisible ? 'block' : 'none';
  });

  // Karte aktualisieren
  mapManager.clearMarkers();
  filtered.forEach(event => {
    if (event.lat && event.lng) {
      const popup = `<strong>${event.title}</strong><br>${event.date}<br>${event.venue}`;
      mapManager.addMarker(event.lat, event.lng, popup, event.imageUrl);
    }
  });

  // Bookmark-Buttons aktualisieren
  document.querySelectorAll('.bookmark-btn').forEach(btn => {
    bookmarkManager.updateButton(btn);
  });

  updateBookmarkCount();
  updateStats();
}

// UI-Helper
function applyFiltersToUI() {
  const state = filterManager.export();
  
  if (document.getElementById('timeFilter')) {
    document.getElementById('timeFilter').value = state.timeRange;
  }
  if (document.getElementById('radiusFilter')) {
    document.getElementById('radiusFilter').value = state.radius;
  }
  if (document.getElementById('locationSelect') && state.location) {
    document.getElementById('locationSelect').value = state.location;
  }
}

function updateBookmarkCount() {
  const count = bookmarkManager.count();
  const countEl = document.getElementById('bookmarkCount');
  if (countEl) {
    countEl.textContent = count;
  }
}

function updateStats() {
  const stats = eventManager.getStats();
  console.log('📊 Stats:', stats);
  
  // Optional: Stats im UI anzeigen
  const statsEl = document.getElementById('eventStats');
  if (statsEl) {
    statsEl.textContent = `${stats.filtered} von ${stats.total} Events`;
  }
}

function savePrefs() {
  Storage.savePrefs(filterManager.export());
}

// Bookmark-Actions
function printBookmarks() {
  const events = bookmarkManager.getEventData();
  if (events.length === 0) {
    alert('Keine Bookmarks vorhanden');
    return;
  }

  const printWindow = window.open('', '_blank');
  printWindow.document.write(`
    <html>
    <head>
      <title>Meine Krawl-Bookmarks</title>
      <style>
        body { font-family: sans-serif; margin: 2cm; }
        h1 { font-size: 24px; }
        .event { margin-bottom: 1cm; page-break-inside: avoid; }
        .event h2 { font-size: 18px; margin: 0; }
        .event p { margin: 0.25cm 0; }
      </style>
    </head>
    <body>
      <h1>🎪 Meine Krawl-Bookmarks</h1>
      ${events.map(e => `
        <div class="event">
          <h2>${e.title}</h2>
          <p><strong>Datum:</strong> ${e.date}</p>
          <p><strong>Ort:</strong> ${e.location}</p>
          <p><a href="${e.url}">${e.url}</a></p>
        </div>
      `).join('')}
    </body>
    </html>
  `);
  printWindow.document.close();
  printWindow.print();
}

function emailBookmarks() {
  const events = bookmarkManager.getEventData();
  if (events.length === 0) {
    alert('Keine Bookmarks vorhanden');
    return;
  }

  const subject = 'Meine Krawl-Bookmarks';
  const body = events.map(e => 
    `${e.title}\n${e.date}\n${e.location}\n${e.url}\n`
  ).join('\n---\n\n');

  window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}

// Export für Debugging
window.krawl = {
  bookmarks: bookmarkManager,
  map: mapManager,
  filters: filterManager,
  events: eventManager,
  refresh: updateDisplay
};
