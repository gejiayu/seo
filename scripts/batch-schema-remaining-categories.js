#!/usr/bin/env node
/**
 * Batch Schema Generator for Remaining Categories
 * Processes multiple categories in order of file count
 * Adds FAQ Schema (5-7 Q&A) and HowTo Schema (3-5 steps) to files
 */

const fs = require('fs');
const path = require('path');

// Categories to process (sorted by file count - descending)
const CATEGORIES_TO_PROCESS = [
  'retail-pos-inventory-tools',        // 63 files
  'wedding-event-rental-tools',        // 50 files
  'education-training-tools',          // 50 files
  'logistics-warehouse-management-tools', // 43 files
  'jewelry-watch-retail-tools',        // 43 files
  'camping-outdoor-gear-rental-tools', // 33 files
  'landscaping-grounds-maintenance',   // 32 files
  'agricultural-farming-rental-tools', // 31 files
  'laundry-dry-cleaning-tools',        // 28 files
  'kitchen-cooking-rental-tools',      // 26 files
  'sports-equipment-rental-tools',     // 25 files
  'event-planning-tools',              // 13 files
  'education-lms-platform-tools',      // 13 files
  'audio-video-equipment-rental-tools', // 5 files
  'renewable-energy-management-tools', // 2 files
  'banking-financial-services-tools',  // 2 files
];

// Stats tracking
const stats = {
  totalFiles: 0,
  processed: 0,
  skipped: 0,
  failed: 0,
  alreadyHasSchemas: 0,
  categoryStats: {}
};

// Category type mappings for schema generation
const CATEGORY_TYPES = {
  'retail-pos-inventory-tools': 'retail',
  'wedding-event-rental-tools': 'event_rental',
  'education-training-tools': 'education',
  'logistics-warehouse-management-tools': 'logistics',
  'jewelry-watch-retail-tools': 'retail',
  'camping-outdoor-gear-rental-tools': 'rental',
  'landscaping-grounds-maintenance': 'service',
  'agricultural-farming-rental-tools': 'agricultural_rental',
  'laundry-dry-cleaning-tools': 'service',
  'kitchen-cooking-rental-tools': 'rental',
  'sports-equipment-rental-tools': 'rental',
  'event-planning-tools': 'event',
  'education-lms-platform-tools': 'education',
  'audio-video-equipment-rental-tools': 'rental',
  'renewable-energy-management-tools': 'energy',
  'banking-financial-services-tools': 'financial'
};

/**
 * Generate FAQ schema based on title and category type
 */
