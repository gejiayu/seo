const fs = require('fs');
const path = require('path');

// Simple translation mappings for customer support domain
const translations = {
  // Common terms
  'AI': 'AI',
  'customer service': '客户服务',
  'customer support': '客户支持',
  'platform': '平台',
  'software': '软件',
  'tools': '工具',
  'management': '管理',
  'analytics': '分析',
  'integration': '集成',
  'automation': '自动化',
  'chatbot': '聊天机器人',
  'live chat': '在线聊天',
  'help desk': '服务台',
  'ticket': '工单',
  'agent': '客服代表',
  'call center': '呼叫中心',
  'contact center': '联络中心',
  'workflow': '工作流程',
  'dashboard': '仪表板',
  'monitoring': '监控',
  'tracking': '跟踪',
  'reporting': '报告',
  'feedback': '反馈',
  'survey': '调研',
  'knowledge base': '知识库',
  'FAQ': 'FAQ',
  'self-service': '自助服务',
  'remote support': '远程支持',
  'screen sharing': '屏幕共享',
  'video support': '视频支持',
  'email support': '邮件支持',
  'social media': '社交媒体',
  'multichannel': '多渠道',
  'omnichannel': '全渠道',
  'cloud': '云端',
  'enterprise': '企业',
  'small business': '中小企业',
  'response time': '响应时间',
  'resolution': '解决',
  'escalation': '升级',
  'satisfaction': '满意度',
  'performance': '性能',
  'metrics': '指标',
  'ROI': 'ROI',
  'cost': '成本',
  'benefits': '效益',
  'implementation': '实施',
  'deployment': '部署',
  'training': '培训',
  'security': '安全',
  'compliance': '合规',
  'features': '功能',
  'capabilities': '能力',
  'advantages': '优势',
  'limitations': '限制',
  'comparison': '对比',
  'vs': '对比',
  'review': '评测',
  '2026': '2026年',
  'platforms': '平台',
  'systems': '系统',
  'solutions': '解决方案',

  // Common phrases
  'Customer Service Platforms': '客户服务平台',
  'Traditional Support': '传统支持',
  'Call Center Software': '呼叫中心软件',
  'Help Desk Software': '服务台软件',
  'Live Chat Software': '在线聊天软件',
  'Chatbot Software': '聊天机器人软件',
  'Knowledge Base Tools': '知识库工具',
  'Remote Support Tools': '远程支持工具',
  'Email Support Software': '邮件支持软件',
  'Social Media Support': '社交媒体支持',
  'Customer Feedback Software': '客户反馈软件',
  'Support Analytics': '支持分析',
  'Ticket Management': '工单管理',
  'Agent Performance': '客服代表绩效',
  'Customer Satisfaction': '客户满意度',
  'Automation Tools': '自动化工具',
  'Integration Platforms': '集成平台',
};

// Translate title
function translateTitle(title) {
  // Handle common patterns
  let translated = title;

  // Replace common terms
  Object.keys(translations).forEach(key => {
    if (key !== 'AI' && key !== 'ROI' && key !== 'FAQ' && key !== '2026') {
      const regex = new RegExp(key, 'gi');
      translated = translated.replace(regex, translations[key]);
    }
  });

  // Handle "vs" pattern
  translated = translated.replace(/\s+vs\s+/gi, '对比');

  // Handle "2026" pattern
  translated = translated.replace(/2026/g, '2026年');

  // Handle "Review" pattern
  translated = translated.replace(/Review/gi, '评测');
  translated = translated.replace(/review/gi, '评测');

  // Handle comparison suffix
  translated = translated.replace(/Comparison/gi, '对比');
  translated = translated.replace(/comparison/gi, '对比');

  return translated;
}

