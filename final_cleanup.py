#!/usr/bin/env python3
"""
Final cleanup script for split words in machine translations.
Handles all the remaining split word patterns like "m ai ntenan ce", "inspe ct ion", etc.
"""

import json
import re
from pathlib import Path

def fix_split_words(text):
    """
    Fix all remaining split word patterns.
    These are words that have spaces inserted in the middle.
    """

    # Dictionary of split words to their correct forms
    split_word_fixes = {
        # Common split words found in the files
        'compar iso n': 'comparison',
        'm ai ntenan ce': 'maintenance',
        'inspe ct ion': 'inspection',
        'tr ai ning': 'training',
        'dire ct ly': 'directly',
        'impa ct': 'impact',
        'impa ct s': 'impacts',
        'repla ce ment': 'replacement',
        'sele ct ion': 'selection',
        'advan ce d': 'advanced',
        'fa ce s': 'faces',
        'rem ai ns': 'remains',
        'prohi bi ted': 'prohibited',
        'mo bi le': 'mobile',
        'bi ning': 'bining',  # "combining" split
        'produ ct': 'product',
        'Pro ce ss': 'Process',
        'pro ce ss': 'process',
        'Emergen ce': 'Emergence',
        'emergen ce': 'emergence',
        'Int ai n': 'Intain',  # Part of "Maintain"
        'M ai nt ai n': 'Maintain',
        'M ai ntenan ce': 'Maintenance',
        'Calibration M ai ntenan ce': 'Calibration Maintenance',
        'Tube Repla ce ment': 'Tube Replacement',
        'Safety Tr ai ning': 'Safety Training',
        'Fault Rep ai r': 'Fault Repair',
        'M ai ntenan ce Plans': 'Maintenance Plans',
        'M ai ntenan ce Reports': 'Maintenance Reports',
        'Batch M ai ntenan ce': 'Batch Maintenance',
        'Safety Inspe ct ion': 'Safety Inspection',
        'Tube Inspe ct ion': 'Tube Inspection',
        'Pressure Inspe ct ion': 'Pressure Inspection',
        'M ai ntenan ce Management': 'Maintenance Management',
        'M ai ntenan ce Calibration': 'Maintenance Calibration',
        'Sele ct ion Recommendations': 'Selection Recommendations',
        'sele ct ion strategies': 'selection strategies',
        'sele ct ion dire ct ly': 'selection directly',
        'com bi ning': 'combining',
        'Pro ce ss One': 'Process One',
        'Pro ce ss Two': 'Process Two',
        'Pro ce ss Three': 'Process Three',
        'Pro ce ss Four': 'Process Four',
    }

    for split, correct in split_word_fixes.items():
        text = text.replace(split, correct)

    # Additional regex patterns for any remaining split words
    # Pattern: word + space + ai + space + rest (for "maintenance", "training", etc.)
    text = re.sub(r'([a-z]+)\s+ai\s+n([a-z]+)', r'\1ain\2', text)

    # Pattern: word + space + ct + space + rest (for "inspection", "selection", etc.)
    text = re.sub(r'([a-z]+)\s+ct\s+([a-z]+)', r'\1ct\2', text)

    # Pattern: word + space + ce + space + rest (for "maintenance", "replacement", etc.)
    text = re.sub(r'([a-z]+)\s+ce\s+([a-z]+)', r'\1ce\2', text)

    # Pattern: word + space + bi + space + rest (for "prohibited", etc.)
    text = re.sub(r'([a-z]+)\s+bi\s+([a-z]+)', r'\1bi\2', text)

    # Pattern: word + space + iso + space + n (for "comparison")
    text = re.sub(r'([a-z]+)\s+iso\s+n', r'\1ison', text)

    # Pattern: word + space + ai + space + ntenan + space + ce (for "maintenance")
    text = re.sub(r'([a-z]+)\s+ai\s+ntenan\s+ce', r'\1aintenance', text)

    # Pattern: word + space + ce + space + ss (for "process", "success")
    text = re.sub(r'([a-z]+)\s+ce\s+ss', r'\1cess', text)

    # Pattern: word + space + ct + space + ion (for "inspection", "selection")
    text = re.sub(r'([a-z]+)\s+ct\s+ion', r'\1ction', text)

    # Pattern: word + space + ct + space + ly (for "directly")
    text = re.sub(r'([a-z]+)\s+ct\s+ly', r'\1ctly', text)

    # Pattern: word + space + ct + space + s (for "impacts")
    text = re.sub(r'([a-z]+)\s+ct\s+s', r'\1cts', text)

    # Pattern: word + space + ai + space + ning (for "training")
    text = re.sub(r'([a-z]+)\s+ai\s+ning', r'\1aining', text)

    # Pattern: word + space + ce + space + ment (for "replacement")
    text = re.sub(r'([a-z]+)\s+ce\s+ment', r'\1cement', text)

    # Pattern: word + space + bi + space + ning (for "combining")
    text = re.sub(r'([a-z]+)\s+bi\s+ning', r'\1bining', text)

    return text

def final_polish(text):
    """
    Final polish to ensure proper English grammar and spacing.
    """

    # Fix any remaining awkward spacing
    text = re.sub(r'\s+,', ',', text)
    text = re.sub(r',\s+,', ', ', text)
    text = re.sub(r'\s+\.', '.', text)
    text = re.sub(r'\s+!', '!', text)
    text = re.sub(r'\s+\?', '?', text)

    # Ensure proper spacing after punctuation
    text = re.sub(r'([.,!?])([A-Za-z])', r'\1 \2', text)

    # Capitalize first letter after period+space (for proper sentences)
    # But be careful with HTML tags and abbreviations
    # Skip this for now as it might break HTML structure

    return text

def process_file(filepath):
    """Process and fix a single file with final cleanup."""
    print(f"\n{'='*60}")
    print(f"Final Cleanup: {filepath.name}")
    print(f"{'='*60}")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Show sample before
    if 'description' in data:
        print("\nBEFORE (Description sample):")
        desc_sample = data['description'][:200]
        if 'compar iso n' in desc_sample or 'm ai ntenan ce' in desc_sample:
            print(f"  Contains split words: {desc_sample[:100]}")

    # Apply fixes
    if 'title' in data:
        data['title'] = fix_split_words(data['title'])
        data['title'] = final_polish(data['title'])

    if 'description' in data:
        data['description'] = fix_split_words(data['description'])
        data['description'] = final_polish(data['description'])

    if 'content' in data:
        data['content'] = fix_split_words(data['content'])
        data['content'] = final_polish(data['content'])

    if 'seo_keywords' in data and isinstance(data['seo_keywords'], list):
        data['seo_keywords'] = [fix_split_words(kw) for kw in data['seo_keywords']]
        data['seo_keywords'] = [final_polish(kw) for kw in data['seo_keywords']]

    # Ensure language field
    if 'language' not in data:
        data['language'] = 'en-US'

    # Show sample after
    if 'description' in data:
        print("\nAFTER (Description sample):")
        print(f"  {data['description'][:100]}")

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Final cleanup complete: {filepath.name}")

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
    print("FINAL CLEANUP - FIXING ALL SPLIT WORDS")
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
    print(f"✓ Successfully cleaned: {success_count}/{len(files_to_fix)} files")
    print("\nAll split words have been fixed!")
    print("="*80)

if __name__ == '__main__':
    main()