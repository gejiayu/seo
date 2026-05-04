const fs = require('fs');
const path = require('path');

// Categories to process
const categories = [
  'portable-sanitation-rental-tools',
  'manufacturing-quality-control-tools',
  'tent-canopy-rental-tools'
];

const dataDir = '/Users/gejiayu/owner/seo/data';

// Stats tracking
const stats = {
  totalFiles: 0,
  processed: 0,
  skipped: 0,
  errors: 0
};

// Generate FAQ Schema based on content and title
function generateFAQSchema(title, content, category) {
  const faqs = [];

  // Extract key information from content
  const lowerContent = content.toLowerCase();
  const lowerTitle = title.toLowerCase();

  // Determine context based on category
  const isRental = category.includes('rental');
  const isManufacturing = category.includes('manufacturing');
  const isPortableSanitation = category.includes('portable-sanitation');
  const isTent = category.includes('tent-canopy');

  // Generate FAQs based on category type
  if (isPortableSanitation) {
    faqs.push({
      question: "What is a portable sanitation booking management system?",
      answer: "A portable sanitation booking management system is a software platform that helps rental businesses manage customer bookings, online portals, automatic quotes, order processing, and electronic contracts for portable toilets, restroom trailers, and sanitation equipment rentals."
    });
    faqs.push({
      question: "How much does a portable sanitation booking system cost?",
      answer: "Portable sanitation booking systems typically range from $299 to $1999 per month depending on features and order volume. Basic systems for under 100 orders monthly start around $299, while comprehensive platforms with CRM and automation features can cost $699-$1999 monthly."
    });
    faqs.push({
      question: "What features should I look for in portable sanitation booking software?",
      answer: "Key features to look for include online booking portals, smart quote engines with automatic pricing, order process tracking, electronic contract systems with online signing, automatic reminders for payments and delivery, and customer CRM management for full lifecycle tracking."
    });
    faqs.push({
      question: "Can customers book portable sanitation rentals online?",
      answer: "Yes, modern portable sanitation booking systems provide online portals where customers can self-select equipment type, quantity, and rental duration, receive automatic quotes, and complete bookings without manual intervention, improving conversion rates by up to 35%."
    });
    faqs.push({
      question: "How do electronic contracts work in portable sanitation booking systems?",
      answer: "Electronic contract systems provide template libraries with legal validity, enable online signing through secure platforms, automatically generate contracts based on booking details, and reduce contract processing time from 3 days to 1 hour or less."
    });
    faqs.push({
      question: "What is the ROI timeline for implementing a portable sanitation booking system?",
      answer: "Most portable sanitation rental businesses see ROI within 6 months after implementing a booking management system. Benefits include 35% higher conversion rates from online portals, 60% reduced customer follow-up workload, and 40% improved order processing efficiency."
    });
  } else if (isTent) {
    faqs.push({
      question: "What is a tent and canopy rental management system?",
      answer: "A tent and canopy rental management system is specialized software that helps rental businesses manage inventory tracking, booking scheduling, delivery coordination, pricing calculations, and customer relationships for event tent, canopy, and shelter rentals."
    });
    faqs.push({
      question: "How much does tent rental management software cost?",
      answer: "Tent rental management software pricing ranges from $199 to $999 per month based on features and business size. Basic inventory-focused systems start at $199 monthly, while comprehensive platforms with booking, delivery, and CRM features range from $499-$999 monthly."
    });
    faqs.push({
      question: "What features are essential for tent canopy rental businesses?",
      answer: "Essential features include real-time inventory tracking for different tent sizes and types, booking scheduling with calendar integration, delivery route optimization, setup crew management, weather contingency planning, and customer portal for self-service bookings."
    });
    faqs.push({
      question: "Can tent rental systems handle event inventory planning?",
      answer: "Yes, tent rental systems can manage event inventory planning by tracking tent availability across multiple events, calculating setup requirements based on guest counts, optimizing equipment allocation, and providing 3D visualization tools for layout planning."
    });
    faqs.push({
      question: "How does delivery management work in tent rental software?",
      answer: "Tent rental software includes delivery management features like route optimization for multiple event locations, crew scheduling based on setup complexity, real-time GPS tracking, delivery confirmation workflows, and automatic scheduling of pickup after events."
    });
    faqs.push({
      question: "What ROI can tent rental businesses expect from management software?",
      answer: "Tent rental businesses typically see 25-40% improvement in inventory utilization, 30% reduction in delivery coordination time, and 50% faster customer quote generation. Most businesses achieve full ROI within 6-8 months of implementation."
    });
  } else if (isManufacturing) {
    faqs.push({
      question: "What is a manufacturing quality control system?",
      answer: "A manufacturing quality control system is software that helps manufacturers monitor production quality, manage inspection processes, track defect rates, implement quality standards compliance, and analyze quality metrics across production lines."
    });
    faqs.push({
      question: "How much does manufacturing quality control software cost?",
      answer: "Manufacturing quality control software costs range from $299 to $2499 monthly depending on scale. Small manufacturing operations can find systems starting at $299 monthly, while enterprise solutions with advanced analytics and IoT integration can cost $999-$2499 monthly."
    });
    faqs.push({
      question: "What quality control features should manufacturers look for?",
      answer: "Key features include real-time defect detection and tracking, inspection workflow management, quality metrics dashboards, compliance documentation for ISO and industry standards, supplier quality management, and predictive quality analytics."
    });
    faqs.push({
      question: "Can quality control systems integrate with production equipment?",
      answer: "Yes, modern quality control systems integrate with production equipment through IoT sensors and PLC connections, enabling automatic data collection, real-time quality monitoring, predictive maintenance alerts, and automated quality gates in production lines."
    });
    faqs.push({
      question: "How do manufacturing quality systems help reduce defect rates?",
      answer: "Quality control systems reduce defect rates by enabling early detection through statistical process control, providing root cause analysis tools, tracking defect patterns across batches, and implementing corrective action workflows that address quality issues systematically."
    });
    faqs.push({
      question: "What compliance standards can quality control systems support?",
      answer: "Quality control systems support ISO 9001, ISO 13485 for medical devices, IATF 16949 for automotive, AS9100 for aerospace, FDA regulations, and other industry-specific quality standards through compliance checklists, audit trails, and documentation management features."
    });
  } else {
    // Generic rental/business FAQs
    faqs.push({
      question: `What is a ${category.replace(/-/g, ' ').replace('tools', 'system')}?`,
      answer: `A ${category.replace(/-/g, ' ').replace('tools', 'management system')} is specialized software that helps businesses manage operations, inventory, customers, bookings, and financial processes specific to their industry.`
    });
    faqs.push({
      question: "How much does this type of management software typically cost?",
      answer: "Management software for small businesses typically ranges from $199 to $999 per month, with basic plans starting around $199 for core features and professional plans at $499-$999 for advanced functionality and integrations."
    });
    faqs.push({
      question: "What key features should small businesses look for?",
      answer: "Small businesses should prioritize features including inventory management, booking/scheduling capabilities, customer relationship management, automated reporting, mobile accessibility, and integration with accounting and payment systems."
    });
    faqs.push({
      question: "How long does it take to implement a management system?",
      answer: "Implementation typically takes 2-4 weeks for small businesses, including data migration, staff training, and system configuration. Cloud-based solutions offer faster deployment compared to traditional on-premise systems."
    });
    faqs.push({
      question: "What ROI can businesses expect from implementing management software?",
      answer: "Most businesses see ROI within 6-9 months through operational efficiency gains of 25-40%, reduced administrative workload by 50%, improved customer satisfaction, and better inventory management reducing waste by 20-30%."
    });
    faqs.push({
      question: "Can these systems integrate with existing business tools?",
      answer: "Yes, modern management systems integrate with common business tools including QuickBooks, Xero for accounting, Stripe and PayPal for payments, email platforms, CRM systems, and industry-specific equipment through APIs and built-in connectors."
    });
  }

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

// Generate HowTo Schema based on content and category
function generateHowToSchema(title, content, category) {
  const steps = [];

  const isPortableSanitation = category.includes('portable-sanitation');
  const isTent = category.includes('tent-canopy');
  const isManufacturing = category.includes('manufacturing');

  let howToTitle = "";
  let description = "";

  if (isPortableSanitation) {
    howToTitle = "How to Choose a Portable Sanitation Booking Management System";
    description = "Step-by-step guide to selecting and implementing the right portable sanitation booking system for your rental business";
    steps.push({
      "@type": "HowToStep",
      "name": "Assess Your Booking Volume",
      "text": "Evaluate your monthly order volume and booking complexity. Businesses with under 100 monthly orders need basic booking portals, while businesses with 500+ orders require comprehensive CRM and automation features.",
      "position": 1
    });
    steps.push({
      "@type": "HowToStep",
      "name": "Define Key Features Needed",
      "text": "Identify must-have features: online booking portal, automatic quote generation, electronic contracts, order tracking, payment integration, and customer reminder automation. Prioritize based on your pain points.",
      "position": 2
    });
    steps.push({
      "@type": "HowToStep",
      "name": "Compare Platform Options",
      "text": "Evaluate platforms like BookEasy for portal strength, ReservePro for CRM depth, and OrderFlow for automation. Request demos and compare pricing against your expected order volume tier.",
      "position": 3
    });
    steps.push({
      "@type": "HowToStep",
      "name": "Calculate ROI Timeline",
      "text": "Estimate ROI based on conversion rate improvements (35% from portals), reduced follow-up time (60%), and processing efficiency gains. Most businesses see ROI within 6 months of implementation.",
      "position": 4
    });
    steps.push({
      "@type": "HowToStep",
      "name": "Plan Implementation",
      "text": "Schedule implementation including data migration from existing booking records, staff training on portal and CRM features, electronic contract setup, and integration with accounting systems.",
      "position": 5
    });
  } else if (isTent) {
    howToTitle = "How to Select a Tent and Canopy Rental Management System";
    description = "Complete guide to choosing tent rental software for inventory tracking, booking management, and delivery coordination";
    steps.push({
      "@type": "HowToStep",
      "name": "Inventory Assessment",
      "text": "Catalog your tent and canopy inventory by size, type, and condition. Calculate peak season demand and identify inventory gaps. Systems should track tent sizes from 10x10 to large event tents.",
      "position": 1
    });
    steps.push({
      "@type": "HowToStep",
      "name": "Define Feature Requirements",
      "text": "List essential features: real-time inventory availability, booking calendar integration, delivery route optimization, crew scheduling, weather contingency tools, and customer self-service portals.",
      "position": 2
    });
    steps.push({
      "@type": "HowToStep",
      "name": "Evaluate Software Platforms",
      "text": "Compare platforms on inventory tracking accuracy, booking scheduling ease, delivery management capabilities, pricing tools, and CRM features. Request trials and check event planning capabilities.",
      "position": 3
    });
    steps.push({
      "@type": "HowToStep",
      "name": "Budget Planning",
      "text": "Match pricing tiers to your event volume. Basic inventory systems start at $199 monthly, comprehensive platforms with delivery and CRM cost $499-$999. Factor in implementation and training costs.",
      "position": 4
    });
    steps.push({
      "@type": "HowToStep",
      "name": "Launch and Training",
      "text": "Implement with phased rollout: first inventory tracking, then booking scheduling, finally delivery optimization. Train staff on inventory updates, booking workflows, and delivery coordination tools.",
      "position": 5
    });
  } else if (isManufacturing) {
    howToTitle = "How to Implement a Manufacturing Quality Control System";
    description = "Step-by-step process for deploying quality control software to reduce defects and improve production quality";
    steps.push({
      "@type": "HowToStep",
      "name": "Baseline Quality Metrics",
      "text": "Measure current defect rates, inspection times, and quality compliance gaps. Identify critical quality control points in your production process. Document current inspection workflows and pain points.",
      "position": 1
    });
    steps.push({
      "@type": "HowToStep",
      "name": "Define Quality Requirements",
      "text": "List required features: defect tracking, inspection workflows, compliance documentation (ISO standards), supplier quality management, real-time monitoring, and predictive analytics capabilities.",
      "position": 2
    });
    steps.push({
      "@type": "HowToStep",
      "name": "System Selection",
      "text": "Evaluate quality control platforms on defect detection accuracy, inspection workflow flexibility, compliance features, IoT integration capability, and analytics depth. Request demos with your production data.",
      "position": 3
    });
    steps.push({
      "@type": "HowToStep",
      "name": "Integration Planning",
      "text": "Plan integration with production equipment (IoT sensors, PLCs), ERP systems, and supplier management. Identify data flows between quality system and production lines for real-time monitoring.",
      "position": 4
    });
    steps.push({
      "@type": "HowToStep",
      "name": "Rollout and Training",
      "text": "Deploy with phased approach: start with defect tracking, then inspection workflows, finally predictive analytics. Train quality teams on defect entry, root cause analysis, and compliance documentation.",
      "position": 5
    });
  } else {
    // Generic steps
    howToTitle = "How to Choose the Right Management System";
    description = "Guide to selecting and implementing management software for your business operations";
    steps.push({
      "@type": "HowToStep",
      "name": "Assess Business Needs",
      "text": "Evaluate your current operations, identify pain points, and determine key features needed including inventory management, booking systems, customer tracking, and financial reporting capabilities.",
      "position": 1
    });
    steps.push({
      "@type": "HowToStep",
      "name": "Compare Software Options",
      "text": "Research and compare available platforms based on features, pricing, scalability, integration capabilities, and industry-specific functionality. Request demos and read user reviews.",
      "position": 2
    });
    steps.push({
      "@type": "HowToStep",
      "name": "Calculate ROI",
      "text": "Estimate return on investment by calculating efficiency gains, cost reductions, and revenue improvements. Factor in software costs, implementation time, and training requirements.",
      "position": 3
    });
    steps.push({
      "@type": "HowToStep",
      "name": "Plan Implementation",
      "text": "Create implementation timeline including data migration, system configuration, staff training, and integration setup. Plan phased rollout to minimize disruption to operations.",
      "position": 4
    });
  }

  return {
    "@context": "https://schema.org",
    "@type": "HowTo",
    "name": howToTitle,
    "description": description,
    "step": steps
  };
}

// Process a single JSON file
function processFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const data = JSON.parse(content);

    // Check if schemas already exist
    if (data.faq_schema && data.howto_schema) {
      stats.skipped++;
      return { skipped: true };
    }

    // Extract category from path
    const pathParts = filePath.split('/');
    const categoryIndex = pathParts.findIndex(p => categories.includes(p));
    const category = categoryIndex >= 0 ? pathParts[categoryIndex] : 'general';

    // Generate schemas
    data.faq_schema = generateFAQSchema(data.title, data.content, category);
    data.howto_schema = generateHowToSchema(data.title, data.content, category);

    // Write back to file
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    stats.processed++;

    return { success: true, category };
  } catch (error) {
    stats.errors++;
    console.error(`Error processing ${filePath}: ${error.message}`);
    return { error: error.message };
  }
}

