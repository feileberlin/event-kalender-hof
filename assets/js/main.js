/**
 * Krawl Event Calendar - Main Orchestrator
 * 
 * Architecture: Modular design with separated concerns
 * Pattern: Manager instances coordinate module interactions
 * Lifecycle: Load → Init → Listen → React
 * 
 * Modules:
 * - Storage: Persistent data (LocalStorage)
 * - BookmarkManager: User's saved events
 * - MapManager: Leaflet.js map with markers
 * - FilterManager: Multi-criteria event filtering
 * - EventManager: Event data & business logic
 * 
 * Why this structure:
 * - Each module has ONE clear responsibility (Single Responsibility Principle)
 * - Easy to test modules in isolation
 * - Easy to extend (add new filter types, etc.)
 * - No global variables polluting namespace
 */

import { Storage } from './modules/storage.js';
import { BookmarkManager } from './modules/bookmarks.js';
import { MapManager } from './modules/map.js';
import { FilterManager } from './modules/filters.js';
import { EventManager } from './modules/events.js';

// ========================================
// MODULE INSTANCES
// ========================================
// Initialized in DOMContentLoaded

let bookmarkManager;
let mapManager;
let filterManager;
let eventManager;

// ========================================
// APPLICATION LIFECYCLE
// ========================================

/**
 * Main initialization - runs when DOM is ready
 * Lifecycle: Load data → Init UI → Restore state → Listen
 */
document.addEventListener('DOMContentLoaded', async () => {
  console.log('🎪 Krawl initializing...');

  // 1. INSTANTIATE MODULES
  bookmarkManager = new BookmarkManager();
  mapManager = new MapManager('map', [50.3195, 11.9173], 13);
  filterManager = new FilterManager();
  eventManager = new EventManager();

  // 2. LOAD DATA
  // Events are embedded in HTML by Jekyll (static site)
  await eventManager.loadFromDOM();

  // 3. INIT MAP
  mapManager.init();
  mapManager.getUserLocation((location) => {
    console.log('📍 User location:', location);
  });

  // 4. RESTORE USER PREFERENCES
  // Load saved filter settings from previous session
  const savedPrefs = Storage.loadPrefs();
  if (savedPrefs) {
    filterManager.import(savedPrefs);
    applyFiltersToUI();
  }

  // 5. WIRE UP EVENT LISTENERS
  setupEventListeners();

  // 6. INITIAL RENDER
  updateDisplay();

  console.log('✅ Krawl ready!');
});

// ========================================
// EVENT LISTENERS
// ========================================

/**
 * Register all UI event handlers
 * Pattern: Event delegation for dynamic elements
 */
function setupEventListeners() {
  
  // ------ FILTER CONTROLS ------
  
  const categoryFilter = document.getElementById('categoryFilter');
  const timeFilter = document.getElementById('timeFilter');
  const radiusFilter = document.getElementById('radiusFilter');
  const locationSelect = document.getElementById('locationSelect');

  // Category: Multi-select via dropdown
  if (categoryFilter) {
    categoryFilter.addEventListener('change', () => {
      const selected = categoryFilter.value;
      if (selected) {
        filterManager.toggleCategory(selected);
        categoryFilter.value = ''; // Reset dropdown to "Select..."
      }
      updateDisplay();
      savePrefs();
    });
  }

  // Time range: upcoming/past/all
  if (timeFilter) {
    timeFilter.addEventListener('change', () => {
      filterManager.setTimeRange(timeFilter.value);
      updateDisplay();
      savePrefs();
    });
  }

  // Radius: Distance from user location
  if (radiusFilter) {
    radiusFilter.addEventListener('change', () => {
      filterManager.setRadius(radiusFilter.value);
      updateDisplay();
      savePrefs();
    });
  }

  // Location: Specific venue
  if (locationSelect) {
    locationSelect.addEventListener('change', () => {
      filterManager.setLocation(locationSelect.value);
      updateDisplay();
      savePrefs();
    });
  }

  // ------ BOOKMARKS ------
  // Pattern: Event delegation (works for dynamically added elements) [1]
  
  document.addEventListener('click', (e) => {
    
    // Toggle bookmark
    if (e.target.matches('.bookmark-btn')) { // [2]
      const eventUrl = e.target.dataset.eventUrl;
      bookmarkManager.toggle(eventUrl);
      bookmarkManager.updateButton(e.target);
      updateBookmarkCount();
    }

    // Clear all bookmarks
    if (e.target.matches('#clearBookmarksBtn')) {
      if (bookmarkManager.clear()) {
        updateDisplay();
      }
    }

    // Print bookmarks
    if (e.target.matches('#printBookmarksBtn')) {
      printBookmarks();
    }

    // Email bookmarks
    if (e.target.matches('#emailBookmarksBtn')) {
      emailBookmarks();
    }
  });

  // ------ UI TOGGLES ------
  
  // Search panel collapse/expand
  const searchToggle = document.getElementById('searchToggle');
  const searchPanel = document.getElementById('searchPanel');
  if (searchToggle && searchPanel) {
    searchToggle.addEventListener('click', () => {
      searchPanel.classList.toggle('collapsed');
      searchPanel.classList.toggle('expanded');
    });
  }

  // Sidebar collapse/expand
  const sidebarToggle = document.getElementById('sidebarToggle');
  const eventSidebar = document.getElementById('eventSidebar');
  if (sidebarToggle && eventSidebar) {
    sidebarToggle.addEventListener('click', () => {
      eventSidebar.classList.toggle('collapsed');
    });
  }
}

