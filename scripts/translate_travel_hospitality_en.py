#!/usr/bin/env python3
"""
Translate Chinese content to English in travel-hospitality-tools directory
Files have language="en-US" but contain Chinese content
Uses DashScope/Claude API for accurate translation
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, Optional, List

# Configuration
BASE_DIR = Path("/Users/gejiayu/owner/seo/data")
TARGET_DIR = BASE_DIR / "travel-hospitality-tools"

API_KEY = os.environ.get("ANTHROPIC_AUTH_TOKEN")
BASE_URL = os.environ.get("ANTHROPIC_BASE_URL", "https://dashscope.aliyuncs.com/apps/anthropic")

if not API_KEY:
    print("ERROR: ANTHROPIC_AUTH_TOKEN environment variable not set")
    sys.exit(1)

# Rate limiting
BATCH_DELAY = 2  # seconds between batches
BATCH_SIZE = 5   # files per batch


def call_api(prompt: str, max_tokens: int = 16000) -> str:
    """Call Claude API via DashScope using urllib"""
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01"
    }

    data = {
        "model": "claude-sonnet-4-6-20250514",
        "max_tokens": max_tokens,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    url = f"{BASE_URL}/v1/messages"

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result["content"][0]["text"]
    except urllib.error.HTTPError as e:
        print(f"API call failed: {e.code} - {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"API call error: {e}")
        return None


def contains_chinese(text: str) -> bool:
    """Check if text contains Chinese characters"""
    return bool([c for c in text if '一' <= c <= '鿿'])


def translate_title(title: str) -> str:
    """Translate Chinese title to English"""
    prompt = f"""Translate this Chinese SEO title to English.
Keep it concise, professional, and SEO-friendly.
Maintain the year (2026) and any proper nouns/brand names.
Return ONLY the translated title, no explanations.

Chinese title: {title}"""

    return call_api(prompt, max_tokens=500)


def translate_description(description: str) -> str:
    """Translate Chinese description to English"""
    prompt = f"""Translate this Chinese SEO meta description to English.
Keep it under 160 characters, compelling, and include a call-to-action.
Return ONLY the translated description, no explanations.

Chinese description: {description}"""

    return call_api(prompt, max_tokens=500)


def translate_content(content: str) -> str:
    """Translate Chinese HTML content to English"""
    prompt = f"""Translate this Chinese HTML content to English.
IMPORTANT RULES:
1. Keep ALL HTML tags exactly the same (h1, h2, h3, p, table, th, td, tr, ul, li, etc.)
2. Translate ONLY the text content inside the HTML tags
3. Keep all numbers, percentages, prices, and brand names unchanged
4. Keep the table structure intact, only translate cell contents
5. Return ONLY the translated HTML content, no explanations

Chinese HTML content:
{content}"""

    return call_api(prompt, max_tokens=16000)


def clean_keywords(keywords: List[str]) -> List[str]:
    """Clean seo_keywords - remove extra spaces"""
    return [kw.replace('  ', ' ').strip() for kw in keywords]


def process_file(filepath: Path) -> Dict[str, Any]:
    """Process a single JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if file needs translation
        has_chinese_title = contains_chinese(data.get("title", ""))
        has_chinese_desc = contains_chinese(data.get("description", ""))
        has_chinese_content = contains_chinese(data.get("content", ""))

        if not (has_chinese_title or has_chinese_desc or has_chinese_content):
            return {"status": "skipped", "reason": "already English"}

        # Translate fields
        translated = False

        if has_chinese_title:
            print(f"    Translating title...")
            new_title = translate_title(data["title"])
            if new_title:
                data["title"] = new_title.strip()
                translated = True
            else:
                print(f"    Warning: Title translation failed")

        if has_chinese_desc:
            print(f"    Translating description...")
            new_desc = translate_description(data["description"])
            if new_desc:
                data["description"] = new_desc.strip()
                translated = True
            else:
                print(f"    Warning: Description translation failed")

        if has_chinese_content:
            print(f"    Translating content...")
            new_content = translate_content(data["content"])
            if new_content:
                data["content"] = new_content.strip()
                translated = True
            else:
                print(f"    Warning: Content translation failed")

        # Clean keywords
        if "seo_keywords" in data and isinstance(data["seo_keywords"], list):
            data["seo_keywords"] = clean_keywords(data["seo_keywords"])

        # Save file
        if translated:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return {"status": "translated"}

        return {"status": "partial", "reason": "some translations failed"}

    except Exception as e:
        return {"status": "error", "error": str(e)}


def main():
    """Process all files"""
    files = list(TARGET_DIR.glob("*.json"))

    print(f"Found {len(files)} files to process\n")

    translated = 0
    skipped = 0
    errors = 0
    partial = 0

    # Process in batches
    total_batches = (len(files) + BATCH_SIZE - 1) // BATCH_SIZE

    for batch_num in range(total_batches):
        start_idx = batch_num * BATCH_SIZE
        end_idx = min(start_idx + BATCH_SIZE, len(files))
        batch = files[start_idx:end_idx]

        print(f"Processing batch {batch_num + 1}/{total_batches}...")

        for filepath in batch:
            filename = filepath.name
            print(f"  Processing {filename}...")

            result = process_file(filepath)

            if result["status"] == "translated":
                translated += 1
                print(f"    ✓ Translated")
            elif result["status"] == "skipped":
                skipped += 1
                print(f"    - Skipped ({result['reason']})")
            elif result["status"] == "partial":
                partial += 1
                print(f"    ~ Partial ({result['reason']})")
            else:
                errors += 1
                print(f"    ✗ Error: {result['error']}")

        # Delay between batches
        if batch_num + 1 < total_batches:
            print(f"\n  Waiting {BATCH_DELAY}s before next batch...\n")
            time.sleep(BATCH_DELAY)

    print("\n=== Summary ===")
    print(f"Translated: {translated} files")
    print(f"Skipped (already English): {skipped} files")
    print(f"Partial: {partial} files")
    print(f"Errors: {errors} files")
    print(f"Total: {len(files)} files")


if __name__ == "__main__":
    main()