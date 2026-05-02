#!/usr/bin/env python3
"""
Translate Chinese content to English in massage-spa-wellness-tools JSON files
using Google Translator for accurate translation.
"""
import os
import json
import re
import time
from deep_translator import GoogleTranslator

def contains_chinese(text):
    """Check if text contains Chinese characters."""
    if not text:
        return False
    return bool(re.search('[一-鿿]', str(text)))

def translate_text(text, translator):
    """Translate Chinese text to English using Google Translator."""
    if not text or not contains_chinese(text):
        return text

    # Split text into chunks to avoid Google Translator limits
    max_chunk_size = 4500  # Google Translator has a ~5000 char limit

    if len(text) <= max_chunk_size:
        try:
            result = translator.translate(text)
            return result
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    # Split into chunks and translate each
    chunks = []
    while len(text) > max_chunk_size:
        # Find a good split point (prefer end of sentence)
        split_point = max_chunk_size
        for i in range(max_chunk_size - 100, max_chunk_size):
            if text[i] in '.!?。！？':
                split_point = i + 1
                break
        chunks.append(text[:split_point])
        text = text[split_point:]
    chunks.append(text)

    # Translate each chunk
    translated_chunks = []
    for chunk in chunks:
        try:
            translated = translator.translate(chunk)
            translated_chunks.append(translated)
            time.sleep(0.1)  # Small delay to avoid rate limiting
        except Exception as e:
            print(f"Translation error for chunk: {e}")
            translated_chunks.append(chunk)

    return ''.join(translated_chunks)

def translate_json_file(filepath, translator):
    """Translate Chinese content in JSON file to English."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Translate fields
    if 'title' in data and contains_chinese(data['title']):
        print(f"  Translating title...")
        data['title'] = translate_text(data['title'], translator)

    if 'description' in data and contains_chinese(data['description']):
        print(f"  Translating description...")
        data['description'] = translate_text(data['description'], translator)

    if 'content' in data and contains_chinese(data['content']):
        print(f"  Translating content...")
        data['content'] = translate_text(data['content'], translator)

    if 'author' in data and contains_chinese(data['author']):
        print(f"  Translating author...")
        data['author'] = translate_text(data['author'], translator)

    if 'seo_keywords' in data:
        translated_keywords = []
        for keyword in data['seo_keywords']:
            if contains_chinese(keyword):
                print(f"  Translating keyword: {keyword}")
                translated_keywords.append(translate_text(keyword, translator))
            else:
                translated_keywords.append(keyword)
        data['seo_keywords'] = translated_keywords

    # Ensure language is en-US
    data['language'] = 'en-US'

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return filepath

def main():
    """Process all files in the directory."""
    directory = '/Users/gejiayu/owner/seo/data/massage-spa-wellness-tools'

    # Initialize translator
    translator = GoogleTranslator(source='zh-CN', target='en')

    # Get list of files to translate
    files_to_translate = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    has_chinese = False
                    for field in ['title', 'description', 'content', 'author', 'seo_keywords']:
                        if field in data:
                            if field == 'seo_keywords':
                                for keyword in data[field]:
                                    if contains_chinese(keyword):
                                        has_chinese = True
                                        break
                            else:
                                if contains_chinese(data[field]):
                                    has_chinese = True
                                    break
                    if has_chinese:
                        files_to_translate.append(filepath)
            except Exception as e:
                print(f'Error reading {filename}: {e}')

    # Translate files
    print(f'Total files to translate: {len(files_to_translate)}')

    for i, filepath in enumerate(files_to_translate):
        try:
            filename = os.path.basename(filepath)
            print(f"\n[{i+1}/{len(files_to_translate)}] Processing: {filename}")
            translate_json_file(filepath, translator)
            print(f"  Completed!")
            time.sleep(0.5)  # Delay between files to avoid rate limiting
        except Exception as e:
            print(f'Error translating {filepath}: {e}')
            continue

    print('\nTranslation complete!')

if __name__ == '__main__':
    main()