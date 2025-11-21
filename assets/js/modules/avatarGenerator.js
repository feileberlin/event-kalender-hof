/**
 * Avatar Generator - Layered 3D Staging System
 * 
 * Creates a multi-layered 3D staging system instead of single character markers:
 * Layer 1 (Bottom): Venue/Place base (200x150px)
 * Layer 2 (Middle): Organizer papercut character (120x140px, y-offset: -30px)
 * Layer 3 (Upper): Event start time neon sign (80x40px, y-offset: -60px from Layer 2)
 * Layer 4 (Top): Event details paper (150x100px, y-offset: -40px from Layer 3)
 */

export class AvatarGenerator {
  constructor(themeConfig) {
    this.config = themeConfig?.avatars || this.getDefaultConfig();
    this.characterTypes = this.config.characters || [];
    this.venueScenery = this.config.venue_scenery || {};
    
    // Neon sign colors
    this.neonColors = ['#ff00ff', '#00ffff', '#ff0066', '#00ff00', '#ffff00', '#ff6600'];
    
    // Paper fonts
    this.paperFonts = ['Arial', 'Times New Roman', 'Courier', 'Georgia', 'Verdana', 'Comic Sans MS'];
  }

  getDefaultConfig() {
    return {
      enabled: true,
      style: 'papercut',
      venue_scenery: {
        enabled: true,
        height: 40
      },
      characters: [
        { name: 'punk', hair_style: 'mohawk', hair_color: '#e74c3c', body_color: '#2c3e50' },
        { name: 'loser', hair_style: 'messy', hair_color: '#7f8c8d', body_color: '#ecf0f1' },
        { name: 'hipster', hair_style: 'bun', hair_color: '#8b4513', body_color: '#f5e6d3', glasses: true },
        { name: 'metalhead', hair_style: 'long', hair_color: '#000000', body_color: '#bdc3c7' },
        { name: 'raver', hair_style: 'dreads', hair_color: '#ff00ff', body_color: '#f39c12' },
        { name: 'activist', hair_style: 'short', hair_color: '#2c3e50', body_color: '#95a5a6' }
      ]
    };
  }

  /**
   * Generate layered 3D staging marker for an event
   * @param {Object} event - Event data with title, date, organizer, venue
   * @param {Object} organizerData - Organizer metadata
   * @param {Object} venueData - Venue metadata
   * @returns {string} SVG data URL
   */
  generateAvatar(event, organizerData, venueData) {
    return this.generateLayeredMarker(event, organizerData, venueData);
  }

  /**
   * Main method: Generate layered marker with 4 layers
   */
  generateLayeredMarker(event, organizerData, venueData) {
    const character = this.selectCharacter(event, organizerData);
    const venueIcon = this.getVenueIcon(venueData);
    const neonColor = this.selectNeonColor(event);
    
    const width = 200;
    const height = 400;
    
    // Layer positions (y-coordinates)
    const layer1Y = height - 150; // Venue base at bottom
    const layer2Y = layer1Y - 30;  // Character offset from base
    const layer3Y = layer2Y - 170; // Neon sign offset from character (character is 140px + 30px gap)
    const layer4Y = layer3Y - 40;  // Paper offset from neon sign

    const svg = `
      <svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
        <defs>
          <style>
            .papercut-stroke { stroke: #2c3e50; stroke-width: 2; }
            .papercut-text { font-family: 'Comic Sans MS', cursive; font-weight: bold; fill: #2c3e50; }
            .neon-text { 
              font-family: 'Arial Black', 'Arial', sans-serif; 
              font-weight: bold;
              fill: ${neonColor};
            }
            .paper-texture {
              fill: #fefefe;
            }
          </style>
          <filter id="paper-grain">
            <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" result="noise"/>
            <feDiffuseLighting in="noise" lighting-color="white" surfaceScale="1">
              <feDistantLight azimuth="45" elevation="60"/>
            </feDiffuseLighting>
          </filter>
        </defs>
        
        <!-- Layer 1: Venue/Place Base -->
        ${this.renderVenueBase(venueIcon, width, layer1Y)}
        
        <!-- Layer 2: Organizer Character -->
        <g transform="translate(40, ${layer2Y})">
          ${this.renderOrganizerCharacter(character)}
        </g>
        
        <!-- Layer 3: Event Time Neon Sign -->
        ${this.renderNeonTimeSign(event, neonColor, width, layer3Y)}
        
        <!-- Layer 4: Event Details Paper -->
        ${this.renderEventDetailsPaper(event, width, layer4Y)}
      </svg>
    `;

    // Convert SVG to data URL for Leaflet icon
    const encoded = encodeURIComponent(svg);
    return `data:image/svg+xml,${encoded}`;
  }

