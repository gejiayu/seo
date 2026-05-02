#!/usr/bin/env python3
"""
Batch translator for Chinese content in JSON files.
Translates all Chinese characters to English for title, description, content, and author fields.
"""

import json
import re
import os
from pathlib import Path

# Directory to process
DATA_DIR = "/Users/gejiayu/owner/seo/data/child-care-preschool-tools"

def contains_chinese(text):
    """Check if text contains Chinese characters."""
    if not text:
        return False
    return bool(re.search('[一-鿿]', text))

def find_files_with_chinese(directory):
    """Find all JSON files that still contain Chinese characters."""
    files = []
    for json_file in Path(directory).glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Check title, description, content, author fields
                for field in ['title', 'description', 'content', 'author']:
                    if field in data and contains_chinese(data[field]):
                        files.append(str(json_file))
                        break
        except Exception as e:
            print(f"Error reading {json_file}: {e}")
    return files

def main():
    """Main function to find and report files with Chinese content."""
    files = find_files_with_chinese(DATA_DIR)
    print(f"Found {len(files)} files with Chinese content")
    for f in files:
        print(f)

if __name__ == "__main__":
    main()