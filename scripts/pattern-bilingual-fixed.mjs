#!/usr/bin/env node
/**
 * pSEO Pattern-Based Bilingual Translation (Fixed)
 * Generates bilingual files without external API
 */

import fs from 'fs';
import path from 'path';

const SITE_URL = process.env.SITE_URL || 'https://www.housecar.life';

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

// Comprehensive translation mappings with spaces preserved
const ZH_TO_EN = {
  // Common terms
  '评测': 'Review',
  '对比': 'Comparison',
  '指南': 'Guide',
  '工具': 'Tools',
  '系统': 'System',
  '平台': 'Platform',
  '软件': 'Software',
  '管理': 'Management',
  '解决方案': 'Solution',
  '深度': 'Comprehensive',
  '专业': 'Professional',
  '全面': 'Complete',
  '最佳': 'Best',
  '推荐': 'Recommended',
  '分析': 'Analysis',
  '报告': 'Reporting',
  '追踪': 'Tracking',
  '监控': 'Monitoring',
  '自动化': 'Automation',
  '智能化': 'Intelligent',
  '数字化': 'Digital',
  '流程': 'Process',
  '流程图': 'Flowchart',
  '清单': 'Checklist',
  '模板': 'Template',
  '表格': 'Form',
  '文档': 'Document',
  '功能': 'Features',
  '价格': 'Pricing',
  '选型': 'Selection',
  '行业': 'Industry',
  '趋势': 'Trends',
  '建议': 'Recommendations',
  '策略': 'Strategy',
  '优化': 'Optimization',
  '效率': 'Efficiency',
  '数据': 'Data',
  '智能': 'Smart',
  '预测': 'Prediction',
  '预警': 'Alert',
  '审计': 'Audit',
  '合规': 'Compliance',
  '风控': 'Risk Control',
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

  // Laundry specific
  '洗衣店': 'Laundry Shop',
  '干洗店': 'Dry Cleaning Shop',
  '洗衣': 'Laundry',
  '干洗': 'Dry Cleaning',
  '衣物': 'Clothing',
  '洗涤': 'Washing',
  '预约': 'Booking',
  '配送': 'Delivery',
  '会员': 'Membership',
  '营销': 'Marketing',
  '定价': 'Pricing',
  '质量': 'Quality',
  '投诉': 'Complaint',
  '反馈': 'Feedback',
  '通知': 'Notification',
  '数据分析': 'Data Analytics',
  '数字化转型': 'Digital Transformation',
  '设备': 'Equipment',
  '连锁': 'Chain',
  '自助': 'Self-Service',
  '运营': 'Operations',
  '供应链': 'Supply Chain',
  '用品': 'Supplies',
  '供应商': 'Supplier',
  '财务': 'Financial',
  '在线支付': 'Online Payment',
  '会员管理': 'Membership Management',
  'CRM': 'CRM',
  'POS': 'POS',
  '员工': 'Staff',
  '服务质量': 'Service Quality',
  '智能系统': 'Intelligent System',
  '预订': 'Booking',
  '价格策略': 'Pricing Strategy',
  '完整指南': 'Complete Guide',

  // Legal specific
  '法律': 'Legal',
  '法务': 'Legal Department',
  '知识产权': 'Intellectual Property',
  '专利': 'Patent',
  '商标': 'Trademark',
  '版权': 'Copyright',
  '侵权': 'Infringement',
  '诉讼': 'Litigation',
  '仲裁': 'Arbitration',
  '律师': 'Lawyer',
  '律师事务所': 'Law Firm',
  '案例': 'Case',
  '证据': 'Evidence',
  '档案': 'Archive',
  '风险': 'Risk',
  '工作流': 'Workflow',
  '电子签名': 'E-Signature',
  '数字签名': 'Digital Signature',
  'GDPR': 'GDPR',
  '隐私': 'Privacy',
  '数据保护': 'Data Protection',
  '监管': 'Regulatory',
  '政策': 'Policy',
  '企业': 'Corporate',
  '资产': 'Asset',
  '估值': 'Valuation',
  '授权': 'Authorization',
  '许可': 'License',
  '申请': 'Application',
  '截止日期': 'Deadline',
  '组合': 'Portfolio',
  '品牌': 'Brand',
  '保护': 'Protection',
  '监测': 'Monitoring',
  '侵权检测': 'Infringement Detection',
  '搜索': 'Search',
  '预警': 'Watch',
  '分析': 'Analytics',
  '自动化': 'Automation',
  '起草': 'Drafting',
  '创建': 'Creation',
  '生命周期': 'Lifecycle',
  '签名': 'Signature',
  '跟踪': 'Tracking',
  '小型企业': 'Small Business',
  '条款库': 'Clause Library',
  '风险评估': 'Risk Assessment',
  '风险管理': 'Risk Management',
  '培训管理': 'Training Management',
  '报告': 'Reporting',
  '管理': 'Management',
  '平台': 'Platform',
  '品牌监测': 'Brand Monitoring',
  '品牌保护': 'Brand Protection',
  '内容许可': 'Content Licensing',
  '内容保护': 'Content Protection',
  '同意管理': 'Consent Management',
  '条款': 'Terms',
  '服务': 'Service',
  '隐私政策': 'Privacy Policy',
  '关于我们': 'About Us',

  // Lighting specific
  '灯具': 'Lighting',
  '灯光': 'Light',
  '租赁': 'Rental',
  '舞台': 'Stage',
  '剧院': 'Theater',
  '演出': 'Performance',
  '音乐会': 'Concert',
  '婚礼': 'Wedding',
  '电影': 'Film',
  '户外': 'Outdoor',
  'LED灯': 'LED Lamp',
  '激光灯': 'Laser Light',
  '追光': 'Follow Spot',
  '特效': 'Special Effects',
  '智能照明': 'Smart Lighting',
  '节能': 'Energy Saving',
  '调度': 'Scheduling',
  '预订': 'Booking',
  '物流': 'Logistics',
  '保险理赔': 'Insurance Claims',
  '损耗评估': 'Damage Assessment',
  '运营培训': 'Operation Training',
  '可持续': 'Sustainability',
  'API集成': 'API Integration',
  '清洁维护': 'Cleaning Maintenance',
  '控制': 'Control',
  '计算器': 'Calculator',
  '财务计费': 'Financial Billing',
  '客户CRM': 'Customer CRM',
  '演唱会': 'Concert',
  '活动照明': 'Event Lighting',
  '库存系统': 'Inventory System',

  // Logistics specific
  '物流': 'Logistics',
  '运输': 'Transportation',
  '仓储': 'Warehouse',
  '配送': 'Delivery',
  '末端': 'Last Mile',
  '冷链': 'Cold Chain',
  '跨境': 'Cross Border',
  '海关': 'Customs',
  '清关': 'Clearance',
  '货代': 'Freight Forwarding',
  '货运': 'Freight',
  '船运': 'Shipping',
  '空运': 'Air Freight',
  '陆运': 'Ground Freight',
  '多式联运': 'Multimodal',
  '集装箱': 'Container',
  '托盘': 'Pallet',
  '叉车': 'Forklift',
  '机器人': 'Robot',
  'AGV': 'AGV',
  '拣选': 'Picking',
  '分拣': 'Sorting',
  '上架': 'Put-away',
  '补货': 'Replenishment',
  '盘点': 'Cycle Counting',
  '布局': 'Layout',
  '货位': 'Slotting',
  '月台': 'Dock',
  '车队': 'Fleet',
  '司机': 'Driver',
  '路线': 'Route',
  '需求': 'Demand',
  '供应': 'Supply',
  '采购': 'Procurement',
  '协作': 'Collaboration',
  '可视化': 'Visibility',
  '控制塔': 'Control Tower',
  '弹性': 'Resilience',
  '金融': 'Finance',
  '结算': 'Settlement',
  '费率': 'Rate',
  '碳减排': 'Carbon Reduction',
  '绿色': 'Green',
  '环保': 'Environmental',
  '危险品': 'Hazardous',
  '危化品': 'Hazmat',
  '理赔': 'Claims',
  '追踪': 'Tracking',
  '包裹': 'Parcel',
  'OMS': 'OMS',
  'TMS': 'TMS',
  'WMS': 'WMS',
  'SRM': 'SRM',
  '3PL': '3PL',
  '区块链': 'Blockchain',
  '物联网': 'IoT',
  '数字孪生': 'Digital Twin',
  'OCR': 'OCR',
  '语音': 'Voice',
  '移动': 'Mobile',
  '安全': 'Security',
  '人力': 'Labor',
  '绩效': 'Performance',
  '质量': 'Quality',
  '退货': 'Returns',
  '逆向': 'Reverse',
  '越库': 'Cross Docking',
  '运时': 'Transit Time',
  'AI预测': 'AI Prediction',
  '预测引擎': 'Prediction Engine',
  '分析平台': 'Analytics Platform',
  'API集成': 'API Integration',
  '资产管理': 'Asset Management',
  '区块链追溯': 'Blockchain Traceability',
  'BPM工具': 'BPM Tools',
  '容量规划': 'Capacity Planning',
  '成本管理': 'Cost Management',
  '客户服务': 'Customer Service',
  '需求预测': 'Demand Forecasting',
  '数字化转型': 'Digital Transformation',
  '电子文档': 'E-Document',
  '环境管理': 'Environmental Management',
  '异常管理': 'Exception Management',
  '人力管理': 'HR Management',
  '智能调度': 'Intelligent Scheduling',
  'KPI仪表盘': 'KPI Dashboards',
  '管理系统': 'Management System',
  '移动应用': 'Mobile Applications',
  '网络安全': 'Network Security',
  'OCR扫描': 'OCR Scanning',
  '外包': 'Outsourcing',
  '绩效管理': 'Performance Management',
  '质量管理': 'Quality Management',
  '机器人操作系统': 'Robotics Operating Systems',
  '培训管理': 'Training Management',
  '语音拣选': 'Voice Picking',
  '劳动力调度': 'Workforce Scheduling',
  'yard管理': 'Yard Management',
  'yard调度': 'Yard Scheduling',
  'yard作业': 'Yard Jockey'
};

