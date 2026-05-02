import json
import re
from pathlib import Path
from typing import Dict, List

def contains_chinese(text: str) -> bool:
    """Check if text contains Chinese characters or punctuation"""
    chinese_pattern = re.compile(r'[一-鿿㐀-䶿豈-﫿，。、；：？！""''【】《》（）]+')
    return bool(chinese_pattern.search(text))

def get_file_list() -> List[str]:
    """Get list of Chinese files to process (positions 26-50)"""
    return [
        'candidate-drug-screening-tools-2026.json',
        'candidate-education-verification-tools-2026.json',
        'candidate-email-automation-tools-2026.json',
        'candidate-emergency-contact-tools-2026.json',
        'candidate-employment-verification-tools-2026.json',
        'candidate-equipment-management-tools-2026.json',
        'candidate-experience-management-tools-2026.json',
        'candidate-geolocation-analysis-tools-2026.json',
        'candidate-health-check-tools-2026.json',
        'candidate-identity-verification-tools-2026.json',
        'candidate-interview-evaluation-tools-2026.json',
        'candidate-language-assessment-tools-2026.json',
        'candidate-loyalty-scoring-tools-2026.json',
        'candidate-management-systems-2026.json',
        'candidate-notes-management-tools-2026.json',
        'candidate-offboarding-management-tools-2026.json',
        'candidate-onboarding-tools-2026.json',
        'candidate-performance-evaluation-tools-2026.json',
        'candidate-performance-prediction-tools-2026.json',
        'candidate-personality-assessment-tools-2026.json',
        'candidate-pipeline-management-tools-2026.json',
        'candidate-privacy-management-tools-2026.json',
        'candidate-profile-generation-tools-2026.json',
        'candidate-project-management-tools-2026.json'
    ]

def count_chinese_files(base_dir: Path, file_list: List[str]) -> Dict:
    """Count how many files still contain Chinese content"""
    stats = {
        'total': len(file_list),
        'with_chinese': 0,
        'without_chinese': 0,
        'missing_language': 0,
        'details': []
    }

    for filename in file_list:
        filepath = base_dir / filename
        if not filepath.exists():
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        has_chinese = False
        chinese_fields = []

        # Check all fields for Chinese content
        for field in ['title', 'description', 'content', 'author']:
            if field in data and contains_chinese(str(data[field])):
                has_chinese = True
                chinese_fields.append(field)

        # Check seo_keywords
        if 'seo_keywords' in data:
            for keyword in data['seo_keywords']:
                if contains_chinese(str(keyword)):
                    has_chinese = True
                    chinese_fields.append('seo_keywords')
                    break

        # Check if language field exists
        has_language = 'language' in data

        if has_chinese:
            stats['with_chinese'] += 1
        else:
            stats['without_chinese'] += 1

        if not has_language:
            stats['missing_language'] += 1

        stats['details'].append({
            'filename': filename,
            'has_chinese': has_chinese,
            'chinese_fields': chinese_fields,
            'has_language': has_language
        })

    return stats

def print_report(stats: Dict):
    """Print a comprehensive report"""
    print("="*60)
    print("Chinese Files Detection Report")
    print("="*60)
    print(f"\nTotal files in batch (26-50): {stats['total']}")
    print(f"Files with Chinese content: {stats['with_chinese']}")
    print(f"Files without Chinese content: {stats['without_chinese']}")
    print(f"Files missing 'language' field: {stats['missing_language']}")

    print("\nDetailed Analysis:")
    print("-"*60)

    for detail in stats['details']:
        status = "✗ NEEDS FIX" if detail['has_chinese'] else "✓ OK"
        print(f"\n{detail['filename']}: {status}")

        if detail['has_chinese']:
            print(f"  Chinese fields: {', '.join(detail['chinese_fields'])}")

        if not detail['has_language']:
            print(f"  Missing 'language' field")

def main():
    base_dir = Path('/Users/gejiayu/owner/seo/data/staffing-recruitment-agency-tools/')
    file_list = get_file_list()

    stats = count_chinese_files(base_dir, file_list)
    print_report(stats)

    # List files that need fixing
    print("\n" + "="*60)
    print("Files Requiring Translation")
    print("="*60)

    needs_fix = [d for d in stats['details'] if d['has_chinese']]
    if needs_fix:
        for i, detail in enumerate(needs_fix, 1):
            print(f"{i}. {detail['filename']}")
            print(f"   Fields: {', '.join(detail['chinese_fields'])}")
    else:
        print("✓ All files are properly translated!")

if __name__ == "__main__":
    main()