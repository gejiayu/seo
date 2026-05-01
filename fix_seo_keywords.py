#!/usr/bin/env python3
"""
JSON SEO Keywords Repair Script
修复 seo_keywords 字段格式问题（从字符串转为数组）
同时修复JSON格式错误（控制字符、非法转义等）
"""

import json
import os
import re
from pathlib import Path

def clean_json_content(content):
    """清理JSON内容中的非法字符"""
    # 移除控制字符（除了\n\r\t）
    content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', content)
    # 修复非法转义序列
    content = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', content)
    return content

def fix_seo_keywords(data):
    """将seo_keywords从字符串转换为数组"""
    if 'seo_keywords' in data:
        keywords = data['seo_keywords']

        # 如果是字符串，转换为数组
        if isinstance(keywords, str):
            # 按逗号分割，去除前后空格
            keywords_list = [k.strip() for k in keywords.split(',') if k.strip()]
            data['seo_keywords'] = keywords_list
            return True

        # 如果已经是数组，验证格式
        elif isinstance(keywords, list):
            # 确保所有元素都是字符串
            data['seo_keywords'] = [str(k).strip() for k in keywords if k]
            return False

    return False

def process_json_file(filepath):
    """处理单个JSON文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 清理非法字符
        cleaned_content = clean_json_content(content)

        # 解析JSON
        try:
            data = json.loads(cleaned_content)
        except json.JSONDecodeError as e:
            # 尝试更激进的修复
            # 移除所有反斜杠（临时方案）
            cleaned_content_aggressive = re.sub(r'\\[^"\\/bfnrtu]', '', cleaned_content)
            try:
                data = json.loads(cleaned_content_aggressive)
                print(f"⚠️  激进修复成功: {filepath}")
            except:
                print(f"❌ 无法解析: {filepath} - {e}")
                return None

        # 修复seo_keywords
        fixed = fix_seo_keywords(data)

        # 保存修复后的文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return fixed

    except Exception as e:
        print(f"❌ 处理失败: {filepath} - {e}")
        return None

def main():
    """主函数"""
    data_dir = Path('/Users/gejiayu/owner/seo/data')

    # 统计计数
    stats = {
        'total_files': 0,
        'keywords_fixed': 0,
        'format_fixed': 0,
        'failed': 0
    }

    # 遍历所有JSON文件
    for json_file in data_dir.rglob('*.json'):
        stats['total_files'] += 1
        result = process_json_file(json_file)

        if result is True:
            stats['keywords_fixed'] += 1
        elif result is False:
            stats['format_fixed'] += 1
        elif result is None:
            stats['failed'] += 1

    # 输出统计结果
    print("\n" + "="*60)
    print("📊 修复统计报告")
    print("="*60)
    print(f"✅ 总扫描文件: {stats['total_files']}")
    print(f"✅ seo_keywords修复: {stats['keywords_fixed']} (字符串→数组)")
    print(f"✅ 格式修复: {stats['format_fixed']} (已是正确格式)")
    print(f"❌ 处理失败: {stats['failed']}")
    print("="*60)

    # 展示修复样本
    if stats['keywords_fixed'] > 0:
        print("\n📝 修复样本示例:")
        sample_file = list(data_dir.rglob('*.json'))[0]
        try:
            with open(sample_file, 'r', encoding='utf-8') as f:
                sample_data = json.load(f)
                print(f"\n文件: {sample_file.name}")
                print(f"seo_keywords: {json.dumps(sample_data.get('seo_keywords', []), ensure_ascii=False)}")
        except:
            pass

if __name__ == '__main__':
    main()