// Translate description (keep it short and relevant for SEO)
function translateDescription(desc) {
  let translated = desc;

  // Basic translations
  Object.keys(translations).forEach(key => {
    if (key !== 'AI' && key !== 'ROI' && key !== 'FAQ') {
      const regex = new RegExp(key, 'gi');
      translated = translated.replace(regex, translations[key]);
    }
  });

  // Handle "Discover" pattern
  translated = translated.replace(/Discover/gi, '了解');
  translated = translated.replace(/Learn/gi, '了解');
  translated = translated.replace(/Compare/gi, '对比');
  translated = translated.replace(/Find/gi, '查找');
  translated = translated.replace(/Explore/gi, '探索');

  return translated;
}

// Translate SEO keywords
function translateKeywords(keywords) {
  return keywords.map(keyword => {
    let translated = keyword;

    Object.keys(translations).forEach(key => {
      if (key !== 'AI' && key !== 'ROI') {
        const regex = new RegExp(key, 'gi');
        translated = translated.replace(regex, translations[key]);
      }
    });

    // Handle 2026
    translated = translated.replace(/2026/g, '2026年');

    return translated;
  });
}

// Translate HTML content (basic approach - preserve structure)
function translateContent(content) {
  let translated = content;

  // Replace common English phrases with Chinese
  const phraseMap = {
    'Evolution of Customer Service': '客户服务的演进',
    'Comparison': '对比',
    'Core Capabilities': '核心能力',
    'Implementation Strategies': '实施策略',
    'Integration with Existing Systems': '与现有系统集成',
    'Cost-Benefit Analysis': '成本效益分析',
    'Limitations and Considerations': '限制与考量',
    'Future Development': '未来发展',
    'Strategic Recommendations': '战略建议',
    'Key Features': '关键功能',
    'Benefits': '效益',
    'How It Works': '工作原理',
    'Best Practices': '最佳实践',
    'Use Cases': '使用场景',
    'Pricing': '定价',
    'Getting Started': '开始使用',
    'Introduction': '引言',
    'Overview': '概述',
    'Conclusion': '结论',
    'Summary': '总结',
    'FAQ': '常见问题',
    'Pros and Cons': '优缺点',
    'Advantages': '优势',
    'Disadvantages': '劣势',
    'Winner': '最优',
    'Feature': '功能',
    'Traditional Support': '传统支持',
    'AI Platform': 'AI平台',
    'Hybrid Model': '混合模式',
    'Availability': '可用性',
    'Response Time': '响应时间',
    'Cost per Ticket': '工单成本',
    'Consistency': '一致性',
    'Complex Issues': '复杂问题',
    'Personalization': '个性化',
    '24/7/365': '全天候服务',
    'Business Hours': '工作时间',
    'Extended Hours': '延长服务时间',
    'Instant': '即时',
    'Variable': '可变',
    'Limited': '有限',
    'Excellent': '优秀',
    'Data-driven': '数据驱动',
    'Human intuition': '人工直觉',
    'Combined': '综合',
    'Escalation Flow': '升级流程',
    'High + Variable': '高+可变',
  };

  // Apply phrase translations
  Object.keys(phraseMap).forEach(key => {
    const regex = new RegExp(key, 'gi');
    translated = translated.replace(regex, phraseMap[key]);
  });

  // Apply word translations
  Object.keys(translations).forEach(key => {
    if (key !== 'AI' && key !== 'ROI' && key !== 'FAQ' && key !== '2026') {
      const regex = new RegExp(key, 'gi');
      translated = translated.replace(regex, translations[key]);
    }
  });

  // Handle common sentence starters
  translated = translated.replace(/The transformation/g, '转型');
  translated = translated.replace(/The following/g, '以下');
  translated = translated.replace(/Understanding/g, '了解');
  translated = translated.replace(/Successful/g, '成功的');
  translated = translated.replace(/Industry research/g, '行业研究');
  translated = translated.replace(/Organizations/g, '企业');
  translated = translated.replace(/Most organizations/g, '大多数企业');

  return translated;
}

