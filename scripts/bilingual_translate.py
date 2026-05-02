#!/usr/bin/env python3
"""
Bilingual pSEO Translation Script
Processes JSON files and adds English fields while preserving Chinese content.
"""

import json
import os
import shutil
from pathlib import Path

# Categories to process
CATEGORIES = [
    "scooter-moped-rental-tools",
    "security-surveillance-rental-tools",
    "ski-snowboard-rental-tools",
    "sporting-goods-retail-tools",
    "sports-equipment-rental-tools",
    "sports-fitness-tools"
]

BASE_DIR = Path("/Users/gejiayu/owner/seo/data")

# Translation mappings for common terms
TRANSLATION_MAP = {
    # Common terms
    "评测": "Review",
    "系统": "System",
    "平台": "Platform",
    "工具": "Tools",
    "管理": "Management",
    "分析": "Analysis",
    "租赁": "Rental",
    "预订": "Booking",
    "维护": "Maintenance",
    "追踪": "Tracking",
    "优化": "Optimization",
    "智能": "Smart",
    "自动化": "Automation",
    "数字化": "Digital",
    "解决方案": "Solution",
    "关键": "Key",
    "核心": "Core",
    "专业": "Professional",
    "深度": "Deep",
    "全面": "Comprehensive",
    "高效": "Efficient",
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
    "报告": "Report",
    "仪表盘": "Dashboard",
    "趋势": "Trends",
    "预测": "Forecast",
    "策略": "Strategy",
    "监控": "Monitoring",
    "预警": "Alert",
    "流程": "Process",
    "财务": "Financial",
    "人力资源": "HR",
    "客户": "Customer",
    "员工": "Staff",
    "培训": "Training",
    "合规": "Compliance",
    "风险": "Risk",
    "保险": "Insurance",
    "合同": "Contract",
    "会员": "Membership",
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
    "报告": "Reporting",
    "整合": "Integration",
    "生态": "Ecosystem",
    "移动": "Mobile",
    "云端": "Cloud",
    "本地": "Local",
    "部署": "Deployment",
    "API": "API",
    "CRM": "CRM",
    "ERP": "ERP",
    "BI": "BI",
    "AI": "AI",
    "IoT": "IoT",
    "RFID": "RFID",
    "GPS": "GPS",
    "蓝牙": "Bluetooth",
    "传感器": "Sensor",

    # Category-specific (Sports & Equipment)
    "电动滑板车": "Electric Scooter",
    "摩托车": "Motorcycle",
    "滑板车": "Scooter",
    "滑雪": "Ski",
    "滑雪板": "Snowboard",
    "滑雪装备": "Ski Equipment",
    "滑雪设备": "Ski Equipment",
    "滑雪场": "Ski Resort",
    "雪杖": "Ski Pole",
    "雪靴": "Ski Boot",
    "护目镜": "Goggles",
    "头盔": "Helmet",
    "运动装备": "Sports Equipment",
    "体育用品": "Sporting Goods",
    "健身": "Fitness",
    "运动": "Sports",
    "自行车": "Bicycle",
    "高尔夫": "Golf",
    "瑜伽": "Yoga",
    "登山": "Mountaineering",
    "潜水": "Diving",
    "拳击": "Boxing",
    "露营": "Camping",
    "CrossFit": "CrossFit",
    "动感单车": "Spinning Bike",
    "水上运动": "Water Sports",
    "户外运动": "Outdoor Sports",
    "体育器材": "Sports Gear",
    "运动器材": "Sports Gear",
    "健身器材": "Fitness Equipment",
    "健身房": "Gym",
    "跑步": "Running",
    "游泳": "Swimming",
    "网球": "Tennis",
    "足球": "Soccer",
    "篮球": "Basketball",
    "攀岩": "Climbing",
    "骑行": "Cycling",

    # Security & Surveillance
    "安防": "Security",
    "监控": "Monitoring",
    "摄像头": "Camera",
    "视频": "Video",
    "事件": "Event",
    "临时监控": "Temporary Monitoring",
    "视频监控": "Video Monitoring",
    "安全设备": "Security Equipment",

    # Tennis & Sports (from original)
    "网球": "Tennis",
    "球拍": "Racket",
    "场地": "Court",
    "设备": "Equipment",
    "帐篷": "Tent",
    "天篷": "Canopy",
    "工具": "Tool",
    "硬件": "Hardware",
    "运输": "Transportation",
    "车队": "Fleet",
    "旅游": "Travel",
    "旅行社": "Agency",
    "运营商": "Operator",
    "酒店": "Hospitality",
    "住宿": "Accommodation",

    # Action verbs
    "助": "Help",
    "提升": "Boost",
    "优化": "Optimize",
    "降低": "Reduce",
    "延长": "Extend",
    "实现": "Enable",
    "构建": "Build",
    "整合": "Integrate",
    "自动化": "Automate",
    "数字化": "Digitize",

    # Time markers
    "2026年": "2026",
    "年度": "Annual",
    "季度": "Quarterly",
    "月度": "Monthly",

    # Descriptive
    "最佳": "Best",
    "首选": "Top Choice",
    "必备": "Essential",
    "关键": "Critical",
    "核心": "Core",
    "重要": "Important",
    "显著": "Significant",
    "有效": "Effective",
}

