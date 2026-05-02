#!/usr/bin/env python3
"""
SEO双语文件批量转换处理器
将中文文件转换为英文+中文双语版本
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime

BASE_DIR = "/Users/gejiayu/owner/seo/data"
ZH_DIR = "/Users/gejiayu/owner/seo/data/zh"
SITE_URL = "https://www.housecar.life"

# 统计计数器
total_files = 0
processed_files = 0
error_files = 0

def translate_title(title_zh):
    """
    翻译中文标题为英文标题
    格式：[吸引力词汇] + [主题] + [2026] + [附加价值]
    """
    # 常见词汇映射
    words_map = {
        "派对音响设备租赁管理系统": "Party Audio Equipment Rental Management System",
        "派对服装道具租赁管理系统": "Party Costume Prop Rental Management System",
        "派对装饰租赁CRM系统": "Party Decoration Rental CRM System",
        "派对甜品设备租赁管理系统": "Party Dessert Equipment Rental Management System",
        "派对设备租赁预约管理系统": "Party Equipment Rental Booking Management System",
        "派对活动用品租赁营销自动化系统": "Party Event Supplies Rental Marketing Automation System",
        "派对花卉装饰租赁管理系统": "Party Floral Decoration Rental Management System",
        "派对餐饮设备租赁管理平台": "Party Food Service Equipment Rental Management Platform",
        "派对家具租赁库存管理系统": "Party Furniture Rental Inventory Management System",
        "派对游戏设备租赁管理系统": "Party Game Equipment Rental Management System",
        "派对充气城堡租赁管理系统": "Party Inflatable Castle Rental Management System",
        "派对卡拉OK设备租赁管理系统": "Party Karaoke Equipment Rental Management System",
        "派对灯光设备租赁财务管理": "Party Lighting Equipment Rental Financial Management",
        "派对摄影棚租赁管理系统": "Party Photo Booth Rental Management System",
        "派对摄影设备租赁管理系统": "Party Photography Equipment Rental Management System",
        "派对租赁合同管理系统": "Party Rental Contract Management System",
        "派对租赁客户服务管理系统": "Party Rental Customer Service Management System",
        "派对租赁保险管理系统": "Party Rental Insurance Management System",
        "派对舞台设备租赁项目管理": "Party Stage Equipment Rental Project Management",

        # 通用词汇
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
        "管理": "Management",
        "系统": "System",
        "软件": "Software",
        "平台": "Platform",
        "工具": "Tools",
        "2026年": "2026",
        "2026": "2026",
    }

    # 处理标题
    title_en = title_zh

    # 移除年份前缀中的"年"
    title_en = title_en.replace("2026年", "2026")

    # 替换中文词汇
    for zh, en in sorted(words_map.items(), key=lambda x: len(x[0]), reverse=True):
        title_en = title_en.replace(zh, en)

    # 格式化：添加吸引力词汇
    if not any(word in title_en.lower() for word in ['best', 'top', 'ultimate', 'guide', 'review', 'comparison']):
        # 检查是否已有评测/对比等词汇
        if 'Review' in title_en or 'Comparison' in title_en or 'Guide' in title_en or 'Analysis' in title_en:
            # 已有，保持原样
            pass
        else:
            # 添加吸引力词汇
            title_en = f"Best {title_en}"

    # 分隔符标准化
    if "：" in title_en:
        parts = title_en.split("：", 1)
        title_en = f"{parts[0]}: {parts[1]}"
    elif "|" in title_en:
        # 保持竖线分隔符
        pass

    return title_en

def translate_description(desc_zh):
    """
    翻译中文描述为英文描述
    添加CTA，控制在140-160字符
    """
    words_map = {
        "深度评测": "In-depth review of",
        "对比": "Compare",
        "分析": "Analyze",
        "核心功能": "core features",
        "价格": "pricing",
        "性能": "performance",
        "助您选择": "Help you choose",
        "最佳": "best",
        "解决方案": "solutions",
        "适合": "suitable for",
        "中小企业": "small business",
        "初创企业": "startups",
        "成长型企业": "growing business",
        "大型企业": "large enterprises",
        "全面": "comprehensive",
        "专业": "professional",
        "精选": "selected",
        "深度": "detailed",
        "终极": "ultimate",
        "指南": "guide",
        "评测": "review",
        "2026年": "2026",
        "。": ".",
        "，": ",",
    }

    desc_en = desc_zh
    for zh, en in sorted(words_map.items(), key=lambda x: len(x[0]), reverse=True):
        desc_en = desc_en.replace(zh, en)

    # 添加CTA
    cta_phrases = [
        "Discover pricing, features, and expert ratings. Find your perfect match today!",
        "Read our expert analysis and find the perfect solution.",
        "Get your comprehensive comparison and make the right choice.",
        "See the full review and find the best tool for your needs.",
    ]

    # 检查是否已有CTA词汇
    cta_words = ['discover', 'learn', 'read', 'find', 'get', 'see', 'compare', 'explore']
    desc_lower = desc_en.lower()

    if not any(word in desc_lower for word in cta_words):
        # 添加CTA
        cta = cta_phrases[0]
        desc_en = f"{desc_en} {cta}"

    # 控制长度（140-160字符）
    if len(desc_en) > 160:
        desc_en = desc_en[:160]
    elif len(desc_en) < 140:
        # 添加额外内容
        desc_en = f"{desc_en} Expert insights included."

    return desc_en

def translate_keywords(keywords_zh):
    """
    翻译中文关键词为英文关键词
    保持专业术语英文
    """
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
        "派对设备租赁": "party equipment rental",
        "活动设备管理": "event equipment management",
        "租赁软件": "rental software",
        "库存管理": "inventory management",
        "预约系统": "booking system",
        "客户服务": "customer service",
        "财务管理": "financial management",
        "合同管理": "contract management",
        "营销自动化": "marketing automation",
    }

    keywords_en = []
    for kw in keywords_zh:
        if kw in keyword_map:
            keywords_en.append(keyword_map[kw])
        else:
            # 通用翻译
            kw_en = kw
            for zh, en in keyword_map.items():
                if zh in kw:
                    kw_en = kw.replace(zh, en)
            keywords_en.append(kw_en.lower())

    return keywords_en

def translate_content(content_zh):
    """
    翻译中文内容为英文内容
    保持HTML结构，翻译文本内容
    专业术语保持英文
    """
    # 内容词汇映射
    content_map = {
        "派对音响设备租赁管理系统": "Party Audio Equipment Rental Management System",
        "派对音响设备租赁行业": "party audio equipment rental industry",
        "技术革新": "technological revolution",
        "婚礼宴会": "weddings and banquets",
        "企业年会": "corporate annual meetings",
        "音乐节": "music festivals",
        "户外庆典": "outdoor celebrations",
        "专业音响设备": "professional audio equipment",
        "租赁企业": "rental businesses",
        "设备种类繁多": "diverse equipment types",
        "维护成本高昂": "high maintenance costs",
        "运输调度复杂": "complex transportation scheduling",
        "技术支持专业性强": "strong technical support requirements",
        "传统管理方式": "traditional management methods",
        "数字化转型": "digital transformation",
        "运营效率": "operational efficiency",
        "客户体验": "customer experience",
        "设备损耗": "equipment depreciation",
        "关键工具": "key tools",
        "市场主流": "mainstream market",
        "明智选择": "wise decision",
        "背景介绍": "Background Introduction",
        "核心功能": "Core Features",
        "参数对比": "Parameters Comparison",
        "行业趋势": "Industry Trends",
        "选择建议": "Selection Recommendations",
        "深度解析": "In-depth Analysis",
        "优势分析": "Advantages Analysis",
        "决策关键": "Decision Key Factors",
        "实施建议": "Implementation Recommendations",
        "最佳实践": "Best Practices",
        "2026年": "2026",
        "中小企业": "small and medium businesses",
        "初创企业": "startups",
        "成长型企业": "growing businesses",
        "大型企业": "large enterprises",
    }

    content_en = content_zh

    # 替换标题标签中的文本
    for zh, en in sorted(content_map.items(), key=lambda x: len(x[0]), reverse=True):
        content_en = content_en.replace(zh, en)

    # 处理HTML标题
    content_en = re.sub(r'<h1>([^<]+)</h1>', lambda m: f'<h1>{translate_title(m.group(1))}</h1>', content_en)
    content_en = re.sub(r'<h2>([^<]+)</h2>', lambda m: f'<h2>{m.group(1).replace("背景介绍", "Background").replace("核心功能", "Core Features").replace("行业趋势", "Trends").replace("选择建议", "Recommendations")}</h2>', content_en)

    return content_en

def process_file(file_path, category, file_index):
    """
    处理单个JSON文件
    生成英文版（data/[category]/）和中文版（data/zh/[category]/）
    """
    global processed_files, error_files

    try:
        # 读取原文件
        with open(file_path, 'r', encoding='utf-8') as f:
            data_zh = json.load(f)

        # 检查是否已处理
        if 'language' in data_zh and data_zh['language'] in ['en-US', 'zh-CN']:
            print(f"  [{file_index}] 已处理，跳过: {file_path.name}")
            return False

        slug = data_zh.get('slug', '')
        if not slug:
            # 从文件名生成slug
            slug = file_path.stem

        # ===== 创建英文版本 =====
        data_en = {
            "title": translate_title(data_zh['title']),
            "description": translate_description(data_zh['description']),
            "content": translate_content(data_zh['content']),
            "seo_keywords": translate_keywords(data_zh['seo_keywords']),
            "slug": slug,
            "published_at": data_zh['published_at'],
            "author": data_zh['author'],
            "language": "en-US",
            "canonical_link": f"{SITE_URL}/posts/{slug}",
            "alternate_links": {
                "en-US": f"{SITE_URL}/posts/{slug}",
                "zh-CN": f"{SITE_URL}/posts/zh/{slug}"
            }
        }

        # ===== 创建中文版本 =====
        data_zh_new = {
            "title": data_zh['title'],
            "description": data_zh['description'],
            "content": data_zh['content'],
            "seo_keywords": data_zh['seo_keywords'],
            "slug": slug,
            "published_at": data_zh['published_at'],
            "author": data_zh['author'],
            "language": "zh-CN",
            "canonical_link": f"{SITE_URL}/posts/zh/{slug}",
            "alternate_links": {
                "en-US": f"{SITE_URL}/posts/{slug}",
                "zh-CN": f"{SITE_URL}/posts/zh/{slug}"
            }
        }

        # ===== 写入文件 =====
        # 创建目录
        en_dir = Path(BASE_DIR) / category
        zh_dir = Path(ZH_DIR) / category
        en_dir.mkdir(parents=True, exist_ok=True)
        zh_dir.mkdir(parents=True, exist_ok=True)

        # 英文版文件路径
        en_file = en_dir / f"{slug}.json"

        # 中文版文件路径
        zh_file = zh_dir / f"{slug}.json"

        # 写入英文版
        with open(en_file, 'w', encoding='utf-8') as f:
            json.dump(data_en, f, ensure_ascii=False, indent=2)

        # 写入中文版
        with open(zh_file, 'w', encoding='utf-8') as f:
            json.dump(data_zh_new, f, ensure_ascii=False, indent=2)

        processed_files += 1
        print(f"  [{file_index}] ✓ 完成: {slug}")

        return True

    except Exception as e:
        error_files += 1
        print(f"  [{file_index}] ✗ 错误: {file_path.name} - {e}")
        return False

def process_category(category):
    """
    处理整个类别目录
    """
    global total_files

    category_dir = Path(BASE_DIR) / category

    if not category_dir.exists():
        print(f"目录不存在: {category}")
        return 0

    # 获取所有JSON文件
    json_files = list(category_dir.glob("*.json"))
    total_files += len(json_files)

    print(f"\n{'='*60}")
    print(f"类别: {category}")
    print(f"文件总数: {len(json_files)}")
    print(f"{'='*60}")

    # 处理每个文件
    for i, file_path in enumerate(json_files, 1):
        process_file(file_path, category, i)

        # 每20个文件报告进度
        if i % 20 == 0:
            progress = i / len(json_files) * 100
            print(f"\n进度报告: {i}/{len(json_files)} ({progress:.1f}%)")
            print(f"已处理: {processed_files}, 错误: {error_files}\n")

    print(f"\n类别完成: {category}")
    print(f"处理: {processed_files}, 错误: {error_files}")

def main():
    """
    主函数：处理所有类别
    """
    print(f"\n{'='*60}")
    print(f"SEO双语文件批量转换处理器")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

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

    # 处理每个类别
    for category in categories:
        process_category(category)

    # 最终统计
    print(f"\n{'='*60}")
    print(f"处理完成")
    print(f"总文件数: {total_files}")
    print(f"成功处理: {processed_files}")
    print(f"错误文件: {error_files}")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()