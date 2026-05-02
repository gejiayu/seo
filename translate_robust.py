#!/usr/bin/env python3
"""
Robust translation script for machinery-heavy-equipment-rental-tools JSON files.
Translates Chinese content to English using Google Translate API.
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

# Constants
DIRECTORY = '/Users/gejiayu/owner/seo/data/machinery-heavy-equipment-rental-tools'
MAX_RETRIES = 3
DELAY_BETWEEN_REQUESTS = 0.5

def contains_chinese(text):
    """Check if text contains Chinese characters"""
    if not isinstance(text, str):
        return False
    # Match Chinese characters including common CJK ranges
    return bool(re.search(r'[一-龥]', text))

def translate_google_api(text, retry_count=0):
    """Translate text using Google Translate unofficial API"""
    if not text or not contains_chinese(text):
        return text

    try:
        # Encode the text
        encoded_text = urllib.parse.quote(text, safe='')

        # Google Translate API endpoint
        url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-CN&tl=en&dt=t&q={encoded_text}'

        # Create request with headers
        request = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
        )

        # Make request with timeout
        response = urllib.request.urlopen(request, timeout=60)
        result = response.read().decode('utf-8')

        # Parse the response
        # Response format: [[["translated text","original text",null,null,10],...],null,"en",...]
        translated_parts = []

        # Parse the nested JSON-like structure
        # Find all translated segments
        import ast
        try:
            data = ast.literal_eval(result)
            if isinstance(data, list) and len(data) > 0:
                first = data[0]
                if isinstance(first, list):
                    for item in first:
                        if isinstance(item, list) and len(item) > 0:
                            translated_text = item[0]
                            if translated_text:
                                translated_parts.append(str(translated_text))
        except Exception as parse_error:
            # Fallback: try regex extraction
            matches = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', result)
            if matches:
                # Take the first significant match
                for m in matches:
                    if len(m) > 10 and not m.startswith('zh-CN'):
                        translated_parts.append(m)
                        break

        if translated_parts:
            full_translation = ''.join(translated_parts)
            # Unescape HTML entities
            return html.unescape(full_translation)

        print(f"  Warning: Could not parse translation response", flush=True)
        return text

    except urllib.error.HTTPError as e:
        if retry_count < MAX_RETRIES:
            print(f"  HTTP error {e.code}, retrying... (attempt {retry_count + 1})", flush=True)
            time.sleep(2)
            return translate_google_api(text, retry_count + 1)
        print(f"  HTTP error {e.code}, max retries exceeded", flush=True)
        return text

    except urllib.error.URLError as e:
        if retry_count < MAX_RETRIES:
            print(f"  URL error, retrying... (attempt {retry_count + 1})", flush=True)
            time.sleep(2)
            return translate_google_api(text, retry_count + 1)
        print(f"  URL error: {e.reason}", flush=True)
        return text

    except Exception as e:
        print(f"  Translation error: {type(e).__name__}: {e}", flush=True)
        return text

def translate_content_chunked(content):
    """Translate large HTML content by splitting into smaller chunks"""
    if not contains_chinese(content):
        return content

    # Split by <section> tags for better context preservation
    if '<section>' in content:
        parts = content.split('<section>')
        translated_parts = []

        for i, part in enumerate(parts):
            if i == 0:
                # First part (before first <section>)
                if contains_chinese(part):
                    translated = translate_google_api(part)
                    time.sleep(DELAY_BETWEEN_REQUESTS)
                    translated_parts.append(translated)
                else:
                    translated_parts.append(part)
            else:
                # Add <section> back and translate the content
                section_content = '<section>' + part
                if contains_chinese(section_content):
                    translated = translate_google_api(section_content)
                    time.sleep(DELAY_BETWEEN_REQUESTS)
                    translated_parts.append(translated)
                else:
                    translated_parts.append(section_content)

        return ''.join(translated_parts)

    # For content without sections, translate directly but limit size
    if len(content) > 5000:
        # Split into paragraphs
        paragraphs = re.split(r'</p>', content)
        translated_paras = []

        for para in paragraphs:
            if para.strip():
                if contains_chinese(para):
                    translated = translate_google_api(para)
                    time.sleep(DELAY_BETWEEN_REQUESTS)
                    translated_paras.append(translated)
                else:
                    translated_paras.append(para)

        return '</p>'.join(translated_paras)

    # Small content - translate directly
    return translate_google_api(content)

def translate_keywords(keywords):
    """Translate keywords array"""
    if not isinstance(keywords, list):
        return keywords

    translated = []
    for kw in keywords:
        if contains_chinese(kw):
            trans_kw = translate_google_api(kw)
            time.sleep(DELAY_BETWEEN_REQUESTS)
            translated.append(trans_kw)
        else:
            translated.append(kw)

    return translated

def translate_file(filepath):
    """Translate a single JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if file has Chinese content
        fields_to_check = ['title', 'description', 'content', 'author']
        has_chinese = any(contains_chinese(data.get(field, '')) for field in fields_to_check)

        if not has_chinese:
            return False, "No Chinese content"

        # Translate each field
        if contains_chinese(data.get('title', '')):
            data['title'] = translate_google_api(data['title'])
            time.sleep(DELAY_BETWEEN_REQUESTS)

        if contains_chinese(data.get('description', '')):
            data['description'] = translate_google_api(data['description'])
            time.sleep(DELAY_BETWEEN_REQUESTS)

        if contains_chinese(data.get('content', '')):
            data['content'] = translate_content_chunked(data['content'])

        if isinstance(data.get('seo_keywords', []), list):
            data['seo_keywords'] = translate_keywords(data['seo_keywords'])

        if contains_chinese(data.get('author', '')):
            data['author'] = translate_google_api(data['author'])

        # Keep language as en-US
        data['language'] = 'en-US'

        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True, "Success"

    except json.JSONDecodeError as e:
        return False, f"JSON error: {e}"
    except Exception as e:
        return False, f"Error: {type(e).__name__}: {e}"

def main():
    # Get all JSON files
    files = sorted([f for f in os.listdir(DIRECTORY) if f.endswith('.json')])
    total = len(files)

    print(f"{'='*60}", flush=True)
    print(f"Translation Script for Machinery Equipment Rental Tools", flush=True)
    print(f"Total files to process: {total}", flush=True)
    print(f"{'='*60}", flush=True)

    translated_count = 0
    skipped_count = 0
    error_count = 0

    for i, filename in enumerate(files, 1):
        filepath = os.path.join(DIRECTORY, filename)

        print(f"\n[{i}/{total}] {filename}", flush=True)

        success, message = translate_file(filepath)

        if success:
            translated_count += 1
            print(f"  -> Translated successfully", flush=True)
        elif "No Chinese" in message:
            skipped_count += 1
            print(f"  -> Skipped: {message}", flush=True)
        else:
            error_count += 1
            print(f"  -> Error: {message}", flush=True)

    print(f"\n{'='*60}", flush=True)
    print(f"Translation Complete", flush=True)
    print(f"{'='*60}", flush=True)
    print(f"  Translated: {translated_count}", flush=True)
    print(f"  Skipped:    {skipped_count}", flush=True)
    print(f"  Errors:     {error_count}", flush=True)
    print(f"  Total:      {total}", flush=True)
    print(f"{'='*60}", flush=True)

if __name__ == '__main__':
    main()