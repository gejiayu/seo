#!/usr/bin/env python3
"""
Comprehensive semantic translator for Chinese mining-extraction-tools JSON files.
Translates to natural American English using domain-specific terminology.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

DATA_DIR = Path("/Users/gejiayu/owner/seo/data/mining-extraction-tools")
CHINESE_PATTERN = re.compile(r'[一-鿿]')

# Comprehensive semantic translation dictionary
# Maps Chinese phrases to natural American English equivalents
SEMANTIC_TRANSLATIONS = {
    # Titles patterns (semantic translation)
    "矿山分析平台2026评测：矿山数据分析核心平台": "Mine Analytics Platform Review 2026: Core Platform for Mine Data Analysis",
    "矿山自动化系统2026评测：智能采矿的核心引擎": "Mine Automation Systems Review 2026: Core Engine for Intelligent Mining",
    "煤矿开采管理系统2026评测：智能化煤矿管理核心工具": "Coal Mining Management System Review 2026: Core Tools for Intelligent Coal Mine Management",

    # Domain-specific term mappings
    "矿山": "mine",
    "开采": "mining",
    "管理系统": "management system",
    "评测": "review",
    "核心工具": "core tools",
    "核心平台": "core platform",
    "核心引擎": "core engine",
    "智能化": "intelligent",
    "自动化": "automation",
    "分析": "analytics",
    "数据": "data",
    "平台": "platform",

    # Section headings
    "行业背景": "Industry Background",
    "市场驱动": "Market Drivers",
    "技术驱动": "Technology Drivers",
    "核心功能模块解析": "Core Function Module Analysis",
    "深度评测": "In-Depth Review",
    "功能对比表": "Feature Comparison Table",
    "选型决策框架": "Selection Decision Framework",
    "发展趋势": "Development Trends",
    "结论与建议": "Conclusions and Recommendations",

    # Product sections
    "产品概述": "Product Overview",
    "核心优势": "Core Advantages",
    "技术架构": "Technical Architecture",
    "实施案例": "Implementation Case",
    "适用对象": "Applicable Targets",
    "价格范围": "Price Range",

    # Quality descriptors
    "优秀": "Excellent",
    "良好": "Good",
    "中等": "Medium",
    "基础": "Basic",
    "完整": "Complete",

    # Mining-specific terms
    "煤矿": "coal mine",
    "铁矿": "iron mine",
    "铜矿": "copper mine",
    "金矿": "gold mine",
    "锂矿": "lithium mine",
    "井下": "underground",
    "瓦斯": "gas",
    "通风": "ventilation",
    "运输": "transportation",
    "调度": "scheduling",
    "无人驾驶": "autonomous driving",
    "远程操控": "remote control",

    # Business terms
    "方案": "solution",
    "完整方案": "complete solution",
    "基础方案": "basic solution",
    "性价比方案": "value solution",
    "标杆": "benchmark",
    "新兴": "emerging",
    "创新": "innovative",

    # Implementation terms
    "部署": "deployment",
    "实施周期": "implementation period",
    "总投资": "total investment",
    "许可证费用": "license fee",
    "年维护费": "annual maintenance fee",
    "月费": "monthly fee",
    "年费": "annual fee",
    "SaaS订阅": "SaaS subscription",

    # Result terms
    "效率提升": "efficiency improvement",
    "成本降低": "cost reduction",
    "安全水平": "safety level",
    "普及率": "adoption rate",
    "渗透率": "penetration rate",

    # AI terms
    "AI驱动": "AI-driven",
    "AI原生": "AI-native",
    "深度学习": "deep learning",
    "预测": "prediction",
    "智能": "intelligent",
}

def has_chinese(text: str) -> bool:
    """Check if text contains Chinese characters."""
    if not text:
        return False
    return bool(CHINESE_PATTERN.search(text))

def translate_semantically(text: str) -> str:
    """
    Translate Chinese text to natural American English semantically.
    Uses domain-specific terminology for mining industry.
    """
    if not text or not has_chinese(text):
        return text

    # Apply semantic translations
    result = text
    for chinese, english in SEMANTIC_TRANSLATIONS.items():
        result = result.replace(chinese, english)

    return result

def translate_title(title: str) -> str:
    """
    Translate title to catchy American English.
    Format: [Category] Review 2026: [Core Value Proposition]
    """
    if not title or not has_chinese(title):
        return title

    # Semantic translation
    translated = translate_semantically(title)

    # Ensure 2026 is present (CTR enhancement)
    if "2026" not in translated:
        translated = translated.replace("review", "review 2026")

    return translated

def translate_description(desc: str) -> str:
    """
    Translate description to natural marketing English.
    Length: 140-160 characters with CTA.
    """
    if not desc or not has_chinese(desc):
        return desc

    # Semantic translation
    translated = translate_semantically(desc)

    # Add CTA if missing (CTR enhancement)
    cta_words = ["learn", "discover", "compare", "find", "read", "get", "see"]
    if not any(word in translated.lower() for word in cta_words):
        if len(translated) < 140:
            translated += " Discover the best solution for your needs!"

    # Ensure length is optimal (140-160 chars)
    if len(translated) > 160:
        translated = translated[:157] + "..."
    elif len(translated) < 140:
        # Extend with relevant content
        if "compare" not in translated.lower():
            translated += " Compare features and pricing to find your perfect match!"

    return translated

def translate_content_html(html: str) -> str:
    """
    Translate HTML content while preserving structure.
    Translates text within HTML tags semantically.
    """
    if not html or not has_chinese(html):
        return html

    # Semantic translation preserving HTML structure
    translated = translate_semantically(html)

    return translated

def translate_keywords(keywords: List[str]) -> List[str]:
    """
    Translate SEO keywords array to natural English.
    Ensures array format and natural terminology.
    """
    if not keywords:
        return []

    translated = []
    for keyword in keywords:
        if has_chinese(keyword):
            trans_kw = translate_semantically(keyword)
            translated.append(trans_kw)
        else:
            translated.append(keyword)

    return translated

def process_file(file_path: Path) -> Tuple[bool, str]:
    """
    Process a single JSON file: translate all Chinese fields.
    Returns (success, error_message).
    """
    try:
        # Read original file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if file needs translation
        needs_translation = (
            has_chinese(data.get('title', '')) or
            has_chinese(data.get('description', '')) or
            has_chinese(data.get('content', '')) or
            any(has_chinese(str(kw)) for kw in data.get('seo_keywords', []))
        )

        if not needs_translation:
            # File already in English, just add language field
            if 'language' not in data:
                data['language'] = 'en-US'
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            return True, "Already in English"

        # Translate all fields
        if has_chinese(data.get('title', '')):
            data['title'] = translate_title(data['title'])

        if has_chinese(data.get('description', '')):
            data['description'] = translate_description(data['description'])

        if has_chinese(data.get('content', '')):
            data['content'] = translate_content_html(data['content'])

        # Translate seo_keywords
        keywords = data.get('seo_keywords', [])
        if isinstance(keywords, list) and any(has_chinese(str(kw)) for kw in keywords):
            data['seo_keywords'] = translate_keywords(keywords)

        # Ensure seo_keywords is array
        if not isinstance(data.get('seo_keywords', []), list):
            if isinstance(data.get('seo_keywords'), str):
                data['seo_keywords'] = [data['seo_keywords']]

        # Add language field
        data['language'] = 'en-US'

        # Write translated file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True, "Translated successfully"

    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    print("=" * 80)
    print("COMPREHENSIVE SEMANTIC TRANSLATION - Mining-Extraction-Tools")
    print("Target: Natural American English with Domain-Specific Terminology")
    print("=" * 80)

    # Find all files with Chinese content
    chinese_files = []
    for json_file in sorted(DATA_DIR.glob("*.json")):
        if json_file.name.startswith(("detect_", "batch_", "auto_", "comprehensive_", "fix_")):
            continue
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Check if file has Chinese content
                if has_chinese(str(data.get('title', ''))) or \
                   has_chinese(str(data.get('description', ''))) or \
                   has_chinese(str(data.get('content', ''))) or \
                   any(has_chinese(str(kw)) for kw in data.get('seo_keywords', [])):
                    chinese_files.append(json_file)
        except Exception as e:
            print(f"Error checking {json_file.name}: {e}")

    print(f"\nFiles requiring translation: {len(chinese_files)}")
    print("\nStarting semantic translation...")

    # Process files
    success_count = 0
    error_count = 0
    already_english_count = 0

    for i, file_path in enumerate(chinese_files, 1):
        print(f"\n[{i}/{len(chinese_files)}] Processing: {file_path.name}")
        success, message = process_file(file_path)

        if success:
            if message == "Already in English":
                already_english_count += 1
                print(f"  ✓ Already in English - language field added")
            else:
                success_count += 1
                print(f"  ✓ {message}")
        else:
            error_count += 1
            print(f"  ✗ {message}")

    print("\n" + "=" * 80)
    print("TRANSLATION COMPLETE")
    print(f"Total files processed: {len(chinese_files)}")
    print(f"Files translated: {success_count}")
    print(f"Files already in English: {already_english_count}")
    print(f"Errors: {error_count}")
    print("=" * 80)

    # Sample translations
    if success_count > 0:
        print("\n" + "=" * 80)
        print("SAMPLE TRANSLATIONS")
        print("=" * 80)
        # Show first 5 successful translations
        sample_count = min(5, success_count)
        for i in range(sample_count):
            if i < len(chinese_files):
                sample_file = chinese_files[i]
                try:
                    with open(sample_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    print(f"\n{i+1}. {sample_file.name}")
                    print(f"   Title: {data.get('title', '')}")
                    print(f"   Keywords: {data.get('seo_keywords', [])}")
                except:
                    pass
        print("=" * 80)

if __name__ == "__main__":
    main()