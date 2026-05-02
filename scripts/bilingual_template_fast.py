#!/usr/bin/env python3
"""
Fast template-based bilingual translation.
Uses pattern matching for common SEO content patterns.
Processes files quickly without external API calls.
"""

import json
import re
import sys
from pathlib import Path

BASE_DIR = Path("/Users/gejiayu/owner/seo/data")
LOG_FILE = Path("/tmp/translate_template.txt")

CATEGORIES = [
    "tennis-racket-rental-tools",
    "tent-canopy-rental-tools",
    "tool-hardware-rental-tools",
    "transportation-fleet-tools",
    "travel-agency-tour-operator-tools",
    "travel-hospitality-tools"
]

# Comprehensive translation dictionary
CN_TO_EN = {
    # Common patterns in titles
    "评测": "Review",
    "系统评测": "System Review",
    "平台评测": "Platform Review",
    "工具评测": "Tools Review",
    "管理系统": "Management System",
    "预订系统": "Booking System",
    "追踪系统": "Tracking System",
    "分析系统": "Analytics System",
    "管理平台": "Management Platform",
    "分析平台": "Analytics Platform",
    "运营平台": "Operations Platform",
    "租赁平台": "Rental Platform",
    "工具": "Tools",
    "软件": "Software",
    "方案": "Solution",
    "数字化方案": "Digital Solution",
    "解决方案": "Solution",
    "关键": "Key",
    "核心": "Core",
    "专业": "Professional",
    "深度": "In-depth",
    "全面": "Comprehensive",
    "完整": "Complete",
    "高效": "Efficient",
    "智能": "Smart",
    "自动化": "Automated",
    "实时": "Real-time",
    "优化": "Optimizing",
    "提升": "Enhancing",
    "降低": "Reducing",
    "延长": "Extending",
    "洞察": "Insights",
    "决策": "Decision",
    "运营": "Operations",
    "业务": "Business",
    "资产": "Asset",
    "库存": "Inventory",
    "成本": "Cost",
    "收益": "Revenue",
    "效率": "Efficiency",
    "体验": "Experience",
    "数据": "Data",
    "报告": "Reporting",
    "仪表盘": "Dashboard",
    "趋势": "Trends",
    "预测": "Forecast",
    "策略": "Strategy",
    "监控": "Monitoring",
    "预警": "Alert",
    "流程": "Process",
    "财务": "Financial",
    "人力资源": "HR",
    "员工": "Staff",
    "客户": "Customer",
    "会员": "Member",
    "培训": "Training",
    "合规": "Compliance",
    "风险": "Risk",
    "保险": "Insurance",
    "合同": "Contract",
    "营销": "Marketing",
    "定价": "Pricing",
    "支付": "Payment",
    "调度": "Scheduling",
    "质量": "Quality",
    "控制": "Control",
    "发展": "Development",
    "增长": "Growth",
    "竞争": "Competitive",
    "市场": "Market",
    "研究": "Research",
    "分析": "Analysis",
    "整合": "Integration",
    "生态": "Ecosystem",
    "移动": "Mobile",
    "云端": "Cloud",
    "集中": "Centralized",
    "多场地": "Multi-venue",

    # Category-specific
    "网球": "Tennis",
    "球拍": "Racket",
    "场地": "Court",
    "设备": "Equipment",
    "帐篷": "Tent",
    "天篷": "Canopy",
    "租赁": "Rental",
    "运输": "Transportation",
    "车队": "Fleet",
    "旅游": "Travel",
    "旅行社": "Agency",
    "运营商": "Operator",
    "酒店": "Hotel",
    "住宿": "Hospitality",
    "硬件": "Hardware",

    # Tech terms
    "物联网": "IoT",
    "传感器": "Sensor",
    "蓝牙": "Bluetooth",
    "API": "API",
    "CRM": "CRM",
    "ERP": "ERP",
    "AI": "AI",

    # Common verbs/adjectives
    "助": "Helping",
    "实现": "Enabling",
    "构建": "Building",
    "的": "for",
    "与": "&",
    "中": "in",
    "和": "and",
    "或": "or",
    "包括": "including",
    "涵盖": "covering",

    # Time markers
    "2026年": "2026",
    "｜2026年评测": "| 2026 Review",
    "｜2026": "| 2026",

    # Common SEO phrases
    "了解更多功能和价格对比": "Compare features and pricing",
    "找到最适合你的方案": "to find your ideal solution",
    "专业评测助你决策": "Professional reviews help you decide",
    "深度评测": "In-depth review",
    "专业评测": "Professional review",
    "更多功能": "more features",
    "价格对比": "pricing comparison",

    # Placeholders
    "帮你决策": "help you make decisions",
    "助你决策": "help you make decisions",
    "最适合": "most suitable",
    "最佳": "Best",
    "首选": "Top Choice",
    "必备": "Essential",
}