function isChineseContent(text) {
  if (!text) return false;
  const chineseChars = (text.match(/[一-鿿]/g) || []).length;
  const totalChars = text.trim().length;
  return chineseChars > totalChars * 0.3;
}

function translateZhToEn(text) {
  if (!text) return text;
  let result = text;

  // Sort by length (longest first) to avoid partial replacements
  const sortedEntries = Object.entries(ZH_TO_EN).sort((a, b) => b[0].length - a[0].length);

  for (const [zh, en] of sortedEntries) {
    result = result.replace(new RegExp(zh, 'g'), en);
  }

  // Clean up remaining Chinese characters and fix spacing
  result = result
    .replace(/[一-鿿]/g, '')
    .replace(/[｜]/g, '|')
    .replace(/[，]/g, ',')
    .replace(/[。]/g, '.')
    .replace(/[：]/g, ':')
    .replace(/[！]/g, '!')
    .replace(/[？]/g, '?')
    .replace(/\s+/g, ' ')  // Normalize spaces
    .trim();

  return result;
}

function translateTitle(title, direction) {
  let translated;

  if (direction === 'en') {
    translated = translateZhToEn(title);
    // Ensure proper spacing
    translated = translated.replace(/([a-z])([A-Z])/g, '$1 $2');  // Add space between lowercase and uppercase
    translated = translated.replace(/(\d{4})([A-Z])/g, '$1 $2');  // Add space after year
    translated = translated.replace(/([A-Z]+)([A-Z][a-z])/g, '$1 $2');  // Add space between acronyms and words

    // Add suffix if not present
    if (!translated.includes('2026')) {
      translated = translated + ' - 2026 Review';
    }
  } else {
    // For Chinese, keep original
    translated = title;
  }

  return translated;
}

