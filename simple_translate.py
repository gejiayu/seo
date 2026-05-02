#!/usr/bin/env python3
import json
from pathlib import Path

# Simple but comprehensive translation mapping
TRANSLATE_MAP = {
    # Common words
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
    "色彩": "Color",
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
    # Common phrases
    "在": "in",
    "为": "for",
    "与": "and",
    "的": "",
    "和": "and",
    "是": "is",
    "有": "has",
    "或": "or",
    "及": "and",
    "可": "can",
    "从": "from",
    "到": "to",
    "年": "Year",
    "月": "Month",
    "日": "Day",
    "中": "in",
    "于": "in",
    "需": "need",
    "将": "will",
    "已": "already",
    "被": "be",
    "使": "use",
    "能": "can",
    "并": "and",
    "全": "full",
    "最": "most",
    "新": "new",
    "好": "good",
    "高": "high",
    "低": "low",
    "快": "fast",
    "慢": "slow",
    "大": "big",
    "小": "small",
    "多": "many",
    "少": "few",
    "强": "strong",
    "弱": "weak",
    "主": "main",
    "次": "sub",
    "实": "real",
    "内": "inner",
    "外": "outer",
    "上": "up",
    "下": "down",
    "前": "front",
    "后": "back",
    "深": "deep",
    "浅": "shallow",
    "宽": "wide",
    "窄": "narrow",
    "厚": "thick",
    "薄": "thin",
    "长": "long",
    "短": "short",
    "重": "heavy",
    "轻": "light",
}

def translate_text(text):
    """Apply translation mapping"""
    result = text
    for cn, en in TRANSLATE_MAP.items():
        result = result.replace(cn, en)
    return result

def process_file(filepath):
    """Process a single JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Translate all fields
    if 'title' in data:
        data['title'] = translate_text(data['title'])
    
    if 'description' in data:
        data['description'] = translate_text(data['description'])
    
    if 'content' in data:
        data['content'] = translate_text(data['content'])
    
    if 'seo_keywords' in data and isinstance(data['seo_keywords'], list):
        data['seo_keywords'] = [translate_text(k) for k in data['seo_keywords']]
    
    if 'author' in data:
        data['author'] = translate_text(data['author'])
    
    # Save back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return True

# Process all 100 files
directory = Path("/Users/gejiayu/owner/seo/data/print-graphic-design-tools")
files = sorted(directory.glob("*.json"))

count = 0
for filepath in files:
    if process_file(filepath):
        count += 1
        print(f"{count}. {filepath.name}")

print(f"\nCompleted: {count} files translated")
