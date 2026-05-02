#!/usr/bin/env python3
"""
Proper translation of Chinese mining JSON files to English
Uses multiple translation backends with retry logic
"""
import json
import re
import os
import time
import random
from pathlib import Path

def has_chinese(text):
    """Check if text contains Chinese characters"""
    if not text:
        return False
    return bool(re.search(r'[一-鿿]', text))

def translate_with_retry(text, max_retries=3):
    """Translate text using available translators with retry logic"""
    if not has_chinese(text):
        return text

    # Try different translators
    translators = []

    # Try to import different translators
    try:
        from deep_translator import GoogleTranslator
        translators.append(('Google', GoogleTranslator(source='zh-CN', target='en')))
    except Exception as e:
        pass  # Google may fail, skip silently

    try:
        from deep_translator import MyMemoryTranslator
        translators.append(('MyMemory', MyMemoryTranslator(source='zh-CN', target='en')))
    except Exception as e:
        pass  # MyMemory may fail, skip silently

    if not translators:
        print("  No translators available!")
        return text

    # For very long text, split into chunks
    if len(text) > 4500:
        # Split at HTML markers to preserve structure
        parts = re.split(r'(?<=</p>|</section>|</h3>|</h2>|</li>|</ul>|</td>|</tr>)', text)
        translated_parts = []
        for part in parts:
            if has_chinese(part):
                translated_parts.append(translate_with_retry(part, max_retries))
            else:
                translated_parts.append(part)
        return ''.join(translated_parts)

    for name, translator in translators:
        for attempt in range(max_retries):
            try:
                # Add small delay to avoid rate limiting
                time.sleep(random.uniform(0.3, 0.8))
                result = translator.translate(text)
                if result and not has_chinese(result):
                    return result
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(1 + attempt)
                    continue
                print(f"  {name} failed after {max_retries} attempts: {str(e)[:50]}")

    # If all translators fail, return original
    print(f"  All translators failed for text of length {len(text)}")
    return text

def translate_keywords(keywords):
    """Translate SEO keywords array"""
    translated = []
    for kw in keywords:
        if has_chinese(kw):
            trans = translate_with_retry(kw)
            translated.append(trans)
        else:
            translated.append(kw)
    return translated

def process_file(filepath):
    """Process and translate a single JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if already English
    if not has_chinese(data.get('title', '')):
        return False, 'already_english'

    print(f"  Translating: {filepath.name}")

    # Translate fields
    data['title'] = translate_with_retry(data['title'])
    data['description'] = translate_with_retry(data['description'])
    data['content'] = translate_with_retry(data['content'])
    data['seo_keywords'] = translate_keywords(data['seo_keywords'])

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return True, 'success'

def main():
    translated_count = 0
    skipped_count = 0
    error_count = 0

    files = sorted([f for f in os.listdir('.') if f.endswith('.json')])
    total_files = len(files)

    print(f"Processing {total_files} JSON files...")
    print("="*60)

    for i, filename in enumerate(files, 1):
        filepath = Path(filename)
        try:
            success, status = process_file(filepath)
            if success:
                translated_count += 1
                print(f"[{i}/{total_files}] ✓ {filename}")
            elif status == 'already_english':
                skipped_count += 1
                print(f"[{i}/{total_files}] ⊙ {filename} (already English)")
            else:
                error_count += 1
                print(f"[{i}/{total_files}] ✗ {filename} - {status}")

        except Exception as e:
            error_count += 1
            print(f"[{i}/{total_files}] ✗ {filename} - {e}")

    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"  Total translated: {translated_count}")
    print(f"  Already English (skipped): {skipped_count}")
    print(f"  Errors: {error_count}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()