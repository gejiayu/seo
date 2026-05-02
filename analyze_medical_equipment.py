#!/usr/bin/env python3
"""
Script to detect and fix broken machine translation in medical-equipment-rental-tools JSON files.
Two problems:
1. Chinese content needs translation
2. Broken machine translation (word concatenation without spaces)
"""

import json
import re
import os
from pathlib import Path

# Directory to process
DATA_DIR = "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools"

# Pattern to detect Chinese characters
CHINESE_PATTERN = re.compile(r'[一-鿿]')

# Pattern to detect broken machine translation (long concatenated words without spaces)
# Words like "diagnosticequipmentrentalmanagementsystemreview" (40+ chars, all lowercase, no spaces)
BROKEN_TRANSLATION_PATTERN = re.compile(r'[a-z]{30,}')

def analyze_file(filepath):
    """Analyze a JSON file for problems."""
    problems = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return [f"Error reading file: {e}"]

    # Check for Chinese content
    for key in ['title', 'description', 'content']:
        if key in data:
            if CHINESE_PATTERN.search(str(data[key])):
                problems.append(f"Chinese content in {key}")

    # Check for broken machine translation
    for key in ['title', 'description', 'content']:
        if key in data:
            text = str(data[key])
            # Find all broken words
            broken_words = BROKEN_TRANSLATION_PATTERN.findall(text)
            if broken_words:
                problems.append(f"Broken translation in {key}: {len(broken_words)} instances")
                # Show sample
                if len(broken_words) > 0:
                    problems.append(f"  Sample: {broken_words[0][:50]}...")

    # Check seo_keywords format
    if 'seo_keywords' in data:
        if isinstance(data['seo_keywords'], str):
            problems.append("seo_keywords is string, not array")
        elif isinstance(data['seo_keywords'], list):
            # Check if keywords themselves are broken
            for kw in data['seo_keywords']:
                if BROKEN_TRANSLATION_PATTERN.search(kw):
                    problems.append(f"Broken keyword: {kw[:30]}...")

    # Check if language field exists
    if 'language' not in data:
        problems.append("Missing 'language' field")

    return problems

def main():
    """Main analysis function."""
    files = sorted(Path(DATA_DIR).glob('*.json'))

    print(f"Total files: {len(files)}\n")

    files_with_problems = []

    for filepath in files:
        problems = analyze_file(filepath)
        if problems:
            files_with_problems.append((filepath.name, problems))

    print(f"Files with problems: {len(files_with_problems)}\n")

    # Show first 10 files with problems
    for filename, problems in files_with_problems[:10]:
        print(f"\n{filename}:")
        for p in problems:
            print(f"  - {p}")

    # Save full report
    report_file = Path(DATA_DIR) / 'analysis_report.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"Total files: {len(files)}\n")
        f.write(f"Files with problems: {len(files_with_problems)}\n\n")
        for filename, problems in files_with_problems:
            f.write(f"\n{filename}:\n")
            for p in problems:
                f.write(f"  - {p}\n")

    print(f"\nFull report saved to: {report_file}")

if __name__ == "__main__":
    main()