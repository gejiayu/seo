#!/usr/bin/env node
/**
 * pSEO Bilingual Translation Agent
 * Processes specific categories to generate bilingual (English + Chinese) files.
 * - English version: data/[category]/[slug].json
 * - Chinese version: data/zh/[category]/[slug].json
 * - Each file has: language, canonical_link, alternate_links fields
 */

import fs from 'fs';
import path from 'path';
import OpenAI from 'openai';

const SITE_URL = process.env.SITE_URL || 'https://www.housecar.life';

// Categories to process
const TARGET_CATEGORIES = [
  'laundry-dry-cleaning-tools',
  'legal',
  'legal-compliance-tools',
  'legal-document-management-tools',
  'lighting-lamp-rental-tools',
  'logistics-supply-chain-tools'
];

const dataDir = '/Users/gejiayu/owner/seo/data';
const zhDir = '/Users/gejiayu/owner/seo/data/zh';

// Initialize OpenAI client
const client = new OpenAI();

/**
 * Check if text is primarily Chinese
 */
function isChineseContent(text) {
  if (!text) return false;
  const chineseChars = (text.match(/[一-鿿]/g) || []).length;
  const totalChars = text.trim().length;
  return chineseChars > totalChars * 0.3;
}

/**
 * Translate text using OpenAI API
 */
async function translateText(text, direction, fieldType) {
  if (!text) return text;

  // Skip if already in target language
  if (direction === 'en' && !isChineseContent(text)) return text;
  if (direction === 'zh' && isChineseContent(text)) return text;

  const maxTokens = fieldType === 'content' ? 4000 : 500;
  const textToTranslate = text.slice(0, maxTokens * 4);

  const systemPrompts = {
    'en': {
      'title': "You are a professional SEO translator. Translate this Chinese title to English. Make it professional and include CTR words like 'Review', 'Guide', 'Comparison', 'Best'. Add suffix '- 2026 Review' if appropriate. Output only the English title.",
      'description': "You are a professional SEO translator. Translate this Chinese description to English. Keep it 140-160 characters with a compelling CTA. Output only the English description.",
      'content': "You are a professional translator. Translate this Chinese content to English. Maintain all HTML tags, headings, lists, and formatting exactly. Output only the translation.",
      'keywords': "You are an SEO expert. Translate these Chinese keywords to English SEO keywords (5-8 terms). Output as a JSON array of strings only."
    },
    'zh': {
      'title': "You are a professional SEO translator. Translate this English title to Chinese. Make it professional and include CTR words like '评测', '指南', '对比'. Add suffix '｜2026年评测' if not present. Output only the Chinese title.",
      'description': "You are a professional SEO translator. Translate this English description to Chinese. Keep it 140-160 characters with a CTA like '了解更多功能和价格对比，找到最适合你的方案！'. Output only the Chinese description.",
      'content': "You are a professional translator. Translate this English content to Chinese. Maintain all HTML tags, headings, lists, and formatting exactly. Output only the translation.",
      'keywords': "You are an SEO expert. Translate these English keywords to Chinese SEO keywords (5-8 terms). Output as a JSON array of strings only."
    }
  };

  try {
    const response = await client.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: systemPrompts[direction][fieldType] || systemPrompts[direction]['content'] },
        { role: 'user', content: textToTranslate }
      ],
      max_tokens: maxTokens,
      temperature: 0.3
    });

    let result = response.choices[0].message.content.trim();

    // Parse keywords if returned as JSON array string
    if (fieldType === 'keywords' && result.startsWith('[')) {
      try {
        const parsed = JSON.parse(result);
        if (Array.isArray(parsed)) {
          return parsed;
        }
      } catch (e) {
        // If parse fails, return as-is
      }
    }

    return result;
  } catch (error) {
    console.error(`Translation error: ${error.message}`);
    return text;
  }
}

/**
 * Translate keywords array
 */
async function translateKeywords(keywords, direction) {
  if (!keywords || keywords.length === 0) return [];

  // Translate as a batch
  const keywordStr = JSON.stringify(keywords);
  const translated = await translateText(keywordStr, direction, 'keywords');

  if (Array.isArray(translated)) {
    return translated.slice(0, 8);
  }

  // If translation failed, try individual keywords
  const result = [];
  for (const kw of keywords) {
    if (direction === 'en' && isChineseContent(kw)) {
      result.push(await translateText(kw, 'en', 'keywords'));
    } else if (direction === 'zh' && !isChineseContent(kw)) {
      result.push(await translateText(kw, 'zh', 'keywords'));
    } else {
      result.push(kw);
    }
  }

  return result.slice(0, 8);
}

/**
 * Generate canonical link
 */
function generateCanonicalLink(slug) {
  return `${SITE_URL}/posts/${slug}`;
}

/**
 * Generate alternate links
 */
