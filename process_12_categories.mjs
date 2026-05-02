#!/usr/bin/env node
/**
 * Translate JSON files in 12 specified categories to bilingual format
 * Uses OpenAI GPT-4o-mini for accurate translation
 */

import fs from 'fs';
import path from 'path';
import OpenAI from 'openai';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Initialize OpenAI
const openai = new OpenAI();

// Categories to process
const categories = [
  'bike-cycling-rental-tools',
  'blue-collar-tools',
  'boat-marine-rental-tools',
  'camera-photography-rental-tools',
  'camping-outdoor-gear-rental-tools',
  'car-vehicle-rental-tools',
  'casino-gaming-entertainment-tools',
  'child-care-preschool-tools',
  'cleaning-maintenance-rental-tools',
  'construction-building-rental-tools',
  'construction-contractor-tools',
  'costume-fashion-rental-tools'
];

const dataDir = '/Users/gejiayu/owner/seo/data';

/**
 * Detect if text is primarily Chinese
 */
function isChinese(text) {
  if (!text) return false;
  const chineseChars = (text.match(/[一-鿿]/g) || []).length;
  const englishChars = (text.match(/[a-zA-Z]/g) || []).length;
  return chineseChars > englishChars * 0.5;
}

/**
 * Translate text using OpenAI
 */
async function translateText(text, fieldType = 'content') {
  if (!text) return text;

  // Skip if already in target language
  const lang = isChinese(text) ? 'zh' : 'en';

  // Truncate for API limits
  const maxTokens = fieldType === 'content' ? 4000 : 500;
  const textToTranslate = text.substring(0, maxTokens * 4);

  try {
    const targetLang = lang === 'zh' ? 'English' : 'Chinese';
    const prompt = `Translate this ${fieldType} from ${lang === 'zh' ? 'Chinese' : 'English'} to ${targetLang}. Maintain all HTML structure and formatting exactly. Output only the translation:`;

    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: prompt },
        { role: 'user', content: textToTranslate }
      ],
      max_tokens: maxTokens,
      temperature: 0.3
    });

    return response.choices[0].message.content.trim();
  } catch (error) {
    console.error(`Translation error for ${fieldType}: ${error.message}`);
    return text;
  }
}

/**
 * Translate keywords array
 */
async function translateKeywords(keywords, sourceLang) {
  if (!keywords || !Array.isArray(keywords)) return keywords;

  const translated = [];
  for (const kw of keywords) {
    if (!kw) {
      translated.push(kw);
      continue;
    }

    const kwLang = isChinese(kw) ? 'zh' : 'en';

    // Skip if already in target language
    if (sourceLang === 'zh' && kwLang === 'en') {
      translated.push(kw);
      continue;
    } else if (sourceLang === 'en' && kwLang === 'zh') {
      translated.push(kw);
      continue;
    }

    try {
      const targetLang = kwLang === 'zh' ? 'English' : 'Chinese';
      const response = await openai.chat.completions.create({
        model: 'gpt-4o-mini',
        messages: [
          {
            role: 'system',
            content: `Translate this SEO keyword from ${kwLang === 'zh' ? 'Chinese' : 'English'} to ${targetLang}. Output only the translated keyword:`
          },
          { role: 'user', content: kw }
        ],
        max_tokens: 50,
        temperature: 0.3
      });

      translated.push(response.choices[0].message.content.trim());
    } catch (error) {
      translated.push(kw);
    }

    // Small delay between keywords
    await sleep(0.1);
  }

  return translated;
}

/**
 * Sleep helper
 */
function sleep(seconds) {
  return new Promise(resolve => setTimeout(resolve, seconds * 1000));
}

/**
 * Process single file to bilingual format
 */
async function processFile(filePath) {
  try {
    const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));

    // Skip if already bilingual
    if (data.title_zh || data.title_en) {
      return 'already bilingual';
    }

    // Detect original language
    const originalLang = isChinese(data.title || data.content || '') ? 'zh' : 'en';

    if (originalLang === 'zh') {
      // Chinese file - add English translation
      data.title_zh = data.title || '';
      data.title_en = await translateText(data.title, 'title');

      data.description_zh = data.description || '';
      data.description_en = await translateText(data.description, 'description');

      data.content_zh = data.content || '';
      data.content_en = await translateText(data.content, 'content');

      // Translate keywords
      const keywordsZh = data.seo_keywords || [];
      data.seo_keywords_zh = keywordsZh;
      data.seo_keywords_en = await translateKeywords(keywordsZh, 'zh');

      // Remove old fields
      delete data.title;
      delete data.description;
      delete data.content;
      delete data.seo_keywords;
    } else {
      // English file - add Chinese translation
      data.title_en = data.title || '';
      data.title_zh = await translateText(data.title, 'title');

      data.description_en = data.description || '';
      data.description_zh = await translateText(data.description, 'description');

      data.content_en = data.content || '';
      data.content_zh = await translateText(data.content, 'content');

      // Translate keywords
      const keywordsEn = data.seo_keywords || [];
      data.seo_keywords_en = keywordsEn;
      data.seo_keywords_zh = await translateKeywords(keywordsEn, 'en');

      // Remove old fields
      delete data.title;
      delete data.description;
      delete data.content;
      delete data.seo_keywords;
    }

    // Write back
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');

    return 'success';
  } catch (error) {
    return `error: ${error.message}`;
  }
}

/**
 * Main execution
 */
async function main() {
  console.log('========================================');
  console.log('Bilingual Translation for 12 Categories');
  console.log('========================================\n');

  // Collect all files
  const allFiles = [];
  for (const category of categories) {
    const catDir = path.join(dataDir, category);
    if (fs.existsSync(catDir)) {
      const files = fs.readdirSync(catDir)
        .filter(f => f.endsWith('.json'))
        .map(f => path.join(catDir, f));
      allFiles.push(...files);
    }
  }

  console.log(`Total files to process: ${allFiles.length}`);
  console.log(`Categories: ${categories.join(', ')}`);
  console.log('\n');

  // Process files
  let successCount = 0;
  let skipCount = 0;
  let errorCount = 0;

  for (let i = 0; i < allFiles.length; i++) {
    const filePath = allFiles[i];
    const fileName = path.basename(filePath);

    const status = await processFile(filePath);

    if (status === 'success') {
      successCount++;
    } else if (status === 'already bilingual') {
      skipCount++;
    } else {
      errorCount++;
      console.log(`❌ Error: ${fileName} - ${status}`);
    }

    // Report every 20 files
    if ((i + 1) % 20 === 0) {
      console.log(`✓ Progress: ${i + 1}/${allFiles.length} | Success: ${successCount} | Skip: ${skipCount} | Error: ${errorCount}`);
    }

    // Rate limit delay
    await sleep(0.5);
  }

  console.log('\n========================================');
  console.log('FINAL RESULTS');
  console.log('========================================');
  console.log(`Total processed: ${allFiles.length}`);
  console.log(`Success: ${successCount}`);
  console.log(`Skipped: ${skipCount}`);
  console.log(`Errors: ${errorCount}`);
  console.log('========================================\n');
}

// Run
main().catch(console.error);