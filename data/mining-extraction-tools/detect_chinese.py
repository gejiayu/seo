#!/usr/bin/env python3
"""
Script to detect and translate Chinese JSON files to English.
Uses semantic AI translation for natural American English.
"""

import json
import re
import os
from pathlib import Path
from typing import Dict, List, Any
import sys

# Directory to process
DATA_DIR = Path("/Users/gejiayu/owner/seo/data/mining-extraction-tools")

# Pattern to detect Chinese characters (CJK unified ideographs)
CHINESE_PATTERN = re.compile(r'[一-鿿]')

def has_chinese(text: str) -> bool:
    """Check if text contains Chinese characters."""
    if not text:
        return False
    return bool(CHINESE_PATTERN.search(text))

def find_chinese_files(directory: Path) -> List[Path]:
    """Find all JSON files with Chinese content."""
    chinese_files = []
    for json_file in directory.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Check all text fields for Chinese
                if has_chinese(str(data.get('title', ''))):
                    chinese_files.append(json_file)
                    continue
                if has_chinese(str(data.get('description', ''))):
                    chinese_files.append(json_file)
                    continue
                if has_chinese(str(data.get('content', ''))):
                    chinese_files.append(json_file)
                    continue
                # Check keywords array
                keywords = data.get('seo_keywords', [])
                if isinstance(keywords, list):
                    for kw in keywords:
                        if has_chinese(str(kw)):
                            chinese_files.append(json_file)
                            break
        except Exception as e:
            print(f"Error reading {json_file}: {e}")
            continue
    return sorted(chinese_files)

def main():
    print(f"Scanning directory: {DATA_DIR}")
    chinese_files = find_chinese_files(DATA_DIR)
    print(f"\nFound {len(chinese_files)} files with Chinese content:")
    for i, file in enumerate(chinese_files, 1):
        print(f"{i}. {file.name}")
    print(f"\nTotal: {len(chinese_files)} files to translate")

    # Write list to file for processing
    output_file = DATA_DIR / "chinese_files_list.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for file in chinese_files:
            f.write(f"{file.name}\n")
    print(f"\nFile list saved to: {output_file}")

if __name__ == "__main__":
    main()