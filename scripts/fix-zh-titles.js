const fs = require('fs');
const path = require('path');

const dataDir = '/Users/gejiayu/owner/seo/data';
const dirs = ['scooter-moped-rental-tools', 'portable-sanitation-rental-tools', 'medical-equipment-rental-tools'];

// Translation mappings for common patterns
const titleTranslations = {
  'Best Electric Scooter': '电动滑板车',
  'Analytics Platforms': '数据分析平台',
  'Booking Systems': '预订系统',
  'Customer Experience Management Systems': '客户体验管理系统',
  'Dynamic Pricing System': '动态定价系统',
  'Employee Management System': '员工管理系统',
  'Fleet Management Software': '车队管理软件',
  'GPS Tracking Systems': 'GPS追踪系统',
  'Insurance Management Systems': '保险管理系统',
  'Maintenance Management System': '维护管理系统',
  'Mobile App Management System': '移动应用管理系统',
  'Payment Processing Systems': '支付处理系统',
  'Data Analytics Platform': '数据分析平台',
  'Rental Management System': '租赁管理系统',
  'Safety Compliance Systems': '安全合规系统',
  'Sustainability Management System': '可持续发展管理系统',
  'Motorcycle Rental': '摩托车租赁',
  'Scooter Rental': '滑板车租赁',
  'Top 5': '五大',
  'Complete Guide': '完全指南',
  'Ultimate Guide': '终极指南',
  '2026': '2026年',
  'Small Business': '中小企业',
  'Guide': '指南',
  'Review': '评测',
  'Portable Sanitation': '便携卫生间',
  'Medical Equipment Rental': '医疗设备租赁',
  'Management System': '管理系统'
};

function translateTitle(title) {
  let zhTitle = title;
  for (const [en, zh] of Object.entries(titleTranslations)) {
    zhTitle = zhTitle.replace(new RegExp(en, 'gi'), zh);
  }
  // Clean up any remaining English patterns
  zhTitle = zhTitle.replace(/: /g, '：');
  zhTitle = zhTitle.replace(/ vs /gi, ' vs ');
  return zhTitle;
}

function translateDescription(desc) {
  // Common description patterns
  let zhDesc = desc;
  zhDesc = zhDesc.replace(/Compare the top/gi, '对比五大');
  zhDesc = zhDesc.replace(/Discover features, pricing, and expert ratings/gi, '了解功能、价格和专家评级');
  zhDesc = zhDesc.replace(/Find your perfect/gi, '找到最适合你的');
  zhDesc = zhDesc.replace(/solution today/gi, '解决方案');
  zhDesc = zhDesc.replace(/electric scooter/gi, '电动滑板车');
  zhDesc = zhDesc.replace(/rentals in 2026/gi, '租赁2026年');
  zhDesc = zhDesc.replace(/Comprehensive comparison/gi, '全面对比');
  zhDesc = zhDesc.replace(/providing decision support/gi, '提供决策支持');
  zhDesc = zhDesc.replace(/Learn more/gi, '了解更多');
  zhDesc = zhDesc.replace(/Professional reviews/gi, '专业评测');
  return zhDesc;
}

function fixZhFile(zhFile, enFile) {
  try {
    const zhData = JSON.parse(fs.readFileSync(zhFile, 'utf8'));
    const enData = JSON.parse(fs.readFileSync(enFile, 'utf8'));
    
    // Check if title/description are in English (not Chinese)
    if (zhData.title && !zhData.title.match(/[一-龥]/)) {
      zhData.title = translateTitle(enData.title);
    }
    
    if (zhData.description && !zhData.description.match(/[一-龥]/)) {
      zhData.description = translateDescription(enData.description);
    }
    
    // Ensure author is Chinese
    if (zhData.author && !zhData.author.match(/[一-龥]/)) {
      zhData.author = '租赁管理专家';
    }
    
    fs.writeFileSync(zhFile, JSON.stringify(zhData, null, 2));
    return { fixed: true, file: zhFile };
  } catch (err) {
    return { error: true, message: err.message };
  }
}

let results = { fixed: 0, errors: [] };

dirs.forEach(dir => {
  const dirPath = path.join(dataDir, dir);
  const zhFiles = fs.readdirSync(dirPath)
    .filter(f => f.endsWith('-zh.json'))
    .map(f => path.join(dirPath, f));
  
  zhFiles.forEach(zhFile => {
    const enFile = zhFile.replace('-zh.json', '.json');
    if (fs.existsSync(enFile)) {
      const result = fixZhFile(zhFile, enFile);
      if (result.fixed) results.fixed++;
      else if (result.error) results.errors.push(result);
    }
  });
});

console.log(JSON.stringify(results, null, 2));
