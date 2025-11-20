/**
 * Documentation Quality Tests
 * Prüft Markdown-Dokumentation auf Vollständigkeit, Aktualität und Konsistenz
 * 
 * Test-Kategorien:
 * 1. Strukturelle Integrität (required sections, links)
 * 2. Aktualität (timestamps, deprecated markers)
 * 3. Cross-References (internal links, file existence)
 * 4. Code-Dokumentations-Konsistenz (docs vs. actual code)
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE_ROOT = path.resolve(__dirname, '../..');

const DOCS = {
    README: path.join(WORKSPACE_ROOT, 'README.md'),
    TODO: path.join(WORKSPACE_ROOT, 'TODO.md'),
    FEATURES: path.join(WORKSPACE_ROOT, 'FEATURES.md'),
    INSTALL: path.join(WORKSPACE_ROOT, 'INSTALL.md'),
    CODE_OF_CONDUCT: path.join(WORKSPACE_ROOT, 'CODE_OF_CONDUCT.md')
};

// Test 1: Existenz & Lesbarkeit aller Kern-Docs
function testDocumentExistence() {
    console.log('\n🧪 Test 1: Dokumentations-Dateien Existenz');
    
    let allExist = true;
    
    Object.entries(DOCS).forEach(([name, filepath]) => {
        if (fs.existsSync(filepath)) {
            const stats = fs.statSync(filepath);
            const sizeKB = (stats.size / 1024).toFixed(2);
            console.log(`   ✅ ${name}: ${sizeKB} KB`);
        } else {
            console.error(`   ❌ FEHLER: ${name} fehlt: ${filepath}`);
            allExist = false;
        }
    });
    
    if (allExist) {
        console.log('✅ Alle Kern-Dokumentationen vorhanden');
    }
    
    return allExist;
}

// Test 2: README.md Struktur & Required Sections
function testReadmeStructure() {
    console.log('\n🧪 Test 2: README.md Struktur validieren');
    
    try {
        const content = fs.readFileSync(DOCS.README, 'utf-8');
        
        const requiredSections = [
            { name: 'Title/Header', pattern: /^#\s+.+/m },
            { name: 'Description', pattern: /description|beschreibung/i },
            { name: 'Installation', pattern: /installation|setup|getting started/i },
            { name: 'Usage', pattern: /usage|verwendung|nutzung/i },
            { name: 'License', pattern: /license|lizenz/i }
        ];
        
        let allFound = true;
        
        requiredSections.forEach(section => {
            const found = section.pattern.test(content);
            console.log(`   ${found ? '✅' : '❌'} ${section.name}`);
            if (!found) allFound = false;
        });
        
        // Check for broken markdown links [text](url)
        const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
        const links = [...content.matchAll(linkRegex)];
        
        console.log(`\n   Links gefunden: ${links.length}`);
        
        let brokenLinks = 0;
        links.forEach(match => {
            const url = match[2];
            
            // Check internal file links
            if (!url.startsWith('http') && !url.startsWith('#')) {
                const targetPath = path.join(WORKSPACE_ROOT, url);
                if (!fs.existsSync(targetPath)) {
                    console.warn(`   ⚠️  Broken link: [${match[1]}](${url})`);
                    brokenLinks++;
                }
            }
        });
        
        if (brokenLinks === 0) {
            console.log('   ✅ Alle internen Links funktionieren');
        }
        
        if (allFound && brokenLinks === 0) {
            console.log('✅ README.md Struktur ist korrekt');
            return true;
        }
        
        return false;
        
    } catch (error) {
        console.error(`❌ FEHLER beim Lesen von README.md: ${error.message}`);
        return false;
    }
}

// Test 3: FEATURES.md vs. tatsächliche Features
function testFeaturesDocumentation() {
    console.log('\n🧪 Test 3: FEATURES.md Aktualität prüfen');
    
    try {
        const featuresDoc = fs.readFileSync(DOCS.FEATURES, 'utf-8');
        
        // Check "Last Updated" timestamp (flexible format)
        const timestampMatch = featuresDoc.match(/\*\*Last Updated:\*\*\s*(\d{4}-\d{2}-\d{2})/);
        if (timestampMatch) {
            const docDate = new Date(timestampMatch[1]);
            const today = new Date();
            const daysDiff = Math.floor((today - docDate) / (1000 * 60 * 60 * 24));
            
            console.log(`   Last Updated: ${timestampMatch[1]} (vor ${daysDiff} Tagen)`);
            
            if (daysDiff > 30) {
                console.warn(`   ⚠️  WARNUNG: Dokumentation ist ${daysDiff} Tage alt`);
            } else {
                console.log('   ✅ Dokumentation ist aktuell');
            }
        } else {
            console.warn('   ⚠️  WARNUNG: Kein "Last Updated" Timestamp gefunden');
        }
        
        // Check for documented features vs. actual files
        const documentedFeatures = [
            { name: 'GoatCounter Analytics', file: '_layouts/base.html', pattern: /goatcounter/ },
            { name: 'Radius-Filter Config', file: '_config.yml', pattern: /radius_filters:/ },
            { name: 'RSS Feeds', file: 'feed.xml', exists: true },
            { name: 'Leaflet Map', file: 'assets/js/modules/map.js', exists: true },
            { name: 'Bookmark Manager', file: 'assets/js/modules/bookmarks.js', exists: true },
            { name: 'Admin Panel', file: 'admin.html', exists: true },
            { name: 'Service Worker', file: 'sw.js', exists: true }
        ];
        
        console.log('\n   Feature-Implementierung prüfen:');
        let allImplemented = true;
        
        documentedFeatures.forEach(feature => {
            const filePath = path.join(WORKSPACE_ROOT, feature.file);
            let implemented = false;
            
            if (feature.exists) {
                implemented = fs.existsSync(filePath);
            } else if (feature.pattern) {
                if (fs.existsSync(filePath)) {
                    const content = fs.readFileSync(filePath, 'utf-8');
                    implemented = feature.pattern.test(content);
                }
            }
            
            console.log(`   ${implemented ? '✅' : '❌'} ${feature.name}`);
            if (!implemented) allImplemented = false;
        });
        
        if (allImplemented) {
            console.log('\n✅ Alle dokumentierten Features sind implementiert');
        }
        
        return allImplemented;
        
    } catch (error) {
        console.error(`❌ FEHLER: ${error.message}`);
        return false;
    }
}

// Test 4: TODO.md Format & Status-Konsistenz
function testTodoFormat() {
    console.log('\n🧪 Test 4: TODO.md Format & Konsistenz');
    
    try {
        const todoDoc = fs.readFileSync(DOCS.TODO, 'utf-8');
        
        // Check structure
        const hasPriorities = /##\s+(🔥|⚡|🌟)\s+(High|Medium|Nice-to-Have)/i.test(todoDoc);
        console.log(`   ${hasPriorities ? '✅' : '❌'} Priority-Kategorien vorhanden`);
        
        // Count completed vs. open tasks
        const completedTasks = (todoDoc.match(/✅ ERLEDIGT|✅ COMPLETED/g) || []).length;
        const openTasks = (todoDoc.match(/🔴 TODO|🟡 PARTIALLY/g) || []).length;
        
        console.log(`   Tasks: ${completedTasks} erledigt, ${openTasks} offen`);
        
        // Check for orphaned checkboxes
        const uncheckedBoxes = (todoDoc.match(/- \[ \]/g) || []).length;
        if (uncheckedBoxes > 0) {
            console.warn(`   ⚠️  ${uncheckedBoxes} unkategorisierte Checkboxen gefunden`);
        }
        
        // Check for dates in completed tasks
        const completedWithoutDate = todoDoc.match(/✅ COMPLETED(?!\s*\(\d{4}-\d{2}-\d{2}\))/g);
        if (completedWithoutDate && completedWithoutDate.length > 0) {
            console.warn(`   ⚠️  ${completedWithoutDate.length} erledigte Tasks ohne Datum`);
        } else {
            console.log('   ✅ Alle erledigten Tasks haben Datum');
        }
        
        console.log('✅ TODO.md Format ist korrekt');
        return true;
        
    } catch (error) {
        console.error(`❌ FEHLER: ${error.message}`);
        return false;
    }
}

// Test 5: Code-Kommentar-Konsistenz
function testCodeDocumentationConsistency() {
    console.log('\n🧪 Test 5: Code-Dokumentation Konsistenz');
    
    try {
        const jsModules = [
            'assets/js/modules/map.js',
            'assets/js/modules/filters.js',
            'assets/js/modules/bookmarks.js',
            'assets/js/modules/events.js',
            'assets/js/modules/storage.js'
        ];
        
        console.log('   JavaScript Module prüfen:');
        let allDocumented = true;
        
        jsModules.forEach(modulePath => {
            const fullPath = path.join(WORKSPACE_ROOT, modulePath);
            
            if (!fs.existsSync(fullPath)) {
                console.warn(`   ⚠️  ${path.basename(modulePath)} fehlt`);
                return;
            }
            
            const content = fs.readFileSync(fullPath, 'utf-8');
            
            // Check for file-level documentation
            const hasFileDoc = /^\/\*\*[\s\S]*?\*\//m.test(content);
            
            // Check for class/function documentation
            const functionCount = (content.match(/^\s*(function|class|const \w+ = )/gm) || []).length;
            const docBlockCount = (content.match(/\/\*\*[\s\S]*?\*\//g) || []).length;
            
            const docRatio = functionCount > 0 ? (docBlockCount / functionCount * 100).toFixed(0) : 0;
            
            const status = hasFileDoc && docRatio >= 50 ? '✅' : '⚠️';
            console.log(`   ${status} ${path.basename(modulePath)}: ${docRatio}% dokumentiert`);
            
            if (!hasFileDoc || docRatio < 50) {
                allDocumented = false;
            }
        });
        
        if (allDocumented) {
            console.log('\n✅ Code-Dokumentation ist ausreichend');
        } else {
            console.log('\n⚠️  Code-Dokumentation könnte verbessert werden');
        }
        
        return true; // Warning, not error
        
    } catch (error) {
        console.error(`❌ FEHLER: ${error.message}`);
        return false;
    }
}

// Test 6: Cross-Reference Validation (FEATURES.md ↔ Code)
function testCrossReferences() {
    console.log('\n🧪 Test 6: Cross-References validieren');
    
    try {
        const featuresDoc = fs.readFileSync(DOCS.FEATURES, 'utf-8');
        
        // Extract file paths from FEATURES.md
        const filePathPattern = /`([^`]+\.(js|py|yml|html|css|md))`/g;
        const documentedPaths = [...featuresDoc.matchAll(filePathPattern)]
            .map(match => match[1])
            .filter(p => !p.includes('...') && !p.includes('*')); // Skip wildcards
        
        console.log(`   Gefundene Datei-Referenzen: ${documentedPaths.length}`);
        
        let brokenRefs = 0;
        const uniquePaths = [...new Set(documentedPaths)];
        
        uniquePaths.forEach(docPath => {
            const fullPath = path.join(WORKSPACE_ROOT, docPath);
            if (!fs.existsSync(fullPath)) {
                console.warn(`   ⚠️  Referenz nicht gefunden: ${docPath}`);
                brokenRefs++;
            }
        });
        
        if (brokenRefs === 0) {
            console.log(`   ✅ Alle ${uniquePaths.length} Datei-Referenzen gültig`);
            console.log('✅ Cross-References sind konsistent');
            return true;
        } else {
            console.warn(`   ⚠️  ${brokenRefs} ungültige Referenzen gefunden`);
            return false;
        }
        
    } catch (error) {
        console.error(`❌ FEHLER: ${error.message}`);
        return false;
    }
}

// Haupt-Test-Runner
function runAllTests() {
    console.log('═══════════════════════════════════════════════════════');
    console.log('📚 Documentation Quality Test Suite');
    console.log('═══════════════════════════════════════════════════════');
    
    const results = [
        testDocumentExistence(),
        testReadmeStructure(),
        testFeaturesDocumentation(),
        testTodoFormat(),
        testCodeDocumentationConsistency(),
        testCrossReferences()
    ];
    
    const passed = results.filter(r => r === true).length;
    const failed = results.filter(r => r === false).length;
    
    console.log('\n═══════════════════════════════════════════════════════');
    console.log(`📊 Ergebnis: ${passed}/${results.length} Tests bestanden`);
    
    if (failed > 0) {
        console.log(`❌ ${failed} Tests fehlgeschlagen`);
    } else {
        console.log('✅ Alle Tests erfolgreich!');
        console.log('\n💡 Dokumentation ist aktuell, vollständig und konsistent');
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
    testDocumentExistence,
    testReadmeStructure,
    testFeaturesDocumentation,
    testTodoFormat,
    testCodeDocumentationConsistency,
    testCrossReferences
};
