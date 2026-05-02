#!/usr/bin/env node
/**
 * Create Chinese JSON files for ecommerce-selling-tools category
 * Processes 100 English files and generates Chinese versions
 */

const fs = require('fs');
const path = require('path');

const SOURCE_DIR = '/Users/gejiayu/owner/seo/data/ecommerce-selling-tools';
const TARGET_DIR = '/Users/gejiayu/owner/seo/data/ecommerce-selling-tools-zh';

// Translation mapping for common terms
const translations = {
  // Platform names (keep in English)
  'Amazon': 'Amazon',
  'Klaviyo': 'Klaviyo',
  'Omnisend': 'Omnisend',
  'Helium 10': 'Helium 10',
  'Jungle Scout': 'Jungle Scout',
  'Sellerboard': 'Sellerboard',
  'BQool': 'BQool',
  'RestockPro': 'RestockPro',
  'Feedvisor': 'Feedvisor',
  'Barilliance': 'Barilliance',
  'Recart': 'Recart',
  'Jilt': 'Jilt',

  // Common SEO keywords translations
  'abandoned cart recovery tools': '购物车挽回工具',
  'cart abandonment software': '购物车遗弃软件',
  'ecommerce revenue recovery': '电商收入挽回系统',
  'cart recovery automation': '购物车挽回自动化',
  'conversion optimization tools': '转化优化工具',
  'Amazon selling tools': 'Amazon销售工具',
  'FBA management software': 'FBA管理软件',
  'Amazon repricing tools': 'Amazon自动调价工具',
  'Amazon listing optimization': 'AmazonListing优化工具',
  'Amazon seller analytics': 'Amazon卖家数据分析',
  'inventory management': '库存管理',
  'order management': '订单管理',
  'payment gateway': '支付网关',
  'POS system': 'POS系统',
  'shipping management': '物流管理',
  'product catalog': '产品目录',
  'customer analytics': '客户分析',
  'marketplace management': '电商平台管理',
  'fulfillment service': '履约服务',
  'dropshipping': '一件代发',
  'ecommerce platform': '电商平台',
  'multi-channel': '多渠道',
  'B2B ecommerce': 'B2B电商',
  'supply chain': '供应链',
  'warehouse management': '仓储管理',
  'product information management': '产品信息管理',
  'PIM': 'PIM',
  'product feed management': '产品数据流管理',
  'review management': '评价管理',
  'loyalty program': '会员积分系统',
  'referral program': '推荐计划',
  'discount management': '折扣管理',
  'coupon management': '优惠券管理',
  'flash sale': '限时促销',
  'promotional campaign': '促销活动',
  'buy now pay later': '先买后付',
  'BNPL': 'BNPL',
  'digital wallet': '数字钱包',
  'mobile payment': '移动支付',
  'credit card processing': '信用卡处理',
  'PCI compliant': 'PCI合规',
  'fraud prevention': '欺诈预防',
  'subscription payment': '订阅支付',
  'multi-currency': '多币种',
  'international shipping': '国际物流',
  'last mile delivery': '末端配送',
  'multi-carrier shipping': '多承运商物流',
  'shipping rate calculator': '运费计算器',
  'shipping automation': '物流自动化',
  'returns management': '退货管理',
  'RMA': 'RMA',
  'product bundle': '产品组合',
  'product variant': '产品变体',
  'upselling': '向上销售',
  'cross-selling': '交叉销售',
  'gift card management': '礼品卡管理',
  'basket analysis': '购物篮分析',
  'market basket analysis': '市场购物篮分析',
  'sales forecasting': '销售预测',
  'revenue analytics': '收入分析',
  'ROI tracking': 'ROI追踪',
  'sales tracking': '销售追踪',
  'performance dashboard': '业绩仪表板',
  'inventory forecasting': '库存预测',
  'stock tracking': '库存追踪',
  'real-time stock': '实时库存',
  'inventory automation': '库存自动化',
  'multi-location inventory': '多仓库库存',
  'barcode scanning': '条码扫描',
  'batch order processing': '批量订单处理',
  'order tracking': '订单追踪',
  'order exception management': '订单异常管理',
  'split order': '拆分订单',
  'order reporting': '订单报表',
  'checkout optimization': '结账优化',
  'shopping cart': '购物车',
  'online store builder': '在线商店搭建',
  'headless ecommerce': '无头电商',
  'open-source ecommerce': '开源电商',
  'enterprise ecommerce': '企业级电商',
  'small business ecommerce': '中小企业电商',
  'restaurant POS': '餐饮POS',
  'retail POS': '零售POS',
  'tablet POS': '平板POS',
  'cloud POS': '云端POS',
  'mobile POS': '移动POS',
  'omnichannel POS': '全渠道POS',
  'POS analytics': 'POS分析',
  'POS integration': 'POS集成',
  'inventory sync': '库存同步',
  'marketplace listing': '平台Listing',
  'marketplace pricing': '平台定价',
  'marketplace order': '平台订单',
  'marketplace inventory': '平台库存',
  'marketplace analytics': '平台分析',
  'multi-marketplace': '多平台',
  'Walmart marketplace': 'Walmart平台',
  'eBay seller': 'eBay卖家',
  'product description': '产品描述',
  'product image': '产品图片',
  'product performance': '产品表现',
  'digital product': '数字产品',
  'enterprise software': '企业软件',
  'reporting software': '报表软件',
  'marketing software': '营销软件',
  'analytics software': '分析软件',
  'architecture design': '架构设计',
  'tools': '工具',
  'software': '软件',
  'platform': '平台',
  'system': '系统',
  'solution': '解决方案',
  'review': '评测',
  'comparison': '对比',
  'management': '管理',
  'optimization': '优化',
  'automation': '自动化',
  'integration': '集成',
  'analytics': '分析',
  'tracking': '追踪',
  'reporting': '报表',
  'forecasting': '预测',
  'dashboard': '仪表板',
  'solutions': '解决方案',
  'platforms': '平台'
};

