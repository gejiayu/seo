#!/usr/bin/env python3
"""
pSEO CTR Enhancement Script v2 - Test Mode (中文智能增强版)
批量优化标题和描述，智能保留中文内容并添加吸引力词汇和CTA
"""

import json
import os
import re
from pathlib import Path

# 中文吸引力词汇库
CN_ATTRACTION_PREFIXES = {
    '评测类': ['最佳', '十大', '精选', '完整指南', '专家评测'],
    '对比类': ['深度对比', '全面评测', '详细分析', '选购指南'],
    '指南类': ['完整攻略', '选择指南', '入门指南', '必看指南']
}

CN_ATTRACTION_SUFFIXES = ['2026年评测', '2026年精选', '最新评测', '年度推荐']

# 中文CTA模板
CN_CTA_TEMPLATES = [
    "了解更多功能和价格对比，找到最适合你的方案！",
    "查看完整评测和专家推荐，做出明智选择！",
    "获取详细对比分析，选择最佳解决方案！",
    "发现最适合中小企业的工具，立即查看！",
    "阅读专业评测，找到你的理想选择！"
]

def has_attraction_words(title):
    """检查标题是否包含吸引力词汇（支持中英文）"""
    cn_words = ['最佳', '十大', '精选', '指南', '评测', '对比', '攻略', '推荐',
                '完整', '全面', '详细', '深度', '专家']
    en_words = ['best', 'top', 'ultimate', 'guide', 'review', 'comparison',
                'expert', 'complete', 'comprehensive', 'how to']
    title_lower = title.lower()
    return any(word in title for word in cn_words) or any(word in title_lower for word in en_words)

def has_2026(title):
    """检查标题是否包含2026"""
    return '2026' in title or '2026年' in title

def has_cta(description):
    """检查描述是否包含明确的CTA（行动号召词）"""
    # 明确的CTA短语（必须在句末或独立出现）
    explicit_cn_cta = ['了解更多', '查看完整', '获取详细', '发现最适合', '阅读专业',
                       '立即查看', '做出明智', '找到最适合你的方案', '选择最佳']
    explicit_en_cta = ['discover the best', 'learn more', 'read our', 'find your perfect',
                       'get expert', 'see the full', 'make your choice', 'choose wisely']

    # 检查是否有明确的CTA短语
    for cta in explicit_cn_cta:
        if cta in description:
            return True
    desc_lower = description.lower()
    for cta in explicit_en_cta:
        if cta in desc_lower:
            return True

    return False

def is_chinese_content(text):
    """判断内容是否主要为中文"""
    chinese_chars = sum(1 for char in text if '一' <= char <= '鿿')
    return chinese_chars > len(text) * 0.3

def enhance_title(title, category):
    """智能优化标题，保留原有内容"""
    enhanced = title

    # 判断是否为中文标题
    is_cn = is_chinese_content(title)

    # 添加吸引力词汇前缀（如果缺失）
    if not has_attraction_words(title):
        if is_cn:
            # 中文标题：根据内容类型选择合适的前缀
            if 'vs' in title.lower() or '对比' in title or '评测' in title:
                prefix = "深度评测："
            elif '工具' in title or '软件' in title or '系统' in title:
                prefix = "最佳"
            else:
                prefix = "精选推荐："
            # 在标题开头插入前缀
            enhanced = f"{prefix}{title}"
        else:
            # 英文标题
            if 'vs' in title.lower():
                prefix = "Expert Comparison:"
            elif 'review' in title.lower():
                prefix = "Best"
            else:
                prefix = "Top 10"
            enhanced = f"{prefix} {title}"

    # 添加2026后缀（如果缺失）
    if not has_2026(title):
        if is_cn:
            # 中文：在标题末尾添加
            enhanced = f"{enhanced}｜2026年评测"
        else:
            enhanced = f"{enhanced} - 2026 Review"

    # 清理重复添加
    enhanced = re.sub(r'｜2026年评测.*｜2026年', '｜2026年评测', enhanced)
    enhanced = re.sub(r'- 2026 Review.*- 2026', '- 2026 Review', enhanced)

    return enhanced