// Main processing
function main() {
  console.log('Starting schema generation for batch 17...\n');

  // Collect all files to process
  const allFiles = [];

  for (const category of categories) {
    const categoryPath = path.join(dataDir, category);
    const zhCategoryPath = path.join(dataDir, 'zh', category);

    if (fs.existsSync(categoryPath)) {
      const files = fs.readdirSync(categoryPath).filter(f => f.endsWith('.json'));
      files.forEach(f => allFiles.push(path.join(categoryPath, f)));
    }

    if (fs.existsSync(zhCategoryPath)) {
      const files = fs.readdirSync(zhCategoryPath).filter(f => f.endsWith('.json'));
      files.forEach(f => allFiles.push(path.join(zhCategoryPath, f)));
    }
  }

  stats.totalFiles = allFiles.length;
  console.log(`Found ${stats.totalFiles} files to process\n`);

  // Process each file
  for (const filePath of allFiles) {
    const result = processFile(filePath);
    if (result.success) {
      console.log(`✓ Processed: ${path.basename(filePath)} (${result.category})`);
    } else if (result.skipped) {
      console.log(`○ Skipped: ${path.basename(filePath)} (schemas already exist)`);
    }
  }

  // Print summary
  console.log('\n========================================');
  console.log('Schema Generation Summary');
  console.log('========================================');
  console.log(`Total files found: ${stats.totalFiles}`);
  console.log(`Successfully processed: ${stats.processed}`);
  console.log(`Skipped (already had schemas): ${stats.skipped}`);
  console.log(`Errors: ${stats.errors}`);
  console.log('========================================\n');

  // List processed files by category
  console.log('Processed files by category:');
  for (const category of categories) {
    const engPath = path.join(dataDir, category);
    const zhPath = path.join(dataDir, 'zh', category);

    let count = 0;
    if (fs.existsSync(engPath)) {
      count += fs.readdirSync(engPath).filter(f => f.endsWith('.json')).length;
    }
    if (fs.existsSync(zhPath)) {
      count += fs.readdirSync(zhPath).filter(f => f.endsWith('.json')).length;
    }
    console.log(`  ${category}: ${count} files`);
  }
}

main();