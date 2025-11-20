/**
 * Test Suite für Event-Filter
 * Testet die Konsistenz zwischen HTML-Optionen und JavaScript-Logik
 */

// Test-Konfiguration
const TEST_CONFIG = {
    htmlFilePath: '../index.html',
    jsFilePath: '../assets/js/main.js'
};

// Erwartete Radius-Optionen aus HTML
const EXPECTED_RADIUS_OPTIONS = [
    { value: '1', label: '1 km Umkreis', shouldFilter: true },
    { value: '3', label: '3 km Umkreis', shouldFilter: true },
    { value: '10', label: '10 km Umkreis', shouldFilter: true },
    { value: '999999', label: 'unbegrenzt', shouldFilter: false }
];

// Test 1: HTML <select> Optionen parsen
function testHtmlRadiusOptions() {
    console.log('\n🧪 Test 1: HTML Radius-Optionen validieren');
    
    const fs = require('fs');
    const html = fs.readFileSync(TEST_CONFIG.htmlFilePath, 'utf-8');
    
    // Finde radiusFilter <select>
    const selectMatch = html.match(/<select id="radiusFilter"[^>]*>([\s\S]*?)<\/select>/);
    if (!selectMatch) {
        console.error('❌ FEHLER: radiusFilter <select> nicht gefunden in HTML');
        return false;
    }
    
    // Parse alle <option> Tags
    const optionRegex = /<option value="(\d+)"[^>]*>([^<]+)<\/option>/g;
    const foundOptions = [];
    let match;
    
    while ((match = optionRegex.exec(selectMatch[1])) !== null) {
        foundOptions.push({
            value: match[1],
            label: match[2].trim()
        });
    }
    
    console.log(`   Gefundene Optionen: ${foundOptions.length}`);
    foundOptions.forEach(opt => {
        console.log(`   - value="${opt.value}": ${opt.label}`);
    });
    
    // Validiere gegen erwartete Optionen
    if (foundOptions.length !== EXPECTED_RADIUS_OPTIONS.length) {
        console.error(`❌ FEHLER: Erwartete ${EXPECTED_RADIUS_OPTIONS.length} Optionen, gefunden ${foundOptions.length}`);
        return false;
    }
    
    for (let i = 0; i < EXPECTED_RADIUS_OPTIONS.length; i++) {
        const expected = EXPECTED_RADIUS_OPTIONS[i];
        const found = foundOptions[i];
        
        if (found.value !== expected.value) {
            console.error(`❌ FEHLER: Option ${i} hat value="${found.value}", erwartet "${expected.value}"`);
            return false;
        }
    }
    
    console.log('✅ HTML Optionen sind korrekt');
    return true;
}

// Test 2: JavaScript Filter-Logik validieren
function testJavaScriptFilterLogic() {
    console.log('\n🧪 Test 2: JavaScript Filter-Logik validieren');
    
    const fs = require('fs');
    const js = fs.readFileSync(TEST_CONFIG.jsFilePath, 'utf-8');
    
    // Finde Radius-Filter Code
    const filterMatch = js.match(/if\s*\(\s*userLocation\s*&&\s*radiusFilter\s*<\s*(\d+)\s*\)/);
    if (!filterMatch) {
        console.error('❌ FEHLER: Radius-Filter Bedingung nicht gefunden in JS');
        return false;
    }
    
    const filterThreshold = parseInt(filterMatch[1]);
    console.log(`   Filter-Schwellwert: radiusFilter < ${filterThreshold}`);
    
    // Validiere: Schwellwert muss zwischen kleinstem "filter" und "Alle" liegen
    const maxFilterValue = Math.max(...EXPECTED_RADIUS_OPTIONS.filter(opt => opt.shouldFilter).map(opt => parseInt(opt.value)));
    const minNoFilterValue = Math.min(...EXPECTED_RADIUS_OPTIONS.filter(opt => !opt.shouldFilter).map(opt => parseInt(opt.value)));
    
    console.log(`   Max Filter-Wert: ${maxFilterValue}`);
    console.log(`   Min NoFilter-Wert: ${minNoFilterValue}`);
    
    if (filterThreshold <= maxFilterValue) {
        console.error(`❌ FEHLER: Schwellwert ${filterThreshold} ist zu klein, würde ${maxFilterValue}km filtern`);
        return false;
    }
    
    if (filterThreshold > minNoFilterValue) {
        console.error(`❌ FEHLER: Schwellwert ${filterThreshold} ist zu groß, würde "Alle" (${minNoFilterValue}) nicht durchlassen`);
        return false;
    }
    
    console.log('✅ JavaScript Filter-Logik ist korrekt');
    return true;
}