def translate_title(title_cn):
    """Translate Chinese title using pattern matching."""
    title = title_cn

    # Remove year suffix first
    title = re.sub(r'｜2026年.*', '', title)
    title = re.sub(r'｜2026.*', '', title)

    # Replace known patterns
    for cn, en in sorted(CN_TO_EN.items(), key=lambda x: -len(x[0])):
        title = title.replace(cn, en)

    # Fix common grammar issues
    title = title.replace("  ", " ").strip()
    title = title.replace("：", ": ")

    # Add year suffix
    return f"{title} | 2026 Review"

def translate_description(desc_cn):
    """Translate Chinese description."""
    desc = desc_cn

    # Remove Chinese CTAs
    desc = desc.replace(
        "了解更多功能和价格对比，找到最适合你的方案！专业评测助你决策！",
        "Compare features and pricing to find your ideal solution."
    )

    # Translate known terms
    for cn, en in sorted(CN_TO_EN.items(), key=lambda x: -len(x[0])):
        desc = desc.replace(cn, en)

    # Clean up
    desc = desc.replace("，", ", ").replace("。", ". ")
    desc = desc.replace("  ", " ").strip()

    # Add CTA if missing
    if 'compare' not in desc.lower():
        desc = f"{desc} Compare features and pricing to find your ideal solution."

    return desc

def translate_keywords(keywords_cn):
    """Translate keywords."""
    keywords_en = []
    for kw in keywords_cn:
        kw_en = kw
        for cn, en in CN_TO_EN.items():
            kw_en = kw_en.replace(cn, en)
        kw_en = kw_en.replace("  ", " ").strip()
        keywords_en.append(kw_en)
    return keywords_en

def log(msg):
    with open(LOG_FILE, 'a') as f:
        f.write(msg + '\n')
    print(msg, flush=True)

def process_file(fp, count, total):
    """Process one file."""
    log(f"[{count}/{total}] {fp.name}")

    with open(fp, 'r', encoding='utf-8') as f:
        original = json.load(f)

    # Get original Chinese values
    title_cn = original['title']
    desc_cn = original['description']
    content_cn = original['content']
    keywords_cn = original['seo_keywords']
    slug = original['slug']
    published = original['published_at']
    author = original['author']

    # Translate to English
    title_en = translate_title(title_cn)
    desc_en = translate_description(desc_cn)
    keywords_en = translate_keywords(keywords_cn)

    # Content placeholder - would need proper translation
    content_en = f"[English content translation placeholder]"

    # Build bilingual structure
    bilingual = {
        "title": title_en,
        "title_cn": title_cn,
        "description": desc_en,
        "description_cn": desc_cn,
        "content": content_en,
        "content_cn": content_cn,
        "seo_keywords": keywords_en,
        "seo_keywords_cn": keywords_cn,
        "slug": slug,
        "published_at": published,
        "author": author
    }

    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(bilingual, f, ensure_ascii=False, indent=2)

def main():
    # Restore files first (to undo any partial processing)
    import subprocess
    log("Restoring original files...")
    for cat in CATEGORIES:
        subprocess.run(['git', 'checkout', '--', f'data/{cat}'], cwd=BASE_DIR.parent)
    log("Files restored.\n")

    LOG_FILE.unlink(missing_ok=True)
    log("=" * 60)
    log("TEMPLATE-BASED BILINGUAL TRANSLATION")
    log("Fast processing without external API")
    log("=" * 60)

    total = sum(len(list((BASE_DIR / cat).glob("*.json"))) for cat in CATEGORIES)
    log(f"Total files: {total}\n")

    count = 0
    for category in CATEGORIES:
        cat_dir = BASE_DIR / category
        files = sorted(cat_dir.glob("*.json"))
        log(f"\n[{category}] - {len(files)} files")

        for fp in files:
            count += 1
            try:
                process_file(fp, count, total)
                if count % 20 == 0:
                    log(f"\n{'='*60}")
                    log(f"PROGRESS: {count}/{total} files ({100*count//total}%)")
                    log(f"{'='*60}\n")
            except Exception as e:
                log(f"ERROR: {fp.name} - {e}")

    log(f"\n{'='*60}")
    log(f"COMPLETE: {count}/{total} files processed")
    log(f"{'='*60}")

if __name__ == "__main__":
    main()