function generateAlternateLinks(slug) {
  return {
    'en-US': `${SITE_URL}/posts/${slug}`,
    'zh-CN': `${SITE_URL}/zh/posts/${slug}`
  };
}

/**
 * Process a single file
 */
async function processFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const data = JSON.parse(content);

  const originalTitle = data.title || '';
  const originalDesc = data.description || '';
  const originalContent = data.content || '';
  const originalKeywords = data.seo_keywords || [];
  const slug = data.slug || '';
  const publishedAt = data.published_at || '';
  const author = data.author || '';

  const category = path.dirname(filePath).split('/').pop();
  const isChinese = isChineseContent(originalTitle);

  // Generate English version
  let enTitle, enDesc, enContent, enKeywords;
  if (isChinese) {
    enTitle = await translateText(originalTitle, 'en', 'title');
    enDesc = await translateText(originalDesc, 'en', 'description');
    enContent = await translateText(originalContent, 'en', 'content');
    enKeywords = await translateKeywords(originalKeywords, 'en');
  } else {
    enTitle = originalTitle;
    enDesc = originalDesc;
    enContent = originalContent;
    enKeywords = Array.isArray(originalKeywords) ? originalKeywords : [];
  }

  // Generate Chinese version
  let zhTitle, zhDesc, zhContent, zhKeywords;
  if (isChinese) {
    zhTitle = originalTitle;
    zhDesc = originalDesc;
    zhContent = originalContent;
    zhKeywords = Array.isArray(originalKeywords) ? originalKeywords : [];
  } else {
    zhTitle = await translateText(originalTitle, 'zh', 'title');
    zhDesc = await translateText(originalDesc, 'zh', 'description');
    zhContent = await translateText(originalContent, 'zh', 'content');
    zhKeywords = await translateKeywords(originalKeywords, 'zh');
  }

  // Build English JSON
  const enData = {
    title: enTitle,
    description: enDesc,
    content: enContent,
    seo_keywords: enKeywords,
    slug: slug,
    published_at: publishedAt,
    author: author,
    language: 'en-US',
    canonical_link: generateCanonicalLink(slug),
    alternate_links: generateAlternateLinks(slug),
    category: category
  };

  // Build Chinese JSON
  const zhData = {
    title: zhTitle,
    description: zhDesc,
    content: zhContent,
    seo_keywords: zhKeywords,
    slug: slug,
    published_at: publishedAt,
    author: author,
    language: 'zh-CN',
    canonical_link: generateCanonicalLink(slug),
    alternate_links: generateAlternateLinks(slug),
    category: category
  };

  return { enData, zhData };
}

/**
 * Main processing function
 */
async function main() {
  console.log('pSEO Bilingual Translation Agent');
  console.log('=' .repeat(60));
  console.log(`Categories: ${TARGET_CATEGORIES.join(', ')}`);
  console.log('');

  // Collect all files from target categories
  const allFiles = [];
  for (const category of TARGET_CATEGORIES) {
    const catDir = path.join(dataDir, category);
    if (fs.existsSync(catDir)) {
      const files = fs.readdirSync(catDir).filter(f => f.endsWith('.json'));
      for (const file of files) {
        allFiles.push(path.join(catDir, file));
      }
    }
  }

  console.log(`Total files to process: ${allFiles.length}`);
  console.log('');

  let successCount = 0;
  let errorCount = 0;

  for (let i = 0; i < allFiles.length; i++) {
    const filePath = allFiles[i];

    try {
      const { enData, zhData } = await processFile(filePath);

      const category = path.dirname(filePath).split('/').pop();
      const slug = enData.slug;

      // Write English version (update original file)
      fs.writeFileSync(filePath, JSON.stringify(enData, null, 2), 'utf8');

      // Write Chinese version
      const zhCategoryDir = path.join(zhDir, category);
      if (!fs.existsSync(zhCategoryDir)) {
        fs.mkdirSync(zhCategoryDir, { recursive: true });
      }
      const zhFilePath = path.join(zhCategoryDir, `${slug}.json`);
      fs.writeFileSync(zhFilePath, JSON.stringify(zhData, null, 2), 'utf8');

      successCount++;

      // Report every 20 files
      if ((i + 1) % 20 === 0) {
        console.log(`Progress: ${i + 1}/${allFiles.length} - Success: ${successCount}, Error: ${errorCount}`);
        console.log(`  Latest: ${path.basename(filePath)}`);
      }

      // Rate limit delay
      await new Promise(resolve => setTimeout(resolve, 300));

    } catch (error) {
      errorCount++;
      console.error(`Error processing ${filePath}: ${error.message}`);
    }
  }

  console.log('');
  console.log('=' .repeat(60));
  console.log('FINAL RESULTS');
  console.log(`Total files: ${allFiles.length}`);
  console.log(`Success: ${successCount}`);
  console.log(`Error: ${errorCount}`);
  console.log('=' .repeat(60));
}

main().catch(console.error);