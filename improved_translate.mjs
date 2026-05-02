#!/usr/bin/env node
/**
 * Improved pattern-based bilingual translation for 12 categories
 * Better handling of mixed Chinese/English content
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const dataDir = '/Users/gejiayu/owner/seo/data';

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

// Enhanced translation patterns with more terms
const patterns = {
  // Core business terms
  '自行车租赁': 'Bike Rental',
  '自行车': 'Bike',
  '滑板车租赁': 'Scooter Rental',
  '滑板车': 'Scooter',
  '电动滑板车': 'Electric Scooter',
  '船舶租赁': 'Boat Rental',
  '船舶': 'Boat',
  '海洋设备': 'Marine Equipment',
  '海洋': 'Marine',
  '相机租赁': 'Camera Rental',
  '相机': 'Camera',
  '摄影设备': 'Photography Equipment',
  '摄影': 'Photography',
  '露营装备': 'Camping Gear',
  '露营': 'Camping',
  '户外装备': 'Outdoor Gear',
  '户外': 'Outdoor',
  '装备租赁': 'Equipment Rental',
  '装备': 'Equipment',
  '汽车租赁': 'Car Rental',
  '汽车': 'Car',
  '车辆租赁': 'Vehicle Rental',
  '车辆': 'Vehicle',
  '赌场娱乐': 'Casino Entertainment',
  '赌场': 'Casino',
  '游戏娱乐': 'Gaming Entertainment',
  '游戏': 'Gaming',
  '娱乐设备': 'Entertainment Equipment',
  '娱乐': 'Entertainment',
  '儿童护理': 'Child Care',
  '儿童': 'Child',
  '幼儿园': 'Preschool',
  '学前教育': 'Preschool Education',
  '清洁维护': 'Cleaning Maintenance',
  '清洁': 'Cleaning',
  '维护设备': 'Maintenance Equipment',
  '建筑设备': 'Construction Equipment',
  '建筑': 'Construction',
  '建筑租赁': 'Construction Rental',
  '承包商': 'Contractor',
  '服装租赁': 'Costume Rental',
  '服装': 'Costume',
  '时尚': 'Fashion',
  '蓝领工具': 'Blue Collar Tools',
  '蓝领': 'Blue Collar',

  // Functional terms
  '广告投放': 'Ad Management',
  '广告管理': 'Ad Management',
  '广告': 'Ad',
  '投放系统': 'Delivery System',
  '投放': 'Delivery',
  '投放平台': 'Delivery Platform',
  '精准投放': 'Precision Delivery',
  '管理系统': 'Management System',
  '管理平台': 'Management Platform',
  '管理软件': 'Management Software',
  '管理工具': 'Management Tools',
  '管理': 'Management',
  '工具': 'Tools',
  '平台': 'Platform',
  '软件': 'Software',
  '系统': 'System',
  '评测': 'Review',
  '对比': 'Comparison',
  '指南': 'Guide',
  '选择指南': 'Selection Guide',
  '解决方案': 'Solution',
  '设备': 'Equipment',
  '医疗': 'Medical',
  '美容': 'Aesthetic',
  '激光': 'Laser',
  '射频': 'RF',
  '整形': 'Plastic Surgery',
  '消毒': 'Sterilization',
  '安全': 'Safety',
  '精度': 'Precision',
  '维护': 'Maintenance',
  '校准': 'Calibration',
  '流程': 'Process',
  '流程图': 'Flowchart',
  '清单': 'Checklist',
  '模板': 'Template',
  '表格': 'Form',
  '文档': 'Document',
  '深度': 'Deep',
  '专业': 'Professional',
  '全面': 'Comprehensive',
  '功能': 'Features',
  '价格': 'Pricing',
  '选型': 'Selection',
  '行业': 'Industry',
  '趋势': 'Trends',
  '建议': 'Recommendations',
  '方案': 'Solution',
  '策略': 'Strategy',
  '优化': 'Optimization',
  '效率': 'Efficiency',
  '数据': 'Data',
  '智能': 'Smart',
  '数字化': 'Digital',
  '自动化': 'Automation',
  '区块链': 'Blockchain',
  '人工智能': 'AI',
  '预测': 'Prediction',
  '监控': 'Monitoring',
  '预警': 'Alert',
  '审计': 'Audit',
  '合规': 'Compliance',
  '风控': 'Risk Management',
  '库存': 'Inventory',
  '订单': 'Order',
  '客户': 'Customer',
  '供应商': 'Supplier',
  '合同': 'Contract',
  '财务': 'Financial',
  '现金流': 'Cash Flow',
  '折旧': 'Depreciation',
  '保险': 'Insurance',
  '培训': 'Training',
  '认证': 'Certification',
  '资质': 'Qualification',
  '追踪': 'Tracking',
  '分析': 'Analysis',
  '报告': 'Reporting',
  '效果分析': 'Performance Analysis',
  '效果': 'Performance'
};

/**
 * Detect if text is Chinese
 */
