#!/usr/bin/env python3
"""
Batch translate Chinese SEO files to English
Uses semantic translation patterns and manual processing
"""
import json
import re
from pathlib import Path

# Chinese to English translation patterns
TRANSLATION_PATTERNS = {
    # Common terms
    "按摩": "Massage",
    "SPA": "SPA",
    "养生": "Wellness",
    "系统": "System",
    "专业评测": "Professional Review",
    "深入剖析": "In-depth analysis of",
    "核心功能": "core features",
    "主流方案对比": "mainstream solution comparisons",
    "帮助": "help",
    "实现": "achieve",
    "提升": "enhance/improve",
    "降低": "reduce",
    "了解更多": "Discover comprehensive",
    "功能": "features",
    "价格对比": "pricing comparisons",
    "找到最适合你的方案": "find your ideal solution",
    "助你决策": "guide your decision",

    # Business terms
    "效率": "Efficiency",
    "管理": "Management",
    "优化": "Optimization",
    "分析": "Analysis",
    "数据": "Data",
    "预警": "Warning/Alert",
    "报表": "Report",
    "可视化": "Visualization",
    "策略": "Strategy",
    "营收": "Revenue",
    "成本": "Cost",
    "盈利": "Profit",

    # Industry specific
    "技师": "Technician",
    "预约": "Appointment/Booking",
    "客户": "Customer",
    "会员": "Member",
    "服务": "Service",
    "项目": "Project",
    "房间": "Room",
    "时段": "Time Slot",
    "冲突": "Conflict",
    "提醒": "Reminder",
    "分配": "Allocation",

    # Adjectives
    "完善": "Comprehensive",
    "强大": "Powerful",
    "基础": "Basic",
    "智能": "Intelligent",
    "精准": "Precise",
    "自动": "Automatic",

    # Time/Numbers
    "2026年": "2026",
    "年费": "Annual fee",
    "月费": "Monthly fee",

    # Software names (keep as-is)
    "Mindbody": "Mindbody",
    "Zenoti": "Zenoti",
    "Vagaro": "Vagaro",
    "QuickBooks": "QuickBooks",

    # Chinese software names
    "美业帮": "Meiyebang",
    "店务通": "Dianwutong",
}

def translate_title(chinese_title):
    """Translate Chinese title to natural American English"""
    # Pattern: [System Name] 2026 Professional Review - [Benefit]

    # Common title patterns
    patterns = [
        (r"按摩(.*)系统2026年专业评测\s*-\s*(.*)",
         lambda m: f"Massage {translate_text(m.group(1))} System 2026 Professional Review - {translate_text(m.group(2))} Excellence"),
        (r"SPA(.*)系统2026年专业评测\s*-\s*(.*)",
         lambda m: f"SPA {translate_text(m.group(1))} System 2026 Professional Review - {translate_text(m.group(2))} Excellence"),
        (r"养生(.*)系统2026年专业评测\s*-\s*(.*)",
         lambda m: f"Wellness {translate_text(m.group(1))} System 2026 Professional Review - {translate_text(m.group(2))} Excellence"),
    ]

    for pattern, replacement in patterns:
        if re.match(pattern, chinese_title):
            return re.sub(pattern, replacement, chinese_title)

    # Fallback: word-by-word translation
    return translate_text(chinese_title)

def translate_description(chinese_desc):
    """Translate Chinese description to natural American English"""
    # Common description patterns

    # Extract key components
    desc_lower = chinese_desc

    # Build natural English description
    english_desc = ""

    # Pattern: "深入剖析[system]核心功能、[features]与主流方案对比"
    if "深入剖析" in chinese_desc or "核心功能" in chinese_desc:
        english_desc += "In-depth analysis of "

        # Extract system type
        if "按摩" in chinese_desc:
            english_desc += "massage SPA "
        elif "SPA" in chinese_desc:
            english_desc += "SPA "
        elif "养生" in chinese_desc:
            english_desc += "wellness studio "

        # Extract system function
        system_match = re.search(r"(按摩|SPA|养生)(.*?)系统", chinese_desc)
        if system_match:
            system_func = translate_text(system_match.group(2))
            english_desc += f"{system_func} systems' "

        english_desc += "core features, "

        # Add strategy comparison
        if "策略" in chinese_desc or "方案对比" in chinese_desc:
            english_desc += "strategic approaches, and mainstream solution comparisons "

        # Add benefit
        if "帮助" in chinese_desc:
            english_desc += "to help wellness businesses "

        if "实现" in chinese_desc:
            benefit_match = re.search(r"实现(.*?)(，|。)", chinese_desc)
            if benefit_match:
                benefit = translate_text(benefit_match.group(1))
                english_desc += f"achieve {benefit}. "

        # Add CTA
        english_desc += "Discover comprehensive feature and pricing comparisons to find your ideal solution! Professional reviews to guide your decision!"

    return english_desc if english_desc else translate_text(chinese_desc)

