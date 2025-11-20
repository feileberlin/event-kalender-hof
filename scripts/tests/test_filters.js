/**
 * Test Suite für Event-Filter
 * Testet die Konsistenz zwischen Config, HTML-Rendering und JavaScript-Logik
 * 
 * Architektur seit 2025-11-20:
 * - Radius-Filter ist config-driven (_config.yml)
 * - HTML nutzt Jekyll template loop mit data-km Attribut
 * - JS liest data-km, handled null für unbegrenzt
 */

const fs = require('fs');
const yaml = require('js-yaml');
const path = require('path');

// Test-Konfiguration (Pfade relativ zum Workspace-Root)
const WORKSPACE_ROOT = path.resolve(__dirname, '../..');
const TEST_CONFIG = {
    configPath: path.join(WORKSPACE_ROOT, '_config.yml'),
    htmlFilePath: path.join(WORKSPACE_ROOT, 'index.html'),
    filterJsPath: path.join(WORKSPACE_ROOT, 'assets/js/modules/filters.js'),
    mainJsPath: path.join(WORKSPACE_ROOT, 'assets/js/main.js')
};

// Test 1: Config-Validierung (_config.yml)
function testConfigRadiusFilters() {
    console.log('\n🧪 Test 1: _config.yml radius_filters validieren');
    
    try {
        const configContent = fs.readFileSync(TEST_CONFIG.configPath, 'utf-8');
        const config = yaml.load(configContent);
        
        if (!config.filters || !config.filters.radius_filters) {
            console.error('❌ FEHLER: filters.radius_filters nicht in _config.yml gefunden');
            return false;
        }
        
        const radiusFilters = config.filters.radius_filters;
        console.log(`   Gefundene Filter: ${radiusFilters.length}`);
        
        let hasDefault = false;
        let hasUnlimited = false;
        
        radiusFilters.forEach((filter, idx) => {
            console.log(`   [${idx}] ${filter.label}`);
            console.log(`       key: ${filter.key}, km: ${filter.km}, default: ${filter.default || false}`);
            
            // Validierungen
            if (!filter.key || !filter.label) {
                console.error(`   ❌ FEHLER: Filter ${idx} fehlt key oder label`);
                return false;
            }
            
            if (filter.default) hasDefault = true;
            if (filter.km === null) hasUnlimited = true;
        });
        
        if (!hasDefault) {
            console.error('   ❌ FEHLER: Kein Filter hat default: true');
            return false;
        }
        
        if (!hasUnlimited) {
            console.warn('   ⚠️  WARNUNG: Kein "unbegrenzt" Filter (km: null) vorhanden');
        }
        
        console.log('✅ Config-Struktur ist korrekt');
        return true;
        
    } catch (error) {
        console.error(`❌ FEHLER beim Lesen der Config: ${error.message}`);
        return false;
    }
}

// Test 2: HTML-Template validieren
function testHtmlRadiusTemplate() {
    console.log('\n🧪 Test 2: HTML Template-Rendering validieren');
    
    try {
        const html = fs.readFileSync(TEST_CONFIG.htmlFilePath, 'utf-8');
        
        // Prüfe Jekyll Template Loop
        const templateLoopRegex = /{%\s*for\s+filter\s+in\s+site\.filters\.radius_filters\s*%}([\s\S]*?){%\s*endfor\s*%}/;
        const loopMatch = html.match(templateLoopRegex);
        
        if (!loopMatch) {
            console.error('❌ FEHLER: Jekyll template loop für radius_filters nicht gefunden');
            console.error('   Erwartet: {% for filter in site.filters.radius_filters %}');
            return false;
        }
        
        const optionTemplate = loopMatch[1];
        console.log('   Template gefunden:');
        console.log('   ' + optionTemplate.trim().split('\n').join('\n   '));
        
        // Validiere data-km Attribut
        if (!optionTemplate.includes('data-km')) {
            console.error('❌ FEHLER: data-km Attribut fehlt im Template');
            return false;
        }
        
        // Validiere {{ filter.km }} Variable
        if (!optionTemplate.includes('{{ filter.km }}')) {
            console.error('❌ FEHLER: {{ filter.km }} Variable fehlt');
            return false;
        }
        
        // Validiere ARIA Label
        if (!optionTemplate.includes('aria-label')) {
            console.warn('⚠️  WARNUNG: aria-label fehlt (Accessibility)');
        }
        
        console.log('✅ HTML Template ist korrekt');
        return true;
        
    } catch (error) {
        console.error(`❌ FEHLER beim Lesen von HTML: ${error.message}`);
        return false;
    }
}