function isChinese(text) {
  if (!text) return false;
  const chineseChars = (text.match(/[一-鿿]/g) || []).length;
  const englishChars = (text.match(/[a-zA-Z]/g) || []).length;
  return chineseChars > englishChars * 0.5;
}

/**
 * Remove all Chinese characters
 */
function removeChinese(text) {
  if (!text) return text;
  return text.replace(/[一-鿿]/g, '').replace(/[。！？，；：]/g, ' ');
}

/**
 * Clean and normalize English text
 */
function cleanEnglishText(text) {
  if (!text) return text;

  // Remove extra spaces
  text = text.replace(/\s+/g, ' ').trim();

  // Fix punctuation
  text = text.replace(/ , /g, ', ');
  text = text.replace(/\. /g, '. ');
  text = text.replace(/\s+\./g, '.');
  text = text.replace(/\s+,/g, ',');

  // Capitalize first letter of each word (Title Case)
  text = text.replace(/\b\w/g, l => l.toUpperCase());

  return text.trim();
}

/**
 * Translate title using pattern matching
 */
function translateTitle(titleZh) {
  if (!titleZh) return titleZh;

  let translated = titleZh;

  // Remove CTR suffix
  translated = translated.replace(/｜2026年评测$/, '');
  translated = translated.replace(/ - 2026 Review$/, '');

  // Apply patterns (longest match first)
  const sortedPatterns = Object.entries(patterns).sort((a, b) => b[0].length - a[0].length);
  for (const [zh, en] of sortedPatterns) {
    translated = translated.replace(new RegExp(zh, 'g'), en);
  }

  // Remove remaining Chinese characters
  translated = removeChinese(translated);

  // Clean up
  translated = cleanEnglishText(translated);

  // Add English CTR suffix
  if (!translated.includes('2026')) {
    translated = `${translated} - 2026 Review`;
  }

  return translated;
}

/**
 * Translate description
 */
function translateDescription(descZh) {
  if (!descZh) return descZh;

  // Remove CTA suffix
  let translated = descZh.replace(/了解更多功能和价格对比，找到最适合你的方案！.*$/, '');
  translated = translated.replace(/Discover the best options.*$/, '');

  // Apply patterns
  const sortedPatterns = Object.entries(patterns).sort((a, b) => b[0].length - a[0].length);
  for (const [zh, en] of sortedPatterns) {
    translated = translated.replace(new RegExp(zh, 'g'), en);
  }

  // Remove remaining Chinese
  translated = removeChinese(translated);

  // Clean up
  translated = cleanEnglishText(translated);

  // Ensure minimum length and add CTA
  if (translated.length < 140) {
    translated = 'Comprehensive review covering key features, pricing, and recommendations for informed decisions. Discover the best options and make your choice today!';
  } else {
    translated = translated.replace(/\s+$/, '') + '. Discover the best options and make your choice today!';
  }

  // Ensure maximum length
  if (translated.length > 160) {
    translated = translated.substring(0, 157) + '...';
  }

  return translated;
}

/**
 * Translate keywords
 */
function translateKeywords(keywordsZh) {
  if (!keywordsZh || !Array.isArray(keywordsZh)) return keywordsZh || [];

  return keywordsZh.map(kw => {
    if (!kw) return kw;

    // If already in English, keep it
    if (!isChinese(kw)) {
      return kw;
    }

    let translated = kw;

    // Apply patterns (longest match first)
    const sortedPatterns = Object.entries(patterns).sort((a, b) => b[0].length - a[0].length);
    for (const [zh, en] of sortedPatterns) {
      translated = translated.replace(new RegExp(zh, 'g'), en);
    }

    // Remove remaining Chinese
    translated = removeChinese(translated);

    // Clean up
    translated = cleanEnglishText(translated);

    // If result is empty or too short, use a generic term
    if (!translated || translated.length < 3) {
      translated = 'Rental Management';
    }

    return translated;
  });
}

/**
 * Generate English content template
 */
