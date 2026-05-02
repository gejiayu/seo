#!/usr/bin/env python3
"""
Clean translation script - properly extracts translations from Google Translate response.
"""

import os
import sys
import json
import re
import time
import html
import urllib.request
import urllib.parse

DIRECTORY = '/Users/gejiayu/owner/seo/data/machinery-heavy-equipment-rental-tools'

def contains_chinese(text):
    """Check if text contains Chinese characters"""
    if not isinstance(text, str):
        return False
    return bool(re.search(r'[一-龥]', text))

def translate_text(text, delay=1.0):
    """Translate Chinese text to English using Google Translate"""
    if not text or not contains_chinese(text):
        return text

    try:
        encoded = urllib.parse.quote(text, safe='')
        url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-CN&tl=en&dt=t&q={encoded}'

        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(request, timeout=60)
        raw = response.read().decode('utf-8')

        # Parse response carefully
        # Format: [[["translation","original",null,null,10],...],...]
        # We need only the first string of each inner triple

        translations = []

        # Use a simple state machine to parse
        # Find content between [[[" and "]]]
        start = raw.find('[[["')
        if start >= 0:
            start += 4  # Skip [[["

            # Find each translation string
            i = start
            while i < len(raw):
                if raw[i] == '"':
                    # Find the end of this quoted string
                    j = i + 1
                    while j < len(raw) and raw[j] != '"':
                        if raw[j] == '\\':
                            j += 2  # Skip escaped character
                        else:
                            j += 1

                    # Extract the string
                    if j < len(raw):
                        str_content = raw[i+1:j]
                        # Skip if it looks like metadata (contains numbers or .md)
                        if not re.search(r'^\d+$|\.md$', str_content):
                            translations.append(str_content)
                        i = j + 2  # Skip " and ,
                        # Stop after we get the main content
                        if len(raw[i:i+10]) in ['",null', '",', ']]']:
                            break
                    else:
                        break
                else:
                    i += 1

        if translations:
            result = ''.join(translations)
            return html.unescape(result)

        return text

    except Exception as e:
        print(f"  Error: {e}", flush=True)
        return text

def translate_file(filepath):
    """Translate a JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        has_chinese = any(contains_chinese(data.get(field, '')) for field in ['title', 'description', 'content', 'author'])

        if not has_chinese:
            return False

        filename = os.path.basename(filepath)
        print(f"  Translating fields...", flush=True)

        # Translate title
        if contains_chinese(data.get('title', '')):
            data['title'] = translate_text(data['title'])
            time.sleep(1)

        # Translate description
        if contains_chinese(data.get('description', '')):
            data['description'] = translate_text(data['description'])
            time.sleep(1)

        # Translate content in chunks
        if contains_chinese(data.get('content', '')):
            content = data['content']
            if '<section>' in content:
                parts = content.split('<section>')
                translated_parts = []
                for i, part in enumerate(parts):
                    if contains_chinese(part):
                        trans = translate_text(part)
                        translated_parts.append(trans)
                        time.sleep(1.5)
                        print(f"    Section {i+1}/{len(parts)} done", flush=True)
                    else:
                        translated_parts.append(part)
                data['content'] = '<section>'.join(translated_parts)
            else:
                data['content'] = translate_text(content)
                time.sleep(1)

        # Translate keywords
        if isinstance(data.get('seo_keywords', []), list):
            keywords = []
            for kw in data['seo_keywords']:
                if contains_chinese(kw):
                    keywords.append(translate_text(kw))
                    time.sleep(0.5)
                else:
                    keywords.append(kw)
            data['seo_keywords'] = keywords

        # Translate author
        if contains_chinese(data.get('author', '')):
            data['author'] = translate_text(data['author'])

        data['language'] = 'en-US'

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True

    except Exception as e:
        print(f"  File error: {e}", flush=True)
        return False

def main():
    files = sorted([f for f in os.listdir(DIRECTORY) if f.endswith('.json')])
    total = len(files)

    print(f"{'='*60}", flush=True)
    print(f"Clean Translation - {total} files", flush=True)
    print(f"{'='*60}", flush=True)

    count = 0

    for i, filename in enumerate(files, 1):
        filepath = os.path.join(DIRECTORY, filename)
        print(f"\n[{i}/{total}] {filename}", flush=True)

        if translate_file(filepath):
            count += 1
            print(f"  Completed", flush=True)

    print(f"\n{'='*60}", flush=True)
    print(f"Translated: {count}/{total}", flush=True)
    print(f"{'='*60}", flush=True)

if __name__ == '__main__':
    main()