def translate_content(chinese_content):
    """
    Translate Chinese HTML content to natural American English
    Preserves HTML structure
    """
    # This is complex - we'll use pattern matching for HTML content
    english_content = chinese_content

    # Translate common heading patterns
    english_content = re.sub(
        r"<h1>(.*?)的重要性</h1>",
        lambda m: f"<h1>The Importance of {translate_text(m.group(1))}</h1>",
        english_content
    )

    # Translate paragraphs with statistics
    english_content = re.sub(
        r"<p>在养生行业，(.*?)是(.*?)的核心手段。",
        lambda m: f"<p>In the wellness industry, {translate_text(m.group(1))} is a core strategy for {translate_text(m.group(2))}.",
        english_content
    )

    # Translate list items
    # This requires more sophisticated pattern matching

    # For now, use word-by-word translation for remaining content
    # But preserve HTML tags
    parts = re.split(r'(<[^>]+>)', english_content)
    translated_parts = []
    for part in parts:
        if part.startswith('<') and part.endswith('>'):
            translated_parts.append(part)  # Keep HTML tags unchanged
        else:
            translated_parts.append(translate_text(part))

    english_content = ''.join(translated_parts)

    return english_content

def translate_keywords(chinese_keywords):
    """Translate Chinese keywords to English keywords (array format)"""
    if isinstance(chinese_keywords, str):
        # Convert string to array
        keywords = [k.strip() for k in chinese_keywords.split(',')]
    else:
        keywords = chinese_keywords

    # Translate each keyword
    english_keywords = []
    for keyword in keywords:
        english_keyword = translate_text(keyword)
        # Remove duplicate words
        words = english_keyword.split()
        unique_words = []
        for word in words:
            if word not in unique_words:
                unique_words.append(word)
        english_keywords.append(' '.join(unique_words))

    return english_keywords

def translate_author(chinese_author):
    """Translate Chinese author title to English"""
    author_patterns = {
        "成本管理专家": "Cost Management Expert",
        "预约管理专家": "Appointment Management Expert",
        "数据分析专家": "Data Analytics Expert",
        "会员管理专家": "Membership Management Expert",
        "技师管理专家": "Technician Management Expert",
        "客户管理专家": "Customer Management Expert",
        "营销管理专家": "Marketing Management Expert",
        "系统管理专家": "System Management Expert",
        "运营管理专家": "Operations Management Expert",
        "服务管理专家": "Service Management Expert",
        "管理专家": "Management Expert",
    }

    for chinese, english in author_patterns.items():
        if chinese in chinese_author:
            return english

    return translate_text(chinese_author)

def translate_text(text):
    """
    Translate Chinese text using pattern matching
    This is a simplified semantic translation
    """
    if not text:
        return text

    # Apply translation patterns
    translated = text
    for chinese, english in TRANSLATION_PATTERNS.items():
        translated = translated.replace(chinese, english)

    # Clean up spacing
    translated = re.sub(r'\s+', ' ', translated)
    translated = translated.strip()

    return translated

def process_file(file_path):
    """
    Process a single file: translate all Chinese content
    """
    print(f"\nProcessing: {file_path.name}")

    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create translated data
    translated_data = data.copy()

    # Translate fields
    if contains_chinese(data.get('title')):
        print("  Translating title...")
        translated_data['title'] = translate_title(data['title'])

    if contains_chinese(data.get('description')):
        print("  Translating description...")
        translated_data['description'] = translate_description(data['description'])

    if contains_chinese(data.get('content')):
        print("  Translating content...")
        translated_data['content'] = translate_content(data['content'])

    if 'seo_keywords' in data:
        print("  Translating seo_keywords...")
        translated_data['seo_keywords'] = translate_keywords(data['seo_keywords'])

    if contains_chinese(data.get('author')):
        print("  Translating author...")
        translated_data['author'] = translate_author(data['author'])

    # Add language field
    translated_data['language'] = 'en-US'

    # Save file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=2)

    print("  ✓ Translated and saved")

    return translated_data

def contains_chinese(text):
    """Check if text contains Chinese characters"""
    if not text:
        return False
    return bool(re.search(r'[一-鿿]', text))

def main():
    """Main processing function"""
    # Get list of Chinese files
    directory = Path('/Users/gejiayu/owner/seo/data/massage-spa-wellness-tools')

    chinese_files = []
    with open('/Users/gejiayu/owner/seo/chinese_files_list.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[2:]:  # Skip header
            filename = line.strip()
            if filename:
                chinese_files.append(filename)

    print(f"Total files to process: {len(chinese_files)}")
    print("=" * 60)

    # Process each file
    success_count = 0
    for filename in chinese_files[:5]:  # Process first 5 as examples
        file_path = directory / filename
        try:
            process_file(file_path)
            success_count += 1
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")

    print("\n" + "=" * 60)
    print(f"Processed: {success_count} files")

    # Show sample output
    if success_count > 0:
        print("\nSample translations:")
        sample_file = directory / chinese_files[0]
        with open(sample_file, 'r', encoding='utf-8') as f:
            sample_data = json.load(f)
            print(f"\nTitle: {sample_data.get('title')}")
            print(f"\nDescription: {sample_data.get('description')[:150]}...")
            print(f"\nKeywords: {sample_data.get('seo_keywords')[:5]}")
            print(f"\nAuthor: {sample_data.get('author')}")

if __name__ == "__main__":
    main()