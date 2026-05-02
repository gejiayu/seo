#!/usr/bin/env python3
"""
Optimized translation script for machinery-heavy-equipment-rental-tools JSON files.
Uses smaller chunks and concurrent processing for faster translation.
"""

import os
import sys
import json
import re
import time
import html
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Constants
DIRECTORY = '/Users/gejiayu/owner/seo/data/machinery-heavy-equipment-rental-tools'
CHUNK_SIZE = 2000  # Characters per chunk for translation
MAX_WORKERS = 3    # Number of concurrent translation workers
DELAY = 0.3        # Delay between requests to avoid rate limiting

def contains_chinese(text):
    """Check if text contains Chinese characters"""
    if not isinstance(text, str):
        return False
    return bool(re.search(r'[一-鿿]', text))

def translate_chunk(text, retry=3):
    """Translate a single chunk using Google Translate unofficial API"""
    if not text or not contains_chinese(text):
        return text

    for attempt in range(retry):
        try:
            # Encode text
            text_encoded = urllib.parse.quote(text)

            # Google Translate endpoint
            url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-CN&tl=en&dt=t&q={text_encoded}'

            request = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )

            response = urllib.request.urlopen(request, timeout=30)
            result = response.read().decode('utf-8')

            # Parse response - format: [[["translated","original",null,null,10],...],...]
            translated_parts = []

            # Extract translated text from response
            # The response is a nested list where the first element contains translation segments
            import ast
            try:
                data = ast.literal_eval(result)
                if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                    for item in data[0]:
                        if isinstance(item, list) and len(item) > 0 and item[0]:
                            translated_parts.append(str(item[0]))
            except:
                # Fallback: extract first quoted string after [[[
                match = re.search(r'\[\[\["([^"]+)"', result)
                if match:
                    translated_parts.append(match.group(1))

            if translated_parts:
                return html.unescape(''.join(translated_parts))

            return text

        except Exception as e:
            if attempt < retry - 1:
                time.sleep(1)
            else:
                print(f"Translation failed after {retry} attempts: {e}", flush=True)
                return text

    return text

def translate_text(text):
    """Translate text, splitting into chunks for large content"""
    if not contains_chinese(text):
        return text

    # For small text, translate directly
    if len(text) <= CHUNK_SIZE:
        result = translate_chunk(text)
        time.sleep(DELAY)
        return result

    # For large content, split by paragraphs/sections
    # Try to split by HTML sections first
    if '<section>' in text:
        sections = text.split('<section>')
        translated_sections = []
        for i, section in enumerate(sections):
            if section.strip():
                if contains_chinese(section):
                    translated = translate_chunk(section.strip())
                    translated_sections.append(translated)
                    time.sleep(DELAY)
                else:
                    translated_sections.append(section)
        return '<section>' + '<section>'.join(translated_sections)

    # Otherwise split by paragraph
    paragraphs = text.split('</p>')
    translated_paragraphs = []
    for para in paragraphs:
        if para.strip():
            if contains_chinese(para):
                translated = translate_chunk(para.strip())
                translated_paragraphs.append(translated)
                time.sleep(DELAY)
            else:
                translated_paragraphs.append(para)
    return '</p>'.join(translated_paragraphs)

def translate_keywords(keywords):
    """Translate keywords array"""
    if not isinstance(keywords, list):
        return keywords

    translated = []
    for kw in keywords:
        if contains_chinese(kw):
            translated_kw = translate_chunk(kw)
            translated.append(translated_kw)
            time.sleep(DELAY)
        else:
            translated.append(kw)

    return translated

def translate_file(filepath):
    """Translate a JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if needs translation
    needs_translation = False
    for field in ['title', 'description', 'content', 'author']:
        if contains_chinese(data.get(field, '')):
            needs_translation = True
            break

    if not needs_translation:
        return False

    filename = os.path.basename(filepath)
    print(f"  Translating fields...", flush=True)

    # Translate each field
    if contains_chinese(data.get('title', '')):
        data['title'] = translate_text(data['title'])

    if contains_chinese(data.get('description', '')):
        data['description'] = translate_text(data['description'])

    if contains_chinese(data.get('content', '')):
        data['content'] = translate_text(data['content'])

    if isinstance(data.get('seo_keywords', []), list):
        data['seo_keywords'] = translate_keywords(data['seo_keywords'])

    if contains_chinese(data.get('author', '')):
        data['author'] = translate_text(data['author'])

    # Keep language as en-US
    data['language'] = 'en-US'

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return True

def main():
    files = sorted([f for f in os.listdir(DIRECTORY) if f.endswith('.json')])
    total = len(files)

    print(f"Starting translation of {total} files...", flush=True)
    print(f"Using chunk size: {CHUNK_SIZE}, max workers: {MAX_WORKERS}", flush=True)

    count = 0

    for i, filename in enumerate(files, 1):
        filepath = os.path.join(DIRECTORY, filename)
        print(f"[{i}/{total}] {filename}", flush=True)

        try:
            if translate_file(filepath):
                count += 1
                print(f"  Done!", flush=True)
            else:
                print(f"  Skipped (no Chinese)", flush=True)
        except Exception as e:
            print(f"  Error: {e}", flush=True)

    print(f"\n{'='*50}", flush=True)
    print(f"Total files translated: {count}/{total}", flush=True)
    print(f"{'='*50}", flush=True)

if __name__ == '__main__':
    main()