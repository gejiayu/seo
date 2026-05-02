const fs = require('fs');
const path = require('path');

// Read all files from stdin
const files = fs.readFileSync(0, 'utf-8').trim().split('\n');

files.forEach(file => {
  const data = JSON.parse(fs.readFileSync(file, 'utf-8'));
  
  // Check if already bilingual
  if (data.title_en && data.title_zh) {
    console.log(`SKIP: ${file} (already bilingual)`);
    return;
  }
  
  // Determine source language
  const isChinese = /[一-鿿]/.test(data.title);
  
  if (isChinese) {
    // Chinese source - add _zh and need _en translation
    data.title_zh = data.title;
    data.description_zh = data.description;
    data.content_zh = data.content;
    console.log(`CN: ${file} - needs EN translation`);
  } else {
    // English source - add _en and need _zh translation
    data.title_en = data.title;
    data.description_en = data.description;
    data.content_en = data.content;
    console.log(`EN: ${file} - needs ZH translation`);
  }
  
  // Remove old fields
  delete data.title;
  delete data.description;
  delete data.content;
  
  // Write back
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
});

console.log(`Processed ${files.length} files`);
