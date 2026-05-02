#!/usr/bin/env python3
"""
Translation script using deep-translator library.
"""

import os
import sys
import json
import re
import time
from deep_translator import GoogleTranslator

# Constants
DIRECTORY = '/Users/gejiayu/owner/seo/data/machinery-heavy-equipment-rental-tools'
DELAY = 0.5  # Delay between requests

def contains_chinese(text):
    """Check if text contains Chinese characters"""
    if not isinstance(text, str):
        return False
    return bool(re.search(r'[一-龥]', text))

def translate_text(translator, text, retry=3):
    """Translate text using deep-translator"""
    if not text or not contains_chinese(text):
        return text

    for attempt in range(retry):
        try:
            result = translator.translate(text)
            return result
        except Exception as e:
            if attempt < retry - 1:
                print(f"  Retry ({attempt+1}/{retry})...", flush=True)
                time.sleep(2)
            else:
                print(f"  Failed: {e}", flush=True)
                return text

    return text

def translate_file(filepath, translator):
    """Translate a single JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if file has Chinese content
        fields_to_check = ['title', 'description', 'content', 'author']
        has_chinese = any(contains_chinese(data.get(field, '')) for field in fields_to_check)

        if not has_chinese:
            return False, "No Chinese"

        filename = os.path.basename(filepath)
        print(f"  Translating...", flush=True)

        # Translate title
        if contains_chinese(data.get('title', '')):
            data['title'] = translate_text(translator, data['title'])
            time.sleep(DELAY)

        # Translate description
        if contains_chinese(data.get('description', '')):
            data['description'] = translate_text(translator, data['description'])
            time.sleep(DELAY)

        # Translate content (handle large content)
        if contains_chinese(data.get('content', '')):
            content = data['content']
            # Split by sections for large content
            if '<section>' in content and len(content) > 5000:
                parts = content.split('<section>')
                translated_parts = []
                for i, part in enumerate(parts):
                    if contains_chinese(part):
                        trans = translate_text(translator, part)
                        translated_parts.append(trans)
                        time.sleep(DELAY)
                        print(f"    Section {i+1}/{len(parts)}", flush=True)
                    else:
                        translated_parts.append(part)
                data['content'] = '<section>'.join(translated_parts)
            else:
                data['content'] = translate_text(translator, content)
                time.sleep(DELAY)

        # Translate keywords
        if isinstance(data.get('seo_keywords', []), list):
            translated_keywords = []
            for kw in data['seo_keywords']:
                if contains_chinese(kw):
                    trans_kw = translate_text(translator, kw)
                    translated_keywords.append(trans_kw)
                    time.sleep(DELAY/2)
                else:
                    translated_keywords.append(kw)
            data['seo_keywords'] = translated_keywords

        # Translate author
        if contains_chinese(data.get('author', '')):
            data['author'] = translate_text(translator, data['author'])

        # Keep language as en-US
        data['language'] = 'en-US'

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True, "OK"

    except Exception as e:
        return False, f"Error: {e}"

def main():
    files = sorted([f for f in os.listdir(DIRECTORY) if f.endswith('.json')])
    total = len(files)

    print(f"{'='*60}", flush=True)
    print(f"Translating {total} files with deep-translator", flush=True)
    print(f"{'='*60}", flush=True)

    # Create translator
    translator = GoogleTranslator(source='zh-CN', target='en')

    translated = 0
    skipped = 0
    errors = 0

    for i, filename in enumerate(files, 1):
        filepath = os.path.join(DIRECTORY, filename)
        print(f"\n[{i}/{total}] {filename}", flush=True)

        success, message = translate_file(filepath, translator)

        if success:
            translated += 1
            print(f"  Done!", flush=True)
        elif "No Chinese" in message:
            skipped += 1
            print(f"  Skipped", flush=True)
        else:
            errors += 1
            print(f"  {message}", flush=True)

    print(f"\n{'='*60}", flush=True)
    print(f"Result: {translated} translated, {skipped} skipped, {errors} errors", flush=True)
    print(f"{'='*60}", flush=True)

if __name__ == '__main__':
    main()