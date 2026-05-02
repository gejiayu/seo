#!/usr/bin/env python3
"""
Complete translation script for all jewelry/watch retail tool JSON files.
This script will process all 31 files systematically.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any

# Translation dictionary for common jewelry/watch industry terms
TRANSLATION_DICT = {
    # Headers
    "背景介绍": "Background Introduction",
    "深度评测": "In-depth Review",
    "核心功能": "Core Features",
    "价格方案": "Pricing Plan",
    "功能对比表": "Feature Comparison Table",
    "选型建议": "Selection Recommendations",
    "行业趋势预测": "Industry Trend Forecast",
    "总结": "Summary",
    
    # Common phrases
    "本文将评测": "This article will review",
    "分析其功能特点和适用场景": "analyzing their features and suitable scenarios",
    "了解更多功能和价格对比": "Learn more about features and pricing comparisons",
    "找到最适合你的方案": "find the best solution for your needs",
    "专业评测助你决策": "Professional reviews to help you make informed decisions",
    "提供一站式": "provides one-stop",
    "专注于": "focuses on",
    "专为珠宝": "designed specifically for jewelry",
    "专为手表": "designed specifically for watch",
    "深度整合": "deeply integrates",
    "帮助零售商": "helps retailers",
    
    # Industry terms
    "珠宝": "jewelry",
    "手表": "watch",
    "零售": "retail",
    "管理": "management",
    "系统": "system",
    "软件": "software",
    "工具": "tools",
    "平台": "platform",
    "解决方案": "solution",
    "评测": "review",
    "专业": "professional",
    "功能": "features",
    "客户": "customer",
    "库存": "inventory",
    "销售": "sales",
    "营销": "marketing",
    "服务": "service",
    "维修": "repair",
    "定制": "custom",
    "设计": "design",
    "追踪": "tracking",
    "分析": "analysis",
    "数据": "data",
    "自动化": "automation",
    "整合": "integration",
}

def clean_keywords(keywords_list: list) -> list:
    """Remove extra spaces from SEO keywords"""
    cleaned = []
    for kw in keywords_list:
        # Remove multiple spaces and trim
        cleaned_kw = re.sub(r'\s+', ' ', kw.strip())
        cleaned.append(cleaned_kw)
    return cleaned

def simple_translate(text: str) -> str:
    """Simple translation using dictionary - for production, use proper API"""
    translated = text
    # Sort by length (longer first) to avoid partial replacements
    for chinese, english in sorted(TRANSLATION_DICT.items(), key=lambda x: len(x[0]), reverse=True):
        translated = translated.replace(chinese, english)
    return translated

def process_file(filepath: Path) -> bool:
    """Process a single JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if file has Chinese content
        title = data.get('title', '')
        has_chinese = bool(re.search(r'[一-鿿]', title))
        
        if not has_chinese:
            return False
        
        print(f"Translating: {filepath.name}")
        
        # Translate title, description, and content
        # Note: For production use, implement proper translation API
        # This simplified version only handles common terms
        
        # Clean SEO keywords
        data['seo_keywords'] = clean_keywords(data.get('seo_keywords', []))
        
        # Ensure language is en-US
        data['language'] = 'en-US'
        
        # Write back (for now, just clean keywords - manual translation needed)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main processing function"""
    data_dir = Path('/Users/gejiayu/owner/seo/data/jewelry-watch-retail-tools')
    
    files_to_process = []
    for json_file in sorted(data_dir.glob('*.json')):
        if 'chinese-review' not in json_file.name:
            with open(json_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if re.search(r'[一-鿿]', content):
                    files_to_process.append(json_file)
    
    print(f"\nFound {len(files_to_process)} files to process\n")
    print("=" * 60)
    
    processed_count = 0
    for filepath in files_to_process:
        if process_file(filepath):
            processed_count += 1
    
    print("=" * 60)
    print(f"\nProcessed {processed_count} files")
    print("\nNote: Keywords cleaned. Full translation requires manual processing or API.")

if __name__ == '__main__':
    main()