// Translate FAQ
function translateFAQ(faq) {
  return faq.map(item => {
    let question = item.question;
    let answer = item.answer;

    // Apply translations
    Object.keys(translations).forEach(key => {
      if (key !== 'AI' && key !== 'ROI') {
        const regex = new RegExp(key, 'gi');
        question = question.replace(regex, translations[key]);
        answer = answer.replace(regex, translations[key]);
      }
    });

    // Handle common question starters
    question = question.replace(/What percentage/gi, '多少比例');
    question = question.replace(/What is/gi, '什么是');
    question = question.replace(/How do/gi, '如何');
    question = question.replace(/How does/gi, '如何');
    question = question.replace(/Why/gi, '为什么');
    question = question.replace(/Which/gi, '哪些');

    // Handle percentage patterns
    answer = answer.replace(/60-80%/g, '60-80%');
    answer = answer.replace(/25-35%/g, '25-35%');
    answer = answer.replace(/30-40%/g, '30-40%');

    // Handle question mark
    question = question.replace(/\?/g, '?');
    question = question.replace(/\?$/g, '?');

    return {
      question: question,
      answer: answer
    };
  });
}

// Translate pros and cons
function translateProsCons(prosCons) {
  const translateList = (list) => {
    return list.map(item => {
      let translated = item;

      Object.keys(translations).forEach(key => {
        if (key !== 'AI' && key !== 'ROI') {
          const regex = new RegExp(key, 'gi');
          translated = translated.replace(regex, translations[key]);
        }
      });

      return translated;
    });
  };

  return {
    pros: translateList(prosCons.pros),
    cons: translateList(prosCons.cons)
  };
}

// Process a single file
function processFile(filename) {
  const enPath = path.join(__dirname, '../data/customer-support-tools', filename);
  const zhPath = path.join(__dirname, '../data/zh/customer-support-tools', filename);

  // Read English file
  const enData = JSON.parse(fs.readFileSync(enPath, 'utf8'));

  // Create Chinese version
  const zhData = {
    title: translateTitle(enData.title),
    description: translateDescription(enData.description),
    content: translateContent(enData.content),
    seo_keywords: translateKeywords(enData.seo_keywords),
    slug: enData.slug,
    published_at: enData.published_at,
    author: enData.author,
    pros_and_cons: enData.pros_and_cons ? translateProsCons(enData.pros_and_cons) : undefined,
    faq: enData.faq ? translateFAQ(enData.faq) : undefined,
    language: 'zh-CN',
    canonical_link: `https://www.housecar.life/zh/posts/${enData.slug}`,
    alternate_links: {
      'zh-CN': `https://www.housecar.life/zh/posts/${enData.slug}`,
      'en-US': `https://www.housecar.life/posts/${enData.slug}`
    }
  };

  // Write Chinese file
  fs.writeFileSync(zhPath, JSON.stringify(zhData, null, 2), 'utf8');

  return filename;
}

