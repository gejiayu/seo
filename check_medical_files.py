#!/usr/bin/env python3
"""
Script to identify Chinese files and broken machine translations in medical-equipment-rental-tools.
"""

import json
import os
import re
from pathlib import Path

def contains_chinese(text):
    """Check if text contains Chinese characters."""
    chinese_pattern = re.compile(r'[一-鿿]+')
    return bool(chinese_pattern.search(text))

def has_broken_translation(text):
    """Check for concatenated words without spaces (broken machine translations)."""
    # Pattern to find concatenated lowercase words (e.g., "diagnosticequipmentrentalmanagementsystemreview")
    broken_pattern = re.compile(r'[a-z]{40,}')
    return bool(broken_pattern.search(text))

def check_file(filepath):
    """Check a JSON file for Chinese content and broken translations."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check all text fields
        text_fields = ['title', 'description', 'content', 'author']
        has_chinese = False
        has_broken = False
        issues = []

        for field in text_fields:
            if field in data:
                text = str(data[field])
                if contains_chinese(text):
                    has_chinese = True
                    issues.append(f"Chinese content in '{field}'")
                if has_broken_translation(text):
                    has_broken = True
                    issues.append(f"Broken translation in '{field}'")

        # Check if language field exists
        has_language = 'language' in data

        return {
            'filepath': filepath,
            'has_chinese': has_chinese,
            'has_broken': has_broken,
            'has_language_field': has_language,
            'issues': issues
        }
    except Exception as e:
        return {
            'filepath': filepath,
            'error': str(e)
        }

def main():
    directory = '/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/'

    # Get all JSON files
    json_files = sorted([f for f in os.listdir(directory) if f.endswith('.json')])

    # Process files 1-20
    target_files = json_files[:20]

    print(f"Found {len(json_files)} JSON files in directory")
    print(f"Processing files 1-20: {target_files}\n")

    results = []
    for filename in target_files:
        filepath = os.path.join(directory, filename)
        result = check_file(filepath)
        results.append(result)

        if 'error' in result:
            print(f"❌ {filename}: ERROR - {result['error']}")
        elif result['has_chinese'] or result['has_broken']:
            print(f"⚠️  {filename}: NEEDS FIXING")
            for issue in result['issues']:
                print(f"   - {issue}")
            if not result['has_language_field']:
                print(f"   - Missing 'language' field")
        else:
            print(f"✓ {filename}: OK (has language field: {result['has_language_field']})")

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    files_to_fix = [r for r in results if ('has_chinese' in r and r['has_chinese']) or ('has_broken' in r and r['has_broken'])]
    files_with_issues = [r for r in results if 'error' in r or ('has_chinese' in r and (r['has_chinese'] or r['has_broken']))]

    print(f"Total files processed: {len(results)}")
    print(f"Files needing fixes: {len(files_to_fix)}")

    if files_to_fix:
        print("\nFiles to fix:")
        for r in files_to_fix:
            print(f"  - {os.path.basename(r['filepath'])}")
            for issue in r['issues']:
                print(f"    {issue}")

if __name__ == '__main__':
    main()