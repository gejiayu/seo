#!/usr/bin/env python3
import json
import os
import re

def contains_chinese(text):
    """Check if text contains Chinese characters"""
    if not isinstance(text, str):
        return False
    chinese_pattern = re.compile(r'[一-鿿]')
    return bool(chinese_pattern.search(text))

# Files 31-40 with Chinese content
chinese_files = [
    'massage-technician-performance-system-2026.json',
    'massage-technician-promotion-system-2026.json',
    'massage-technician-resignation-management-system-2026.json',
    'massage-technician-service-standardization-system-2026.json',
    'massage-technician-skill-management-system-2026.json',
    'spa-add-on-service-system-2026.json',
    'spa-attendance-management-system-2026.json',
    'spa-booking-channel-management-system-2026.json',
    'spa-booking-demand-prediction-system-2026.json',
    'spa-booking-system-guide-2026.json'
]

# Files with missing language field
missing_language_files = [
    'massage-spa-finance-management-software-2026.json',
    'massage-technician-career-development-system-2026.json'
]

directory = '/Users/gejiayu/owner/seo/data/massage-spa-wellness-tools/'

print("=" * 80)
print("FILES TO TRANSLATE (Files 31-40)")
print("=" * 80)

for filename in chinese_files:
    filepath = os.path.join(directory, filename)
    print(f"\n{filename}")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"  Title: {data.get('title', 'N/A')[:60]}...")
    print(f"  Has Chinese title: {contains_chinese(data.get('title', ''))}")
    print(f"  Has Chinese description: {contains_chinese(data.get('description', ''))}")
    print(f"  Has Chinese content: {contains_chinese(data.get('content', ''))}")

print("\n" + "=" * 80)
print("FILES MISSING LANGUAGE FIELD")
print("=" * 80)

for filename in missing_language_files:
    filepath = os.path.join(directory, filename)
    print(f"\n{filename}")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"  Current language: {data.get('language', 'MISSING')}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"  Chinese files to translate: {len(chinese_files)}")
print(f"  Files needing language field: {len(missing_language_files)}")
print("\nNext: I will read and translate each file directly using my semantic translation capabilities.")