  /**
   * Layer 1: Render venue base (stage floor)
   */
  renderVenueBase(venueIcon, width, y) {
    const baseWidth = 200;
    const baseHeight = 150;
    const x = (width - baseWidth) / 2;

    return `
      <g>
        <!-- Venue base rectangle with gradient -->
        <defs>
          <linearGradient id="venueGrad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style="stop-color:${venueIcon.color};stop-opacity:0.3" />
            <stop offset="100%" style="stop-color:${venueIcon.color};stop-opacity:0.6" />
          </linearGradient>
        </defs>
        <rect x="${x}" y="${y}" width="${baseWidth}" height="${baseHeight}" 
              fill="url(#venueGrad)" 
              stroke="${venueIcon.color}" stroke-width="3" rx="10"/>
        
        <!-- Venue icon centered -->
        <text x="${width / 2}" y="${y + baseHeight / 2}" 
              text-anchor="middle" font-size="60" dominant-baseline="middle">
          ${venueIcon.icon}
        </text>
        
        <!-- Stage floor line effect -->
        <line x1="${x + 20}" y1="${y + baseHeight - 20}" x2="${x + baseWidth - 20}" y2="${y + baseHeight - 20}" 
              stroke="${venueIcon.color}" stroke-width="2" stroke-dasharray="5,5" opacity="0.5"/>
      </g>
    `;
  }

  /**
   * Layer 2: Render organizer character (papercut style)
   */
  renderOrganizerCharacter(character) {
    const width = 120;
    const height = 140;

    return `
      <g>
        <!-- Character Body -->
        ${this.renderCharacterBody(character, width, height)}
        
        <!-- Character Head & Hair -->
        ${this.renderCharacterHead(character, width, height)}
        
        <!-- Arms -->
        ${this.renderArms(character, width, height)}
      </g>
    `;
  }

  /**
   * Layer 3: Render neon time sign
   */
  renderNeonTimeSign(event, neonColor, width, y) {
    const startTime = event.start_time || '??:??';
    const signWidth = 80;
    const signHeight = 40;
    const x = (width - signWidth) / 2;

    return `
      <g>
        <!-- Neon sign background (dark) -->
        <rect x="${x}" y="${y}" width="${signWidth}" height="${signHeight}" 
              fill="#1a1a1a" stroke="${neonColor}" stroke-width="2" rx="5"/>
        
        <!-- Neon time text with glow -->
        <text x="${x + signWidth / 2}" y="${y + signHeight / 2 + 8}" 
              text-anchor="middle" font-size="20" class="neon-text"
              style="filter: drop-shadow(0 0 5px ${neonColor}) drop-shadow(0 0 10px ${neonColor}) drop-shadow(0 0 15px ${neonColor});">
          ${startTime}
        </text>
        
        <!-- Corner decorations -->
        <circle cx="${x + 5}" cy="${y + 5}" r="2" fill="${neonColor}" opacity="0.8"/>
        <circle cx="${x + signWidth - 5}" cy="${y + 5}" r="2" fill="${neonColor}" opacity="0.8"/>
        <circle cx="${x + 5}" cy="${y + signHeight - 5}" r="2" fill="${neonColor}" opacity="0.8"/>
        <circle cx="${x + signWidth - 5}" cy="${y + signHeight - 5}" r="2" fill="${neonColor}" opacity="0.8"/>
      </g>
    `;
  }

