#!/usr/bin/env python3
import json
import os
import re

def contains_chinese(text):
    """Check if text contains Chinese characters"""
    if not isinstance(text, str):
        return False
    # Chinese character range: 一-鿿 (CJK Unified Ideographs)
    chinese_pattern = re.compile(r'[一-鿿]')
    return bool(chinese_pattern.search(text))

def check_json_file(filepath):
    """Check if JSON file contains Chinese content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check all relevant fields
        fields_to_check = ['title', 'description', 'content']
        has_chinese = False

        for field in fields_to_check:
            if field in data:
                if contains_chinese(data[field]):
                    has_chinese = True
                    break

        # Also check if language field exists and is not en-US
        language_issue = False
        if 'language' not in data:
            language_issue = True
        elif data.get('language') != 'en-US':
            language_issue = True

        return has_chinese, language_issue, data
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False, False, None

def main():
    directory = '/Users/gejiayu/owner/seo/data/massage-spa-wellness-tools/'

    # Get all files sorted
    all_files = sorted([f for f in os.listdir(directory) if f.endswith('.json')])

    # Select files 21-40 (indices 20-39 in 0-based indexing)
    target_files = all_files[20:40]

    print(f"Checking files 21-40 ({len(target_files)} files):")
    print("=" * 80)

    chinese_files = []
    missing_language_files = []

    for i, filename in enumerate(target_files, start=21):
        filepath = os.path.join(directory, filename)
        has_chinese, language_issue, data = check_json_file(filepath)

        if has_chinese:
            chinese_files.append((i, filename, filepath, data))
            print(f"[File {i}] CHINESE CONTENT: {filename}")
        elif language_issue:
            missing_language_files.append((i, filename, filepath))
            print(f"[File {i}] MISSING/WRONG LANGUAGE: {filename}")
        else:
            print(f"[File {i}] OK: {filename}")

    print("\n" + "=" * 80)
    print(f"SUMMARY:")
    print(f"  Files with Chinese content: {len(chinese_files)}")
    print(f"  Files with missing/wrong language field: {len(missing_language_files)}")

    if chinese_files:
        print("\nFiles requiring translation:")
        for i, filename, filepath, data in chinese_files:
            print(f"  {i}. {filename}")
            if data:
                print(f"     Title: {data.get('title', 'N/A')[:50]}...")

    return chinese_files, missing_language_files

if __name__ == '__main__':
    main()