// ========================================
// DISPLAY UPDATE (CORE RENDERING)
// ========================================

/**
 * Re-render entire UI based on current filter state
 * Pattern: Explicit re-render (no virtual DOM - KISS)
 * Triggered by: Filter changes, bookmark actions
 * 
 * Steps:
 * 1. Filter events
 * 2. Show/hide event cards in DOM
 * 3. Update map markers
 * 4. Update bookmark UI
 * 5. Update stats
 */
function updateDisplay() {
  
  // 1. APPLY FILTERS
  const filtered = filterManager.filterEvents(eventManager.allEvents, mapManager);
  eventManager.setFiltered(filtered);

  // 2. SHOW/HIDE EVENT CARDS
  // Direct DOM manipulation (no framework overhead)
  eventManager.allEvents.forEach(event => {
    const isVisible = filtered.includes(event);
    event.element.style.display = isVisible ? 'block' : 'none';
  });

  // 3. UPDATE MAP
  mapManager.clearMarkers();
  filtered.forEach(event => {
    if (event.lat && event.lng) {
      const popup = `<strong>${event.title}</strong><br>${event.date}<br>${event.venue}`;
      mapManager.addMarker(event.lat, event.lng, popup, event.imageUrl);
    }
  });

  // 4. UPDATE BOOKMARK BUTTONS
  document.querySelectorAll('.bookmark-btn').forEach(btn => {
    bookmarkManager.updateButton(btn);
  });

  // 5. UPDATE COUNTERS
  updateBookmarkCount();
  updateStats();
}

// ========================================
// UI HELPERS
// ========================================

/**
 * Apply saved filter state to UI controls
 * Use case: Restore filter dropdowns after page reload
 */
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

/**
 * Update bookmark counter badge
 */
function updateBookmarkCount() {
  const count = bookmarkManager.count();
  const countEl = document.getElementById('bookmarkCount');
  if (countEl) {
    countEl.textContent = count;
  }
}

/**
 * Update event statistics display
 */
function updateStats() {
  const stats = eventManager.getStats();
  console.log('📊 Stats:', stats);
  
  // Optional: Display stats in UI
  const statsEl = document.getElementById('eventStats');
  if (statsEl) {
    statsEl.textContent = `${stats.filtered} of ${stats.total} events`;
  }
}

/**
 * Save current filter state to persistent storage
 */
function savePrefs() {
  Storage.savePrefs(filterManager.export());
}

// ========================================
// BOOKMARK ACTIONS
// ========================================

/**
 * Print bookmarked events
 * Opens print dialog with formatted event list
 */
function printBookmarks() {
  const events = bookmarkManager.getEventData();
  
  if (events.length === 0) {
    alert('No bookmarks yet');
    return;
  }

  // Generate printable HTML in new window
  const printWindow = window.open('', '_blank');
  printWindow.document.write(`
    <html>
    <head>
      <title>My Krawl Bookmarks</title>
      <style>
        body { font-family: sans-serif; margin: 2cm; }
        h1 { font-size: 24px; }
        .event { margin-bottom: 1cm; page-break-inside: avoid; }
        .event h2 { font-size: 18px; margin: 0; }
        .event p { margin: 0.25cm 0; }
      </style>
    </head>
    <body>
      <h1>🎪 My Krawl Bookmarks</h1>
      ${events.map(e => `
        <div class="event">
          <h2>${e.title}</h2>
          <p><strong>Date:</strong> ${e.date}</p>
          <p><strong>Location:</strong> ${e.location}</p>
          <p><a href="${e.url}">${e.url}</a></p>
        </div>
      `).join('')}
    </body>
    </html>
  `);
  printWindow.document.close();
  printWindow.print();
}

