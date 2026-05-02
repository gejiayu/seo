#!/usr/bin/env python3
"""
Detect Chinese files in massage-spa-wellness-tools directory
"""
import json
import re
from pathlib import Path

# Chinese character regex
chinese_pattern = re.compile(r'[一-鿿]')

# Directory to scan
directory = Path('/Users/gejiayu/owner/seo/data/massage-spa-wellness-tools')

# Find all JSON files
json_files = sorted(directory.glob('*.json'))

print(f"Total JSON files found: {len(json_files)}\n")

# Check for Chinese content
chinese_files = []
for file_path in json_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

        # Check if file contains Chinese characters
        if chinese_pattern.search(content):
            chinese_files.append(file_path.name)

print(f"Files with Chinese content: {len(chinese_files)}\n")

# Show first 10 Chinese file names
print("First 10 Chinese files:")
for i, filename in enumerate(chinese_files[:10], 1):
    print(f"{i}. {filename}")

# Save list to file
output_file = Path('/Users/gejiayu/owner/seo/chinese_files_list.txt')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"Total: {len(chinese_files)}\n\n")
    for filename in chinese_files:
        f.write(f"{filename}\n")

print(f"\nFull list saved to: {output_file}")