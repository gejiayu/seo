#!/usr/bin/env python3
import json
import re
import os

# Extended vocabulary with medical equipment rental domain terms
VOCAB = {
    # Core terms
    'medical', 'equipment', 'rental', 'compliance', 'management', 'system', 'review', 'tool',
    'certification', 'tracking', 'safety', 'inspection', 'fda', 'ce', 'iso', 'plan',
    'disinfection', 'quality', 'device', 'standard', 'market', 'validity', 'period',
    'expired', 'renewal', 'scope', 'cover', 'model', 'functionality', 'use', 'update',
    'reminder', 'expiration', 'automatic', 'class', 'level', 'technology', 'documentation',
    'storage', 'public', 'report', 'structure', 'information', 'audit', 'design',
    'maintenance', 'process', 'project', 'list', 'electric', 'gas', 'machine', 'instrument',
    'radiation', 'result', 'record', 'rectification', 'completed', 'recovery', 'prevent',
    'infection', 'high', 'temperature', 'agent', 'personnel', 'time', 'verification',
    'effectiveness', 'prohibit', 'mainstream', 'product', 'suite', 'professional',
    'core', 'database', 'cloud', 'deployment', 'generate', 'pricing', 'strategy',
    'basic', 'version', 'include', 'depth', 'manager', 'focuses', 'connect', 'api',
    'real', 'status', 'query', 'european', 'union', 'method', 'platform', 'allocation',
    'execution', 'task', 'mobile', 'terminal', 'app', 'support', 'sterilize', 'log',
    'prediction', 'demand', 'crm', 'customer', 'service', 'satisfaction', 'analytics',
    'data', 'bi', 'visualization', 'delivery', 'digital', 'transformation', 'document',
    'energy', 'finance', 'financial', 'flow', 'roi', 'calculate', 'fleet', 'globalization',
    'hr', 'human', 'resource', 'innovation', 'churn', 'ai', 'big', 'blockchain',
    'cashflow', 'change', 'and', 'for', 'the', 'with', 'analysis', 'related', 'domain',
    'solution', 'marketing', 'automation', 'type', 'calculate',

    # Compound terms that should stay together
    'certificationtracking', 'safetyinspection', 'compliancemanagement', 'equipmentrental',
    'managementtool', 'certificationmanagement', 'systemreview'
}

def smart_vocabulary_split(word):
    """
    Split word using vocabulary, prioritizing longer matches
    """
    word_lower = word.lower()
    result = []
    remaining = word_lower

    # Get max word length from vocabulary
    max_word_len = max(len(w) for w in VOCAB)

    while remaining:
        matched = False
        # Try longest matches first (from max to min)
        for length in range(min(max_word_len, len(remaining)), 3, -1):  # Minimum 3 chars
            candidate = remaining[:length]
            if candidate in VOCAB:
                result.append(candidate)
                remaining = remaining[length:]
                matched = True
                break

        if not matched:
            # Fallback: take 4-6 chars if no match (avoid tiny chunks)
            chunk_size = min(6, len(remaining))
            if len(remaining) < 4:
                # If remaining is too short, just add it
                result.append(remaining)
                remaining = ''
            else:
                result.append(remaining[:chunk_size])
                remaining = remaining[chunk_size:]

    return ' '.join(result)

def intelligent_split(text):
    """
    Combine camelCase splitting + vocabulary splitting
    """
    # Step 1: CamelCase splitting
    result = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    result = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', result)

    # Step 2: Find remaining long lowercase sequences (>12 chars)
    long_lower = re.compile(r'[a-z]{12,}')

    for match in long_lower.finditer(result):
        word = match.group(0)
        split_version = smart_vocabulary_split(word)
        result = result.replace(word, split_version, 1)  # Replace only first occurrence

    return result

def fix_file(filepath):
    """Fix broken translations in JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Fix all text fields
        for key in ['title', 'description', 'content']:
            if key in data:
                data[key] = intelligent_split(data[key])

        # Fix keywords
        if 'seo_keywords' in data:
            data['seo_keywords'] = [intelligent_split(kw) for kw in data['seo_keywords']]

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

# Files to fix
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
print("FIXING BROKEN MACHINE TRANSLATIONS (IMPROVED ALGORITHM)")
print("=" * 80)

fixed = []
for filename in files:
    filepath = os.path.join(base_path, filename)
    print(f"\n📝 {filename}")

    if fix_file(filepath):
        fixed.append(filename)
        print(f"   ✅ Fixed")

        # Preview
        with open(filepath, 'r') as f:
            data = json.load(f)
        print(f"   Preview: {data['title'][:120]}")

print("\n" + "=" * 80)
print(f"SUMMARY: {len(fixed)}/{len(files)} files fixed")
print("=" * 80)