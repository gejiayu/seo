#!/usr/bin/env python3
"""
Bilingual translation with explicit progress logging.
"""

import json
import re
import time
import sys
from pathlib import Path
from deep_translator import GoogleTranslator

BASE_DIR = Path("/Users/gejiayu/owner/seo/data")
LOG_FILE = Path("/tmp/translate_progress.txt")

CATEGORIES = [
    "tennis-racket-rental-tools",
    "tent-canopy-rental-tools",
    "tool-hardware-rental-tools",
    "transportation-fleet-tools",
    "travel-agency-tour-operator-tools",
    "travel-hospitality-tools"
]

def log(msg):
    """Write to log file and stdout."""
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')
        f.flush()
    print(msg)
    sys.stdout.flush()

translator = GoogleTranslator(source='zh-CN', target='en')

def translate_text(text):
    """Translate Chinese text."""
    if not text:
        return text
    if not any('一' <= c <= '鿿' for c in text):
        return text

    try:
        if len(text) > 4500:
            chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
            return ''.join([translator.translate(c) for c in chunks])
        return translator.translate(text)
    except Exception as e:
        log(f"  Error: {e}")
        return text

def process_file(file_path, count, total):
    """Process one file."""
    log(f"[{count}/{total}] {file_path.name}")

    with open(file_path, 'r', encoding='utf-8') as f:
        original = json.load(f)

    title_cn = original['title']
    desc_cn = original['description']
    content_cn = original['content']
    keywords_cn = original['seo_keywords']
    slug = original['slug']
    published = original['published_at']
    author = original['author']

    title_en = translate_text(title_cn)
    if '2026' not in title_en:
        title_en = f"{title_en} | 2026 Review"

    desc_en = translate_text(desc_cn)
    if 'compare' not in desc_en.lower():
        desc_en = f"{desc_en} Compare features and pricing."

    content_en = translate_text(content_cn)

    keywords_en = [translate_text(kw) for kw in keywords_cn]

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

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(bilingual, f, ensure_ascii=False, indent=2)

def main():
    LOG_FILE.unlink(missing_ok=True)
    log("Starting bilingual translation...")

    total = sum(len(list((BASE_DIR / cat).glob("*.json"))) for cat in CATEGORIES)
    log(f"Total files: {total}")

    count = 0
    for category in CATEGORIES:
        cat_dir = BASE_DIR / category
        files = sorted(cat_dir.glob("*.json"))
        log(f"\n[{category}] - {len(files)} files")

        for fp in files:
            count += 1
            try:
                process_file(fp, count, total)
                time.sleep(0.3)
                if count % 20 == 0:
                    log(f"\n=== Progress: {count}/{total} ({100*count//total}%) ===\n")
            except Exception as e:
                log(f"ERROR: {fp.name} - {e}")

    log(f"\n=== COMPLETE: {count} files ===")

if __name__ == "__main__":
    main()