function generateFaqSchema(title, categoryType) {
  const topicMatch = title.match(/^(.+?)(?:\s+(?:2026|Best|Comparison|Review|Tools|Platforms|Software|Guide))/i);
  const topic = topicMatch ? topicMatch[1].trim() : 'business tools';

  // Category-specific question templates
  const questionSets = {
    retail: [
      { q: `What are the key features of ${topic}?`, a: `${topic} typically include inventory management, POS capabilities, customer tracking, sales reporting, barcode scanning, multi-store management, mobile payment support, and integration with e-commerce platforms. Modern systems also offer AI-powered analytics and real-time inventory updates.` },
      { q: `How much does ${topic} cost?`, a: `Pricing varies by scale. Basic retail systems start at $50-100/month, mid-tier solutions range $100-300/month, and enterprise platforms cost $300-800/month. Additional costs may include hardware, payment processing fees, and premium support packages.` },
      { q: `What are the benefits for small businesses?`, a: `Small businesses gain automated inventory tracking, faster checkout processes, reduced stock errors, improved customer service, sales analytics, loyalty program management, and omnichannel capabilities. Systems typically reduce manual inventory work by 50-70%.` },
      { q: `How do these systems integrate with existing platforms?`, a: `${topic} offer integration through APIs, pre-built connectors for major e-commerce platforms (Shopify, WooCommerce), accounting software (QuickBooks), payment gateways, and shipping carriers. Most support real-time sync and webhook notifications.` },
      { q: `What security features are included?`, a: `Security includes PCI compliance, data encryption, access controls, audit logging, employee permission management, secure payment processing, fraud detection, regular backups, and GDPR/CCPA compliance features.` },
      { q: `Can these tools help with inventory optimization?`, a: `Yes, tools provide automated reorder alerts, stock level tracking, demand forecasting, vendor management, purchase order automation, dead stock identification, and inventory turnover analytics to optimize stock levels.` }
    ],
    event_rental: [
      { q: `What items can be rented through ${topic}?`, a: `${topic} offer rentals for event essentials including tables, chairs, linens, dinnerware, centerpieces, tents, lighting, audio/visual equipment, staging, dance floors, and decorative items. Most services include delivery, setup, and pickup.` },
      { q: `How much does ${topic} rental cost?`, a: `Costs depend on item types and quantity. Basic furniture rentals range $2-15 per item daily, premium items $20-100 daily. Complete event packages start at $500-2000, with large events costing $2000-10000+ depending on guest count.` },
      { q: `What is included in rental services?`, a: `Most packages include delivery, professional setup, breakdown, and pickup. Premium services offer event coordination, on-site support, backup equipment, styling consultations, and rush delivery options.` },
      { q: `How far in advance should I book rentals?`, a: `For major events, book 3-6 months ahead. Smaller events require 2-4 weeks minimum. Peak seasons (spring/summer) need earlier booking. Last-minute bookings may have limited inventory or premium pricing.` },
      { q: `What happens if rented items are damaged?`, a: `Rental agreements typically include damage waivers or insurance options. Minor damage may be covered under standard fees. Major damage requires replacement costs. Most companies offer damage protection plans for added coverage.` },
      { q: `Can rentals be customized for specific themes?`, a: `Yes, services offer custom color selections, theme-specific decor, fabric choices, centerpiece arrangements, lighting designs, and branded items. Consultations help match rentals to event vision and venue requirements.` }
    ],
    education: [
      { q: `What features does ${topic} offer?`, a: `${topic} include learning management, course creation tools, student tracking, automated grading, content libraries, video hosting, discussion forums, certificate generation, and analytics dashboards. Advanced features include adaptive learning and AI tutoring.` },
      { q: `What is the pricing structure?`, a: `Educational platforms typically charge per student or course. Basic plans start at $5-20 per student monthly, institutional licenses range $500-5000 monthly, and enterprise solutions cost $5000-20000+ annually. Free tiers often exist for small classes.` },
      { q: `How do these tools support remote learning?`, a: `Platforms provide video conferencing, asynchronous learning modules, mobile apps, offline access, virtual classrooms, interactive whiteboards, breakout rooms, peer collaboration tools, and cloud-based content delivery.` },
      { q: `What analytics and tracking features are available?`, a: `Tools offer engagement metrics, completion rates, time-tracking, assessment scores, learning path progress, competency mapping, dropout predictions, attendance tracking, and detailed performance reports for students and courses.` },
      { q: `How do educators create and manage content?`, a: `Features include drag-drop course builders, multimedia embedding, quiz creators, assignment templates, rubric systems, content banks, version control, collaborative editing, and automatic backup of educational materials.` },
      { q: `What integration options exist?`, a: `Platforms integrate with student information systems, video tools (Zoom/Teams), calendars, payment gateways, authentication systems, plagiarism checkers, e-textbooks, and third-party educational content providers.` }
    ],
    logistics: [
      { q: `What core features does ${topic} provide?`, a: `${topic} include inventory control, order fulfillment, shipping integration, barcode scanning, warehouse mapping, pick-pack optimization, real-time tracking, demand forecasting, and multi-location management. Advanced features include robotics integration and IoT sensors.` },
      { q: `What is typical pricing?`, a: `Warehouse management systems range from $100-500 monthly for small operations, $500-2000 for mid-sized, and $2000-10000+ for large enterprises. Cloud-based solutions often charge per transaction or storage volume.` },
      { q: `How do these tools improve warehouse efficiency?`, a: `Systems reduce picking errors by 60-80%, improve inventory accuracy to 99%+, cut fulfillment time by 30-50%, optimize storage space, automate reorder processes, and provide real-time visibility into stock levels across locations.` },
      { q: `What shipping integrations are supported?`, a: `Tools connect with major carriers (FedEx, UPS, USPS), freight forwarders, parcel services, last-mile delivery, international shipping, customs systems, and provide rate comparison, label generation, and tracking updates.` },
      { q: `Can these systems handle multiple warehouses?`, a: `Yes, enterprise solutions support multi-location inventory, cross-docking, transfer management, regional fulfillment optimization, distributed order routing, and centralized reporting across all warehouse locations.` },
      { q: `What reporting capabilities exist?`, a: `Platforms offer inventory turnover reports, fulfillment metrics, accuracy tracking, cost analysis, productivity reports, cycle time analytics, stock aging reports, and customizable dashboards for operations management.` }
    ],
    rental: [
      { q: `What equipment is available through ${topic}?`, a: `${topic} offer various equipment including professional-grade items, recreational gear, specialty tools, safety equipment, and maintenance supplies. Rental inventory ranges from basic to premium options with different specifications.` },
      { q: `What are typical rental rates?`, a: `Daily rates range $10-50 for basic equipment, $50-200 for standard items, and $200-500+ for premium/specialty equipment. Weekly rentals often offer 30-40% discounts. Monthly packages provide best value for extended use.` },
      { q: `What is included in rental packages?`, a: `Most rentals include basic accessories, instruction guides, safety equipment where applicable, insurance options, delivery/pickup services (may vary), maintenance support, and replacement guarantees for defective items.` },
      { q: `What are rental requirements and policies?`, a: `Rentals typically require ID verification, credit card deposit, signed agreement, and possibly insurance verification. Policies cover damage liability, late fees, cancellation terms, and equipment return conditions.` },
      { q: `How do I reserve rental equipment?`, a: `Book online through rental platforms, call customer service, or visit physical locations. Early reservations recommended for peak seasons. Many services offer real-time availability checking and instant confirmation.` },
      { q: `What support services are provided?`, a: `Services include equipment training, setup assistance, troubleshooting support, emergency replacements, technical consultations, usage guidance, and customer service via phone, email, or live chat.` }
    ],
    service: [
      { q: `What services does ${topic} provide?`, a: `${topic} offer professional service delivery including scheduling, client management, service tracking, billing automation, route optimization, team coordination, quality assurance, and performance analytics.` },
      { q: `What are typical costs?`, a: `Service business software ranges from $30-100 monthly for basic tools, $100-300 for professional tiers, and $300-800+ for enterprise solutions. Pricing often scales by users, clients, or service volume.` },
      { q: `How do these tools help with scheduling?`, a: `Features include online booking, calendar sync, automated reminders, recurring appointments, team scheduling, availability management, conflict resolution, waitlists, and customer self-service portals.` },
      { q: `What client management features exist?`, a: `Tools provide customer databases, service history, preferences tracking, communication logs, loyalty programs, feedback collection, automated follow-ups, and CRM integration for comprehensive client relationships.` },
      { q: `Can these systems handle field operations?`, a: `Yes, mobile apps enable on-site service delivery, GPS tracking, digital signatures, photo documentation, real-time updates, field-to-office sync, route optimization, and location-based customer assignments.` },
      { q: `What integrations are available?`, a: `Platforms connect with accounting software, payment processors, calendar systems, email marketing, GPS tools, communication apps, industry-specific databases, and third-party APIs for extended functionality.` }
    ],
    agricultural_rental: [
      { q: `What equipment can be rented for agricultural use?`, a: `${topic} provide tractors, harvesters, irrigation systems, sprayers, planting equipment, tillage tools, grain handling, GPS-guided machinery, drones for field monitoring, and specialized crop processing equipment.` },
      { q: `What are rental costs for farm equipment?`, a: `Daily rates: small equipment $50-150, medium machinery $200-500, large equipment $500-1500+. Weekly rentals offer significant savings. Seasonal packages available for planting/harvesting periods. Insurance typically extra.` },
      { q: `How does equipment rental benefit farms?`, a: `Rental reduces capital investment, provides access to latest technology, handles seasonal needs without ownership costs, offers specialized equipment for specific tasks, and provides backup during breakdowns or peak periods.` },
      { q: `What support is included with rentals?`, a: `Services include equipment delivery, setup assistance, operator training (where needed), maintenance support, field service calls, replacement units, insurance options, and technical support during rental period.` },
      { q: `How do I choose appropriate equipment?`, a: `Consult with rental specialists about crop types, field size, soil conditions, timing requirements, and budget. They recommend suitable equipment, provide specifications, and offer demonstrations before rental.` },
      { q: `What scheduling flexibility exists?`, a: `Reservations available by day, week, or season. Early booking recommended for peak agricultural seasons. Some services offer standby equipment, emergency rentals, and flexible return policies for weather delays.` }
    ],
    event: [
      { q: `What planning services does ${topic} include?`, a: `${topic} provide event design, vendor coordination, timeline management, budget tracking, guest management, venue selection, logistics planning, contract negotiation, contingency planning, and post-event analysis.` },
      { q: `What are typical service costs?`, a: `Event planning fees vary by event size: social events $500-3000, corporate events $2000-10000, large productions $10000-50000+. Hourly consulting $50-200. Package pricing often includes planning, coordination, and vendor management.` },
      { q: `How far in advance should events be planned?`, a: `Major events: 6-12 months. Corporate events: 3-6 months. Social events: 2-4 months. Last-minute planning available but may limit venue/vendor options and increase costs due to rush bookings.` },
      { q: `What vendor coordination services exist?`, a: `Planners manage vendor selection, contract negotiation, scheduling, delivery coordination, setup supervision, quality control, payment processing, and post-event vendor relations including feedback and issue resolution.` },
      { q: `Can planners handle multiple event types?`, a: `Yes, professionals manage weddings, corporate meetings, conferences, parties, fundraisers, product launches, and specialty events. Each type has specific expertise, vendor networks, and planning methodologies.` },
      { q: `What technology do planners use?`, a: `Tools include event management software, budgeting apps, timeline tools, guest list managers, floor plan designers, vendor databases, communication platforms, and project tracking systems for comprehensive planning.` }
    ],
    energy: [
      { q: `What energy management features does ${topic} offer?`, a: `${topic} include consumption monitoring, efficiency analysis, cost tracking, renewable integration, grid management, predictive maintenance, emissions reporting, automated controls, and sustainability metrics.` },
      { q: `What are typical implementation costs?`, a: `Basic monitoring systems: $500-2000 setup. Professional platforms: $2000-10000 annually. Enterprise solutions: $10000-50000+. ROI typically achieved through 10-30% energy cost reduction within 1-2 years.` },
      { q: `How do these tools optimize energy usage?`, a: `Systems identify waste patterns, automate peak shaving, optimize HVAC schedules, manage lighting controls, coordinate renewable sources, balance grid loads, and provide actionable recommendations for efficiency improvements.` },
      { q: `What renewable energy tracking exists?`, a: `Tools monitor solar/wind generation, track feed-in tariffs, manage battery storage, calculate carbon offsets, forecast production, compare grid vs. renewable costs, and report sustainability metrics for compliance.` },
      { q: `Can systems integrate with existing infrastructure?`, a: `Yes, platforms connect with building management systems, utility meters, solar inverters, wind turbines, battery systems, HVAC controls, lighting networks, and IoT sensors for comprehensive energy management.` },
      { q: `What reporting and compliance features exist?`, a: `Tools generate consumption reports, carbon footprint calculations, efficiency benchmarks, regulatory compliance documentation, sustainability scorecards, and data exportable for audits and certifications.` }
    ],
    financial: [
      { q: `What services does ${topic} provide?`, a: `${topic} offer transaction processing, account management, payment solutions, fraud detection, compliance monitoring, risk assessment, reporting dashboards, customer portals, and integration with financial networks.` },
      { q: `What are typical platform costs?`, a: `Financial service platforms range from $500-2000 monthly for basic services, $2000-5000 for professional tiers, and $5000-20000+ for enterprise solutions. Transaction fees may apply based on volume.` },
      { q: `How do these tools ensure security?`, a: `Security includes encryption, multi-factor authentication, fraud detection algorithms, PCI compliance, regulatory audits, access controls, transaction monitoring, secure data storage, and real-time threat detection.` },
      { q: `What compliance features are included?`, a: `Tools support KYC/AML verification, regulatory reporting, audit trails, documentation management, policy enforcement, risk scoring, suspicious activity monitoring, and compliance with financial regulations.` },
      { q: `Can platforms handle multiple financial products?`, a: `Yes, systems manage accounts, payments, loans, investments, cards, transfers, and various financial services. Modular design allows institutions to deploy needed features while maintaining unified operations.` },
      { q: `What integration options exist?`, a: `Platforms connect with core banking systems, payment networks, credit bureaus, regulatory databases, customer CRMs, accounting systems, and third-party fintech services through APIs and standardized protocols.` }
    ]
  };

  // Get appropriate questions based on category type
  const questions = questionSets[categoryType] || questionSets.retail;
  const selectedQuestions = questions.slice(0, 6);

  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": selectedQuestions.map(item => ({
      "@type": "Question",
      "name": item.q,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": item.a
      }
    }))
  };
}

