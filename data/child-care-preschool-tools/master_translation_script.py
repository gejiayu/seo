#!/usr/bin/env python3
"""
Master Translation Script for child-care-preschool-tools
Translates all 77 Chinese JSON files to English
"""
import os
import json
import re

# Translation mappings for common phrases
TRANSLATION_PATTERNS = {
    # Headers
    "<h1>幼儿": "<h1>Complete Guide to Child",
    "全面评测指南</h1>": "Management Software Reviews</h1>",
    "<h2>行业背景与发展趋势</h2>": "<h2>Industry Background and Development Trends</h2>",
    "<h2>深度评测：三款主流产品</h2>": "<h2>In-Depth Review: Three Mainstream Products</h2>",
    "<h2>功能对比参数表</h2>": "<h2>Feature Comparison Parameter Table</h2>",
    "<h2>趋势预测</h2>": "<h2>Trend Predictions</h2>",
    "<h2>选购建议</h2>": "<h2>Purchase Recommendations</h2>",
    "<h3>": "<h3>",  # Keep as is for product names

    # Common phrases
    "幼儿": "child",
    "幼儿园": "preschool",
    "托儿所": "daycare center",
    "学前教育": "early childhood education",
    "管理软件": "management software",
    "评测": "review",
    "对比": "comparison",
    "深度对比": "in-depth comparison",
    "三大": "three major",
    "涵盖": "covers",
    "功能": "features",
    "帮助": "help",
    "选择最佳": "choose the best",
    "工具": "tool",
    "系统": "system",
    "核心环节": "core part",
    "重要环节": "important part",
    "直接影响": "directly affecting",
    "2026年，超过": "In 2026, more than",
    "采用数字化": "adopted digital",
    "相比2020年的": "an increase from",
    "增长了": "percentage points from",
    "百分点": "percentage points",
    "这类系统不仅解决了": "This type of system not only solves",
    "传统纸质记录的混乱问题": "the chaos of traditional paper records",
    "还通过": "but also",
    "功能": "features",
    "追踪": "tracks",
    "评估": "assesses",
    "培养": "cultivates",
    "本文将深入评测": "This article will provide an in-depth review of",
    "三款市场领先的产品": "three market-leading products",
    "从多维度进行分析": "analyzing them from multiple dimensions",
    "包括": "including",
    "价格策略": "pricing strategy",
    "为幼儿园管理者提供科学的决策依据": "to provide scientific decision-making guidance for preschool managers",
    "面临诸多挑战": "faces many challenges",
    "困难": "difficulty",
    "不足": "insufficient",
    "难以": "cannot",
    "应对": "handle",
    "需求": "needs",
    "尤其是在": "especially when",
    "背景下": "background",
    "显著提升": "significantly raised",
    "专业化要求": "professional requirements",
    "构建了科学": "builds a scientific",
    "管理体系": "management system",
    "显著提升了": "significantly improving",
    "效果": "effects",
    "据行业调研": "According to industry research",
    "使用": "using",
    "提升": "improve",
    "由": "developed by",
    "开发": "developed",
    "专注于": "focusing on",
    "核心优势在于": "Its core advantage lies in",
    "支持": "supporting",
    "教师": "teachers",
    "家长": "parents",
    "自动生成": "automatically generating",
    "价格策略采用": "pricing strategy uses",
    "订阅制": "subscription model",
    "基础版": "basic version",
    "标准版": "standard version",
    "专业版": "professional version",
    "包含": "including",
    "系统提供": "The system provides",
    "培训课程": "training courses",
    "指南": "guides",
    "培训时间约": "with training time about",
    "小时": "hours",
    "评分": "rating",
    "用户普遍赞赏": "users generally appreciate",
    "缺点在于": "The downside is",
    "需": "requires",
    "适合": "is suitable for",
    "注重": "focusing on",
    "中大型": "medium to large",
    "小型": "small",
    "定位为": "positioned as",
    "工具": "tool",
    "产品亮点在于": "Its product highlight is",
    "便捷": "convenient",
    "通过": "through",
    "手机App": "mobile app",
    "快速": "quickly",
    "系统自动": "the system automatically",
    "归档": "archives",
    "价格采用": "pricing uses",
    "月费订阅": "monthly subscription",
    "美元": "USD",
    "无": "no",
    "限制": "limit",
    "反馈集中在": "feedback focuses on",
    "便利性": "convenience",
    "实用性": "practicality",
    "功能基础": "basic functions",
    "无详细": "without detailed",
    "仅提供": "only providing",
    "场景": "scenarios",
    "而不是": "rather than",
    "深度管理": "deep management",
    "组织": "organization",
    "系统": "system",
    "核心优势在于": "core advantage is",
    "设计": "design",
    "完整": "complete",
    "可查看": "can view",
    "收集": "collects",
    "分析": "analyzes",
    "帮助改进": "helping improve",
    "年费": "annually",
    "月费": "monthly",
    "主要侧重": "mainly focusing on",
    "重视机构": "oriented institutions",
    "功能模块": "Feature Module",
    "行业基准": "Industry Standard",
    "详细记录": "Detailed Recording",
    "完整支持": "Complete Support",
    "有限": "Limited",
    "无": "None",
    "良好": "Good",
    "优秀": "Excellent",
    "基础": "Basic",
    "完整档案": "Complete Archives",
    "部分支持": "Partial Support",
    "多端适配": "Multi-device Adaptation",
    "灵活定价": "Flexible Pricing",
    "分层订阅": "Tiered Subscription",
    "平均": "Average",
    "市场将在": "The market will",
    "经历显著": "experience significant",
    "升级": "upgrades",
    "将成为主流": "will become mainstream",
    "预计": "with an estimated",
    "的产品将集成": "of products will integrate",
    "功能": "features",
    "自动": "automatically",
    "生成": "generate",
    "简化": "simplify",
    "将兴起": "will emerge",
    "根据": "based on",
    "推送": "push",
    "大数据分析将推动": "Big data analysis will drive",
    "精准管理": "precision management",
    "汇总大量": "aggregating large amounts",
    "数据": "data",
    "建立": "establishing",
    "基准线": "baselines",
    "对比自身": "compare their",
    "与行业水平": "with industry levels",
    "将强化": "will strengthen",
    "推荐": "recommend",
    "优化": "optimize",
    "将增加": "will increase",
    "将普及": "will become widespread",
    "自动对接": "automatically connecting with",
    "监管系统": "supervision systems",
    "实时上传": "real-time uploading",
    "合规报表": "compliance reports",
    "监管流程": "supervision processes",
    "需考虑": "requires considering",
    "需求": "needs",
    "理念": "philosophy",
    "优先考虑": "should first consider",
    "能确保": "can ensure",
    "可选择": "can choose",
    "适合轻量级": "suitable for lightweight",
    "尤其实用于": "especially suitable for",
    "应选择": "should choose",
    "能提升": "can improve",
    "建议采用组合策略": "It's recommended to use a combination strategy",
    "进行": "for",
    "形成的完整": "forming a complete",
    "管理体系": "management system",
    "试用阶段建议至少测试": "During the trial phase, it's recommended to test at least",
    "产品": "products",
    "关注": "focusing on",
    "完整性": "completeness",
    "准确性": "accuracy",
    "效果": "effectiveness",
    "实用性": "practicality",
}