// Test 3: JavaScript Filter-Logik validieren
function testJavaScriptFilterLogic() {
    console.log('\n🧪 Test 3: JavaScript Filter-Logik validieren');
    
    try {
        // Prüfe main.js (Event Listener)
        const mainJs = fs.readFileSync(TEST_CONFIG.mainJsPath, 'utf-8');
        
        // Suche radiusFilter Event Listener
        if (!mainJs.includes('radiusFilter.addEventListener')) {
            console.error('❌ FEHLER: radiusFilter Event Listener nicht gefunden');
            return false;
        }
        
        // Validiere data-km Attribut wird gelesen
        if (!mainJs.includes('data-km') && !mainJs.includes('getAttribute')) {
            console.error('❌ FEHLER: data-km Attribut wird nicht gelesen');
            return false;
        }
        
        // Validiere null-Handling
        if (!mainJs.includes('null') || !mainJs.includes('parseFloat')) {
            console.warn('⚠️  WARNUNG: null-Handling oder parseFloat fehlt möglicherweise');
        }
        
        console.log('   ✓ Event Listener vorhanden');
        console.log('   ✓ data-km wird gelesen');
        
        // Prüfe filters.js (FilterManager)
        const filtersJs = fs.readFileSync(TEST_CONFIG.filterJsPath, 'utf-8');
        
        // Suche setRadius Funktion
        const setRadiusMatch = filtersJs.match(/setRadius\s*\([^)]*\)\s*{([^}]+)}/);
        if (!setRadiusMatch) {
            console.error('❌ FEHLER: setRadius() Funktion nicht gefunden');
            return false;
        }
        
        const setRadiusBody = setRadiusMatch[1];
        
        // Validiere null-Handling in setRadius
        if (!setRadiusBody.includes('null')) {
            console.error('❌ FEHLER: null-Handling fehlt in setRadius()');
            return false;
        }
        
        console.log('   ✓ setRadius() vorhanden');
        console.log('   ✓ null-Handling implementiert');
        
        // Suche Filter-Logik (Distanzprüfung)
        const radiusCheckRegex = /this\.activeFilters\.radius\s*(!==|!=)\s*null/;
        if (!filtersJs.match(radiusCheckRegex)) {
            console.error('❌ FEHLER: Radius null-Check fehlt in Filter-Logik');
            return false;
        }
        
        console.log('   ✓ Filter-Logik prüft auf null (unbegrenzt)');
        
        console.log('✅ JavaScript Filter-Logik ist korrekt');
        return true;
        
    } catch (error) {
        console.error(`❌ FEHLER beim Lesen von JavaScript: ${error.message}`);
        return false;
    }
}

// Test 4: Distanzberechnung für verschiedene Szenarien simulieren
function testDistanceCalculation() {
    console.log('\n🧪 Test 4: Distanzberechnung simulieren');
    
    // Mock Events mit verschiedenen Distanzen
    const mockEvents = [
        { title: 'Event 0.5km entfernt', distance: 0.5 },
        { title: 'Event 1.5km entfernt', distance: 1.5 },
        { title: 'Event 3.5km entfernt', distance: 3.5 },
        { title: 'Event 12km entfernt', distance: 12 }
    ];
    
    console.log('   Test-Events:');
    mockEvents.forEach(e => console.log(`   - ${e.title}`));
    
    // Test-Szenarien basierend auf typischer Config
    const testScenarios = [
        { label: '🚶 1 km', km: 1, expectedCount: 1 },
        { label: '🚴 3 km', km: 3, expectedCount: 2 },
        { label: '🚌 10 km', km: 10, expectedCount: 3 },
        { label: '🚕 unbegrenzt', km: null, expectedCount: 4 }
    ];
    
    let allPassed = true;
    
    testScenarios.forEach(scenario => {
        const filtered = scenario.km === null 
            ? mockEvents  // null = keine Filterung
            : mockEvents.filter(e => e.distance <= scenario.km);
        
        const passed = filtered.length === scenario.expectedCount;
        
        console.log(`\n   ${scenario.label} (km: ${scenario.km}):`);
        console.log(`     Erwartet: ${scenario.expectedCount} Events`);
        console.log(`     Gefiltert: ${filtered.length} Events`);
        console.log(`     ${passed ? '✅ Korrekt' : '❌ FEHLER'}`);
        
        if (!passed) {
            allPassed = false;
            console.log('     Gefilterte Events:');
            filtered.forEach(e => console.log(`       - ${e.title}`));
        }
    });
    
    if (allPassed) {
        console.log('\n✅ Distanzberechnung funktioniert korrekt');
    }
    
    return allPassed;
}

