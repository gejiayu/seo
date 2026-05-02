#!/usr/bin/env python3
"""
Efficient bilingual translation processor
Uses batch processing for large-scale file translation
"""
import json
import sys
import os
from pathlib import Path

# Translation cache to avoid re-translating common terms
translation_cache = {}

def translate_to_english(chinese_text, field_type='general'):
    """
    Translate Chinese text to English
    This function will be called by Claude during processing
    """
    # Placeholder - actual translation happens via Claude
    return chinese_text

def process_single_file(filepath, translations):
    """
    Process a single JSON file with provided translations
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Add English fields
        data['title_en'] = translations.get('title_en', '')
        data['description_en'] = translations.get('description_en', '')
        data['content_en'] = translations.get('content_en', '')

        # Handle seo_keywords
        if 'seo_keywords' in data and isinstance(data['seo_keywords'], list):
            data['seo_keywords_en'] = translations.get('seo_keywords_en', [])

        # Write back with proper formatting
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def get_file_list():
    """
    Get list of all files to process
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
    files = []

    for category in categories:
        cat_path = base_path / category
        if cat_path.exists():
            files.extend([str(f) for f in sorted(cat_path.glob('*.json'))])

    return files

if __name__ == '__main__':
    # For testing
    files = get_file_list()
    print(f"Found {len(files)} files to process")
    print("This script is ready for batch processing with Claude")