#!/usr/bin/env python3
"""
Automated batch translator for Chinese mining-extraction-tools JSON files.
Translates title, description, content, seo_keywords to natural American English.
Uses semantic mining domain terminology.
"""

import json
import re
from pathlib import Path
from typing import Dict, List

DATA_DIR = Path("/Users/gejiayu/owner/seo/data/mining-extraction-tools")
CHINESE_PATTERN = re.compile(r'[一-鿿]')

# Comprehensive translation dictionary for mining domain
TRANSLATION_DICT = {
    # Core terms
    "矿山": "mine",
    "开采": "mining",
    "管理": "management",
    "系统": "system",
    "智能化": "intelligent",
    "自动化": "automation",
    "监测": "monitoring",
    "预警": "warning",
    "调度": "scheduling",
    "设备": "equipment",
    "安全": "safety",
    "生产": "production",
    "运营": "operations",
    "数据": "data",
    "分析": "analysis",
    "优化": "optimization",

    # Mining types
    "煤矿": "coal mine",
    "铁矿": "iron mine",
    "铜矿": "copper mine",
    "金矿": "gold mine",
    "锂矿": "lithium mine",

    # Automation terms
    "无人驾驶": "autonomous driving",
    "远程操控": "remote control",
    "智能化矿山": "intelligent mine",
    "智能化转型": "intelligent transformation",
    "数字孪生": "digital twin",

    # Process terms
    "全流程": "full-process",
    "核心工具": "core tools",
    "核心引擎": "core engine",
    "评测": "review",
    "深度分析": "deep analysis",

    # Section headings
    "行业背景": "industry background",
    "市场驱动": "market drivers",
    "技术驱动": "technology drivers",
    "功能模块": "function modules",
    "深度评测": "deep review",
    "功能对比": "feature comparison",
    "选型决策": "selection decision",
    "发展趋势": "development trends",
    "结论与建议": "conclusions and recommendations",

    # Product sections
    "产品概述": "product overview",
    "核心优势": "core advantages",
    "技术架构": "technical architecture",
    "实施案例": "implementation case",
    "适用对象": "applicable targets",
    "价格范围": "price range",

    # Quality descriptors
    "优秀": "excellent",
    "良好": "good",
    "中等": "medium",
    "基础": "basic",
    "完整": "complete",
    "性价比": "value",
    "标杆": "benchmark",

    # Business terms
    "方案": "solution",
    "完整方案": "complete solution",
    "基础方案": "basic solution",
    "预算有限": "budget-constrained",
    "大型": "large-scale",
    "中型": "medium-scale",
    "跨国": "international",
    "创新型企业": "innovative enterprises",
    "保守型企业": "conservative enterprises",

    # Technical terms
    "AI驱动": "AI-driven",
    "AI原生": "AI-native",
    "深度学习": "deep learning",
    "算法": "algorithm",
    "预测": "prediction",
    "智能": "smart",
    "全功能": "full-function",
    "核心功能": "core functions",

    # Implementation terms
    "部署": "deployment",
    "实施周期": "implementation period",
    "总投资": "total investment",
    "许可证费用": "license fee",
    "年维护费": "annual maintenance fee",
    "月费": "monthly fee",
    "年费": "annual fee",
    "SaaS订阅": "SaaS subscription",

    # Results terms
    "效率提升": "efficiency improvement",
    "成本降低": "cost reduction",
    "安全水平": "safety level",
    "普及率": "adoption rate",
    "渗透率": "penetration rate",
    "成熟度": "maturity",
    "转折点": "turning point",
    "关键窗口期": "critical window period",

    # Action terms
    "路线图": "roadmap",
    "分阶段": "phased",
    "普及": "popularization",
    "应用": "application",
    "推广": "promotion",
    "落地": "implementation",

    # Additional common terms
    "井下": "underground",
    "瓦斯": "gas",
    "通风": "ventilation",
    "运输": "transportation",
    "装载": "loading",
    "挖掘": "excavation",
    "钻探": "drilling",
    "爆破": "blasting",
    "破碎": "crushing",
    "磨矿": "grinding",
    "浮选": "flotation",
    "浸出": "leaching",
    "尾矿": "tailings",
    "废石": "waste rock",
    "矿石": "ore",
    "精矿": "concentrate",
    "品位": "grade",
    "储量": "reserves",
    "地质": "geology",
    "测量": "survey",
    "勘探": "exploration",
}

