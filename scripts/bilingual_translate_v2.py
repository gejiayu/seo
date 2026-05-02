#!/usr/bin/env python3
"""
Proper bilingual translation for pSEO JSON files.
Uses deep-translator for Chinese to English translation.
Preserves original Chinese content with "_cn" suffix.
"""

import json
import re
import time
from pathlib import Path
from deep_translator import GoogleTranslator

BASE_DIR = Path("/Users/gejiayu/owner/seo/data")

CATEGORIES = [
    "tennis-racket-rental-tools",
    "tent-canopy-rental-tools",
    "tool-hardware-rental-tools",
    "transportation-fleet-tools",
    "travel-agency-tour-operator-tools",
    "travel-hospitality-tools"
]

# Initialize translator
translator = GoogleTranslator(source='zh-CN', target='en')

def translate_text(text, max_retries=3):
    """Translate Chinese text to English."""
    if not text:
        return text

    # Check if text contains Chinese characters
    if not any('一' <= c <= '鿿' for c in text):
        return text  # Already English

    for attempt in range(max_retries):
        try:
            # Split long texts to avoid API limits
            if len(text) > 4500:
                chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
                translated = []
                for chunk in chunks:
                    translated.append(translator.translate(chunk))
                    time.sleep(0.5)
                return ''.join(translated)

            result = translator.translate(text)
            time.sleep(0.3)
            return result
        except Exception as e:
            print(f"  Translation error (attempt {attempt+1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                return text

def process_file(file_path, count, total):
    """Process single JSON file."""
    print(f"\n[{count}/{total}] Processing: {file_path.name}")

    with open(file_path, 'r', encoding='utf-8') as f:
        original = json.load(f)

    # Keep original Chinese fields
    title_cn = original['title']
    desc_cn = original['description']
    content_cn = original['content']
    keywords_cn = original['seo_keywords']
    slug = original['slug']
    published = original['published_at']
    author = original['author']

    print(f"  Original title (CN): {title_cn[:50]}...")

    # Translate title
    print(f"  Translating title...")
    title_en = translate_text(title_cn)
    # Add year suffix if not present
    if '2026' not in title_en:
        title_en = f"{title_en} | 2026 Review"

    # Translate description
    print(f"  Translating description...")
    desc_en = translate_text(desc_cn)
    # Add CTA if not present
    if 'compare' not in desc_en.lower():
        desc_en = f"{desc_en} Compare features and pricing to find your ideal solution."

    # Translate content
    print(f"  Translating content...")
    content_en = translate_text(content_cn)

    # Translate keywords
    print(f"  Translating keywords...")
    keywords_en = []
    for kw in keywords_cn:
        kw_en = translate_text(kw)
        keywords_en.append(kw_en)
        time.sleep(0.1)

    # Create bilingual structure
    bilingual = {
        "title": title_en,
        "title_cn": title_cn,
        "description": desc_en,
        "description_cn": desc_cn,
        "content": content_en,
        "content_cn": content_cn,
        "seo_keywords": keywords_en,
        "seo_keywords_cn": keywords_cn,
        "slug": slug,
        "published_at": published,
        "author": author
    }

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(bilingual, f, ensure_ascii=False, indent=2)

    print(f"  Done! Title (EN): {title_en[:50]}...")

def process_all():
    """Process all categories."""
    total_files = 0
    processed = 0
    report_interval = 20

    # Count total files
    for category in CATEGORIES:
        cat_dir = BASE_DIR / category
        total_files += len(list(cat_dir.glob("*.json")))

    print(f"Total files to process: {total_files}")

    for category in CATEGORIES:
        cat_dir = BASE_DIR / category
        files = sorted(cat_dir.glob("*.json"))

        print(f"\n{'='*60}")
        print(f"Category: {category} ({len(files)} files)")
        print(f"{'='*60}")

        for file_path in files:
            processed += 1
            try:
                process_file(file_path, processed, total_files)

                if processed % report_interval == 0:
                    print(f"\n{'='*60}")
                    print(f"Progress: {processed}/{total_files} files ({100*processed//total_files}%)")
                    print(f"{'='*60}\n")

                time.sleep(0.5)  # Rate limiting

            except Exception as e:
                print(f"\n  ERROR processing {file_path.name}: {e}")

    print(f"\n{'='*60}")
    print(f"COMPLETE: {processed}/{total_files} files processed")
    print(f"{'='*60}")

if __name__ == "__main__":
    process_all()