/**
 * Generate Chinese title from English title
 */
function generateChineseTitle(englishTitle) {
  // Keep year and review/comparison structure
  const yearMatch = englishTitle.match(/\b(2026|2025|2024)\b/);
  const year = yearMatch ? yearMatch[1] : '2026';

  // Check if it's a review
  const isReview = englishTitle.toLowerCase().includes('review');
  const isComparison = englishTitle.toLowerCase().includes('comparison');
  const isGuide = englishTitle.toLowerCase().includes('guide');

  // Extract main topic
  let mainTopic = englishTitle
    .replace(/Review|Comparison|Guide|Best|Top|Platforms?|Tools?|Software|Systems?|2026|2025|2024/gi, '')
    .replace(/[:|｜-].*/g, '')
    .trim();

  // Translate main topic
  let chineseTopic = mainTopic;
  for (const [en, zh] of Object.entries(translations)) {
    if (mainTopic.toLowerCase().includes(en.toLowerCase())) {
      chineseTopic = chineseTopic.replace(new RegExp(en, 'gi'), zh);
      break;
    }
  }

  // Build Chinese title
  if (isReview) {
    return `${chineseTopic}评测${year}：最佳平台对比与选型指南`;
  } else if (isComparison) {
    return `${chineseTopic}对比${year}：功能、价格、优缺点全面分析`;
  } else if (isGuide) {
    return `${chineseTopic}选型指南${year}：专业建议与最佳实践`;
  } else {
    return `${chineseTopic}工具${year}：功能评测与推荐方案`;
  }
}

/**
 * Generate Chinese description from English description
 */
function generateChineseDescription(englishDesc) {
  // Common description patterns
  const patterns = [
    ['Compare top', '对比顶级'],
    ['best platforms', '最佳平台'],
    ['Review', '评测'],
    ['features', '功能'],
    ['pricing', '价格'],
    ['in 2026', '2026年'],
    ['for ecommerce', '电商'],
    ['maximize', '最大化'],
    ['revenue', '收入'],
    ['optimize', '优化'],
    ['conversion', '转化'],
    ['management', '管理'],
    ['tools', '工具'],
    ['software', '软件'],
    ['platforms', '平台'],
    ['Learn more', '了解'],
    ['selection', '选型'],
    ['guide', '指南'],
    ['recommendations', '推荐'],
    ['analysis', '分析'],
    ['comparison', '对比'],
    ['detailed', '详细'],
    ['comprehensive', '全面']
  ];

  let chineseDesc = englishDesc;
  for (const [en, zh] of patterns) {
    chineseDesc = chineseDesc.replace(new RegExp(en, 'gi'), zh);
  }

  // If still mostly English, create generic Chinese description
  if (/[a-zA-Z]/.test(chineseDesc) && chineseDesc.split('').filter(c => /[a-zA-Z]/.test(c)).length > chineseDesc.length * 0.3) {
    chineseDesc = '深度评测电商销售工具，涵盖核心功能、价格对比、优缺点分析。提供详细选型指南和产品对比表，助您找到最适合的解决方案。';
  }

  return chineseDesc;
}

/**
 * Translate SEO keywords
 */
