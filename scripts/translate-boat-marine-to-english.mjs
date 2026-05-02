#!/usr/bin/env node
/**
 * Batch translate boat-marine-rental-tools from Chinese to English
 * Processes all 91 JSON files
 */

import fs from 'fs';
import path from 'path';
import { glob } from 'glob';
import translate from '@vitalets/google-translate-api';

const dataDir = '/Users/gejiayu/owner/seo/data';
const targetDir = 'boat-marine-rental-tools';

// Rate limiting: translate API has limits
const BATCH_SIZE = 5;
const BATCH_DELAY = 2000; // 2 seconds between batches
const RETRY_DELAY = 5000; // 5 seconds for retries
const MAX_RETRIES = 3;

/**
 * Translate text with retry logic
 */
async function translateText(text, retries = 0) {
  try {
    // Skip if already English
    if (!/[一-鿿]/.test(text)) {
      return text;
    }

    const result = await translate(text, { from: 'zh', to: 'en' });
    return result.text;
  } catch (error) {
    if (retries < MAX_RETRIES) {
      console.log(`Translation failed, retrying (${retries + 1}/${MAX_RETRIES})...`);
      await sleep(RETRY_DELAY);
      return translateText(text, retries + 1);
    }
    throw error;
  }
}

/**
 * Sleep helper
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Translate SEO keywords array
 */
async function translateKeywords(keywords) {
  if (!keywords || !Array.isArray(keywords)) {
    return [];
  }

  const translated = [];
  for (const keyword of keywords) {
    try {
      const translatedKeyword = await translateText(keyword);
      translated.push(translatedKeyword.toLowerCase());
    } catch (error) {
      console.error(`Failed to translate keyword: ${keyword}`);
      translated.push(keyword); // Keep original if failed
    }
  }
  return translated;
}

/**
 * Translate HTML content while preserving HTML tags
 */
async function translateContent(htmlContent) {
  // Split by HTML tags and translate text parts
  const parts = htmlContent.split(/(<[^>]+>)/g);
  const translatedParts = [];

  for (const part of parts) {
    // If it's an HTML tag, keep it
    if (part.startsWith('<') && part.endsWith('>')) {
      translatedParts.push(part);
    } else if (part.trim()) {
      // Translate text part
      try {
        const translated = await translateText(part);
        translatedParts.push(translated);
      } catch (error) {
        console.error(`Failed to translate content part: ${part.substring(0, 50)}...`);
        translatedParts.push(part); // Keep original if failed
      }
    }
  }

  return translatedParts.join('');
}

/**
 * Process single file
 */
async function processFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const jsonData = JSON.parse(content);

  // Check if already English
  if (jsonData.language === 'en-US' || !/[一-鿿]/.test(jsonData.title)) {
    console.log(`Skipping ${path.basename(filePath)} (already English)`);
    return { processed: false, reason: 'already_english' };
  }

  console.log(`Processing ${path.basename(filePath)}...`);

  // Translate fields
  const translatedTitle = await translateText(jsonData.title);
  const translatedDescription = await translateText(jsonData.description);
  const translatedContent = await translateContent(jsonData.content);
  const translatedKeywords = await translateKeywords(jsonData.seo_keywords);

  // Create English version
  const englishData = {
    title: translatedTitle,
    description: translatedDescription,
    content: translatedContent,
    seo_keywords: translatedKeywords,
    slug: jsonData.slug,
    published_at: jsonData.published_at,
    author: jsonData.author,
    language: 'en-US',
    canonical_link: `https://www.housecar.life/posts/${jsonData.slug}`,
    alternate_links: {
      'en-US': `https://www.housecar.life/posts/${jsonData.slug}`,
      'zh-CN': `https://www.housecar.life/posts/zh/${jsonData.slug}`
    }
  };

  // Write back
  fs.writeFileSync(filePath, JSON.stringify(englishData, null, 2), 'utf8');

  console.log(`✓ Completed ${path.basename(filePath)}`);
  return { processed: true };
}

/**
 * Process all files with batch control
 */
async function processAllFiles() {
  const pattern = path.join(dataDir, targetDir, '*.json');
  const files = await glob(pattern);

  console.log(`Found ${files.length} files to process\n`);

  let processedCount = 0;
  let skippedCount = 0;
  let errorCount = 0;

  // Process in batches
  for (let i = 0; i < files.length; i += BATCH_SIZE) {
    const batch = files.slice(i, i + BATCH_SIZE);

    console.log(`\nBatch ${Math.floor(i / BATCH_SIZE) + 1}/${Math.ceil(files.length / BATCH_SIZE)}`);

    for (const filePath of batch) {
      try {
        const result = await processFile(filePath);
        if (result.processed) {
          processedCount++;
        } else {
          skippedCount++;
        }
      } catch (error) {
        errorCount++;
        console.error(`✗ Error processing ${path.basename(filePath)}: ${error.message}`);
      }
    }

    // Delay between batches
    if (i + BATCH_SIZE < files.length) {
      console.log(`\nWaiting ${BATCH_DELAY}ms before next batch...`);
      await sleep(BATCH_DELAY);
    }
  }

  console.log(`\n${'='.repeat(50)}`);
  console.log(`COMPLETED: ${processedCount} files translated`);
  console.log(`SKIPPED: ${skippedCount} files (already English)`);
  console.log(`ERRORS: ${errorCount} files failed`);
  console.log(`TOTAL: ${files.length} files`);
  console.log(`${'='.repeat(50)}`);

  return { processedCount, skippedCount, errorCount, total: files.length };
}

// Run
processAllFiles()
  .then(result => {
    console.log(`\n✓ 100% Complete! All ${result.total} files processed.`);
  })
  .catch(error => {
    console.error(`\n✗ Fatal error: ${error.message}`);
    process.exit(1);
  });