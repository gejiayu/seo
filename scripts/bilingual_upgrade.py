#!/usr/bin/env python3
"""
pSEO Bilingual Architecture Upgrade Script
双语化架构升级：英文主站 + 中文子站
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
import random

# 翻译映射词典（关键词级别）
KEYWORD_TRANSLATIONS = {
    # 中文 → 英文
    "理赔人工智能": "Claims AI",
    "理赔AI平台": "Claims AI Platform",
    "理赔AI算法": "Claims AI Algorithm",
    "理赔AI模型": "Claims AI Model",
    "理赔AI应用": "Claims AI Application",
    "电动滑板车维护": "Electric Scooter Maintenance",
    "车辆保养": "Vehicle Maintenance",
    "故障预测": "Fault Prediction",
    "维修管理": "Repair Management",
    "备件管理": "Parts Management",
    "评测": "Review",
    "对比": "Comparison",
    "指南": "Guide",
    "工具": "Tools",
    "系统": "System",
    "平台": "Platform",
    "软件": "Software",

    # 英文 → 中文
    "Claims AI": "理赔AI",
    "Electric Scooter": "电动滑板车",
    "Maintenance": "维护",
    "Management": "管理",
    "System": "系统",
    "Platform": "平台",
    "Tools": "工具",
    "Review": "评测",
    "Comparison": "对比",
    "Guide": "指南",
}

def is_chinese_content(text: str) -> bool:
    """判断内容是否主要为中文"""
    chinese_chars = sum(1 for char in text if '一' <= char <= '鿿')
    return chinese_chars > len(text) * 0.3

def translate_keywords(keywords: List[str], target_lang: str) -> List[str]:
    """翻译关键词数组"""
    translated = []
    for keyword in keywords:
        if target_lang == 'en':
            # 中文 → 英文
            translated_keyword = KEYWORD_TRANSLATIONS.get(keyword, keyword)
            if is_chinese_content(keyword) and translated_keyword == keyword:
                # 如果没有找到翻译且是中文，保留原词（后续可手动翻译）
                translated_keyword = keyword
        else:
            # 英文 → 中文
            translated_keyword = KEYWORD_TRANSLATIONS.get(keyword, keyword)
            if not is_chinese_content(keyword) and translated_keyword == keyword:
                # 如果没有找到翻译且是英文，保留原词
                translated_keyword = keyword
        translated.append(translated_keyword)
    return translated

def translate_title(title: str, target_lang: str) -> str:
    """翻译标题（简化版：仅处理已知关键词）"""
    # 移除CTR增强的后缀
    title = re.sub(r'｜2026年评测$', '', title)
    title = re.sub(r' - 2026 Review$', '', title)

    # 关键词替换（简化版）
    translated = title
    for cn, en in KEYWORD_TRANSLATIONS.items():
        if target_lang == 'en' and cn in translated:
            translated = translated.replace(cn, en)
        elif target_lang == 'zh' and en in translated:
            translated = translated.replace(en, cn)

    # 添加CTR增强后缀
    if target_lang == 'en':
        if '2026' not in translated:
            translated = f"{translated} - 2026 Review"
    else:
        if '2026' not in translated:
            translated = f"{translated}｜2026年评测"

    return translated

def translate_description(desc: str, target_lang: str) -> str:
    """翻译描述（简化版：仅处理已知关键词）"""
    # 移除CTR增强的CTA
    desc = re.sub(r'了解更多功能和价格对比，找到最适合你的方案！.*$', '', desc)
    desc = re.sub(r'Discover the best options.*$', '', desc)

    # 关键词替换
    translated = desc
    for cn, en in KEYWORD_TRANSLATIONS.items():
        if target_lang == 'en' and cn in translated:
            translated = translated.replace(cn, en)
        elif target_lang == 'zh' and en in translated:
            translated = translated.replace(en, cn)

    # 添加CTA
    if target_lang == 'en':
        cta = " Discover the best options and make your choice today!"
    else:
        cta = "了解更多功能和价格对比，找到最适合你的方案！"

    # 确保长度在140-160字符
    if len(translated) > 160:
        translated = translated[:157] + "..."
    elif len(translated) < 140:
        translated = translated + cta
    else:
        translated = translated

    return translated

def generate_canonical_link(slug: str, category: str) -> str:
    """生成canonical链接（指向英文版）"""
    site_url = os.environ.get('SITE_URL', 'https://www.housecar.life')
    return f"{site_url}/posts/{slug}"

def generate_alternate_links(slug: str, category: str) -> Dict[str, str]:
    """生成hreflang alternate链接"""
    site_url = os.environ.get('SITE_URL', 'https://www.housecar.life')
    return {
        'en-US': f"{site_url}/posts/{slug}",
        'zh-CN': f"{site_url}/zh/posts/{slug}"
    }

def convert_slug_to_english(slug: str, title: str) -> str:
    """转换slug为英文（如果包含中文）"""
    if is_chinese_content(slug):
        # 从英文标题提取slug
        # 移除CTR后缀
        clean_title = re.sub(r'｜2026年评测$', '', title)
        clean_title = re.sub(r' - 2026 Review$', '', clean_title)

        # 转换为slug格式
        slug = clean_title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[\s]+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        slug = slug.strip('-')

    return slug

def process_file(filepath: Path, test_mode: bool = False) -> Tuple[Dict, Dict]:
    """处理单个文件，生成双语版本"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_title = data.get('title', '')
    original_desc = data.get('description', '')
    original_keywords = data.get('seo_keywords', [])
    original_slug = data.get('slug', '')
    category = filepath.parent.name

    # 判断原始语言
    is_chinese = is_chinese_content(original_title)

    # 生成英文版
    if is_chinese:
        en_title = translate_title(original_title, 'en')
        en_desc = translate_description(original_desc, 'en')
        en_keywords = translate_keywords(original_keywords, 'en')
        en_slug = convert_slug_to_english(original_slug, en_title)
    else:
        en_title = original_title
        en_desc = original_desc
        en_keywords = original_keywords if isinstance(original_keywords, list) else []
        en_slug = original_slug

    # 生成中文版
    if is_chinese:
        zh_title = original_title
        zh_desc = original_desc
        zh_keywords = original_keywords if isinstance(original_keywords, list) else []
        zh_slug = original_slug
    else:
        zh_title = translate_title(original_title, 'zh')
        zh_desc = translate_description(original_desc, 'zh')
        zh_keywords = translate_keywords(original_keywords, 'zh')
        zh_slug = original_slug  # 中文版slug保持不变（或可转换为拼音）

    # 构建英文版JSON
    en_data = {
        'title': en_title,
        'description': en_desc,
        'content': data.get('content', ''),
        'seo_keywords': en_keywords,
        'slug': en_slug,
        'published_at': data.get('published_at', ''),
        'author': data.get('author', ''),
        'language': 'en-US',
        'canonical_link': generate_canonical_link(en_slug, category),
        'alternate_links': generate_alternate_links(en_slug, category),
        'category': category
    }

    # 构建中文版JSON
    zh_data = {
        'title': zh_title,
        'description': zh_desc,
        'content': data.get('content', ''),
        'seo_keywords': zh_keywords,
        'slug': zh_slug,
        'published_at': data.get('published_at', ''),
        'author': data.get('author', ''),
        'language': 'zh-CN',
        'canonical_link': generate_canonical_link(en_slug, category),  # 中文版canonical指向英文版
        'alternate_links': generate_alternate_links(en_slug, category),
        'category': category
    }

    return en_data, zh_data

