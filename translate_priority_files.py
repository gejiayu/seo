#!/usr/bin/env python3
"""
Translate remaining Chinese content in priority files using Google Translator.
"""
import os
import json
import re
import time
from deep_translator import GoogleTranslator

PRIORITY_FILES = [
    "wellness-compliance-management-system-2026.json",
    "spa-interior-design-system-2026.json",
    "massage-spa-management-software-guide-2026.json",
    "spa-booking-system-guide-2026.json",
    "spa-location-analysis-system-2026.json",
    "wellness-crm-system-guide-2026.json",
    "spa-membership-management-system-2026.json",
    "spa-marketing-automation-tools-2026.json",
    "wellness-data-analytics-platform-2026.json",
    "massage-technician-resignation-management-system-2026.json",
]

def contains_chinese(text):
    """Check if text contains Chinese characters."""
    if not text:
        return False
    return bool(re.search('[一-鿿]', str(text)))

def translate_text(text, translator):
    """Translate Chinese text to English using Google Translator."""
    if not text or not contains_chinese(text):
        return text

    # For content field, split into smaller chunks for better translation
    if len(text) > 3000:
        # Split by HTML tags and paragraphs
        parts = re.split(r'(<[^>]+>|</[^>]+>)', text)
        translated_parts = []
        for part in parts:
            if part and contains_chinese(part):
                try:
                    translated = translator.translate(part)
                    translated_parts.append(translated)
                    time.sleep(0.05)
                except Exception as e:
                    translated_parts.append(part)
            else:
                translated_parts.append(part)
        return ''.join(translated_parts)

    try:
        result = translator.translate(text)
        return result
    except Exception as e:
        print(f"  Translation error: {e}")
        return text

def main():
    directory = '/Users/gejiayu/owner/seo/data/massage-spa-wellness-tools'
    translator = GoogleTranslator(source='zh-CN', target='en')

    print(f'Translating {len(PRIORITY_FILES)} priority files...')

    for i, filename in enumerate(PRIORITY_FILES):
        filepath = os.path.join(directory, filename)
        print(f'\n[{i+1}/{len(PRIORITY_FILES)}] {filename}')

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Translate content (the largest field with most Chinese)
            if 'content' in data and contains_chinese(data['content']):
                print('  Translating content...')
                data['content'] = translate_text(data['content'], translator)

            # Ensure language is en-US
            data['language'] = 'en-US'

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print('  Completed!')
            time.sleep(0.2)

        except Exception as e:
            print(f'  Error: {e}')
            continue

    print('\nPriority files translation complete!')

if __name__ == '__main__':
    main()