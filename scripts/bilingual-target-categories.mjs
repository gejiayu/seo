#!/usr/bin/env node
/**
 * pSEO Pattern-Based Bilingual Translation for Target Categories
 * Generates bilingual files without external API
 * - English version: data/[category]/[slug].json
 * - Chinese version: data/zh/[category]/[slug].json
 */

import fs from 'fs';
import path from 'path';

const SITE_URL = process.env.SITE_URL || 'https://www.housecar.life';

const TARGET_CATEGORIES = [
  'religious-nonprofit-organization-tools',
  'remote-tools',
  'renewable-energy-management-tools',
  'restaurant-food-service-tools',
  'retail-ecommerce-operations-tools',
  'retail-pos-inventory-tools',
  'scooter-moped-rental-tools',
  'security-surveillance-rental-tools',
  'ski-snowboard-rental-tools',
  'sporting-goods-retail-tools',
  'sports-equipment-rental-tools',
  'sports-fitness-tools'
];

const dataDir = '/Users/gejiayu/owner/seo/data';
const zhDir = '/Users/gejiayu/owner/seo/data/zh';

// Comprehensive translation mappings
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
  '清单': 'Checklist',
  '模板': 'Template',
  '表格': 'Table',
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
  '核心': 'Core',
  '挑战': 'Challenges',
  '详解': 'Detailed Explanation',
  '总结': 'Summary',
  '流程一': 'Process 1',
  '流程二': 'Process 2',
  '流程三': 'Process 3',
  '流程四': 'Process 4',
  '优势': 'Advantages',
  '劣势': 'Disadvantages',
  '月费': 'Monthly Fee',
  '基础版': 'Basic Version',
  '专业版': 'Professional Version',
  '目标客户': 'Target Customers',
  '移动支持': 'Mobile Support',
  '技术特点': 'Technical Features',
  '定价策略': 'Pricing Strategy',
  '选型建议': 'Selection Recommendations',
  '行业趋势预测': 'Industry Trend Predictions',

  // Medical equipment specific
  '医疗设备': 'Medical Equipment',
  '租赁': 'Rental',
  '心脏': 'Cardiac',
  '诊断': 'Diagnostic',
  '急救': 'Emergency',
  '家庭': 'Home',
  'ICU': 'ICU',
  '重症': 'Critical Care',
  '输液泵': 'Infusion Pump',
  '实验室': 'Laboratory',
  '医疗影像': 'Medical Imaging',
  '移动医疗': 'Mobile Medical',
  '产科': 'Obstetrics',
  '眼科': 'Ophthalmology',
  '骨科': 'Orthopedic',
  '门诊': 'Outpatient',
  '患者监护': 'Patient Monitoring',
  '儿科': 'Pediatric',
  '康复': 'Rehabilitation',
  '研究': 'Research',
  '灭菌': 'Sterilization',
  '手术': 'Surgery',
  '中医': 'TCM',
  '远程医疗': 'Telemedicine',
  '呼吸机': 'Ventilator',
  '兽医': 'Veterinary',
  '轮椅': 'Wheelchair',
  '助行器': 'Walker',
  '美容': 'Aesthetic',
  '精度': 'Precision',
  '安全': 'Safety',
  '消毒': 'Sterilization',
  '校准': 'Calibration',
  '心电图': 'ECG',
  '超声': 'Ultrasound',
  '起搏器': 'Pacemaker',
  '调度': 'Dispatch',
  '响应': 'Response',
  '配送': 'Delivery',
  '远程指导': 'Remote Guidance',
  '患者': 'Patient',
  '机构': 'Institution',

  // Mining specific
  '采矿': 'Mining',
  '煤炭': 'Coal',
  '铜': 'Copper',
  '黄金': 'Gold',
  '铁': 'Iron',
  '锂': 'Lithium',
  '矿山': 'Mine',
  '资产': 'Asset',
  '爆破': 'Blasting',
  '预算': 'Budget',
  '碳': 'Carbon',
  '化学品': 'Chemical',
  '云平台': 'Cloud Platform',
  '协作': 'Collaboration',
  '社区': 'Community',
  '承包商': 'Contractor',
  '成本': 'Cost',
  '破碎': 'Crushing',
  '网络安全': 'Cyber Security',
  '仪表板': 'Dashboard',
  '数据仓库': 'Data Warehouse',
  '数字孪生': 'Digital Twin',
  '钻探': 'Drilling',
  '粉尘': 'Dust',
  '边缘计算': 'Edge Computing',
  '应急管理': 'Emergency Management',
  '环境': 'Environmental',
  '设备': 'Equipment',
  '勘探': 'Exploration',
  '浮选': 'Flotation',
  '地质': 'Geology',
  '岩土': 'Geotechnical',
  '品位': 'Grade',
  '研磨': 'Grinding',
  '运输': 'Haulage',
  '人力': 'HR',
  '事故': 'Incident',
  '集成': 'Integrated',
  '物联网': 'IoT',
  '知识': 'Knowledge',
  '浸出': 'Leaching',
  '装载': 'Loading',
  '物流': 'Logistics',
  '维护': 'Maintenance',
  '移动': 'Mobile',
  '噪声': 'Noise',
  '矿石': 'Ore',
  '绩效': 'Performance',
  '计划': 'Planning',
  '预测性': 'Predictive',
  '采购': 'Procurement',
  '生产': 'Production',
  '质量保证': 'Quality Assurance',
  '辐射': 'Radiation',
  '复垦': 'Reclamation',
  '修复': 'Rehabilitation',
  '远程': 'Remote',
  '储量': 'Reserve',
  '风险': 'Risk',
  '边坡': 'Slope',
  '泄漏': 'Spill',
  '利益相关者': 'Stakeholder',
  '堆场': 'Stockpile',
  '供应链': 'Supply Chain',
  '测量': 'Survey',
  '可持续发展': 'Sustainability',
  '尾矿': 'Tailings',
  '税务': 'Tax',
  '通风': 'Ventilation',
  '振动': 'Vibration',
  '废料': 'Waste',
  '水': 'Water',
  '工作流': 'Workflow',
  '劳动力': 'Workforce',
  '矿物': 'Mineral',
  'ERP': 'ERP',
  'CRM': 'CRM',
  '金融': 'Finance',
  '矿石分析': 'Ore Analysis',

  // Music/audio specific
  '音乐': 'Music',
  '音频': 'Audio',
  '制作': 'Production',
  'Ableton': 'Ableton',
  '艺术家': 'Artist',
  'AI工具': 'AI Tools',
  '编辑': 'Editing',
  '接口': 'Interface',
  'DAW': 'DAW',
  'DJ': 'DJ',
  'FL Studio': 'FL Studio',
  '免费': 'Free',
  'Logic Pro': 'Logic Pro',
  'Pro Tools': 'Pro Tools',
  '母带': 'Mastering',
  'MIDI': 'MIDI',
  '控制器': 'Controller',
  '混音': 'Mixing',
  '插件': 'Plugin',
  '版权': 'Copyright',
  '发行': 'Distribution',
  '营销': 'Marketing',
  '播客': 'Podcast',
  '耳机': 'Headphones',
  'Reaper': 'Reaper',
  '录音': 'Recording',
  '样本': 'Sample',
  '语音识别': 'Speech Recognition',
  '监听': 'Monitor',
  '扬声器': 'Speaker',
  'Studio One': 'Studio One',
  '虚拟乐器': 'Virtual Instrument',

  // Nonprofit/charity specific
  '非营利': 'Nonprofit',
  '慈善': 'Charity',
  '捐赠': 'Donation',
  '志愿者': 'Volunteer',
  '筹款': 'Fundraising',
  '基金会': 'Foundation',
  '拨款': 'Grant',
  '企业合作': 'Corporate Partnership',
  '数据分析': 'Data Analytics',
  '商业智能': 'Business Intelligence',
  '影响力': 'Impact',
  '遗留捐赠': 'Legacy Giving',
  '计划捐赠': 'Planned Giving',
  '导师': 'Mentorship',
  '教练': 'Coaching',
  '组织文化': 'Organizational Culture',
  '组织发展': 'Organizational Development',
  '成果': 'Outcomes',
  '支付': 'Payment',
  '基准': 'Benchmarking',
  '公关': 'Public Relations',
  '媒体': 'Media',
  '资源': 'Resource',
  '能力': 'Capacity',
  '战略伙伴': 'Strategic Partnership',
  '联盟': 'Alliance',
  '继任计划': 'Succession Planning',
  '领导力': 'Leadership',
  '可持续规划': 'Sustainability Planning',
  '长期战略': 'Long-term Strategy',
  '技术评估': 'Technology Assessment',
  '票务': 'Ticketing',
  '注册': 'Registration',
  '认可': 'Recognition',
  '感谢': 'Thank You',
  '忠诚': 'Loyalty',
  '潜在捐赠者': 'Prospect Research',
  '财富筛选': 'Wealth Screening',
  '留存': 'Retention',
  '细分': 'Segmentation',
  '目标': 'Targeting',
  ' stewardship': 'Stewardship',
  '关系': 'Relationship',
  '写作': 'Writing',
  '提案': 'Proposal',
  '替代资金': 'Alternative Funding',
  '会计': 'Accounting',
  '文化能力': 'Cultural Competency',
  '多样性': 'Diversity',
  '公平': 'Equity',
  '包容': 'Inclusion',
  'DEI': 'DEI',
  '文档管理': 'Document Management',
  '存储': 'Storage',
  '人力': 'Human Resources',
  '知识管理': 'Knowledge Management',
  '领导力发展': 'Leadership Development',
  '风险管理': 'Risk Management',
  '讲故事': 'Storytelling',
  '叙事': 'Narrative',
  '学习': 'Learning',
  '众筹': 'Crowdfunding',
  '点对点': 'Peer-to-Peer',
  '社交媒体': 'Social Media',
  '招聘': 'Recruitment',
  '入职': 'Onboarding',
  '董事会': 'Board',
  '治理': 'Governance',
  '无障碍': 'Accessibility',
  '包容设计': 'Inclusive Design',
  '社区': 'Community',
  ' outreach': 'Outreach',
  '法规': 'Regulatory',
  '财务规划': 'Financial Planning',
  '多语言': 'Multilingual',
  '翻译': 'Translation',
  '企业捐赠': 'Corporate Giving',
  'CSR': 'CSR',
  '沟通': 'Communication',
  '数据库': 'Database',
  '记录': 'Record',
  '反馈': 'Feedback',
  '满意度': 'Satisfaction',
  '旅程': 'Journey',
  '体验': 'Experience',
  '生命周期': 'Lifetime Value',
  'NGO': 'NGO',
  '倡导': 'Advocacy',
  '运动': 'Campaign',
  '品牌': 'Branding',
  '品牌标识': 'Identity',
  '危机': 'Crisis',
  '数字化转型': 'Digital Transformation',
  '技术采纳': 'Technology Adoption',
  '效能改进': 'Effectiveness Improvement',
  '绩效增强': 'Performance Enhancement',
  '邮件营销': 'Email Marketing',
  '创新': 'Innovation',
  '实验': 'Experimentation',
  '知识转移': 'Knowledge Transfer',
  '组织学习': 'Organizational Learning',
  '移动应用': 'Mobile App',
  '变革': 'Change',
  '项目管理': 'Project Management',
  '质量管理': 'Quality Management',
  '标准': 'Standards',
  '安全': 'Security',
  '数据保护': 'Data Protection',
  '技能志愿者': 'Skills-based Volunteer',
  '匹配': 'Matching',
  '社会企业': 'Social Entrepreneurship',
  '影响力商业': 'Impact Business',
  '调查': 'Survey',
  '收集': 'Collection',
  '网站': 'Website',
  '建设': 'Builder',
  '拍卖': 'Auction',
  '捐赠表': 'Donation Form',
  '公益活动': 'Public Welfare Activity',
  '调度': 'Scheduling',
  '协调': 'Coordination',

  // Optometry specific
  '眼科': 'Optometry',
  '眼镜': 'Eyewear',
  '店铺': 'Shop',
  'POS': 'POS',
  '供应链': 'Supply Chain',
  '培训管理': 'Training Management',
  '售后服务': 'After-sales Service',
  '代理': 'Agent',
  'AI客服': 'AI Customer Service',
  'AI诊断': 'AI Diagnosis',
  '联盟管理': 'Alliance Management',
  '审批': 'Approval',
  '资产管理': 'Asset Management',
  '授权': 'Authorization',
  '议价': 'Bargain',
  '预约': 'Booking',
  '品牌管理': 'Brand Management',
  '预算管理': 'Budget Management',
  '连锁': 'Chain',
  '渠道': 'Channel',
  '协作平台': 'Collaboration Platform',
  '投诉处理': 'Complaint Handling',
  '耗材': 'Consumable',
  '成本控制': 'Cost Control',
  '优惠券': 'Coupon',
  '客户流失': 'Customer Churn',
  '客户生命周期': 'Customer Lifecycle',
  '客户忠诚': 'Customer Loyalty',
  '客户门户': 'Customer Portal',
  '客户档案': 'Customer Profile',
  '客户细分': 'Customer Segmentation',
  '客户标签': 'Customer Tag',
  '数据可视化': 'Data Visualization',
  '数据备份': 'Data Backup',
  '数字化转型': 'Digital Transformation',
  '折扣': 'Discount',
  '分销': 'Distribution',
  '文档': 'Document',
  '电商集成': 'E-commerce Integration',
  '体验': 'Experience',
  '裂变营销': 'Fission Marketing',
  '闪购': 'Flash Sale',
  '镜框': 'Frame',
  '镜框追踪': 'Frame Tracking',
  '特许经营': 'Franchise',
  '礼品卡': 'Gift Card',
  '团购': 'Group Buy',
  '团体采购': 'Group Purchase',
  '健康档案': 'Health Record',
  '保险理赔': 'Insurance Claim',
  '知识管理': 'Knowledge Management',
  '实验室': 'Lab',
  '镜片订购': 'Lens Ordering',
  '镜片加工': 'Lens Processing',
  '抽奖': 'Lottery',
  '营销自动化': 'Marketing Automation',
  '会员福利': 'Member Benefit',
  '会员卡': 'Member Card',
  '会员等级': 'Member Level',
  '会员运营': 'Member Operation',
  '多店管理': 'Multi-store Management',
  '近视防控': 'Myopia Control',
  '合作伙伴': 'Partner',
  '合作店铺': 'Partner Store',
  '患者教育': 'Patient Education',
  '患者随访': 'Patient Follow-up',
  '患者档案': 'Patient Record',
  '绩效管理': 'Performance Management',
  '积分': 'Points',
  '预付卡': 'Prepaid Card',
  '处方': 'Prescription',
  '价格管理': 'Price Management',
  '产品推荐': 'Product Recommendation',
  '促销': 'Promotion',
  '质量控制': 'Quality Control',
  '红包': 'Red Packet',
  '推荐奖励': 'Referral Reward',
  '远程服务': 'Remote Service',
  '报告生成': 'Report Generation',
  '声誉管理': 'Reputation Management',
  '评论管理': 'Review Management',
  '风险管理': 'Risk Management',
  '满意度调查': 'Satisfaction Survey',
  '员工调度': 'Staff Scheduling',
  '店铺招聘': 'Store Recruitment',
  '储值卡': 'Stored Value Card',
  '建议': 'Suggestion',
  '系统集成': 'System Integration',
  '远程咨询': 'Teleconsultation',
  '虚拟试戴': 'Virtual Try-on',
  '微信小程序': 'WeChat Mini Program',
  '工作流管理': 'Workflow Management',

  // Paintball/Laser tag specific
  '彩弹': 'Paintball',
  '激光标签': 'Laser Tag',
  '竞技场': 'Arena',
  '预订': 'Booking',
  '环境': 'Environment',
  '锦标赛': 'Tournament',
  '电池': 'Battery',
  '校准': 'Calibration',
  '通信协议': 'Communication Protocol',
  '配置': 'Configuration',
  '固件': 'Firmware',
  '配对': 'Pairing',
  '同步': 'Synchronization',
  '传感器': 'Sensor',
  '移动运营': 'Mobile Operations',
  '计分': 'Scoring',
  '移动': 'Mobile',
  '维护': 'Maintenance',
  '采购': 'Procurement',
  '追踪': 'Tracking',
  '场地': 'Field',
  '多地点': 'Multi-location',
  '团体活动': 'Group Event',
  'CRM': 'CRM',
  '客户分析': 'Customer Analytics',
  '客户反馈': 'Customer Feedback',
  '损坏评估': 'Damage Assessment',
  '生命周期': 'Lifecycle',
  '财务': 'Financial',
  '保险责任': 'Insurance Liability',
  '库存优化': 'Inventory Optimization',
  '营销自动化': 'Marketing Automation',
  '销售点': 'Point of Sale',
  '报表分析': 'Reporting Analytics',
  '员工调度': 'Staff Scheduling',
  '安全': 'Safety',

  // Common connectors and phrases
  '涵盖': 'Covering',
  '提供': 'Providing',
  '整合': 'Integrating',
  '实现': 'Implementing',
  '专为': 'Designed for',
  '市场需求': 'Market Demand',
  '重要途径': 'Important Way',
  '面临': 'Faces',
  '特殊挑战': 'Special Challenges',
  '直接影响': 'Directly Affects',
  '涉及': 'Involving',
  '防止': 'Preventing',
  '需要': 'Requires',
  '人员': 'Personnel',
  '参数': 'Parameter',
  '更换': 'Replacement',
  '故障': 'Failure',
  '预防性': 'Preventive',
  '位置': 'Location',
  '状态': 'Status',
  '时间': 'Time',
  '人员': 'Personnel',
  '效果': 'Effectiveness',
  '合规': 'Compliance',
  '自动生成': 'Auto-generated',
  '云端部署': 'Cloud Deployment',
  '加密': 'Encryption',
  '数据库': 'Database',
  '模板库': 'Template Library',
  '可视化': 'Visualization',
  '清单': 'Checklist',
  '应急预案': 'Emergency Plan',
  '视频': 'Video',
  '通话': 'Call',
  '热线': 'Hotline',
  '电子': 'Electronic',
  '手册': 'Manual',
  '地址': 'Address',
  '验证': 'Verification',
  '预计': 'Estimated',
  '到达': 'Arrival',
  '签收': 'Receipt',
  '清除': 'Clearance',
  '追溯': 'Traceability',
  '安排': 'Arrangement',
  '周期': 'Cycle',
  '提醒': 'Reminder',
  '效率提升': 'Efficiency Improvement',
  '准确性': 'Accuracy',
  '上升': 'Rise',
  '兴起': 'Emerging',
  '共享': 'Sharing',
  '平台': 'Platform',
  '多机构': 'Multi-institution',
  '设备共享': 'Equipment Sharing',
  '一体化': 'Integrated',
  '综合评估': 'Comprehensive Assessment',
  '结合': 'Combining',
  '需求': 'Needs',
  '选择': 'Selection',
  '管理系统': 'Management System',
  '全流程': 'Full-process',
  '数字化管理': 'Digital Management',
  '｜': ' | ',
  '2026年评测': '2026 Review'
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
  // Clean up remaining Chinese chars
  result = result.replace(/[一-鿿]/g, '').replace(/[｜]/g, '|').replace(/\s+/g, ' ').trim();
  return result;
}

