#!/usr/bin/env python3
"""
Script to identify and fix Chinese files in the boat-marine-rental-tools directory.
Processes files 1-13 only.
"""

import json
import os
import re
from pathlib import Path

# Directory path
data_dir = Path("/Users/gejiayu/owner/seo/data/boat-marine-rental-tools")

# Get all JSON files sorted alphabetically
all_files = sorted([f for f in data_dir.glob("*.json")])

# Process only first 13 files
files_to_process = all_files[:13]

print(f"Total files in directory: {len(all_files)}")
print(f"Processing first {len(files_to_process)} files:")
print("=" * 80)

# Function to detect Chinese characters
def has_chinese(text):
    """Check if text contains Chinese characters."""
    chinese_pattern = re.compile(r'[一-鿿]+')
    return bool(chinese_pattern.search(text))

# Function to check if file contains Chinese content
def is_chinese_file(filepath):
    """Check if JSON file contains Chinese content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check all fields for Chinese characters
        fields_to_check = ['title', 'description', 'content']
        for field in fields_to_check:
            if field in data and isinstance(data[field], str):
                if has_chinese(data[field]):
                    return True

        # Check seo_keywords array
        if 'seo_keywords' in data and isinstance(data['seo_keywords'], list):
            for keyword in data['seo_keywords']:
                if isinstance(keyword, str) and has_chinese(keyword):
                    return True

        return False
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

# Identify Chinese files
chinese_files = []
for idx, filepath in enumerate(files_to_process, 1):
    print(f"{idx}. {filepath.name}")
    if is_chinese_file(filepath):
        chinese_files.append(filepath)
        print(f"   -> Contains Chinese content ✓")
    else:
        print(f"   -> No Chinese content")

print("\n" + "=" * 80)
print(f"Chinese files found: {len(chinese_files)}")
print("=" * 80)

if chinese_files:
    print("\nChinese files to be fixed:")
    for idx, filepath in enumerate(chinese_files, 1):
        print(f"{idx}. {filepath.name}")
else:
    print("\nNo Chinese files found in the first 13 files.")