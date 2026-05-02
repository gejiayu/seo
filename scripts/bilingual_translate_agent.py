#!/usr/bin/env python3
"""
pSEO Bilingual Translation Agent
Processes specific categories to generate bilingual (English + Chinese) files.
- English version: data/[category]/[slug].json
- Chinese version: data/zh/[category]/[slug].json
- Each file has: language, canonical_link, alternate_links fields
"""

import json
import os
import re
import time
from pathlib import Path
from typing import Dict, List, Tuple
from openai import OpenAI
import sys

# Initialize OpenAI client
client = OpenAI()

SITE_URL = os.environ.get('SITE_URL', 'https://www.housecar.life')

# Categories to process - Updated for batch 2
TARGET_CATEGORIES = [
    "religious-nonprofit-organization-tools",
    "remote-tools",
    "renewable-energy-management-tools",
    "restaurant-food-service-tools",
    "retail-ecommerce-operations-tools",
    "retail-pos-inventory-tools",
    "scooter-moped-rental-tools",
    "security-surveillance-rental-tools",
    "ski-snowboard-rental-tools",
    "sporting-goods-retail-tools",
    "sports-equipment-rental-tools",
    "sports-fitness-tools"
]

def is_chinese_content(text: str) -> bool:
    """Check if text is primarily Chinese"""
    if not text:
        return False
    chinese_chars = len(re.findall(r'[一-鿿]', text))
    total_chars = len(text.strip())
    return chinese_chars > total_chars * 0.3

def translate_to_english(text: str, field_type: str = 'content') -> str:
    """Translate Chinese to English using OpenAI"""
    if not text or is_chinese_content(text) == False:
        return text

    # Truncate for API limits
    max_tokens = 4000 if field_type == 'content' else 500
    text_to_translate = text[:max_tokens * 4]

    try:
        system_prompt = {
            'title': "You are a professional SEO translator. Translate this Chinese title to English. Make it professional and include CTR words like 'Review', 'Guide', 'Comparison', 'Best'. Output only the English title.",
            'description': "You are a professional SEO translator. Translate this Chinese description to English. Keep it 140-160 characters with a compelling CTA like 'Discover the best options today!'. Output only the English description.",
            'content': "You are a professional translator. Translate this Chinese content to English. Maintain all HTML tags, headings, lists, and formatting exactly. Output only the translation.",
            'keywords': "You are an SEO expert. Translate these Chinese keywords to English SEO keywords (5-8 terms). Output as a JSON array of strings."
        }

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt.get(field_type, system_prompt['content'])},
                {"role": "user", "content": text_to_translate}
            ],
            max_tokens=max_tokens,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def translate_to_chinese(text: str, field_type: str = 'content') -> str:
    """Translate English to Chinese using OpenAI"""
    if not text or is_chinese_content(text):
        return text

    max_tokens = 4000 if field_type == 'content' else 500
    text_to_translate = text[:max_tokens * 4]

    try:
        system_prompt = {
            'title': "You are a professional SEO translator. Translate this English title to Chinese. Make it professional and include CTR words like '评测', '指南', '对比'. Add suffix '｜2026年评测' if not present. Output only the Chinese title.",
            'description': "You are a professional SEO translator. Translate this English description to Chinese. Keep it 140-160 characters with a CTA like '了解更多功能和价格对比，找到最适合你的方案！'. Output only the Chinese description.",
            'content': "You are a professional translator. Translate this English content to Chinese. Maintain all HTML tags, headings, lists, and formatting exactly. Output only the translation.",
            'keywords': "You are an SEO expert. Translate these English keywords to Chinese SEO keywords (5-8 terms). Output as a JSON array of strings."
        }

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt.get(field_type, system_prompt['content'])},
                {"role": "user", "content": text_to_translate}
            ],
            max_tokens=max_tokens,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def translate_keywords_to_english(keywords: List[str]) -> List[str]:
    """Translate Chinese keywords to English"""
    if not keywords:
        return []

    translated = []
    for kw in keywords:
        if is_chinese_content(kw):
            en_kw = translate_to_english(kw, 'keywords')
            # Clean up JSON array format if returned
            if en_kw.startswith('['):
                try:
                    parsed = json.loads(en_kw)
                    if isinstance(parsed, list):
                        translated.extend(parsed)
                        continue
                except:
                    pass
            translated.append(en_kw)
        else:
            translated.append(kw)

    return translated[:8]  # Limit to 8 keywords

def translate_keywords_to_chinese(keywords: List[str]) -> List[str]:
    """Translate English keywords to Chinese"""
    if not keywords:
        return []

    translated = []
    for kw in keywords:
        if not is_chinese_content(kw):
            zh_kw = translate_to_chinese(kw, 'keywords')
            # Clean up JSON array format if returned
            if zh_kw.startswith('['):
                try:
                    parsed = json.loads(zh_kw)
                    if isinstance(parsed, list):
                        translated.extend(parsed)
                        continue
                except:
                    pass
            translated.append(zh_kw)
        else:
            translated.append(kw)

    return translated[:8]  # Limit to 8 keywords

