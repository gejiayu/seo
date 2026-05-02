#!/usr/bin/env python3
"""
Simple bilingual converter for pSEO JSON files.
Adds English fields while preserving Chinese content.
"""

import json
import os
from pathlib import Path

BASE_DIR = Path("/Users/gejiayu/owner/seo/data")

CATEGORIES = [
    "tennis-racket-rental-tools",
    "tent-canopy-rental-tools",
    "tool-hardware-rental-tools",
    "transportation-fleet-tools",
    "travel-agency-tour-operator-tools",
    "travel-hospitality-tools"
]

# Common translations
TERM_MAP = {
    # Systems & Platforms
    "管理系统": "Management System",
    "预订系统": "Booking System",
    "分析平台": "Analytics Platform",
    "追踪系统": "Tracking System",
    "维护系统": "Maintenance System",
    "租赁系统": "Rental System",
    "管理平台": "Management Platform",
    "运营平台": "Operations Platform",
    "监控平台": "Monitoring Platform",
    "预警系统": "Alert System",

    # Actions
    "评测": "Review",
    "优化": "Optimization",
    "提升": "Enhancement",
    "降低": "Reduction",
    "延长": "Extension",
    "自动化": "Automation",
    "数字化": "Digitization",
    "智能化": "Smart",

    # Domains
    "网球": "Tennis",
    "球拍": "Racket",
    "场地": "Court",
    "设备": "Equipment",
    "帐篷": "Tent",
    "天篷": "Canopy",
    "租赁": "Rental",
    "库存": "Inventory",
    "资产": "Asset",
    "维护": "Maintenance",
    "追踪": "Tracking",
    "数据": "Data",
    "财务": "Financial",
    "人力": "HR",
    "营销": "Marketing",
    "客户": "Customer",
    "员工": "Staff",
    "支付": "Payment",
    "定价": "Pricing",
    "调度": "Scheduling",
    "质量": "Quality",
    "风险": "Risk",
    "保险": "Insurance",
    "合规": "Compliance",
    "合同": "Contract",
    "会员": "Member",
    "培训": "Training",
    "成本": "Cost",
    "收益": "Revenue",
    "效率": "Efficiency",
    "运营": "Operations",
    "业务": "Business",
    "报告": "Reporting",
    "仪表盘": "Dashboard",
    "趋势": "Trends",
    "预测": "Forecast",
    "决策": "Decision",
    "洞察": "Insights",
    "分析": "Analysis",
    "策略": "Strategy",
    "流程": "Process",
    "体验": "Experience",
    "服务": "Service",

    # Tech
    "物联网": "IoT",
    "传感器": "Sensor",
    "蓝牙": "Bluetooth",
    "RFID": "RFID",
    "GPS": "GPS",
    "API": "API",
    "云端": "Cloud",
    "移动": "Mobile",

    # Descriptors
    "关键": "Key",
    "核心": "Core",
    "专业": "Professional",
    "深度": "In-depth",
    "全面": "Comprehensive",
    "高效": "Efficient",
    "智能": "Intelligent",
    "预防性": "Preventive",
    "实时": "Real-time",
    "集中": "Centralized",
    "多场地": "Multi-venue",
    "多设备": "Multi-device",

    # Objects
    "俱乐部": "Club",
    "场馆": "Venue",
    "连锁": "Chain",
    "企业": "Enterprise",
    "中小": "Small & Medium",

    # Qualifiers
    "最佳": "Best",
    "首选": "Top Choice",
    "必备": "Essential",
    "实用": "Practical",
    "完整": "Complete",
}

def translate_title(cn_title):
    """Translate Chinese title to English."""
    # Remove year suffix
    title = cn_title.replace("｜2026年评测", "").replace("｜2026", "")

    # Translate known terms
    for cn, en in sorted(TERM_MAP.items(), key=lambda x: -len(x[0])):
        title = title.replace(cn, en)

    # Clean up
    title = title.replace("：", ": ").replace("  ", " ")

    # Add suffix
    return f"{title} | 2026 Review"

