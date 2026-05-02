#!/usr/bin/env node
/**
 * Translate Chinese content to English in travel-hospitality-tools directory
 * Uses @vitalets/google-translate-api for free translation
 */

import fs from 'fs';
import path from 'path';
import { glob } from 'glob';
import { translate } from '@vitalets/google-translate-api';

const dataDir = '/Users/gejiayu/owner/seo/data/travel-hospitality-tools';
const BATCH_SIZE = 5; // Smaller batches
const DELAY_MS = 3000; // 3 seconds between translations to avoid rate limits

/**
 * Check if text contains Chinese characters
 */
function containsChinese(text) {
  return /[一-鿿]/.test(text);
}

/**
 * Translate text with retry logic
 */
async function translateText(text, maxRetries = 3) {
  if (!text || !containsChinese(text)) {
    return text;
  }

  // Define hosts array outside try block
  const hosts = ['translate.google.com', 'translate.google.cn', 'translate.googleapis.com'];

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const host = hosts[attempt % hosts.length];

      // For long texts, split into chunks
      if (text.length > 5000) {
        const chunks = [];
        const chunkSize = 4500;
        for (let i = 0; i < text.length; i += chunkSize) {
          const chunk = text.slice(i, i + chunkSize);
          const result = await translate(chunk, { from: 'zh', to: 'en', host });
          chunks.push(result.text);
          await new Promise(resolve => setTimeout(resolve, DELAY_MS));
        }
        return chunks.join('');
      }

      const result = await translate(text, { from: 'zh', to: 'en', host });
      return result.text;
    } catch (error) {
      if (attempt < maxRetries - 1) {
        console.log(`    Retry ${attempt + 1} (host: ${hosts[(attempt + 1) % hosts.length]})...`);
        await new Promise(resolve => setTimeout(resolve, 5000));
      } else {
        console.error(`    Translation failed: ${error.message}`);
        return text;
      }
    }
  }
  return text;
}

/**
 * Translate title
 */
async function translateTitle(title) {
  const translated = await translateText(title);
  // Ensure year is included
  if (!translated.includes('2026') && title.includes('2026')) {
    return `${translated} | 2026 Review`;
  }
  return translated;
}

/**
 * Translate description
 */
async function translateDescription(description) {
  const translated = await translateText(description);
  return translated;
}

/**
 * Translate HTML content while preserving structure
 */
async function translateContent(content) {
  // Translate the whole HTML content
  // The structure will be preserved by Google Translate
  const translated = await translateText(content);
  return translated;
}

/**
 * Clean seo_keywords
 */
function cleanKeywords(keywords) {
  if (!keywords || !Array.isArray(keywords)) {
    return keywords;
  }
  return keywords.map(kw => kw.replace(/\s+/g, ' ').trim());
}

/**
 * Process a single file
 */
async function processFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const data = JSON.parse(content);

    const hasChineseTitle = containsChinese(data.title);
    const hasChineseDesc = containsChinese(data.description);
    const hasChineseContent = containsChinese(data.content);

    if (!hasChineseTitle && !hasChineseDesc && !hasChineseContent) {
      return { status: 'skipped', reason: 'already English' };
    }

    let translated = false;

    if (hasChineseTitle) {
      console.log('    Translating title...');
      data.title = await translateTitle(data.title);
      translated = true;
      await new Promise(resolve => setTimeout(resolve, DELAY_MS));
    }

    if (hasChineseDesc) {
      console.log('    Translating description...');
      data.description = await translateDescription(data.description);
      translated = true;
      await new Promise(resolve => setTimeout(resolve, DELAY_MS));
    }

    if (hasChineseContent) {
      console.log('    Translating content...');
      data.content = await translateContent(data.content);
      translated = true;
      await new Promise(resolve => setTimeout(resolve, DELAY_MS));
    }

    // Clean keywords
    data.seo_keywords = cleanKeywords(data.seo_keywords);

    // Write back
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');

    return { status: 'translated' };
  } catch (error) {
    return { status: 'error', error: error.message };
  }
}

/**
 * Process all files
 */
async function processAllFiles() {
  const pattern = path.join(dataDir, '*.json');
  const files = await glob(pattern);

  console.log(`Found ${files.length} files to process\n`);

  let translated = 0;
  let skipped = 0;
  let errors = 0;

  const totalBatches = Math.ceil(files.length / BATCH_SIZE);

  for (let batchNum = 0; batchNum < totalBatches; batchNum++) {
    const startIdx = batchNum * BATCH_SIZE;
    const endIdx = Math.min(startIdx + BATCH_SIZE, files.length);
    const batch = files.slice(startIdx, endIdx);

    console.log(`Processing batch ${batchNum + 1}/${totalBatches}...`);

    for (const filePath of batch) {
      const fileName = path.basename(filePath);
      console.log(`  Processing ${fileName}...`);

      const result = await processFile(filePath);

      if (result.status === 'translated') {
        translated++;
        console.log(`    ✓ Translated`);
      } else if (result.status === 'skipped') {
        skipped++;
        console.log(`    - Skipped (${result.reason})`);
      } else {
        errors++;
        console.log(`    ✗ Error: ${result.error}`);
      }
    }

    // Delay between batches
    if (batchNum + 1 < totalBatches) {
      console.log(`\n  Waiting ${DELAY_MS}ms before next batch...\n`);
      await new Promise(resolve => setTimeout(resolve, DELAY_MS));
    }
  }

  console.log('\n=== Summary ===');
  console.log(`Translated: ${translated} files`);
  console.log(`Skipped: ${skipped} files`);
  console.log(`Errors: ${errors} files`);
  console.log(`Total: ${files.length} files`);
}

processAllFiles().catch(console.error);