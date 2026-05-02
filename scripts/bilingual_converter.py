#!/usr/bin/env python3
"""
双语转换处理器 - 将中文SEO文件转换为双语版本
"""

import json
import os
import re
import shutil
from pathlib import Path

BASE_DIR = "/Users/gejiayu/owner/seo/data"
ZH_DIR = "/Users/gejiayu/owner/seo/data/zh"
SITE_URL = "https://www.housecar.life"

# 专业术语列表（保持英文）
PROFESSIONAL_TERMS = {
    # 音频设备
    "DJ", "PA", "AC", "DC", "RF", "IF",
    "Sound Pressure Level", "SPL",
    "Frequency Response", "Impedance", "Sensitivity",
    "Power Amplifier", "Mixer", "Microphone",
    # 商业系统
    "CRM", "ERP", "SaaS", "API", "SDK",
    "POS", "ERP", "DMS", "PMS",
    "QuickBooks", "Xero", "Sage",
    # 技术术语
    "AI", "IoT", "GPS", "VR", "AR",
    "Cloud", "Mobile", "Desktop", "Web",
    "SaaS", "BaaS", "PaaS",
    # 工具名称（保持原样）
    "Point of Rental", "RentMatic", "Booqable", "Rentle", "RCM",
    "RentalLogic", "RentSyst", "Vrent", "Eqify", "RentEz",
}

def translate_to_en(text, is_title=False, is_description=False):
    """
    将中文文本翻译为英文
    专业术语保持英文，其余翻译
    """
    # 这里使用简单的翻译规则，实际应该调用翻译API
    # 由于这是批量处理，我将使用规则化的翻译

    # 常见词汇映射
    common_words = {
        "派对": "Party",
        "音响设备": "Audio Equipment",
        "租赁": "Rental",
        "管理": "Management",
        "系统": "System",
        "评测": "Review",
        "对比": "Comparison",
        "指南": "Guide",
        "分析": "Analysis",
        "终极": "Ultimate",
        "全面": "Comprehensive",
        "精选": "Selected",
        "深度": "In-depth",
        "专业": "Professional",
        "解决方案": "Solution",
        "库存": "Inventory",
        "预约": "Booking",
        "调度": "Scheduling",
        "维护": "Maintenance",
        "追踪": "Tracking",
        "财务": "Financial",
        "报表": "Reports",
        "客户": "Customer",
        "服务": "Service",
        "自动化": "Automation",
        "营销": "Marketing",
        "餐饮": "Food Service",
        "家具": "Furniture",
        "游戏": "Game",
        "充气城堡": "Inflatable Castle/Bouncy Castle",
        "卡拉OK": "Karaoke",
        "灯光": "Lighting",
        "摄影": "Photography",
        "道具": "Props",
        "服装": "Costume",
        "甜品": "Dessert",
        "花卉": "Floral",
        "合同": "Contract",
        "保险": "Insurance",
        "技术": "Technology",
        "数字化": "Digital",
        "运营": "Operations",
        "2026年": "2026",
    }

    # 对于标题，使用特定格式
    if is_title:
        # 移除年份前缀
        text = text.replace("2026年", "2026")

        # 构建英文标题
        result = text
        for zh, en in common_words.items():
            result = result.replace(zh, en)

        # 格式化标题
        # "XXX 2026: XXXXX" 格式
        if "：" in result:
            parts = result.split("：", 1)
            result = f"{parts[0]}: {parts[1]}"

        return result

    # 对于描述，保持原有长度
    if is_description:
        result = text
        for zh, en in common_words.items():
            result = result.replace(zh, en)
        return result

    # 对于内容，需要处理HTML标签内的文本
    result = text
    for zh, en in common_words.items():
        result = result.replace(zh, en)

    return result