function translateDescription(desc, direction) {
  let translated;

  if (direction === 'en') {
    translated = translateZhToEn(desc);
    translated = translated.replace(/了解更多功能和价格对比.*$/, '');

    // Ensure minimum length with CTA
    if (translated.length < 140) {
      translated = translated.trim() + ' Discover the best options and make your choice today!';
    }

    // Max length
    if (translated.length > 160) {
      translated = translated.slice(0, 157) + '...';
    }
  } else {
    // For Chinese, keep original
    translated = desc;
  }

  return translated;
}

function translateKeywords(keywords, direction) {
  if (!keywords || !Array.isArray(keywords)) return [];

  return keywords.map(kw => {
    if (direction === 'en' && isChineseContent(kw)) {
      return translateZhToEn(kw);
    }
    return kw;
  }).slice(0, 8);
}

function generateEnglishContent(content, category) {
  // For Chinese content, generate template English content
  const h1Match = content.match(/<h1>(.*?)<\/h1>/);
  const h1Text = h1Match ? translateZhToEn(h1Match[1]).replace(/([a-z])([A-Z])/g, '$1 $2') : 'Comprehensive Review';

  // Generate category-specific English content
  let enContent = `<article><h1>${h1Text}</h1>`;

  if (category.includes('laundry')) {
    enContent += `
<section><h2>Overview</h2><p>This comprehensive review covers laundry and dry cleaning shop management solutions for 2026, including booking systems, customer management, inventory tracking, and operational efficiency tools.</p></section>
<section><h2>Key Features</h2><p>The system provides comprehensive tools for order tracking, customer CRM, inventory management, staff scheduling, and financial reporting with real-time monitoring capabilities.</p></section>
<section><h2>Product Comparison</h2><p>Detailed comparison table covering pricing, features, IoT integration, mobile support, and target user segments for informed decision making.</p></section>
<section><h2>Selection Recommendations</h2><p>Recommendations based on shop size, service type, and specific operational needs.</p></section>`;
  } else if (category.includes('legal-compliance')) {
    enContent += `
<section><h2>Overview</h2><p>This comprehensive review covers legal compliance management solutions for 2026, including contract lifecycle management, intellectual property tracking, regulatory compliance, and risk assessment tools.</p></section>
<section><h2>Key Features</h2><p>The platform provides comprehensive tools for contract automation, compliance monitoring, IP portfolio management, e-signature integration, and audit reporting.</p></section>
<section><h2>Product Comparison</h2><p>Detailed comparison covering automation capabilities, compliance frameworks, integration options, and pricing for enterprise and SMB segments.</p></section>
<section><h2>Selection Recommendations</h2><p>Guidance based on organization size, compliance requirements, and industry-specific regulatory needs.</p></section>`;
  } else if (category.includes('legal-document')) {
    enContent += `
<section><h2>Overview</h2><p>This comparison review covers legal document management platforms for 2026, including document automation, workflow management, archival systems, and collaboration tools.</p></section>
<section><h2>Key Features</h2><p>Side-by-side comparison of document generation, version control, search capabilities, OCR features, security compliance, and mobile access.</p></section>
<section><h2>Platform Comparison</h2><p>Detailed feature comparison including pricing tiers, implementation costs, training requirements, and ROI analysis.</p></section>
<section><h2>Selection Guide</h2><p>Decision framework based on law firm size, document volume, integration needs, and budget constraints.</p></section>`;
  } else if (category.includes('lighting')) {
    enContent += `
<section><h2>Overview</h2><p>This comprehensive review covers lighting and lamp rental management solutions for 2026 for events, concerts, theaters, and film production.</p></section>
<section><h2>Key Features</h2><p>The system provides inventory tracking, booking management, maintenance scheduling, damage assessment, logistics coordination, and financial reporting.</p></section>
<section><h2>Product Comparison</h2><p>Comparison of lighting-specific features including LED management, smart control, energy efficiency tracking, and API integration capabilities.</p></section>
<section><h2>Recommendations</h2><p>Guidance based on rental scale, lighting types, event categories, and operational complexity.</p></section>`;
  } else if (category.includes('logistics')) {
    enContent += `
<section><h2>Overview</h2><p>This comprehensive review covers logistics and supply chain management solutions for 2026, including warehouse management, transportation optimization, inventory tracking, and demand forecasting.</p></section>
<section><h2>Key Features</h2><p>The platform provides tools for WMS/TMS/OMS integration, route optimization, fleet management, real-time tracking, and analytics dashboards.</p></section>
<section><h2>Product Comparison</h2><p>Comparison covering automation capabilities, IoT integration, AI prediction features, blockchain traceability, and sustainability metrics.</p></section>
<section><h2>Selection Framework</h2><p>Decision guide based on logistics scale, mode requirements, technology needs, and budget considerations.</p></section>`;
  } else if (category === 'legal') {
    enContent += `
<section><h2>Overview</h2><p>Legal policy and compliance documentation for our platform operations.</p></section>
<section><h2>Key Points</h2><p>Terms of service, privacy policy, user rights, and compliance commitments.</p></section>`;
  } else {
    enContent += `
<section><h2>Overview</h2><p>Comprehensive review and analysis of management solutions for this industry category in 2026.</p></section>
<section><h2>Key Features</h2><p>Core functionality including tracking, reporting, automation, and analytics capabilities.</p></section>
<section><h2>Selection Guide</h2><p>Recommendations based on specific operational requirements and budget considerations.</p></section>`;
  }

  enContent += '</article>';
  return enContent;
}