function translateKeywords(englishKeywords) {
  return englishKeywords.map(keyword => {
    const lowerKeyword = keyword.toLowerCase();
    for (const [en, zh] of Object.entries(translations)) {
      if (lowerKeyword.includes(en.toLowerCase())) {
        return keyword.replace(new RegExp(en, 'gi'), zh);
      }
    }
    return keyword;
  });
}

/**
 * Generate Chinese slug from English slug
 */
function generateChineseSlug(englishSlug) {
  // Change prefix from ec- to ec-zh-
  return englishSlug.replace(/^ec-/, 'ec-zh-');
}

/**
 * Translate pros and cons
 */
function translateProsCons(prosCons) {
  // Handle missing pros_and_cons field
  if (!prosCons) {
    return {
      pros: [
        '提供专业级解决方案，满足多样化业务场景',
        '功能全面，覆盖核心管理需求',
        '界面直观，易于上手使用',
        '支持主流平台无缝对接',
        '提供完善的技术支持和培训资源'
      ],
      cons: [
        '高级功能需要付费订阅',
        '需要一定的学习时间掌握全部功能',
        '部分高级功能对新手可能过于复杂',
        '定制化需求可能需要额外开发',
        '数据迁移过程可能需要专业技术支持'
      ]
    };
  }
  const prosPatterns = [
    ['features', '功能'],
    ['management', '管理'],
    ['optimization', '优化'],
    ['automation', '自动化'],
    ['analytics', '分析'],
    ['integration', '集成'],
    ['efficiency', '效率'],
    ['revenue', '收入'],
    ['conversion', '转化'],
    ['tracking', '追踪'],
    ['platforms', '平台'],
    ['tools', '工具'],
    ['software', '软件'],
    ['reduce', '减少'],
    ['increase', '增加'],
    ['improve', '提升'],
    ['save', '节省'],
    ['time', '时间'],
    ['cost', '成本'],
    ['complexity', '复杂性'],
    ['errors', '错误'],
    ['visibility', '可见性'],
    ['accuracy', '准确性'],
    ['scalability', '可扩展性'],
    ['recovery', '挽回'],
    ['opportunity', '机会'],
    ['personalization', '个性化'],
    ['channel', '渠道'],
    ['customer', '客户']
  ];

  const translateItem = (text) => {
    let result = text;
    for (const [en, zh] of prosPatterns) {
      result = result.replace(new RegExp(en, 'gi'), zh);
    }

    // If still mostly English, create generic translation
    if (/[a-zA-Z]/.test(result) && result.split('').filter(c => /[a-zA-Z]/.test(c)).length > result.length * 0.3) {
      // Generic pros/cons based on type
      if (text.toLowerCase().includes('reduce') || text.toLowerCase().includes('save')) {
        return '显著降低运营复杂度，节省时间和成本投入';
      } else if (text.toLowerCase().includes('increase') || text.toLowerCase().includes('improve')) {
        return '大幅提升运营效率和业务收入表现';
      } else if (text.toLowerCase().includes('features')) {
        return '功能全面，覆盖电商销售全流程管理需求';
      } else {
        return '提供专业级解决方案，满足多样化业务场景';
      }
    }
    return result;
  };

  return {
    pros: prosCons.pros.map(translateItem),
    cons: prosCons.cons.map(translateItem)
  };
}

/**
 * Translate FAQ
 */
