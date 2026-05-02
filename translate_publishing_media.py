#!/usr/bin/env python3
"""
Translate all Chinese content to English in publishing-media-tools JSON files.
"""
import json
import os
import re
from pathlib import Path

def contains_chinese(text):
    """Check if text contains Chinese characters."""
    if not isinstance(text, str):
        return False
    chinese_pattern = re.compile(r'[一-鿿]')
    return bool(chinese_pattern.search(text))

def translate_text(text):
    """
    Translate Chinese text to English.
    For programmatic SEO content, we'll use systematic translation patterns.
    """
    if not isinstance(text, str) or not contains_chinese(text):
        return text

    # Common translation patterns for this specific content type
    translations = {
        # Title patterns
        "终极评测": "Ultimate Review",
        "终极指南": "Ultimate Guide",
        "终极对比": "Ultimate Comparison",
        "深度评测": "Comprehensive Review",
        "完整指南": "Complete Guide",
        "详细对比": "Detailed Comparison",
        "专业指南": "Professional Guide",
        "专业评测": "Professional Review",
        "完整评测": "Complete Review",
        "系统性对比": "Systematic Comparison",
        "十大学术文献排版平台": "Top 10 Academic Document Typesetting Platforms",
        "十大": "Top 10",
        "助力学术出版": "Empowering Academic Publishing",
        "助力": "Empowering",

        # Description patterns
        "深度评测": "In-depth review of",
        "对比": "comparing",
        "为": "for",
        "提供": "provides",
        "技术方案": "technical solutions",
        "了解更多功能和价格对比": "Learn more about features and pricing comparisons",
        "找到最适合你的方案": "find the best solution for you",
        "专业评测助你决策": "Professional reviews help you make decisions",

        # Content patterns - General
        "全球": "Global",
        "市场规模": "market size",
        "预计达到": "expected to reach",
        "年增长率": "annual growth rate",
        "保持在": "maintained at",
        "以上": "above",
        "行业面临": "industry faces",
        "核心挑战": "core challenges",
        "传统方法": "traditional methods",
        "难以满足": "struggle to meet",
        "现代需求": "modern demands",
        "成为核心竞争力": "becomes a core competitive advantage",
        "选择合适的工具": "Choosing the right tool",
        "直接影响": "directly impacts",
        "效率、成本与质量": "efficiency, cost, and quality",

        # Section headers
        "一、行业特殊需求分析": "I. Industry Special Requirements Analysis",
        "二、十大平台深度评测": "II. Top 10 Platforms In-depth Review",
        "三、核心功能参数对比表": "III. Core Functionality Comparison Table",
        "四、发展趋势": "IV. Development Trends",
        "五、选型策略与实施路径": "V. Selection Strategy and Implementation Path",

        # Common phrases
        "与传统行业存在显著差异": "significantly differs from traditional industries",
        "需高效率处理": "requires high-efficiency processing",
        "需成本控制优化": "requires cost control optimization",
        "需高质量输出": "requires high-quality output",
        "需数据分析支持": "requires data analysis support",
        "工具需支持": "tools need to support",
        "自动化流程": "automated workflows",
        "成本分析管理": "cost analysis management",
        "质量检验功能": "quality inspection functions",
        "数据深度分析": "in-depth data analysis",

        # Platform descriptions
        "专业级": "Professional-level",
        "工具工具": "tool",
        "工具": "tool",
        "核心功能": "Core features:",
        "自动化管理": "automated management",
        "成本优化分析支持": "cost optimization analysis support",
        "质量检验深度化": "in-depth quality inspection",
        "价格": "Price:",
        "订阅制": "Subscription-based",
        "月": "/month",
        "特色": "Special features:",
        "专业能力顶尖": "top-tier professional capabilities",
        "适合大型团队": "suitable for large teams",
        "适合中型团队": "suitable for medium-sized teams",
        "适合小型团队": "suitable for small teams",
        "性价比高": "high cost-effectiveness",
        "快速上手": "quick to start",

        # Table headers
        "平台名称": "Platform Name",
        "核心定位": "Core Positioning",
        "价格区间": "Price Range",
        "效率能力": "Efficiency Capability",
        "成本控制": "Cost Control",
        "质量保障": "Quality Assurance",
        "数据分析": "Data Analysis",
        "高": "High",
        "中": "Medium",
        "低": "Low",

        # Trends
        "行业将呈现关键发展趋势": "The industry will present key development trends:",
        "AI驱动自动化": "AI-driven automation",
        "AI自动化覆盖率": "AI automation coverage",
        "从": "from",
        "提升至": "increases to",
        "效率提升": "efficiency improves by",
        "成本控制智能化": "intelligent cost control",
        "智能化成本控制覆盖率": "intelligent cost control coverage",
        "成本降低": "cost reduction by",
        "质量检验实时化": "real-time quality inspection",
        "实时质量检验覆盖率": "real-time quality inspection coverage",
        "质量提升": "quality improvement by",
        "数据分析深度化": "in-depth data analysis",
        "深度数据分析覆盖率": "in-depth data analysis coverage",
        "决策准确性提升": "decision-making accuracy improves by",

        # Selection strategy
        "团队应根据规模与需求选择工具": "Teams should choose tools based on size and requirements:",
        "选择企业级平台": "Choose enterprise-level platforms",
        "选择专业级平台": "Choose professional-level platforms",
        "选择轻量级平台": "Choose lightweight platforms",
        "月投入": "monthly investment of",
        "实施路径": "Implementation path:",
        "先完成需求评估": "First complete requirements assessment",
        "再试用核心工具": "then trial core tools",
        "最后规模化部署": "finally scale deployment",
        "预计": "Expected",
        "个": "",  # Remove Chinese counter word

        # Time periods
        "个月": "months",

        # SEO keywords patterns
        "排版工具": "typesetting tools",
        "排版系统": "typesetting system",
        "排版平台": "typesetting platform",
        "排版软件": "typesetting software",
        "学术排版": "academic typesetting",
        "文献排版": "document typesetting",
        "学术文献": "academic documents",
        "公式处理": "formula processing",
        "引用管理": "reference management",
        "工具软件": "tool software",

        # Author patterns
        "出版数字化研究院": "Publishing Digitalization Research Institute",
        "研究院": "Research Institute",
        "数字化": "Digitalization",
        "出版": "Publishing",
    }

    # Apply translations
    translated = text
    for chinese, english in sorted(translations.items(), key=lambda x: len(x[0]), reverse=True):
        translated = translated.replace(chinese, english)

    # Handle specific patterns that need regex
    translated = re.sub(r'2026年', '2026', translated)
    translated = re.sub(r'2026-2028', '2026-2028', translated)
    translated = re.sub(r'(\d+)(美元)', r'$\1', translated)
    translated = re.sub(r'(\d+)%', r'\1%', translated)  # Keep percentage format

    # Clean up multiple spaces
    translated = re.sub(r'  +', ' ', translated)

    # Clean up common HTML entities
    translated = translated.replace('&amp;', '&')

    return translated.strip()

