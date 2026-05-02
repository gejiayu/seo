#!/usr/bin/env python3
"""
Process all JSON files to bilingual format using batch operations.
This script handles the translation work by processing files in batches.
"""

import json
import os
import re
from pathlib import Path

def detect_language(text):
    """Detect if text is primarily Chinese"""
    if not text:
        return 'unknown'
    chinese_chars = len(re.findall(r'[一-鿿]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    return 'zh' if chinese_chars > english_chars * 0.3 else 'en'

def convert_to_bilingual_zh(data):
    """Convert Chinese file to bilingual format - adds English translation placeholders"""
    bilingual = {}
    # Chinese fields
    bilingual['title_zh'] = data.get('title', '')
    bilingual['description_zh'] = data.get('description', '')
    bilingual['content_zh'] = data.get('content', '')
    bilingual['seo_keywords_zh'] = data.get('seo_keywords', [])
    # English fields - placeholder for translation
    bilingual['title_en'] = ''  # Needs translation
    bilingual['description_en'] = ''  # Needs translation
    bilingual['content_en'] = ''  # Needs translation
    bilingual['seo_keywords_en'] = []  # Needs translation
    # Keep other fields
    bilingual['slug'] = data.get('slug', '')
    bilingual['published_at'] = data.get('published_at', '')
    bilingual['author'] = data.get('author', '')
    if 'pros_and_cons' in data:
        bilingual['pros_and_cons'] = data['pros_and_cons']
    if 'faq' in data:
        bilingual['faq'] = data['faq']
    return bilingual

def convert_to_bilingual_en(data):
    """Convert English file to bilingual format - adds Chinese translation placeholders"""
    bilingual = {}
    # English fields
    bilingual['title_en'] = data.get('title', '')
    bilingual['description_en'] = data.get('description', '')
    bilingual['content_en'] = data.get('content', '')
    bilingual['seo_keywords_en'] = data.get('seo_keywords', [])
    # Chinese fields - placeholder for translation
    bilingual['title_zh'] = ''  # Needs translation
    bilingual['description_zh'] = ''  # Needs translation
    bilingual['content_zh'] = ''  # Needs translation
    bilingual['seo_keywords_zh'] = []  # Needs translation
    # Keep other fields
    bilingual['slug'] = data.get('slug', '')
    bilingual['published_at'] = data.get('published_at', '')
    bilingual['author'] = data.get('author', '')
    if 'pros_and_cons' in data:
        bilingual['pros_and_cons'] = data['pros_and_cons']
    if 'faq' in data:
        bilingual['faq'] = data['faq']
    return bilingual

def process_category(category, base_dir, count_callback=None):
    """Process all files in a category directory"""
    cat_dir = base_dir / category
    if not cat_dir.exists():
        return 0, 0

    processed = 0
    errors = 0

    for json_file in cat_dir.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Skip if already bilingual
            if 'title_zh' in data or 'title_en' in data:
                continue

            lang = detect_language(data.get('title', '') or data.get('content', ''))

            if lang == 'zh':
                bilingual = convert_to_bilingual_zh(data)
            elif lang == 'en':
                bilingual = convert_to_bilingual_en(data)
            else:
                continue

            # Write back (with placeholders - will need translation)
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(bilingual, f, ensure_ascii=False, indent=2)

            processed += 1
            if count_callback and processed % 20 == 0:
                count_callback(category, processed)

        except Exception as e:
            errors += 1
            print(f"Error processing {json_file}: {e}")

    return processed, errors

def main():
    categories = [
        "event-planning-tools",
        "finance-accounting-tools",
        "fishing-gear-rental-tools",
        "fitness-gym-management",
        "florist-flower-shop-tools",
        "food-beverage-distribution-tools",
        "franchise-business-tools",
        "furniture-home-rental-tools",
        "generator-power-rental-tools",
        "golf-equipment-rental-tools",
        "government-public-sector-tools",
        "healthcare-medical-tools"
    ]

    base_dir = Path("/Users/gejiayu/owner/seo/data")

    total_processed = 0
    total_errors = 0

    def report_progress(cat, count):
        print(f"Progress: {cat} - {count} files processed")

    for category in categories:
        print(f"\nProcessing category: {category}")
        processed, errors = process_category(category, base_dir, report_progress)
        total_processed += processed
        total_errors += errors
        print(f"  Category {category}: {processed} files processed, {errors} errors")

    print(f"\n\n=== FINAL SUMMARY ===")
    print(f"Total files processed: {total_processed}")
    print(f"Total errors: {total_errors}")
    print(f"\nNote: Files have been converted to bilingual format with placeholders.")
    print(f"English/Chinese translations need to be filled in separately.")

if __name__ == "__main__":
    main()