#!/usr/bin/env python3
"""
Comprehensive translation helper for insurance-agency-tools files
This script processes all JSON files and prepares translation templates
"""
import json
import os
import re

DATA_DIR = '/Users/gejiayu/owner/seo/data/insurance-agency-tools'
OUTPUT_DIR = '/Users/gejiayu/owner/seo/temp/translation_output'

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def has_chinese(text):
    """Check if text contains Chinese characters"""
    if not text:
        return False
    chinese_pattern = re.compile(r'[一-鿿]+')
    return bool(chinese_pattern.search(text))

def clean_keywords(keywords):
    """Clean keywords - remove extra spaces and translate Chinese"""
    if not isinstance(keywords, list):
        return keywords

    cleaned = []
    for kw in keywords:
        # Remove extra spaces
        kw_clean = ' '.join(kw.split())
        # Check if contains Chinese
        if has_chinese(kw_clean):
            # For Chinese keywords, we'll mark them for translation
            kw_clean = f"[NEEDS_TRANSLATION: {kw_clean}]"
        cleaned.append(kw_clean)
    return cleaned

def extract_chinese_content(data):
    """Extract Chinese content that needs translation"""
    fields_to_extract = {}

    for field in ['title', 'description', 'content', 'author']:
        if field in data and has_chinese(data[field]):
            fields_to_extract[field] = data[field]

    # Check seo_keywords for Chinese
    if 'seo_keywords' in data:
        for kw in data['seo_keywords']:
            if has_chinese(kw):
                if 'seo_keywords_chinese' not in fields_to_extract:
                    fields_to_extract['seo_keywords_chinese'] = []
                fields_to_extract['seo_keywords_chinese'].append(kw)

    return fields_to_extract

def process_all_files():
    """Process all files and create translation mapping"""
    translation_needed = []

    for filename in sorted(os.listdir(DATA_DIR)):
        if not filename.endswith('.json'):
            continue

        filepath = os.path.join(DATA_DIR, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            chinese_content = extract_chinese_content(data)

            if chinese_content:
                translation_needed.append({
                    'filename': filename,
                    'filepath': filepath,
                    'chinese_content': chinese_content,
                    'fields_count': len(chinese_content)
                })

        except Exception as e:
            print(f"Error reading {filename}: {e}")

    return translation_needed

def generate_translation_report(translation_needed):
    """Generate a report of all files needing translation"""
    report_file = os.path.join(OUTPUT_DIR, 'translation_report.txt')

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"TRANSLATION REPORT FOR insurance-agency-tools\n")
        f.write(f"Generated on: 2026-05-02\n")
        f.write(f"Total files needing translation: {len(translation_needed)}\n\n")

        for item in translation_needed:
            f.write(f"File: {item['filename']}\n")
            f.write(f"  Fields to translate: {list(item['chinese_content'].keys())}\n")

            if 'title' in item['chinese_content']:
                f.write(f"  Title: {item['chinese_content']['title'][:100]}...\n")

            if 'author' in item['chinese_content']:
                f.write(f"  Author: {item['chinese_content']['author']}\n")

            if 'seo_keywords_chinese' in item['chinese_content']:
                f.write(f"  Chinese keywords: {item['chinese_content']['seo_keywords_chinese']}\n")

            f.write("\n")

    print(f"Report saved to: {report_file}")

def main():
    translation_needed = process_all_files()
    print(f"\n{'='*80}")
    print(f"TRANSLATION ANALYSIS COMPLETE")
    print(f"{'='*80}")
    print(f"Total files needing translation: {len(translation_needed)}")
    print(f"\n")

    # Show first 10 files as preview
    print("First 10 files needing translation:")
    for i, item in enumerate(translation_needed[:10], 1):
        print(f"{i}. {item['filename']}")
        print(f"   Fields: {list(item['chinese_content'].keys())}")
        if 'author' in item['chinese_content']:
            print(f"   Author: {item['chinese_content']['author']}")

    # Generate full report
    generate_translation_report(translation_needed)

    # Save full data
    full_data_file = os.path.join(OUTPUT_DIR, 'translation_needed.json')
    with open(full_data_file, 'w', encoding='utf-8') as f:
        json.dump(translation_needed, f, ensure_ascii=False, indent=2)

    print(f"\nFull data saved to: {full_data_file}")

    # Count unique authors
    authors = set()
    for item in translation_needed:
        if 'author' in item['chinese_content']:
            authors.add(item['chinese_content']['author'])

    print(f"\nUnique authors needing translation: {len(authors)}")
    for author in authors:
        print(f"  - {author}")

if __name__ == '__main__':
    main()