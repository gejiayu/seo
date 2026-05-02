#!/usr/bin/env python3
"""
Translate Chinese JSON content to English for blue-collar-tools files.
Maintains HTML structure and technical accuracy.
"""
import json
import os
from pathlib import Path

# Translation mapping for common Chinese terms in blue-collar context
TRANSLATIONS = {
    "背景介绍": "Background Introduction",
    "核心功能对比": "Core Features Comparison",
    "功能模块": "Feature Module",
    "对比分析": "Comparison Analysis",
    "深度评测": "In-depth Review",
    "价格与适用场景对比": "Pricing and Use Case Comparison",
    "中小企业选择建议": "Small Business Selection Recommendations",
    "发展趋势预测": "Development Trend Forecast",
    "技师管理": "Technician Management",
    "客户管理": "Customer Management",
    "现场服务": "Field Service",
    "开票计费": "Invoicing Billing",
    "路线优化": "Route Optimization",
    "数据分析": "Data Analysis",
    "定期服务": "Recurring Service",
    "报价估算": "Quote Estimation",
    "调度派工": "Scheduling Dispatch",
    "移动端应用": "Mobile Application",
    "中小企业": "Small Business",
    "月费": "Monthly Fee",
    "美元": "USD",
    "年营收": "Annual Revenue",
    "适合": "Suitable for",
    "核心优势": "Core Advantage",
    "优势": "Advantage",
    "劣势": "Disadvantage",
    "优点": "Pros",
    "缺点": "Cons",
    "评分": "Rating",
    "定位": "Positioning",
    "免费额度": "Free Tier",
    "付费版": "Paid Version",
    "核心功能": "Core Features",
    "适用场景": "Use Cases",
    "强烈推荐": "Highly Recommended",
    "建议": "Recommendation",
}

def translate_content_field(content_html):
    """
    Translate content HTML maintaining structure.
    This is a placeholder - actual implementation would use translation API.
    """
    # For now, return placeholder - actual translation needs proper implementation
    return content_html

def needs_translation(text):
    """Check if text contains Chinese characters."""
    if not isinstance(text, str):
        return False
    for char in text:
        if '一' <= char <= '鿿':
            return True
    return False

def get_chinese_files(directory):
    """Get all files with Chinese content in title field."""
    chinese_files = []
    for json_file in Path(directory).glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if needs_translation(data.get('title', '')):
                    chinese_files.append(json_file)
        except Exception as e:
            print(f"Error reading {json_file}: {e}")
    return chinese_files

if __name__ == '__main__':
    directory = Path('/Users/gejiayu/owner/seo/data/blue-collar-tools')
    files = get_chinese_files(directory)
    print(f"Found {len(files)} files with Chinese content")
    
    # Print first 10 for verification
    for i, file in enumerate(files[:10]):
        print(f"{i+1}. {file.name}")
