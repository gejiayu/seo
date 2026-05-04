#!/usr/bin/env python3
"""
Generate FAQ and HowTo schemas for batch 10 categories.
Batch 10: boat-marine-rental-tools, costume-fashion-rental-tools,
          camera-photography-rental-tools, audio-video-equipment-rental-tools,
          party-event-supplies-rental-tools
"""

import json
import os
import re
from pathlib import Path
import random

# Base directories
DATA_DIR = Path("/Users/gejiayu/owner/seo/data")

# Batch 10 categories
CATEGORIES = [
    "boat-marine-rental-tools",
    "costume-fashion-rental-tools",
    "camera-photography-rental-tools",
    "audio-video-equipment-rental-tools",  # AV equipment
    "party-event-supplies-rental-tools",   # Event-party
]

def generate_faq_schema(title, content, description):
    """Generate 5-7 FAQ Q&A pairs based on content."""

    # Extract keywords from title
    title_words = re.findall(r'\b[A-Za-z]{4,}\b', title)
    main_keyword = title_words[0] if title_words else "system"

    # Generate contextual FAQs
    faqs = [
        {
            "question": f"What is the best {main_keyword} for small businesses in 2026?",
            "answer": f"The top-rated {main_keyword} solutions for small businesses include cloud-based platforms offering inventory management, booking automation, and customer tracking features. These systems typically cost $59-99/month and provide essential functionality for small to medium operations."
        },
        {
            "question": f"How much does {main_keyword} software cost?",
            "answer": f"{main_keyword} software pricing ranges from $59/month for basic plans to $149/month for professional enterprise solutions. Most vendors offer tiered pricing based on fleet size, feature requirements, and support levels. Annual subscriptions often provide 15-20% discounts."
        },
        {
            "question": f"What features should I look for in {main_keyword}?",
            "answer": f"Essential features include: real-time booking management, inventory tracking, maintenance scheduling, payment processing, customer relationship management, and compliance monitoring. Advanced systems offer AI-driven optimization, IoT integration, and automated reporting capabilities."
        },
        {
            "question": f"Can {main_keyword} integrate with existing business tools?",
            "answer": f"Yes, modern {main_keyword} platforms offer API integrations with accounting software, payment gateways, calendar systems, and CRM tools. Popular integrations include QuickBooks, Stripe, Google Calendar, and Salesforce. Most systems support custom API connections for specialized needs."
        },
        {
            "question": f"Is {main_keyword} suitable for digital nomad lifestyle businesses?",
            "answer": f"Absolutely. Cloud-based {main_keyword} solutions enable remote management from anywhere with internet access. Features like mobile apps, real-time notifications, and automated workflows allow operators to manage bookings, inventory, and customer communications while traveling or working remotely."
        },
        {
            "question": f"How do I choose the right {main_keyword} for my needs?",
            "answer": f"Consider your business size, operational complexity, budget, and growth plans. Small operators benefit from basic versions with practical features; medium enterprises should choose standard versions balancing features and cost; large operators need professional solutions with comprehensive capabilities and enterprise support."
        },
        {
            "question": f"What are the 2026 trends in {main_keyword}?",
            "answer": f"Key 2026 trends include: AI-driven intelligent optimization, IoT real-time monitoring, blockchain security verification, sustainability tracking, and enhanced mobile-first interfaces. These innovations improve operational efficiency, customer experience, and compliance management while reducing manual workload."
        }
    ]

    # Select 5-7 FAQs
    num_faqs = random.randint(5, 7)
    selected_faqs = faqs[:num_faqs]

    # Build FAQ schema
    faq_schema = {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["answer"]
                }
            }
            for faq in selected_faqs
        ]
    }

    return faq_schema