def translate_description(cn_desc):
    """Translate Chinese description."""
    # Remove Chinese CTAs
    desc = cn_desc.replace(
        "了解更多功能和价格对比，找到最适合你的方案！专业评测助你决策！",
        "Compare features and pricing to find your ideal solution."
    )

    # Translate terms
    for cn, en in sorted(TERM_MAP.items(), key=lambda x: -len(x[0])):
        desc = desc.replace(cn, en)

    # Clean up
    desc = desc.replace("，", ", ").replace("。", ". ")
    desc = desc.replace("  ", " ")

    return desc.strip()

def translate_content(cn_content):
    """Translate content structure. Preserves HTML tags."""
    content = cn_content

    # Translate headers
    header_trans = {
        "行业背景与痛点分析": "Industry Background & Pain Points",
        "市场背景与需求分析": "Market Background & Demand Analysis",
        "数据挑战与决策痛点": "Data Challenges & Decision Pain Points",
        "维护挑战与成本痛点": "Maintenance Challenges & Cost Pain Points",
        "技术背景与行业痛点": "Technology Background & Industry Pain Points",
        "深度评测：主流": "In-depth Review: Leading",
        "功能对比表": "Feature Comparison Table",
        "未来发展趋势": "Future Development Trends",
        "选择建议": "Selection Recommendations",
        "选择指南": "Selection Guide",
        "核心功能：": "Core Features:",
        "技术架构：": "Technical Architecture:",
        "价格方案：": "Pricing Plan:",
        "用户体验：": "User Experience:",
        "关键指标：": "Key Metrics:",
        "趋势洞察：": "Trend Insights:",
        "整合能力：": "Integration Capability:",
        "预防性维护策略：": "Preventive Maintenance Strategy:",
        "检测标准：": "Detection Standards:",
        "全生命周期价值：": "Full Lifecycle Value:",
        "技术原理：": "Technical Principle:",
        "应用场景：": "Application Scenarios:",
        "成本分析：": "Cost Analysis:",
        "技术亮点：": "Technical Highlights:",
        "核心特色：": "Core Features:",
    }

    for cn, en in header_trans.items():
        content = content.replace(cn, en)

    # Translate terms in paragraphs
    for cn, en in sorted(TERM_MAP.items(), key=lambda x: -len(x[0])):
        content = content.replace(cn, en)

    return content

def translate_keywords(cn_keywords):
    """Translate SEO keywords."""
    en_keywords = []
    for kw in cn_keywords:
        kw_en = kw
        for cn, en in TERM_MAP.items():
            kw_en = kw_en.replace(cn, en)
        en_keywords.append(kw_en)
    return en_keywords

def process_file(file_path):
    """Process single JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get original fields
    title_cn = data['title']
    desc_cn = data['description']
    content_cn = data['content']
    slug = data['slug']  # Already in English format
    keywords_cn = data['seo_keywords']
    published = data['published_at']
    author = data['author']

    # Generate English translations
    title_en = translate_title(title_cn)
    desc_en = translate_description(desc_cn)
    content_en = translate_content(content_cn)
    keywords_en = translate_keywords(keywords_cn)

    # Create bilingual structure
    new_data = {
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

    # Filename remains the same (slug is already English)
    return new_data, slug

def process_all():
    """Process all files in all categories."""
    total = 0
    report_interval = 20

    for category in CATEGORIES:
        cat_dir = BASE_DIR / category
        files = sorted(cat_dir.glob("*.json"))

        print(f"\n[{category}] - {len(files)} files")

        for i, file_path in enumerate(files):
            try:
                new_data, slug = process_file(file_path)

                # Write back (filename unchanged)
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(new_data, f, ensure_ascii=False, indent=2)

                total += 1

                # Report progress
                if total % report_interval == 0:
                    print(f"  Progress: {total} files processed")

            except Exception as e:
                print(f"  ERROR: {file_path.name} - {e}")

    print(f"\n=== COMPLETE ===")
    print(f"Total files processed: {total}")

if __name__ == "__main__":
    process_all()