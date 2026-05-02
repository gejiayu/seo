const fs = require('fs');
const path = require('path');

// Translation helper - basic word replacements
const translations = {
  // Common terms
  'software': '软件',
  'platform': '平台',
  'system': '系统',
  'tool': '工具',
  'tools': '工具',
  'management': '管理',
  'best': '最佳',
  'top': '顶级',
  'comparison': '对比',
  'guide': '指南',
  'review': '评测',
  '2026': '2026年',
  'complete': '完整',
  'comprehensive': '全面',
  'ultimate': '终极',
  'solution': '解决方案',
  'solutions': '解决方案',
  'for': '适用于',
  'small': '小型',
  'business': '企业',
  'businesses': '企业',
  'organization': '组织',
  'organizations': '组织',
  'features': '功能',
  'pricing': '定价',
  'implementation': '实施',
  'benefits': '效益',
  'analysis': '分析',
  'enterprise': '企业级',
  'rental': '租赁',
  'equipment': '设备',
  'audio': '音频',
  'video': '视频',
  'event': '活动',
  'events': '活动',
  'nonprofit': '非营利',
  'charity': '慈善',
  'donor': '捐赠者',
  'volunteer': '志愿者',
  'grant': '资助',
  'crowdfunding': '众筹',
  'crm': 'CRM',
  'analytics': '分析',
  'marketing': '营销',
  'operations': '运营',
  'scheduling': '调度',
  'booking': '预订',
  'inventory': '库存',
  'maintenance': '维护',
  'tracking': '追踪',
  'report': '报告',
  'reports': '报告',
  'dashboard': '仪表板',
  'integration': '集成',
  'automation': '自动化',
  'workflow': '工作流',
  'mobile': '移动',
  'app': '应用',
  'application': '应用',
  'security': '安全',
  'data': '数据',
  'customer': '客户',
  'team': '团队',
  'project': '项目',
  'financial': '财务',
  'accounting': '会计',
  'payment': '支付',
  'insurance': '保险',
  'legal': '法律',
  'compliance': '合规',
  'healthcare': '医疗',
  'medical': '医疗',
  'wellness': '健康',
  'telemedicine': '远程医疗',
  'dental': '牙科',
  'practice': '诊所',
  'hospital': '医院',
  'clinic': '诊所',
  'automotive': '汽车',
  'auto': '汽车',
  'dealer': '经销商',
  'repair': '维修',
  'banking': '银行',
  'loan': '贷款',
  'beauty': '美容',
  'salon': '沙龙',
  'pos': 'POS',
  'restaurant': '餐厅',
  'hospitality': '酒店',
  'travel': '旅行',
  'tour': '旅游',
  'agency': '代理',
  'visa': '签证',
  'document': '文档',
  'supplier': '供应商',
  'maritime': '海事',
  'shipping': '航运',
  'container': '集装箱',
  'marine': '海洋',
  'renewable': '可再生能源',
  'solar': '太阳能',
  'wind': '风力',
  'power': '电力',
  'energy': '能源',
  'music': '音乐',
  'production': '制作',
  'studio': '工作室',
  'plugin': '插件',
  'pet': '宠物',
  'services': '服务',
  'smart': '智能',
  'ecosystem': '生态',
  'hiking': '徒步',
  'climbing': '攀岩',
  'gear': '装备',
  'home': '家居',
  'renovation': '装修',
  'party': '派对',
  'supplies': '用品',
  'staging': '舞台',
  'rigging': '索具',
  'truss': '桁架',
  'quality': '质量',
  'collaboration': '协作',
  'promotion': '推广',
  'brand': '品牌',
  'image': '形象',
  'cybersecurity': '网络安全',
  'it': 'IT',
  'threat': '威胁',
  'intelligence': '情报',
  'testing': '测试',
  'risk': '风险',
  'orchestration': '编排',
  'zero': '零',
  'trust': '信任',
  'access': '访问',
  'identity': '身份',
  'verification': '验证',
  'microsegmentation': '微分段',
  'architecture': '架构',

  // Action verbs
  'manage': '管理',
  'track': '追踪',
  'schedule': '调度',
  'book': '预订',
  'rent': '租赁',
  'analyze': '分析',
  'report': '报告',
  'integrate': '集成',
  'automate': '自动化',
  'optimize': '优化',
  'streamline': '简化',
  'improve': '改善',
  'enhance': '增强',
  'boost': '提升',
  'increase': '增加',
  'reduce': '减少',
  'save': '节省',
  'protect': '保护',
  'secure': '安全',

  // Adjectives
  'professional': '专业',
  'advanced': '高级',
  'modern': '现代化',
  'efficient': '高效',
  'powerful': '强大',
  'flexible': '灵活',
  'scalable': '可扩展',
  'intuitive': '直观',
  'comprehensive': '全面',
  'detailed': '详细',
  'specialized': '专业化',
  'purpose-built': '专用',
  'industry-leading': '行业领先',
  'enterprise-grade': '企业级',
  'cloud-based': '云端',

  // Phrases
  'small business': '小型企业',
  'for small business': '适用于小型企业',
  'comparison for': '对比评测',
  'review 2026': '2026年评测',
  'guide 2026': '2026年指南',
  'complete guide': '完整指南',
  'best practices': '最佳实践',
  'feature comparison': '功能对比',
  'pricing comparison': '定价对比',
  'roi analysis': 'ROI分析',
  'implementation guide': '实施指南',
};