def generate_canonical_link(slug: str) -> str:
    """Generate canonical link (always points to English version)"""
    return f"{SITE_URL}/posts/{slug}"

def generate_alternate_links(slug: str) -> Dict[str, str]:
    """Generate hreflang alternate links"""
    return {
        'en-US': f"{SITE_URL}/posts/{slug}",
        'zh-CN': f"{SITE_URL}/zh/posts/{slug}"
    }

def process_file(filepath: Path) -> Tuple[Dict, Dict]:
    """Process single file to generate bilingual versions"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_title = data.get('title', '')
    original_desc = data.get('description', '')
    original_content = data.get('content', '')
    original_keywords = data.get('seo_keywords', [])
    original_slug = data.get('slug', '')
    published_at = data.get('published_at', '')
    author = data.get('author', '')

    # Determine category from file path
    category = filepath.parent.name

    # Determine original language
    is_chinese = is_chinese_content(original_title)

    # Generate English version
    if is_chinese:
        en_title = translate_to_english(original_title, 'title')
        en_desc = translate_to_english(original_desc, 'description')
        en_content = translate_to_english(original_content, 'content')
        en_keywords = translate_keywords_to_english(original_keywords)
        en_slug = original_slug  # Keep original slug (already in English)
    else:
        en_title = original_title
        en_desc = original_desc
        en_content = original_content
        en_keywords = original_keywords if isinstance(original_keywords, list) else []
        en_slug = original_slug

    # Generate Chinese version
    if is_chinese:
        zh_title = original_title
        zh_desc = original_desc
        zh_content = original_content
        zh_keywords = original_keywords if isinstance(original_keywords, list) else []
        zh_slug = original_slug
    else:
        zh_title = translate_to_chinese(original_title, 'title')
        zh_desc = translate_to_chinese(original_desc, 'description')
        zh_content = translate_to_chinese(original_content, 'content')
        zh_keywords = translate_keywords_to_chinese(original_keywords)
        zh_slug = original_slug

    # Build English JSON
    en_data = {
        'title': en_title,
        'description': en_desc,
        'content': en_content,
        'seo_keywords': en_keywords,
        'slug': en_slug,
        'published_at': published_at,
        'author': author,
        'language': 'en-US',
        'canonical_link': generate_canonical_link(en_slug),
        'alternate_links': generate_alternate_links(en_slug),
        'category': category
    }

    # Build Chinese JSON
    zh_data = {
        'title': zh_title,
        'description': zh_desc,
        'content': zh_content,
        'seo_keywords': zh_keywords,
        'slug': zh_slug,
        'published_at': published_at,
        'author': author,
        'language': 'zh-CN',
        'canonical_link': generate_canonical_link(en_slug),  # Points to English version
        'alternate_links': generate_alternate_links(en_slug),
        'category': category
    }

    return en_data, zh_data

def main():
    base_dir = Path('/Users/gejiayu/owner/seo/data')
    zh_dir = Path('/Users/gejiayu/owner/seo/data/zh')

    # Collect all files from target categories
    all_files = []
    for category in TARGET_CATEGORIES:
        cat_dir = base_dir / category
        if cat_dir.exists():
            for json_file in cat_dir.glob("*.json"):
                all_files.append(json_file)

    print(f"Total files to process: {len(all_files)}")
    print(f"Categories: {TARGET_CATEGORIES}")
    print()

    success_count = 0
    error_count = 0

    for i, filepath in enumerate(all_files):
        try:
            # Process file
            en_data, zh_data = process_file(filepath)

            # Category and slug
            category = filepath.parent.name
            slug = en_data['slug']

            # Write English version (update original file)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(en_data, f, ensure_ascii=False, indent=2)

            # Write Chinese version (zh subdirectory)
            zh_category_dir = zh_dir / category
            zh_category_dir.mkdir(parents=True, exist_ok=True)
            zh_filepath = zh_category_dir / f"{slug}.json"
            with open(zh_filepath, 'w', encoding='utf-8') as f:
                json.dump(zh_data, f, ensure_ascii=False, indent=2)

            success_count += 1

            # Report every 20 files
            if (i + 1) % 20 == 0:
                print(f"Progress: {i+1}/{len(all_files)} - Success: {success_count}, Error: {error_count}")
                print(f"  Latest: {filepath.name}")

            # Rate limit delay
            time.sleep(0.3)

        except Exception as e:
            error_count += 1
            print(f"Error processing {filepath}: {e}")

    print()
    print("=" * 60)
    print("FINAL RESULTS")
    print(f"Total files: {len(all_files)}")
    print(f"Success: {success_count}")
    print(f"Error: {error_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()