def translate_text(text, is_slug=False):
    """Translate Chinese text to English using mapping."""
    if is_slug:
        # Slugs should be lowercase with hyphens
        result = text.lower().replace(" ", "-")
        return result

    # For titles and descriptions, use direct translation
    # This is a simplified version - in production use actual translation API
    result = text

    # Replace known terms
    for cn, en in TRANSLATION_MAP.items():
        result = result.replace(cn, en)

    return result

def generate_slug_en(slug_cn, title_cn):
    """Generate English slug from Chinese title/slug."""
    # The slug_cn should already be in English format
    # Just ensure it's lowercase and properly formatted
    slug = slug_cn.lower().replace("_", "-").replace(" ", "-")

    # Remove duplicate hyphens
    while "--" in slug:
        slug = slug.replace("--", "-")

    return slug

def generate_title_en(title_cn):
    """Generate English title based on the Chinese title."""
    # Extract key parts and translate
    # Most titles follow pattern: [Topic] + [System/Platform/Tools] + Review

    # Common title patterns translation
    title = title_cn

    # Remove year suffix
    title = title.replace("｜2026年评测", "")
    title = title.replace("｜2026", "")
    title = title.replace("：", ": ")

    # Translate common patterns
    patterns = {
        "评测": "Review",
        "系统评测": "System Review",
        "平台评测": "Platform Review",
        "工具评测": "Tools Review",
        "管理系统": "Management System",
        "分析平台": "Analytics Platform",
        "预订系统": "Booking System",
        "追踪技术": "Tracking Technology",
        "维护管理": "Maintenance Management",
        "租赁管理": "Rental Management",
    }

    for cn, en in patterns.items():
        title = title.replace(cn, en)

    # Add year suffix
    title = f"{title} | 2026 Review"

    return title

def generate_description_en(description_cn):
    """Generate English description."""
    # Simplified translation - preserve structure
    desc = description_cn

    # Remove Chinese call-to-action phrases
    desc = desc.replace("了解更多功能和价格对比，找到最适合你的方案！专业评测助你决策！", "")
    desc = desc.replace("了解更多", "Learn more about")
    desc = desc.replace("功能和价格对比", "features and pricing comparison")
    desc = desc.replace("找到最适合你的方案", "to find the best solution")
    desc = desc.replace("专业评测助你决策", "Professional reviews help you decide")

    # Translate key terms
    for cn, en in TRANSLATION_MAP.items():
        desc = desc.replace(cn, en)

    # Add English CTA
    if not desc.endswith("!"):
        desc = desc.rstrip(".") + ". "
    desc += "Discover features and pricing to find your ideal solution!"

    return desc