def translate_keywords(keywords):
    """Translate SEO keywords array."""
    if not isinstance(keywords, list):
        return keywords

    translated_keywords = []
    keyword_map = {
        "学术排版工具": "academic typesetting tools",
        "LaTeX排版系统": "LaTeX typesetting system",
        "Overleaf学术排版": "Overleaf academic typesetting",
        "学术文献排版": "academic document typesetting",
        "公式处理平台": "formula processing platform",
        "引用管理工具": "reference management tools",
        "学术排版软件": "academic typesetting software",
        "文献排版平台": "document typesetting platform",
        "学术排版系统": "academic typesetting system",
        "排版工具软件": "typesetting tool software",
        "专业排版工具": "professional typesetting tools",
        "出版排版软件": "publishing typesetting software",
        "智能排版平台": "intelligent typesetting platform",
        "自动化排版系统": "automated typesetting system",
    }

    for keyword in keywords:
        if contains_chinese(keyword):
            # Try predefined mapping first
            if keyword in keyword_map:
                translated_keywords.append(keyword_map[keyword])
            else:
                # Generic translation
                translated_keywords.append(translate_text(keyword))
        else:
            translated_keywords.append(keyword)

    return translated_keywords

def process_file(filepath):
    """Process a single JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Translate each field
        if 'title' in data:
            data['title'] = translate_text(data['title'])

        if 'description' in data:
            data['description'] = translate_text(data['description'])

        if 'content' in data:
            data['content'] = translate_text(data['content'])

        if 'seo_keywords' in data:
            data['seo_keywords'] = translate_keywords(data['seo_keywords'])

        if 'author' in data:
            data['author'] = translate_text(data['author'])

        # Keep slug, published_at, language unchanged

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✓ Translated: {filepath.name}")
        return True

    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False

def main():
    """Main processing function."""
    data_dir = Path('/Users/gejiayu/owner/seo/data/publishing-media-tools')

    if not data_dir.exists():
        print(f"Directory not found: {data_dir}")
        return

    json_files = list(data_dir.glob('*.json'))
    print(f"Found {len(json_files)} JSON files to process")

    success_count = 0
    for filepath in json_files:
        if process_file(filepath):
            success_count += 1

    print(f"\nCompleted: {success_count}/{len(json_files)} files translated successfully")

if __name__ == '__main__':
    main()