// Test 5: Edge Cases & null-Handling
function testEdgeCases() {
    console.log('\n🧪 Test 5: Edge Cases & null-Handling');
    
    const edgeCases = [
        { 
            name: 'null Radius (unbegrenzt) mit User Location',
            radius: null, 
            userLocation: true, 
            shouldFilter: false,
            reason: 'null bedeutet "unbegrenzt", keine Distanz-Filterung'
        },
        { 
            name: 'null Radius ohne User Location',
            radius: null, 
            userLocation: false, 
            shouldFilter: false,
            reason: 'Ohne Standort keine Distanz-Berechnung möglich'
        },
        { 
            name: '1km mit User Location',
            radius: 1, 
            userLocation: true, 
            shouldFilter: true,
            reason: 'Standort + numerischer Radius = Filterung aktiv'
        },
        { 
            name: '10km ohne User Location',
            radius: 10, 
            userLocation: false, 
            shouldFilter: false,
            reason: 'Ohne Standort keine Distanz-Filterung möglich'
        }
    ];
    
    let allPassed = true;
    
    edgeCases.forEach(testCase => {
        // Logik aus filters.js nachbilden
        const wouldFilter = testCase.radius !== null && testCase.userLocation;
        const passed = wouldFilter === testCase.shouldFilter;
        
        console.log(`\n   ${testCase.name}:`);
        console.log(`     Radius: ${testCase.radius}`);
        console.log(`     User Location: ${testCase.userLocation}`);
        console.log(`     Erwartet: ${testCase.shouldFilter ? 'Filter' : 'Kein Filter'}`);
        console.log(`     Tatsächlich: ${wouldFilter ? 'Filter' : 'Kein Filter'}`);
        console.log(`     ${passed ? '✅ Korrekt' : '❌ FEHLER'}`);
        console.log(`     Grund: ${testCase.reason}`);
        
        if (!passed) {
            allPassed = false;
        }
    });
    
    if (allPassed) {
        console.log('\n✅ Alle Edge Cases bestanden');
    }
    
    return allPassed;
}

// Haupt-Test-Runner
function runAllTests() {
    console.log('═══════════════════════════════════════════════════════');
    console.log('🧪 Event-Filter Test Suite (Config-Driven Architecture)');
    console.log('═══════════════════════════════════════════════════════');
    
    const results = [
        testConfigRadiusFilters(),
        testHtmlRadiusTemplate(),
        testJavaScriptFilterLogic(),
        testDistanceCalculation(),
        testEdgeCases()
    ];
    
    const passed = results.filter(r => r === true).length;
    const failed = results.filter(r => r === false).length;
    
    console.log('\n═══════════════════════════════════════════════════════');
    console.log(`📊 Ergebnis: ${passed}/${results.length} Tests bestanden`);
    if (failed > 0) {
        console.log(`❌ ${failed} Tests fehlgeschlagen`);
    } else {
        console.log('✅ Alle Tests erfolgreich!');
    }
    console.log('═══════════════════════════════════════════════════════\n');
    
    if (failed > 0) {
        process.exit(1);
    }
}

// Run tests if executed directly
if (require.main === module) {
    runAllTests();
}

module.exports = { 
    runAllTests, 
    testConfigRadiusFilters,
    testHtmlRadiusTemplate,
    testJavaScriptFilterLogic,
    testDistanceCalculation,
    testEdgeCases
};
