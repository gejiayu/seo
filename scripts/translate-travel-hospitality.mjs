#!/usr/bin/env node
/**
 * Translate Chinese content to English in travel-hospitality-tools directory
 * Files have language="en-US" but contain Chinese content
 * Uses OpenAI for accurate translation
 */

import fs from 'fs';
import path from 'path';
import { glob } from 'glob';
import OpenAI from 'openai';

const dataDir = '/Users/gejiayu/owner/seo/data/travel-hospitality-tools';
const BATCH_SIZE = 10; // Process files in batches to manage API rate limits

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

if (!process.env.OPENAI_API_KEY) {
  console.error('ERROR: OPENAI_API_KEY environment variable not set');
  process.exit(1);
}

/**
 * Translate Chinese text to English using OpenAI
 */
async function translateText(text, fieldType) {
  const prompts = {
    title: `Translate this Chinese SEO title to English. Keep it concise, professional, and SEO-friendly. Do not add any explanations. Just return the translated title:\n\n${text}`,
    description: `Translate this Chinese SEO meta description to English. Keep it under 160 characters, compelling, and include a call-to-action. Do not add any explanations. Just return the translated description:\n\n${text}`,
    content: `Translate this Chinese HTML content to English. Keep the HTML structure exactly the same (h1, h2, h3, p, table, th, td, etc.). Translate only the text content inside the HTML tags. Return only the translated HTML content, no explanations:\n\n${text}`
  };

  const prompt = prompts[fieldType] || prompts.content;

  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        {
          role: 'system',
          content: 'You are a professional translator specializing in hospitality and travel industry content. Translate Chinese to English accurately, maintaining the original tone and style.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      temperature: 0.3
    });

    return response.choices[0]?.message?.content?.trim() || text;
  } catch (error) {
    console.error(`Translation error for ${fieldType}: ${error.message}`);
    return text; // Return original on error
  }
}

/**
 * Check if text contains Chinese characters
 */
function containsChinese(text) {
  return /[一-鿿]/.test(text);
}

/**
 * Process a single JSON file
 */
async function processFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const jsonData = JSON.parse(content);

    // Check if file needs translation (has Chinese content but language is en-US)
    if (!containsChinese(jsonData.title) && !containsChinese(jsonData.description) && !containsChinese(jsonData.content)) {
      return { status: 'skipped', reason: 'already English' };
    }

    // Translate fields that contain Chinese
    let translated = false;

    if (containsChinese(jsonData.title)) {
      jsonData.title = await translateText(jsonData.title, 'title');
      translated = true;
    }

    if (containsChinese(jsonData.description)) {
      jsonData.description = await translateText(jsonData.description, 'description');
      translated = true;
    }

    if (containsChinese(jsonData.content)) {
      jsonData.content = await translateText(jsonData.content, 'content');
      translated = true;
    }

    // Clean up seo_keywords (remove extra spaces)
    if (jsonData.seo_keywords && Array.isArray(jsonData.seo_keywords)) {
      jsonData.seo_keywords = jsonData.seo_keywords.map(kw => kw.replace(/\s+/g, ' ').trim());
    }

    // Write back the translated file
    fs.writeFileSync(filePath, JSON.stringify(jsonData, null, 2), 'utf8');

    return { status: 'translated', translated };
  } catch (error) {
    return { status: 'error', error: error.message };
  }
}

/**
 * Process all files in batches
 */
async function processAllFiles() {
  const pattern = path.join(dataDir, '*.json');
  const files = await glob(pattern);

  console.log(`Found ${files.length} files to process\n`);

  let translated = 0;
  let skipped = 0;
  let errors = 0;
  let alreadyEnglish = 0;

  // Process in batches
  for (let i = 0; i < files.length; i += BATCH_SIZE) {
    const batch = files.slice(i, i + BATCH_SIZE);
    console.log(`Processing batch ${Math.floor(i / BATCH_SIZE) + 1}/${Math.ceil(files.length / BATCH_SIZE)}...`);

    for (const filePath of batch) {
      const result = await processFile(filePath);
      const fileName = path.basename(filePath);

      if (result.status === 'translated') {
        translated++;
        console.log(`  ✓ ${fileName} - translated`);
      } else if (result.status === 'skipped') {
        if (result.reason === 'already English') {
          alreadyEnglish++;
        } else {
          skipped++;
        }
      } else {
        errors++;
        console.error(`  ✗ ${fileName} - error: ${result.error}`);
      }
    }

    // Small delay between batches to avoid rate limits
    if (i + BATCH_SIZE < files.length) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }

  console.log('\n=== Summary ===');
  console.log(`Translated: ${translated} files`);
  console.log(`Already English: ${alreadyEnglish} files`);
  console.log(`Skipped: ${skipped} files`);
  console.log(`Errors: ${errors} files`);
  console.log(`Total processed: ${files.length} files`);
}

processAllFiles().catch(console.error);