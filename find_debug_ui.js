#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Specific debug patterns that might be rendered in UI
const uiDebugPatterns = [
  'Debug Info:',
  'Current filters:',
  'Pagination object:',
  'Users count:',
  'Debug:',
  'DEBUG:',
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

function searchUIDebug(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    let foundPatterns = [];

    // Check for debug patterns
    uiDebugPatterns.forEach(pattern => {
      if (content.includes(pattern)) {
        foundPatterns.push(pattern);
      }
    });

    // Check for debug sections that might be rendered
    const debugSectionRegex = /Debug Info:[\s\S]*?(?=\n\n|\n$|$)/g;
    if (debugSectionRegex.test(content)) {
      foundPatterns.push('Debug Info Section');
    }

    // Check for debug components or sections
    const debugComponentRegex = /{.*?Debug.*?}/g;
    if (debugComponentRegex.test(content)) {
      foundPatterns.push('Debug Component');
    }

    if (foundPatterns.length > 0) {
      console.log(`\n🔍 Found debug patterns in: ${filePath}`);
      foundPatterns.forEach(pattern => {
        console.log(`   - ${pattern}`);
      });

      // Show context around debug patterns
      uiDebugPatterns.forEach(pattern => {
        if (content.includes(pattern)) {
          const lines = content.split('\n');
          lines.forEach((line, index) => {
            if (line.includes(pattern)) {
              console.log(`\n   Line ${index + 1}: ${line.trim()}`);
              // Show surrounding context
              for (let i = Math.max(0, index - 2); i <= Math.min(lines.length - 1, index + 2); i++) {
                const prefix = i === index ? '>>> ' : '    ';
                console.log(`${prefix}${i + 1}: ${lines[i].trim()}`);
              }
            }
          });
        }
      });
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
      searchUIDebug(filePath);
    }
  });
}

console.log('🔍 Searching for UI debug information...');
console.log('This will help identify where debug info is being rendered in the interface\n');

searchDirs.forEach(dir => {
  if (fs.existsSync(dir)) {
    console.log(`📁 Searching in ${dir}`);
    walkDir(dir);
  }
});

console.log('\n✅ UI debug search completed!');
console.log('\n📝 To remove debug information:');
console.log('1. Look for the files listed above');
console.log('2. Remove or comment out the debug sections');
console.log('3. Check if the debug info is in a conditional render (e.g., {process.env.NODE_ENV === "development" && ...})');
console.log('4. Look for any debug components that might be imported'); 