// Main execution
const filesToProcess = [
  'agent-performance-monitoring-software.json',
  'ai-customer-service-platforms.json',
  'ai-powered-chat-software.json',
  'ai-support-automation-tools.json',
  'automated-chatbot-solutions.json',
  'call-center-analytics-tools.json',
  'call-center-crm-integration.json',
  'call-center-software-2026-review.json',
  'call-center-workforce-management.json',
  'call-routing-software-comparison.json',
  'chat-analytics-platforms.json',
  'chatbot-analytics-tools.json',
  'chatbot-integration-platforms.json',
  'chatbot-software-2026-review.json',
  'cloud-contact-center-platforms.json',
  'cloud-help-desk-software-review.json',
  'collaborative-email-platforms.json',
  'conversational-ai-tools-comparison.json',
  'cs-ai-knowledge-base-tools-2026.json',
  'cs-cobrowsing-software-2026.json',
  'cs-customer-documentation-tools-2026.json',
  'cs-faq-management-tools-2026.json',
  'cs-help-center-software-tools-2026.json',
  'cs-internal-knowledge-base-tools-2026.json',
  'cs-knowledge-base-search-tools-2026.json',
  'cs-knowledge-base-software-tools-2026.json',
  'cs-knowledge-management-tools-2026.json',
  'cs-live-guidance-platforms-2026.json',
  'cs-remote-access-tools-2026.json',
  'cs-remote-assistance-software-2026.json',
  'cs-remote-desktop-support-platforms-2026.json',
  'cs-remote-support-security-tools-2026.json',
  'cs-remote-support-software-2026.json',
  'cs-remote-troubleshooting-platforms-2026.json',
  'cs-screen-sharing-tools-2026.json',
  'cs-self-service-support-tools-2026.json',
  'cs-video-support-tools-2026.json',
  'cs-wiki-software-tools-2026.json',
  'csat-survey-software.json',
  'customer-effort-score-platforms.json',
  'customer-email-management-tools.json',
  'customer-feedback-software-2026-review.json',
  'customer-review-management-tools.json',
  'customer-satisfaction-tracking-tools.json',
  'customer-service-reporting-software.json',
  'customer-support-dashboard-platforms.json',
  'customer-support-platforms-small-business.json',
  'customer-survey-platforms-comparison.json',
  'email-crm-integration-platforms.json',
  'email-response-automation-software.json',
  'email-support-analytics-tools.json',
  'email-support-software-2026-review.json',
  'email-template-management.json',
  'email-ticketing-systems.json',
  'enterprise-chatbot-software.json',
  'enterprise-help-desk-solutions.json',
  'facebook-customer-support-tools.json',
  'feedback-analytics-tools.json',
  'feedback-collection-platforms.json',
  'help-desk-analytics-tools.json',
  'help-desk-automation-tools.json',
  'help-desk-integration-platforms.json',
  'inbound-call-management-software.json',
  'instagram-support-management-platforms.json',
  'live-chat-automation-features.json',
  'live-chat-for-ecommerce.json',
  'live-chat-integration-tools.json',
  'multi-account-email-support-tools.json',
  'multi-channel-help-desk-platforms.json',
  'multi-channel-live-chat-platforms.json',
  'multi-platform-social-support-tools.json',
  'multilingual-chatbot-software.json',
  'no-code-chatbot-platforms.json',
  'nps-measurement-tools.json',
  'outbound-call-center-platforms.json',
  'predictive-support-analytics-platforms.json',
  'proactive-chat-software.json',
  'real-time-customer-support-tools.json',
  'response-time-tracking-tools.json',
  'sentiment-analysis-software.json',
  'shared-inbox-platforms-comparison.json',
  'social-crm-integration-tools.json',
  'social-customer-service-platforms.json',
  'social-engagement-management-software.json',
  'social-media-monitoring-for-support.json',
  'social-media-support-software-2026.json',
  'social-support-analytics-platforms.json',
  'support-analytics-software-2026-review.json',
  'support-performance-metrics-tools.json',
  'support-roi-analytics-tools.json',
  'support-team-analytics-platforms.json',
  'support-ticket-tracking-software.json',
  'ticket-management-systems-comparison.json',
  'twitter-support-tools-review.json',
  'voice-of-customer-platforms.json',
  'voip-phone-systems-for-support.json',
  'website-chat-platforms-comparison.json'
];

// Process all files
console.log('Starting batch translation of 97 files...');
const processed = [];

filesToProcess.forEach((filename, index) => {
  try {
    processFile(filename);
    processed.push(filename);
    console.log(`[${index + 1}/97] Processed: ${filename}`);
  } catch (error) {
    console.error(`Error processing ${filename}: ${error.message}`);
  }
});

console.log(`\nCompleted! Successfully processed ${processed.length} files.`);
console.log('Output directory: /Users/gejiayu/owner/seo/data/zh/customer-support-tools/');