/**
 * Generate HowTo schema based on title and category type
 */
function generateHowToSchema(title, categoryType) {
  const topicMatch = title.match(/^(.+?)(?:\s+(?:2026|Best|Comparison|Review|Tools|Platforms|Software|Guide))/i);
  const topic = topicMatch ? topicMatch[1].trim() : 'business tools';

  // Category-specific step templates
  const stepSets = {
    retail: [
      { name: "Evaluate Business Needs", text: "Assess your store's size, inventory volume, transaction frequency, customer flow, payment methods needed, and growth plans. Identify must-have features versus optional capabilities." },
      { name: "Compare Top Solutions", text: "Research leading ${topic} platforms. Review features, pricing structures, hardware compatibility, integration options, and user reviews. Request demos from 3-5 vendors matching your needs." },
      { name: "Verify Integration Compatibility", text: "Check compatibility with existing hardware, e-commerce platforms, accounting software, payment processors, and inventory systems. Test integration capabilities with current business tools." },
      { name: "Plan Implementation", text: "Create rollout timeline including hardware installation, software configuration, staff training, data migration, and testing phases. Schedule parallel running period to catch issues early." },
      { name: "Train Staff and Launch", text: "Train all employees on POS operations, inventory procedures, customer handling, and troubleshooting. Execute phased launch starting with pilot location before full deployment." }
    ],
    event_rental: [
      { name: "Determine Rental Needs", text: "List all items needed for your event including quantities, styles, delivery timeline, and budget constraints. Consider venue requirements and guest count for accurate quantities." },
      { name: "Research Rental Companies", text: "Compare ${topic} services in your area. Review inventory availability, pricing, delivery options, setup services, reviews, and package deals. Request quotes from multiple providers." },
      { name: "Verify Availability and Terms", text: "Confirm item availability for your event date. Review rental agreements including deposit requirements, damage policies, delivery fees, cancellation terms, and insurance options." },
      { name: "Schedule Delivery and Setup", text: "Coordinate delivery timing with venue access. Confirm setup requirements, placement instructions, and breakdown schedule. Arrange venue walkthrough if needed for proper placement." },
      { name: "Execute Event and Return", text: "Supervise setup verification, use items during event, coordinate breakdown timing, ensure proper item condition for return, and schedule pickup with rental company." }
    ],
    education: [
      { name: "Define Learning Objectives", text: "Identify course goals, target audience, learning outcomes, assessment criteria, content formats needed, and engagement requirements. Map objectives to platform capabilities." },
      { name: "Evaluate Platform Features", text: "Compare ${topic} options for content creation, student management, assessment tools, analytics, integrations, mobile access, and scalability. Request demos from education-focused vendors." },
      { name: "Configure Learning Environment", text: "Set up course structure, upload content, configure assessments, establish enrollment rules, create discussion areas, set up grading systems, and integrate external resources." },
      { name: "Develop and Test Content", text: "Create engaging learning materials using platform tools. Test all content for functionality, accessibility, mobile compatibility, and student experience. Pilot with small group for feedback." },
      { name: "Launch and Monitor Progress", text: "Enroll students, provide orientation, track engagement through analytics, address technical issues promptly, collect feedback, and continuously improve based on learning data." }
    ],
    logistics: [
      { name: "Analyze Warehouse Operations", text: "Map current processes, inventory volume, order flow, picking methods, storage layout, team structure, pain points, and growth projections. Define efficiency targets and integration needs." },
      { name: "Compare Warehouse Systems", text: "Evaluate ${topic} solutions for inventory control, order management, shipping integration, reporting, mobile capabilities, and scalability. Consider deployment model (cloud vs. on-premise)." },
      { name: "Design Warehouse Mapping", text: "Configure warehouse zones, bin locations, pick paths, staging areas, and workflow rules in the system. Import or create inventory database with accurate starting positions." },
      { name: "Integrate Operations", text: "Connect with ERP systems, e-commerce platforms, shipping carriers, barcode scanners, and IoT devices. Configure automation rules for reordering, routing, and notifications." },
      { name: "Train Team and Optimize", text: "Train warehouse staff on all system functions, processes, and troubleshooting. Monitor performance metrics, identify optimization opportunities, and refine procedures continuously." }
    ],
    rental: [
      { name: "Identify Equipment Requirements", text: "Determine specific equipment types, specifications, quantities, duration needed, and budget constraints. Research availability and consider alternatives if preferred items unavailable." },
      { name: "Compare Rental Options", text: "Evaluate ${topic} providers based on inventory, pricing, quality, delivery options, support services, insurance options, and reviews. Request quotes from multiple rental services." },
      { name: "Reserve and Arrange Terms", text: "Book equipment with deposit, review rental agreement terms, arrange delivery/pickup schedule, confirm insurance coverage, and verify equipment specifications match needs." },
      { name: "Receive and Inspect", text: "Inspect delivered equipment for condition and functionality. Report any issues immediately. Understand proper operation with training if provided. Document equipment condition." },
      { name: "Use and Return", text: "Operate equipment properly following guidelines. Maintain condition during use. Schedule return pickup, prepare equipment for return, and ensure all items accounted for upon pickup." }
    ],
    service: [
      { name: "Map Service Workflow", text: "Document current service processes, client touchpoints, scheduling methods, team coordination, billing procedures, and quality checkpoints. Identify improvement areas and must-have features." },
      { name: "Compare Service Platforms", text: "Research ${topic} solutions for scheduling, client management, mobile capabilities, routing, reporting, and integrations. Evaluate pricing models and scalability for business growth." },
      { name: "Configure Operations", text: "Set up service catalog, pricing rules, scheduling templates, client categories, team assignments, notification triggers, and reporting dashboards. Import existing client and service data." },
      { name: "Train Team and Launch", text: "Train service staff on scheduling, client interactions, mobile app usage, billing, and reporting. Begin with pilot clients before full rollout. Establish support procedures for issues." },
      { name: "Monitor and Optimize", text: "Track service metrics including satisfaction, efficiency, revenue, and team performance. Use analytics to optimize routes, schedules, and client relationships. Continuously improve based on data." }
    ],
    agricultural_rental: [
      { name: "Assess Farm Requirements", text: "Evaluate crop types, field sizes, soil conditions, seasonal needs, labor availability, and budget. Determine which equipment rentals will optimize planting, maintenance, or harvest operations." },
      { name: "Research Agricultural Rentals", text: "Compare ${topic} providers for equipment availability, specifications, rental terms, delivery options, training services, and support. Verify equipment matches your specific agricultural needs." },
      { name: "Schedule Seasonal Rentals", text: "Book equipment well in advance for peak seasons (planting/harvesting). Confirm delivery dates, setup services, operator training if needed, and support availability during rental period." },
      { name: "Prepare and Train", text: "Ensure field readiness for equipment arrival. Complete operator training for complex machinery. Verify safety protocols and maintenance procedures. Document equipment condition upon delivery." },
      { name: "Operate and Return", text: "Use equipment following operational guidelines and safety requirements. Schedule maintenance checks if included. Coordinate return timing with rental company, ensuring equipment condition for pickup." }
    ],
    event: [
      { name: "Define Event Vision", text: "Establish event purpose, target audience, guest count, budget range, venue preferences, theme/style, and key requirements. Create preliminary timeline from planning to post-event." },
      { name: "Engage Planning Services", text: "Compare ${topic} planners based on event expertise, portfolio, reviews, pricing, and availability. Interview candidates, review proposals, and select planner matching your vision and budget." },
      { name: "Collaborate on Planning", text: "Work with planner on venue selection, vendor coordination, timeline development, budget allocation, logistics planning, and contingency preparations. Maintain regular communication throughout planning." },
      { name: "Coordinate Pre-Event Setup", text: "Oversee vendor deliveries, venue setup, technical installations, final walkthroughs, and contingency activation if needed. Confirm all arrangements with planner before event day." },
      { name: "Execute and Evaluate", text: "Ensure smooth event execution with planner coordination. Manage real-time adjustments. Collect feedback post-event. Review planner's post-event analysis and document lessons for future events." }
    ],
    energy: [
      { name: "Audit Energy Consumption", text: "Analyze current energy usage patterns, costs, inefficiencies, and sustainability goals. Identify monitoring needs, potential savings areas, and priority systems for optimization." },
      { name: "Evaluate Management Platforms", text: "Compare ${topic} solutions for monitoring capabilities, integration options, analytics features, automation controls, reporting tools, and scalability. Consider deployment model and support needs." },
      { name: "Implement Monitoring Systems", text: "Deploy sensors, meters, and monitoring hardware. Configure platform dashboards, alerts, reporting templates, and automation rules. Integrate with existing building management systems." },
      { name: "Analyze and Optimize", text: "Use platform analytics to identify waste patterns, optimization opportunities, and efficiency improvements. Configure automated controls for peak shaving and load balancing." },
      { name: "Report and Maintain", text: "Generate compliance reports, sustainability metrics, and ROI documentation. Maintain system through regular updates, sensor calibration, and continuous improvement based on data insights." }
    ],
    financial: [
      { name: "Assess Financial Operations", text: "Evaluate transaction volumes, compliance requirements, security needs, customer touchpoints, integration requirements, and growth projections. Define platform must-haves and future scalability needs." },
      { name: "Compare Financial Platforms", text: "Research ${topic} solutions for features, compliance certifications, security standards, integration capabilities, pricing models, and vendor reputation in financial services." },
      { name: "Verify Security and Compliance", text: "Confirm PCI compliance, regulatory certifications, data encryption standards, audit capabilities, and fraud prevention features. Ensure platform meets all applicable financial regulations." },
      { name: "Plan Integration and Deployment", text: "Map integration points with core systems, payment networks, and customer channels. Plan phased deployment, data migration, staff training, and parallel operation periods." },
      { name: "Launch and Monitor", text: "Execute deployment with security testing, compliance verification, staff training completion. Monitor transaction success rates, security metrics, and compliance adherence post-launch." }
    ]
  };

  // Get appropriate steps based on category type
  const steps = stepSets[categoryType] || stepSets.retail;

  return {
    "@context": "https://schema.org",
    "@type": "HowTo",
    "name": `How to Choose and Implement ${topic}`,
    "description": `Step-by-step guide for selecting and deploying ${topic}`,
    "totalTime": "PT1-4W",
    "estimatedCost": {
      "@type": "MonetaryAmount",
      "currency": "USD",
      "value": "100-5000"
    },
    "step": steps.map((step, index) => ({
      "@type": "HowToStep",
      "name": step.name,
      "text": step.text.replace('${topic}', topic),
      "position": index + 1
    }))
  };
}

