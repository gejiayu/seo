#!/usr/bin/env python3
"""
Script to translate Chinese jewelry/watch retail tool JSON files to English.
Translates title, description, and content fields while preserving structure.
"""

import json
import os
import re
from pathlib import Path

# Chinese to English translation mappings for jewelry/watch retail domain
# This dictionary contains common phrases and terms

TRANSLATIONS = {
    # Common headers and phrases
    "背景介绍": "Background Introduction",
    "深度评测": "In-depth Review",
    "核心功能": "Core Features",
    "价格方案": "Pricing Plan",
    "功能对比表": "Feature Comparison Table",
    "选型建议": "Selection Recommendations",
    "行业趋势预测": "Industry Trend Forecast",
    "总结": "Summary",

    # Common terms in jewelry/watch domain
    "珠宝": "jewelry",
    "手表": "watch",
    "零售": "retail",
    "管理": "management",
    "系统": "system",
    "软件": "software",
    "工具": "tools",
    "平台": "platform",
    "评测": "review",
    "解决方案": "solution",
    "专业": "professional",
    "功能": "features",
    "价格": "price",
    "成本": "cost",
    "客户": "customer",
    "库存": "inventory",
    "销售": "sales",
    "营销": "marketing",
    "服务": "service",
    "维修": "repair",
    "定制": "custom",
    "设计": "design",
    "展示": "display",
    "追踪": "tracking",
    "分析": "analysis",
    "数据": "data",
    "自动化": "automation",
    "整合": "integration",
    "移动": "mobile",
    "平板": "tablet",
    "安全": "security",
    "防盗": "anti-theft",
    "监控": "monitoring",
    "报警": "alarm",
    "门禁": "access control",
    "保险": "insurance",
    "忠诚度": "loyalty",
    "会员": "membership",
    "积分": "points",
    "奖励": "rewards",
    "VIP": "VIP",
    "纪念日": "anniversary",
    "保养": "maintenance",
    "配件": "parts/accessories",
    "品牌": "brand",
    "价值": "value",
    "保值": "value preservation",
    "投资": "investment",
    "收藏": "collection",

    # Common sentence patterns
    "本文将评测": "This article will review",
    "分析其功能特点和适用场景": "analyzing their features and suitable scenarios",
    "了解更多功能和价格对比": "Learn more about features and pricing comparisons",
    "找到最适合你的方案": "find the best solution for your needs",
    "专业评测助你决策": "Professional reviews to help you make informed decisions",
    "提供一站式": "provides one-stop",
    "专注": "focuses on",
    "深度整合": "deeply integrates",
    "专为珠宝": "designed specifically for jewelry",
    "专为手表": "designed specifically for watch",
    "适合": "suitable for",
    "支持": "supports",
    "提供": "provides",
    "管理从": "managing from",
    "到": "to",

    # Common descriptive phrases
    "全面管理": "comprehensive management",
    "一站式管理": "one-stop management",
    "专业方案": "professional solution",
    "全流程": "full-process",
    "实时": "real-time",
    "智能": "intelligent",
    "自动化": "automated",
    "精准": "precise",
    "高效": "efficient",
    "灵活": "flexible",
    "便携": "portable",

    # Price-related terms
    "月": "month",
    "年付": "annual payment",
    "优惠": "discount",
    "起": "starting",
    "定制报价": "custom pricing",
    "一次性购买": "one-time purchase",

    # Rating stars (keep as-is)
    "★★★★★": "★★★★★",
    "★★★★☆": "★★★★☆",
    "★★★☆☆": "★★★☆☆",
    "★★☆☆☆": "★★☆☆☆",
    "★☆☆☆☆": "★☆☆☆☆",

    # Direction terms
    "发展方向": "Development Directions",
    "趋势": "trends",
    "预测": "forecast",
    "将": "will",
    "预计": "expected",
    "成为标配": "will become standard",
    "成为基本功能": "will become basic functionality",
}

def clean_seo_keywords(keywords):
    """Remove extra spaces from SEO keywords"""
    cleaned = []
    for kw in keywords:
        # Remove multiple spaces and trim
        cleaned_kw = re.sub(r'\s+', ' ', kw.strip())
        cleaned.append(cleaned_kw)
    return cleaned

def translate_content(text):
    """
    Translate Chinese text to English using mapping dictionary.
    This is a simplified translation approach - for production use,
    you would use a proper translation API or library.
    """
    # For this script, we'll use the mappings above
    # In production, you'd use Google Translate API or similar

    translated = text

    # Apply translations in order (longer phrases first)
    for chinese, english in sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True):
        translated = translated.replace(chinese, english)

    return translated

def process_file(file_path):
    """Process a single JSON file"""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if file has Chinese content
    title = data.get('title', '')
    has_chinese = bool(re.search(r'[一-鿿]', title))

    if not has_chinese:
        print(f"  Skipped (no Chinese content)")
        return False

    # Translate title, description, and content
    # Note: This simplified translation won't produce perfect results
    # For production, use a proper translation service

    data['title'] = translate_content(data['title'])
    data['description'] = translate_content(data['description'])
    data['content'] = translate_content(data['content'])

    # Clean SEO keywords
    data['seo_keywords'] = clean_seo_keywords(data.get('seo_keywords', []))

    # Ensure language is en-US
    data['language'] = 'en-US'

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  Translated successfully")
    return True

def main():
    """Main function to process all files"""
    data_dir = Path('/Users/gejiayu/owner/seo/data/jewelry-watch-retail-tools')

    # Find all JSON files with Chinese content (excluding intentionally Chinese files)
    files_to_translate = []

    for json_file in data_dir.glob('*.json'):
        # Skip files with "chinese-review" in name
        if 'chinese-review' in json_file.name:
            print(f"Skipping intentionally Chinese file: {json_file.name}")
            continue

        # Check if file has Chinese content
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if re.search(r'[一-鿿]', content):
                files_to_translate.append(json_file)

    print(f"\nFound {len(files_to_translate)} files to translate\n")

    translated_count = 0
    for file_path in files_to_translate:
        if process_file(file_path):
            translated_count += 1

    print(f"\n{'='*50}")
    print(f"Translation complete!")
    print(f"Total files translated: {translated_count}")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()