function generateCanonicalLink(slug) {
  return `${SITE_URL}/posts/${slug}`;
}

function generateAlternateLinks(slug) {
  return {
    'en-US': `${SITE_URL}/posts/${slug}`,
    'zh-CN': `${SITE_URL}/zh/posts/${slug}`
  };
}

function processFile(filePath) {
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
  const enTitle = isChinese ? translateTitle(originalTitle, 'en') : originalTitle;
  const enDesc = isChinese ? translateDescription(originalDesc, 'en') : originalDesc;
  const enContent = isChinese ? generateEnglishContent(originalContent, category) : originalContent;
  const enKeywords = isChinese ? translateKeywords(originalKeywords, 'en') : originalKeywords;

  // Generate Chinese version
  const zhTitle = isChinese ? originalTitle : originalTitle;
  const zhDesc = isChinese ? originalDesc : originalDesc;
  const zhContent = isChinese ? originalContent : originalContent;
  const zhKeywords = isChinese ? originalKeywords : originalKeywords;

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

function main() {
  console.log('pSEO Pattern-Based Bilingual Translation (Fixed)');
  console.log('=' .repeat(60));
  console.log(`Categories: ${TARGET_CATEGORIES.join(', ')}`);
  console.log('');

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
      const { enData, zhData } = processFile(filePath);

      const category = path.dirname(filePath).split('/').pop();
      const slug = enData.slug;

      // Write English version
      fs.writeFileSync(filePath, JSON.stringify(enData, null, 2), 'utf8');

      // Write Chinese version
      const zhCategoryDir = path.join(zhDir, category);
      if (!fs.existsSync(zhCategoryDir)) {
        fs.mkdirSync(zhCategoryDir, { recursive: true });
      }
      const zhFilePath = path.join(zhCategoryDir, `${slug}.json`);
      fs.writeFileSync(zhFilePath, JSON.stringify(zhData, null, 2), 'utf8');

      successCount++;

      if ((i + 1) % 20 === 0) {
        console.log(`Progress: ${i + 1}/${allFiles.length} - Success: ${successCount}, Error: ${errorCount}`);
        console.log(`  Latest: ${path.basename(filePath)}`);
      }

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

main();