def test_run():
    """测试模式：处理10个样本文件"""
    print("=" * 80)
    print("pSEO Bilingual Architecture Upgrade - Test Mode")
    print("=" * 80)
    print()

    # 找到5个中文文件和5个英文文件
    all_files = list(Path('data').rglob('*.json'))

    chinese_files = []
    english_files = []

    for filepath in all_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                title = data.get('title', '')
                if is_chinese_content(title):
                    chinese_files.append(filepath)
                else:
                    english_files.append(filepath)
        except:
            continue

    # 随机选择样本
    test_cn_files = random.sample(chinese_files, min(5, len(chinese_files)))
    test_en_files = random.sample(english_files, min(5, len(english_files)))

    print(f"Selected {len(test_cn_files)} Chinese files and {len(test_en_files)} English files")
    print()

    # 处理并展示对比
    for filepath in test_cn_files + test_en_files:
        print(f"📄 Processing: {filepath}")
        print()

        # 读取原始文件
        with open(filepath, 'r', encoding='utf-8') as f:
            original = json.load(f)

        # 处理生成双语版本
        en_data, zh_data = process_file(filepath, test_mode=True)

        # 展示对比
        is_cn = is_chinese_content(original.get('title', ''))
        lang_label = "Chinese" if is_cn else "English"

        print(f"  Original ({lang_label}):")
        print(f"    Title: {original.get('title', '')}")
        print(f"    Description: {original.get('description', '')[:100]}...")
        print(f"    Keywords: {original.get('seo_keywords', [])[:3]}")
        print(f"    Slug: {original.get('slug', '')}")
        print()

        print(f"  English Version:")
        print(f"    Title: {en_data['title']}")
        print(f"    Description: {en_data['description'][:100]}...")
        print(f"    Keywords: {en_data['seo_keywords'][:3]}")
        print(f"    Slug: {en_data['slug']}")
        print(f"    Language: {en_data['language']}")
        print(f"    Canonical: {en_data['canonical_link']}")
        print(f"    Alternate: {en_data['alternate_links']}")
        print()

        print(f"  Chinese Version:")
        print(f"    Title: {zh_data['title']}")
        print(f"    Description: {zh_data['description'][:100]}...")
        print(f"    Keywords: {zh_data['seo_keywords'][:3]}")
        print(f"    Slug: {zh_data['slug']}")
        print(f"    Language: {zh_data['language']}")
        print(f"    Canonical: {zh_data['canonical_link']}")
        print(f"    Alternate: {zh_data['alternate_links']}")
        print()

        print("-" * 80)
        print()

    print("Test complete. Please review the output above.")
    print("If satisfied, run the full execution mode.")

