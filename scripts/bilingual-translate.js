const fs = require('fs');
const path = require('path');

// Translation mappings for common terms
const translationMap = {
  // Common phrases
  '评测': 'Review',
  '管理系统': 'Management System',
  '对比': 'Comparison',
  '指南': 'Guide',
  '工具': 'Tools',
  '软件': 'Software',
  '平台': 'Platform',
  '解决方案': 'Solutions',
  '最佳': 'Best',
  '顶级': 'Top',
  '深度': 'Deep',
  '专业': 'Professional',
  '全面': 'Comprehensive',
  '完整': 'Complete',
  '核心': 'Core',
  '功能': 'Features',
  '优势': 'Advantages',
  '劣势': 'Disadvantages',
  '价格': 'Price',
  '月': '/month',
  '年': '/year',
  '选择建议': 'Selection Recommendations',
  '产品对比': 'Product Comparison',
  '行业趋势': 'Industry Trends',
  '选型建议': 'Selection Advice',
  '核心挑战': 'Core Challenges',
  '流程': 'Process',
  '详解': 'Detailed Explanation',
  '总结': 'Summary',

  // Common verbs
  '涵盖': 'Covering',
  '提供': 'Providing',
  '支持': 'Supports',
  '实现': 'Implement',
  '整合': 'Integrate',
  '优化': 'Optimize',
  '追踪': 'Track',
  '管理': 'Manage',
  '监控': 'Monitor',
  '分析': 'Analyze',
  '预测': 'Predict',
  '规划': 'Plan',

  // Qualifiers
  '智能': 'Intelligent',
  '自动化': 'Automated',
  '数字化': 'Digital',
  '云端': 'Cloud-based',
  '移动': 'Mobile',
  '实时': 'Real-time',
  '精准': 'Precision',
  '高效': 'Efficient',

  // Time markers
  '2026年评测': '2026 Review',
  '2026': '2026',

  // Common endings
  '了解更多功能和价格对比，找到最适合你的方案！专业评测助你决策！': 'Learn more about features and pricing comparisons to find the best solution for you! Professional reviews to help you decide!',
};

function translateTitle(chineseTitle) {
  // Extract the main title structure
  let title = chineseTitle;

  // Common title patterns
  title = title.replace('评测：', 'Review: ');
  title = title.replace('｜', ' | ');
  title = title.replace('对比', 'Comparison');
  title = title.replace('指南', 'Guide');
  title = title.replace('2026年评测', '2026 Review');
  title = title.replace('系统评测', 'System Review');
  title = title.replace('工具评测', 'Tools Review');
  title = title.replace('平台评测', 'Platform Review');
  title = title.replace('软件评测', 'Software Review');

  return title;
}

function translateDescription(chineseDesc) {
  let desc = chineseDesc;

  // Common description patterns
  desc = desc.replace('深度评测', 'In-depth review of');
  desc = desc.replace('涵盖', 'covering');
  desc = desc.replace('等功能', 'and other features');
  desc = desc.replace('提供详细产品对比表', 'provides detailed product comparison table');
  desc = desc.replace('了解更多功能和价格对比，找到最适合你的方案！专业评测助你决策！', 'Learn more about features and pricing to find your best solution! Professional review helps your decision!');

  return desc;
}

function translateContent(chineseContent) {
  // For full content translation, we'll need more sophisticated handling
  // This is a simplified version that handles structural elements

  let content = chineseContent;

  // Headers
  content = content.replace(/<h1>(.*?)<\/h1>/g, (match, text) => {
    return `<h1>${translateTitle(text)}</h1>`;
  });

  content = content.replace(/<h2>(.*?)<\/h2>/g, (match, text) => {
    return `<h2>${translateTitle(text)}</h2>`;
  });

  content = content.replace(/<h3>(.*?)<\/h3>/g, (match, text) => {
    return `<h3>${translateTitle(text)}</h3>`;
  });

  // Common content patterns
  content = content.replace('核心功能：', 'Core Features:');
  content = content.replace('技术特点：', 'Technical Features:');
  content = content.replace('定价策略：', 'Pricing Strategy:');
  content = content.replace('核心能力：', 'Core Capabilities:');
  content = content.replace('优势：', 'Advantages:');
  content = content.replace('劣势：', 'Disadvantages:');
  content = content.replace('对比维度', 'Comparison Dimension');
  content = content.replace('对比总结', 'Comparison Summary');
  content = content.replace('选择建议', 'Selection Recommendations');
  content = content.replace('行业趋势预测', 'Industry Trend Predictions');
  content = content.replace('核心挑战', 'Core Challenges');
  content = content.replace('流程一：', 'Process 1:');
  content = content.replace('流程二：', 'Process 2:');
  content = content.replace('流程三：', 'Process 3:');
  content = content.replace('流程四：', 'Process 4:');

  return content;
}

function processFile(inputPath, outputPath) {
  const data = JSON.parse(fs.readFileSync(inputPath, 'utf8'));

  // Create English version
  const englishData = {
    title: translateTitle(data.title),
    description: translateDescription(data.description),
    content: translateContent(data.content),
    seo_keywords: data.seo_keywords, // Keep keywords as they're already in English
    slug: data.slug,
    published_at: data.published_at,
    author: data.author
  };

  fs.writeFileSync(outputPath, JSON.stringify(englishData, null, 2));
  return true;
}

// Process all categories
const categories = [
  'medical-equipment-rental-tools',
  'mining-extraction-tools',
  'music-audio-production',
  'nonprofit-charity-tools',
  'optometry-eye-care-tools',
  'paintball-laser-tag-rental-tools'
];

const baseDir = '/Users/gejiayu/owner/seo/data';
let processedCount = 0;

for (const category of categories) {
  const categoryDir = path.join(baseDir, category);
  const files = fs.readdirSync(categoryDir).filter(f => f.endsWith('.json'));

  console.log(`Processing ${category}: ${files.length} files`);

  for (const file of files) {
    const inputPath = path.join(categoryDir, file);
    const outputPath = path.join(categoryDir, file); // Overwrite with English

    processFile(inputPath, outputPath);
    processedCount++;

    if (processedCount % 20 === 0) {
      console.log(`Progress: ${processedCount} files processed`);
    }
  }
}

console.log(`\nTotal files processed: ${processedCount}`);