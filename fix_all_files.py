#!/usr/bin/env python3
import json
import re
import os

# Domain-specific vocabulary for medical equipment rental
VOCAB = set([
    'tracking', 'safety', 'inspection', 'management', 'system', 'review', 'tool',
    'equipment', 'rental', 'compliance', 'certification', 'fda', 'ce', 'iso',
    'plan', 'disinfection', 'quality', 'device', 'medical', 'standard',
    'market', 'validity', 'period', 'expired', 'renewal', 'scope', 'cover',
    'model', 'functionality', 'use', 'update', 'reminder', 'expiration',
    'automatic', 'class', 'level', 'technology', 'documentation', 'storage',
    'public', 'report', 'structure', 'information', 'audit', 'design',
    'maintenance', 'process', 'project', 'list', 'electric', 'gas', 'machine',
    'instrument', 'radiation', 'result', 'record', 'rectification', 'completed',
    'recovery', 'prevent', 'infection', 'high', 'temperature', 'agent',
    'personnel', 'time', 'verification', 'effectiveness', 'prohibit',
    'mainstream', 'product', 'suite', 'professional', 'core', 'database',
    'cloud', 'deployment', 'generate', 'pricing', 'strategy', 'basic',
    'version', 'include', 'depth', 'manager', 'focuses', 'connect', 'api',
    'real', 'time', 'status', 'query', 'european', 'union', 'method',
    'platform', 'allocation', 'execution', 'task', 'mobile', 'terminal',
    'app', 'support', 'sterilize', 'log', 'prediction', 'demand', 'crm',
    'customer', 'service', 'satisfaction', 'analytics', 'data', 'bi',
    'visualization', 'delivery', 'digital', 'transformation', 'document',
    'energy', 'finance', 'financial', 'flow', 'roi', 'calculate', 'fleet',
    'globalization', 'hr', 'human', 'resource', 'innovation', 'churn', 'ai',
    'big', 'blockchain', 'cashflow', 'change', 'and', 'for', 'the', 'with'
])

def split_word_by_vocabulary(word):
    """Split a word using domain vocabulary"""
    word_lower = word.lower()
    result = []
    remaining = word_lower

    max_word_len = max(len(w) for w in VOCAB)

    while remaining:
        matched = False
        # Try longest matches first
        for length in range(min(max_word_len, len(remaining)), 2, -1):
            candidate = remaining[:length]
            if candidate in VOCAB:
                result.append(candidate)
                remaining = remaining[length:]
                matched = True
                break

        if not matched:
            # Take first 2 chars if no match
            result.append(remaining[:2])
            remaining = remaining[2:]

    return ' '.join(result)

def intelligent_word_splitting(text):
    """
    Intelligently split concatenated words using camelCase + vocabulary
    """
    # Step 1: CamelCase splitting
    result = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    result = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', result)

    # Step 2: Find remaining long lowercase words (>10 chars)
    long_lower_pattern = re.compile(r'[a-z]{10,}')

    for match in long_lower_pattern.finditer(result):
        word = match.group(0)
        # Split by vocabulary
        split_version = split_word_by_vocabulary(word)
        result = result.replace(word, split_version)

    return result

def fix_file(filepath):
    """Fix broken translations in a JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Fix all text fields
        for key in ['title', 'description', 'content']:
            if key in data:
                data[key] = intelligent_word_splitting(data[key])

        # Fix keywords
        if 'seo_keywords' in data:
            data['seo_keywords'] = [intelligent_word_splitting(kw) for kw in data['seo_keywords']]

        # Ensure language field
        if 'language' not in data:
            data['language'] = 'en-US'

        # Save
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# Files to fix (18 files)
files = [
    "medical-equipment-rental-compliance-management-system-review.json",
    "medical-equipment-rental-contract-management-system-review.json",
    "medical-equipment-rental-cost-management-system-review.json",
    "medical-equipment-rental-crm-system-review.json",
    "medical-equipment-rental-customer-satisfaction-system-review.json",
    "medical-equipment-rental-customer-service-management-system-review.json",
    "medical-equipment-rental-data-analytics-platform-review.json",
    "medical-equipment-rental-delivery-management-system-review.json",
    "medical-equipment-rental-demand-prediction-system-review.json",
    "medical-equipment-rental-digital-transformation-system-review.json",
    "medical-equipment-rental-document-management-system-review.json",
    "medical-equipment-rental-energy-management-system-review.json",
    "medical-equipment-rental-finance-management-system-review.json",
    "medical-equipment-rental-financial-management-system-review.json",
    "medical-equipment-rental-fleet-management-system-review.json",
    "medical-equipment-rental-globalization-management-system-review.json",
    "medical-equipment-rental-hr-management-system-review.json",
    "medical-equipment-rental-innovation-management-system-review.json",
]

base_path = "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/"

print("=" * 80)
print("FIXING BROKEN MACHINE TRANSLATIONS IN FILES 21-39")
print("=" * 80)

fixed = []
failed = []

for filename in files:
    filepath = os.path.join(base_path, filename)
    print(f"\nProcessing: {filename}")

    if fix_file(filepath):
        fixed.append(filename)
        print(f"  ✅ Fixed successfully")

        # Show sample
        with open(filepath, 'r') as f:
            data = json.load(f)
        print(f"  Title preview: {data['title'][:100]}...")
    else:
        failed.append(filename)
        print(f"  ❌ Failed to fix")

print("\n" + "=" * 80)
print("FINAL SUMMARY")
print("=" * 80)
print(f"Total files processed: {len(files)}")
print(f"Successfully fixed: {len(fixed)}")
print(f"Failed: {len(failed)}")

if failed:
    print("\nFailed files:")
    for f in failed:
        print(f"  - {f}")
else:
    print("\n✅ All files fixed successfully!")

# Verify by checking one fixed file
print("\n" + "=" * 80)
print("VERIFICATION - Checking first fixed file")
print("=" * 80)
test_file = os.path.join(base_path, fixed[0])
with open(test_file, 'r') as f:
    data = json.load(f)

print(f"\nFile: {fixed[0]}")
print(f"Title: {data['title']}")
print(f"Has language field: {'language' in data}")
print(f"Language value: {data.get('language', 'NOT SET')}")