  /**
   * Layer 4: Render event details paper
   */
  renderEventDetailsPaper(event, width, y) {
    const paperWidth = 150;
    const paperHeight = 100;
    const x = (width - paperWidth) / 2;
    
    const title = this.truncateText(event.title || 'Event', 18);
    const date = this.formatDate(event.date);
    const venue = this.truncateText(event.location || event.venue || '', 15);
    const organizer = this.truncateText(event.organizer || '', 15);

    // Random fonts for each line
    const titleFont = this.paperFonts[this.hashString(event.title || 'a') % this.paperFonts.length];
    const dateFont = this.paperFonts[this.hashString(event.date || 'b') % this.paperFonts.length];
    const venueFont = this.paperFonts[this.hashString(venue || 'c') % this.paperFonts.length];
    const organizerFont = this.paperFonts[this.hashString(organizer || 'd') % this.paperFonts.length];

    // Random font sizes (8-12px)
    const titleSize = 10 + (this.hashString(title) % 3);
    const dateSize = 8 + (this.hashString(date) % 3);
    const venueSize = 8 + (this.hashString(venue) % 3);
    const organizerSize = 8 + (this.hashString(organizer) % 3);

    return `
      <g>
        <!-- Paper background with texture -->
        <rect x="${x}" y="${y}" width="${paperWidth}" height="${paperHeight}" 
              class="paper-texture" 
              stroke="#333" stroke-width="1" rx="2"/>
        
        <!-- Paper fold corner effect -->
        <path d="M${x + paperWidth - 15},${y} L${x + paperWidth},${y} L${x + paperWidth},${y + 15}" 
              fill="#e0e0e0" stroke="#999" stroke-width="0.5"/>
        
        <!-- Event details with varied fonts -->
        <text x="${x + paperWidth / 2}" y="${y + 18}" 
              text-anchor="middle" font-size="${titleSize}" font-family="${titleFont}" 
              font-weight="bold" fill="#000">
          ${title}
        </text>
        
        <text x="${x + 10}" y="${y + 35}" 
              font-size="${dateSize}" font-family="${dateFont}" fill="#333">
          📅 ${date}
        </text>
        
        <text x="${x + 10}" y="${y + 52}" 
              font-size="${venueSize}" font-family="${venueFont}" fill="#333">
          📍 ${venue}
        </text>
        
        <text x="${x + 10}" y="${y + 69}" 
              font-size="${organizerSize}" font-family="${organizerFont}" fill="#333">
          👤 ${organizer}
        </text>
        
        <!-- Separator line -->
        <line x1="${x + 10}" y1="${y + 78}" x2="${x + paperWidth - 10}" y2="${y + 78}" 
              stroke="#ccc" stroke-width="1" stroke-dasharray="2,2"/>
        
        <!-- Bottom detail text -->
        <text x="${x + paperWidth / 2}" y="${y + 92}" 
              text-anchor="middle" font-size="7" font-family="Courier" fill="#666">
          krawl.ist
        </text>
      </g>
    `;
  }

  /**
   * Select character type based on organizer or event category
   */
  selectCharacter(event, organizerData) {
    const organizerName = organizerData?.name || event.organizer || 'default';
    const hash = this.hashString(organizerName);
    const index = hash % this.characterTypes.length;
    
    return this.characterTypes[index] || this.characterTypes[0];
  }

  /**
   * Select neon color for time sign
   */
  selectNeonColor(event) {
    const hash = this.hashString(event.title || 'event');
    return this.neonColors[hash % this.neonColors.length];
  }

  /**
   * Get venue icon/scenery based on venue type
   */
  getVenueIcon(venueData) {
    if (!venueData || !this.venueScenery.enabled) {
      return { icon: '📍', color: '#34495e' };
    }

    const venueType = venueData.icon || '📍';
    const venueColor = venueData.color || '#34495e';

    return { icon: venueType, color: venueColor };
  }



  /**
   * Render character body (torso)
   */
  renderCharacterBody(character, width, height) {
    const bodyColor = character.body_color || '#ecf0f1';
    const shirtColor = character.shirt_color || '#3498db';
    const bodyY = height - 70;

    return `
      <!-- Body/Torso -->
      <rect x="40" y="${bodyY}" width="40" height="50" 
            fill="${shirtColor}" class="papercut-stroke"/>
      <circle cx="50" cy="${bodyY + 15}" r="5" fill="${bodyColor}" class="papercut-stroke"/>
      <circle cx="70" cy="${bodyY + 15}" r="5" fill="${bodyColor}" class="papercut-stroke"/>
    `;
  }



