#!/usr/bin/env python3
"""
Translate Chinese content to English for JSON files in energy-utilities-management directory.
This script processes JSON files with Chinese content marked as en-US and translates them to English.
"""

import json
import os
import re
from pathlib import Path

# Directory containing the JSON files
DATA_DIR = "/Users/gejiayu/owner/seo/data/energy-utilities-management"

def detect_chinese(text):
    """Detect if text contains Chinese characters."""
    if not text:
        return False
    chinese_pattern = re.compile(r'[一-鿿]+')
    return chinese_pattern.search(text) is not None

def simple_translate(text):
    """
    Simple translation mapping for common terms.
    This is a basic approach - for production use, integrate with a translation API.
    """
    # Common translations mapping
    translations = {
        "能源": "Energy",
        "管理": "Management",
        "系统": "System",
        "平台": "Platform",
        "工具": "Tool",
        "评测": "Review",
        "选型": "Selection",
        "指南": "Guide",
        "深度": "In-depth",
        "分析": "Analysis",
        "功能": "Function",
        "核心": "Core",
        "价格": "Price",
        "区间": "Range",
        "美元": "US dollars",
        "年费": "Annual fee",
        "专业": "Professional",
        "完善": "Complete",
        "基础": "Basic",
        "支持": "Support",
        "数据": "Data",
        "监测": "Monitoring",
        "监控": "Monitor",
        "控制": "Control",
        "优化": "Optimization",
        "智能": "Intelligent",
        "自动化": "Automation",
        "效率": "Efficiency",
        "成本": "Cost",
        "用户": "User",
        "企业": "Enterprise",
        "场景": "Scenario",
        "趋势": "Trend",
        "实施": "Implementation",
        "建议": "Suggestion",
        "风险": "Risk",
        "提示": "Tip",
        "总结": "Summary",
        "对比": "Comparison",
        "参数": "Parameter",
        "品牌": "Brand",
        "技术": "Technical",
        "特色": "Feature",
        "应用": "Application",
        "集成": "Integration",
        "解决方案": "Solution",
        "数字化转型": "Digital Transformation",
        "可持续发展": "Sustainable Development",
        "碳中和": "Carbon Neutrality",
        "节能减排": "Energy Saving and Emission Reduction",
        "智能电网": "Smart Grid",
        "能源管理": "Energy Management",
        "电力系统": "Power System",
        "商业建筑": "Commercial Building",
        "制造业": "Manufacturing",
        "基础设施": "Infrastructure",
        "数据处理": "Data Processing",
        "云计算": "Cloud Computing",
        "物联网": "Internet of Things",
        "人工智能": "Artificial Intelligence",
        "机器学习": "Machine Learning",
        "预测": "Prediction",
        "诊断": "Diagnosis",
        "报表": "Report",
        "合规": "Compliance",
        "审计": "Audit",
        "运维": "Operation and Maintenance",
        "部署": "Deployment",
        "本地": "Local",
        "云端": "Cloud",
        "混合": "Hybrid",
        "订阅": "Subscription",
        "服务": "Service",
        "API": "API",
        "协议": "Protocol",
        "传感器": "Sensor",
        "设备": "Equipment",
        "实时": "Real-time",
        "历史": "History",
        "查询": "Query",
        "自助": "Self-service",
        "门户": "Portal",
        "账单": "Bill",
        "用量": "Usage",
        "缴费": "Payment",
        "体验": "Experience",
        "界面": "Interface",
        "设计": "Design",
        "可视化": "Visualization",
        "移动": "Mobile",
        "安全": "Security",
        "认证": "Authentication",
    }

    # For now, return the original text - actual translation needs API
    # This is placeholder for manual translation or API integration
    return text

def translate_file(file_path):
    """Translate a single JSON file from Chinese to English."""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if file has Chinese content but marked as en-US
    if data.get('language') == 'en-US':
        has_chinese = False
        for field in ['title', 'description', 'content']:
            if field in data and detect_chinese(data[field]):
                has_chinese = True
                break

        if has_chinese:
            print(f"  Found Chinese content in en-US file")
            # Return file info for manual processing
            return {
                'file': file_path,
                'language': data.get('language'),
                'has_chinese': True,
                'needs_translation': True
            }

    return None

def main():
    """Main function to process all files."""
    data_path = Path(DATA_DIR)

    if not data_path.exists():
        print(f"Directory not found: {DATA_DIR}")
        return

    files_to_translate = []

    # Process all JSON files
    for json_file in data_path.glob("*.json"):
        result = translate_file(json_file)
        if result:
            files_to_translate.append(result)

    # Print summary
    print(f"\n{'='*80}")
    print(f"Summary:")
    print(f"Total files needing translation: {len(files_to_translate)}")
    print(f"{'='*80}\n")

    # List files needing translation
    for item in files_to_translate:
        print(f"  - {item['file']}")

if __name__ == "__main__":
    main()