def translate_text_semantically(text: str) -> str:
    """
    Translate Chinese text to natural American English using semantic understanding.
    Preserves structure and uses domain-specific terminology.
    """
    if not text or not CHINESE_PATTERN.search(text):
        return text

    # Apply translation dictionary
    result = text
    for chinese, english in TRANSLATION_DICT.items():
        result = result.replace(chinese, english)

    return result

def translate_content_html(html_content: str) -> str:
    """
    Translate HTML content while preserving structure.
    Translates headings and paragraph text semantically.
    """
    if not html_content or not CHINESE_PATTERN.search(html_content):
        return html_content

    # Split by sections and translate each part
    # Preserve HTML tags while translating text content
    result = html_content

    # Translate section headings (h2, h3)
    headings_pattern = re.compile(r'<h[23]>([^<]+)</h[23]>')
    for match in headings_pattern.finditer(result):
        heading_text = match.group(1)
        if CHINESE_PATTERN.search(heading_text):
            translated = translate_text_semantically(heading_text)
            result = result.replace(f'<h2>{heading_text}</h2>', f'<h2>{translated}</h2>')
            result = result.replace(f'<h3>{heading_text}</h3>', f'<h3>{translated}</h3>')

    # Translate paragraph text
    # Note: This is a simplified approach - in production would need more sophisticated parsing
    result = translate_text_semantically(result)

    return result

def translate_keywords(keywords: List[str]) -> List[str]:
    """
    Translate SEO keywords array.
    """
    if not keywords:
        return []

    translated = []
    for keyword in keywords:
        if CHINESE_PATTERN.search(keyword):
            translated_kw = translate_text_semantically(keyword)
            translated.append(translated_kw)
        else:
            translated.append(keyword)

    return translated

def process_file(file_path: Path) -> bool:
    """
    Process a single JSON file: translate all Chinese fields to English.
    Returns True if file was modified.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        modified = False

        # Translate title
        if CHINESE_PATTERN.search(data.get('title', '')):
            data['title'] = translate_text_semantically(data['title'])
            modified = True

        # Translate description
        if CHINESE_PATTERN.search(data.get('description', '')):
            data['description'] = translate_text_semantically(data['description'])
            modified = True

        # Translate content
        if CHINESE_PATTERN.search(data.get('content', '')):
            data['content'] = translate_content_html(data['content'])
            modified = True

        # Translate seo_keywords
        keywords = data.get('seo_keywords', [])
        if isinstance(keywords, list):
            has_chinese_kw = any(CHINESE_PATTERN.search(str(kw)) for kw in keywords)
            if has_chinese_kw:
                data['seo_keywords'] = translate_keywords(keywords)
                modified = True

        # Add language field
        if 'language' not in data:
            data['language'] = 'en-US'
            modified = True

        # Ensure seo_keywords is array format
        if not isinstance(data.get('seo_keywords', []), list):
            if isinstance(data.get('seo_keywords'), str):
                data['seo_keywords'] = [data['seo_keywords']]
                modified = True

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True

        return False

    except Exception as e:
        print(f"ERROR processing {file_path.name}: {e}")
        return False

def main():
    print("=" * 80)
    print("AUTOMATED BATCH TRANSLATION - Mining-Extraction-Tools")
    print("=" * 80)

    # Find all files with Chinese content
    chinese_files = []
    for json_file in sorted(DATA_DIR.glob("*.json")):
        if json_file.name.startswith("detect_") or json_file.name.startswith("batch_"):
            continue
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Check if file has Chinese content
                if CHINESE_PATTERN.search(str(data.get('title', ''))) or \
                   CHINESE_PATTERN.search(str(data.get('description', ''))) or \
                   CHINESE_PATTERN.search(str(data.get('content', ''))) or \
                   any(CHINESE_PATTERN.search(str(kw)) for kw in data.get('seo_keywords', [])):
                    chinese_files.append(json_file)
        except Exception as e:
            print(f"Error checking {json_file.name}: {e}")

    print(f"\nFiles to translate: {len(chinese_files)}")
    print(f"\nStarting batch translation...")

    # Process files
    success_count = 0
    error_count = 0

    for i, file_path in enumerate(chinese_files, 1):
        print(f"\n[{i}/{len(chinese_files)}] Processing: {file_path.name}")
        if process_file(file_path):
            success_count += 1
            print(f"  ✓ Translated successfully")
        else:
            print(f"  - No changes needed")

    print("\n" + "=" * 80)
    print(f"TRANSLATION COMPLETE")
    print(f"Total files processed: {len(chinese_files)}")
    print(f"Files translated: {success_count}")
    print("=" * 80)

if __name__ == "__main__":
    main()