function translateTitle(title) {
  let translated = title;

  // Replace common patterns
  translated = translated.replace(/Best/gi, '最佳');
  translated = translated.replace(/Top/gi, '顶级');
  translated = translated.replace(/Complete Guide/gi, '完整指南');
  translated = translated.replace(/Guide/gi, '指南');
  translated = translated.replace(/Comparison/gi, '对比');
  translated = translated.replace(/Review/gi, '评测');
  translated = translated.replace(/2026/g, '2026年');
  translated = translated.replace(/for Small Business/gi, '适用于小型企业');
  translated = translated.replace(/Management/gi, '管理');
  translated = translated.replace(/Software/gi, '软件');
  translated = translated.replace(/System/gi, '系统');
  translated = translated.replace(/Platform/gi, '平台');
  translated = translated.replace(/Tools/gi, '工具');
  translated = translated.replace(/Solutions/gi, '解决方案');
  translated = translated.replace(/: /gi, '｜');

  return translated;
}

function translateDescription(desc) {
  let translated = desc;

  // Replace common patterns
  translated = translated.replace(/comprehensive/gi, '全面');
  translated = translated.replace(/detailed/gi, '详细');
  translated = translated.replace(/review/gi, '评测');
  translated = translated.replace(/comparison/gi, '对比');
  translated = translated.replace(/guide/gi, '指南');
  translated = translated.replace(/features/gi, '功能');
  translated = translated.replace(/pricing/gi, '定价');
  translated = translated.replace(/implementation/gi, '实施');
  translated = translated.replace(/strategies/gi, '策略');
  translated = translated.replace(/2026/g, '2026年');
  translated = translated.replace(/software/gi, '软件');
  translated = translated.replace(/platform/gi, '平台');
  translated = translated.replace(/system/gi, '系统');
  translated = translated.replace(/tools/gi, '工具');
  translated = translated.replace(/management/gi, '管理');
  translated = translated.replace(/business/gi, '企业');
  translated = translated.replace(/Find the best/gi, '寻找最佳');
  translated = translated.replace(/Compare/gi, '对比');
  translated = translated.replace(/Learn/gi, '了解');

  return translated;
}

function translateKeywords(keywords) {
  return keywords.map(kw => {
    let translated = kw;
    Object.keys(translations).forEach(en => {
      if (kw.toLowerCase().includes(en.toLowerCase())) {
        translated = translated.replace(new RegExp(en, 'gi'), translations[en]);
      }
    });
    return translated;
  });
}

function createZhFromEn(enPath, zhPath) {
  const enData = JSON.parse(fs.readFileSync(enPath, 'utf8'));

  const zhData = {
    title: translateTitle(enData.title),
    description: translateDescription(enData.description),
    content: enData.content, // Will need manual translation for content
    seo_keywords: translateKeywords(enData.seo_keywords || []),
    slug: enData.slug + '-zh',
    published_at: enData.published_at,
    author: enData.author,
    language: 'zh-CN',
    canonical_link: `https://www.housecar.life/zh/posts/${enData.slug}-zh`,
    alternate_links: {
      'en-US': `https://www.housecar.life/posts/${enData.slug}`,
      'zh-CN': `https://www.housecar.life/zh/posts/${enData.slug}-zh`
    }
  };

  fs.writeFileSync(zhPath, JSON.stringify(zhData, null, 2));
  console.log(`Created: ${zhPath}`);
}

