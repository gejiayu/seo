#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const sourceDir = '/Users/gejiayu/owner/seo/data/casino-gaming-entertainment-tools';
const targetDir = '/Users/gejiayu/owner/seo/data/zh/casino-gaming-entertainment-tools';

// Translation mapping for common terms
const translations = {
  // System names - keep original
  'Bally': 'Bally',
  'IGT': 'IGT',
  'GAMLS': 'GAMLS',
  'Synapse': 'Synapse',
  'WinSystems': 'WinSystems',

  // Common casino terms
  'Casino': '赌场',
  'casino': '赌场',
  'gaming': '游戏',
  'Gaming': '游戏',
  'player': '玩家',
  'Player': '玩家',
  'guest': '客户',
  'Guest': '客户',
  'loyalty': '忠诚',
  'Loyalty': '忠诚',
  'reward': '奖励',
  'Reward': '奖励',
  'bonus': '奖金',
  'Bonus': '奖金',
  'promotion': '促销',
  'Promotion': '促销',
  'VIP': 'VIP',
  'vip': 'VIP',

  // System terms
  'Management': '管理',
  'management': '管理',
  'System': '系统',
  'system': '系统',
  'Platform': '平台',
  'platform': '平台',
  'tracking': '追踪',
  'Tracking': '追踪',
  'analytics': '分析',
  'Analytics': '分析',
  'integration': '集成',
  'Integration': '集成',
  'monitoring': '监控',
  'Monitoring': '监控',

  // Financial terms
  'cash': '现金',
  'Cash': '现金',
  'financial': '财务',
  'Financial': '财务',
  'audit': '审计',
  'Audit': '审计',
  'compliance': '合规',
  'Compliance': '合规',
  'revenue': '收入',
  'Revenue': '收入',

  // Role translations
  'Expert': '专家',
  'Specialist': '专家',
  'Analyst': '分析师',
  'Manager': '经理',
  'Administrator': '管理员',
  'Director': '主管',
  'Consultant': '顾问',

  // Feature descriptions
  'comprehensive': '全面的',
  'Comprehensive': '全面的',
  'Excellent': '优秀的',
  'excellent': '优秀的',
  'Advanced': '先进的',
  'advanced': '先进的',
  'Standard': '标准的',
  'standard': '标准的',
  'Basic': '基础的',
  'basic': '基础的',
  'Full': '完整的',
  'full': '完整的',
  'Complete': '完整的',
  'complete': '完整的'
};

// Author translation mapping
const authorTranslations = {
  'Audio Visual Expert': '视听技术专家',
  'Audit Management Expert': '审计管理专家',
  'Bonus Management Expert': '奖金管理专家',
  'Cash Management Expert': '现金管理专家',
  'CRM Expert': 'CRM专家',
  'Customer Support Expert': '客户支持专家',
  'Data Analytics Expert': '数据分析专家',
  'Digital Signage Expert': '数字标牌专家',
  'Digital Wallet Expert': '数字钱包专家',
  'Email Marketing Expert': '邮件营销专家',
  'Environmental Monitoring Expert': '环境监控专家',
  'Facial Recognition Expert': '人脸识别专家',
  'Financial Management Expert': '财务管理专家',
  'Floor Design Expert': '楼层设计专家',
  'Gaming Chip Expert': '游戏筹码专家',
  'Gaming Machine Expert': '游戏机专家',
  'Guest Experience Expert': '客户体验专家',
  'Guest Feedback Expert': '客户反馈专家',
  'Headcount Occupancy Expert': '客流统计专家',
  'Hotel Reservation Expert': '酒店预订专家',
  'Identity Verification Expert': '身份验证专家',
  'Incident Management Expert': '事件管理专家',
  'Inventory Management Expert': '库存管理专家',
  'Kiosk Expert': '自助终端专家',
  'Live Dealer Expert': '真人荷官专家',
  'Loyalty Card Expert': '忠诚卡专家',
  'Loyalty Program Expert': '忠诚计划专家',
  'Machine Performance Expert': '机器性能专家',
  'Management Systems Expert': '管理系统专家',
  'Marketing Automation Expert': '营销自动化专家',
  'Mobile Application Expert': '移动应用专家',
  'Multi-Channel Marketing Expert': '多渠道营销专家',
  'Occupancy Management Expert': '占用管理专家',
  'Payment Processing Expert': '支付处理专家',
  'Player Acquisition Expert': '玩家获取专家',
  'Player Behavior Expert': '玩家行为专家',
  'Player Card Expert': '玩家卡专家',
  'Player Communication Expert': '玩家沟通专家',
  'Player Engagement Expert': '玩家参与专家',
  'Player Feedback Expert': '玩家反馈专家',
  'Player Identity Expert': '玩家身份专家',
  'Player Onboarding Expert': '玩家入门专家',
  'Player Profile Expert': '玩家档案专家',
  'Player Rating Expert': '玩家评级专家',
  'Player Reward Expert': '玩家奖励专家',
  'Player Segmentation Expert': '玩家细分专家',
  'Player Tracking Expert': '玩家追踪专家',
  'Predictive Analytics Expert': '预测分析专家',
  'Predictive Maintenance Expert': '预测维护专家',
  'Preferred Customer Expert': '优选客户专家',
  'Promotion Tracking Expert': '促销追踪专家',
  'Promotional Management Expert': '促销管理专家',
  'Property Management Expert': '物业管理专家',
  'Real-Time Monitoring Expert': '实时监控专家',
  'Real-Time Analytics Expert': '实时分析专家',
  'Revenue Management Expert': '收入管理专家',
  'Rewards Catalog Expert': '奖励目录专家',
  'Security Systems Expert': '安全系统专家',
  'Slot Machine Expert': '老虎机专家',
  'Slot Optimization Expert': '老虎机优化专家',
  'Slot Performance Expert': '老虎机性能专家',
  'Social Media Marketing Expert': '社交媒体营销专家',
  'Sports Betting Expert': '体育博彩专家',
  'Surveillance AI Expert': '监控AI专家',
  'Table Game Expert': '桌游专家',
  'Theft Prevention Expert': '防盗专家',
  'Ticket Redemption Expert': '票据兑换专家',
  'Tier-Based Loyalty Expert': '分层忠诚专家',
  'Tournament Management Expert': '锦标赛管理专家',
  'Tournament Prize Expert': '锦标赛奖品专家',
  'VIP Guest Expert': 'VIP客户专家',
  'VIP Player Expert': 'VIP玩家专家',
  'Wagering Tracking Expert': '投注追踪专家',
  'Web Analytics Expert': '网站分析专家',
  'Whale Player Expert': '鲸鱼玩家专家',
  'Wireless Communication Expert': '无线通信专家',
  'Workforce Management Expert': '员工管理专家'
};

