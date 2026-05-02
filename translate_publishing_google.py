#!/usr/bin/env python3
"""
Translate all Chinese content to English in publishing-media-tools JSON files
using Google Translate (free via deep-translator library).
"""
import json
import os
import re
from pathlib import Path
from deep_translator import GoogleTranslator

def contains_chinese(text):
    """Check if text contains Chinese characters."""
    if not isinstance(text, str):
        return False
    chinese_pattern = re.compile(r'[一-鿿]')
    return bool(chinese_pattern.search(text))

def translate_text(text, translator):
    """Translate Chinese text to English using Google Translator."""
    if not isinstance(text, str) or not contains_chinese(text):
        return text

    try:
        # Use Google Translator
        translated = translator.translate(text)
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def translate_keywords(keywords, translator):
    """Translate SEO keywords array."""
    if not isinstance(keywords, list):
        return keywords

    translated_keywords = []
    for keyword in keywords:
        if contains_chinese(keyword):
            try:
                translated = translator.translate(keyword)
                translated_keywords.append(translated)
            except Exception as e:
                print(f"Keyword translation error: {e}")
                translated_keywords.append(keyword)
        else:
            translated_keywords.append(keyword)

    return translated_keywords

def process_file(filepath, translator):
    """Process a single JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Translate each field
        if 'title' in data and contains_chinese(data['title']):
            data['title'] = translate_text(data['title'], translator)

        if 'description' in data and contains_chinese(data['description']):
            data['description'] = translate_text(data['description'], translator)

        if 'content' in data and contains_chinese(data['content']):
            data['content'] = translate_text(data['content'], translator)

        if 'seo_keywords' in data:
            data['seo_keywords'] = translate_keywords(data['seo_keywords'], translator)

        if 'author' in data and contains_chinese(data['author']):
            data['author'] = translate_text(data['author'], translator)

        # Keep slug, published_at, language unchanged

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✓ Translated: {filepath.name}")
        return True

    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False

def main():
    """Main processing function."""
    # Initialize translator
    translator = GoogleTranslator(source='zh-CN', target='en')

    data_dir = Path('/Users/gejiayu/owner/seo/data/publishing-media-tools')

    if not data_dir.exists():
        print(f"Directory not found: {data_dir}")
        return

    json_files = list(data_dir.glob('*.json'))
    print(f"Found {len(json_files)} JSON files to process\n")

    success_count = 0
    for i, filepath in enumerate(json_files, 1):
        print(f"[{i}/{len(json_files)}] Processing {filepath.name}...")
        if process_file(filepath, translator):
            success_count += 1

    print(f"\n{'='*60}")
    print(f"Completed: {success_count}/{len(json_files)} files translated successfully")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()