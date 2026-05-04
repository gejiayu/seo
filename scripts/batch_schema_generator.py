#!/usr/bin/env python3
"""
Batch Schema Generator for SEO JSON files
Processes files to add FAQ and HowTo schema
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any
import html


def clean_html(html_content: str) -> str:
    """Remove HTML tags and decode entities"""
    text = re.sub(r'<[^>]+>', ' ', html_content)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_sections(content: str) -> Dict[str, str]:
    """Extract sections by h2/h3 headers"""
    sections = {}
    h2_pattern = r'<h2>(.*?)</h2>(.*?)((?:<h2>|$))'
    h3_pattern = r'<h3>(.*?)</h3>(.*?)((?:<h3>|<h2>|$))'

    # Extract h2 sections
    for match in re.finditer(h2_pattern, content, re.DOTALL):
        title = clean_html(match.group(1))
        body = clean_html(match.group(2))
        if title and body:
            sections[title] = body

    # Extract h3 sections
    for match in re.finditer(h3_pattern, content, re.DOTALL):
        title = clean_html(match.group(1))
        body = clean_html(match.group(2))
        if title and body:
            sections[title] = body

    return sections


def generate_faq_from_content(content: str, title: str, keywords: List[str]) -> Dict:
    """Generate FAQ schema from content"""
    sections = extract_sections(content)
    faqs = []

    # Priority topics based on sections
    priority_sections = [
        'Introduction', 'Overview', 'Core', 'Main', 'Key', 'Features',
        'Benefits', 'Advantages', 'Comparison', 'How to', 'Guide',
        'Recommendation', 'Selection', 'Pricing', 'Cost'
    ]

    # Extract FAQ from content sections
    used_sections = []

    # 1. Main purpose question (from first h1 or intro)
    h1_match = re.search(r'<h1>(.*?)</h1>', content)
    if h1_match:
        main_topic = clean_html(h1_match.group(1))
        intro_text = clean_html(content.split('</h1>')[1].split('<h2>')[0] if '</h1>' in content else content[:500])
        if main_topic and len(intro_text) > 50:
            faqs.append({
                "@type": "Question",
                "name": f"What is {main_topic.split(':')[0] if ':' in main_topic else main_topic}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": intro_text[:400] + "..." if len(intro_text) > 400 else intro_text
                }
            })

    # 2. Key features/benefits questions
    for sec_title, sec_content in sections.items():
        if any(p.lower() in sec_title.lower() for p in ['feature', 'benefit', 'advantage', 'capability', 'function']):
            if len(sec_content) > 50 and sec_title not in used_sections:
                question = f"What are the {sec_title.lower()}?"
                faqs.append({
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": sec_content[:350] + "..." if len(sec_content) > 350 else sec_content
                    }
                })
                used_sections.append(sec_title)
                if len(faqs) >= 7:
                    break

    # 3. Comparison questions
    for sec_title, sec_content in sections.items():
        if 'comparison' in sec_title.lower() or 'difference' in sec_title.lower():
            if len(sec_content) > 50 and sec_title not in used_sections:
                question = f"How do these tools compare?"
                faqs.append({
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": sec_content[:350] + "..." if len(sec_content) > 350 else sec_content
                    }
                })
                used_sections.append(sec_title)
                if len(faqs) >= 7:
                    break

    # 4. Recommendation/Selection questions
    for sec_title, sec_content in sections.items():
        if any(r in sec_title.lower() for r in ['recommend', 'selection', 'choose', 'best']):
            if len(sec_content) > 50 and sec_title not in used_sections:
                question = f"Which tool should I choose?"
                faqs.append({
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": sec_content[:350] + "..." if len(sec_content) > 350 else sec_content
                    }
                })
                used_sections.append(sec_title)
                if len(faqs) >= 7:
                    break

    # 5. Trend/Future questions
    for sec_title, sec_content in sections.items():
        if 'trend' in sec_title.lower() or 'future' in sec_title.lower() or '2026' in sec_title or '2027' in sec_title:
            if len(sec_content) > 50 and sec_title not in used_sections:
                question = f"What are the latest trends and developments?"
                faqs.append({
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": sec_content[:350] + "..." if len(sec_content) > 350 else sec_content
                    }
                })
                used_sections.append(sec_title)
                if len(faqs) >= 7:
                    break

    # 6. Use case/scenario questions
    for sec_title, sec_content in sections.items():
        if 'scenario' in sec_title.lower() or 'application' in sec_title.lower() or 'use' in sec_title.lower():
            if len(sec_content) > 50 and sec_title not in used_sections:
                question = f"What are common use cases and scenarios?"
                faqs.append({
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": sec_content[:350] + "..." if len(sec_content) > 350 else sec_content
                    }
                })
                used_sections.append(sec_title)
                if len(faqs) >= 7:
                    break

    # 7. Pricing/Cost questions
    for sec_title, sec_content in sections.items():
        if 'price' in sec_title.lower() or 'cost' in sec_title.lower() or 'pricing' in sec_title.lower():
            if len(sec_content) > 50 and sec_title not in used_sections:
                question = f"What are the pricing models and costs?"
                faqs.append({
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": sec_content[:350] + "..." if len(sec_content) > 350 else sec_content
                    }
                })
                used_sections.append(sec_title)
                if len(faqs) >= 7:
                    break

    # Fill remaining FAQs from other sections if needed
    if len(faqs) < 5:
        for sec_title, sec_content in sections.items():
            if sec_title not in used_sections and len(sec_content) > 50:
                faqs.append({
                    "@type": "Question",
                    "name": f"What about {sec_title}?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": sec_content[:350] + "..." if len(sec_content) > 350 else sec_content
                    }
                })
                used_sections.append(sec_title)
                if len(faqs) >= 7:
                    break

    # If still not enough, generate generic FAQs based on title/keywords
    if len(faqs) < 5:
        clean_title = title.split(':')[0] if ':' in title else title
        clean_title = clean_title.replace('Top 10', '').replace('2026', '').strip()

        generic_faqs = [
            {
                "@type": "Question",
                "name": f"What are {clean_title} tools?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"{clean_title} tools are specialized software solutions designed to help businesses and organizations manage their operations efficiently. These tools provide features like automation, analytics, and integration capabilities."
                }
            },
            {
                "@type": "Question",
                "name": f"Why use {clean_title} tools?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Using {clean_title} tools improves efficiency, reduces manual errors, saves time, and enables better decision-making through data analytics. They help organizations streamline workflows and optimize resource allocation."
                }
            },
            {
                "@type": "Question",
                "name": f"How to choose the best {clean_title} tool?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Consider factors like features, pricing, scalability, user reviews, integration capabilities, and support quality. Evaluate your specific needs and compare multiple options before making a decision."
                }
            },
            {
                "@type": "Question",
                "name": f"What features should {clean_title} tools have?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Key features include automation capabilities, reporting and analytics, integration with existing systems, user-friendly interface, scalability, security measures, and reliable customer support."
                }
            },
            {
                "@type": "Question",
                "name": f"What is the cost of {clean_title} tools?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Costs vary based on features, scale, and vendors. Options range from free basic versions to premium enterprise solutions. Consider total cost including implementation, training, and maintenance."
                }
            },
            {
                "@type": "Question",
                "name": f"Are {clean_title} tools worth the investment?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Yes, {clean_title} tools typically provide significant ROI through time savings, error reduction, improved efficiency, and better decision-making. The investment pays off through operational improvements and cost savings."
                }
            },
            {
                "@type": "Question",
                "name": f"How to implement {clean_title} tools effectively?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Start with clear objectives, involve stakeholders early, provide adequate training, integrate with existing systems, monitor performance metrics, and continuously optimize based on feedback and results."
                }
            }
        ]

        while len(faqs) < 5:
            faqs.append(generic_faqs[len(faqs)])

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faqs[:7]  # Ensure max 7 FAQs
    }


def generate_howto_from_title(title: str, keywords: List[str]) -> Dict:
    """Generate HowTo schema from title"""
    # Parse title to extract tool/service name
    clean_title = title.split(':')[0] if ':' in title else title
    clean_title = clean_title.replace('Top 10', '').replace('2026', '').replace('Guide', '').replace('Comparison', '').strip()

    # Determine action verb based on keywords
    action = 'use'
    if any(k in keywords for k in ['platform', 'software', 'tool', 'system']):
        action = 'implement'
    elif any(k in keywords for k in ['choose', 'select', 'comparison']):
        action = 'choose'
    elif any(k in keywords for k in ['manage', 'management']):
        action = 'use for management'

    # Generate steps
    steps = [
        {
            "@type": "HowToStep",
            "position": 1,
            "name": "Identify Your Requirements",
            "text": f"Assess your specific needs for {clean_title}. Determine key features, budget constraints, integration requirements, and scalability needs. Document your requirements to guide the selection process."
        },
        {
            "@type": "HowToStep",
            "position": 2,
            "name": "Research Available Options",
            "text": f"Research and compare different {clean_title} solutions. Review features, pricing, user reviews, and vendor reputation. Create a shortlist of 3-5 potential solutions that meet your requirements."
        },
        {
            "@type": "HowToStep",
            "position": 3,
            "name": "Evaluate Key Features",
            "text": f"Evaluate each shortlisted {clean_title} solution against your requirements. Test key features through demos or trials. Assess ease of use, integration capabilities, and support quality."
        },
        {
            "@type": "HowToStep",
            "position": 4,
            "name": "Make Your Selection",
            "text": f"Select the {clean_title} solution that best fits your needs. Consider total cost, implementation timeline, training requirements, and long-term scalability. Negotiate terms and finalize the contract."
        },
        {
            "@type": "HowToStep",
            "position": 5,
            "name": "Implement and Optimize",
            "text": f"Implement your chosen {clean_title} solution. Set up integrations, train users, and establish workflows. Monitor performance metrics and continuously optimize based on feedback and results."
        }
    ]

    return {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": f"How to {action} {clean_title}",
        "step": steps
    }


def process_file(file_path: Path) -> bool:
    """Process a single JSON file and add schemas"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Skip if schemas already exist
        if 'faq_schema' in data and 'howto_schema' in data:
            return False

        # Generate schemas
        content = data.get('content', '')
        title = data.get('title', '')
        keywords = data.get('seo_keywords', [])

        data['faq_schema'] = generate_faq_from_content(content, title, keywords)
        data['howto_schema'] = generate_howto_from_title(title, keywords)

        # Save back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Process all files in batch 13 categories"""
    categories = [
        'car-vehicle-rental-tools',
        'paintball-laser-tag-rental-tools',
        'cleaning-maintenance-rental-tools'
    ]

    base_dir = Path('/Users/gejiayu/owner/seo/data')

    total_files = 0
    processed_files = 0
    skipped_files = 0
    error_files = 0
    faq_generated = 0
    howto_generated = 0

    for category in categories:
        cat_dir = base_dir / category
        if not cat_dir.exists():
            print(f"Directory not found: {cat_dir}")
            continue

        json_files = list(cat_dir.glob('*.json'))
        total_files += len(json_files)

        print(f"\nProcessing {category}: {len(json_files)} files")

        for file_path in json_files:
            result = process_file(file_path)
            if result:
                processed_files += 1
                faq_generated += 1
                howto_generated += 1
            else:
                skipped_files += 1

    print(f"\n{'='*60}")
    print(f"BATCH PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"Total files found: {total_files}")
    print(f"Files processed: {processed_files}")
    print(f"Files skipped (already had schemas): {skipped_files}")
    print(f"FAQ schemas generated: {faq_generated}")
    print(f"HowTo schemas generated: {howto_generated}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()