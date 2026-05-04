#!/usr/bin/env python3
"""
Final cleanup - fix truncated endings and ensure all descriptions are complete.
"""

import json
import re
from pathlib import Path

DATA_DIR = Path("data")

def fix_truncated_endings(desc: str) -> str:
    """Fix truncated endings in descriptions."""
    # Fix common truncations
    replacements = {
        r'Ideal\s+for\s+m\.': 'Ideal for modern operations.',
        r'Ideal\s+for\s+mod\.': 'Ideal for modern operations.',
        r'Ideal\s+for\s+modern\s+b\.': 'Ideal for modern businesses.',
        r'Ideal\s+for\s+modern\s+bus\.': 'Ideal for modern businesses.',
        r'Automate\s+op\.': 'Automate operations.',
        r'Automate\s+oper\.': 'Automate operations.',
        r'for\s+y\.': 'for your business.',
        r'for\s+yo\.': 'for your business.',
        r'for\s+your\s+b\.': 'for your business.',
        r'\s+[a-z]{1,2}\.$': '.',  # Remove trailing single letters
    }

    for pattern, replacement in replacements.items():
        desc = re.sub(pattern, replacement, desc)

    # Ensure description ends properly
    if not desc.endswith('.') and not desc.endswith('!'):
        desc += '.'

    return desc

def process_all_files():
    """Process all files and fix truncated endings."""
    print("Fixing truncated endings in descriptions...\n")

    fixed_count = 0

    for json_file in DATA_DIR.rglob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            desc = data['description']
            fixed_desc = fix_truncated_endings(desc)

            if fixed_desc != desc:
                data['description'] = fixed_desc

                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                print(f"Fixed: {json_file.name}")
                print(f"  Before: {desc}")
                print(f"  After:  {fixed_desc}\n")
                fixed_count += 1

        except Exception as e:
            print(f"Error: {json_file.name} - {e}")

    print(f"\n✅ Fixed {fixed_count} files with truncated endings")

if __name__ == "__main__":
    process_all_files()