const fs = require('fs');
const path = require('path');

const BASE_DIR = '/Users/gejiayu/owner/seo/data';

const CATEGORIES = [
  'scooter-moped-rental-tools',
  'lighting-lamp-rental-tools',
  'coworking-space-management-tools',
  'zh/scooter-moped-rental-tools',
  'zh/lighting-lamp-rental-tools',
  'zh/coworking-space-management-tools'
];

function generateFAQSchema(title, content, category) {
  // Extract key information from content
  const questions = [];
  const isChinese = category.startsWith('zh/');

  // Generate 5-7 Q&A pairs based on content patterns
  if (isChinese) {
    // Chinese FAQ
    questions.push({
      question: `${title.includes('对比') ? title.split('对比')[0].replace('Top 5', '').trim() : '这个工具'}的主要功能是什么?`,
      answer: extractCoreFeatures(content) || '该工具提供核心管理功能，帮助企业提高运营效率。'
    });

    questions.push({
      question: '哪个工具性价比最高?',
      answer: extractBestValue(content, isChinese) || '根据您的具体需求和预算，可以选择不同的工具方案。'
    });

    questions.push({
      question: '适合什么规模的企业使用?',
      answer: extractTargetAudience(content, isChinese) || '从小型企业到大型企业都可以使用，具体取决于功能需求和预算。'
    });

    questions.push({
      question: '价格范围是多少?',
      answer: extractPriceRange(content, isChinese) || '价格从几十美元到几百美元不等，具体取决于功能版本和订阅计划。'
    });

    questions.push({
      question: '有什么主要优势?',
      answer: extractAdvantages(content, isChinese) || '主要优势包括功能全面、易于使用、性价比高等。'
    });

    questions.push({
      question: '有什么主要缺点?',
      answer: extractDisadvantages(content, isChinese) || '可能存在的缺点包括价格较高、部署周期较长或某些高级功能需要付费升级。'
    });
  } else {
    // English FAQ
    questions.push({
      question: `What are the main features of ${title.includes('vs') ? 'these tools' : 'this tool'}?`,
      answer: extractCoreFeatures(content) || 'These tools provide core management features for operational efficiency and business growth.'
    });

    questions.push({
      question: 'Which tool offers the best value for money?',
      answer: extractBestValue(content, isChinese) || 'Value depends on your specific needs and budget. Compare features and pricing to find the best fit.'
    });

    questions.push({
      question: 'What business size is this suitable for?',
      answer: extractTargetAudience(content, isChinese) || 'Suitable for small to large enterprises depending on feature requirements and budget.'
    });

    questions.push({
      question: 'What is the pricing range?',
      answer: extractPriceRange(content, isChinese) || 'Pricing ranges from tens to hundreds of dollars monthly depending on features and subscription plans.'
    });

    questions.push({
      question: 'What are the main advantages?',
      answer: extractAdvantages(content, isChinese) || 'Key advantages include comprehensive features, ease of use, and good value for money.'
    });

    questions.push({
      question: 'What are the main limitations?',
      answer: extractDisadvantages(content, isChinese) || 'Potential limitations include higher pricing, longer deployment time, or premium features requiring upgrades.'
    });
  }

  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": questions.slice(0, 6).map(qa => ({
      "@type": "Question",
      "name": qa.question,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": qa.answer
      }
    }))
  };
}

function generateHowToSchema(title, content, category) {
  const isChinese = category.startsWith('zh/');
  const toolName = extractToolName(title);

  const steps = [];

  if (isChinese) {
    steps.push({
      "@type": "HowToStep",
      "name": "确定需求",
      "text": "首先明确您的业务需求，包括功能要求、预算范围和团队规模。",
      "position": 1
    });

    steps.push({
      "@type": "HowToStep",
      "name": "比较选项",
      "text": `查看${title.includes('对比') ? '上述工具对比' : '相关工具'}，比较各工具的功能、价格和用户评价。`,
      "position": 2
    });

    steps.push({
      "@type": "HowToStep",
      "name": "试用评估",
      "text": "利用免费试用期或演示版本，实际体验工具功能是否符合预期。",
      "position": 3
    });

    steps.push({
      "@type": "HowToStep",
      "name": "选择方案",
      "text": "根据评估结果，选择最适合您需求和预算的工具方案。",
      "position": 4
    });

    steps.push({
      "@type": "HowToStep",
      "name": "部署实施",
      "text": "完成购买或订阅，进行系统部署和团队培训，开始使用。",
      "position": 5
    });
  } else {
    steps.push({
      "@type": "HowToStep",
      "name": "Define Requirements",
      "text": "Start by clarifying your business needs including feature requirements, budget range, and team size.",
      "position": 1
    });

    steps.push({
      "@type": "HowToStep",
      "name": "Compare Options",
      "text": `Review ${title.includes('vs') ? 'the tool comparison above' : 'related tools'} and compare features, pricing, and user reviews.`,
      "position": 2
    });

    steps.push({
      "@type": "HowToStep",
      "name": "Test and Evaluate",
      "text": "Utilize free trials or demo versions to experience whether the tool features meet your expectations.",
      "position": 3
    });

    steps.push({
      "@type": "HowToStep",
      "name": "Select Solution",
      "text": "Based on evaluation results, choose the tool solution that best fits your needs and budget.",
      "position": 4
    });

    steps.push({
      "@type": "HowToStep",
      "name": "Deploy and Implement",
      "text": "Complete purchase or subscription, proceed with system deployment and team training, and begin using.",
      "position": 5
    });
  }

  return {
    "@context": "https://schema.org",
    "@type": "HowTo",
    "name": isChinese ? `如何选择${toolName}` : `How to Choose ${toolName}`,
    "description": isChinese ? `${title}的选择指南和步骤` : `Selection guide and steps for ${title}`,
    "step": steps
  };
}

