#!/usr/bin/env python3
"""
Translation script using DeepL free API for better quality.
DeepL allows up to 500,000 characters/month on free tier.
"""

import os
import sys
import json
import re
import time
import urllib.request
import urllib.parse
import urllib.error

# Constants
DIRECTORY = '/Users/gejiayu/owner/seo/data/machinery-heavy-equipment-rental-tools'
# DeepL free API endpoint
DEEPL_URL = 'https://api-free.deepl.com/v2/translate'
# Note: You need a DeepL API key for this to work
# Get free key at: https://www.deepl.com/pro-api

def contains_chinese(text):
    """Check if text contains Chinese characters"""
    if not isinstance(text, str):
        return False
    return bool(re.search(r'[一-龥]', text))

def translate_deepl(text, api_key=None, retry=3):
    """Translate text using DeepL API"""
    if not text or not contains_chinese(text):
        return text

    # If no API key, use fallback to Google Translate
    if not api_key:
        return translate_google_fallback(text, retry)

    for attempt in range(retry):
        try:
            # DeepL API request
            data = urllib.parse.urlencode({
                'auth_key': api_key,
                'text': text,
                'source_lang': 'ZH',
                'target_lang': 'EN',
            }).encode('utf-8')

            request = urllib.request.Request(
                DEEPL_URL,
                data=data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )

            response = urllib.request.urlopen(request, timeout=30)
            result = json.loads(response.read().decode('utf-8'))

            if 'translations' in result and len(result['translations']) > 0:
                return result['translations'][0]['text']

            return text

        except Exception as e:
            if attempt < retry - 1:
                print(f"  Retry ({attempt+1}/{retry})...", flush=True)
                time.sleep(2)
            else:
                print(f"  Error: {e}", flush=True)
                return text

    return text

def translate_google_fallback(text, retry=3):
    """Fallback to Google Translate when DeepL is not available"""
    if not text or not contains_chinese(text):
        return text

    for attempt in range(retry):
        try:
            # Use a simple approach
            encoded = urllib.parse.quote(text, safe='')
            url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-CN&tl=en&dt=t&q={encoded}'

            request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(request, timeout=30)
            result = response.read().decode('utf-8')

            # Parse response more carefully
            import ast
            translated_parts = []
            try:
                data = ast.literal_eval(result)
                if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                    for item in data[0]:
                        if isinstance(item, list) and len(item) > 0 and isinstance(item[0], str):
                            # Only take the first element (translation)
                            translated_parts.append(item[0])
            except:
                pass

            if translated_parts:
                return ''.join(translated_parts)

            return text

        except Exception as e:
            if attempt < retry - 1:
                time.sleep(3)
            else:
                return text

    return text

def translate_file(filepath, api_key=None):
    """Translate a single JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        has_chinese = any(contains_chinese(data.get(field, '')) for field in ['title', 'description', 'content', 'author'])

        if not has_chinese:
            return False, "No Chinese"

        print(f"  Translating...", flush=True)

        # Translate fields with delay
        if contains_chinese(data.get('title', '')):
            data['title'] = translate_deepl(data['title'], api_key)
            time.sleep(1)

        if contains_chinese(data.get('description', '')):
            data['description'] = translate_deepl(data['description'], api_key)
            time.sleep(1)

        if contains_chinese(data.get('content', '')):
            content = data['content']
            if '<section>' in content:
                parts = content.split('<section>')
                translated_parts = []
                for i, part in enumerate(parts):
                    if contains_chinese(part):
                        trans = translate_deepl(part, api_key)
                        translated_parts.append(trans)
                        time.sleep(2)  # Longer delay for sections
                    else:
                        translated_parts.append(part)
                data['content'] = '<section>'.join(translated_parts)
            else:
                data['content'] = translate_deepl(content, api_key)
                time.sleep(1)

        if isinstance(data.get('seo_keywords', []), list):
            translated_keywords = []
            for kw in data['seo_keywords']:
                if contains_chinese(kw):
                    trans_kw = translate_deepl(kw, api_key)
                    translated_keywords.append(trans_kw)
                    time.sleep(0.5)
                else:
                    translated_keywords.append(kw)
            data['seo_keywords'] = translated_keywords

        if contains_chinese(data.get('author', '')):
            data['author'] = translate_deepl(data['author'], api_key)

        data['language'] = 'en-US'

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True, "OK"

    except Exception as e:
        return False, f"Error: {e}"

def main():
    files = sorted([f for f in os.listdir(DIRECTORY) if f.endswith('.json')])
    total = len(files)

    print(f"{'='*60}", flush=True)
    print(f"Translating {total} files", flush=True)
    print(f"{'='*60}", flush=True)

    # Check for DeepL API key in environment
    api_key = os.environ.get('DEEPL_API_KEY', None)
    if api_key:
        print("Using DeepL API", flush=True)
    else:
        print("Using Google Translate fallback (no DEEPL_API_KEY set)", flush=True)

    translated = 0
    skipped = 0
    errors = 0

    for i, filename in enumerate(files, 1):
        filepath = os.path.join(DIRECTORY, filename)
        print(f"\n[{i}/{total}] {filename}", flush=True)

        success, message = translate_file(filepath, api_key)

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