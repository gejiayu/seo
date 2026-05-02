#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path

# Translation dictionary for common terms
TRANSLATIONS = {
    "评测": "Review",
    "对比": "Comparison",
    "软件": "Software",
    "系统": "System",
    "工具": "Tools",
    "平台": "Platform",
    "管理": "Management",
    "解决方案": "Solution",
    "专业": "Professional",
    "最佳": "Best",
    "推荐": "Recommended",
    "分析": "Analysis",
    "功能": "Features",
    "价格": "Price",
    "优势": "Advantages",
    "劣势": "Disadvantages",
    "用户": "User",
    "企业": "Enterprise",
    "中小企业": "Small Business",
    "小型": "Small",
    "大型": "Large",
    "选择": "Selection",
    "建议": "Recommendations",
    "核心": "Core",
    "关键": "Key",
    "重要": "Important",
    "行业": "Industry",
    "市场": "Market",
    "趋势": "Trends",
    "预测": "Prediction",
    "未来": "Future",
    "发展": "Development",
    "应用": "Application",
    "场景": "Scenarios",
    "价值": "Value",
    "成本": "Cost",
    "效率": "Efficiency",
    "质量": "Quality",
    "安全": "Security",
    "服务": "Service",
    "支持": "Support",
    "集成": "Integration",
    "自动化": "Automation",
    "智能化": "Intelligent",
    "数字化": "Digital",
    "云端": "Cloud",
    "移动端": "Mobile",
    "团队": "Team",
    "协作": "Collaboration",
    "客户": "Customer",
    "供应商": "Supplier",
    "产品": "Product",
    "订单": "Order",
    "库存": "Inventory",
    "财务": "Financial",
    "人力资源": "Human Resources",
    "营销": "Marketing",
    "销售": "Sales",
    "运营": "Operations",
    "流程": "Process",
    "数据": "Data",
    "报表": "Reports",
    "监控": "Monitoring",
    "校准": "Calibration",
    "颜色": "Color",
    "印刷": "Print",
    "设计": "Design",
    "包装": "Packaging",
    "排版": "Typesetting",
    "印前": "Prepress",
    "印后": "Postpress",
    "设备": "Equipment",
    "生产": "Production",
    "调度": "Scheduling",
    "报价": "Quoting",
    "质量检测": "Quality Inspection",
    "物流": "Logistics",
    "供应链": "Supply Chain",
    "环境": "Environmental",
    "合规": "Compliance",
    "认证": "Certification",
    "标准": "Standard",
    "培训": "Training",
    "创新": "Innovation",
    "战略": "Strategy",
    "规划": "Planning",
    "门户": "Portal",
    "网站": "Website",
    "移动应用": "Mobile App",
    "自助服务": "Self-Service",
    "电子商务": "E-commerce",
    "交付": "Delivery",
    "员工": "Employee",
    "绩效": "Performance",
    "办公自动化": "Office Automation",
    "知识管理": "Knowledge Management",
    "品牌": "Brand",
    "营销自动化": "Marketing Automation",
    "智能制造": "Smart Manufacturing",
    "能源管理": "Energy Management",
    "安全管理": "Safety Management",
    "样品": "Sample",
    "模板": "Template",
    "数字化资产": "Digital Asset",
    "变量数据": "Variable Data",
    "网络印刷": "Web to Print",
}

def clean_chinese_english_mix(text):
    """Clean mixed Chinese-English text and translate to proper English"""
    if not text:
        return text
    
    # Remove weird Chinese character insertions in English words
    # Pattern: English word followed by Chinese character insertions
    text = re.sub(r'([A-Za-z]+)([^\x00-\x7F]+)', lambda m: m.group(1), text)
    
    # Translate Chinese terms to English
    for chinese, english in TRANSLATIONS.items():
        text = text.replace(chinese, english)
    
    # Clean up leftover Chinese characters
    text = re.sub(r'[^\x00-\x7F\s\.,;:!?\'\"()\[\]{}<>@#$%^&*\-_=+|\\`~]', '', text)
    
    # Fix spacing issues
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s([.,;:!?])', r'\1', text)
    
    # Fix HTML tag issues
    text = re.sub(r'<\s+', '<', text)
    text = re.sub(r'\s+>', '>', text)
    text = re.sub(r'<\s*/\s+', '</', text)
    
    return text.strip()

def translate_json_file(filepath):
    """Translate a single JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Translate title
        if 'title' in data:
            data['title'] = clean_chinese_english_mix(data['title'])
        
        # Translate description
        if 'description' in data:
            data['description'] = clean_chinese_english_mix(data['description'])
        
        # Translate content (maintain HTML structure)
        if 'content' in data:
            data['content'] = clean_chinese_english_mix(data['content'])
        
        # Translate seo_keywords (array format)
        if 'seo_keywords' in data and isinstance(data['seo_keywords'], list):
            data['seo_keywords'] = [clean_chinese_english_mix(k) for k in data['seo_keywords']]
        
        # Translate author
        if 'author' in data:
            data['author'] = clean_chinese_english_mix(data['author'])
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

# Process all files
directory = "/Users/gejiayu/owner/seo/data/print-graphic-design-tools"
files = sorted(Path(directory).glob("*.json"))

success_count = 0
fail_count = 0

for filepath in files:
    if translate_json_file(filepath):
        success_count += 1
        print(f"✓ {filepath.name}")
    else:
        fail_count += 1
        print(f"✗ {filepath.name}")

print(f"\nCompleted: {success_count} success, {fail_count} failed")
