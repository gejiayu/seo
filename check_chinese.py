#!/usr/bin/env python3
"""
Script to help identify Chinese content in JSON files for translation
"""
import json
import os
import re

def has_chinese(text):
    """Check if text contains Chinese characters"""
    if not isinstance(text, str):
        return False
    chinese_pattern = re.compile(r'[一-鿿]+')
    return bool(chinese_pattern.search(text))

def check_file(filepath):
    """Check if JSON file has Chinese content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        fields_with_chinese = []
        for field in ['title', 'description', 'content', 'author', 'seo_keywords']:
            if field in data:
                if field == 'seo_keywords':
                    if isinstance(data[field], list):
                        for kw in data[field]:
                            if has_chinese(kw):
                                fields_with_chinese.append(f"{field}: {kw}")
                else:
                    if has_chinese(data[field]):
                        fields_with_chinese.append(field)

        return len(fields_with_chinese) > 0
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

def main():
    directory = "/Users/gejiayu/owner/seo/data/travel-hospitality-tools"
    files_with_chinese = []

    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            if check_file(filepath):
                files_with_chinese.append(filename)

    print(f"Total files with Chinese content: {len(files_with_chinese)}")
    print("\nFiles to translate:")
    for f in files_with_chinese:
        print(f)

if __name__ == "__main__":
    main()