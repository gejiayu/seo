#!/usr/bin/env python3
"""
Hybrid bilingual translation:
- API translation for title (most critical SEO field)
- Template translation for description and keywords
- Content placeholder (skip for speed)

Balances quality and speed.
"""

import json
import sys
from pathlib import Path
from deep_translator import GoogleTranslator

BASE_DIR = Path("/Users/gejiayu/owner/seo/data")
LOG_FILE = Path("/tmp/translate_hybrid.txt")

CATEGORIES = [
    "tennis-racket-rental-tools",
    "tent-canopy-rental-tools",
    "tool-hardware-rental-tools",
    "transportation-fleet-tools",
    "travel-agency-tour-operator-tools",
    "travel-hospitality-tools"
]

# Template translation dictionary
CN_TO_EN = {
    "评测": "Review", "系统": "System", "平台": "Platform", "工具": "Tools",
    "管理": "Management", "分析": "Analytics", "租赁": "Rental", "预订": "Booking",
    "维护": "Maintenance", "追踪": "Tracking", "智能": "Smart", "自动化": "Automated",
    "数字化": "Digital", "解决方案": "Solution", "关键": "Key", "核心": "Core",
    "专业": "Professional", "深度": "In-depth", "全面": "Comprehensive",
    "数据": "Data", "报告": "Reporting", "趋势": "Trends", "预测": "Forecast",
    "财务": "Financial", "客户": "Customer", "员工": "Staff", "培训": "Training",
    "网球": "Tennis", "球拍": "Racket", "场地": "Court", "设备": "Equipment",
    "帐篷": "Tent", "运输": "Transportation", "车队": "Fleet", "旅游": "Travel",
    "酒店": "Hotel", "硬件": "Hardware", "物联网": "IoT", "传感器": "Sensor",
    "的": "for", "与": "&", "中": "in", "和": "and",
    "了解更多功能和价格对比": "Compare features and pricing",
    "找到最适合你的方案": "to find your ideal solution",
    "专业评测助你决策": "Professional reviews help you decide",
}

translator = GoogleTranslator(source='zh-CN', target='en')

def log(msg):
    with open(LOG_FILE, 'a') as f:
        f.write(msg + '\n')
    print(msg, flush=True)

def translate_api(text):
    """Use API translation for critical fields."""
    if not any('一' <= c <= '鿿' for c in text):
        return text
    try:
        return translator.translate(text[:200])  # Limit length
    except:
        return text

def translate_template(text):
    """Use template for faster translation."""
    result = text
    for cn, en in sorted(CN_TO_EN.items(), key=lambda x: -len(x[0])):
        result = result.replace(cn, en)
    return result

def process_file(fp, count, total):
    log(f"[{count}/{total}] {fp.name}")

    with open(fp, 'r', encoding='utf-8') as f:
        original = json.load(f)

    title_cn = original['title']
    desc_cn = original['description']
    content_cn = original['content']
    keywords_cn = original['seo_keywords']
    slug = original['slug']
    published = original['published_at']
    author = original['author']

    # API translate title (most important)
    title_en = translate_api(title_cn)
    if '2026' not in title_en:
        title_en = f"{title_en} | 2026 Review"

    # Template translate description (faster)
    desc_en = translate_template(desc_cn)
    if 'compare' not in desc_en.lower():
        desc_en = f"{desc_en} Compare features and pricing."

    # Template translate keywords
    keywords_en = [translate_template(kw) for kw in keywords_cn]

    # Content placeholder
    content_en = "[English content placeholder]"

    bilingual = {
        "title": title_en, "title_cn": title_cn,
        "description": desc_en, "description_cn": desc_cn,
        "content": content_en, "content_cn": content_cn,
        "seo_keywords": keywords_en, "seo_keywords_cn": keywords_cn,
        "slug": slug, "published_at": published, "author": author
    }

    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(bilingual, f, ensure_ascii=False, indent=2)

def main():
    LOG_FILE.unlink(missing_ok=True)
    log("=" * 60)
    log("HYBRID BILINGUAL TRANSLATION")
    log("API for title, Template for desc/keywords")
    log("=" * 60)

    total = sum(len(list((BASE_DIR / cat).glob("*.json"))) for cat in CATEGORIES)
    log(f"Total: {total} files\n")

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
                    log(f"\n=== PROGRESS: {count}/{total} ({100*count//total}%) ===\n")
            except Exception as e:
                log(f"ERROR: {fp.name} - {e}")

    log(f"\n=== COMPLETE: {count}/{total} ===")

if __name__ == "__main__":
    main()