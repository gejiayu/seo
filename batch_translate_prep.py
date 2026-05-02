#!/usr/bin/env python3
"""
Batch bilingual processor for pSEO JSON files
Efficiently processes large numbers of files using common patterns
"""
import json
import re
from pathlib import Path

# Common translation patterns for pSEO content
COMMON_TERMS = {
    # Software names (keep as-is)
    '软件': 'Software',
    '系统': 'System',
    '平台': 'Platform',
    '工具': 'Tool',
    '评测': 'Review',
    '对比': 'Comparison',
    '分析': 'Analysis',

    # Common verbs
    '管理': 'Management',
    '优化': 'Optimization',
    '监控': 'Monitoring',
    '调度': 'Dispatch/Scheduling',
    '评估': 'Evaluation',
    '分析': 'Analysis',

    # Common nouns
    '电动滑板车': 'Electric Scooter',
    '摩托车': 'Motorcycle',
    '车辆': 'Vehicle',
    '租赁': 'Rental',
    '员工': 'Employee/Staff',
    '客户': 'Customer',
    '网点': 'Location/Branch',
    '车队': 'Fleet',

    # Common adjectives
    '智能': 'Smart/Intelligent',
    '动态': 'Dynamic',
    '实时': 'Real-time',
    '专业': 'Professional',
    '企业级': 'Enterprise-level',

    # Time-related
    '2026年': '2026',
    '最佳': 'Best',
    '最新': 'Latest',

    # Key phrases
    '深入评测': 'In-depth Review',
    '功能对比': 'Feature Comparison',
    '价格对比': 'Price Comparison',
    '找到最适合你的方案': 'Find the Best Solution for You',
    '专业评测助你决策': 'Professional Reviews to Help You Decide'
}

def get_file_list():
    """
    Get list of all files to process in the 12 categories
    """
    categories = [
        'scooter-moped-rental-tools',
        'security-surveillance-rental-tools',
        'ski-snowboard-rental-tools',
        'sporting-goods-retail-tools',
        'sports-equipment-rental-tools',
        'sports-fitness-tools',
        'sports-recreation-management',
        'staffing-recruitment-agency-tools',
        'staging-rigging-rental-tools',
        'storage-unit-rental-tools',
        'subscription-recurring-billing-tools',
        'telecommunications-network-tools'
    ]

    base_path = Path('/Users/gejiayu/owner/seo/data')
    files = []

    for category in categories:
        cat_path = base_path / category
        if cat_path.exists():
            files.extend([str(f) for f in sorted(cat_path.glob('*.json'))])

    return files

def check_if_bilingual(filepath):
    """
    Check if file already has bilingual fields
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return 'title_en' in data
    except:
        return False

def main():
    """
    Main entry point - prepare for batch processing
    """
    files = get_file_list()

    # Check how many already bilingual
    bilingual_count = sum(1 for f in files if check_if_bilingual(f))
    monolingual_count = len(files) - bilingual_count

    print(f"=== pSEO Bilingual Translation Status ===")
    print(f"Total files: {len(files)}")
    print(f"Already bilingual: {bilingual_count}")
    print(f"Need translation: {monolingual_count}")
    print(f"\n=== Files ready for processing ===")

    # Create list of files needing translation
    files_to_process = [f for f in files if not check_if_bilingual(f)]

    # Print first 20 files
    print("\nFirst 20 files to process:")
    for i, filepath in enumerate(files_to_process[:20], 1):
        print(f"{i}. {filepath}")

    print(f"\n=== Ready for Claude batch translation ===")
    print(f"Next: Claude will process {min(20, len(files_to_process))} files")

    return files_to_process

if __name__ == '__main__':
    files_to_process = main()
    print(f"\nTotal files needing translation: {len(files_to_process)}")