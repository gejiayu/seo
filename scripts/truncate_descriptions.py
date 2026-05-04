#!/usr/bin/env python3
"""Truncate JSON description fields to 155 characters with word boundary preservation."""

import json
import os
from pathlib import Path


def truncate_description(text: str, max_length: int = 155) -> str:
    """Truncate text to max_length, preserving word boundary and adding ellipsis."""
    if len(text) <= max_length:
        return text

    # Truncate to max_length - 3 to account for ellipsis
    truncated = text[:max_length - 3]

    # Find last space to preserve word boundary
    last_space = truncated.rfind(' ')

    if last_space > 0:
        truncated = truncated[:last_space]

    return truncated + '...'


def process_json_file(file_path: Path) -> tuple[bool, int]:
    """Process a single JSON file. Returns (was_modified, original_length)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if 'description' not in data:
            return False, 0

        original_desc = data['description']
        original_length = len(original_desc)

        if original_length <= 155:
            return False, original_length

        # Truncate and save
        data['description'] = truncate_description(original_desc)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return True, original_length

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, 0


def process_directory(directory: Path) -> dict:
    """Process all JSON files in a directory."""
    stats = {
        'total_files': 0,
        'modified_files': 0,
        'skipped_files': 0,
        'total_chars_saved': 0
    }

    if not directory.exists():
        print(f"Directory not found: {directory}")
        return stats

    json_files = list(directory.glob('*.json'))
    stats['total_files'] = len(json_files)

    for json_file in json_files:
        was_modified, original_length = process_json_file(json_file)

        if was_modified:
            stats['modified_files'] += 1
            stats['total_chars_saved'] += original_length - 155
        else:
            stats['skipped_files'] += 1

    return stats


def main():
    """Process all target directories."""
    base_dir = Path('/Users/gejiayu/owner/seo/data')

    directories = [
        'travel-hospitality-tools',
        'insurance-claims-processing-tools'
    ]

    total_stats = {
        'total_files': 0,
        'modified_files': 0,
        'skipped_files': 0,
        'total_chars_saved': 0
    }

    for dir_name in directories:
        print(f"\n{'='*60}")
        print(f"Processing: {dir_name}")
        print(f"{'='*60}")

        # Process main directory
        main_dir = base_dir / dir_name
        stats = process_directory(main_dir)

        print(f"Main directory: {stats['total_files']} files")
        print(f"  - Modified: {stats['modified_files']}")
        print(f"  - Skipped (already <= 155 chars): {stats['skipped_files']}")
        print(f"  - Characters saved: {stats['total_chars_saved']}")

        # Update totals
        for key in total_stats:
            total_stats[key] += stats[key]

        # Process zh/ counterpart
        zh_dir = base_dir / 'zh' / dir_name
        if zh_dir.exists():
            zh_stats = process_directory(zh_dir)
            print(f"\nZH directory: {zh_stats['total_files']} files")
            print(f"  - Modified: {zh_stats['modified_files']}")
            print(f"  - Skipped: {zh_stats['skipped_files']}")

            # Update totals
            for key in total_stats:
                total_stats[key] += zh_stats[key]

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total files processed: {total_stats['total_files']}")
    print(f"Total files modified: {total_stats['modified_files']}")
    print(f"Total files skipped: {total_stats['skipped_files']}")
    print(f"Total characters saved: {total_stats['total_chars_saved']}")


if __name__ == '__main__':
    main()