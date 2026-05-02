#!/usr/bin/env python3
"""
Script to fix Chinese-English mixed content in JSON files
Translates broken Chinese-English content to proper English
"""

import json
import os
import re
import anthropic
from pathlib import Path

# Directory to process
DATA_DIR = "/Users/gejiayu/owner/seo/data/retail-ecommerce-operations-tools/"

# Chinese character pattern
CHINESE_PATTERN = re.compile(r'[一-鿿]')

def find_chinese_files():
    """Find all JSON files with Chinese content"""
    chinese_files = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    # Check title, description, content for Chinese characters
                    for field in ['title', 'description', 'content']:
                        if field in data and isinstance(data[field], str):
                            if CHINESE_PATTERN.search(data[field]):
                                chinese_files.append(filepath)
                                break
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
    return chinese_files

def translate_content(client, content, field_type="content"):
    """
    Translate Chinese-English mixed content to proper English
    Uses Claude Sonnet for semantic translation
    """
    prompt = f"""Translate this {field_type} to proper, fluent English. This is Chinese-English mixed content that needs to be converted to natural English.

Original content:
{content}

Requirements:
1. Translate ALL Chinese characters to English
2. Keep proper English terms intact
3. Maintain the same structure and formatting
4. Ensure the English is natural and professional
5. For technical terms, use standard English equivalents
6. Keep HTML tags and formatting unchanged

Output ONLY the translated {field_type}, nothing else."""

    message = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text.strip()

def translate_keywords(client, keywords):
    """Translate keywords array"""
    keywords_str = json.dumps(keywords, ensure_ascii=False)

    prompt = f"""Translate these SEO keywords to proper English. This contains Chinese keywords that need to be translated.

Original keywords:
{keywords_str}

Requirements:
1. Translate each Chinese keyword to English
2. Keep English keywords unchanged
3. Use standard SEO terminology
4. Return as a JSON array of strings
5. Output ONLY the JSON array, nothing else"""

    message = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    try:
        return json.loads(message.content[0].text.strip())
    except:
        # If parsing fails, return original
        return keywords

def fix_file(filepath, client):
    """Fix a single JSON file"""
    print(f"Processing: {os.path.basename(filepath)}")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Translate title
    if CHINESE_PATTERN.search(data.get('title', '')):
        print(f"  - Translating title...")
        data['title'] = translate_content(client, data['title'], "title")

    # Translate description
    if CHINESE_PATTERN.search(data.get('description', '')):
        print(f"  - Translating description...")
        data['description'] = translate_content(client, data['description'], "description")

    # Translate content
    if CHINESE_PATTERN.search(data.get('content', '')):
        print(f"  - Translating content...")
        data['content'] = translate_content(client, data['content'], "content")

    # Translate seo_keywords
    if 'seo_keywords' in data:
        keywords_str = json.dumps(data['seo_keywords'], ensure_ascii=False)
        if CHINESE_PATTERN.search(keywords_str):
            print(f"  - Translating keywords...")
            data['seo_keywords'] = translate_keywords(client, data['seo_keywords'])

    # Ensure language field
    data['language'] = 'en-US'

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  ✓ Fixed: {os.path.basename(filepath)}")
    return True

def main():
    """Main function"""
    print("Finding files with Chinese content...")
    chinese_files = find_chinese_files()

    print(f"\nFound {len(chinese_files)} files to fix:\n")
    for f in chinese_files:
        print(f"  - {os.path.basename(f)}")

    print("\nStarting translation process...")

    # Initialize Anthropic client
    client = anthropic.Anthropic()

    fixed_count = 0
    for filepath in chinese_files:
        try:
            if fix_file(filepath, client):
                fixed_count += 1
        except Exception as e:
            print(f"  ✗ Error fixing {os.path.basename(filepath)}: {e}")

    print(f"\n{'='*60}")
    print(f"SUMMARY: Fixed {fixed_count} out of {len(chinese_files)} files")
    print(f"{'='*60}")

    return fixed_count

if __name__ == "__main__":
    main()
