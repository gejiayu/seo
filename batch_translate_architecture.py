#!/usr/bin/env python3
"""
Batch translator for architecture-design-tools JSON files.
Translates Chinese content to proper English using deep-translator.
"""
import json
import os
import re
import sys
from pathlib import Path
from deep_translator import GoogleTranslator

DATA_DIR = Path("/Users/gejiayu/owner/seo/data/architecture-design-tools")

def has_chinese(text):
    """Check if text contains Chinese characters."""
    return bool(re.search(r'[一-鿿]', text))

def translate_text(text, translator):
    """Translate text from Chinese to English."""
    try:
        # Split text into manageable chunks if too large
        if len(text) > 5000:
            # Split by paragraphs
            parts = text.split('</p><p>')
            translated_parts = []
            for part in parts:
                if has_chinese(part):
                    translated = translator.translate(part)
                    translated_parts.append(translated)
                else:
                    translated_parts.append(part)
            return '</p><p>'.join(translated_parts)
        else:
            if has_chinese(text):
                translated = translator.translate(text)
                return translated
            return text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def process_file(file_path, translator):
    """Process a single JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if it's an English file with Chinese content
        if data.get('language') != 'en-US':
            return False

        # Check for Chinese in content
        if not has_chinese(data.get('content', '')):
            return False

        print(f"Processing: {file_path.name}")

        # Translate content
        original_content = data['content']
        translated_content = translate_text(original_content, translator)

        # Update the data
        data['content'] = translated_content

        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Translated: {file_path.name}")
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all files."""
    try:
        translator = GoogleTranslator(source='zh-CN', target='en')
    except Exception as e:
        print(f"Error initializing translator: {e}")
        return

    files_processed = 0
    files_translated = 0

    # Get all JSON files sorted
    files = sorted(DATA_DIR.glob('*.json'))

    for file_path in files:
        files_processed += 1
        if process_file(file_path, translator):
            files_translated += 1

    print(f"\n{'='*60}")
    print(f"Total files processed: {files_processed}")
    print(f"Files translated: {files_translated}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()