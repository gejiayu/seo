#!/usr/bin/env python3
import json
import re
import os

# Files to check (21-39)
files_to_check = [
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-compliance-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-contract-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-cost-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-crm-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-customer-satisfaction-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-customer-service-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-customer-service-management-system-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-data-analytics-platform-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-delivery-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-demand-prediction-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-digital-transformation-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-document-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-energy-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-finance-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-financial-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-fleet-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-globalization-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-hr-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-innovation-management-system-review.json",
]

def contains_chinese(text):
    """Check if text contains Chinese characters"""
    chinese_pattern = re.compile(r'[一-鿿]+')
    return bool(chinese_pattern.search(text))

def has_broken_machine_translation(text):
    """Check for broken machine translations like concatenated words without spaces"""
    # Pattern for words like "diagnosticequipmentrentalmanagementsystemreview"
    # Look for sequences of lowercase letters > 20 chars without spaces
    broken_pattern = re.compile(r'[a-z]{20,}')
    matches = broken_pattern.findall(text.lower())
    return len(matches) > 0

def analyze_file(filepath):
    """Analyze a JSON file for issues"""
    issues = {
        'has_chinese': False,
        'has_broken_translation': False,
        'missing_language_field': False,
        'chinese_fields': [],
        'broken_text_examples': []
    }

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if language field exists
        if 'language' not in data:
            issues['missing_language_field'] = True

        # Check all string fields for Chinese and broken translations
        for key, value in data.items():
            if isinstance(value, str):
                if contains_chinese(value):
                    issues['has_chinese'] = True
                    issues['chinese_fields'].append(key)

                if has_broken_machine_translation(value):
                    issues['has_broken_translation'] = True
                    # Extract examples
                    matches = re.findall(r'[a-z]{20,}', value.lower())
                    for match in matches[:3]:  # Limit to 3 examples
                        issues['broken_text_examples'].append(match)

            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        if contains_chinese(item):
                            issues['has_chinese'] = True
                            if key not in issues['chinese_fields']:
                                issues['chinese_fields'].append(key)

        return issues

    except Exception as e:
        return {'error': str(e)}

# Analyze all files
results = {}
for filepath in files_to_check:
    filename = os.path.basename(filepath)
    issues = analyze_file(filepath)
    results[filename] = issues

# Report findings
print("=" * 80)
print("FILES ANALYSIS REPORT (Files 21-39)")
print("=" * 80)

files_with_chinese = []
files_with_broken_trans = []
files_needing_language_field = []

for filename, issues in results.items():
    if 'error' in issues:
        print(f"\n❌ ERROR: {filename}")
        print(f"   {issues['error']}")
        continue

    if issues['has_chinese']:
        files_with_chinese.append(filename)
        print(f"\n🇨🇳 CHINESE FOUND: {filename}")
        print(f"   Fields with Chinese: {', '.join(issues['chinese_fields'])}")

    if issues['has_broken_translation']:
        files_with_broken_trans.append(filename)
        print(f"\n⚠️  BROKEN TRANSLATION: {filename}")
        print(f"   Examples: {', '.join(issues['broken_text_examples'][:2])}")

    if issues['missing_language_field']:
        files_needing_language_field.append(filename)

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Files with Chinese content: {len(files_with_chinese)}")
print(f"Files with broken translations: {len(files_with_broken_trans)}")
print(f"Files needing language field: {len(files_needing_language_field)}")

if files_with_chinese:
    print("\nFiles needing Chinese → English translation:")
    for f in files_with_chinese:
        print(f"  - {f}")

if files_with_broken_trans:
    print("\nFiles needing broken translation fix:")
    for f in files_with_broken_trans:
        print(f"  - {f}")

if files_needing_language_field:
    print("\nFiles needing 'language: en-US' field:")
    for f in files_needing_language_field:
        print(f"  - {f}")