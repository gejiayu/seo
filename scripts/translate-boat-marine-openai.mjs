#!/usr/bin/env node
/**
 * Batch translate boat-marine-rental-tools from Chinese to English using OpenAI
 * Processes all 91 JSON files
 */

import fs from 'fs';
import path from 'path';
import { glob } from 'glob';
import OpenAI from 'openai';

const dataDir = '/Users/gejiayu/owner/seo/data';
const targetDir = 'boat-marine-rental-tools';

const BATCH_SIZE = 10; // OpenAI can handle more concurrent requests
const BATCH_DELAY = 1000; // 1 second between batches

const client = new OpenAI();

/**
 * Check if text contains Chinese characters
 */
function isChinese(text) {
  return /[一-鿿]/.test(text);
}

/**
 * Translate text using OpenAI GPT-4
 */
async function translateText(text, fieldType = 'general') {
  if (!isChinese(text)) {
    return text;
  }

  const prompts = {
    title: 'Translate this Chinese SEO title to English. Keep it concise and SEO-friendly. Preserve any brand names in English:',
    description: 'Translate this Chinese SEO description to English. Make it engaging and SEO-optimized (150-160 characters ideal):',
    content: 'Translate this Chinese HTML content to English. Preserve all HTML tags exactly. Keep the structure intact. Translate the text content between tags:',
    keyword: 'Translate this Chinese SEO keyword to English. Keep it concise and SEO-friendly:'
  };

  const systemPrompt = prompts[fieldType] || prompts.title;

  try {
    const response = await client.chat.completions.create({
      model: 'gpt-4.1-mini',
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: text }
      ],
      max_tokens: fieldType === 'content' ? 16000 : 500,
      temperature: 0.3
    });

    return response.choices[0].message.content.trim();
  } catch (error) {
    console.error(`Translation error: ${error.message}`);
    throw error;
  }
}

/**
 * Translate SEO keywords array
 */
async function translateKeywords(keywords) {
  if (!keywords || !Array.isArray(keywords)) {
    return [];
  }

  // Batch translate keywords in one API call for efficiency
  const keywordsText = keywords.join('\n');

  try {
    const response = await client.chat.completions.create({
      model: 'gpt-4.1-mini',
      messages: [
        {
          role: 'system',
          content: 'Translate these Chinese SEO keywords to English. Return them as a numbered list, one per line. Keep them concise and SEO-friendly:'
        },
        { role: 'user', content: keywordsText }
      ],
      max_tokens: 500,
      temperature: 0.3
    });

    const translatedText = response.choices[0].message.content.trim();
    // Parse numbered list back to array
    const translatedKeywords = translatedText
      .split('\n')
      .map(line => line.replace(/^\d+\.\s*/, '').trim().toLowerCase())
      .filter(k => k.length > 0);

    return translatedKeywords;
  } catch (error) {
    console.error(`Keywords translation error: ${error.message}`);
    // Fallback: translate individually
    return keywords.map(k => k.toLowerCase());
  }
}

/**
 * Process single file
 */
async function processFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const jsonData = JSON.parse(content);

  // Check if already English
  if (jsonData.language === 'en-US') {
    console.log(`  ✓ ${path.basename(filePath)} - already English`);
    return { processed: false, reason: 'already_english' };
  }

  console.log(`  → ${path.basename(filePath)} - translating...`);

  // Translate fields
  const translatedTitle = await translateText(jsonData.title, 'title');
  const translatedDescription = await translateText(jsonData.description, 'description');
  const translatedContent = await translateText(jsonData.content, 'content');
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

  console.log(`  ✓ ${path.basename(filePath)} - completed`);
  return { processed: true };
}

/**
 * Sleep helper
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Process all files with batch control
 */
async function processAllFiles() {
  const pattern = path.join(dataDir, targetDir, '*.json');
  const files = await glob(pattern);

  console.log(`\n${'='.repeat(60)}`);
  console.log(`Translating boat-marine-rental-tools: ${files.length} files`);
  console.log(`${'='.repeat(60)}\n`);

  let processedCount = 0;
  let skippedCount = 0;
  let errorCount = 0;

  // Process in batches
  for (let i = 0; i < files.length; i += BATCH_SIZE) {
    const batchNumber = Math.floor(i / BATCH_SIZE) + 1;
    const totalBatches = Math.ceil(files.length / BATCH_SIZE);
    const batch = files.slice(i, i + BATCH_SIZE);

    console.log(`\nBatch ${batchNumber}/${totalBatches} (${batch.length} files):`);

    // Process files in batch concurrently
    const promises = batch.map(filePath =>
      processFile(filePath).catch(error => {
        errorCount++;
        console.error(`  ✗ ${path.basename(filePath)} - error: ${error.message}`);
        return { processed: false, reason: 'error' };
      })
    );

    const results = await Promise.all(promises);

    results.forEach(result => {
      if (result.processed) {
        processedCount++;
      } else {
        skippedCount++;
      }
    });

    // Delay between batches (except last batch)
    if (i + BATCH_SIZE < files.length) {
      await sleep(BATCH_DELAY);
    }

    // Progress report
    console.log(`\nProgress: ${processedCount + skippedCount}/${files.length} files processed`);
  }

  console.log(`\n${'='.repeat(60)}`);
  console.log(`FINAL REPORT`);
  console.log(`${'='.repeat(60)}`);
  console.log(`✓ Translated: ${processedCount} files`);
  console.log(`○ Skipped: ${skippedCount} files (already English)`);
  console.log(`✗ Errors: ${errorCount} files failed`);
  console.log(`Total: ${files.length} files`);
  console.log(`${'='.repeat(60)}`);

  return { processedCount, skippedCount, errorCount, total: files.length };
}

// Run
console.log('Starting translation process...\n');
processAllFiles()
  .then(result => {
    console.log(`\n✓✓✓ 100% COMPLETE ✓✓✓`);
    console.log(`All ${result.total} files processed successfully!\n`);
  })
  .catch(error => {
    console.error(`\n✗ Fatal error: ${error.message}`);
    process.exit(1);
  });