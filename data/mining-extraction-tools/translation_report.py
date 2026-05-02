#!/usr/bin/env python3
"""
Batch Translation Script for Chinese JSON Files
Processes files 1-20 from mining-extraction-tools directory
"""

import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path("/Users/gejiayu/owner/seo/data/mining-extraction-tools")

# Files that need translation (from first 20)
FILES_TO_TRANSLATE = [
    "iron-mining-management-system-2026.json",
    "lithium-mining-management-system-2026.json",
    "mine-analytics-platform-2026.json",
    "mine-asset-tracking-system-2026.json",
    "mine-automation-systems-review-2026.json",
    "mine-budget-management-system-2026.json",
    "mine-cloud-platform-system-2026.json",
    "mine-collaboration-platform-2026.json",
    "mine-community-management-system-2026.json",
    "mine-compliance-audit-system-2026.json",
    "mine-compliance-management-system-2026.json",
    "mine-contractor-management-system-2026.json",
    "mine-cost-management-system-2026.json",
    "mine-crushing-control-system-2026.json",
    "mine-cyber-security-system-2026.json",
    "mine-dashboard-platform-2026.json",
    "mine-data-analytics-platform-2026.json",
]

# Files already processed (have language: en-US but mixed content)
MIXED_CONTENT_FILES = [
    "mine-analytics-platform-2026.json",
    "mine-asset-tracking-system-2026.json",
    "mine-automation-systems-review-2026.json",
    "mine-budget-management-system-2026.json",
]

def main():
    print("="*60)
    print("Chinese File Translation Analysis Report")
    print("="*60)
    print()

    print("Total files to process from list (1-20): 20")
    print("Files already in English: 3")
    print("  - copper-mining-management-system-2026.json")
    print("  - gold-mining-management-system-2026.json")
    print("  - mine-carbon-management-system-2026.json")
    print()

    print(f"Files requiring translation: {len(FILES_TO_TRANSLATE)}")
    print()

    print("Status Analysis:")
    print("-"*60)

    for i, filename in enumerate(FILES_TO_TRANSLATE, 1):
        filepath = DATA_DIR / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            has_language = 'language' in data
            title_preview = data.get('title', '')[:50]

            print(f"{i}. {filename}")
            print(f"   Language field: {'YES' if has_language else 'NO'}")
            print(f"   Title preview: {title_preview}...")

            if filename in MIXED_CONTENT_FILES:
                print(f"   Status: MIXED Chinese-English (needs proper translation)")
            else:
                print(f"   Status: PURE Chinese (needs full translation)")
            print()

    print("="*60)
    print("Recommendation:")
    print("="*60)
    print("1. Stop the Next.js dev server to prevent file reverts")
    print("2. Use semantic AI translation for natural American English")
    print("3. Process files in batches to manage complexity")
    print("4. Verify translations after completion")
    print()

    print("Next Steps:")
    print("- Stop dev server: pkill -f 'next dev'")
    print("- Translate files 1-5 first")
    print("- Restart dev server after completion")

if __name__ == "__main__":
    main()