def generate_content_en(content_cn):
    """Generate English content structure.

    Note: Full content translation would require external API.
    This function preserves structure and headers.
    """
    # In production, this would call translation API
    # For now, we preserve HTML structure

    content = content_cn

    # Translate section headers
    header_map = {
        "<h1>": "<h1>",
        "</h1>": "</h1>",
        "<h2>行业背景与痛点分析</h2>": "<h2>Industry Background & Pain Point Analysis</h2>",
        "<h2>市场背景与需求分析</h2>": "<h2>Market Background & Demand Analysis</h2>",
        "<h2>数据挑战与决策痛点</h2>": "<h2>Data Challenges & Decision Pain Points</h2>",
        "<h2>维护挑战与成本痛点</h2>": "<h2>Maintenance Challenges & Cost Pain Points</h2>",
        "<h2>技术背景与行业痛点</h2>": "<h2>Technology Background & Industry Pain Points</h2>",
        "<h2>深度评测：主流": "<h2>In-depth Review: Leading ",
        "<h3>1.": "<h3>1.",
        "<h3>2.": "<h3>2.",
        "<h3>3.": "<h3>3.",
        "<h2>功能对比表</h2>": "<h2>Feature Comparison Table</h2>",
        "<h2>未来发展趋势</h2>": "<h2>Future Development Trends</h2>",
        "<h2>选择建议</h2>": "<h2>Selection Recommendations</h2>",
        "<h2>选择指南</h2>": "<h2>Selection Guide</h2>",
        "<strong>核心功能：</strong>": "<strong>Core Features:</strong>",
        "<strong>技术架构：</strong>": "<strong>Technical Architecture:</strong>",
        "<strong>价格方案：</strong>": "<strong>Pricing Plan:</strong>",
        "<strong>用户体验：</strong>": "<strong>User Experience:</strong>",
        "<strong>关键指标：</strong>": "<strong>Key Metrics:</strong>",
        "<strong>趋势洞察：</strong>": "<strong>Trend Insights:</strong>",
        "<strong>整合能力：</strong>": "<strong>Integration Capability:</strong>",
        "<strong>预防性维护策略：</strong>": "<strong>Preventive Maintenance Strategy:</strong>",
        "<strong>检测标准：</strong>": "<strong>Detection Standards:</strong>",
        "<strong>全生命周期价值：</strong>": "<strong>Full Lifecycle Value:</strong>",
        "<strong>技术原理：</strong>": "<strong>Technical Principle:</strong>",
        "<strong>应用场景：</strong>": "<strong>Application Scenarios:</strong>",
        "<strong>成本分析：</strong>": "<strong>Cost Analysis:</strong>",
        "<strong>技术亮点：</strong>": "<strong>Technical Highlights:</strong>",
    }

    for cn, en in header_map.items():
        content = content.replace(cn, en)

    return content

def process_file(file_path):
    """Process a single JSON file to add bilingual fields."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract original Chinese fields
    title_cn = data.get('title', '')
    description_cn = data.get('description', '')
    content_cn = data.get('content', '')
    slug_cn = data.get('slug', '')
    seo_keywords = data.get('seo_keywords', [])
    published_at = data.get('published_at', '')
    author = data.get('author', '')

    # Generate English fields
    title_en = generate_title_en(title_cn)
    description_en = generate_description_en(description_cn)
    content_en = generate_content_en(content_cn)
    slug_en = generate_slug_en(slug_cn, title_cn)

    # Generate English keywords (preserve structure, translate terms)
    seo_keywords_en = []
    for kw in seo_keywords:
        kw_en = kw
        for cn, en in TRANSLATION_MAP.items():
            kw_en = kw_en.replace(cn, en)
        seo_keywords_en.append(kw_en)

    # Create new bilingual structure
    new_data = {
        "title": title_en,
        "title_cn": title_cn,
        "description": description_en,
        "description_cn": description_cn,
        "content": content_en,
        "content_cn": content_cn,
        "seo_keywords": seo_keywords_en,
        "seo_keywords_cn": seo_keywords,
        "slug": slug_en,
        "slug_cn": slug_cn,
        "published_at": published_at,
        "author": author
    }

    return new_data, slug_en

def process_category(category):
    """Process all files in a category."""
    category_dir = BASE_DIR / category
    files = sorted(category_dir.glob("*.json"))

    processed = 0
    renamed = 0

    for file_path in files:
        try:
            new_data, slug_en = process_file(file_path)

            # Determine new filename
            new_filename = f"{slug_en}.json"
            new_file_path = category_dir / new_filename

            # Write new file
            with open(new_file_path, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=2)

            # Remove old file if filename changed
            if file_path.name != new_filename:
                file_path.unlink()
                renamed += 1

            processed += 1

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    return processed, renamed

def main():
    """Process all categories."""
    total_processed = 0
    total_renamed = 0

    for category in CATEGORIES:
        print(f"\nProcessing {category}...")
        processed, renamed = process_category(category)
        total_processed += processed
        total_renamed += renamed
        print(f"  Processed: {processed} files, Renamed: {renamed} files")

    print(f"\n=== Summary ===")
    print(f"Total processed: {total_processed} files")
    print(f"Total renamed: {total_renamed} files")

if __name__ == "__main__":
    main()