def enhance_description(description, title, category):
    """智能优化描述，保留原有内容并添加CTA"""
    # 如果描述太短（<50字符），重新生成
    if len(description) < 50:
        # 从标题提取关键信息生成新描述
        if is_chinese_content(title):
            new_desc = f"深度分析{category if category else '相关工具'}领域解决方案。{CN_CTA_TEMPLATES[0]}"
        else:
            new_desc = f"Comprehensive analysis of {category if category else 'tools'} solutions. Discover the best options for 2026!"
        return new_desc[:160]

    # 如果描述已有CTA但长度不够，补充CTA
    if not has_cta(description):
        # 在末尾添加中文CTA
        if is_chinese_content(description):
            # 选择合适的CTA
            cta = CN_CTA_TEMPLATES[0]
            enhanced = f"{description.rstrip('。')}。{cta}"
        else:
            cta = " Discover the best options and make your choice today!"
            enhanced = description + cta

        # 确保长度在140-160字符范围
        if len(enhanced) > 160:
            enhanced = enhanced[:157] + "..."
        elif len(enhanced) < 140:
            # 再补充一点
            if is_chinese_content(description):
                enhanced = enhanced + "专业评测助你决策！"
            else:
                enhanced = enhanced + " Get expert insights!"

        return enhanced

    # 如果描述已有CTA但太长，截断
    if len(description) > 160:
        return description[:157] + "..."

    # 如果描述长度合适且有CTA，保持不变
    return description

def process_file(filepath, dry_run=True):
    """处理单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        original_title = data.get('title', '')
        original_desc = data.get('description', '')
        category = data.get('category', '')

        # 优化标题
        enhanced_title = enhance_title(original_title, category)

        # 优化描述
        enhanced_desc = enhance_description(original_desc, original_title, category)

        changes = {
            'file': filepath,
            'title': {
                'original': original_title,
                'enhanced': enhanced_title,
                'changed': original_title != enhanced_title
            },
            'description': {
                'original': original_desc,
                'original_len': len(original_desc),
                'enhanced': enhanced_desc,
                'enhanced_len': len(enhanced_desc),
                'changed': original_desc != enhanced_desc
            }
        }

        if not dry_run:
            data['title'] = enhanced_title
            data['description'] = enhanced_desc
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        return changes

    except Exception as e:
        return {'file': filepath, 'error': str(e)}

def main():
    # 测试模式：只处理指定的测试文件
    test_files = [
        "data/architecture-design-tools/architecture-virtual-reality-software-review.json",
        "data/healthcare-wellness-tools/mental-health-note-taking-tools-review-2026.json",
        "data/transportation-fleet-tools/fleet-security-anti-theft-systems.json",
        "data/legal-document-management-tools/legal-cloud-vs-doccloud-pro-2026.json",
        "data/insurance-claims-processing-tools/claims-ai-platform-2026.json"
    ]

    print("=" * 80)
    print("CTR Enhancement Test v2 - 中文智能增强版 Preview")
    print("=" * 80)
    print()

    for filepath in test_files:
        if not os.path.exists(filepath):
            print(f"⚠ File not found: {filepath}")
            continue

        result = process_file(filepath, dry_run=True)

        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            continue

        print(f"📄 {filepath}")
        print()

        # 标题变更
        if result['title']['changed']:
            print("  📝 TITLE ENHANCEMENT:")
            print(f"    Before: {result['title']['original']}")
            print(f"    After:  {result['title']['enhanced']}")
            title_diff = len(result['title']['enhanced']) - len(result['title']['original'])
            print(f"    Change: +{title_diff} chars")
        else:
            print(f"  ✓ TITLE already optimized: {result['title']['original']}")
        print()

        # 描述变更
        if result['description']['changed']:
            print("  📝 DESCRIPTION ENHANCEMENT:")
            print(f"    Before ({result['description']['original_len']} chars):")
            print(f"      {result['description']['original']}")
            print(f"    After ({result['description']['enhanced_len']} chars):")
            print(f"      {result['description']['enhanced']}")
            desc_diff = result['description']['enhanced_len'] - result['description']['original_len']
            print(f"    Change: +{desc_diff} chars, CTA added")
        else:
            print(f"  ✓ DESCRIPTION already optimized ({result['description']['original_len']} chars)")
        print()
        print("-" * 80)
        print()

if __name__ == "__main__":
    main()