/**
 * Process a single JSON file
 */
function processFile(filePath, categoryType) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const data = JSON.parse(content);

    // Check if schemas already exist
    if (data.faq_schema && data.howto_schema) {
      stats.alreadyHasSchemas++;
      stats.skipped++;
      return { status: 'skipped', reason: 'already_has_schemas' };
    }

    // Generate schemas if missing
    const title = data.title || '';

    if (!data.faq_schema) {
      data.faq_schema = generateFaqSchema(title, categoryType);
    }

    if (!data.howto_schema) {
      data.howto_schema = generateHowToSchema(title, categoryType);
    }

    // Write back to file
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n', 'utf8');

    stats.processed++;
    return { status: 'processed', file: path.basename(filePath) };

  } catch (error) {
    stats.failed++;
    return { status: 'failed', file: path.basename(filePath), error: error.message };
  }
}

/**
 * Process a category directory
 */
function processCategory(categoryName) {
  const categoryDir = path.join(__dirname, '..', 'data', categoryName);

  if (!fs.existsSync(categoryDir)) {
    console.log(`Category directory not found: ${categoryName}`);
    return;
  }

  const categoryType = CATEGORY_TYPES[categoryName] || 'retail';

  console.log(`\nProcessing ${categoryName} (${categoryType} type)...\n`);

  // Get all JSON files
  const files = fs.readdirSync(categoryDir)
    .filter(file => file.endsWith('.json'))
    .map(file => path.join(categoryDir, file));

  const categoryFiles = files.length;
  stats.categoryStats[categoryName] = {
    total: categoryFiles,
    processed: 0,
    skipped: 0,
    failed: 0
  };

  stats.totalFiles += categoryFiles;
  console.log(`Found ${categoryFiles} JSON files in ${categoryName}\n`);

  // Process each file
  const results = [];
  for (const file of files) {
    const result = processFile(file, categoryType);
    results.push(result);

    if (result.status === 'processed') {
      stats.categoryStats[categoryName].processed++;
      console.log(`  ✓ ${result.file}`);
    } else if (result.status === 'skipped') {
      stats.categoryStats[categoryName].skipped++;
      console.log(`  ⊗ ${result.file} (has schemas)`);
    } else {
      stats.categoryStats[categoryName].failed++;
      console.log(`  ✗ ${result.file} - ${result.error}`);
    }
  }

  // Category summary
  const catStats = stats.categoryStats[categoryName];
  console.log(`\n${categoryName} Summary: ${catStats.processed}/${catStats.total} processed (${((catStats.processed/catStats.total)*100).toFixed(1)}%)`);
}

