#!/usr/bin/env python3
"""
Translate Chinese content to English using deep_translator with retry logic
"""

import json
import re
import os
import time
from pathlib import Path

# Add the virtual environment path
import sys
sys.path.insert(0, '/Users/gejiayu/owner/seo/.venv/lib/python3.13/site-packages')

from deep_translator import GoogleTranslator

def contains_chinese(text):
    """Check if text contains Chinese characters"""
    if not text:
        return False
    chinese_pattern = re.compile(r'[一-鿿]+')
    return bool(chinese_pattern.search(text))

def translate_with_retry(text, translator, max_retries=3):
    """Translate with retry logic"""
    if not text or not contains_chinese(text):
        return text

    for attempt in range(max_retries):
        try:
            time.sleep(0.5)  # Delay to avoid rate limiting
            translated = translator.translate(text)
            return translated
        except Exception as e:
            print(f"Translation attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Longer delay before retry
            else:
                print(f"Failed to translate: {text[:50]}...")
                return text

def translate_html_content(html_content, translator):
    """Translate HTML content while preserving tags"""
    if not html_content or not contains_chinese(html_content):
        return html_content

    # Split by HTML tags
    parts = re.split(r'(<[^>]+>)', html_content)
    translated_parts = []

    for part in parts:
        if re.match(r'<[^>]+>', part):
            translated_parts.append(part)
        else:
            if contains_chinese(part):
                translated = translate_with_retry(part.strip(), translator)
                translated_parts.append(translated)
            else:
                translated_parts.append(part)

    return ''.join(translated_parts)

def translate_file(filepath, translator):
    """Translate a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if data.get('language') != 'en-US':
            return False

        if not contains_chinese(data.get('title', '')):
            return False

        print(f"\nProcessing: {filepath}")

        # Translate title
        if contains_chinese(data.get('title', '')):
            print(f"  Translating title...")
            data['title'] = translate_with_retry(data['title'], translator)

        # Translate description
        if contains_chinese(data.get('description', '')):
            print(f"  Translating description...")
            data['description'] = translate_with_retry(data['description'], translator)

        # Translate content
        if contains_chinese(data.get('content', '')):
            print(f"  Translating content...")
            data['content'] = translate_html_content(data['content'], translator)

        # Translate author
        if contains_chinese(data.get('author', '')):
            print(f"  Translating author...")
            data['author'] = translate_with_retry(data['author'], translator)

        # Save the file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"  ✓ Saved")
        return True

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Main process"""
    directory = '/Users/gejiayu/owner/seo/data/insurance-claims-processing-tools'
    translator = GoogleTranslator(source='zh-CN', target='en')

    files_to_translate = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if data.get('language') == 'en-US' and contains_chinese(data.get('title', '')):
                    files_to_translate.append(filepath)
            except:
                pass

    print(f"Found {len(files_to_translate)} files to translate")

    translated_count = 0
    for filepath in files_to_translate:
        if translate_file(filepath, translator):
            translated_count += 1

    print(f"\nTotal translated: {translated_count}/{len(files_to_translate)}")

if __name__ == '__main__':
    main()