#!/usr/bin/env python3
"""
Translate Chinese content to English in architecture-design-tools JSON files.
"""
import json
import os
import re
from pathlib import Path

# Directory containing JSON files
DATA_DIR = Path("/Users/gejiayu/owner/seo/data/architecture-design-tools")

def has_chinese(text):
    """Check if text contains Chinese characters."""
    return bool(re.search(r'[一-鿿]', text))

def is_english_file(file_path):
    """Check if file is marked as English language."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('language') == 'en-US'
    except:
        return False

def translate_content(content):
    """
    Translate Chinese content to English.
    This is a placeholder function - actual translation will need to be done
    by a translation service or manually.
    """
    # For now, return the original content
    # This will be replaced with actual translation logic
    return content

def process_file(file_path):
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

        # Translate content
        translated_content = translate_content(data['content'])

        # Update the data
        data['content'] = translated_content

        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all files."""
    files_processed = 0
    files_translated = 0

    for file_path in DATA_DIR.glob('*.json'):
        files_processed += 1
        if process_file(file_path):
            files_translated += 1
            print(f"Translated: {file_path.name}")

    print(f"\nTotal files processed: {files_processed}")
    print(f"Files translated: {files_translated}")

if __name__ == '__main__':
    main()