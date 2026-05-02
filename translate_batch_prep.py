#!/usr/bin/env python3
"""
Batch translate JSON files to bilingual format
Processes files and prepares them for translation
"""
import json
import sys
from pathlib import Path

def prepare_bilingual_structure(filepath):
    """
    Add bilingual structure to JSON file
    Returns the content that needs translation
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Return structure for translation
    return {
        'filepath': filepath,
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'content': data.get('content', ''),
        'seo_keywords': data.get('seo_keywords', []),
        'slug': data.get('slug', ''),
        'published_at': data.get('published_at', ''),
        'author': data.get('author', '')
    }

def list_files_to_process():
    """
    List all files that need bilingual conversion
    """
    categories = [
        'scooter-moped-rental-tools',
        'security-surveillance-rental-tools',
        'ski-snowboard-rental-tools',
        'sporting-goods-retail-tools',
        'sports-equipment-rental-tools',
        'sports-fitness-tools',
        'sports-recreation-management',
        'staffing-recruitment-agency-tools',
        'staging-rigging-rental-tools',
        'storage-unit-rental-tools',
        'subscription-recurring-billing-tools',
        'telecommunications-network-tools'
    ]

    base_path = Path('/Users/gejiayu/owner/seo/data')
    all_files = []

    for category in categories:
        cat_path = base_path / category
        if cat_path.exists():
            for json_file in cat_path.glob('*.json'):
                all_files.append(str(json_file))

    return sorted(all_files)

if __name__ == '__main__':
    files = list_files_to_process()
    print(f"Total files to process: {len(files)}")

    # Print file list
    for i, filepath in enumerate(files, 1):
        print(f"{i}. {filepath}")