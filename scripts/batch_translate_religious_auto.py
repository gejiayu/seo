#!/usr/bin/env python3
"""
Batch translate remaining religious nonprofit organization tools from English to Chinese
Uses Claude API for high-quality translations
"""

import json
import subprocess
from pathlib import Path
import sys

# Configuration
EN_DIR = Path("/Users/gejiayu/owner/seo/data/religious-nonprofit-organization-tools")
ZH_DIR = Path("/Users/gejiayu/owner/seo/data-zh/religious-nonprofit-organization-tools")

# Get all English files
all_files = sorted(EN_DIR.glob("*.json"))

# Filter remaining files
remaining_files = [f for f in all_files if not (ZH_DIR / f.name).exists()]

print(f"Total files: {len(all_files)}")
print(f"Remaining files to process: {len(remaining_files)}")
print("\nProcessing remaining files...\n")

# Process each remaining file
for i, en_file in enumerate(remaining_files, 1):
    filename = en_file.name
    print(f"[{i}/{len(remaining_files)}] {filename}")

    # Read English content
    with open(en_file, 'r', encoding='utf-8') as f:
        en_data = json.load(f)

    # Create prompt for Claude
    prompt = f"""Translate the following JSON content to Chinese. Output ONLY the complete JSON content (no explanations).

Requirements:
1. title: Translate to Chinese with attraction words (最佳/十大/完整指南) and 2026 time marker
2. description: Translate to Chinese, 140-160 chars, include CTA (发现/找到/探索)
3. content: Translate ALL HTML content to Chinese, keep HTML structure intact (no Markdown)
4. seo_keywords: Translate to Chinese keywords, MUST be array format ["keyword1", "keyword2"]
5. language: Change to "zh-CN"
6. canonical_link: Change to Chinese version (replace /posts/ with /zh/posts/)
7. alternate_links: Update with zh-CN as canonical, en-US as alternate
8. Keep same: slug, published_at (use "2026-05-02"), author, category

English JSON:
{json.dumps(en_data, ensure_ascii=False, indent=2)}

Output Chinese JSON now:"""

    # Call Claude to translate
    try:
        result = subprocess.run(
            ['claude', '--print', prompt],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            # Parse Claude's response
            zh_json_str = result.stdout.strip()

            # Remove any markdown code blocks if present
            if zh_json_str.startswith('```'):
                zh_json_str = zh_json_str.split('\n', 1)[1]
            if zh_json_str.endswith('```'):
                zh_json_str = zh_json_str.rsplit('\n', 1)[0]
            if zh_json_str.startswith('json\n'):
                zh_json_str = zh_json_str[5:]

            # Parse JSON
            zh_data = json.loads(zh_json_str)

            # Validate required fields
            assert 'seo_keywords' in zh_data and isinstance(zh_data['seo_keywords'], list)
            assert 'language' in zh_data and zh_data['language'] == 'zh-CN'
            assert 'canonical_link' in zh_data and '/zh/posts/' in zh_data['canonical_link']

            # Write Chinese JSON
            zh_file = ZH_DIR / filename
            with open(zh_file, 'w', encoding='utf-8') as f:
                json.dump(zh_data, f, ensure_ascii=False, indent=2)

            print(f"  ✓ Success")
        else:
            print(f"  ✗ Error: {result.stderr}")

    except subprocess.TimeoutExpired:
        print(f"  ✗ Timeout")
    except json.JSONDecodeError as e:
        print(f"  ✗ JSON Error: {e}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Small delay to avoid rate limits
    if i % 5 == 0:
        print(f"\n--- Batch {i//5} completed ---\n")

print(f"\n\nCompleted! Processed {len(remaining_files)} files")
print(f"Chinese directory: {ZH_DIR}")