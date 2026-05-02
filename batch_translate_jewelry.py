#!/usr/bin/env python3
"""
Batch translation script for jewelry/watch retail tool JSON files.
This script prepares files for translation and tracks progress.
"""

import json
import os
import re
from pathlib import Path

def get_files_to_translate():
    """Get list of files that need translation"""
    data_dir = Path('/Users/gejiayu/owner/seo/data/jewelry-watch-retail-tools')
    
    files = []
    for json_file in data_dir.glob('*.json'):
        # Skip files with "chinese-review" in name
        if 'chinese-review' in json_file.name:
            continue
        
        # Check if file has Chinese content
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if re.search(r'[一-鿿]', content):
                files.append(json_file.name)
    
    return sorted(files)

def main():
    files = get_files_to_translate()
    print(f"Files requiring translation ({len(files)} total):")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")

if __name__ == '__main__':
    main()
