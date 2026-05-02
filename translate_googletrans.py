#!/usr/bin/env python3
"""
Translation script using googletrans library for better rate limit handling.
"""

import os
import sys
import json
import re
import time

# Import googletrans
try:
    from googletrans import Translator
    HAS_GOOGLETRANS = True
except ImportError:
    HAS_GOOGLETRANS = False
    print("googletrans not available, using fallback method", flush=True)

# Constants
DIRECTORY = '/Users/gejiayu/owner/seo/data/machinery-heavy-equipment-rental-tools'
DELAY = 1.0  # Longer delay between requests

def contains_chinese(text):
    """Check if text contains Chinese characters"""
    if not isinstance(text, str):
        return False
    return bool(re.search(r'[一-龥]', text))

def translate_text_googletrans(translator, text, retry=3):
    """Translate text using googletrans"""
    if not text or not contains_chinese(text):
        return text

    for attempt in range(retry):
        try:
            result = translator.translate(text, src='zh-CN', dest='en')
            return result.text
        except Exception as e:
            if attempt < retry - 1:
                print(f"  Translation error, retrying ({attempt+1}/{retry}): {e}", flush=True)
                time.sleep(2)
            else:
                print(f"  Translation failed: {e}", flush=True)
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
            return False, "No Chinese content"

        filename = os.path.basename(filepath)
        print(f"  Translating {filename}...", flush=True)

        # Translate title
        if contains_chinese(data.get('title', '')):
            data['title'] = translate_text_googletrans(translator, data['title'])
            time.sleep(DELAY)

        # Translate description
        if contains_chinese(data.get('description', '')):
            data['description'] = translate_text_googletrans(translator, data['description'])
            time.sleep(DELAY)

        # Translate content (split into chunks for large content)
        if contains_chinese(data.get('content', '')):
            content = data['content']
            # Split by <section> for better handling
            if '<section>' in content:
                parts = content.split('<section>')
                translated_parts = []
                for i, part in enumerate(parts):
                    if contains_chinese(part):
                        trans = translate_text_googletrans(translator, part)
                        translated_parts.append(trans)
                        time.sleep(DELAY)
                    else:
                        translated_parts.append(part)
                data['content'] = '<section>'.join(translated_parts)
            else:
                data['content'] = translate_text_googletrans(translator, content)
                time.sleep(DELAY)

        # Translate keywords
        if isinstance(data.get('seo_keywords', []), list):
            translated_keywords = []
            for kw in data['seo_keywords']:
                if contains_chinese(kw):
                    trans_kw = translate_text_googletrans(translator, kw)
                    translated_keywords.append(trans_kw)
                    time.sleep(DELAY/2)
                else:
                    translated_keywords.append(kw)
            data['seo_keywords'] = translated_keywords

        # Translate author
        if contains_chinese(data.get('author', '')):
            data['author'] = translate_text_googletrans(translator, data['author'])
            time.sleep(DELAY/2)

        # Keep language as en-US
        data['language'] = 'en-US'

        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True, "Success"

    except Exception as e:
        return False, f"Error: {e}"

def main():
    if not HAS_GOOGLETRANS:
        print("Error: googletrans library required", flush=True)
        sys.exit(1)

    files = sorted([f for f in os.listdir(DIRECTORY) if f.endswith('.json')])
    total = len(files)

    print(f"{'='*60}", flush=True)
    print(f"Translating {total} files using googletrans", flush=True)
    print(f"{'='*60}", flush=True)

    # Create translator
    translator = Translator()

    translated_count = 0
    skipped_count = 0
    error_count = 0

    for i, filename in enumerate(files, 1):
        filepath = os.path.join(DIRECTORY, filename)
        print(f"\n[{i}/{total}] {filename}", flush=True)

        success, message = translate_file(filepath, translator)

        if success:
            translated_count += 1
            print(f"  -> Done", flush=True)
        elif "No Chinese" in message:
            skipped_count += 1
            print(f"  -> Skipped", flush=True)
        else:
            error_count += 1
            print(f"  -> {message}", flush=True)

    print(f"\n{'='*60}", flush=True)
    print(f"Complete! Translated: {translated_count}, Skipped: {skipped_count}, Errors: {error_count}", flush=True)
    print(f"{'='*60}", flush=True)

if __name__ == '__main__':
    main()