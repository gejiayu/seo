#!/usr/bin/env python3
import json
import re
import os

# Medical equipment domain vocabulary
MEDICAL_VOCAB = {
    'medical', 'equipment', 'rental', 'compliance', 'management', 'system', 'review',
    'fda', 'certification', 'tracking', 'safety', 'inspection', 'tool', 'ce',
    'plan', 'disinfection', 'iso', 'quality', 'device', 'standard', 'market',
    'validity', 'period', 'expired', 'renewal', 'scope', 'cover', 'model',
    'functionality', 'use', 'update', 'reminder', 'expiration', 'automatic',
    'class', 'level', 'technology', 'documentation', 'storage', 'public',
    'report', 'structure', 'information', 'audit', 'tracking', 'design',
    'birth', 'maintenance', 'process', 'project', 'list', 'electric', 'gas',
    'machine', 'instrument', 'radiation', 'result', 'record', 'non-compliant',
    'warning', 'rectification', 'completed', 'recovery', 'prevent', 'submit',
    'fork', 'sense', 'infection', 'key', 'high', 'temperature', 'ization',
    'study', 'outside', 'line', 'agent', 'personnel', 'time', 'verification',
    'effectiveness', 'prohibit', 'mainstream', 'product', 'suite', 'professional',
    'core', 'database', 'cloud', 'deployment', 'generate', 'pricing', 'strategy',
    'basic', 'version', 'include', 'depth', 'manager', 'focuses', 'connect',
    'api', 'real-time', 'status', 'query', 'compliance', 'european', 'union',
    'method', 'update', 'platform', 'allocation', 'execution', 'task', 'mobile',
    'terminal', 'app', 'support', 'on-site', 'enter', 'sterilize', 'log',
    'prediction', 'demand', 'crm', 'customer', 'service', 'satisfaction',
    'analytics', 'data', 'bi', 'visualization', 'delivery', 'digital',
    'transformation', 'document', 'energy', 'finance', 'financial', 'flow',
    'roi', 'calculate', 'fleet', 'globalization', 'hr', 'human', 'resource',
    'innovation', 'churn', 'ai', 'big', 'blockchain', 'cashflow', 'change'
}

def split_concatenated_words(text):
    """Split concatenated words without spaces"""
    # Pattern for very long concatenated words (>15 chars)
    long_word_pattern = re.compile(r'[a-z]{15,}')

    def split_word(word):
        """Split a concatenated word using vocabulary and camelCase detection"""
        if len(word) < 15:
            return word

        # Try to split using vocabulary
        result = []
        remaining = word.lower()
        max_word_len = max(len(w) for w in MEDICAL_VOCAB)

        while remaining:
            # Try to match the longest possible word from vocabulary
            matched = False
            for length in range(min(max_word_len, len(remaining)), 2, -1):
                candidate = remaining[:length]
                if candidate in MEDICAL_VOCAB:
                    result.append(candidate)
                    remaining = remaining[length:]
                    matched = True
                    break

            if not matched:
                # If no vocabulary match, take 3-6 characters as a fallback
                chunk_size = min(6, len(remaining))
                result.append(remaining[:chunk_size])
                remaining = remaining[chunk_size:]

        return ' '.join(result)

    # Find and replace all long concatenated words
    matches = long_word_pattern.findall(text.lower())
    for match in matches:
        split_version = split_word(match)
        # Replace in original text (case-insensitive)
        text = re.sub(re.escape(match), split_version, text, flags=re.IGNORECASE)

    return text

def fix_broken_translations(filepath):
    """Fix broken machine translations in a JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Fix title
        if 'title' in data:
            data['title'] = split_concatenated_words(data['title'])

        # Fix description
        if 'description' in data:
            data['description'] = split_concatenated_words(data['description'])

        # Fix content (HTML content)
        if 'content' in data:
            data['content'] = split_concatenated_words(data['content'])

        # Fix seo_keywords array
        if 'seo_keywords' in data and isinstance(data['seo_keywords'], list):
            data['seo_keywords'] = [split_concatenated_words(kw) for kw in data['seo_keywords']]

        # Ensure language field exists
        if 'language' not in data:
            data['language'] = 'en-US'

        # Save fixed file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True

    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

# Files to fix (18 files with broken translations)
files_to_fix = [
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-compliance-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-contract-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-cost-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-crm-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-customer-satisfaction-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-customer-service-management-system-review.json",
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

print("=" * 80)
print("FIXING BROKEN MACHINE TRANSLATIONS")
print("=" * 80)

fixed_count = 0
for filepath in files_to_fix:
    filename = os.path.basename(filepath)
    if fix_broken_translations(filepath):
        print(f"✅ Fixed: {filename}")
        fixed_count += 1
    else:
        print(f"❌ Failed: {filename}")

print("\n" + "=" * 80)
print(f"TOTAL FILES FIXED: {fixed_count}/{len(files_to_fix)}")
print("=" * 80)