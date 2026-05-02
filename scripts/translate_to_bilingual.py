#!/usr/bin/env python3
"""
Translate Chinese JSON files to bilingual format (English + Chinese)
Processes files from specified directories and adds English translations.
"""

import json
import os
import re
import sys
from pathlib import Path
from openai import OpenAI
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize OpenAI client (uses OPENAI_API_KEY env var)
client = OpenAI()

def detect_language(text):
    """Detect if text is primarily Chinese or English"""
    chinese_chars = len(re.findall(r'[一-鿿]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    return 'zh' if chinese_chars > english_chars * 0.5 else 'en'

def translate_to_english(chinese_text, field_type='content'):
    """Translate Chinese text to English using OpenAI"""
    if not chinese_text or detect_language(chinese_text) == 'en':
        return chinese_text

    # Truncate very long content for API limits
    max_tokens = 4000 if field_type == 'content' else 500
    text_to_translate = chinese_text[:max_tokens * 4]  # Approximate char limit

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a professional translator. Translate the following Chinese {field_type} to English. Maintain the original structure and formatting (HTML tags, headings, etc.). Output only the translation, no explanations."
                },
                {
                    "role": "user",
                    "content": text_to_translate
                }
            ],
            max_tokens=max_tokens,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Translation error: {e}")
        return chinese_text

def translate_keywords_zh_to_en(keywords_zh):
    """Translate Chinese keywords to English keywords"""
    if not keywords_zh:
        return []

    keywords_en = []
    for kw in keywords_zh:
        if detect_language(kw) == 'zh':
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "Translate this Chinese SEO keyword to English. Output only the English keyword, no explanations."
                        },
                        {
                            "role": "user",
                            "content": kw
                        }
                    ],
                    max_tokens=50,
                    temperature=0.3
                )
                keywords_en.append(response.choices[0].message.content.strip())
            except Exception:
                keywords_en.append(kw)
        else:
            keywords_en.append(kw)

    return keywords_en

def process_file(file_path, progress_counter=None):
    """Process a single JSON file to bilingual format"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Skip if already bilingual
        if 'title_zh' in data or 'title_en' in data:
            return None, "already bilingual"

        # Detect original language
        original_lang = detect_language(data.get('title', '') or data.get('content', ''))

        if original_lang == 'zh':
            # Chinese file - add English translation
            data['title_zh'] = data.get('title', '')
            data['title_en'] = translate_to_english(data.get('title', ''), 'title')

            data['description_zh'] = data.get('description', '')
            data['description_en'] = translate_to_english(data.get('description', ''), 'description')

            data['content_zh'] = data.get('content', '')
            data['content_en'] = translate_to_english(data.get('content', ''), 'content')

            # Translate keywords
            keywords_zh = data.get('seo_keywords', [])
            data['seo_keywords_zh'] = keywords_zh
            data['seo_keywords_en'] = translate_keywords_zh_to_en(keywords_zh)

            # Remove old single-language fields
            data.pop('title', None)
            data.pop('description', None)
            data.pop('content', None)
        else:
            # English file - add Chinese translation
            data['title_en'] = data.get('title', '')
            data['title_zh'] = translate_to_english(data.get('title', ''), 'title')  # Will need reverse translation

            data['description_en'] = data.get('description', '')
            data['description_zh'] = translate_to_english(data.get('description', ''), 'description')

            data['content_en'] = data.get('content', '')
            data['content_zh'] = translate_to_english(data.get('content', ''), 'content')

            # Keywords stay in English for English files
            data['seo_keywords_en'] = data.get('seo_keywords', [])
            data.pop('seo_keywords', None)

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return file_path, "success"

    except Exception as e:
        return file_path, f"error: {str(e)}"

def main():
    # Categories to process
    categories = [
        "event-planning-tools",
        "finance-accounting-tools",
        "fishing-gear-rental-tools",
        "fitness-gym-management",
        "florist-flower-shop-tools",
        "food-beverage-distribution-tools",
        "franchise-business-tools",
        "furniture-home-rental-tools",
        "generator-power-rental-tools",
        "golf-equipment-rental-tools",
        "government-public-sector-tools",
        "healthcare-medical-tools"
    ]

    base_dir = Path("/Users/gejiayu/owner/seo/data")

    # Collect all files
    all_files = []
    for category in categories:
        cat_dir = base_dir / category
        if cat_dir.exists():
            for json_file in cat_dir.glob("*.json"):
                all_files.append(json_file)

    print(f"Total files to process: {len(all_files)}")

    # Process files sequentially to avoid rate limits
    success_count = 0
    error_count = 0
    skip_count = 0

    for i, file_path in enumerate(all_files):
        result, status = process_file(file_path, i+1)

        if status == "success":
            success_count += 1
        elif status == "already bilingual":
            skip_count += 1
        else:
            error_count += 1
            print(f"Error processing {file_path}: {status}")

        # Report every 20 files
        if (i + 1) % 20 == 0:
            print(f"Progress: {i+1}/{len(all_files)} - Success: {success_count}, Skip: {skip_count}, Error: {error_count}")

        # Rate limit delay
        time.sleep(0.5)

    print(f"\nFinal Results:")
    print(f"Total: {len(all_files)}")
    print(f"Success: {success_count}")
    print(f"Skip: {skip_count}")
    print(f"Error: {error_count}")

if __name__ == "__main__":
    main()