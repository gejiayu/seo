#!/usr/bin/env python3
"""
Script to process all insurance-agency-tools files with Chinese content
This script will help identify patterns and prepare for batch translation
"""
import os
import json
import re

DATA_DIR = '/Users/gejiayu/owner/seo/data/insurance-agency-tools'

def has_chinese(text):
    """Check if text contains Chinese characters"""
    if not text:
        return False
    chinese_pattern = re.compile(r'[一-鿿]+')
    return bool(chinese_pattern.search(text))

def clean_keywords(keywords):
    """Clean keywords - remove extra spaces"""
    if isinstance(keywords, list):
        return [kw.strip() for kw in keywords]
    return keywords

def process_all_files():
    """Process all files and prepare translation mapping"""
    files_data = []

    for filename in sorted(os.listdir(DATA_DIR)):
        if not filename.endswith('.json'):
            continue

        filepath = os.path.join(DATA_DIR, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check if file needs translation
            needs_translation = False
            for field in ['title', 'description', 'content', 'author']:
                if field in data and has_chinese(data[field]):
                    needs_translation = True
                    break

            if needs_translation:
                # Clean seo_keywords
                if 'seo_keywords' in data:
                    data['seo_keywords'] = clean_keywords(data['seo_keywords'])

                files_data.append({
                    'filename': filename,
                    'filepath': filepath,
                    'data': data,
                    'fields_to_translate': [
                        field for field in ['title', 'description', 'content', 'author']
                        if field in data and has_chinese(data[field])
                    ]
                })

        except Exception as e:
            print(f"Error reading {filename}: {e}")

    return files_data

def main():
    files_data = process_all_files()
    print(f"Total files needing translation: {len(files_data)}")
    print("\nFiles to process:")
    for i, file_info in enumerate(files_data, 1):
        print(f"{i}. {file_info['filename']} - Fields: {file_info['fields_to_translate']}")

if __name__ == '__main__':
    main()