/**
 * Main processing function
 */
function main() {
  console.log('='.repeat(70));
  console.log('BATCH SCHEMA GENERATOR - REMAINING CATEGORIES');
  console.log('='.repeat(70));
  console.log(`Categories to process: ${CATEGORIES_TO_PROCESS.length}`);
  console.log('Order: By file count (descending)\n');

  // Process each category in order
  for (const category of CATEGORIES_TO_PROCESS) {
    processCategory(category);
  }

  // Final summary
  console.log('\n' + '='.repeat(70));
  console.log('FINAL SUMMARY REPORT');
  console.log('='.repeat(70));
  console.log(`Total files found:      ${stats.totalFiles}`);
  console.log(`Successfully processed: ${stats.processed}`);
  console.log(`Skipped (has schemas):  ${stats.alreadyHasSchemas}`);
  console.log(`Failed:                 ${stats.failed}`);
  console.log(`Overall success rate:   ${((stats.processed / stats.totalFiles) * 100).toFixed(1)}%`);
  console.log('='.repeat(70));

  // Per-category breakdown
  console.log('\nCategory Breakdown:');
  for (const [cat, catStats] of Object.entries(stats.categoryStats)) {
    console.log(`  ${cat}: ${catStats.processed}/${catStats.total} (${((catStats.processed/catStats.total)*100).toFixed(1)}%)`);
  }

  if (stats.failed > 0) {
    console.log('\nFailed files (across all categories):');
    // We'd need to track these separately to show them here
  }
}

// Run
main();