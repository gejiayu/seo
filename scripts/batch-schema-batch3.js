const fs = require('fs');
const path = require('path');

const categories = [
  'nonprofit-charity-tools',
  'remote-tools',
  'optometry-eye-care-tools',
  'customer-support-tools',
  'ecommerce-selling-tools'
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
    .replace(/best /i, '')
    .trim();
  return terms;
}

function extractToolNames(content) {
  // Extract tool names from h3 headings and strong tags
  const h3Matches = content.match(/<h3[^>]*>(?:\d+\.\s*)?([^<]+)/g) || [];
  const tools = h3Matches.slice(0, 3).map(m => {
    const name = m.replace(/<h3[^>]*>/, '').replace(/^\d+\.\s*/, '').trim();
    return name;
  }).filter(name => name.length > 0 && name.length < 50);
  return tools;
}

function generateFAQSchema(title, content, category) {
  const keyTerms = extractKeyTerms(title);
  const tools = extractToolNames(content);

  // Customize based on category
  let categoryContext = '';
  let pricingRange = '';
  let specificFeatures = '';

  switch(category) {
    case 'nonprofit-charity-tools':
      categoryContext = 'nonprofit and charity organizations';
      pricingRange = '$50-200 for basic tools to $500-1500 for enterprise solutions';
      specificFeatures = 'donation management, volunteer coordination, impact reporting, grant tracking';
      break;
    case 'remote-tools':
      categoryContext = 'remote work and distributed teams';
      pricingRange = '$10-50 per user/month for basic tools to $100-300 per user/month for enterprise solutions';
      specificFeatures = 'video conferencing, project collaboration, time tracking, virtual workspace management';
      break;
    case 'optometry-eye-care-tools':
      categoryContext = 'optometry and eye care practices';
      pricingRange = '$100-300 per month for basic tools to $500-2000 for comprehensive practice management';
      specificFeatures = 'patient scheduling, vision testing integration, prescription management, insurance billing';
      break;
    case 'customer-support-tools':
      categoryContext = 'customer support and service teams';
      pricingRange = '$20-100 per agent/month for basic tools to $150-400 per agent/month for enterprise solutions';
      specificFeatures = 'ticket management, live chat, knowledge base, customer analytics, omnichannel support';
      break;
    case 'ecommerce-selling-tools':
      categoryContext = 'ecommerce and online selling businesses';
      pricingRange = '$30-150 per month for basic tools to $300-1000 for enterprise solutions';
      specificFeatures = 'inventory management, order processing, payment integration, marketing automation, analytics';
      break;
    default:
      categoryContext = 'small businesses';
      pricingRange = '$50-500 per month depending on scale';
      specificFeatures = 'core business operations, analytics, automation';
  }

  const faqs = [
    {
      question: `What are the best ${keyTerms} for ${categoryContext} in 2026?`,
      answer: tools.length > 0
        ? `Top ${keyTerms} include ${tools.join(', ')}, offering features like ${specificFeatures} for ${categoryContext}.`
        : `Leading ${keyTerms} provide comprehensive features including ${specificFeatures} for ${categoryContext}.`
    },
    {
      question: `How much do ${keyTerms} typically cost?`,
      answer: `${keyTerms} pricing ranges from ${pricingRange}, depending on features, users, and business scale.`
    },
    {
      question: `What key features should I look for in ${keyTerms}?`,
      answer: `Essential features include ${specificFeatures}, plus integration capabilities, mobile accessibility, reporting dashboards, and reliable customer support.`
    },
    {
      question: `Can ${keyTerms} integrate with existing business systems?`,
      answer: `Yes, modern ${keyTerms} offer API integrations with popular platforms, CRM systems, payment gateways, and third-party applications for seamless workflow automation.`
    },
    {
      question: `How do ${keyTerms} help improve operational efficiency?`,
      answer: `${keyTerms} reduce manual tasks by 40-60%, provide real-time insights, automate routine processes, and enable better decision-making through comprehensive analytics.`
    },
    {
      question: `What's the implementation timeline for ${keyTerms}?`,
      answer: `Most ${keyTerms} can be deployed within 1-4 weeks, including setup, data migration, team training, and testing phases. Complex implementations may require 2-3 months.`
    },
    {
      question: `Are there free trials available for ${keyTerms}?`,
      answer: `Many ${keyTerms} providers offer 14-30 day free trials, allowing you to test features, usability, and compatibility before committing to a subscription.`
    }
  ];

  // Select 5-7 FAQs based on category
  const selectedFaqs = faqs.slice(0, Math.min(7, Math.max(5, 6 + Math.floor(Math.random() * 2))));

  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": selectedFaqs.map(faq => ({
      "@type": "Question",
      "name": faq.question,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": faq.answer
      }
    }))
  };
}

function generateHowToSchema(title, content, category) {
  const keyTerms = extractKeyTerms(title);

  const steps = [
    {
      "@type": "HowToStep",
      "name": "Assess Your Business Requirements",
      "text": `Evaluate your current operational challenges, team size, budget constraints, and specific needs for ${keyTerms} to establish clear selection criteria.`,
      "position": 1
    },
    {
      "@type": "HowToStep",
      "name": "Research and Compare Options",
      "text": `Research 3-5 ${keyTerms} platforms, comparing features, pricing structures, user reviews, integration capabilities, and industry-specific functionality.`,
      "position": 2
    },
    {
      "@type": "HowToStep",
      "name": "Request Demos and Free Trials",
      "text": "Schedule demos with top vendors and initiate free trials to test usability, performance, and compatibility with your existing workflows and team preferences.",
      "position": 3
    },
    {
      "@type": "HowToStep",
      "name": "Evaluate Total Cost and ROI",
      "text": `Calculate total implementation costs including subscription fees, setup costs, training time, and potential productivity gains to determine ROI for ${keyTerms}.`,
      "position": 4
    },
    {
      "@type": "HowToStep",
      "name": "Deploy and Train Your Team",
      "text": `Implement your chosen ${keyTerms}, migrate existing data, conduct comprehensive team training, and establish ongoing support procedures for successful adoption.`,
      "position": 5
    }
  ];

  return {
    "@context": "https://schema.org",
    "@type": "HowTo",
    "name": `How to Choose and Implement ${keyTerms}`,
    "description": `Step-by-step guide for selecting and deploying the best ${keyTerms} for ${category}`,
    "step": steps
  };
}

function processFile(filePath, category) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const json = JSON.parse(content);

    // Generate new schemas
    const faqSchema = generateFAQSchema(json.title, json.content || '', category);
    const howToSchema = generateHowToSchema(json.title, json.content || '', category);

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

function main() {
  const stats = {
    processed: 0,
    failed: 0,
    byCategory: {}
  };

  for (const category of categories) {
    const categoryDir = path.join(dataDir, category);

    if (!fs.existsSync(categoryDir)) {
      console.error(`Directory not found: ${categoryDir}`);
      continue;
    }

    const files = fs.readdirSync(categoryDir).filter(f => f.endsWith('.json'));

    stats.byCategory[category] = { total: files.length, success: 0, failed: 0 };

    console.log(`Processing ${category}: ${files.length} files`);

    for (const file of files) {
      const filePath = path.join(categoryDir, file);
      const success = processFile(filePath, category);

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

main();