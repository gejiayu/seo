#!/usr/bin/env python3
"""
Comprehensive bilingual translation processor
Uses pattern-based + template-based + actual translation for efficiency
"""
import json
import os
import sys
from pathlib import Path

class BilingualTranslator:
    """
    Handles large-scale bilingual translation efficiently
    """

    def __init__(self):
        self.processed_count = 0
        self.error_count = 0
        self.skip_count = 0

    def translate_file(self, filepath):
        """
        Process a single file with bilingual translation
        """
        try:
            # Read file
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check if already bilingual
            if 'title_en' in data:
                self.skip_count += 1
                return 'skip'

            # Create bilingual structure
            bilingual_data = data.copy()

            # Add English translations (placeholder for now)
            # In actual implementation, Claude will provide these
            bilingual_data['title_en'] = self._placeholder_translate(data.get('title', ''), 'title')
            bilingual_data['description_en'] = self._placeholder_translate(data.get('description', ''), 'description')
            bilingual_data['content_en'] = self._placeholder_translate(data.get('content', ''), 'content')

            if 'seo_keywords' in data and isinstance(data['seo_keywords'], list):
                bilingual_data['seo_keywords_en'] = [
                    self._placeholder_translate(kw, 'keyword') for kw in data['seo_keywords']
                ]

            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(bilingual_data, f, ensure_ascii=False, indent=2)

            self.processed_count += 1

            # Report every 20 files
            if self.processed_count % 20 == 0:
                print(f"[PROGRESS] Processed {self.processed_count} files")

            return 'success'

        except Exception as e:
            self.error_count += 1
            print(f"[ERROR] {filepath}: {e}")
            return 'error'

    def _placeholder_translate(self, text, field_type):
        """
        Placeholder - actual translations will be provided by Claude
        This marks where translation is needed
        """
        # Return placeholder indicating translation needed
        return f"[TRANSLATE:{field_type}] {text[:50]}..."

    def process_batch(self, filepaths, start_idx=0, batch_size=20):
        """
        Process a batch of files
        """
        batch = filepaths[start_idx:start_idx + batch_size]

        print(f"\n=== Processing Batch {start_idx//batch_size + 1} ===")
        print(f"Files {start_idx+1} to {start_idx+len(batch)}")

        results = []
        for filepath in batch:
            result = self.translate_file(filepath)
            results.append((filepath, result))

        return results

    def get_summary(self):
        """
        Get processing summary
        """
        return {
            'processed': self.processed_count,
            'skipped': self.skip_count,
            'errors': self.error_count
        }

def get_all_files():
    """
    Get all files in the 12 categories
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
            all_files.extend([str(f) for f in sorted(cat_path.glob('*.json'))])

    return sorted(all_files)

if __name__ == '__main__':
    print("=== pSEO Bilingual Translation System ===")
    print("This script prepares files for Claude batch translation")
    print("\nMode: Placeholder (marks translation needed)")
    print("Use this script to identify what needs translation\n")

    files = get_all_files()
    translator = BilingualTranslator()

    # Process all files (placeholder mode)
    for i in range(0, len(files), 20):
        translator.process_batch(files, start_idx=i, batch_size=20)

    summary = translator.get_summary()
    print(f"\n=== Final Summary ===")
    print(f"Processed: {summary['processed']}")
    print(f"Skipped: {summary['skipped']}")
    print(f"Errors: {summary['errors']}")

    print("\nNote: This was placeholder mode.")
    print("Next step: Use Claude to provide actual translations")