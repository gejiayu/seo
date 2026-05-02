#!/usr/bin/env python3
"""
Batch translator for architecture-design-tools JSON files.
Translates Chinese content to proper English.
"""
import json
import os
import re
from pathlib import Path

DATA_DIR = Path("/Users/gejiayu/owner/seo/data/architecture-design-tools")

# Translation mappings for common mixed terms
TERM_MAPPINGS = {
    "Corevalue": "Core Value",
    "Coreadvantages": "Core Advantages",
    "CoreFeatures": "Core Features",
    "In-depthReview": "In-depth Review",
    "ComparisonTable": "Comparison Table",
    "real-time": "real-time",
    "None缝": "seamless",
    "None障碍": "barrier-free",
    "function": "function",
    "capabilities": "capabilities",
    "optimization": "optimization",
    "integration": "integration",
    "improvement": "improvement",
    "enhancement": "enhancement",
    "configuration": "configuration",
    "applications": "applications",
    "intelligence": "intelligence",
    "digitalization": "digitalization",
    "fair": "fair",
    "flexible": "flexible",
    "efficient": "efficient",
    "comprehensive": "comprehensive",
    "precise": "precise",
    "Custom": "Custom",
    "rich": "rich",
    "fast": "fast",
    "smart": "smart",
    "intuitive": "intuitive",
    "Excellent": "Excellent",
    "Good": "Good",
    "Basic": "Basic",
    "Limited": "Limited",
}

def has_chinese(text):
    """Check if text contains Chinese characters."""
    return bool(re.search(r'[一-鿿]', text))

def get_files_to_translate():
    """Get list of files that need translation."""
    files = []
    for file_path in DATA_DIR.glob('*.json'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('language') == 'en-US' and has_chinese(data.get('content', '')):
                    files.append(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    return sorted(files)

def main():
    """Main function."""
    files = get_files_to_translate()
    print(f"Found {len(files)} files needing translation")
    for i, file_path in enumerate(files, 1):
        print(f"{i}. {file_path.name}")

if __name__ == '__main__':
    main()