function createEnFromZh(zhPath, enPath) {
  const zhData = JSON.parse(fs.readFileSync(zhPath, 'utf8'));

  // Extract base slug (remove -zh suffix if present)
  const baseSlug = zhData.slug.replace(/-zh$/, '');

  const enData = {
    title: zhData.title // Will need manual translation
      .replace(/｜/gi, ': ')
      .replace(/最佳/gi, 'Best')
      .replace(/顶级/gi, 'Top')
      .replace(/完整指南/gi, 'Complete Guide')
      .replace(/指南/gi, 'Guide')
      .replace(/对比/gi, 'Comparison')
      .replace(/评测/gi, 'Review')
      .replace(/2026年/g, '2026')
      .replace(/适用于小型企业/gi, 'for Small Business')
      .replace(/管理/gi, 'Management')
      .replace(/软件/gi, 'Software')
      .replace(/系统/gi, 'System')
      .replace(/平台/gi, 'Platform')
      .replace(/工具/gi, 'Tools')
      .replace(/解决方案/gi, 'Solutions'),
    description: zhData.description // Will need manual translation
      .replace(/全面/gi, 'comprehensive')
      .replace(/详细/gi, 'detailed')
      .replace(/评测/gi, 'review')
      .replace(/对比/gi, 'comparison')
      .replace(/指南/gi, 'guide')
      .replace(/功能/gi, 'features')
      .replace(/定价/gi, 'pricing')
      .replace(/实施/gi, 'implementation')
      .replace(/策略/gi, 'strategies')
      .replace(/2026年/g, '2026')
      .replace(/软件/gi, 'software')
      .replace(/平台/gi, 'platform')
      .replace(/系统/gi, 'system')
      .replace(/工具/gi, 'tools')
      .replace(/管理/gi, 'management')
      .replace(/企业/gi, 'business'),
    content: zhData.content, // Will need manual translation
    seo_keywords: zhData.seo_keywords.map(kw => kw
      .replace(/软件/gi, 'software')
      .replace(/平台/gi, 'platform')
      .replace(/系统/gi, 'system')
      .replace(/工具/gi, 'tools')
      .replace(/管理/gi, 'management')
      .replace(/租赁/gi, 'rental')
      .replace(/设备/gi, 'equipment')),
    slug: baseSlug,
    published_at: zhData.published_at,
    author: zhData.author,
    language: 'en-US',
    canonical_link: `https://www.housecar.life/posts/${baseSlug}`,
    alternate_links: {
      'en-US': `https://www.housecar.life/posts/${baseSlug}`,
      'zh-CN': `https://www.housecar.life/zh/posts/${zhData.slug}`
    }
  };

  fs.writeFileSync(enPath, JSON.stringify(enData, null, 2));
  console.log(`Created: ${enPath}`);
}

// Main execution
const dataDir = '/Users/gejiayu/owner/seo/data';

// Find English files without Chinese counterpart
const enCategories = fs.readdirSync(dataDir).filter(f =>
  fs.statSync(path.join(dataDir, f)).isDirectory() && f !== 'zh'
);

let createdCount = 0;

enCategories.forEach(category => {
  const enCatDir = path.join(dataDir, category);
  const zhCatDir = path.join(dataDir, 'zh', category);

  if (!fs.existsSync(zhCatDir)) {
    fs.mkdirSync(zhCatDir, { recursive: true });
  }

  const enFiles = fs.readdirSync(enCatDir).filter(f => f.endsWith('.json'));

  enFiles.forEach(enFile => {
    const enPath = path.join(enCatDir, enFile);
    const zhFileName = enFile.replace('.json', '-zh.json');
    const zhPath = path.join(zhCatDir, zhFileName);

    if (!fs.existsSync(zhPath)) {
      createZhFromEn(enPath, zhPath);
      createdCount++;
    }
  });
});

// Find Chinese files without English counterpart
const zhCategories = fs.readdirSync(path.join(dataDir, 'zh'));

zhCategories.forEach(category => {
  const zhCatDir = path.join(dataDir, 'zh', category);
  const enCatDir = path.join(dataDir, category);

  if (!fs.existsSync(enCatDir)) {
    return; // Skip if English category doesn't exist
  }

  const zhFiles = fs.readdirSync(zhCatDir).filter(f => f.endsWith('-zh.json'));

  zhFiles.forEach(zhFile => {
    const zhPath = path.join(zhCatDir, zhFile);
    const enFileName = zhFile.replace('-zh.json', '.json');
    const enPath = path.join(enCatDir, enFileName);

    if (!fs.existsSync(enPath)) {
      createEnFromZh(zhPath, enPath);
      createdCount++;
    }
  });
});

console.log(`\nTotal files created: ${createdCount}`);
console.log('Note: Content field needs manual translation refinement.');