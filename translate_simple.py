#!/usr/bin/env python3
"""
Translate Chinese content to English in JSON files using direct Google Translate API
"""

import json
import re
import os
import urllib.request
import urllib.parse
import html as html_module
import time
from pathlib import Path

def contains_chinese(text):
    """Check if text contains Chinese characters"""
    if not text:
        return False
    chinese_pattern = re.compile(r'[一-鿿]+')
    return bool(chinese_pattern.search(text))

def translate_single(text, target_lang='en', source_lang='zh-CN'):
    """Translate a single piece of text using Google Translate API"""
    if not text or not contains_chinese(text):
        return text

    try:
        time.sleep(0.05)  # Small delay to avoid rate limiting
        text_encoded = urllib.parse.quote(text)
        url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={text_encoded}'

        request = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )

        response = urllib.request.urlopen(request, timeout=30)
        result = response.read().decode('utf-8')

        # Parse response
        translated_parts = []
        try:
            import ast
            data = ast.literal_eval(result)
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                for item in data[0]:
                    if isinstance(item, list) and len(item) > 0 and item[0]:
                        translated_parts.append(str(item[0]))
        except:
            pass

        if translated_parts:
            translated_text = ''.join(translated_parts)
            return html_module.unescape(translated_text)
        else:
            print(f"Translation failed for text: {text[:50]}...")
            return text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def translate_html_content(html_content):
    """Translate text content within HTML tags while preserving structure"""
    if not html_content or not contains_chinese(html_content):
        return html_content

    # Split by HTML tags and translate only the text parts
    parts = re.split(r'(<[^>]+>)', html_content)
    translated_parts = []

    for part in parts:
        # If it's an HTML tag, keep it as is
        if re.match(r'<[^>]+>', part):
            translated_parts.append(part)
        else:
            # Translate the text content
            if contains_chinese(part):
                translated = translate_single(part.strip())
                translated_parts.append(translated)
            else:
                translated_parts.append(part)

    return ''.join(translated_parts)

def process_file(filepath):
    """Process a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        needs_update = False

        # Translate title
        if contains_chinese(data.get('title', '')):
            print(f"Translating title in {filepath}")
            data['title'] = translate_single(data['title'])
            needs_update = True

        # Translate description
        if contains_chinese(data.get('description', '')):
            print(f"Translating description in {filepath}")
            data['description'] = translate_single(data['description'])
            needs_update = True

        # Translate content (HTML)
        if contains_chinese(data.get('content', '')):
            print(f"Translating content in {filepath}")
            data['content'] = translate_html_content(data['content'])
            needs_update = True

        # Translate author
        if contains_chinese(data.get('author', '')):
            print(f"Translating author in {filepath}")
            data['author'] = translate_single(data['author'])
            needs_update = True

        if needs_update:
            # Save without HTML escaping
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✓ Saved: {filepath}")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main translation process"""
    directory = '/Users/gejiayu/owner/seo/data/insurance-claims-processing-tools'

    files_to_fix = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if data.get('language') == 'en-US':
                    if contains_chinese(data.get('title', '')):
                        files_to_fix.append(filepath)
            except Exception as e:
                pass

    print(f"Found {len(files_to_fix)} files to translate")

    # Process each file
    fixed_count = 0
    for filepath in files_to_fix:
        if process_file(filepath):
            fixed_count += 1

    print(f"\nTotal files translated: {fixed_count}")

if __name__ == '__main__':
    main()