  /**
   * Render character head with hair
   */
  renderCharacterHead(character, width, height) {
    const bodyColor = character.body_color || '#ecf0f1';
    const hairColor = character.hair_color || '#2c3e50';
    const hairStyle = character.hair_style || 'messy';
    const headY = height - 110;

    let hairSVG = '';
    
    switch (hairStyle) {
      case 'mohawk':
        hairSVG = `
          <path d="M50,${headY - 10} L60,${headY - 25} L70,${headY - 10}" 
                fill="${hairColor}" class="papercut-stroke"/>
        `;
        break;
      case 'long':
        hairSVG = `
          <path d="M45,${headY} L40,${headY + 25} M75,${headY} L80,${headY + 25}" 
                stroke="${hairColor}" stroke-width="4" fill="none"/>
        `;
        break;
      case 'bun':
        hairSVG = `
          <circle cx="60" cy="${headY - 5}" r="8" fill="${hairColor}" class="papercut-stroke"/>
        `;
        break;
      case 'dreads':
        hairSVG = `
          <line x1="50" y1="${headY}" x2="48" y2="${headY + 15}" stroke="${hairColor}" stroke-width="3"/>
          <line x1="60" y1="${headY}" x2="60" y2="${headY + 15}" stroke="${hairColor}" stroke-width="3"/>
          <line x1="70" y1="${headY}" x2="72" y2="${headY + 15}" stroke="${hairColor}" stroke-width="3"/>
        `;
        break;
      default: // messy
        hairSVG = `
          <ellipse cx="60" cy="${headY - 5}" rx="18" ry="12" fill="${hairColor}" class="papercut-stroke"/>
        `;
        break;
      case 'short':
        hairSVG = `
          <ellipse cx="60" cy="${headY - 3}" rx="16" ry="8" fill="${hairColor}" class="papercut-stroke"/>
        `;
    }

    return `
      <!-- Hair -->
      ${hairSVG}
      
      <!-- Head -->
      <circle cx="60" cy="${headY + 5}" r="15" fill="${bodyColor}" class="papercut-stroke"/>
      
      <!-- Eyes -->
      <circle cx="55" cy="${headY + 3}" r="2" fill="#2c3e50"/>
      <circle cx="65" cy="${headY + 3}" r="2" fill="#2c3e50"/>
      
      <!-- Mouth -->
      <line x1="55" y1="${headY + 12}" x2="65" y2="${headY + 12}" 
            stroke="#2c3e50" stroke-width="2" stroke-linecap="round"/>
      
      ${character.glasses ? `
        <!-- Glasses -->
        <circle cx="55" cy="${headY + 3}" r="5" fill="none" stroke="#2c3e50" stroke-width="1.5"/>
        <circle cx="65" cy="${headY + 3}" r="5" fill="none" stroke="#2c3e50" stroke-width="1.5"/>
        <line x1="60" y1="${headY + 3}" x2="60" y2="${headY + 3}" stroke="#2c3e50" stroke-width="1.5"/>
      ` : ''}
    `;
  }

  /**
   * Render arms
   */
  renderArms(character, width, height) {
    const bodyColor = character.body_color || '#ecf0f1';
    const armY = height - 90;

    return `
      <!-- Arms -->
      <line x1="42" y1="${armY}" x2="35" y2="${armY + 10}" 
            stroke="${bodyColor}" stroke-width="6" stroke-linecap="round"/>
      <line x1="78" y1="${armY}" x2="85" y2="${armY + 10}" 
            stroke="${bodyColor}" stroke-width="6" stroke-linecap="round"/>
      
      <!-- Hands -->
      <circle cx="35" cy="${armY + 10}" r="4" fill="${bodyColor}" class="papercut-stroke"/>
      <circle cx="85" cy="${armY + 10}" r="4" fill="${bodyColor}" class="papercut-stroke"/>
    `;
  }

  /**
   * Utility: Simple string hash function
   */
  hashString(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash);
  }

  /**
   * Utility: Truncate text with ellipsis
   */
  truncateText(text, maxLength) {
    if (!text) return '';
    return text.length > maxLength ? text.substring(0, maxLength - 1) + '…' : text;
  }

  /**
   * Utility: Format date for display
   */
  formatDate(dateStr) {
    if (!dateStr) return '';
    try {
      const date = new Date(dateStr);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const year = date.getFullYear();
      return `${day}.${month}.${year}`;
    } catch (e) {
      return dateStr;
    }
  }
}