/**
 * Email bookmarked events
 * Opens default mail client with formatted event list
 */
function emailBookmarks() {
  const events = bookmarkManager.getEventData();
  
  if (events.length === 0) {
    alert('No bookmarks yet');
    return;
  }

  const subject = 'My Krawl Bookmarks';
  const body = events.map(e => 
    `${e.title}\n${e.date}\n${e.location}\n${e.url}\n`
  ).join('\n---\n\n');

  // Use mailto: protocol (opens system mail client) [3]
  window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}

// ========================================
// DEVELOPER TOOLS
// ========================================

/**
 * Expose API for browser console debugging [4]
 * Usage in console:
 *   krawl.bookmarks.getAll()
 *   krawl.events.getStats()
 *   krawl.refresh()
 */
window.krawl = {
  bookmarks: bookmarkManager,
  map: mapManager,
  filters: filterManager,
  events: eventManager,
  refresh: updateDisplay
};

// ========================================
// REFERENCES & INSPIRATIONS
// ========================================

/**
 * [1] Event delegation pattern
 * Source: JavaScript design patterns, jQuery best practices
 * Reference: https://davidwalsh.name/event-delegate
 * 
 * Why notable: Instead of attaching click handlers to each bookmark button:
 * 
 *   buttons.forEach(btn => btn.addEventListener('click', handler))
 * 
 * We attach ONE handler to document and check e.target. Benefits:
 * - Works for dynamically added elements (no re-binding needed)
 * - Less memory (1 listener instead of N)
 * - Simpler cleanup (no need to remove individual listeners)
 * 
 * This pattern is fundamental to modern SPA frameworks (React uses it internally).
 * Historical note: jQuery popularized this as .on() with delegation parameter.
 */

/**
 * [2] Element.matches() for CSS selector matching
 * Source: DOM Living Standard
 * https://developer.mozilla.org/en-US/docs/Web/API/Element/matches
 * 
 * Why notable: e.target.matches('.bookmark-btn') checks if element matches selector.
 * This is more flexible than className checks:
 * 
 *   // Old way:
 *   if (e.target.className.includes('bookmark-btn')) { ... }
 *   
 *   // New way:
 *   if (e.target.matches('.bookmark-btn')) { ... }
 * 
 * matches() supports full CSS selector syntax (.class, #id, [attr], :pseudo, etc.)
 * and handles multiple classes correctly. Supported since IE9.
 * 
 * Pro tip: For checking parent chain, use e.target.closest('.selector')
 */

/**
 * [3] mailto: protocol for email sharing
 * Source: RFC 6068 - mailto URI Scheme
 * https://tools.ietf.org/html/rfc6068
 * 
 * Why notable: mailto: is a standard way to open default mail client with pre-filled
 * content. No server-side code needed, works offline, respects user's email preference.
 * 
 * Caveats:
 * - Body length limited (~2000 chars on some clients)
 * - Formatting is plain text only
 * - Requires default mail client configured
 * 
 * Alternative approaches (not used):
 * - Web Share API (navigator.share) - better UX but limited support
 * - Server-side email sending - requires backend
 * - Copy to clipboard - less discoverable
 * 
 * For our use case (event list sharing), mailto: is the KISS solution.
 */

/**
 * [4] window namespace for debugging API
 * Source: JavaScript module patterns, browser DevTools best practices
 * 
 * Why notable: In modular code, variables are scoped to modules (not global).
 * This is great for production but annoying for debugging. Solution:
 * 
 *   window.krawl = { ...modules }
 * 
 * Now developers can interact with modules in console:
 * 
 *   > krawl.events.getStats()
 *   { total: 42, filtered: 15, ... }
 *   
 *   > krawl.bookmarks.getAll()
 *   ['event-1', 'event-2']
 *   
 *   > krawl.refresh()  // Force re-render
 * 
 * This is common in libraries (e.g., jQuery as $, lodash as _). For dev experience,
 * exposing a debug API is invaluable. Production builds could strip this via
 * minifier or build flag.
 * 
 * Pro tip: Use Object.freeze(window.krawl) to prevent accidental mutations.
 */
