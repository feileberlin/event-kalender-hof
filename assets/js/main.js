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

  // 4. EXTRACT CONFIGURED CATEGORIES FROM DOM
  // These are rendered from _config.yml by Jekyll
  const categoryFilter = document.getElementById('categoryFilter');
  if (categoryFilter) {
    const configuredCategories = Array.from(categoryFilter.options)
      .filter(opt => opt.value !== '' && opt.value !== 'Sonstiges')
      .map(opt => opt.value);
    filterManager.setConfiguredCategories(configuredCategories);
    console.log('📋 Configured categories:', configuredCategories);
  }

  // 5. RESTORE USER PREFERENCES
  // Load saved filter settings from previous session
  const savedPrefs = Storage.loadPrefs();
  if (savedPrefs) {
    filterManager.import(savedPrefs);
    applyFiltersToUI();
  }

  // 6. WIRE UP EVENT LISTENERS
  setupEventListeners();

  // 7. INITIAL RENDER
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
  // Pattern: Event delegation (works for dynamically added elements) [18]
  
  document.addEventListener('click', (e) => {
    
    // Toggle bookmark
    if (e.target.matches('.bookmark-btn')) { // [19]
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
  updateCategoryCounts();
}

/**
 * Update category counts in the filter dropdown
 * Shows live count for each category and total
 */
function updateCategoryCounts() {
  const categoryFilter = document.getElementById('categoryFilter');
  if (!categoryFilter) return;

  // Get configured categories from dropdown (these are from _config.yml)
  const configuredCategories = Array.from(categoryFilter.options)
    .filter(opt => opt.value !== '' && opt.value !== 'Sonstiges')
    .map(opt => opt.value);
  
  // Get filtered events
  const filteredEvents = eventManager.events;

  // Count events per category
  const counts = {};
  configuredCategories.forEach(cat => { counts[cat] = 0; });
  counts['Sonstiges'] = 0;

  filteredEvents.forEach(event => {
    let matchedConfiguredCategory = false;
    
    // Check if event matches any configured category
    event.categories.forEach(cat => {
      if (configuredCategories.includes(cat)) {
        counts[cat] = (counts[cat] || 0) + 1;
        matchedConfiguredCategory = true;
      }
    });
    
    // If event doesn't match any configured category, count it as "Sonstiges"
    if (!matchedConfiguredCategory) {
      counts['Sonstiges']++;
    }
  });

  // Helper: Pluralisierung für deutsche Kategorien
  const pluralize = (category, count) => {
    // Try to get singular/plural from data attributes
    const option = Array.from(categoryFilter.options).find(opt => opt.value === category);
    if (option) {
      const singular = option.getAttribute('data-singular');
      const plural = option.getAttribute('data-plural');
      if (singular && plural) {
        return count === 1 ? singular : plural;
      }
    }
    
    // Fallback: return category name
    return category;
  };

  // Update options in select
  Array.from(categoryFilter.options).forEach(option => {
    const cat = option.value;
    const icon = option.getAttribute('data-icon') || '';
    
    if (!cat) {
      // Default: "Events aller Art" (from config) mit Counter voran
      const defaultLabel = option.textContent.trim();
      option.textContent = `${filteredEvents.length} ${icon} ${defaultLabel}`;
    } else {
      // Kategorie-Option: Counter + Plural/Singular (auch wenn Count = 0)
      const count = counts[cat] || 0;
      const label = pluralize(cat, count);
      option.textContent = `${count} ${icon} ${label}`;
    }
  });
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

  // Use mailto: protocol (opens system mail client) [20]
  window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}

// ========================================
// DEVELOPER TOOLS
// ========================================

/**
 * Expose API for browser console debugging [21]
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
 * [18] Event Delegation Pattern
 * Source: David Walsh - "How JavaScript Event Delegation Works" (2012)
 * https://davidwalsh.name/event-delegate
 * Also: jQuery's .on() popularized this pattern (2006-2012)
 * 
 * Insight: Instead of adding listeners to every button, add ONE listener to a
 * parent (document) and check e.target. Works for dynamically added elements.
 * Memory-efficient (one listener vs. thousands). Fundamental DOM pattern that
 * pre-dates modern frameworks. jQuery made this mainstream.
 * 
 * [19] Element.matches() for Selector Checking
 * Source: DOM Living Standard - Element.matches()
 * https://developer.mozilla.org/en-US/docs/Web/API/Element/matches
 * 
 * Insight: Before matches(), we'd use classList.contains() or check IDs manually.
 * matches('.class') or matches('#id') uses CSS selector syntax. Unified API for
 * checking if element matches ANY selector. Elegant DX improvement.
 * 
 * [20] mailto: Protocol for Email Integration
 * Source: RFC 6068 - The 'mailto' URI Scheme (2010)
 * https://www.rfc-editor.org/rfc/rfc6068.html
 * 
 * Insight: No server-side email handling needed. Browser opens user's default
 * mail client. Works on mobile too (opens Gmail/Mail/Outlook app). Zero dependencies
 * for email functionality. Old-school web API that still works perfectly.
 * 
 * [21] Debug API on window Object
 * Source: Pattern from browser DevTools (Chrome DevTools, 2008+)
 * Popularized by libraries like jQuery ($), Lodash (_), moment (moment)
 * 
 * Insight: Exposing module instances on window makes REPL debugging effortless.
 * Type `krawl.events.getStats()` in console and see live data. No breakpoints
 * needed. This is how jQuery ($) became so developer-friendly. Simple but powerful.
 */
