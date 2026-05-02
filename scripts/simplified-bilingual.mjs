#!/usr/bin/env node
/**
 * pSEO Bilingual Translation (Simplified)
 * For Chinese files: Generate clean English from slug + category
 * For English files: Keep original, generate Chinese version
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

// Category-specific title templates
const TITLE_TEMPLATES = {
  'laundry-dry-cleaning-tools': {
    'management-software': 'Laundry Shop Management Software',
    'booking': 'Laundry Shop Booking System',
    'crm': 'Laundry Shop CRM System',
    'pos': 'Laundry Shop POS System',
    'delivery': 'Laundry Delivery Management',
    'inventory': 'Laundry Shop Inventory Management',
    'staff': 'Laundry Shop Staff Management',
    'customer': 'Laundry Shop Customer Management',
    'equipment': 'Laundry Shop Equipment Management',
    'financial': 'Laundry Shop Financial Management',
    'marketing': 'Laundry Shop Marketing Software',
    'quality': 'Laundry Shop Quality Control',
    'pricing': 'Laundry Shop Pricing Strategy',
    'digital': 'Laundry Shop Digital Transformation',
    'ai': 'Laundry Shop AI Intelligent System',
    'payment': 'Laundry Shop Online Payment',
    'membership': 'Dry Cleaning Membership Management',
    'complaint': 'Laundry Shop Complaint Handling',
    'feedback': 'Laundry Shop Feedback System',
    'notification': 'Laundry Shop Notification System',
    'analytics': 'Laundry Shop Data Analytics',
    'supplier': 'Laundry Shop Supplier Management',
    'process': 'Laundry Shop Service Process',
    'chain': 'Laundry Chain Shop Management',
    'self-service': 'Self-Service Laundry Shop',
    'dry-cleaning': 'Dry Cleaning',
    'laundry': 'Laundry Shop',
    'operation': 'Laundry Shop Operations',
    'complete-guide': 'Complete Guide'
  },
  'legal-compliance-tools': {
    'compliance': 'Compliance Management',
    'contract': 'Contract Management',
    'risk': 'Legal Risk Management',
    'ip': 'Intellectual Property',
    'patent': 'Patent Management',
    'trademark': 'Trademark Management',
    'copyright': 'Copyright Management',
    'gdpr': 'GDPR Compliance',
    'privacy': 'Privacy Compliance',
    'e-signature': 'E-Signature',
    'digital-signature': 'Digital Signature',
    'audit': 'Compliance Audit',
    'training': 'Compliance Training',
    'reporting': 'Compliance Reporting',
    'monitoring': 'Compliance Monitoring',
    'automation': 'Legal Automation',
    'workflow': 'Legal Workflow',
    'document': 'Legal Document',
    'template': 'Legal Template',
    'case': 'Case Management',
    'law-firm': 'Law Firm',
    'practice': 'Law Practice',
    'brand': 'Brand Protection',
    'consent': 'Consent Management',
    'policy': 'Policy Compliance',
    'regulatory': 'Regulatory Compliance',
    'corporate': 'Corporate Compliance'
  },
  'legal-document-management-tools': {
    'doc': 'Document',
    'document': 'Document',
    'management': 'Management',
    'archive': 'Archive',
    'version': 'Version Control',
    'template': 'Template',
    'workflow': 'Workflow',
    'search': 'Search',
    'ocr': 'OCR',
    'api': 'API',
    'mobile': 'Mobile',
    'cloud': 'Cloud',
    'backup': 'Backup',
    'classify': 'Classification',
    'index': 'Index',
    'merge': 'Merge',
    'split': 'Split',
    'convert': 'Convert',
    'compress': 'Compress',
    'watermark': 'Watermark',
    'secure': 'Security',
    'permission': 'Permission',
    'collab': 'Collaboration',
    'report': 'Reporting',
    'vs': 'Comparison'
  },
  'lighting-lamp-rental-tools': {
    'lighting': 'Lighting Lamp Rental',
    'lamp': 'Lamp Rental',
    'rental': 'Rental Management',
    'booking': 'Booking System',
    'inventory': 'Inventory System',
    'stage': 'Stage Lighting',
    'theater': 'Theater Lighting',
    'concert': 'Concert Lighting',
    'wedding': 'Wedding Lighting',
    'film': 'Film Lighting',
    'outdoor': 'Outdoor Lighting',
    'led': 'LED Lighting',
    'laser': 'Laser Lighting',
    'follow-spot': 'Follow Spot',
    'special-effect': 'Special Effect Lighting',
    'smart': 'Smart Lighting',
    'energy': 'Energy Saving',
    'control': 'Lighting Control',
    'scheduling': 'Lighting Scheduling',
    'logistics': 'Logistics Delivery',
    'insurance': 'Insurance Claims',
    'damage': 'Damage Assessment',
    'training': 'Operation Training',
    'sustainability': 'Sustainability',
    'api': 'API Integration',
    'cleaning': 'Cleaning Maintenance',
    'calculator': 'Price Calculator',
    'billing': 'Financial Billing',
    'crm': 'Customer CRM'
  },
  'logistics-supply-chain-tools': {
    'logistics': 'Logistics',
    'supply-chain': 'Supply Chain',
    'warehouse': 'Warehouse',
    'wms': 'Warehouse Management System',
    'tms': 'Transportation Management System',
    'oms': 'Order Management System',
    'srm': 'Supplier Management System',
    '3pl': '3PL Management',
    'fleet': 'Fleet Management',
    'carrier': 'Carrier Management',
    'tracking': 'Tracking',
    'route': 'Route Optimization',
    'delivery': 'Delivery',
    'last-mile': 'Last Mile Delivery',
    'cold-chain': 'Cold Chain',
    'cross-border': 'Cross Border',
    'customs': 'Customs Clearance',
    'freight': 'Freight',
    'container': 'Container',
    'pallet': 'Pallet',
    'inventory': 'Inventory',
    'forecasting': 'Demand Forecasting',
    'planning': 'Planning',
    'analytics': 'Analytics',
    'automation': 'Automation',
    'iot': 'IoT',
    'blockchain': 'Blockchain',
    'ai': 'AI Prediction',
    'robot': 'Robotics',
    'sorting': 'Sorting',
    'picking': 'Picking',
    'yard': 'Yard Management',
    'dock': 'Dock Scheduling',
    'audit': 'Audit',
    'settlement': 'Settlement',
    'insurance': 'Cargo Insurance',
    'hazardous': 'Hazardous Goods',
    'returns': 'Returns Processing',
    'green': 'Green Logistics',
    'visibility': 'Visibility',
    'collaboration': 'Collaboration',
    'control-tower': 'Control Tower'
  },
  'legal': {
    'privacy': 'Privacy Policy',
    'terms': 'Terms of Service',
    'about': 'About Us'
  }
};

function isChineseContent(text) {
  if (!text) return false;
  const chineseChars = (text.match(/[一-鿿]/g) || []).length;
  const totalChars = text.trim().length;
  return chineseChars > totalChars * 0.3;
}

function generateEnglishTitleFromSlug(slug, category) {
  // Clean slug and convert to title
  const parts = slug.split('-');

  // Build title from slug parts
  let titleParts = [];

  const templates = TITLE_TEMPLATES[category] || {};

  for (const part of parts) {
    // Skip year suffix
    if (part.match(/^\d{4}$/)) continue;

    // Try template match
    const templateKey = Object.keys(templates).find(k => part.includes(k));
    if (templateKey) {
      titleParts.push(templates[templateKey]);
    } else if (part === 'review') {
      titleParts.push('Review');
    } else if (part === 'comparison') {
      titleParts.push('Comparison');
    } else if (part === 'guide') {
      titleParts.push('Guide');
    } else if (part === 'tools') {
      titleParts.push('Tools');
    } else if (part === 'system') {
      titleParts.push('System');
    } else if (part === 'platform') {
      titleParts.push('Platform');
    } else if (part === 'software') {
      titleParts.push('Software');
    } else if (part === 'vs') {
      titleParts.push('vs');
    } else if (part === '2026') {
      continue;
    } else {
      // Capitalize first letter
      titleParts.push(part.charAt(0).toUpperCase() + part.slice(1));
    }
  }

  // Remove duplicates and build title
  titleParts = [...new Set(titleParts)];

  let title = titleParts.join(' ');

  // Add year suffix
  if (!title.includes('2026')) {
    title = title + ' - 2026 Review';
  }

  return title;
}

function generateEnglishDescription(category) {
  const templates = {
    'laundry-dry-cleaning-tools': 'Comprehensive review of laundry shop management solutions covering booking, customer management, inventory tracking, and operational efficiency. Discover the best options and make your choice today!',
    'legal-compliance-tools': 'Complete guide to compliance management software covering contract automation, IP tracking, regulatory compliance, and risk assessment. Discover the best options and make your choice today!',
    'legal-document-management-tools': 'Side-by-side comparison of legal document management platforms covering features, pricing, and implementation requirements. Discover the best options and make your choice today!',
    'lighting-lamp-rental-tools': 'Comprehensive review of lighting rental management solutions covering inventory, booking, maintenance, and logistics coordination. Discover the best options and make your choice today!',
    'logistics-supply-chain-tools': 'Complete guide to logistics and supply chain management covering warehouse, transportation, inventory, and demand forecasting. Discover the best options and make your choice today!',
    'legal': 'Legal documentation and policy information for our platform services.'
  };

  return templates[category] || 'Comprehensive review covering features, pricing, and selection recommendations. Discover the best options and make your choice today!';
}

function generateEnglishContent(category, slug) {
  let titleFromSlug = generateEnglishTitleFromSlug(slug, category).replace(' - 2026 Review', '');

  let content = `<article><h1>${titleFromSlug}</h1>`;

  if (category.includes('laundry')) {
    content += `
<section><h2>Overview</h2><p>This comprehensive review covers laundry and dry cleaning shop management solutions for 2026, including booking systems, customer management, inventory tracking, and operational efficiency tools.</p></section>
<section><h2>Key Features</h2><p>The system provides comprehensive tools for order tracking, customer CRM, inventory management, staff scheduling, and financial reporting with real-time monitoring capabilities.</p></section>
<section><h2>Product Comparison</h2><p>Detailed comparison table covering pricing, features, IoT integration, mobile support, and target user segments for informed decision making.</p></section>
<section><h2>Selection Recommendations</h2><p>Recommendations based on shop size, service type, and specific operational needs.</p></section>`;
  } else if (category.includes('legal-compliance')) {
    content += `
<section><h2>Overview</h2><p>This comprehensive review covers legal compliance management solutions for 2026, including contract lifecycle management, intellectual property tracking, regulatory compliance, and risk assessment tools.</p></section>
<section><h2>Key Features</h2><p>The platform provides comprehensive tools for contract automation, compliance monitoring, IP portfolio management, e-signature integration, and audit reporting.</p></section>
<section><h2>Product Comparison</h2><p>Detailed comparison covering automation capabilities, compliance frameworks, integration options, and pricing for enterprise and SMB segments.</p></section>
<section><h2>Selection Recommendations</h2><p>Guidance based on organization size, compliance requirements, and industry-specific regulatory needs.</p></section>`;
  } else if (category.includes('legal-document')) {
    content += `
<section><h2>Overview</h2><p>This comparison review covers legal document management platforms for 2026, including document automation, workflow management, archival systems, and collaboration tools.</p></section>
<section><h2>Key Features</h2><p>Side-by-side comparison of document generation, version control, search capabilities, OCR features, security compliance, and mobile access.</p></section>
<section><h2>Platform Comparison</h2><p>Detailed feature comparison including pricing tiers, implementation costs, training requirements, and ROI analysis.</p></section>
<section><h2>Selection Guide</h2><p>Decision framework based on law firm size, document volume, integration needs, and budget constraints.</p></section>`;
  } else if (category.includes('lighting')) {
    content += `
<section><h2>Overview</h2><p>This comprehensive review covers lighting and lamp rental management solutions for 2026 for events, concerts, theaters, and film production.</p></section>
<section><h2>Key Features</h2><p>The system provides inventory tracking, booking management, maintenance scheduling, damage assessment, logistics coordination, and financial reporting.</p></section>
<section><h2>Product Comparison</h2><p>Comparison of lighting-specific features including LED management, smart control, energy efficiency tracking, and API integration capabilities.</p></section>
<section><h2>Recommendations</h2><p>Guidance based on rental scale, lighting types, event categories, and operational complexity.</p></section>`;
  } else if (category.includes('logistics')) {
    content += `
<section><h2>Overview</h2><p>This comprehensive review covers logistics and supply chain management solutions for 2026, including warehouse management, transportation optimization, inventory tracking, and demand forecasting.</p></section>
<section><h2>Key Features</h2><p>The platform provides tools for WMS/TMS/OMS integration, route optimization, fleet management, real-time tracking, and analytics dashboards.</p></section>
<section><h2>Product Comparison</h2><p>Comparison covering automation capabilities, IoT integration, AI prediction features, blockchain traceability, and sustainability metrics.</p></section>
<section><h2>Selection Framework</h2><p>Decision guide based on logistics scale, mode requirements, technology needs, and budget considerations.</p></section>`;
  } else if (category === 'legal') {
    content += `
<section><h2>Overview</h2><p>Legal policy and compliance documentation for our platform operations.</p></section>
<section><h2>Key Points</h2><p>Terms of service, privacy policy, user rights, and compliance commitments.</p></section>`;
  } else {
    content += `
<section><h2>Overview</h2><p>Comprehensive review and analysis of management solutions for this industry category in 2026.</p></section>
<section><h2>Key Features</h2><p>Core functionality including tracking, reporting, automation, and analytics capabilities.</p></section>
<section><h2>Selection Guide</h2><p>Recommendations based on specific operational requirements and budget considerations.</p></section>`;
  }

  content += '</article>';
  return content;
}

function generateEnglishKeywords(category) {
  const keywords = {
    'laundry-dry-cleaning-tools': ['laundry shop management', 'dry cleaning software', 'laundry booking system', 'laundry CRM', 'laundry POS'],
    'legal-compliance-tools': ['compliance management', 'legal software', 'contract management', 'compliance automation', 'GRC platform'],
    'legal-document-management-tools': ['legal document management', 'law firm software', 'document automation', 'legal workflow', 'e-signature legal'],
    'lighting-lamp-rental-tools': ['lighting rental', 'stage lighting software', 'event lighting management', 'lamp rental system', 'lighting booking'],
    'logistics-supply-chain-tools': ['logistics management', 'supply chain software', 'warehouse management', 'TMS', 'WMS'],
    'legal': ['legal policy', 'privacy policy', 'terms of service']
  };

  return keywords[category] || ['management software', 'business tools', 'software review', 'comparison', 'guide'];
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
  let enTitle, enDesc, enContent, enKeywords;

  if (isChinese) {
    // Generate clean English from slug + category
    enTitle = generateEnglishTitleFromSlug(slug, category);
    enDesc = generateEnglishDescription(category);
    enContent = generateEnglishContent(category, slug);
    enKeywords = generateEnglishKeywords(category);
  } else {
    // Keep original English content
    enTitle = originalTitle;
    enDesc = originalDesc;
    enContent = originalContent;
    enKeywords = Array.isArray(originalKeywords) ? originalKeywords : [];
  }

  // Chinese version: always keep original content
  const zhTitle = originalTitle;
  const zhDesc = originalDesc;
  const zhContent = originalContent;
  const zhKeywords = Array.isArray(originalKeywords) ? originalKeywords : [];

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
  console.log('pSEO Bilingual Translation (Simplified)');
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
  let chineseCount = 0;
  let englishCount = 0;

  for (let i = 0; i < allFiles.length; i++) {
    const filePath = allFiles[i];

    try {
      const { enData, zhData } = processFile(filePath);

      const category = path.dirname(filePath).split('/').pop();
      const slug = enData.slug;

      if (isChineseContent(zhData.title)) {
        chineseCount++;
      } else {
        englishCount++;
      }

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
        console.log(`  Chinese: ${chineseCount}, English: ${englishCount}`);
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
  console.log(`Chinese original: ${chineseCount}`);
  console.log(`English original: ${englishCount}`);
  console.log('=' .repeat(60));
}

main();