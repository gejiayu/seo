#!/usr/bin/env python3
"""
Manual batch translator with retry logic.
"""
import json
import os
import re
import time
from pathlib import Path
from deep_translator import GoogleTranslator

DATA_DIR = Path("/Users/gejiayu/owner/seo/data/architecture-design-tools")

files_to_process = [
    "architecture-design-software-plugins-review-2026.json",
    "architecture-design-software-rendering-engine-review-2026.json",
    "architecture-design-software-user-experience-review-2026.json",
    "architecture-quality-inspection-software-review.json",
    "best-architecture-design-software-guide.json",
    "bim-software-complete-review-guide.json"
]

def translate_with_retry(text, translator, max_retries=3):
    """Translate text with retry logic."""
    for i in range(max_retries):
        try:
            # Split into smaller chunks
            if len(text) > 3000:
                parts = text.split('</p><p>')
                translated_parts = []
                for part in parts:
                    if re.search(r'[一-鿿]', part):
                        translated = translator.translate(part)
                        translated_parts.append(translated)
                        time.sleep(1)  # Add delay to avoid rate limiting
                    else:
                        translated_parts.append(part)
                return '</p><p>'.join(translated_parts)
            else:
                if re.search(r'[一-鿿]', text):
                    return translator.translate(text)
                return text
        except Exception as e:
            print(f"Retry {i+1}/{max_retries} failed: {e}")
            time.sleep(2)
            continue
    return text

translator = GoogleTranslator(source='zh-CN', target='en')

for filename in files_to_process:
    file_path = DATA_DIR / filename
    if file_path.exists():
        print(f"\nProcessing: {filename}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check for Chinese
            content = data.get('content', '')
            if re.search(r'[一-鿿]', content):
                print(f"  Found Chinese content, translating...")
                translated_content = translate_with_retry(content, translator)
                data['content'] = translated_content

                # Write back
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                print(f"  ✓ Translated: {filename}")
            else:
                print(f"  ✓ No Chinese content")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    else:
        print(f"File not found: {filename}")

print("\n" + "="*60)
print("Translation complete!")
print("="*60)