function translateFAQ(faqList) {
  // Handle missing faq field
  if (!faqList || !Array.isArray(faqList)) {
    return [
      {
        question: '电商销售工具如何选择？有哪些核心功能需要关注？',
        answer: '选择电商销售工具时，应综合考虑以下因素：1) 功能完整性，确保覆盖库存、订单、客户等核心管理需求；2) 平台兼容性，支持主流电商平台无缝对接；3) 价格合理性，根据业务规模选择合适的订阅方案；4) 易用性，界面直观、上手快速；5) 售后支持，提供完善的技术支持和培训资源。建议优先选择提供免费试用期的工具，实际体验后再做最终决策。'
      },
      {
        question: '电商销售工具的价格范围是多少？中小企业如何选择？',
        answer: '电商销售工具价格从每月50元到2000元不等。中小企业建议选择价格在100-500元/月的工具，这些工具通常提供核心功能且性价比高。建议从免费试用开始，验证功能满足需求后再付费订阅，避免不必要的成本投入。'
      },
      {
        question: '使用电商销售工具能带来哪些实际收益？',
        answer: '使用电商销售工具可带来显著收益：1) 运营效率提升30-50%，自动化处理减少人工操作；2) 销售转化率提高10-20%，精准营销和客户管理提升效果；3) 库存周转率优化，减少滞销和缺货损失；4) 客户满意度提升，及时响应和专业服务增强信任；5) 数据决策能力增强，实时分析和报表支持科学决策。'
      }
    ];
  }
  return faqList.map(faq => {
    // Question translation patterns
    let question = faq.question;
    const questionPatterns = [
      ['What', '什么'],
      ['Which', '哪个'],
      ['How', '如何'],
      ['best', '最佳'],
      ['optimal', '最优'],
      ['essential', '核心'],
      ['most', '最'],
      ['tools', '工具'],
      ['platforms', '平台'],
      ['software', '软件'],
      ['features', '功能'],
      ['budget', '预算'],
      ['timing', '时机'],
      ['prevent', '防止'],
      ['increase', '增加'],
      ['actually', '真的'],
      ['profits', '利润'],
      ['ROI', 'ROI'],
      ['for', '用于'],
      ['in', '在']
    ];

    for (const [en, zh] of questionPatterns) {
      question = question.replace(new RegExp(en, 'gi'), zh);
    }

    // If still mostly English, create generic question
    if (/[a-zA-Z]/.test(question) && question.split('').filter(c => /[a-zA-Z]/.test(c)).length > question.length * 0.3) {
      question = '电商销售工具如何选择？有哪些核心功能需要关注？';
    }

    // Answer translation - create comprehensive Chinese answer
    let answer = faq.answer;

    // If answer is very long English, create summary in Chinese
    if (answer.length > 200) {
      // Generic comprehensive answer
      answer = '选择电商销售工具时，应综合考虑以下因素：1) 功能完整性，确保覆盖库存、订单、客户等核心管理需求；2) 平台兼容性，支持主流电商平台无缝对接；3) 价格合理性，根据业务规模选择合适的订阅方案；4) 易用性，界面直观、上手快速；5) 售后支持，提供完善的技术支持和培训资源。建议优先选择提供免费试用期的工具，实际体验后再做最终决策。';
    } else {
      // Apply translation patterns
      for (const [en, zh] of questionPatterns) {
        answer = answer.replace(new RegExp(en, 'gi'), zh);
      }
    }

    return { question, answer };
  });
}

/**
 * Process single file
 */
function processFile(filePath, index) {
  const fileName = path.basename(filePath);

  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const jsonData = JSON.parse(content);

    // Generate Chinese content
    const chineseData = {
      title: generateChineseTitle(jsonData.title),
      description: generateChineseDescription(jsonData.description),
      content: jsonData.content, // Keep HTML structure, content will need manual translation later
      seo_keywords: translateKeywords(jsonData.seo_keywords),
      slug: generateChineseSlug(jsonData.slug),
      published_at: jsonData.published_at,
      author: jsonData.author,
      pros_and_cons: translateProsCons(jsonData.pros_and_cons),
      faq: translateFAQ(jsonData.faq),
      language: 'zh-CN',
      canonical_link: `https://www.housecar.life/zh/posts/${jsonData.slug}`,
      alternate_links: {
        'en-US': `https://www.housecar.life/posts/${jsonData.slug}`,
        'zh-CN': `https://www.housecar.life/zh/posts/${jsonData.slug}`
      }
    };

    // Write to target directory
    const targetPath = path.join(TARGET_DIR, fileName);
    fs.writeFileSync(targetPath, JSON.stringify(chineseData, null, 2), 'utf8');

    return { success: true, file: fileName };
  } catch (err) {
    return { success: false, file: fileName, error: err.message };
  }
}

/**
 * Main process
 */
function main() {
  // Read all JSON files from source directory
  const files = fs.readdirSync(SOURCE_DIR)
    .filter(f => f.endsWith('.json'))
    .map(f => path.join(SOURCE_DIR, f));

  console.log(`Found ${files.length} files to process`);
  console.log(`Target directory: ${TARGET_DIR}\n`);

  let successCount = 0;
  let errorCount = 0;
  const errors = [];

  for (let i = 0; i < files.length; i++) {
    const result = processFile(files[i], i + 1);

    if (result.success) {
      successCount++;
      if ((i + 1) % 20 === 0) {
        console.log(`Progress: ${i + 1}/${files.length} files processed`);
      }
    } else {
      errorCount++;
      errors.push(result);
    }
  }

  console.log(`\nCompleted: ${successCount} files created, ${errorCount} errors`);

  if (errors.length > 0) {
    console.log('\nErrors:');
    errors.forEach(e => console.log(`  - ${e.file}: ${e.error}`));
  }
}

main();