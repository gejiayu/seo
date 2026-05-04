#!/usr/bin/env python3
"""
Batch Schema Generator for SEO JSON files.
Generates FAQ Schema (FAQPage) and HowTo Schema for each JSON file.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any

# Base paths
DATA_DIR = Path("/Users/gejiayu/owner/seo/data")

# Categories to process
CATEGORIES = [
    "manufacturing-production-tools",
    "blue-collar-tools",
    "agriculture-farming-tools",
]

# Stats tracking
stats = {
    "total_files": 0,
    "processed": 0,
    "skipped": 0,
    "errors": 0,
    "faq_added": 0,
    "howto_added": 0,
}


def extract_tools_from_content(content: str) -> List[str]:
    """Extract tool names from content."""
    tools = []
    # Look for tool names in headings and specific patterns
    patterns = [
        r'<h3[^>]*>\d+>([A-Za-z][A-Za-z0-9\s]+)</h3>',  # numbered headings
        r'<h2[^>]*>([A-Za-z][A-Za-z0-9\s]+)(?:\s+(?:Review|Comparison|vs|tool|system|platform|software))?</h2>',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            clean_name = match.strip()
            if clean_name and len(clean_name) > 2 and clean_name not in tools:
                # Filter out generic terms
                generic_terms = ['background', 'introduction', 'conclusion', 'features', 'comparison',
                                 'trend', 'recommendation', 'guide', 'overview', 'summary', 'analysis']
                if clean_name.lower() not in generic_terms:
                    tools.append(clean_name)

    return tools[:5]  # Return top 5 tools


def extract_category_from_content(content: str) -> str:
    """Extract the main category/topic from content."""
    # Look for first h1 or h2
    h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    if h1_match:
        return h1_match.group(1).strip()

    h2_match = re.search(r'<h2[^>]*>([^<]+)</h2>', content)
    if h2_match:
        return h2_match.group(1).strip()

    return "Software Tool"


def generate_faq_schema(title: str, tools: List[str], category: str) -> Dict[str, Any]:
    """Generate FAQPage schema with 5-7 Q&A pairs."""

    # Generate contextual questions based on the content
    main_tool = tools[0] if tools else "This software"
    tool_list = ", ".join(tools[:3]) if len(tools) >= 3 else (tools[0] if tools else "these tools")

    faq_items = []

    # Q1: General overview question
    faq_items.append({
        "question": f"What are the key features of {category} tools like {main_tool}?",
        "answer": f"{main_tool} and similar {category} tools offer comprehensive functionality including management features, monitoring capabilities, automation tools, and reporting systems. These tools help businesses streamline operations, improve efficiency, and reduce manual tasks. {tool_list} are leading solutions in this category."
    })

    # Q2: Pricing/cost question
    faq_items.append({
        "question": f"How much does {category} software typically cost?",
        "answer": f"{category} software pricing varies based on features and scale. Entry-level solutions like {tools[1] if len(tools) > 1 else 'basic tools'} start around $49-99/month, while comprehensive platforms like {main_tool} range from $199-500/month. Enterprise solutions with advanced features can cost $1000+/month. Most tools offer free trials and tiered pricing to match business needs."
    })

    # Q3: Best for small business
    faq_items.append({
        "question": f"Which {category} tool is best for small businesses?",
        "answer": f"For small businesses, {tool_list} offer the best value. {main_tool} provides advanced features ideal for growing operations. {tools[1] if len(tools) > 1 else 'Budget alternatives'} offers affordable pricing with essential features. Consider your specific needs, budget, and growth plans when selecting a tool. Free trials help evaluate fit before commitment."
    })

    # Q4: Integration/connectivity
    faq_items.append({
        "question": f"Do {category} tools integrate with other business systems?",
        "answer": f"Yes, most {category} tools offer integration capabilities. {main_tool} connects with accounting software, CRM systems, and business platforms. {tool_list} support API connections, third-party integrations, and mobile apps. Integration enables seamless data flow between systems, reducing manual entry and improving workflow efficiency."
    })

    # Q5: Mobile access
    faq_items.append({
        "question": f"Can I access {category} tools on mobile devices?",
        "answer": f"Most {category} tools provide mobile apps or mobile-responsive web interfaces. {main_tool} offers a complete mobile app for field teams. {tool_list} enable on-the-go access to key features like monitoring, reporting, and management. Mobile capability is essential for businesses with field operations or remote teams."
    })

    # Q6: Automation benefits
    faq_items.append({
        "question": f"How does automation benefit {category} operations?",
        "answer": f"Automation in {category} tools reduces manual tasks, streamlines workflows, and improves efficiency. {main_tool} offers strong automation for routine processes. Features like automated reporting, alerts, and scheduling save hours of manual work. Automation also reduces errors and ensures consistent operations, helping businesses scale efficiently."
    })

    # Q7: Choosing the right tool
    faq_items.append({
        "question": f"What factors should I consider when choosing {category} software?",
        "answer": f"Key factors include: 1) Core features matching your needs, 2) Pricing within budget, 3) Ease of use and adoption, 4) Integration with existing systems, 5) Mobile capabilities for field teams, 6) Customer support quality, and 7) Scalability for growth. Compare {tool_list} to find the best fit for your business size and requirements."
    })

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["answer"]
                }
            }
            for item in faq_items
        ]
    }


def generate_howto_schema(title: str, tools: List[str], category: str) -> Dict[str, Any]:
    """Generate HowTo schema with 3-5 steps."""

    main_tool = tools[0] if tools else "the software"

    steps = []

    # Step 1: Research and evaluate
    steps.append({
        "name": "Research and Compare Tools",
        "text": f"Start by researching {category} tools like {', '.join(tools[:3]) if len(tools) >= 3 else main_tool}. Compare features, pricing, reviews, and integration capabilities. Identify which tools align with your business size and operational needs. Use free trials to test functionality before making decisions.",
        "image": "https://www.housecar.life/images/howto-research.png",
        "estimatedTime": "PT2H"
    })

    # Step 2: Plan implementation
    steps.append({
        "name": "Plan Your Implementation",
        "text": f"Create an implementation plan for {main_tool}. Define your goals, timeline, and team responsibilities. Prepare data migration requirements and identify integration needs. Set up user accounts and configure settings based on your workflow requirements.",
        "image": "https://www.housecar.life/images/howto-plan.png",
        "estimatedTime": "PT4H"
    })

    # Step 3: Set up and configure
    steps.append({
        "name": "Set Up and Configure the System",
        "text": f"Install and configure {main_tool} for your operations. Set up user permissions, customize dashboards, and configure automation rules. Connect integrations with existing systems. Import historical data and establish baseline settings for monitoring.",
        "image": "https://www.housecar.life/images/howto-setup.png",
        "estimatedTime": "PT6H"
    })

    # Step 4: Train your team
    steps.append({
        "name": "Train Your Team",
        "text": f"Train your team on {main_tool} features and workflows. Provide hands-on sessions for key functions. Create documentation for standard procedures. Establish support channels for questions. Ensure all users understand their roles and can use core features effectively.",
        "image": "https://www.housecar.life/images/howto-train.png",
        "estimatedTime": "PT8H"
    })

    # Step 5: Monitor and optimize
    steps.append({
        "name": "Monitor and Optimize Performance",
        "text": f"Regularly monitor {main_tool} performance and metrics. Review analytics to identify improvement areas. Optimize workflows based on data insights. Schedule regular maintenance and updates. Gather team feedback to refine processes and maximize tool effectiveness.",
        "image": "https://www.housecar.life/images/howto-monitor.png",
        "estimatedTime": "PT2H"
    })

    return {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": f"How to Implement {category} Tools: {title}",
        "description": f"Step-by-step guide to selecting, implementing, and optimizing {category} tools like {main_tool} for your business operations.",
        "totalTime": "PT22H",
        "estimatedCost": {
            "@type": "EstimatedCost",
            "currency": "USD",
            "value": "49-500"
        },
        "step": [
            {
                "@type": "HowToStep",
                "name": step["name"],
                "text": step["text"],
                "image": step.get("image"),
                "estimatedTime": step.get("estimatedTime")
            }
            for step in steps
        ]
    }


def process_file(file_path: Path) -> bool:
    """Process a single JSON file and add schemas."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if schemas already exist
        has_faq_schema = False
        has_howto_schema = False

        # Look for existing schemas
        if 'faq_schema' in data or 'faq_page_schema' in data:
            has_faq_schema = True
        if 'howto_schema' in data or 'how_to_schema' in data:
            has_howto_schema = True

        # Extract info from content
        content = data.get('content', '')
        title = data.get('title', '')
        tools = extract_tools_from_content(content)
        category = extract_category_from_content(content)

        # Generate and add FAQ schema if not present
        if not has_faq_schema:
            faq_schema = generate_faq_schema(title, tools, category)
            data['faq_page_schema'] = faq_schema
            stats['faq_added'] += 1

        # Generate and add HowTo schema if not present
        if not has_howto_schema:
            howto_schema = generate_howto_schema(title, tools, category)
            data['how_to_schema'] = howto_schema
            stats['howto_added'] += 1

        # Save the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        stats['processed'] += 1
        return True

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        stats['errors'] += 1
        return False


def main():
    """Main processing function."""
    print("=" * 60)
    print("Batch Schema Generator - Batch 8")
    print("=" * 60)
    print(f"Categories: {', '.join(CATEGORIES)}")
    print()

    for category in CATEGORIES:
        category_path = DATA_DIR / category

        if not category_path.exists():
            print(f"Warning: {category} directory not found, skipping...")
            continue

        json_files = list(category_path.glob("*.json"))
        stats['total_files'] += len(json_files)

        print(f"\nProcessing {category}: {len(json_files)} files")

        for file_path in json_files:
            process_file(file_path)
            if stats['processed'] % 50 == 0:
                print(f"  Progress: {stats['processed']} files processed")

    # Print final stats
    print("\n" + "=" * 60)
    print("FINAL STATISTICS")
    print("=" * 60)
    print(f"Total files found: {stats['total_files']}")
    print(f"Files processed: {stats['processed']}")
    print(f"FAQ schemas added: {stats['faq_added']}")
    print(f"HowTo schemas added: {stats['howto_added']}")
    print(f"Errors: {stats['errors']}")
    print("=" * 60)


if __name__ == "__main__":
    main()