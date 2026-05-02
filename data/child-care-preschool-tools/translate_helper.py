#!/usr/bin/env python3
"""
Helper script for batch translating Chinese JSON files to English.
"""
import os
import json
import sys

def read_file(filepath):
    """Read a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_file(filepath, data):
    """Write a JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def update_file(filepath, title, description, content, seo_keywords):
    """Update a file with translated content."""
    data = read_file(filepath)
    data['title'] = title
    data['description'] = description
    data['content'] = content
    data['seo_keywords'] = seo_keywords
    write_file(filepath, data)
    print(f"Updated: {filepath}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        data = read_file(filepath)
        print(json.dumps(data, indent=2, ensure_ascii=False))