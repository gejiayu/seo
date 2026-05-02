#!/usr/bin/env python3
import json
import re

def split_long_words(text):
    """
    Split very long concatenated words (>20 chars) using camelCase pattern and word boundaries
    """
    # Find words longer than 20 characters (no spaces)
    long_word_pattern = re.compile(r'[a-zA-Z]{20,}')

    def split_word(word):
        """Split a single long word"""
        # CamelCase splitting - insert space before capitals
        result = re.sub(r'([a-z])([A-Z])', r'\1 \2', word)
        # Handle all-caps sequences like "FDA" followed by lowercase
        result = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', result)
        return result

    # Replace all long words
    result = text
    for match in long_word_pattern.finditer(text):
        word = match.group(0)
        split_version = split_word(word)
        result = result.replace(word, split_version)

    return result

def fix_file(filepath):
    """Fix broken translations in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Fix all text fields
        for key in ['title', 'description', 'content']:
            if key in data:
                data[key] = split_long_words(data[key])

        # Fix keywords
        if 'seo_keywords' in data:
            data['seo_keywords'] = [split_long_words(kw) for kw in data['seo_keywords']]

        # Ensure language field
        if 'language' not in data:
            data['language'] = 'en-US'

        # Save
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

# Test
test_file = "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-compliance-management-system-review.json"
if fix_file(test_file):
    print("✅ Test successful")
    with open(test_file, 'r') as f:
        data = json.load(f)
    print(f"\nFixed title preview:\n{data['title'][:150]}...")
else:
    print("❌ Test failed")