function extractCoreFeatures(content) {
  const featureMatch = content.match(/<h2>Core Feature[^<]*<\/h2>(.*?)<h2>/s);
  if (featureMatch) {
    const features = featureMatch[1].match(/<td>(Excellent|Good|Average)[^<]*<\/td>/g);
    if (features && features.length > 0) {
      return `Core features include: ${features.slice(0, 3).map(f => f.replace(/<[^>]+>/g, '').trim()).join(', ')}.`;
    }
  }
  return null;
}

function extractBestValue(content, isChinese) {
  const priceMatch = content.match(/Monthly Price[^<]*<\/td><td>\$(\d+)<\/td>/i);
  const lowestPriceMatch = content.match(/lowest.*?\$(\d+)/i);
  if (lowestPriceMatch) {
    return isChinese ? `最实惠的选项价格约为$${lowestPriceMatch[1]}/月，适合预算有限的用户。` : `The most affordable option costs around $${lowestPriceMatch[1]}/month, suitable for budget-conscious users.`;
  }
  if (priceMatch) {
    return isChinese ? `价格从$${priceMatch[1]}起步，具体性价比取决于功能需求。` : `Pricing starts from $${priceMatch[1]}, with value depending on feature requirements.`;
  }
  return null;
}

function extractTargetAudience(content, isChinese) {
  if (content.includes('startup') || content.includes('small')) {
    return isChinese ? '适合初创企业和中小型企业，也支持大型企业的需求。' : 'Suitable for startups and small-medium enterprises, also supporting large enterprise needs.';
  }
  if (content.includes('large enterprise')) {
    return isChinese ? '更适合大型企业，功能全面但成本较高。' : 'Better suited for large enterprises with comprehensive features but higher cost.';
  }
  return null;
}

function extractPriceRange(content, isChinese) {
  const prices = content.match(/\$\d+/g);
  if (prices && prices.length > 0) {
    const minPrice = Math.min(...prices.map(p => parseInt(p.replace('$', ''))));
    const maxPrice = Math.max(...prices.map(p => parseInt(p.replace('$', ''))));
    return isChinese ? `价格范围从$${minPrice}到$${maxPrice}不等，具体取决于版本和功能。` : `Pricing ranges from $${minPrice} to $${maxPrice} depending on version and features.`;
  }
  return null;
}

function extractAdvantages(content, isChinese) {
  const advMatch = content.match(/<strong>Advantages<\/strong>:(.*?)(<\/li>|<strong>)/s);
  if (advMatch) {
    const text = advMatch[1].replace(/<[^>]+>/g, '').trim().slice(0, 150);
    return isChinese ? `主要优势：${text}` : `Key advantages: ${text}`;
  }
  return null;
}

function extractDisadvantages(content, isChinese) {
  const disMatch = content.match(/<strong>Disadvantages<\/strong>:(.*?)(<\/li>|<strong>)/s);
  if (disMatch) {
    const text = disMatch[1].replace(/<[^>]+>/g, '').trim().slice(0, 150);
    return isChinese ? `主要缺点：${text}` : `Key limitations: ${text}`;
  }
  return null;
}

function extractToolName(title) {
  const match = title.match(/Top \d+ (.+?) 2026/i);
  if (match) return match[1];
  return title.replace(/2026.*$/, '').trim();
}

async function processFiles() {
  let stats = {
    total: 0,
    processed: 0,
    errors: 0
  };

  for (const category of CATEGORIES) {
    const categoryPath = path.join(BASE_DIR, category);
    if (!fs.existsSync(categoryPath)) {
      console.log(`Directory not found: ${categoryPath}`);
      continue;
    }

    const files = fs.readdirSync(categoryPath).filter(f => f.endsWith('.json'));
    stats.total += files.length;

    console.log(`\nProcessing ${category}: ${files.length} files`);

    for (const file of files) {
      const filePath = path.join(categoryPath, file);
      try {
        const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

        // Generate schemas
        const faqSchema = generateFAQSchema(data.title, data.content, category);
        const howToSchema = generateHowToSchema(data.title, data.content, category);

        // Add schemas to JSON
        data.faq_schema = faqSchema;
        data.howto_schema = howToSchema;

        // Save updated JSON
        fs.writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n');
        stats.processed++;
      } catch (error) {
        console.error(`Error processing ${file}: ${error.message}`);
        stats.errors++;
      }
    }
  }

  console.log('\n=== Final Statistics ===');
  console.log(`Total files found: ${stats.total}`);
  console.log(`Successfully processed: ${stats.processed}`);
  console.log(`Errors: ${stats.errors}`);
}

processFiles().catch(console.error);