def full_run():
    """全量执行模式"""
    print("=" * 80)
    print("pSEO Bilingual Architecture Upgrade - Full Execution")
    print("=" * 80)
    print()

    # 创建zh子目录结构
    data_dir = Path('data')
    zh_dir = Path('data/zh')

    # 统计
    total_files = 0
    processed_files = 0
    errors = 0

    # 遍历所有JSON文件
    for json_file in data_dir.rglob('*.json'):
        if 'zh' in json_file.parts:  # 跳过zh子目录下的文件
            continue

        total_files += 1

        try:
            # 处理文件
            en_data, zh_data = process_file(json_file)

            # 英文版路径（保持原位置）
            category = json_file.parent.name
            en_filename = en_data['slug'] + '.json'
            en_filepath = json_file.parent / en_filename

            # 中文版路径（zh子目录）
            zh_category_dir = zh_dir / category
            zh_category_dir.mkdir(parents=True, exist_ok=True)
            zh_filename = zh_data['slug'] + '.json'
            zh_filepath = zh_category_dir / zh_filename

            # 写入英文版
            with open(en_filepath, 'w', encoding='utf-8') as f:
                json.dump(en_data, f, ensure_ascii=False, indent=2)

            # 写入中文版
            with open(zh_filepath, 'w', encoding='utf-8') as f:
                json.dump(zh_data, f, ensure_ascii=False, indent=2)

            processed_files += 1

            # 每100个文件打印进度
            if total_files % 100 == 0:
                print(f"Processed: {total_files} files")

        except Exception as e:
            print(f"Error processing {json_file}: {e}")
            errors += 1

    print()
    print("=" * 80)
    print("Execution Complete")
    print(f"Total files: {total_files}")
    print(f"Processed files: {processed_files}")
    print(f"Errors: {errors}")
    print("=" * 80)

    # 展示新的目录结构
    print()
    print("New directory structure:")
    print("data/")
    print("├── [category]/          # 英文主站")
    print("│   ├── [slug].json")
    print("└── zh/                  # 中文子站")
    print("    └── [category]/")
    print("        └── [slug].json")

def main():
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        test_run()
    elif len(sys.argv) > 1 and sys.argv[1] == '--full':
        full_run()
    else:
        print("Usage:")
        print("  python scripts/bilingual_upgrade.py --test   # Test mode (10 samples)")
        print("  python scripts/bilingual_upgrade.py --full   # Full execution mode")

if __name__ == "__main__":
    main()