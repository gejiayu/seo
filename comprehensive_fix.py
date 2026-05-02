#!/usr/bin/env python3
"""
Comprehensive fix script for broken machine translations.
Handles all edge cases and provides proper English spacing.
"""

import json
import re
from pathlib import Path

def comprehensive_fix(text):
    """
    Comprehensive fix for broken machine translations.
    Handles all edge cases including split words and awkward spacing.
    """

    # Fix split words (words broken by spaces)
    split_words_fixes = [
        ('pro ce ss', 'process'),
        ('suc ce ss', 'success'),
        ('Compar iso n', 'Comparison'),
        ('Predi ct ion', 'Prediction'),
        ('Fun ct ionality', 'Functionality'),
        ('m ai nstream', 'mainstream'),
        ('det ai led', 'detailed'),
        ('produ ct', 'product'),
        ('fun ct ionality', 'functionality'),
        ('compar iso ns', 'comparisons'),
    ]

    for broken, fixed in split_words_fixes:
        text = text.replace(broken, fixed)

    # Fix specific content issues we've seen
    content_fixes = [
        # Description fixes
        ('In-depth review of ICU critical care equipment rental management systems , covering',
         'In-depth review of ICU critical care equipment rental management systems, covering'),
        ('Provides det ai led produ ct compar iso n tables',
         'Provides detailed product comparison tables'),
        ('Learn more about fun ct ionality and pricing compar iso ns',
         'Learn more about functionality and pricing comparisons'),

        # Title colon spacing
        ('Review: ICU', 'Review: ICU'),

        # Content flow fixes
        ('ICU critical care equipment rental is a core step in critical care medicine . Monitoring instruments , ventilators , infusion pumps , defibrillators and other equipment have strong rental demand . ICU equipment management systems ensure critical care efficiency .',
         'ICU critical care equipment rental is essential in critical care medicine. Monitoring instruments, ventilators, infusion pumps, defibrillators, and other equipment have strong rental demand. ICU equipment management systems ensure critical care efficiency.'),
    ]

    for old, new in content_fixes:
        text = text.replace(old, new)

    # Fix punctuation spacing (remove extra spaces before punctuation)
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)

    # Fix punctuation spacing (ensure space after punctuation)
    text = re.sub(r'([.,!?;:])([A-Za-z])', r'\1 \2', text)

    # Fix comma lists (ensure consistent spacing)
    # Pattern: "word , word , word" -> "word, word, word"
    text = re.sub(r'(\w+)\s*,\s*(\w+)', r'\1, \2', text)

    # Remove extra spaces around punctuation
    text = re.sub(r'\s+,', ',', text)
    text = re.sub(r',\s+,', ', ', text)
    text = re.sub(r'\s+\.', '.', text)
    text = re.sub(r'\.\s+\.', '.', text)

    # Fix spacing around parentheses
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r'\s+\)', ')', text)

    # Fix spacing around dashes
    text = re.sub(r'\s*-\s*', '-', text)  # For hyphenated words

    # Ensure proper sentence structure (capitalize after period+space)
    text = re.sub(r'\.\s+([a-z])', lambda m: '. ' + m.group(1).upper(), text)

    # Fix HTML tag spacing
    # Don't add spaces inside HTML tags
    text = re.sub(r'<\s+', '<', text)
    text = re.sub(r'\s+>', '>', text)
    text = re.sub(r'<\s*([hH][1-6]|p|ul|ol|li|table|thead|tbody|tr|th|td|strong|em|a|div|span])', r'<\1', text)
    text = re.sub(r'([hH][1-6]|p|ul|ol|li|table|thead|tbody|tr|th|td|strong|em|a|div|span])\s*>', r'\1>', text)

    return text

def fix_all_fields(data):
    """Fix all text fields in a JSON data object."""

    if 'title' in data:
        data['title'] = comprehensive_fix(data['title'])

    if 'description' in data:
        data['description'] = comprehensive_fix(data['description'])

    if 'content' in data:
        data['content'] = comprehensive_fix(data['content'])

    if 'seo_keywords' in data and isinstance(data['seo_keywords'], list):
        data['seo_keywords'] = [comprehensive_fix(kw) for kw in data['seo_keywords']]

    # Ensure language field
    if 'language' not in data:
        data['language'] = 'en-US'

    return data

def process_file(filepath):
    """Process and fix a single file."""
    print(f"\n{'='*60}")
    print(f"Processing: {filepath.name}")
    print(f"{'='*60}")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Show before state (sample)
    print("\nBEFORE (Title):")
    print(f"  {data.get('title', 'N/A')[:100]}")

    print("\nBEFORE (Description):")
    print(f"  {data.get('description', 'N/A')[:150]}")

    # Fix the data
    data = fix_all_fields(data)

    # Show after state (sample)
    print("\nAFTER (Title):")
    print(f"  {data.get('title', 'N/A')[:100]}")

    print("\nAFTER (Description):")
    print(f"  {data.get('description', 'N/A')[:150]}")

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Successfully fixed: {filepath.name}")

def main():
    base_dir = Path('/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools')

    files_to_fix = [
        'icu-critical-care-equipment-rental-management-system-review.json',
        'infusion-pump-equipment-rental-management-system-review.json',
        'medical-device-rental-erp-selection-guide.json',
        'medical-equipment-depreciation-management-system-review.json',
        'medical-equipment-rental-churn-prediction-system-review.json'
    ]

    print("\n" + "="*80)
    print("COMPREHENSIVE FIX FOR BROKEN MACHINE TRANSLATIONS")
    print("="*80)

    success_count = 0
    for filename in files_to_fix:
        filepath = base_dir / filename
        if filepath.exists():
            process_file(filepath)
            success_count += 1
        else:
            print(f"\n❌ File not found: {filepath}")

    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    print(f"✓ Successfully fixed: {success_count}/{len(files_to_fix)} files")
    print("="*80)

if __name__ == '__main__':
    main()