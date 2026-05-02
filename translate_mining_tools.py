#!/usr/bin/env python3
"""
Translate all Chinese JSON files in mining-extraction-tools to natural American English.
Uses Claude API for semantic translation.
"""

import os
import json
import re
from anthropic import Anthropic

# Initialize Anthropic client
client = Anthropic()

BASE_PATH = '/Users/gejiayu/owner/seo/data/mining-extraction-tools'

# Find all files with Chinese characters
chinese_pattern = re.compile(r'[一-鿿]')
chinese_files = []

for filename in os.listdir(BASE_PATH):
    if filename.endswith('.json'):
        filepath = os.path.join(BASE_PATH, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if chinese_pattern.search(content):
                chinese_files.append(filepath)

print(f"Found {len(chinese_files)} files with Chinese content")

def translate_to_english(text, field_type="content"):
    """Translate Chinese text to natural American English using Claude API."""

    if not text or not chinese_pattern.search(text):
        return text

    # Build prompt based on field type
    if field_type == "title":
        prompt = f"Translate this Chinese title to natural American English. Keep it concise and SEO-friendly. Do not add any explanations:\n\n{text}"
    elif field_type == "description":
        prompt = f"Translate this Chinese description to natural American English. Keep it compelling and SEO-friendly (150-160 chars ideal). Do not add any explanations:\n\n{text}"
    elif field_type == "keywords":
        prompt = f"Translate these Chinese SEO keywords to natural American English keywords. Return as a JSON array. Do not add any explanations:\n\n{text}"
    else:  # content
        prompt = f"Translate this Chinese content to natural American English. Maintain all HTML tags and structure exactly. Keep technical terminology accurate. Do not add any explanations:\n\n{text}"

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8000 if field_type == "content" else 500,
            messages=[{"role": "user", "content": prompt}]
        )

        result = message.content[0].text.strip()

        # For keywords, parse as JSON array
        if field_type == "keywords":
            # Remove any markdown formatting
            result = result.replace('```json', '').replace('```', '').strip()
            try:
                parsed = json.loads(result)
                if isinstance(parsed, list):
                    return parsed
            except:
                # If not valid JSON, split by common delimiters
                keywords = [k.strip() for k in result.replace(',', '\n').split('\n') if k.strip() and not k.startswith('#')]
                return keywords

        return result
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def process_file(filepath):
    """Process a single JSON file - translate all Chinese content."""

    print(f"\nProcessing: {os.path.basename(filepath)}")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Translate title
    if chinese_pattern.search(data.get('title', '')):
        print("  Translating title...")
        data['title'] = translate_to_english(data['title'], 'title')
        print(f"  Title: {data['title'][:80]}...")

    # Translate description
    if chinese_pattern.search(data.get('description', '')):
        print("  Translating description...")
        data['description'] = translate_to_english(data['description'], 'description')
        print(f"  Description: {data['description'][:80]}...")

    # Translate content
    if chinese_pattern.search(data.get('content', '')):
        print("  Translating content...")
        data['content'] = translate_to_english(data['content'], 'content')
        print(f"  Content length: {len(data['content'])} chars")

    # Translate seo_keywords - ensure it's an array
    keywords = data.get('seo_keywords', [])
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.replace(',', ';').split(';') if k.strip()]
    elif keywords and any(chinese_pattern.search(k) for k in keywords):
        print("  Translating keywords...")
        keywords_text = json.dumps(keywords)
        keywords = translate_to_english(keywords_text, 'keywords')

    data['seo_keywords'] = keywords if isinstance(keywords, list) else []
    print(f"  Keywords: {data['seo_keywords']}")

    # Add language field
    data['language'] = 'en-US'

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  ✓ Completed: {os.path.basename(filepath)}")
    return True

# Process all files
success_count = 0
error_count = 0

for filepath in sorted(chinese_files):
    try:
        if process_file(filepath):
            success_count += 1
    except Exception as e:
        print(f"  ✗ Error processing {filepath}: {e}")
        error_count += 1

print(f"\n{'='*60}")
print(f"SUMMARY: {success_count} files translated successfully, {error_count} errors")
print(f"{'='*60}")