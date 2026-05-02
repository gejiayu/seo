#!/usr/bin/env python3
"""
Translate Chinese JSON files to English using deep-translator library.
"""

import json
import re
import time
from pathlib import Path
from deep_translator import GoogleTranslator

# Initialize translator
translator = GoogleTranslator(source='zh-CN', target='en')

def translate_text(text, max_retries=3):
    """Translate text using Google Translator with retries."""
    if not text or not isinstance(text, str):
        return text

    # Check if text is already in English (no Chinese characters)
    if not re.search('[一-鿿]', text):
        return text

    for attempt in range(max_retries):
        try:
            # Limit text length to avoid API limits
            if len(text) > 5000:
                # Split into chunks
                chunks = []
                sentences = re.split(r'[。！？\n]', text)
                current_chunk = ""
                for sentence in sentences:
                    if len(current_chunk + sentence) < 4500:
                        current_chunk += sentence + " "
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence + " "
                if current_chunk:
                    chunks.append(current_chunk.strip())

                # Translate each chunk
                translated_chunks = []
                for chunk in chunks:
                    try:
                        translated = translator.translate(chunk)
                        translated_chunks.append(translated)
                        time.sleep(0.1)  # Small delay to avoid rate limiting
                    except Exception as e:
                        print(f"Error translating chunk: {e}")
                        translated_chunks.append(chunk)

                return ' '.join(translated_chunks)
            else:
                translated = translator.translate(text)
                return translated
        except Exception as e:
            print(f"Translation error (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                print(f"Failed to translate: {text[:50]}...")
                return text

    return text

def translate_html_content(content):
    """Translate HTML content while preserving structure."""
    if not content or not isinstance(content, str):
        return content

    # Check if already in English
    if not re.search('[一-鿿]', content):
        return content

    # Extract text from HTML tags and translate
    # Pattern to match text between HTML tags
    def translate_tag_content(match):
        tag = match.group(1)
        text = match.group(2)
        translated_text = translate_text(text)
        return f"<{tag}>{translated_text}</{tag}>"

    # Translate content in various tags
    content = re.sub(r'<(h[1-6])>([^<]+)</h[1-6]>', translate_tag_content, content)
    content = re.sub(r'<(p)>([^<]+)</p>', translate_tag_content, content)
    content = re.sub(r'<(li)>([^<]+)</li>', translate_tag_content, content)
    content = re.sub(r'<(th)>([^<]+)</th>', translate_tag_content, content)
    content = re.sub(r'<(td)>([^<]+)</td>', translate_tag_content, content)
    content = re.sub(r'<(strong)>([^<]+)</strong>', translate_tag_content, content)

    # Translate title and other standalone text
    content = re.sub(r'<(title)>([^<]+)</title>', translate_tag_content, content)

    return content

def translate_pros_cons(pros_cons):
    """Translate pros and cons arrays."""
    if not isinstance(pros_cons, list):
        return pros_cons

    translated = []
    for item in pros_cons:
        if isinstance(item, dict):
            new_item = {}
            for key, value in item.items():
                if key == 'tool':
                    new_item[key] = value  # Keep tool name as is
                elif isinstance(value, list):
                    translated_list = []
                    for v in value:
                        translated_v = translate_text(v)
                        translated_list.append(translated_v)
                        time.sleep(0.05)  # Small delay
                    new_item[key] = translated_list
                else:
                    new_item[key] = translate_text(value)
            translated.append(new_item)
        else:
            translated.append(item)

    return translated

def translate_json_file(filepath):
    """Translate a JSON file from Chinese to English."""
    print(f"\nProcessing: {filepath.name}")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Translate title
    if 'title' in data and re.search('[一-鿿]', data['title']):
        print(f"  Translating title...")
        data['title'] = translate_text(data['title'])
        time.sleep(0.2)

    # Translate description
    if 'description' in data and re.search('[一-鿿]', data['description']):
        print(f"  Translating description...")
        data['description'] = translate_text(data['description'])
        time.sleep(0.2)

    # Translate content
    if 'content' in data and re.search('[一-鿿]', data['content']):
        print(f"  Translating content...")
        data['content'] = translate_html_content(data['content'])
        time.sleep(0.5)

    # Translate pros_and_cons
    if 'pros_and_cons' in data:
        print(f"  Translating pros_and_cons...")
        data['pros_and_cons'] = translate_pros_cons(data['pros_and_cons'])

    # Keep seo_keywords as is (they're already in English)
    # Keep language as is (already "en-US")
    # Keep other metadata fields as is

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  ✓ Completed: {filepath.name}")
    return filepath

def main():
    """Process all files in the transportation-fleet-tools directory."""
    base_dir = Path('/Users/gejiayu/owner/seo/data/transportation-fleet-tools')

    count = 0
    files_to_translate = []

    # First, collect all files that need translation
    for filepath in sorted(base_dir.glob('*.json')):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        title = data.get('title', '')
        language = data.get('language', '')

        # Check if file has Chinese content and needs translation
        # Translate if: language is en-US, empty, or not set
        has_chinese = re.search('[一-鿿]', title)
        needs_translation = has_chinese and (language == 'en-US' or not language or language == '')

        if needs_translation:
            files_to_translate.append(filepath)

    print(f"Found {len(files_to_translate)} files to translate")
    print("=" * 60)

    # Translate files
    for filepath in files_to_translate:
        try:
            translate_json_file(filepath)
            count += 1
            time.sleep(1)  # Delay between files to avoid rate limiting
        except Exception as e:
            print(f"Error processing {filepath.name}: {e}")
            continue

    print("\n" + "=" * 60)
    print(f"Total files successfully translated: {count}")

if __name__ == '__main__':
    main()