#!/usr/bin/env python3
"""
Script to identify files with Chinese content in insurance-agency-tools directory
"""
import os
import json
import re

def has_chinese(text):
    """Check if text contains Chinese characters"""
    if not text:
        return False
    chinese_pattern = re.compile(r'[一-鿿]+')
    return bool(chinese_pattern.search(text))

def scan_directory():
    """Scan all JSON files and identify those with Chinese content"""
    dir_path = '/Users/gejiayu/owner/seo/data/insurance-agency-tools'
    chinese_files = []

    for filename in os.listdir(dir_path):
        if filename.endswith('.json'):
            filepath = os.path.join(dir_path, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Check title, description, content, author for Chinese
                has_chinese_content = False
                fields_to_check = ['title', 'description', 'content', 'author']

                for field in fields_to_check:
                    if field in data and has_chinese(data[field]):
                        has_chinese_content = True
                        break

                if has_chinese_content:
                    chinese_files.append(filename)

            except Exception as e:
                print(f"Error reading {filename}: {e}")

    return chinese_files

if __name__ == '__main__':
    chinese_files = scan_directory()
    print(f"Total files with Chinese content: {len(chinese_files)}")
    print("\nFiles list:")
    for f in chinese_files:
        print(f)