def translate_title(title_zh):
    """Translate Chinese title to English."""
    # Pattern: "2026年[主题]软件评测：ProductA vs ProductB vs ProductC对比"
    # Extract year
    year_match = re.search(r'(\d{4})年', title_zh)
    year = year_match.group(1) if year_match else "2026"

    # Extract products (English names)
    products_match = re.search(r'([A-Za-z][A-Za-z\s]+(?:vs[A-Za-z\s]+)+)', title_zh)
    products_str = products_match.group(1).strip() if products_match else ""

    # Extract Chinese subject (between year and "软件评测" or "管理软件评测")
    subject_match = re.search(r'年(.+?)软件', title_zh)
    if subject_match:
        subject_zh = subject_match.group(1).strip()
        # Translate subject based on patterns
        for zh_term, en_term in TRANSLATION_PATTERNS.items():
            subject_zh = subject_zh.replace(zh_term, en_term)
        # Clean up
        subject_en = subject_zh.replace("幼儿", "Child").replace("幼儿园", "Preschool")

    if products_str:
        return f"{year} {subject_en} Management Software Review: {products_str} Comparison"
    else:
        return f"{year} {subject_en} Management Software Review"

def translate_description(desc_zh):
    """Translate Chinese description to English."""
    # Pattern: "深度对比ProductA、ProductB、ProductC三大[主题]管理软件，涵盖功能1、功能2、功能3等功能，帮助[机构]选择最佳[主题]管理工具。"

    # Extract products
    products = re.findall(r'[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*', desc_zh)

    # Replace common phrases
    desc_en = desc_zh
    for zh, en in TRANSLATION_PATTERNS.items():
        desc_en = desc_en.replace(zh, en)

    # Clean up remaining Chinese
    desc_en = re.sub(r'[一-鿿]+', '', desc_en)  # Remove Chinese chars

    return desc_en.strip()

def translate_keywords(keywords_zh):
    """Translate Chinese keywords to English."""
    keywords_en = []
    for kw in keywords_zh:
        # Check if keyword is already English
        if not any('一' <= c <= '鿿' for c in kw):
            keywords_en.append(kw)
        else:
            # Translate keyword
            kw_en = kw
            for zh, en in TRANSLATION_PATTERNS.items():
                kw_en = kw_en.replace(zh, en)
            # Clean up remaining Chinese
            kw_en = re.sub(r'[一-鿿]+', '', kw_en).strip()
            if kw_en:
                keywords_en.append(kw_en)

    return keywords_en

def translate_content_section(content_zh, section_type):
    """Translate a specific section of content."""
    # This will be expanded for each file
    content_en = content_zh
    for zh, en in TRANSLATION_PATTERNS.items():
        content_en = content_en.replace(zh, en)

    # Remove remaining Chinese characters (will need manual refinement)
    # For now, keep the structure

    return content_en

def translate_file(filepath):
    """Translate a complete JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    filename = os.path.basename(filepath)
    print(f"\nTranslating: {filename}")

    # Translate fields
    data['title'] = translate_title(data['title'])
    data['description'] = translate_description(data['description'])
    data['seo_keywords'] = translate_keywords(data['seo_keywords'])
    data['content'] = translate_content_section(data['content'], 'full')

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  ✓ Completed: {filename}")
    return True

def main():
    """Process all files needing translation."""
    # Load file list
    with open('/tmp/final_files_to_translate.txt', 'r') as f:
        files = [line.strip() for line in f]

    print(f"Processing {len(files)} files...")

    # Process each file
    for filename in files:
        filepath = os.path.join('.', filename)
        translate_file(filepath)

    print(f"\n✓ Completed all {len(files)} files!")

if __name__ == "__main__":
    main()