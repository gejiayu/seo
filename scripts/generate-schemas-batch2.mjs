import fs from 'fs';
import path from 'path';

// Categories to process (both EN and ZH versions)
const categories = [
  'wine-spirits-liquor-store-tools',
  'medical-equipment-rental-tools',
  'vending-machine-management-tools',
  'restaurant-food-service-tools',
  'hospitality-restaurant-pos-tools'
];

const dataDir = '/Users/gejiayu/owner/seo/data';
const zhDataDir = '/Users/gejiayu/owner/seo/data/zh';

// Process both EN and ZH directories
const directories = [];
categories.forEach(category => {
  directories.push({ path: path.join(dataDir, category), category, lang: 'en' });
  directories.push({ path: path.join(zhDataDir, category), category, lang: 'zh' });
});

// Generate FAQ Schema from content
function generateFAQSchema(content, title) {
  // Extract key topics from content
  const sections = content.split(/##+\s/).filter(s => s.trim());
  const qaPairs = [];

  // Generate 5-7 Q&A pairs based on content
  const questions = [
    {
      q: `What are the main features mentioned in ${title}?`,
      a: extractFeaturesFromContent(content)
    },
    {
      q: `How does this tool help businesses?`,
      a: extractBenefitsFromContent(content)
    },
    {
      q: `What should businesses consider when choosing this type of tool?`,
      a: extractCriteriaFromContent(content)
    },
    {
      q: `What are the implementation best practices?`,
      a: extractPracticesFromContent(content)
    },
    {
      q: `Why is this tool important for business operations?`,
      a: extractImportanceFromContent(content, title)
    },
    {
      q: `What are the key benefits for users?`,
      a: extractUserBenefitsFromContent(content)
    },
    {
      q: `How can businesses get started with this tool?`,
      a: extractGettingStartedFromContent(content)
    }
  ];

  // Select 5-7 questions based on available content
  let selectedQuestions = questions.filter(q => q.a && q.a.length > 20);
  if (selectedQuestions.length < 5) {
    selectedQuestions = questions.slice(0, 5);
  }

  selectedQuestions.slice(0, 7).forEach(q => {
    qaPairs.push({
      question: q.q,
      answer: q.a.substring(0, 500) // Limit answer length
    });
  });

  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": qaPairs.map(qa => ({
      "@type": "Question",
      "name": qa.question,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": qa.answer
      }
    }))
  };
}

// Generate HowTo Schema from title
function generateHowToSchema(title, content) {
  // Generate 3-5 implementation steps based on title
  const steps = generateStepsFromTitle(title, content);

  return {
    "@context": "https://schema.org",
    "@type": "HowTo",
    "name": `How to implement ${title.toLowerCase().replace(/top \d+ /i, '').replace(/2026: .*/i, '').trim()}`,
    "description": `Step-by-step guide for implementing the best solution from: ${title}`,
    "step": steps.map((step, index) => ({
      "@type": "HowToStep",
      "position": index + 1,
      "name": step.name,
      "text": step.text
    }))
  };
}