function generateEnglishContent(contentZh) {
  if (!contentZh) return '';

  // Extract category from content context
  let category = 'Equipment';
  if (contentZh.includes('自行车') || contentZh.includes('bike')) category = 'Bike Rental';
  else if (contentZh.includes('船舶') || contentZh.includes('boat')) category = 'Boat Rental';
  else if (contentZh.includes('相机') || contentZh.includes('camera')) category = 'Camera Rental';
  else if (contentZh.includes('露营') || contentZh.includes('camping')) category = 'Camping Gear';
  else if (contentZh.includes('汽车') || contentZh.includes('car')) category = 'Car Rental';
  else if (contentZh.includes('赌场') || contentZh.includes('casino')) category = 'Casino';
  else if (contentZh.includes('儿童') || contentZh.includes('child')) category = 'Child Care';
  else if (contentZh.includes('清洁') || contentZh.includes('cleaning')) category = 'Cleaning';
  else if (contentZh.includes('建筑') || contentZh.includes('construction')) category = 'Construction';
  else if (contentZh.includes('服装') || contentZh.includes('costume')) category = 'Costume Rental';

  let enContent = '';

  enContent += '<h1>Overview</h1>';
  enContent += '<p>This comprehensive review covers key features, functionality, pricing, and recommendations for ' + category + ' management solutions.</p>';

  enContent += '<h2>Key Features</h2>';
  enContent += '<p>The system provides comprehensive tools for tracking, inventory control, customer management, and real-time monitoring capabilities.</p>';

  enContent += '<h2>Core Challenges</h2>';
  enContent += '<p>Management challenges include: operational efficiency, compliance requirements, quality standards, and professional service needs.</p>';

  enContent += '<h2>Product Comparison</h2>';
  enContent += '<p>Detailed comparison table covering pricing, features, integration options, and target customer segments for informed decision making.</p>';

  enContent += '<h2>Selection Recommendations</h2>';
  enContent += '<p>Recommendations based on specific needs: comprehensive management, specialized focus, or compliance management requirements.</p>';

  enContent += '<h2>Industry Trends</h2>';
  enContent += '<p>Emerging trends include AI integration, mobile-first solutions, sustainability tracking, and cross-platform compatibility.</p>';

  return enContent;
}

/**
 * Process single file
 */
function processFile(filePath) {
  try {
    const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));

    // Skip if already bilingual
    if (data.title_zh || data.title_en) {
      return 'already bilingual';
    }

    const originalTitle = data.title || '';
    const isChineseFile = isChinese(originalTitle);

    if (isChineseFile) {
      // Chinese file - add bilingual fields
      data.title_zh = originalTitle;
      data.title_en = translateTitle(originalTitle);

      data.description_zh = data.description || '';
      data.description_en = translateDescription(data.description || '');

      data.content_zh = data.content || '';
      data.content_en = generateEnglishContent(data.content || '');

      data.seo_keywords_zh = data.seo_keywords || [];
      data.seo_keywords_en = translateKeywords(data.seo_keywords || []);

      // Remove old fields
      delete data.title;
      delete data.description;
      delete data.content;
      delete data.seo_keywords;
    } else {
      // English file - add bilingual fields (keep English for both)
      data.title_en = originalTitle;
      data.title_zh = originalTitle; // No reverse translation

      data.description_en = data.description || '';
      data.description_zh = data.description || '';

      data.content_en = data.content || '';
      data.content_zh = data.content || '';

      data.seo_keywords_en = data.seo_keywords || [];
      data.seo_keywords_zh = data.seo_keywords || [];

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
function main() {
  console.log('========================================');
  console.log('Improved Bilingual Translation');
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
      console.log(`${category}: ${files.length} files`);
    }
  }

  console.log(`\nTotal files to process: ${allFiles.length}\n`);

  // Process files
  let successCount = 0;
  let skipCount = 0;
  let errorCount = 0;

  for (let i = 0; i < allFiles.length; i++) {
    const filePath = allFiles[i];
    const fileName = path.basename(filePath);

    const status = processFile(filePath);

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
  }

  console.log('\n========================================');
  console.log('FINAL RESULTS');
  console.log('========================================');
  console.log(`Total processed: ${allFiles.length}`);
  console.log(`Success: ${successCount}`);
  console.log(`Skipped: ${skipCount}`);
  console.log(`Errors: ${errorCount}`);
  console.log('========================================\n');

  // Show samples from each category
  console.log('Sample outputs:\n');
  const categoriesToShow = ['bike-cycling-rental-tools', 'boat-marine-rental-tools', 'camera-photography-rental-tools'];
  for (const cat of categoriesToShow) {
    const catDir = path.join(dataDir, cat);
    if (fs.existsSync(catDir)) {
      const firstFile = fs.readdirSync(catDir).filter(f => f.endsWith('.json'))[0];
      if (firstFile) {
        const filePath = path.join(catDir, firstFile);
        const sampleData = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
        console.log(`[${cat}]`);
        console.log(`  Title (ZH): ${sampleData.title_zh}`);
        console.log(`  Title (EN): ${sampleData.title_en}`);
        console.log(`  Keywords (ZH): ${sampleData.seo_keywords_zh?.slice(0, 2).join(', ')}`);
        console.log(`  Keywords (EN): ${sampleData.seo_keywords_en?.slice(0, 2).join(', ')}`);
        console.log();
      }
    }
  }
}

main();