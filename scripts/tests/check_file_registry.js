#!/usr/bin/env node
/**
 * File Registry Validator
 * Prüft, ob alle Dateien im Repo in FILE_REGISTRY.md dokumentiert sind
 * 
 * Usage: node check_file_registry.js
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE_ROOT = path.resolve(__dirname, '../..');
const REGISTRY_FILE = path.join(WORKSPACE_ROOT, 'FILE_REGISTRY.md');

// Directories/Files to ignore (nie dokumentieren)
const IGNORE_PATTERNS = [
    /^\.git\//,
    /^_site\//,
    /^node_modules\//,
    /^\.jekyll-cache\//,
    /^\.sass-cache\//,
    /^__pycache__\//,
    /\.pyc$/,
    /^\.DS_Store$/,
    /^\.env$/,
    /package-lock\.json$/,
    /Gemfile\.lock$/,
    /^\.vscode\//,
    /^\.devcontainer\//
];

// Rekursiv alle Files sammeln
function getAllFiles(dirPath, arrayOfFiles = []) {
    const files = fs.readdirSync(dirPath);

    files.forEach(file => {
        const fullPath = path.join(dirPath, file);
        const relativePath = path.relative(WORKSPACE_ROOT, fullPath);

        // Skip ignored patterns
        if (IGNORE_PATTERNS.some(pattern => pattern.test(relativePath))) {
            return;
        }

        if (fs.statSync(fullPath).isDirectory()) {
            arrayOfFiles = getAllFiles(fullPath, arrayOfFiles);
        } else {
            arrayOfFiles.push(relativePath);
        }
    });

    return arrayOfFiles;
}

// Parse FILE_REGISTRY.md für dokumentierte Dateien
function getDocumentedFiles() {
    if (!fs.existsSync(REGISTRY_FILE)) {
        console.error('❌ FILE_REGISTRY.md fehlt!');
        process.exit(1);
    }

    const content = fs.readFileSync(REGISTRY_FILE, 'utf-8');
    const documented = new Set();

    // Extract file paths from code blocks and inline code
    const codeBlockRegex = /```[\s\S]*?```/g;
    const inlineCodeRegex = /`([^`]+\.(md|html|js|py|css|csv|json|yml|yaml|txt|xml))`/g;
    
    // Extract from code blocks
    const codeBlocks = content.match(codeBlockRegex) || [];
    codeBlocks.forEach(block => {
        const lines = block.split('\n');
        lines.forEach(line => {
            // Match file paths (including dotfiles, with or without extension)
            const fileMatch = line.match(/^(\.\/)?\.?[\w\.\/-]+(\.(md|html|js|py|css|csv|json|yml|yaml|txt|xml|svg|ico))?/);
            if (fileMatch && fileMatch[0].length > 2 && !fileMatch[0].startsWith('..')) {
                let filepath = fileMatch[0]
                    .replace(/^\.\//, '')  // Remove leading ./
                    .replace(/\s+#.*$/, ''); // Remove trailing comments
                
                if (filepath && filepath !== '.' && filepath !== '..') {
                    documented.add(filepath);
                }
            }
            
            // Match directory paths with files
            const dirMatch = line.match(/^(\.?[\w\.\/-]+\/)/);
            if (dirMatch) {
                let dirpath = dirMatch[1].replace(/^\.\//, '');
                if (dirpath && dirpath !== './' && dirpath !== '../') {
                    documented.add(dirpath);
                }
            }
        });
    });

    // Extract from inline code
    let match;
    while ((match = inlineCodeRegex.exec(content)) !== null) {
        documented.add(match[1]);
    }

    return documented;
}

// Main validation
function validateRegistry() {
    console.log('═══════════════════════════════════════════════════════');
    console.log('📦 File Registry Validator');
    console.log('═══════════════════════════════════════════════════════\n');

    const allFiles = getAllFiles(WORKSPACE_ROOT);
    const documented = getDocumentedFiles();

    console.log(`📁 Gefundene Dateien: ${allFiles.length}`);
    console.log(`📝 Dokumentierte Einträge: ${documented.size}\n`);

    // Check for undocumented files
    const undocumented = [];
    
    allFiles.forEach(file => {
        const isDocumented = 
            documented.has(file) || // Exact match
            Array.from(documented).some(doc => {
                // Check if file is in documented directory
                if (doc.endsWith('/')) {
                    return file.startsWith(doc);
                }
                // Check if documented path is a pattern
                if (doc.includes('*') || doc.includes('YYYY-MM-DD')) {
                    const pattern = doc
                        .replace(/\*/g, '.*')
                        .replace(/YYYY-MM-DD/g, '\\d{4}-\\d{2}-\\d{2}');
                    return new RegExp(pattern).test(file);
                }
                return false;
            });

        if (!isDocumented) {
            undocumented.push(file);
        }
    });

    if (undocumented.length === 0) {
        console.log('✅ Alle Dateien sind dokumentiert!');
        console.log('\n💡 FILE_REGISTRY.md ist vollständig und aktuell.\n');
        console.log('═══════════════════════════════════════════════════════\n');
        return true;
    }

    // Group undocumented files by directory
    const byDirectory = {};
    undocumented.forEach(file => {
        const dir = path.dirname(file);
        if (!byDirectory[dir]) {
            byDirectory[dir] = [];
        }
        byDirectory[dir].push(path.basename(file));
    });

    console.log(`⚠️  ${undocumented.length} undokumentierte Dateien gefunden:\n`);

    Object.entries(byDirectory)
        .sort(([a], [b]) => a.localeCompare(b))
        .forEach(([dir, files]) => {
            console.log(`📂 ${dir}/`);
            files.forEach(file => {
                console.log(`   - ${file}`);
            });
            console.log();
        });

    console.log('💡 Aktion erforderlich:');
    console.log('   1. Entscheide: Braucht Krawl diese Dateien?');
    console.log('   2. JA → Füge zu FILE_REGISTRY.md hinzu');
    console.log('   3. NEIN → Lösche die Datei oder füge zu .gitignore hinzu\n');
    console.log('═══════════════════════════════════════════════════════\n');

    return false;
}

// Run validation
if (require.main === module) {
    const success = validateRegistry();
    process.exit(success ? 0 : 1);
}

module.exports = { validateRegistry, getAllFiles, getDocumentedFiles };
