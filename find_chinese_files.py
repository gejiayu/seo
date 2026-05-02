import json
import re
from pathlib import Path

def contains_chinese(text):
    """Check if text contains Chinese characters (more comprehensive pattern)"""
    # Match Chinese characters in multiple Unicode ranges
    chinese_pattern = re.compile(r'[一-鿿㐀-䶿豈-﫿]+')
    return bool(chinese_pattern.search(text))

def check_file_for_chinese(filepath):
    """Check if JSON file contains Chinese content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check all relevant fields
        fields_to_check = ['title', 'description', 'content', 'author']
        for field in fields_to_check:
            if field in data and isinstance(data[field], str) and contains_chinese(data[field]):
                return True

        # Check seo_keywords array
        if 'seo_keywords' in data:
            for keyword in data['seo_keywords']:
                if isinstance(keyword, str) and contains_chinese(keyword):
                    return True

        return False
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

def main():
    base_dir = Path('/Users/gejiayu/owner/seo/data/staffing-recruitment-agency-tools/')

    # List all files sorted
    all_files = sorted([f for f in base_dir.glob('*.json') if f.is_file()])

    # Select files 26-50 (indices 25-49 in 0-based)
    target_files = all_files[25:50]

    print(f"Processing files 26-50 (total {len(target_files)} files)")

    chinese_files = []
    for i, filepath in enumerate(target_files, start=26):
        if check_file_for_chinese(filepath):
            chinese_files.append((i, filepath))
            print(f"✓ File #{i}: {filepath.name} - Contains Chinese")

    print(f"\nTotal Chinese files found: {len(chinese_files)}")

    return chinese_files

if __name__ == "__main__":
    chinese_files = main()
    print("\nFiles to fix:")
    for idx, filepath in chinese_files:
        print(f"  {idx}. {filepath.name}")