function translateText(text) {
  let translated = text;

  // Replace common terms
  for (const [eng, chi] of Object.entries(translations)) {
    const regex = new RegExp(eng, 'g');
    translated = translated.replace(regex, chi);
  }

  return translated;
}

function translateAuthor(author) {
  return authorTranslations[author] || translateText(author);
}

function translateKeywords(keywords) {
  return keywords.map(kw => translateText(kw));
}

function translateTitle(title) {
  // Keep English product names, translate descriptive parts
  let translated = title;

  // Common title patterns
  if (title.includes('Top 10')) {
    translated = translated.replace('Top 10', '十大');
  }
  if (title.includes('- 2026 Review')) {
    translated = translated.replace('- 2026 Review', '对比2026');
  }
  if (title.includes('2026')) {
    translated = translated.replace('2026', '2026');
  }

  return translateText(translated);
}

function translateDescription(desc) {
  let translated = translateText(desc);

  // Add CTA at end if not present
  const ctaPhrases = ['立即了解', '阅读专业评测', '了解更多功能和价格', '找到最适合你的方案'];
  if (!ctaPhrases.some(cta => translated.includes(cta))) {
    translated += '立即了解完整评测，找到最适合你的方案！';
  }

  return translated;
}

function translateContent(content) {
  // Translate HTML content preserving structure
  let translated = content;

  // Translate h1-h3 headings
  translated = translated.replace(/<h1>(.*?)<\/h1>/g, (match, text) => {
    return `<h1>${translateText(text)}</h1>`;
  });
  translated = translated.replace(/<h2>(.*?)<\/h2>/g, (match, text) => {
    return `<h2>${translateText(text)}</h2>`;
  });
  translated = translated.replace(/<h3>(.*?)<\/h3>/g, (match, text) => {
    return `<h3>${translateText(text)}</h3>`;
  });

  // Translate paragraphs
  translated = translated.replace(/<p>(.*?)<\/p>/g, (match, text) => {
    return `<p>${translateText(text)}</p>`;
  });

  // Translate table headers and cells
  translated = translated.replace(/<th>(.*?)<\/th>/g, (match, text) => {
    return `<th>${translateText(text)}</th>`;
  });
  translated = translated.replace(/<td>(.*?)<\/td>/g, (match, text) => {
    return `<td>${translateText(text)}</td>`;
  });

  // Translate list items
  translated = translated.replace(/<li>(.*?)<\/li>/g, (match, text) => {
    return `<li>${translateText(text)}</li>`;
  });

  return translated;
}

// Read all source files
const files = fs.readdirSync(sourceDir).filter(f => f.endsWith('.json'));

console.log(`Processing ${files.length} files...`);

let processed = 0;
files.forEach(file => {
  try {
    const sourcePath = path.join(sourceDir, file);
    const targetPath = path.join(targetDir, file);

    // Read English JSON
    const english = JSON.parse(fs.readFileSync(sourcePath, 'utf8'));

    // Create Chinese translation
    const chinese = {
      title: translateTitle(english.title),
      description: translateDescription(english.description),
      content: translateContent(english.content),
      seo_keywords: translateKeywords(english.seo_keywords),
      slug: english.slug,
      published_at: english.published_at,
      author: translateAuthor(english.author),
      language: 'zh-CN',
      canonical_link: `https://www.housecar.life/posts/${english.slug}`,
      alternate_links: {
        'en-US': `https://www.housecar.life/posts/${english.slug}`,
        'zh-CN': `https://www.housecar.life/zh/posts/${english.slug}`
      },
      category: 'casino-gaming-entertainment-tools'
    };

    // Write Chinese JSON
    fs.writeFileSync(targetPath, JSON.stringify(chinese, null, 2), 'utf8');

    processed++;
    if (processed % 10 === 0) {
      console.log(`Processed ${processed}/${files.length} files`);
    }
  } catch (err) {
    console.error(`Error processing ${file}:`, err.message);
  }
});

console.log(`\n✅ Successfully processed ${processed}/${files.length} files`);
console.log(`Target directory: ${targetDir}`);