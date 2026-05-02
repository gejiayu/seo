#!/usr/bin/env python3
"""
Batch translate religious nonprofit organization tools from English to Chinese
"""

import json
import os
from pathlib import Path

# Configuration
EN_DIR = Path("/Users/gejiayu/owner/seo/data/religious-nonprofit-organization-tools")
ZH_DIR = Path("/Users/gejiayu/owner/seo/data-zh/religious-nonprofit-organization-tools")

# Ensure target directory exists
ZH_DIR.mkdir(parents=True, exist_ok=True)

# Get all English JSON files
en_files = sorted(EN_DIR.glob("*.json"))

print(f"Found {len(en_files)} English JSON files to process")

# Process each file
for i, en_file in enumerate(en_files, 1):
    filename = en_file.name
    zh_file = ZH_DIR / filename

    print(f"\n[{i}/{len(en_files)}] Processing: {filename}")

    # Read English JSON
    with open(en_file, 'r', encoding='utf-8') as f:
        en_data = json.load(f)

    # Generate Chinese JSON structure
    zh_data = {
        "title": f"[待翻译] {en_data['title']}",
        "description": f"[待翻译] {en_data['description'][:150]}...",
        "content": f"<p>[待翻译内容 - 原长度: {len(en_data['content'])} 字符]</p>",
        "seo_keywords": ["待翻译关键词"] * len(en_data.get('seo_keywords', [])),
        "slug": en_data['slug'],
        "published_at": en_data['published_at'],
        "author": en_data['author'],
        "language": "zh-CN",
        "canonical_link": en_data['canonical_link'].replace('/posts/', '/zh/posts/'),
        "alternate_links": {
            "zh-CN": en_data['canonical_link'].replace('/posts/', '/zh/posts/'),
            "en-US": en_data['canonical_link']
        },
        "category": en_data['category']
    }

    # Write placeholder Chinese JSON
    with open(zh_file, 'w', encoding='utf-8') as f:
        json.dump(zh_data, f, ensure_ascii=False, indent=2)

print(f"\n\nCompleted! Generated {len(en_files)} placeholder files")
print(f"Target directory: {ZH_DIR}")
print("\nNext: Use Claude to translate actual content for each file")