#!/usr/bin/env python3
"""
Translation script for machinery-heavy-equipment-rental-tools JSON files.
Translates Chinese content to English while preserving JSON structure.
"""

import os
import sys
import json
import re
import time
from deep_translator import GoogleTranslator

# Initialize translator
translator = GoogleTranslator(source='zh-CN', target='en')

def contains_chinese(text):
    """Check if text contains Chinese characters"""
    if not isinstance(text, str):
        return False
    return bool(re.search(r'[一-鿿]', text))

def translate_text(text, max_chunk_size=4500):
    """Translate text, splitting large content into chunks"""
    if not contains_chinese(text):
        return text

    # For large content, split into chunks
    if len(text) > max_chunk_size:
        # Split by sections for HTML content
        sections = re.split(r'</section>', text)
        translated_sections = []

        for section in sections:
            if section.strip():
                try:
                    translated = translator.translate(section.strip())
                    translated_sections.append(translated)
                except Exception as e:
                    print(f"Translation error for chunk: {e}")
                    translated_sections.append(section)

        return ''.join(translated_sections)

    try:
        return translator.translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def translate_keywords(keywords):
    """Translate keywords array"""
    if not isinstance(keywords, list):
        return keywords

    translated = []
    for kw in keywords:
        if contains_chinese(kw):
            try:
                translated_kw = translator.translate(kw)
                translated.append(translated_kw)
            except Exception as e:
                print(f"Keyword translation error: {e}")
                translated.append(kw)
        else:
            translated.append(kw)

    return translated

def translate_file(filepath):
    """Translate a JSON file's Chinese content to English"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if file needs translation
    needs_translation = False
    for field in ['title', 'description', 'content', 'author']:
        if contains_chinese(data.get(field, '')):
            needs_translation = True
            break

    if not needs_translation:
        return False

    # Translate fields
    print(f"Translating: {os.path.basename(filepath)}", flush=True)

    if contains_chinese(data.get('title', '')):
        data['title'] = translate_text(data['title'])
        time.sleep(0.1)  # Rate limiting

    if contains_chinese(data.get('description', '')):
        data['description'] = translate_text(data['description'])
        time.sleep(0.1)

    if contains_chinese(data.get('content', '')):
        data['content'] = translate_text(data['content'])
        time.sleep(0.2)  # Longer delay for large content

    if isinstance(data.get('seo_keywords', []), list):
        data['seo_keywords'] = translate_keywords(data['seo_keywords'])
        time.sleep(0.1)

    if contains_chinese(data.get('author', '')):
        data['author'] = translate_text(data['author'])

    # Keep language as en-US
    data['language'] = 'en-US'

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return True

def main():
    directory = '/Users/gejiayu/owner/seo/data/machinery-heavy-equipment-rental-tools'
    files = sorted([f for f in os.listdir(directory) if f.endswith('.json')])

    total = len(files)
    count = 0

    print(f"Processing {total} files...", flush=True)

    for i, filename in enumerate(files, 1):
        filepath = os.path.join(directory, filename)
        print(f"[{i}/{total}] Processing {filename}...", flush=True)

        try:
            if translate_file(filepath):
                count += 1
        except Exception as e:
            print(f"Error processing {filename}: {e}", flush=True)
            continue

    print(f"\nTotal files translated: {count}/{total}", flush=True)

if __name__ == '__main__':
    main()