// Helper functions to extract content
function extractFeaturesFromContent(content) {
  const featureMatch = content.match(/##+ Key Features\s*\n([\s\S]*?)(?=\n##+|$)/i);
  if (featureMatch) {
    return cleanExtract(featureMatch[1]);
  }
  // Look for bullet points in general
  const bulletMatch = content.match(/[-*]\s*\*?\*?([^*\n]+)\*?\*?:?\s*([^\n]+)/);
  if (bulletMatch) {
    return `Key features include: ${bulletMatch[2].trim()}`;
  }
  return "Modern tools offer advanced features including automation, integration capabilities, and real-time analytics to help businesses improve efficiency and compliance.";
}

function extractBenefitsFromContent(content) {
  const benefitMatch = content.match(/##+ Benefits\s*\n([\s\S]*?)(?=\n##+|$)/i);
  if (benefitMatch) {
    return cleanExtract(benefitMatch[1]);
  }
  const benefitMatch2 = content.match(/##+ Benefits for[\s\S]*?\n([\s\S]*?)(?=\n##+|$)/i);
  if (benefitMatch2) {
    return cleanExtract(benefitMatch2[1]);
  }
  return "These tools help businesses save time, reduce errors, improve compliance, enhance customer experience, and increase operational efficiency.";
}

function extractCriteriaFromContent(content) {
  const criteriaMatch = content.match(/##+ Selection Criteria\s*\n([\s\S]*?)(?=\n##+|$)/i);
  if (criteriaMatch) {
    return cleanExtract(criteriaMatch[1]);
  }
  const choosingMatch = content.match(/##+ Choosing[\s\S]*?\n([\s\S]*?)(?=\n##+|$)/i);
  if (choosingMatch) {
    return cleanExtract(choosingMatch[1]);
  }
  return "When selecting tools, consider factors such as ease of use, integration capabilities, cost, scalability, customer support, and compliance with industry regulations.";
}

function extractPracticesFromContent(content) {
  const practicesMatch = content.match(/##+ Implementation[\s\S]*?\n([\s\S]*?)(?=\n##+|$)/i);
  if (practicesMatch) {
    return cleanExtract(practicesMatch[1]);
  }
  const bestMatch = content.match(/##+ Best Practices\s*\n([\s\S]*?)(?=\n##+|$)/i);
  if (bestMatch) {
    return cleanExtract(bestMatch[1]);
  }
  return "Successful implementation requires proper planning, staff training, system integration, regular testing, and ongoing monitoring to ensure optimal performance.";
}

function extractImportanceFromContent(content, title) {
  const intro = content.split('\n\n')[0];
  if (intro && intro.length > 50) {
    return intro.replace(/#+\s/g, '').trim().substring(0, 500);
  }
  return `${title} is essential for modern businesses to maintain compliance, improve efficiency, and deliver better customer experiences while reducing operational risks.`;
}

function extractUserBenefitsFromContent(content) {
  const userMatch = content.match(/##+ (?:For Users|Customer Benefits|User Experience)\s*\n([\s\S]*?)(?=\n##+|$)/i);
  if (userMatch) {
    return cleanExtract(userMatch[1]);
  }
  return "Users benefit from faster processing, improved accuracy, better service quality, enhanced security, and more convenient interactions with the business.";
}

function extractGettingStartedFromContent(content) {
  const startMatch = content.match(/##+ Getting Started\s*\n([\s\S]*?)(?=\n##+|$)/i);
  if (startMatch) {
    return cleanExtract(startMatch[1]);
  }
  return "To get started, evaluate your current processes, identify key requirements, research available solutions, select the best fit for your needs, and plan a phased implementation with proper training.";
}

function cleanExtract(text) {
  // Remove markdown formatting and clean up
  return text
    .replace(/[-*]\s*\*?\*?([^*\n]+)\*?\*?\n/g, '$1. ')
    .replace(/\*?\*?([^*\n]+)\*?\*?/g, '$1')
    .replace(/\n+/g, ' ')
    .trim()
    .substring(0, 500);
}

function generateStepsFromTitle(title, content) {
  // Extract tool type from title
  const toolType = title.toLowerCase()
    .replace(/top \d+ /i, '')
    .replace(/2026: .*/i, '')
    .replace(/comparison/i, '')
    .replace(/small business/i, '')
    .trim();

  // Generate generic but relevant steps
  const steps = [
    {
      name: "Assess Current Needs",
      text: `Evaluate your current ${toolType} requirements and identify pain points that need addressing. Document your current processes and identify gaps where automation or improvement is needed.`
    },
    {
      name: "Research Available Solutions",
      text: `Research and compare available ${toolType} solutions in the market. Consider factors such as features, pricing, integration capabilities, and user reviews to narrow down your options.`
    },
    {
      name: "Select the Right Solution",
      text: `Choose the ${toolType} solution that best fits your business requirements, budget, and technical capabilities. Consider scalability and long-term support from the vendor.`
    },
    {
      name: "Plan Implementation",
      text: `Develop a detailed implementation plan including timeline, resource allocation, training requirements, and integration with existing systems. Set clear milestones and success metrics.`
    },
    {
      name: "Deploy and Train",
      text: `Deploy the ${toolType} solution and conduct comprehensive staff training. Monitor initial performance, address issues promptly, and gather feedback for optimization.`
    }
  ];

  return steps.slice(0, 5);
}

// Process all files
let processedCount = 0;
let errorCount = 0;
const startTime = Date.now();

directories.forEach(({ path: categoryPath, category, lang }) => {
  if (!fs.existsSync(categoryPath)) {
    console.log(`Directory not found: ${categoryPath}`);
    return;
  }

  const files = fs.readdirSync(categoryPath).filter(f => f.endsWith('.json'));

  console.log(`Processing ${files.length} files in ${category} (${lang})...`);

  files.forEach(file => {
    const filePath = path.join(categoryPath, file);

    try {
      // Read JSON
      const jsonContent = fs.readFileSync(filePath, 'utf8');
      const data = JSON.parse(jsonContent);

      // Check if schemas already exist
      if (data.faq_schema && data.howto_schema) {
        console.log(`  Skipping ${file} (schemas already exist)`);
        return;
      }

      // Generate schemas
      const faqSchema = generateFAQSchema(data.content, data.title);
      const howtoSchema = generateHowToSchema(data.title, data.content);

      // Add schemas to JSON
      data.faq_schema = faqSchema;
      data.howto_schema = howtoSchema;

      // Write back to file
      fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');

      processedCount++;
      if (processedCount % 50 === 0) {
        console.log(`  Processed ${processedCount} files...`);
      }
    } catch (error) {
      console.error(`  Error processing ${file}: ${error.message}`);
      errorCount++;
    }
  });
});

const endTime = Date.now();
const duration = ((endTime - startTime) / 1000).toFixed(2);

console.log('\n=== Batch 2 Schema Generation Complete ===');
console.log(`Total files processed: ${processedCount}`);
console.log(`Errors: ${errorCount}`);
console.log(`Duration: ${duration} seconds`);
console.log(`Average time per file: ${(duration / processedCount).toFixed(3)} seconds`);