#!/usr/bin/env python3
"""Test translation with a single file."""
import json
from pathlib import Path
from deep_translator import GoogleTranslator

def test_translation():
    # Initialize translator
    translator = GoogleTranslator(source='zh-CN', target='en')

    # Test with first file
    filepath = Path('/Users/gejiayu/owner/seo/data/publishing-media-tools/academic-typesetting-tools-2026.json')

    print(f"Testing with: {filepath.name}")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"\nOriginal title: {data['title']}")
    print(f"Original author: {data['author']}")

    # Translate title
    translated_title = translator.translate(data['title'])
    print(f"\nTranslated title: {translated_title}")

    # Translate author
    translated_author = translator.translate(data['author'])
    print(f"Translated author: {translated_author}")

    print("\n✓ Test successful!")

if __name__ == '__main__':
    test_translation()