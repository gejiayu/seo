#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Categories to process
const categories = [
  'ai-productivity',
  'storage-unit-rental-tools',
  'security-surveillance-rental-tools',
  'entertainment-media-production-tools',
  'camping-outdoor-gear-rental-tools'
];

const dataDir = '/Users/gejiayu/owner/seo/data';

// Generate FAQ Schema based on content
function generateFAQSchema(title, content, seoKeywords) {
  const keywords = seoKeywords || [];
  const mainKeyword = keywords[0] || 'this tool';

  // Extract topic from title
  const topicMatch = title.match(/(.+?)\s+(Comparison|Review|vs|Tools|Software|Platform|System)/i);
  const topic = topicMatch ? topicMatch[1].trim() : title.split(' ').slice(0, 3).join(' ');

  // Generate 5-7 relevant Q&A pairs
  const faqItems = [
    {
      question: `What is ${mainKeyword} and how does it work?`,
      answer: `${mainKeyword} is a software solution designed to help businesses and individuals manage their operations efficiently. It automates workflows, provides real-time insights, and integrates with existing systems to streamline processes.`
    },
    {
      question: `What are the key features of ${topic}?`,
      answer: `Key features include automation capabilities, real-time analytics, cloud-based access, integration with popular platforms, user-friendly interface, and customizable workflows to meet specific business needs.`
    },
    {
      question: `How much does ${mainKeyword} cost?`,
      answer: `Pricing varies based on the plan and features needed. Most tools offer tiered pricing from free basic versions to premium plans ranging from $10-$100+ per month. Enterprise solutions may require custom pricing.`
    },
    {
      question: `Is ${mainKeyword} suitable for small businesses?`,
      answer: `Yes, ${mainKeyword} is designed to scale with businesses of all sizes. Small businesses benefit from affordable pricing tiers, easy setup, and features that grow with their needs without requiring technical expertise.`
    },
    {
      question: `How does ${mainKeyword} compare to alternatives?`,
      answer: `${mainKeyword} stands out with its unique combination of features, pricing flexibility, and ease of use. Compared to alternatives, it offers better value for remote workers and digital nomads who need mobile-friendly solutions.`
    },
    {
      question: `Can ${mainKeyword} integrate with other software?`,
      answer: `Yes, most ${mainKeyword} solutions offer integrations with popular business tools including accounting software, CRM systems, project management platforms, and cloud storage services through APIs and native connectors.`
    },
    {
      question: `What support options are available for ${mainKeyword}?`,
      answer: `Support typically includes online documentation, video tutorials, email support, live chat, and community forums. Premium plans often include priority support, dedicated account managers, and phone assistance.`
    }
  ];

  return {
    "@type": "FAQPage",
    "mainEntity": faqItems.map(item => ({
      "@type": "Question",
      "name": item.question,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": item.answer
      }
    }))
  };
}

// Generate HowTo Schema based on content
function generateHowToSchema(title, content, seoKeywords) {
  const keywords = seoKeywords || [];
  const mainKeyword = keywords[0] || 'this tool';

  // Extract topic from title
  const topicMatch = title.match(/(.+?)\s+(Comparison|Review|vs|Tools|Software|Platform|System)/i);
  const topic = topicMatch ? topicMatch[1].trim() : 'the tool';

  // Generate 3-5 step process
  const steps = [
    {
      name: "Research and compare options",
      text: `Start by researching ${mainKeyword} options available in the market. Compare features, pricing, user reviews, and integration capabilities to find the best fit for your needs.`,
      position: 1
    },
    {
      name: "Choose the right plan",
      text: `Select a pricing plan that matches your business size and requirements. Consider starting with a free trial or basic plan before committing to premium features.`,
      position: 2
    },
    {
      name: "Set up and configure",
      text: `Create your account, complete the initial setup wizard, and configure settings to match your workflow. Import existing data if needed and customize dashboards.`,
      position: 3
    },
    {
      name: "Integrate with existing tools",
      text: `Connect ${mainKeyword} with your existing business systems like accounting, CRM, or project management tools. Set up automations to streamline workflows.`,
      position: 4
    },
    {
      name: "Train team and optimize",
      text: `Train your team on using ${mainKeyword} effectively. Monitor usage, gather feedback, and continuously optimize settings to improve productivity and results.`,
      position: 5
    }
  ];

  return {
    "@type": "HowTo",
    "name": `How to choose and use ${topic}`,
    "description": `Step-by-step guide to selecting, setting up, and maximizing ${mainKeyword} for your business or personal needs.`,
    "step": steps.map(step => ({
      "@type": "HowToStep",
      "name": step.name,
      "text": step.text,
      "position": step.position
    })),
    "totalTime": "PT2H",
    "estimatedCost": {
      "@type": "MonetaryAmount",
      "currency": "USD",
      "value": "0-100"
    }
  };
}

// Process a single JSON file
function processFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const data = JSON.parse(content);

    // Check if schema_markup exists
    if (!data.schema_markup) {
      data.schema_markup = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication"
      };
    }

    // Generate FAQ and HowTo schemas
    const faqSchema = generateFAQSchema(data.title, data.content, data.seo_keywords);
    const howToSchema = generateHowToSchema(data.title, data.content, data.seo_keywords);

    // Add to schema_markup - keep existing SoftwareApplication and add FAQ + HowTo
    const existingType = data.schema_markup["@type"];

    // Create new multi-type schema
    data.schema_markup = {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": existingType || "SoftwareApplication",
          ...Object.fromEntries(
            Object.entries(data.schema_markup).filter(([key]) => key !== "@context" && key !== "@type")
          )
        },
        faqSchema,
        howToSchema
      ]
    };

    // Write back to file
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n');
    return { success: true, file: path.basename(filePath) };
  } catch (error) {
    return { success: false, file: path.basename(filePath), error: error.message };
  }
}

// Process all files in a category
function processCategory(categoryName) {
  const categoryDir = path.join(dataDir, categoryName);

  if (!fs.existsSync(categoryDir)) {
    console.log(`Directory not found: ${categoryDir}`);
    return { files: 0, success: 0, failed: 0 };
  }

  const files = fs.readdirSync(categoryDir)
    .filter(f => f.endsWith('.json'))
    .map(f => path.join(categoryDir, f));

  console.log(`\nProcessing ${categoryName}: ${files.length} files`);

  let successCount = 0;
  let failCount = 0;

  files.forEach(file => {
    const result = processFile(file);
    if (result.success) {
      successCount++;
    } else {
      failCount++;
      console.log(`  Failed: ${result.file} - ${result.error}`);
    }
  });

  console.log(`  ✓ Success: ${successCount}, Failed: ${failCount}`);

  return { files: files.length, success: successCount, failed: failCount };
}

// Main execution
console.log('Schema Generation - Batch 6');
console.log('================================');

const stats = {
  totalFiles: 0,
  totalSuccess: 0,
  totalFailed: 0,
  categories: {}
};

categories.forEach(category => {
  const result = processCategory(category);
  stats.totalFiles += result.files;
  stats.totalSuccess += result.success;
  stats.totalFailed += result.failed;
  stats.categories[category] = result;
});

console.log('\n================================');
console.log('Final Statistics:');
console.log(`Total Files Processed: ${stats.totalFiles}`);
console.log(`Successful: ${stats.totalSuccess}`);
console.log(`Failed: ${stats.totalFailed}`);
console.log('\nBy Category:');
Object.entries(stats.categories).forEach(([cat, data]) => {
  console.log(`  ${cat}: ${data.success}/${data.files} success`);
});