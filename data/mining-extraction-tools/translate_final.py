#!/usr/bin/env python3
"""
Proper translation of Chinese mining JSON files to English
Uses deep_translator with proper error handling
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

def get_translator():
    """Get available translator"""
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source='zh-CN', target='en')
    except Exception:
        return None

def translate_chunk(text, translator):
    """Translate a chunk of text"""
    if not has_chinese(text):
        return text

    try:
        result = translator.translate(text)
        return result
    except Exception as e:
        print(f"    Chunk translation error: {str(e)[:50]}")
        return text

def translate_text(text, translator):
    """Translate text, splitting if too long"""
    if not has_chinese(text):
        return text

    if not translator:
        print("    No translator available")
        return text

    # Google Translate has a limit around 5000 chars
    if len(text) <= 4500:
        time.sleep(random.uniform(0.5, 1.0))
        return translate_chunk(text, translator)

    # Split at HTML section boundaries (fixed pattern without look-behind)
    # Split after closing tags
    parts = []
    remaining = text
    while len(remaining) > 4500:
        # Find a good split point - after a closing tag
        split_pos = 4500
        # Look for closing tags before the split position
        for tag in ['</p>', '</section>', '</h3>', '</h2>', '</li>', '</ul>', '</td>', '</tr>']:
            pos = remaining.rfind(tag, 0, split_pos + len(tag))
            if pos > 0 and pos + len(tag) < split_pos + 100:
                split_pos = pos + len(tag)
                break

        if split_pos < 100:
            # No good split found, force split at 4500
            split_pos = 4500

        parts.append(remaining[:split_pos])
        remaining = remaining[split_pos:]

    parts.append(remaining)

    # Translate each part
    translated_parts = []
    for i, part in enumerate(parts):
        if has_chinese(part):
            time.sleep(random.uniform(0.5, 1.5))
            translated = translate_chunk(part, translator)
            translated_parts.append(translated)
        else:
            translated_parts.append(part)

    return ''.join(translated_parts)

def translate_keywords(keywords, translator):
    """Translate SEO keywords array"""
    translated = []
    for kw in keywords:
        if has_chinese(kw):
            time.sleep(random.uniform(0.3, 0.6))
            trans = translate_chunk(kw, translator)
            translated.append(trans)
        else:
            translated.append(kw)
    return translated

def process_file(filepath, translator):
    """Process and translate a single JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if ANY field has Chinese (not just title)
    title = data.get('title', '')
    description = data.get('description', '')
    content = data.get('content', '')

    has_any_chinese = has_chinese(title) or has_chinese(description) or has_chinese(content)

    if not has_any_chinese:
        return False, 'already_english'

    print(f"  Title: {title[:50]}...")

    # Translate fields
    print(f"  Translating title...")
    data['title'] = translate_text(data['title'], translator)

    print(f"  Translating description...")
    data['description'] = translate_text(data['description'], translator)

    print(f"  Translating content...")
    data['content'] = translate_text(data['content'], translator)

    print(f"  Translating keywords...")
    data['seo_keywords'] = translate_keywords(data.get('seo_keywords', []), translator)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return True, 'success'

def main():
    # Initialize translator
    translator = get_translator()
    if not translator:
        print("ERROR: Could not initialize translator")
        return

    translated_count = 0
    skipped_count = 0
    error_count = 0

    files = sorted([f for f in os.listdir('.') if f.endswith('.json')])
    total_files = len(files)

    print(f"Processing {total_files} JSON files...")
    print("="*60)

    for i, filename in enumerate(files, 1):
        filepath = Path(filename)
        print(f"\n[{i}/{total_files}] Processing: {filename}")
        try:
            success, status = process_file(filepath, translator)
            if success:
                translated_count += 1
                print(f"  ✓ Translated")
            elif status == 'already_english':
                skipped_count += 1
                print(f"  ⊙ Already English")
            else:
                error_count += 1
                print(f"  ✗ Error: {status}")

        except Exception as e:
            error_count += 1
            print(f"  ✗ Exception: {e}")

    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"  Total translated: {translated_count}")
    print(f"  Already English (skipped): {skipped_count}")
    print(f"  Errors: {error_count}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()