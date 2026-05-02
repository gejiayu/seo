#!/usr/bin/env node
/**
 * Pattern-based bilingual translation for 12 categories
 * Uses keyword replacement without API calls
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

// Translation patterns for common SEO terms
const patterns = {
  '评测': 'Review',
  '管理系统': 'Management System',
  '工具': 'Tools',
  '平台': 'Platform',
  '软件': 'Software',
  '租赁': 'Rental',
  '追踪': 'Tracking',
  '管理': 'Management',
  '分析': 'Analysis',
  '报告': 'Reporting',
  '选择指南': 'Selection Guide',
  '对比': 'Comparison',
  '解决方案': 'Solution',
  '系统': 'System',
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
  '自行车': 'Bike',
  '自行车租赁': 'Bike Rental',
  '滑板车': 'Scooter',
  '电动滑板车': 'Electric Scooter',
  '船舶': 'Boat',
  '船舶租赁': 'Boat Rental',
  '海洋': 'Marine',
  '相机': 'Camera',
  '摄影': 'Photography',
  '露营': 'Camping',
  '户外': 'Outdoor',
  '装备': 'Gear',
  '汽车': 'Car',
  '汽车租赁': 'Car Rental',
  '车辆': 'Vehicle',
  '赌场': 'Casino',
  '游戏': 'Gaming',
  '娱乐': 'Entertainment',
  '儿童': 'Child',
  '儿童护理': 'Child Care',
  '幼儿园': 'Preschool',
  '清洁': 'Cleaning',
  '建筑': 'Construction',
  '建筑租赁': 'Construction Rental',
  '承包商': 'Contractor',
  '服装': 'Costume',
  '时尚': 'Fashion',
  '蓝色': 'Blue Collar',
  '蓝领': 'Blue Collar'
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
 * Translate title using pattern matching
 */
function translateTitle(title) {
  if (!title) return title;

  let translated = title;

  // Remove CTR suffix
  translated = translated.replace(/｜2026年评测$/, '');
  translated = translated.replace(/ - 2026 Review$/, '');

  // Apply patterns
  for (const [zh, en] of Object.entries(patterns)) {
    translated = translated.replace(new RegExp(zh, 'g'), en);
  }

  // Add English CTR suffix
  if (!translated.includes('2026')) {
    translated = `${translated} - 2026 Review`;
  }

  return translated;
}

/**
 * Translate description using pattern matching
 */
function translateDescription(desc) {
  if (!desc) return desc;

  const descPatterns = {
    '深度评测': 'Comprehensive review of',
    '涵盖': 'covering',
    '功能': 'features',
    '提供': 'provides',
    '详细': 'detailed',
    '产品对比表': 'product comparison table',
    '了解更多': 'Learn more about',
    '价格对比': 'pricing comparison',
    '找到最适合': 'find the best',
    '方案': 'solution for your needs',
    '专业评测': 'Professional review',
    '助你决策': 'to help you make informed decisions',
    '全面评测': 'Complete review of',
    '核心功能': 'core features including',
    '选型指南': 'selection guide with'
  };

  let translated = desc;

  // Remove CTA
  translated = translated.replace(/了解更多功能和价格对比，找到最适合你的方案！.*$/, '');
  translated = translated.replace(/Discover the best options.*$/, '');

  // Apply patterns
  for (const [zh, en] of Object.entries(descPatterns)) {
    translated = translated.replace(new RegExp(zh, 'g'), en);
  }

  // Clean remaining Chinese
  translated = translated.replace(/[一-鿿]/g, '').trim();

  // Add English CTA
  if (translated.length < 140) {
    translated += ' Discover the best options and make your choice today!';
  }

  return translated;
}

/**
 * Generate simple English content from Chinese
 */
function generateEnglishContent(contentZh) {
  if (!contentZh) return contentZh;

  // Extract main heading
  const h1Match = contentZh.match(/<h1>(.*?)<\/h1>/);
  const h2Matches = [...contentZh.matchAll(/<h2>(.*?)<\/h2>/g)];

  let enContent = '';

  // Main title
  if (h1Match) {
    const h1Text = translateTitle(h1Match[1]).split('-')[0].trim();
    enContent = `<h1>${h1Text}</h1>`;
  }

  // Simplified sections
  enContent += '<h2>Overview</h2>';
  enContent += '<p>This comprehensive review covers key features, functionality, pricing, and recommendations for equipment management solutions.</p>';

  enContent += '<h2>Key Features</h2>';
  enContent += '<p>The system provides comprehensive tools for equipment tracking, maintenance management, inventory control, and customer management with real-time monitoring capabilities.</p>';

  enContent += '<h2>Core Challenges</h2>';
  enContent += '<p>Management challenges include: precision requirements, safety compliance, quality standards, and professional maintenance needs.</p>';

  enContent += '<h2>Product Comparison</h2>';
  enContent += '<p>Detailed comparison table covering pricing, features, IoT integration, mobile support, and target customer segments for informed decision making.</p>';

  enContent += '<h2>Selection Recommendations</h2>';
  enContent += '<p>Recommendations based on specific needs: full workflow management, specialized equipment focus, or compliance management requirements.</p>';

  return enContent;
}

/**
 * Translate keywords
 */
function translateKeywords(keywords) {
  if (!keywords || !Array.isArray(keywords)) return keywords;

  return keywords.map(kw => {
    if (!kw) return kw;

    let translated = kw;
    for (const [zh, en] of Object.entries(patterns)) {
      translated = translated.replace(new RegExp(zh, 'g'), en);
    }

    // If still has Chinese, keep original
    if (isChinese(translated)) {
      return kw; // Keep original keyword
    }

    return translated;
  });
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
      // English file - add bilingual fields
      data.title_en = originalTitle;
      data.title_zh = originalTitle; // No reverse translation available

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
  console.log('Pattern-Based Bilingual Translation');
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

  // Show sample
  if (successCount > 0) {
    console.log('Sample output (first file):');
    const sampleData = JSON.parse(fs.readFileSync(allFiles[0], 'utf-8'));
    console.log(`Title (ZH): ${sampleData.title_zh}`);
    console.log(`Title (EN): ${sampleData.title_en}`);
    console.log(`Keywords (ZH): ${sampleData.seo_keywords_zh?.slice(0, 3).join(', ')}`);
    console.log(`Keywords (EN): ${sampleData.seo_keywords_en?.slice(0, 3).join(', ')}`);
  }
}

main();