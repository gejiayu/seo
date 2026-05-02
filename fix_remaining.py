#!/usr/bin/env python3
"""
Fix remaining Chinese content in files that failed due to SSL errors.
"""

import os
import json
import re
import time
import urllib.request
import urllib.parse

DIRECTORY = '/Users/gejiayu/owner/seo/data/machinery-heavy-equipment-rental-tools'

# Files with remaining Chinese content
FILES_TO_FIX = [
    'equipment-rental-inventory-management-review.json',
    'equipment-rental-quoting-system-review.json',
    'equipment-rental-scheduling-optimization-review.json',
    'forklift-rental-management-system-review.json',
    'heavy-machinery-digital-transformation-topic-38.json',
    'heavy-machinery-digital-transformation-topic-40.json',
    'heavy-machinery-digital-transformation-topic-45.json',
    'heavy-machinery-digital-transformation-topic-46.json',
    'heavy-machinery-digital-transformation-topic-53.json',
    'heavy-machinery-digital-transformation-topic-59.json',
    'heavy-machinery-digital-transformation-topic-77.json',
    'heavy-machinery-digital-transformation-topic-81.json',
    'heavy-machinery-digital-transformation-topic-82.json',
    'heavy-machinery-digital-transformation-topic-90.json',
    'heavy-machinery-digital-transformation-topic-93.json',
    'heavy-machinery-digital-transformation-topic-95.json',
    'heavy-machinery-digital-transformation-topic-96.json',
    'heavy-machinery-rental-finance-management-review.json',
    'heavy-machinery-rental-management-system-review-2026.json',
    'roller-rental-management-system-review.json',
]

def contains_chinese(text):
    if not isinstance(text, str):
        return False
    return bool(re.search(r'[一-龥]', text))

def translate_text(text, retry=5):
    """Translate Chinese text to English"""
    if not text or not contains_chinese(text):
        return text

    for attempt in range(retry):
        try:
            encoded = urllib.parse.quote(text, safe='')
            url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-CN&tl=en&dt=t&q={encoded}'

            request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(request, timeout=90)
            raw = response.read().decode('utf-8')

            data = json.loads(raw)
            translations = []
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                for item in data[0]:
                    if isinstance(item, list) and len(item) > 0 and isinstance(item[0], str):
                        translations.append(item[0])

            if translations:
                return ''.join(translations)

            return text

        except Exception as e:
            if attempt < retry - 1:
                print(f"  Retry {attempt+1}/{retry}...", flush=True)
                time.sleep(3)
            else:
                print(f"  Failed: {e}", flush=True)
                return text

    return text

def fix_file(filepath):
    """Fix remaining Chinese in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check which fields need fixing
        fields_to_fix = []
        for field in ['title', 'description', 'content', 'author']:
            if isinstance(data.get(field), str) and contains_chinese(data[field]):
                fields_to_fix.append(field)

        if not fields_to_fix:
            return False

        print(f"  Fixing: {fields_to_fix}", flush=True)

        # Fix each field
        for field in fields_to_fix:
            if field == 'content' and '<section>' in data[field]:
                # Split content into sections
                parts = data[field].split('<section>')
                translated_parts = []
                for i, part in enumerate(parts):
                    if contains_chinese(part):
                        trans = translate_text(part)
                        translated_parts.append(trans)
                        time.sleep(2)
                        print(f"    {field} section {i+1}/{len(parts)}", flush=True)
                    else:
                        translated_parts.append(part)
                data[field] = '<section>'.join(translated_parts)
            else:
                data[field] = translate_text(data[field])
                time.sleep(2)

        data['language'] = 'en-US'

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True

    except Exception as e:
        print(f"  Error: {e}", flush=True)
        return False

def main():
    print(f"{'='*60}", flush=True)
    print(f"Fixing {len(FILES_TO_FIX)} files with remaining Chinese", flush=True)
    print(f"{'='*60}", flush=True)

    fixed = 0

    for i, filename in enumerate(FILES_TO_FIX, 1):
        filepath = os.path.join(DIRECTORY, filename)
        print(f"\n[{i}/{len(FILES_TO_FIX)}] {filename}", flush=True)

        if fix_file(filepath):
            fixed += 1
            print(f"  Fixed!", flush=True)

    print(f"\n{'='*60}", flush=True)
    print(f"Fixed: {fixed}/{len(FILES_TO_FIX)}", flush=True)
    print(f"{'='*60}", flush=True)

if __name__ == '__main__':
    main()