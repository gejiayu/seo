#!/usr/bin/env python3
"""
pSEO CTR Enhancement Script - Full Execution
批量优化8000+ JSON文件的标题和描述
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime

# 中文吸引力词汇库
CN_ATTRACTION_PREFIXES = {
    '评测类': ['最佳', '十大', '精选', '完整指南', '专家评测'],
    '对比类': ['深度对比', '全面评测', '详细分析', '选购指南'],
    '指南类': ['完整攻略', '选择指南', '入门指南', '必看指南']
}

CN_ATTRACTION_SUFFIXES = ['｜2026年评测', '｜2026年精选', '｜最新评测']

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
    explicit_cn_cta = ['了解更多', '查看完整', '获取详细', '发现最适合', '阅读专业',
                       '立即查看', '做出明智', '找到最适合你的方案', '选择最佳']
    explicit_en_cta = ['discover the best', 'learn more', 'read our', 'find your perfect',
                       'get expert', 'see the full', 'make your choice', 'choose wisely']

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
    is_cn = is_chinese_content(title)

    # 添加吸引力词汇前缀（如果缺失）
    if not has_attraction_words(title):
        if is_cn:
            if 'vs' in title.lower() or '对比' in title or '评测' in title:
                prefix = "深度评测："
            elif '工具' in title or '软件' in title or '系统' in title:
                prefix = "最佳"
            else:
                prefix = "精选推荐："
            enhanced = f"{prefix}{title}"
        else:
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
        if is_chinese_content(title):
            new_desc = f"深度分析{category if category else '相关工具'}领域解决方案。{CN_CTA_TEMPLATES[0]}"
        else:
            new_desc = f"Comprehensive analysis of {category if category else 'tools'} solutions. Discover the best options for 2026!"
        return new_desc[:160]

    # 如果描述没有CTA，添加CTA
    if not has_cta(description):
        if is_chinese_content(description):
            cta = CN_CTA_TEMPLATES[0]
            enhanced = f"{description.rstrip('。')}。{cta}"
        else:
            cta = " Discover the best options and make your choice today!"
            enhanced = description + cta

        # 确保长度在140-160字符范围
        if len(enhanced) > 160:
            enhanced = enhanced[:157] + "..."
        elif len(enhanced) < 140:
            if is_chinese_content(description):
                enhanced = enhanced + "专业评测助你决策！"
            else:
                enhanced = enhanced + " Get expert insights!"

        return enhanced

    # 如果描述已有CTA但太长，截断
    if len(description) > 160:
        return description[:157] + "..."

    return description

def process_file(filepath):
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

        # 只有实际变化才写入
        if enhanced_title != original_title or enhanced_desc != original_desc:
            data['title'] = enhanced_title
            data['description'] = enhanced_desc

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True

        return False

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    # 统计
    total_files = 0
    modified_files = 0
    errors = 0

    # 扫描data目录下的所有JSON文件
    data_dir = Path('data')

    print("=" * 80)
    print("pSEO CTR Enhancement - Full Execution")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    for json_file in data_dir.rglob('*.json'):
        total_files += 1

        if process_file(json_file):
            modified_files += 1

        # 每100个文件打印进度
        if total_files % 100 == 0:
            print(f"Processed: {total_files} files, Modified: {modified_files}")

    print()
    print("=" * 80)
    print("Execution Complete")
    print(f"Total files: {total_files}")
    print(f"Modified files: {modified_files}")
    print(f"Errors: {errors}")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    main()