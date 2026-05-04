const fs = require('fs');
const path = require('path');

const categories = [
  'ai-marketing',
  'publishing-media-tools',
  'energy-utilities-management',
  'furniture-home-rental-tools',
  'sporting-goods-retail-tools'
];

const dataDir = '/Users/gejiayu/owner/seo/data';

function extractKeyTerms(title) {
  const terms = title.toLowerCase()
    .replace(/top \d+ /i, '')
    .replace(/ \d+/i, '')
    .replace(/: .*/i, '')
    .replace(/ comparison/i, '')
    .replace(/ review/i, '')
    .replace(/ ultimate/i, '')
    .replace(/ small business/i, '')
    .trim();
  return terms;
}

function extractToolNames(content) {
  const matches = content.match(/<strong>([^<]+)<\/strong>/g) || [];
  return matches.slice(0, 3).map(m => m.replace(/<strong>|<\/strong>/g, '').trim());
}

function generateFAQSchema(title, content) {
  const keyTerms = extractKeyTerms(title);
  const tools = extractToolNames(content);

  const faqs = [
    {
      question: `What are the best ${keyTerms} for small businesses in 2026?`,
      answer: tools.length > 0
        ? `Top ${keyTerms} platforms include ${tools.join(', ')}, offering features like analytics, management, and automation for business operations.`
        : `Leading ${keyTerms} platforms provide comprehensive features including data analysis, operational management, and cost optimization for small businesses.`
    },
    {
      question: `How much do ${keyTerms} typically cost per month?`,
      answer: `${keyTerms} pricing ranges from ¥300-600 for basic tools to ¥3500-7000 for comprehensive enterprise solutions, depending on features and scale.`
    },
    {
      question: `What features should I look for when choosing ${keyTerms}?`,
      answer: `Key features to consider include real-time analytics, workflow management, customer tracking, automated reporting, and integration capabilities with existing business systems.`
    },
    {
      question: `Can ${keyTerms} help reduce operational costs?`,
      answer: `Yes, modern ${keyTerms} can reduce operational costs by 20-30% through optimized workflows, reduced manual work, predictive insights, and improved resource allocation.`
    },
    {
      question: `How do I implement ${keyTerms} in my business?`,
      answer: `Start by identifying your core needs, compare 3-5 platforms using trial versions, train your team on the chosen system, and gradually migrate data while monitoring performance improvements.`
    },
    {
      question: `What's the difference between basic and premium ${keyTerms}?`,
      answer: `Basic tools offer simple tracking and reporting, while premium solutions include AI-powered analytics, predictive insights, real-time monitoring, advanced integrations, and dedicated support.`
    },
    {
      question: `Are ${keyTerms} suitable for startups and small businesses?`,
      answer: `Yes, many ${keyTerms} offer scalable pricing plans starting from basic tiers perfect for startups, with the ability to upgrade as your business grows and needs evolve.`
    }
  ];

  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": faqs.map(faq => ({
      "@type": "Question",
      "name": faq.question,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": faq.answer
      }
    }))
  };
}

function generateHowToSchema(title, content) {
  const keyTerms = extractKeyTerms(title);

  const steps = [
    {
      "@type": "HowToStep",
      "name": "Identify Business Requirements",
      "text": `Assess your current operational challenges, ${keyTerms} needs, and business scale to determine which features are essential for your operations.`,
      "position": 1
    },
    {
      "@type": "HowToStep",
      "name": "Research and Compare Platforms",
      "text": `Evaluate at least 3-5 ${keyTerms} platforms by reviewing features, pricing, user reviews, and industry-specific capabilities.`,
      "position": 2
    },
    {
      "@type": "HowToStep",
      "name": "Request Demo or Trial",
      "text": "Schedule demos or start free trials with top candidates to test usability, performance, and compatibility with your existing systems.",
      "position": 3
    },
    {
      "@type": "HowToStep",
      "name": "Evaluate ROI and Cost",
      "text": "Calculate potential cost savings and efficiency gains versus monthly subscription fees to determine true return on investment.",
      "position": 4
    },
    {
      "@type": "HowToStep",
      "name": "Implement and Train Team",
      "text": "Deploy the chosen platform, migrate historical data, train staff on key features, and establish ongoing monitoring procedures for continuous optimization.",
      "position": 5
    }
  ];

  return {
    "@context": "https://schema.org",
    "@type": "HowTo",
    "name": `How to Choose and Implement ${keyTerms}`,
    "description": `Step-by-step guide for selecting and deploying the best ${keyTerms} for small business operations`,
    "step": steps
  };
}

function processFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const json = JSON.parse(content);

    // Generate new schemas
    const faqSchema = generateFAQSchema(json.title, json.content);
    const howToSchema = generateHowToSchema(json.title, json.content);

    // Add schemas to JSON
    json.faq_schema = faqSchema;
    json.howto_schema = howToSchema;

    // Write back
    fs.writeFileSync(filePath, JSON.stringify(json, null, 2));
    return true;
  } catch (err) {
    console.error(`Error processing ${filePath}:`, err.message);
    return false;
  }
}

async function main() {
  const stats = {
    processed: 0,
    failed: 0,
    byCategory: {}
  };

  for (const category of categories) {
    const categoryDir = path.join(dataDir, category);
    const files = fs.readdirSync(categoryDir).filter(f => f.endsWith('.json'));

    stats.byCategory[category] = { total: files.length, success: 0, failed: 0 };

    console.log(`Processing ${category}: ${files.length} files`);

    for (const file of files) {
      const filePath = path.join(categoryDir, file);
      const success = processFile(filePath);

      if (success) {
        stats.processed++;
        stats.byCategory[category].success++;
      } else {
        stats.failed++;
        stats.byCategory[category].failed++;
      }
    }
  }

  console.log('\n=== Processing Complete ===');
  console.log(`Total processed: ${stats.processed}`);
  console.log(`Failed: ${stats.failed}`);
  console.log('\nBy Category:');
  for (const [cat, data] of Object.entries(stats.byCategory)) {
    console.log(`  ${cat}: ${data.success}/${data.total} success`);
  }
}

main().catch(console.error);