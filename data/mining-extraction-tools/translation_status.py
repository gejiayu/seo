#!/usr/bin/env python3
"""
Comprehensive translation script for mining-extraction-tools JSON files.
Translates all Chinese content (title, description, content) to natural American English.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any

DATA_DIR = Path("/Users/gejiayu/owner/seo/data/mining-extraction-tools")
CHINESE_PATTERN = re.compile(r'[一-鿿]')

def has_chinese(text: str) -> bool:
    """Check if text contains Chinese characters."""
    if not text:
        return False
    return bool(CHINESE_PATTERN.search(text))

def get_files_needing_translation() -> List[tuple]:
    """Get all files with Chinese content."""
    files = []
    for json_file in DATA_DIR.glob("*.json"):
        if json_file.name.startswith(("detect_", "chinese_files_list", "TRANSLATION")):
            continue
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Check if any of the main fields contain Chinese
                title_cn = has_chinese(str(data.get('title', '')))
                desc_cn = has_chinese(str(data.get('description', '')))
                content_cn = has_chinese(str(data.get('content', '')))

                status = []
                if title_cn:
                    status.append("title")
                if desc_cn:
                    status.append("description")
                if content_cn:
                    status.append("content")

                if status:
                    files.append((json_file, status))
        except Exception as e:
            print(f"Error reading {json_file}: {e}")
    return sorted(files, key=lambda x: x[0].name)

def main():
    print("=" * 80)
    print("Mining-Extraction-Tools Translation Report")
    print("=" * 80)

    files = get_files_needing_translation()
    print(f"\nTotal files needing translation: {len(files)}")

    # Group files by status
    fully_chinese = []
    partially_translated = []

    for file_path, status in files:
        if len(status) == 3:
            fully_chinese.append((file_path, status))
        else:
            partially_translated.append((file_path, status))

    print(f"\nFully Chinese files (title + description + content): {len(fully_chinese)}")
    print(f"Partially translated files: {len(partially_translated)}")

    print("\n" + "=" * 80)
    print("Files needing translation:")
    print("=" * 80)

    for i, (file_path, status) in enumerate(files, 1):
        print(f"\n{i}. {file_path.name}")
        print(f"   Chinese fields: {', '.join(status)}")

    print("\n" + "=" * 80)
    print("Summary:")
    print("=" * 80)
    print(f"Total files to process: {len(files)}")
    print("\nFields needing translation:")

    title_count = sum(1 for _, s in files if 'title' in s)
    desc_count = sum(1 for _, s in files if 'description' in s)
    content_count = sum(1 for _, s in files if 'content' in s)

    print(f"  - Titles: {title_count}")
    print(f"  - Descriptions: {desc_count}")
    print(f"  - Contents: {content_count}")

if __name__ == "__main__":
    main()