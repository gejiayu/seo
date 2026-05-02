#!/usr/bin/env python3
"""
Bilingual pSEO Translation Script with proper Chinese-to-English translation.
Uses deep-translator library for accurate translations.
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
    """Translate Chinese text to English using Google Translate."""
    if not text or not any(ord(c) > 127 for c in text):
        return text  # Already English or empty

    for attempt in range(max_retries):
        try:
            # Split long texts to avoid API limits
            if len(text) > 5000:
                chunks = [text[i:i+4500] for i in range(0, len(text), 4500)]
                translated_chunks = []
                for chunk in chunks:
                    translated_chunks.append(translator.translate(chunk))
                    time.sleep(0.5)  # Rate limiting
                return ''.join(translated_chunks)

            result = translator.translate(text)
            time.sleep(0.3)  # Rate limiting
            return result
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retry
            else:
                print(f"Translation failed: {e}")
                return text

def translate_title(title_cn):
    """Translate Chinese title to English."""
    # Remove year suffix temporarily
    title = re.sub(r'｜2026年.*', '', title_cn)
    title = re.sub(r'｜2026.*', '', title)

    # Translate
    title_en = translate_text(title)

    # Add year suffix
    return f"{title_en} | 2026 Review"

def translate_description(description_cn):
    """Translate Chinese description to English."""
    # Remove Chinese CTAs
    desc = description_cn.replace(
        "了解更多功能和价格对比，找到最适合你的方案！专业评测助你决策！",
        ""
    )

    # Translate
    desc_en = translate_text(desc)

    # Add English CTA
    return f"{desc_en} Compare features and pricing to find your ideal solution."

def translate_content(content_cn):
    """Translate HTML content while preserving structure."""
    # Extract text from HTML while preserving tags
    content = content_cn

    # Split by HTML tags and translate text portions
    # This preserves HTML structure

    # Translate headers first
    header_patterns = [
        (r'<h1>([^<]+)</h1>', 'h1'),
        (r'<h2>([^<]+)</h2>', 'h2'),
        (r'<h3>([^<]+)</h3>', 'h3'),
        (r'<strong>([^<]+)</strong>', 'strong'),
        (r'<p>([^<]+)</p>', 'p'),
        (r'<li>([^<]+)</li>', 'li'),
        (r'<th>([^<]+)</th>', 'th'),
        (r'<td>([^<]+)</td>', 'td'),
    ]

    for pattern, tag in header_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            original_text = match.group(1)
            if any(ord(c) > 127 for c in original_text):  # Has Chinese
                translated_text = translate_text(original_text)
                content = content.replace(f'<{tag}>{original_text}</{tag}>',
                                         f'<{tag}>{translated_text}</{tag}>')
                time.sleep(0.2)

    return content

def translate_keywords(keywords_cn):
    """Translate SEO keywords."""
    keywords_en = []
    for kw in keywords_cn:
        kw_en = translate_text(kw)
        keywords_en.append(kw_en)
        time.sleep(0.1)
    return keywords_en

def process_file(file_path):
    """Process single JSON file with proper translation."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get original fields
    title_cn = data['title']
    desc_cn = data['description']
    content_cn = data['content']
    slug = data['slug']
    keywords_cn = data['seo_keywords']
    published = data['published_at']
    author = data['author']

    print(f"  Translating: {file_path.name}")

    # Generate English translations with proper translation
    title_en = translate_title(title_cn)
    time.sleep(0.5)

    desc_en = translate_description(desc_cn)
    time.sleep(0.5)

    content_en = translate_content(content_cn)
    time.sleep(0.5)

    keywords_en = translate_keywords(keywords_cn)

    # Create bilingual structure
    new_data = {
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

    return new_data

def process_all():
    """Process all files in all categories."""
    total = 0
    report_interval = 20

    for category in CATEGORIES:
        cat_dir = BASE_DIR / category
        files = sorted(cat_dir.glob("*.json"))

        print(f"\n[{category}] - {len(files)} files")

        for file_path in files:
            try:
                new_data = process_file(file_path)

                # Write back
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(new_data, f, ensure_ascii=False, indent=2)

                total += 1

                # Report progress
                if total % report_interval == 0:
                    print(f"\n=== Progress: {total} files processed ===\n")

                time.sleep(0.5)  # Rate limiting between files

            except Exception as e:
                print(f"  ERROR: {file_path.name} - {e}")

    print(f"\n=== COMPLETE ===")
    print(f"Total files processed: {total}")

if __name__ == "__main__":
    process_all()