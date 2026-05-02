#!/usr/bin/env python3
"""
Batch translation processor for mining-extraction-tools JSON files.
Translates Chinese content (title, description, content) to natural American English.
Uses semantic understanding for natural translation.
"""

import json
import re
from pathlib import Path

DATA_DIR = Path("/Users/gejiayu/owner/seo/data/mining-extraction-tools")
CHINESE_PATTERN = re.compile(r'[一-鿿]')

def has_chinese(text: str) -> bool:
    """Check if text contains Chinese characters."""
    if not text:
        return False
    return bool(CHINESE_PATTERN.search(text))

def needs_translation(file_path: Path) -> dict:
    """Check which fields need translation."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = {
        'title': has_chinese(str(data.get('title', ''))),
        'description': has_chinese(str(data.get('description', ''))),
        'content': has_chinese(str(data.get('content', ''))),
        'data': data
    }
    return result

def main():
    """Process all files needing translation."""
    files_to_process = []

    # Find all files needing translation
    for json_file in sorted(DATA_DIR.glob("*.json")):
        if json_file.name.startswith(("detect_", "chinese_files_list", "TRANSLATION", "translation_", "batch_", "comprehensive_", "auto_", "process_", "translate_")):
            continue

        status = needs_translation(json_file)
        if status['title'] or status['description'] or status['content']:
            files_to_process.append((json_file, status))

    print(f"Found {len(files_to_process)} files needing translation")

    # Create detailed report
    report = []
    for i, (file_path, status) in enumerate(files_to_process, 1):
        needs = []
        if status['title']:
            needs.append('title')
        if status['description']:
            needs.append('description')
        if status['content']:
            needs.append('content')

        report.append({
            'index': i,
            'filename': file_path.name,
            'fields_needing_translation': needs,
            'seo_keywords_type': type(status['data'].get('seo_keywords', [])).__name__,
            'language_field': status['data'].get('language', 'missing')
        })

    # Save report
    with open(DATA_DIR / 'translation_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\nReport saved to: translation_report.json")
    print(f"\nSummary:")
    print(f"  Files with Chinese title: {sum(1 for r in report if 'title' in r['fields_needing_translation'])}")
    print(f"  Files with Chinese description: {sum(1 for r in report if 'description' in r['fields_needing_translation'])}")
    print(f"  Files with Chinese content: {sum(1 for r in report if 'content' in r['fields_needing_translation'])}")

if __name__ == "__main__":
    main()