#!/usr/bin/env python3
"""
修复seo_keywords - 替换为纯中文关键词
"""

import json
from pathlib import Path

# 关键词映射（英文到中文）
KEYWORD_MAP = {
    'shipping': '航运',
    'management': '管理',
    'software': '软件',
    'systems': '系统',
    'platforms': '平台',
    'vessel': '船舶',
    'fleet': '船队',
    'tracking': '跟踪',
    'monitoring': '监控',
    'crew': '船员',
    'cargo': '货物',
    'port': '港口',
    'terminal': '码头',
    'operations': '运营',
    'safety': '安全',
    'compliance': '合规',
    'navigation': '导航',
    'scheduling': '调度',
    'insurance': '保险',
    'risk': '风险',
    'tanker': '油轮',
    'container': '集装箱',
    'bulk': '散货',
    'environmental': '环保',
    'emissions': '排放',
    'performance': '性能',
    'maintenance': '维护',
    'inspection': '检查',
    'vetting': '审查',
    'survey': '检验',
    'communication': '通信',
    'cybersecurity': '网络安全',
    'training': '培训',
    'weather': '天气',
    'route': '航线',
    'logistics': '物流',
    'procurement': '采购',
    'finance': '财务',
    'emergency': '应急',
    'digital': '数字',
    'solutions': '解决方案',
    'marine': '海事',
}

def fix_keywords():
    """修复所有文件的seo_keywords"""
    zh_dir = Path('/Users/gejiayu/owner/seo/data/zh/maritime-shipping-tools')

    for f in zh_dir.glob('*.json'):
        try:
            with open(f) as fp:
                data = json.load(fp)

            keywords = data.get('seo_keywords', [])
            if not isinstance(keywords, list):
                keywords = []

            # 修复关键词
            zh_keywords = []
            for kw in keywords:
                zh_kw = kw
                for en, zh in KEYWORD_MAP.items():
                    if en.lower() in kw.lower():
                        # 替换英文为中文
                        zh_kw = kw.replace(en, zh).replace(en.capitalize(), zh)
                        zh_kw = zh_kw.replace(en.lower(), zh)
                        break

                # 如果关键词还是混合，提取中文部分或生成纯中文
                if any(c.isalpha() and ord(c) < 128 for c in zh_kw):
                    # 还有英文字母
                    # 生成纯中文关键词
                    zh_kw = generate_pure_zh_keyword(zh_kw)

                zh_keywords.append(zh_kw.strip())

            # 确保关键词数量合适（5-8个）
            zh_keywords = zh_keywords[:8] if len(zh_keywords) > 8 else zh_keywords

            # 更新数据
            data['seo_keywords'] = zh_keywords

            # 保存
            with open(f, 'w') as fp:
                json.dump(data, fp, ensure_ascii=False, indent=2)

            print(f'✓ 修复: {f.name}')

        except Exception as e:
            print(f'✗ 错误: {f.name} - {e}')

def generate_pure_zh_keyword(mixed_kw):
    """生成纯中文关键词"""
    # 提取关键词中的中文部分
    chinese_parts = []
    for char in mixed_kw:
        if ord(char) > 127:  # 中文字符
            chinese_parts.append(char)

    if chinese_parts:
        return ''.join(chinese_parts)

    # 如果没有中文，根据英文生成中文
    for en, zh in KEYWORD_MAP.items():
        if en.lower() in mixed_kw.lower():
            return zh + '系统'

    return '海事管理系统'

if __name__ == '__main__':
    fix_keywords()