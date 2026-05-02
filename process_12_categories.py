#!/usr/bin/env python3
"""
Translate JSON files to bilingual format for 12 specific categories
"""

import json
import re
import time
from pathlib import Path
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

def detect_language(text):
    """Detect if text is primarily Chinese or English"""
    if not text:
        return 'en'
    chinese_chars = len(re.findall(r'[一-鿿]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    return 'zh' if chinese_chars > english_chars * 0.5 else 'en'

def translate_text(text, field_type='content'):
    """Translate text to target language using OpenAI"""
    if not text:
        return text

    # Check if already in target language
    lang = detect_language(text)

    # Truncate for API limits
    max_tokens = 4000 if field_type == 'content' else 500
    text_to_translate = text[:max_tokens * 4]

    try:
        if lang == 'zh':
            # Translate Chinese to English
            prompt = f"Translate this Chinese {field_type} to English. Maintain all HTML structure and formatting. Output only the translation:"
        else:
            # Translate English to Chinese
            prompt = f"Translate this English {field_type} to Chinese. Maintain all HTML structure and formatting. Output only the translation:"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text_to_translate}
            ],
            max_tokens=max_tokens,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Translation error for {field_type}: {e}")
        return text

def translate_keywords(keywords, source_lang):
    """Translate keywords array"""
    if not keywords or not isinstance(keywords, list):
        return keywords

    translated = []
    for kw in keywords:
        if not kw:
            translated.append(kw)
            continue

        kw_lang = detect_language(kw)

        # Skip if already in target language
        if source_lang == 'zh' and kw_lang == 'en':
            translated.append(kw)
            continue
        elif source_lang == 'en' and kw_lang == 'zh':
            translated.append(kw)
            continue

        try:
            prompt = f"Translate this SEO keyword from {kw_lang} to {'en' if source_lang == 'zh' else 'zh'}. Output only the translated keyword:"
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": kw}
                ],
                max_tokens=50,
                temperature=0.3
            )
            translated.append(response.choices[0].message.content.strip())
        except Exception:
            translated.append(kw)

    return translated

def process_file(file_path):
    """Process a single JSON file to bilingual format"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Skip if already bilingual
        if 'title_zh' in data or 'title_en' in data:
            return "already bilingual"

        # Detect original language
        original_lang = detect_language(data.get('title', '') or data.get('content', ''))

        if original_lang == 'zh':
            # Chinese file - add English translation
            data['title_zh'] = data.get('title', '')
            data['title_en'] = translate_text(data.get('title', ''), 'title')

            data['description_zh'] = data.get('description', '')
            data['description_en'] = translate_text(data.get('description', ''), 'description')

            data['content_zh'] = data.get('content', '')
            data['content_en'] = translate_text(data.get('content', ''), 'content')

            # Translate keywords
            keywords_zh = data.get('seo_keywords', [])
            data['seo_keywords_zh'] = keywords_zh
            data['seo_keywords_en'] = translate_keywords(keywords_zh, 'zh')

            # Remove old single-language fields
            data.pop('title', None)
            data.pop('description', None)
            data.pop('content', None)
            data.pop('seo_keywords', None)
        else:
            # English file - add Chinese translation
            data['title_en'] = data.get('title', '')
            data['title_zh'] = translate_text(data.get('title', ''), 'title')

            data['description_en'] = data.get('description', '')
            data['description_zh'] = translate_text(data.get('description', ''), 'description')

            data['content_en'] = data.get('content', '')
            data['content_zh'] = translate_text(data.get('content', ''), 'content')

            # Translate keywords
            keywords_en = data.get('seo_keywords', [])
            data['seo_keywords_en'] = keywords_en
            data['seo_keywords_zh'] = translate_keywords(keywords_en, 'en')

            # Remove old single-language fields
            data.pop('title', None)
            data.pop('description', None)
            data.pop('content', None)
            data.pop('seo_keywords', None)

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return "success"

    except Exception as e:
        return f"error: {str(e)}"

def main():
    # Categories to process
    categories = [
        "bike-cycling-rental-tools",
        "blue-collar-tools",
        "boat-marine-rental-tools",
        "camera-photography-rental-tools",
        "camping-outdoor-gear-rental-tools",
        "car-vehicle-rental-tools",
        "casino-gaming-entertainment-tools",
        "child-care-preschool-tools",
        "cleaning-maintenance-rental-tools",
        "construction-building-rental-tools",
        "construction-contractor-tools",
        "costume-fashion-rental-tools"
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
    print(f"Categories: {categories}")
    print()

    # Process files sequentially
    success_count = 0
    skip_count = 0
    error_count = 0

    for i, file_path in enumerate(all_files):
        status = process_file(file_path)

        if status == "success":
            success_count += 1
        elif status == "already bilingual":
            skip_count += 1
        else:
            error_count += 1
            print(f"❌ Error processing {file_path.name}: {status}")

        # Report every 20 files
        if (i + 1) % 20 == 0:
            print(f"✓ Progress: {i+1}/{len(all_files)} | Success: {success_count} | Skip: {skip_count} | Error: {error_count}")

        # Rate limit delay
        time.sleep(0.5)

    print()
    print("=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)
    print(f"Total processed: {len(all_files)}")
    print(f"Success: {success_count}")
    print(f"Skipped (already bilingual): {skip_count}")
    print(f"Errors: {error_count}")
    print("=" * 80)

if __name__ == "__main__":
    main()