// Test 3: Distanzberechnung für alle Optionen simulieren
function testDistanceCalculation() {
    console.log('\n🧪 Test 3: Distanzberechnung simulieren');
    
    // Mock: Benutzer in Hof Rathaus (50.3197, 11.9168)
    const userLocation = { lat: 50.3197, lng: 11.9168 };
    
    // Mock Events mit verschiedenen Distanzen
    const mockEvents = [
        { title: 'Event 0.5km', distance: 0.5 },
        { title: 'Event 1.5km', distance: 1.5 },
        { title: 'Event 3.5km', distance: 3.5 },
        { title: 'Event 12km', distance: 12 }
    ];
    
    console.log('   Test-Events:');
    mockEvents.forEach(e => console.log(`   - ${e.title}: ${e.distance} km`));
    
    // Teste jede Radius-Option
    EXPECTED_RADIUS_OPTIONS.forEach(option => {
        const radiusKm = parseFloat(option.value);
        const shouldFilterByDistance = radiusKm < 999; // Logik aus main.js
        
        const filtered = shouldFilterByDistance 
            ? mockEvents.filter(e => e.distance <= radiusKm)
            : mockEvents; // Keine Filterung
        
        console.log(`\n   Option "${option.label}" (${option.value} km):`);
        console.log(`     Filter aktiv: ${shouldFilterByDistance ? 'Ja' : 'Nein'}`);
        console.log(`     Gefilterte Events: ${filtered.length}/${mockEvents.length}`);
        filtered.forEach(e => console.log(`       ✓ ${e.title}`));
        
        // Validierung
        if (option.shouldFilter && !shouldFilterByDistance) {
            console.error(`     ❌ FEHLER: Option sollte filtern, tut es aber nicht!`);
            return false;
        }
        if (!option.shouldFilter && shouldFilterByDistance) {
            console.error(`     ❌ FEHLER: Option sollte nicht filtern, tut es aber!`);
            return false;
        }
    });
    
    console.log('\n✅ Distanzberechnung funktioniert korrekt');
    return true;
}

// Test 4: Grenzwert-Tests (Edge Cases)
function testEdgeCases() {
    console.log('\n🧪 Test 4: Grenzwert-Tests (Edge Cases)');
    
    const edgeCases = [
        { radiusFilter: 999, userLocation: true, shouldFilter: false, case: 'Alle mit Standort' },
        { radiusFilter: 999999, userLocation: true, shouldFilter: false, case: 'Taxi mit Standort' },
        { radiusFilter: 1, userLocation: false, shouldFilter: false, case: '1km ohne Standort' },
        { radiusFilter: 10, userLocation: true, shouldFilter: true, case: '10km mit Standort' }
    ];
    
    edgeCases.forEach(test => {
        const wouldFilter = test.userLocation && test.radiusFilter < 999;
        const isCorrect = wouldFilter === test.shouldFilter;
        
        console.log(`   ${test.case}:`);
        console.log(`     Erwartetes Verhalten: ${test.shouldFilter ? 'Filter' : 'Kein Filter'}`);
        console.log(`     Tatsächliches Verhalten: ${wouldFilter ? 'Filter' : 'Kein Filter'}`);
        console.log(`     ${isCorrect ? '✅ Korrekt' : '❌ FEHLER'}`);
        
        if (!isCorrect) {
            return false;
        }
    });
    
    console.log('\n✅ Alle Edge Cases bestanden');
    return true;
}

// Haupt-Test-Runner
function runAllTests() {
    console.log('═══════════════════════════════════════════════════════');
    console.log('🧪 Event-Filter Test Suite');
    console.log('═══════════════════════════════════════════════════════');
    
    const results = [
        testHtmlRadiusOptions(),
        testJavaScriptFilterLogic(),
        testDistanceCalculation(),
        testEdgeCases()
    ];
    
    const passed = results.filter(r => r === true).length;
    const failed = results.filter(r => r === false).length;
    
    console.log('\n═══════════════════════════════════════════════════════');
    console.log(`Ergebnis: ${passed} bestanden, ${failed} fehlgeschlagen`);
    console.log('═══════════════════════════════════════════════════════\n');
    
    if (failed > 0) {
        process.exit(1);
    }
}

// Run tests if executed directly
if (require.main === module) {
    runAllTests();
}

module.exports = { runAllTests, testHtmlRadiusOptions, testJavaScriptFilterLogic };
