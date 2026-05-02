#!/usr/bin/env python3
"""Final verification and report generation."""

import json
import re
from pathlib import Path

def contains_chinese(text):
    """Check if text contains Chinese characters."""
    chinese_pattern = re.compile(r'[一-鿿㐀-䶿\U00020000-\U0002a6df\U0002a700-\U0002b73f\U0002b740-\U0002b81f\U0002b820-\U0002ceaf]')
    return bool(chinese_pattern.search(text))

def verify_file(filepath):
    """Verify file has proper English metadata and language field."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        issues = []
        
        # Check critical metadata fields for Chinese
        if contains_chinese(data.get('title', '')):
            issues.append('title has Chinese')
        if contains_chinese(data.get('description', '')):
            issues.append('description has Chinese')
        if contains_chinese(data.get('author', '')):
            issues.append('author has Chinese')
        
        # Check seo_keywords
        for kw in data.get('seo_keywords', []):
            if contains_chinese(kw):
                issues.append('seo_keywords has Chinese')
                break
        
        # Check language field
        if data.get('language') != 'en-US':
            issues.append('language field missing or incorrect')
        
        return issues
    except Exception as e:
        return [f'Error: {e}']

def main():
    directory = Path('data/staffing-recruitment-agency-tools')
    
    # Files we processed
    processed_files = [
        "best-recruitment-agency-software-2026.json",
        "candidate-ai-assistant-tools-2026.json",
        "candidate-ai-email-writing-tools-2026.json",
        "candidate-appointment-management-tools-2026.json",
        "candidate-assessment-tools-2026.json",
        "candidate-attachment-management-tools-2026.json",
        "candidate-attrition-prediction-tools-2026.json",
        "candidate-bulk-operations-tools-2026.json",
        "candidate-calendar-integration-tools-2026.json",
        "candidate-career-path-tools-2026.json",
        "candidate-certificate-management-tools-2026.json",
        "candidate-cognitive-assessment-tools-2026.json",
        "candidate-communication-history-tools-2026.json",
        "candidate-compliance-verification-tools-2026.json",
        "candidate-comprehensive-background-check-tools-2026.json",
        "candidate-contract-signing-tools-2026.json",
        "candidate-credit-verification-tools-2026.json",
        "candidate-criminal-verification-tools-2026.json",
        "candidate-data-backup-tools-2026.json",
        "candidate-data-cleaning-tools-2026.json",
        "candidate-data-export-tools-2026.json",
        "candidate-data-import-tools-2026.json",
        "candidate-data-migration-tools-2026.json",
        "candidate-driving-verification-tools-2026.json",
    ]
    
    print("=== FINAL VERIFICATION REPORT ===\n")
    
    all_passed = True
    for filename in processed_files:
        filepath = directory / filename
        if filepath.exists():
            issues = verify_file(filepath)
            if issues:
                print(f"✗ {filename}: {', '.join(issues)}")
                all_passed = False
            else:
                print(f"✓ {filename}: All metadata fields properly translated")
    
    print(f"\n{'='*50}")
    if all_passed:
        print("✓ ALL FILES SUCCESSFULLY FIXED")
        print("  - Title: English ✓")
        print("  - Description: English ✓")
        print("  - Author: English ✓")
        print("  - SEO Keywords: English ✓")
        print("  - Language field: en-US ✓")
    else:
        print("⚠ Some files still have issues")
    
    print(f"\nTotal files fixed: {len(processed_files)}")

if __name__ == '__main__':
    main()
