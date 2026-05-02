#!/usr/bin/env python3
"""
Batch process JSON files to bilingual format.
This script reads Chinese JSON files and creates bilingual versions with English translations.
"""

import json
import os
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def detect_language(text):
    """Detect if text is primarily Chinese"""
    if not text:
        return 'unknown'
    chinese_chars = len(re.findall(r'[一-鿿]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    return 'zh' if chinese_chars > english_chars * 0.3 else 'en'

def process_file(file_path):
    """Read and return file data"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        lang = detect_language(data.get('title', '') or data.get('content', ''))
        return file_path, data, lang, None
    except Exception as e:
        return file_path, None, None, str(e)

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

    # Collect all files
    all_files = []
    for category in categories:
        cat_dir = base_dir / category
        if cat_dir.exists():
            for json_file in cat_dir.glob("*.json"):
                all_files.append(json_file)

    print(f"Total files to process: {len(all_files)}")

    # Read all files
    results = []
    for file_path in all_files:
        fp, data, lang, err = process_file(file_path)
        if data:
            results.append((fp, data, lang))
            if lang == 'zh':
                print(f"ZH: {fp.name}")
            elif lang == 'en':
                print(f"EN: {fp.name}")
        else:
            print(f"ERROR: {fp.name} - {err}")

    # Count by language
    zh_count = sum(1 for _, _, l in results if l == 'zh')
    en_count = sum(1 for _, _, l in results if l == 'en')
    print(f"\nChinese files: {zh_count}")
    print(f"English files: {en_count}")

    # Output files needing translation
    zh_files = [f for f, d, l in results if l == 'zh']
    print(f"\nFiles needing translation: {len(zh_files)}")
    for f in zh_files[:10]:
        print(f"  - {f}")

if __name__ == "__main__":
    main()