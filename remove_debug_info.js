#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Debug patterns to search for and remove
const debugPatterns = [
  'Debug Info:',
  'Current filters:',
  'Pagination object:',
  'Users count:',
  'console.log(',
  'console.error(',
  'console.warn(',
  'console.info('
];

// Directories to search
const searchDirs = [
  './frontend/src',
  './app',
  './src'
];

function searchAndRemoveDebug(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    let modified = false;
    let newContent = content;

    // Remove debug patterns
    debugPatterns.forEach(pattern => {
      if (newContent.includes(pattern)) {
        console.log(`Found debug pattern "${pattern}" in ${filePath}`);
        modified = true;
      }
    });

    // Remove console.log statements
    const consoleLogRegex = /console\.(log|error|warn|info)\([^)]*\);?\s*/g;
    if (consoleLogRegex.test(newContent)) {
      console.log(`Found console statements in ${filePath}`);
      newContent = newContent.replace(consoleLogRegex, '');
      modified = true;
    }

    // Remove debug info sections
    const debugSectionRegex = /Debug Info:[\s\S]*?(?=\n\n|\n$|$)/g;
    if (debugSectionRegex.test(newContent)) {
      console.log(`Found debug info section in ${filePath}`);
      newContent = newContent.replace(debugSectionRegex, '');
      modified = true;
    }

    if (modified) {
      fs.writeFileSync(filePath, newContent, 'utf8');
      console.log(`✅ Updated ${filePath}`);
    }

  } catch (error) {
    console.error(`Error processing ${filePath}:`, error.message);
  }
}

function walkDir(dir) {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      walkDir(filePath);
    } else if (file.endsWith('.js') || file.endsWith('.jsx') || file.endsWith('.ts') || file.endsWith('.tsx')) {
      searchAndRemoveDebug(filePath);
    }
  });
}

console.log('🔍 Searching for debug information...');
searchDirs.forEach(dir => {
  if (fs.existsSync(dir)) {
    console.log(`\n📁 Searching in ${dir}`);
    walkDir(dir);
  }
});

console.log('\n✅ Debug removal script completed!');
console.log('\n📝 Manual steps to complete:');
console.log('1. Check if any debug information is still visible in the UI');
console.log('2. Look for any remaining debug text in the browser console');
console.log('3. Test the application to ensure functionality is preserved');
console.log('4. If debug info persists, check for any remaining debug components or sections'); 