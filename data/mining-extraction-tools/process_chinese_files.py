#!/usr/bin/env python3
"""
Script to translate Chinese JSON files to English using semantic AI.
Processes files 1-20 from the Chinese files list.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any

DATA_DIR = Path("/Users/gejiayu/owner/seo/data/mining-extraction-tools")

# Pattern to detect Chinese characters
CHINESE_PATTERN = re.compile(r'[一-鿿]')

def has_chinese(text: str) -> bool:
    """Check if text contains Chinese characters."""
    if not text:
        return False
    return bool(CHINESE_PATTERN.search(text))

def load_chinese_files_list() -> list:
    """Load the list of Chinese files."""
    list_file = DATA_DIR / "chinese_files_list.txt"
    with open(list_file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def read_json_file(filename: str) -> Dict[Any, Any]:
    """Read a JSON file."""
    filepath = DATA_DIR / filename
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(filename: str, data: Dict[Any, Any]):
    """Save a JSON file."""
    filepath = DATA_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def process_files(files_to_process: list):
    """Process and print info about files that need translation."""
    print(f"\n{'='*60}")
    print(f"Files to Process: {len(files_to_process)}")
    print(f"{'='*60}\n")

    for i, filename in enumerate(files_to_process, 1):
        try:
            data = read_json_file(filename)
            has_chinese_content = (
                has_chinese(str(data.get('title', ''))) or
                has_chinese(str(data.get('description', ''))) or
                has_chinese(str(data.get('content', ''))) or
                any(has_chinese(str(kw)) for kw in data.get('seo_keywords', []))
            )
            has_language_field = 'language' in data

            print(f"{i}. {filename}")
            print(f"   - Chinese content: {'YES' if has_chinese_content else 'NO'}")
            print(f"   - Language field: {'YES' if has_language_field else 'NO'}")
            print(f"   - Needs translation: {'YES' if has_chinese_content and not has_language_field else 'NO'}")
            print()

        except Exception as e:
            print(f"{i}. {filename} - ERROR: {e}\n")

def main():
    # Load file list
    all_files = load_chinese_files_list()

    # Process first 20 files
    files_to_process = all_files[:20]

    print(f"Total Chinese files detected: {len(all_files)}")
    print(f"Processing first {len(files_to_process)} files\n")

    # Analyze files
    process_files(files_to_process)

    # Return list for further processing
    return files_to_process

if __name__ == "__main__":
    files = main()
    print("\nFiles ready for translation:")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")