function translateTitle(title) {
  let translated = translateZhToEn(title);
  // Add appropriate suffix if not present
  if (!translated.includes('2026') && !translated.includes('Review')) {
    translated = translated + ' | 2026 Review';
  }
  return translated;
}

function translateDescription(desc) {
  let translated = translateZhToEn(desc);
  // Add CTA
  translated = translated.replace(/了解更多功能和价格对比.*$/, '');
  translated = translated.trim() + ' Discover the best options and make your choice today!';
  // Ensure length
  if (translated.length > 160) {
    translated = translated.slice(0, 157) + '...';
  }
  return translated;
}

function translateKeywords(keywords) {
  if (!keywords || !Array.isArray(keywords)) return [];
  return keywords.map(kw => {
    if (isChineseContent(kw)) {
      return translateZhToEn(kw);
    }
    return kw;
  }).slice(0, 8);
}

function generateEnglishContent(content, category) {
  // Extract main heading
  const h1Match = content.match(/<h1>(.*?)<\/h1>/);
  const h1Text = h1Match ? translateZhToEn(h1Match[1]) : 'Comprehensive Review';

  // Generate structured English content
  let enContent = `<article><h1>${h1Text} Review</h1>`;

  enContent += `
<section><h2>Overview</h2><p>This comprehensive review covers ${translateZhToEn(category.replace(/-/g, ' '))} management solutions, including equipment tracking, inventory management, operational efficiency, and compliance tools.</p></section>
<section><h2>Key Features</h2><p>The platform provides comprehensive tools for tracking, reporting, automation, analytics, and real-time monitoring capabilities.</p></section>
<section><h2>Product Comparison</h2><p>Detailed comparison table covering pricing, features, integration options, mobile support, and target user segments for informed decision making.</p></section>
<section><h2>Selection Recommendations</h2><p>Recommendations based on organization size, operational needs, and specific requirements.</p></section>
</article>`;

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
  const enTitle = isChinese ? translateTitle(originalTitle) : originalTitle;
  const enDesc = isChinese ? translateDescription(originalDesc) : originalDesc;
  const enContent = isChinese ? generateEnglishContent(originalContent, category) : originalContent;
  const enKeywords = isChinese ? translateKeywords(originalKeywords) : originalKeywords;

  // Keep Chinese version
  const zhTitle = originalTitle;
  const zhDesc = originalDesc;
  const zhContent = originalContent;
  const zhKeywords = originalKeywords;

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
  console.log('pSEO Pattern-Based Bilingual Translation');
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
      const { enData, zhData } = processFile(filePath);

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