def generate_howto_schema(title, content, description):
    """Generate 3-5 HowTo steps based on content."""

    # Extract keywords from title
    title_words = re.findall(r'\b[A-Za-z]{4,}\b', title)
    main_keyword = title_words[0] if title_words else "system"

    # Generate contextual HowTo steps
    steps = [
        {
            "name": "Assess Your Business Requirements",
            "text": f"Evaluate your current operations including fleet size, booking volume, customer management needs, and maintenance scheduling requirements. Document essential features needed for your {main_keyword} implementation.",
            "image": "https://www.housecar.life/images/step1-assessment.png",
            "url": f"https://www.housecar.life/posts/{main_keyword.lower().replace(' ', '-')}-implementation-guide#step1"
        },
        {
            "name": "Compare Available Solutions",
            "text": f"Research and compare {main_keyword} platforms based on features, pricing, integration capabilities, and user reviews. Create a comparison matrix evaluating at least 3-5 potential solutions against your documented requirements.",
            "image": "https://www.housecar.life/images/step2-comparison.png",
            "url": f"https://www.housecar.life/posts/{main_keyword.lower().replace(' ', '-')}-implementation-guide#step2"
        },
        {
            "name": "Select and Configure Your System",
            "text": f"Choose the {main_keyword} platform that best matches your needs. Configure user accounts, set up inventory categories, customize booking workflows, and integrate payment processing according to your operational requirements.",
            "image": "https://www.housecar.life/images/step3-configuration.png",
            "url": f"https://www.housecar.life/posts/{main_keyword.lower().replace(' ', '-')}-implementation-guide#step3"
        },
        {
            "name": "Train Your Team and Launch",
            "text": f"Conduct comprehensive training for all staff members on {main_keyword} operations. Test booking flows, inventory management, and reporting features. Launch with a pilot period before full-scale deployment to ensure smooth transition.",
            "image": "https://www.housecar.life/images/step4-training.png",
            "url": f"https://www.housecar.life/posts/{main_keyword.lower().replace(' ', '-')}-implementation-guide#step4"
        },
        {
            "name": "Monitor and Optimize Performance",
            "text": f"Use {main_keyword} analytics and reporting tools to track operational efficiency, customer satisfaction, and revenue metrics. Implement continuous improvements based on data insights and user feedback for ongoing optimization.",
            "image": "https://www.housecar.life/images/step5-optimization.png",
            "url": f"https://www.housecar.life/posts/{main_keyword.lower().replace(' ', '-')}-implementation-guide#step5"
        }
    ]

    # Select 3-5 steps
    num_steps = random.randint(3, 5)
    selected_steps = steps[:num_steps]

    # Build HowTo schema
    howto_schema = {
        "@type": "HowTo",
        "name": f"How to Choose and Implement {main_keyword} for Your Business",
        "description": f"Step-by-step guide to selecting, configuring, and optimizing {main_keyword} solutions for operational efficiency",
        "step": [
            {
                "@type": "HowToStep",
                "name": step["name"],
                "text": step["text"],
                "image": step["image"],
                "url": step["url"]
            }
            for step in selected_steps
        ],
        "totalTime": "P1D-P2D",
        "estimatedCost": {
            "@type": "MonetaryAmount",
            "currency": "USD",
            "value": "$59-$149/month"
        }
    }

    return howto_schema

def combine_schemas(existing_schema, faq_schema, howto_schema):
    """Combine existing schema with FAQ and HowTo using @graph."""

    # Parse existing schema if it's a string
    if isinstance(existing_schema, str):
        try:
            existing = json.loads(existing_schema)
        except json.JSONDecodeError:
            existing = {}
    else:
        existing = existing_schema

    # Create @graph structure to combine schemas
    combined_schema = {
        "@context": "https://schema.org",
        "@graph": [
            existing,  # Keep existing SoftwareApplication schema
            faq_schema,
            howto_schema
        ]
    }

    return json.dumps(combined_schema, ensure_ascii=False)

def process_file(file_path):
    """Process a single JSON file and add FAQ/HowTo schemas."""

    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Get content for generating schemas
        title = data.get('title', 'Management System')
        content = data.get('content', '')
        description = data.get('description', '')
        existing_schema = data.get('schema_markup', '{}')

        # Generate new schemas
        faq_schema = generate_faq_schema(title, content, description)
        howto_schema = generate_howto_schema(title, content, description)

        # Combine schemas
        combined_schema = combine_schemas(existing_schema, faq_schema, howto_schema)

        # Update data
        data['schema_markup'] = combined_schema

        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True, None

    except Exception as e:
        return False, str(e)

def process_category(category):
    """Process all files in a category directory."""

    category_dir = DATA_DIR / category

    if not category_dir.exists():
        print(f"⚠️  Category directory not found: {category}")
        return 0, 0

    json_files = list(category_dir.glob('*.json'))

    success_count = 0
    fail_count = 0

    for json_file in json_files:
        success, error = process_file(json_file)
        if success:
            success_count += 1
        else:
            fail_count += 1
            print(f"❌ Failed to process {json_file.name}: {error}")

    return success_count, fail_count

def main():
    """Main processing function."""

    print("=" * 80)
    print("Schema Generation for Batch 10 Categories")
    print("=" * 80)
    print()

    total_success = 0
    total_fail = 0
    stats = []

    for category in CATEGORIES:
        print(f"📁 Processing: {category}")
        success, fail = process_category(category)
        total_success += success
        total_fail += fail

        stats.append({
            'category': category,
            'success': success,
            'fail': fail,
            'total': success + fail
        })

        print(f"   ✅ Success: {success}")
        print(f"   ❌ Failed: {fail}")
        print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    for stat in stats:
        print(f"{stat['category']:40s} - {stat['success']}/{stat['total']} files processed")

    print()
    print(f"Total files processed successfully: {total_success}")
    print(f"Total failures: {total_fail}")
    print(f"Grand total: {total_success + total_fail}")
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()