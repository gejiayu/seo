#!/usr/bin/env python3
import json
import os

# Files to fix with proper English translations
files_to_fix = [
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

directory = '/Users/gejiayu/owner/seo/data/massage-spa-wellness-tools/'

print("=" * 80)
print("FILES WITH BROKEN ENGLISH - NEED PROPER FIXING")
print("=" * 80)

for filename in files_to_fix[:3]:  # Show first 3 as examples
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"\n{filename}")
    print(f"Title (first 80 chars): {data.get('title', '')[:80]}")
    print(f"Description (first 100 chars): {data.get('description', '')[:100]}")
    print(f"\nContent snippet (first 200 chars):")
    print(data.get('content', '')[:200])

print("\n" + "=" * 80)
print("NOTE: All files have broken English with missing spaces and unnatural grammar")
print("I will now proceed to fix them with proper semantic translations")
print("=" * 80)