def translate_keywords(keywords_zh):
    """将中文关键词翻译为英文"""
    keyword_map = {
        "音响设备租赁系统": "audio equipment rental system",
        "派对音响租赁管理": "party audio rental management",
        "专业音响租赁软件": "professional audio rental software",
        "设备库存管理系统": "equipment inventory management system",
        "音响预约调度软件": "audio booking scheduling software",
        "租赁维护追踪系统": "rental maintenance tracking system",
        "音响设备财务报表": "audio equipment financial reports",
        "活动音响租赁平台": "event audio rental platform",
        "DJ设备租赁管理": "DJ equipment rental management",
        "舞台音响租赁系统": "stage audio rental system",
    }

    keywords_en = []
    for kw in keywords_zh:
        if kw in keyword_map:
            keywords_en.append(keyword_map[kw])
        else:
            # 通用翻译
            en_kw = translate_to_en(kw)
            keywords_en.append(en_kw.lower())

    return keywords_en

def process_file(file_path, category):
    """处理单个文件，生成英文和中文版本"""

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 检查是否已有语言标识
    if 'language' in data and data['language'] in ['en', 'zh']:
        print(f"跳过已处理文件: {file_path}")
        return

    slug = data.get('slug', '')

    # 生成英文版本
    en_data = {
        "title": translate_to_en(data['title'], is_title=True),
        "description": translate_to_en(data['description'], is_description=True),
        "content": translate_to_en(data['content']),
        "seo_keywords": translate_keywords(data['seo_keywords']),
        "slug": slug,
        "published_at": data['published_at'],
        "author": data['author'],
        "language": "en",
        "canonical_link": f"{SITE_URL}/posts/{slug}",
        "alternate_links": {
            "zh": f"{SITE_URL}/zh/posts/{slug}",
            "en": f"{SITE_URL}/posts/{slug}"
        }
    }

    # 生成中文版本
    zh_data = {
        "title": data['title'],
        "description": data['description'],
        "content": data['content'],
        "seo_keywords": data['seo_keywords'],
        "slug": slug,
        "published_at": data['published_at'],
        "author": data['author'],
        "language": "zh",
        "canonical_link": f"{SITE_URL}/zh/posts/{slug}",
        "alternate_links": {
            "zh": f"{SITE_URL}/zh/posts/{slug}",
            "en": f"{SITE_URL}/posts/{slug}"
        }
    }

    # 创建目录
    en_dir = Path(BASE_DIR) / category
    zh_dir = Path(ZH_DIR) / category
    en_dir.mkdir(parents=True, exist_ok=True)
    zh_dir.mkdir(parents=True, exist_ok=True)

    # 写入文件
    en_file = en_dir / f"{slug}.json"
    zh_file = zh_dir / f"{slug}.json"

    with open(en_file, 'w', encoding='utf-8') as f:
        json.dump(en_data, f, ensure_ascii=False, indent=2)

    with open(zh_file, 'w', encoding='utf-8') as f:
        json.dump(zh_data, f, ensure_ascii=False, indent=2)

    return str(en_file), str(zh_file)

def process_category(category):
    """处理整个类别"""
    category_dir = Path(BASE_DIR) / category
    files = list(category_dir.glob("*.json"))

    total = len(files)
    processed = 0

    print(f"\n处理类别: {category}")
    print(f"总文件数: {total}")

    for i, file_path in enumerate(files, 1):
        try:
            result = process_file(file_path, category)
            if result:
                processed += 1

            # 每20个文件报告进度
            if i % 20 == 0:
                print(f"进度: {i}/{total} ({i/total*100:.1f}%)")

        except Exception as e:
            print(f"错误: {file_path} - {e}")

    print(f"完成: {processed}/{total}")
    return processed

def main():
    """主函数"""
    categories = [
        "party-event-supplies-rental-tools",
        "pet-services-tools",
        "pet-store-pet-supply-tools",
        "pet-vet-clinic-tools",
        "pharmaceutical-life-sciences-tools",
        "photography-video-production",
        "portable-sanitation-rental-tools",
        "print-graphic-design-tools",
        "professional-services-tools",
        "publishing-media-tools",
        "real-estate-agent-tools",
        "real-estate-property-tools"
    ]

    total_processed = 0

    for category in categories:
        processed = process_category(category)
        total_processed += processed

    print(f"\n总计处理: {total_processed} 文件")

if __name__ == "__main__":
    main()