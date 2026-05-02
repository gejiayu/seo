#!/usr/bin/env python3
"""
Translation script with multiple fallback methods.
Uses different translation endpoints to handle rate limiting.
"""

import os
import sys
import json
import re
import time
import html
import urllib.request
import urllib.parse
import urllib.error
import random

# Constants
DIRECTORY = '/Users/gejiayu/owner/seo/data/machinery-heavy-equipment-rental-tools'

# Multiple endpoints for translation (to avoid rate limiting)
TRANSLATE_ENDPOINTS = [
    'https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-CN&tl=en&dt=t&q=',
    'https://translate.googleapis.com/translate_a/single?client=dict-chrome-ex&sl=zh-CN&tl=en&dt=t&q=',
]

def contains_chinese(text):
    """Check if text contains Chinese characters"""
    if not isinstance(text, str):
        return False
    return bool(re.search(r'[一-龥]', text))

def translate_with_endpoint(text, endpoint_index=0, retry=5):
    """Translate using Google Translate endpoint"""
    if not text or not contains_chinese(text):
        return text

    for attempt in range(retry):
        try:
            # Use random endpoint to distribute load
            endpoint = TRANSLATE_ENDPOINTS[endpoint_index % len(TRANSLATE_ENDPOINTS)]

            encoded_text = urllib.parse.quote(text, safe='')
            url = endpoint + encoded_text

            # Create request with random user agent
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            ]

            request = urllib.request.Request(
                url,
                headers={
                    'User-Agent': random.choice(user_agents),
                }
            )

            response = urllib.request.urlopen(request, timeout=30)
            result = response.read().decode('utf-8')

            # Parse response
            import ast
            translated_parts = []
            try:
                data = ast.literal_eval(result)
                if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                    for item in data[0]:
                        if isinstance(item, list) and len(item) > 0 and item[0]:
                            translated_parts.append(str(item[0]))
            except:
                # Regex fallback
                matches = re.findall(r'"([^"]+)"', result)
                if matches:
                    for m in matches:
                        if len(m) > 5:
                            translated_parts.append(m)

            if translated_parts:
                return html.unescape(''.join(translated_parts))

            return text

        except urllib.error.HTTPError as e:
            if e.code == 429:  # Rate limited
                print(f"  Rate limited, waiting 5s...", flush=True)
                time.sleep(5)
                endpoint_index += 1  # Try different endpoint
            elif attempt < retry - 1:
                time.sleep(2)
            else:
                print(f"  HTTP error {e.code}", flush=True)
                return text

        except Exception as e:
            if attempt < retry - 1:
                time.sleep(2)
            else:
                print(f"  Error: {e}", flush=True)
                return text

    return text

def translate_file(filepath):
    """Translate a single JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if file has Chinese content
        has_chinese = any(contains_chinese(data.get(field, '')) for field in ['title', 'description', 'content', 'author'])

        if not has_chinese:
            return False, "No Chinese"

        print(f"  Translating...", flush=True)

        # Translate each field with delay
        if contains_chinese(data.get('title', '')):
            data['title'] = translate_with_endpoint(data['title'], 0)
            time.sleep(1)

        if contains_chinese(data.get('description', '')):
            data['description'] = translate_with_endpoint(data['description'], 1)
            time.sleep(1)

        if contains_chinese(data.get('content', '')):
            content = data['content']
            # Split by sections for large content
            if '<section>' in content:
                parts = content.split('<section>')
                translated_parts = []
                for i, part in enumerate(parts):
                    if contains_chinese(part):
                        trans = translate_with_endpoint(part, i % 2)
                        translated_parts.append(trans)
                        time.sleep(1.5)  # Longer delay for sections
                    else:
                        translated_parts.append(part)
                data['content'] = '<section>'.join(translated_parts)
            else:
                data['content'] = translate_with_endpoint(content, 2)
                time.sleep(1)

        # Translate keywords
        if isinstance(data.get('seo_keywords', []), list):
            translated_keywords = []
            for kw in data['seo_keywords']:
                if contains_chinese(kw):
                    trans_kw = translate_with_endpoint(kw, 3)
                    translated_keywords.append(trans_kw)
                    time.sleep(0.5)
                else:
                    translated_keywords.append(kw)
            data['seo_keywords'] = translated_keywords

        if contains_chinese(data.get('author', '')):
            data['author'] = translate_with_endpoint(data['author'], 4)

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
    print(f"Translating {total} files (with rate limit handling)", flush=True)
    print(f"{'='*60}", flush=True)

    translated = 0
    skipped = 0
    errors = 0

    for i, filename in enumerate(files, 1):
        filepath = os.path.join(DIRECTORY, filename)
        print(f"\n[{i}/{total}] {filename}", flush=True)

        success, message = translate_file(filepath)

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