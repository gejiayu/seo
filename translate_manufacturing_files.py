#!/usr/bin/env python3
"""
Translation script for manufacturing-production-tools JSON files.
Translates all Chinese content to proper English.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any

# Common Chinese-English translation mappings for manufacturing context
TRANSLATIONS = {
    # Industry terms
    "汽车": "Automotive",
    "电子": "Electronics",
    "制药": "Pharmaceutical",
    "食品": "Food",
    "饮料": "Beverage",
    "Manufacturing": "Manufacturing",
    "生产": "Production",
    "工厂": "Factory",
    "制造业": "Manufacturing Industry",
    "企业": "Enterprise",
    "行业": "Industry",

    # System/Software terms
    "System": "System",
    "软件": "Software",
    "平台": "Platform",
    "工具": "Tool",
    "方案": "Solution",
    "Solutionsolution": "Solution",
    "模块": "Module",
    "应用": "Application",
    "should用": "Application",

    # Management terms
    "Management": "Management",
    "管理": "Management",
    "控制": "Control",
    "监控": "Monitoring",
    "追溯": "Traceability",
    "跟踪": "Tracking",
    "计划": "Planning",
    "调度": "Scheduling",
    "优化": "Optimization",
    "optimize": "optimize",
    "分析": "Analysis",
    "评估": "Evaluation",
    "审计": "Audit",
    "检验": "Inspection",
    "检测": "Detection",
    "测试": "Testing",
    "维护": "Maintenance",
    "Maintenance": "Maintenance",
    "校准": "Calibration",

    # Quality terms
    "质量": "Quality",
    "Quality": "Quality",
    "缺陷": "Defect",
    "故障": "Fault",
    "错误": "Error",
    "问题": "Issue",
    "合格": "Qualified",
    "不合格": "Unqualified",
    "合规": "Compliance",
    "Compliance": "Compliance",

    # Production terms
    "装配": "Assembly",
    "生产线": "Production Line",
    "装配线": "Assembly Line",
    "工序": "Process",
    "流程": "Workflow",
    "工单": "Work Order",
    "Work Order": "Work Order",
    "订单": "Order",
    "批次": "Batch",
    "批次": "Batch",
    "批量": "Volume",
    "节拍": "Takt Time",

    # Equipment terms
    "设备": "Equipment",
    "机器": "Machine",
    "机器人": "Robot",
    "机械": "Mechanical",
    "自动化": "Automation",
    "Automated": "Automated",
    "智能": "Intelligent",
    "Intelligent": "Intelligent",
    "传感器": "Sensor",
    "仪表": "Instrument",
    "仪器": "Instrument",

    # Data terms
    "数据": "Data",
    "信息": "Information",
    "记录": "Record",
    "Recording": "Recording",
    "报告": "Report",
    "报表": "Report",
    "报告": "Report",
    "文档": "Document",
    "图表": "Chart",
    "指标": "Metric",
    "KPI": "KPI",

    # Resource terms
    "物料": "Material",
    "材料": "Material",
    "零部件": "Component",
    "零件": "Part",
    "元器件": "Component",
    "备件": "Spare Part",
    "库存": "Inventory",
    "Inventory": "Inventory",
    "资源": "Resource",
    "资产": "Asset",
    "成本": "Cost",
    "Cost": "Cost",
    "预算": "Budget",
    "费用": "Expense",

    # People terms
    "人员": "Personnel",
    "员工": "Employee",
    "工人": "Worker",
    "工程师": "Engineer",
    "专家": "Expert",
    "技师": "Technician",
    "主管": "Supervisor",
    "经理": "Manager",
    "团队": "Team",

    # Action verbs
    "提供": "Provide",
    "支持": "Support",
    "实现": "Implement",
    "部署": "Deploy",
    "deploying": "deploying",
    "集成": "Integration",
    "连接": "Connect",
    "采集": "Collect",
    "生成": "Generate",
    "Automatic Generation": "Automatic Generation",
    "计算": "Calculate",
    "预测": "Predict",
    "预警": "Alert",
    "Warning": "Warning",
    "通知": "Notify",
    "响应": "Response",
    "响should": "Response",
    "恢复": "Recovery",
    "改进": "Improve",
    "improve": "improve",
    "提高": "Increase",
    "提升": "Enhance",
    "减少": "Reduce",
    "reduce": "reduce",
    "降低": "Lower",
    "消除": "Eliminate",
    "缩短": "Shorten",
    "shorten": "shorten",
    "延长": "Extend",
    "节约": "Save",
    "优化": "Optimize",
    "automate": "automate",
    "Automatic": "Automatic",
    "自动化": "Automated",

    # Status/Condition terms
    "完整": "Complete",
    "Complete": "Complete",
    "全面": "Comprehensive",
    "专业": "Professional",
    "领先": "Leading",
    "Most Powerful": "Most Powerful",
    "Powerful": "Powerful",
    "Functionality": "Functionality",
    "foundation of": "Basic",
    "基础": "Basic",
    "foundation of": "Foundation",
    "核心": "Core",
    "关键": "Key",
    "key to": "Key",
    "主要": "Main",
    "重要": "Important",
    "显著": "Significant",
    "显著": "Significant",
    "有效": "Effective",
    "高效": "Efficient",
    "High效": "Efficient",
    "实时": "Real-time",
    "Real-time": "Real-time",
    "在线": "Online",
    "in线": "Inline",
    "移动": "Mobile",
    "Mobile": "Mobile",
    "远程": "Remote",
    "数字": "Digital",
    "虚拟": "Virtual",

    # Scale/Size terms
    "大型": "Large-scale",
    "Large": "Large",
    "中型": "Medium-sized",
    "Medium": "Medium",
    "MediumLarge": "Medium to Large",
    "中小型": "Small to Medium",
    "Small and Medium": "Small to Medium",
    "小型": "Small-scale",
    "规模": "Scale",
    "范围": "Scope",

    # Comparison terms
    "对比": "Comparison",
    "for比": "Comparison",
    "比较": "Compare",
    "差异": "Difference",
    "Variance": "Variance",
    "相似": "Similar",
    "相同": "Same",
    "优于": "Superior",
    "领先": "Leading",
    "最佳": "Best",
    "最适合": "Most Suitable",
    "Suitable for": "Suitable for",
    "推荐": "Recommended",
    "recommend": "recommend",
    "选择": "Select",
    "选型": "Selection",

    # Value/Benefit terms
    "价值": "Value",
    "优势": "Advantage",
    "core advantage": "Core Advantage",
    "益处": "Benefit",
    "收益": "Return",
    "ROI": "ROI",
    "效果": "Effect",
    "成效": "Result",
    "效率": "Efficiency",
    "Efficiency": "Efficiency",
    "性能": "Performance",
    "生产力": "Productivity",
    "利用率": "Utilization Rate",
    "Utilization Rate": "Utilization Rate",
    "可靠性": "Reliability",
    "稳定性": "Stability",
    "准确性": "Accuracy",
    "准确性": "Accuracy",
    "精确": "Precision",
    "合规性": "Compliance",
    "安全性": "Safety",
    "保障": "Guarantee",
    "保障": "Guarantee",

    # Time terms
    "周期": "Cycle",
    "时间": "Time",
    "实时": "Real-time",
    "延迟": "Delay",
    "delayed": "Delayed",
    "快速": "Fast",
    "迅速": "Rapid",
    "立即": "Immediate",
    "提前": "Advance",
    "定期": "Regular",
    "持续": "Continuous",
    "长期": "Long-term",
    "短期": "Short-term",

    # Financial terms
    "费用": "Fee",
    "定价": "Pricing",
    "价格": "Price",
    "收费": "Charge",
    "License Fee": "License Fee",
    "Annual License Fee": "Annual License Fee",
    "成本效益": "Cost-effectiveness",
    "Cost-effectiveness": "Cost-effectiveness",
    "预算": "Budget",
    "投资": "Investment",
    "回报": "Return",
    "收益": "Revenue",
    "Annual Revenue": "Annual Revenue",
    "营收": "Revenue",
    "盈利": "Profit",
    "节省": "Saving",

    # Feature descriptors
    "最Complete": "Most Complete",
    "最Complete": "Most Comprehensive",
    "Most Powerful": "Most Powerful",
    "最专业": "Most Professional",
    "最领先": "Most Advanced",
    "最适合": "Best Fit",
    "最完整": "Most Complete",
    "最全面": "Most Comprehensive",
    "最高": "Highest",
    "Highest": "Highest",
    "最低": "Lowest",
    "最Low": "Lowest",
    "最快": "Fastest",
    "最准确": "Most Accurate",
    "最可靠": "Most Reliable",
    "最智能": "Most Intelligent",

    # Integration terms
    "集成": "Integration",
    "Integration": "Integration",
    "协同": "Coordination",
    "连接": "Connection",
    "接口": "Interface",
    "兼容": "Compatible",
    "兼容性": "Compatibility",
    "生态": "Ecosystem",
    "Ecosystem": "Ecosystem",
    "无缝": "Seamless",
    "Seamlessly Integrated": "Seamlessly Integrated",
    "原生": "Native",
    "深度": "Deep",
    "友好": "Friendly",

    # Risk/Issue terms
    "风险": "Risk",
    "Risk": "Risk",
    "挑战": "Challenge",
    "困难": "Difficulty",
    "障碍": "Obstacle",
    "限制": "Limitation",
    "约束": "Constraint",
    "瓶颈": "Bottleneck",
    "停机": "Downtime",
    "停线": "Line Stop",
    "故障": "Failure",
    "失效": "Failure",
    "损失": "Loss",
    "浪费": "Waste",

    # Technology terms
    "AI": "AI",
    "AI-based": "AI-based",
    "IoT": "IoT",
    "IoT集成": "IoT Integration",
    "5G": "5G",
    "AR": "AR",
    "VR": "VR",
    "数字孪生": "Digital Twin",
    "区块链": "Blockchain",
    "云计算": "Cloud Computing",
    "Cloud": "Cloud",
    "边缘计算": "Edge Computing",
    "大数据": "Big Data",
    "机器学习": "Machine Learning",
    "深度学习": "Deep Learning",
    "视觉检测": "Visual Inspection",
    "图像识别": "Image Recognition",

    # Specific system names (keep as is but fix context)
    "西门子": "Siemens",
    "Siemens": "Siemens",
    "SAP": "SAP",
    "Rockwell": "Rockwell",
    "Allen-Bradley": "Allen-Bradley",
    "PLC": "PLC",
    "OPC": "OPC",
    "OPC-UA": "OPC-UA",
    "MES": "MES",
    "MES": "MES",
    "ERP": "ERP",
    "PLM": "PLM",
    "EAM": "EAM",
    "CRM": "CRM",
    "SCADA": "SCADA",
    "HMI": "HMI",
    "WMS": "WMS",
    "TMS": "TMS",
    "QMS": "QMS",
    "LIMS": "LIMS",
    "BOM": "BOM",
    "EBOM": "EBOM",
    "MBOM": "MBOM",
    "SMT": "SMT",
    "PCB": "PCB",
    "AOI": "AOI",
    "ICT": "ICT",
    "FCT": "FCT",
    "OEE": "OEE",
    "VIN": "VIN",
    "IATF16949": "IATF 16949",
    "ISO": "ISO",
    "FDA": "FDA",
    "GMP": "GMP",

    # Additional common terms
    "帮助": "Help",
    "helping": "helping",
    "指导": "Guide",
    "决策": "Decision",
    "decisions": "decisions",
    "需求": "Requirement",
    "Requirements": "Requirements",
    "要求": "Requirement",
    "标准": "Standard",
    "规范": "Specification",
    "流程": "Process",
    "方法": "Method",
    "策略": "Strategy",
    "模式": "Mode",
    "功能": "Function",
    "Functionality": "Functionality",
    "特性": "Feature",
    "能力": "Capability",
    "场景": "Scenario",
    "环境": "Environment",
    "条件": "Condition",
    "参数": "Parameter",
    "配置": "Configuration",
    "设置": "Setting",
    "选项": "Option",
    "版本": "Version",
    "更新": "Update",
    "升级": "Upgrade",
    "变更": "Change",
    "审批": "Approval",
    "历史": "History",
    "日志": "Log",
    "统计": "Statistics",
    "洞察": "Insight",
    "趋势": "Trend",
    "预测": "Prediction",
    "展望": "Outlook",
    "未来": "Future",
    "发展": "Development",
    "创新": "Innovation",
    "转型": "Transformation",
    "现代化": "Modernization",

    # Grammar corrections
    "你": "Your",
    "我们": "We",
    "他们": "They",
    "它": "It",
    "这": "This",
    "那": "That",
    "哪些": "Which",
    "如何": "How",
    "为什么": "Why",
    "什么": "What",
    "何时": "When",
    "哪里": "Where",
    "是否": "Whether",
    "可以": "Can",
    "can": "Can",
    "能够": "Able",
    "需要": "Need",
    "requires": "requires",
    "应": "Should",
    "should": "should",
    "将": "Will",
    "will": "will",
    "已": "Already",
    "already": "already",
    "正在": "Currently",
    "currently": "currently",
    "从": "From",
    "from": "from",
    "到": "To",
    "to": "to",
    "与": "With",
    "with": "with",
    "和": "And",
    "and": "and",
    "或": "Or",
    "or": "or",
    "但": "But",
    "但是": "However",
    "因为": "Because",
    "所以": "Therefore",
    "如果": "If",
    "if": "if",
    "虽然": "Although",
    "然而": "However",
    "此外": "Additionally",
    "以及": "And",
    "包括": "Including",
    "例如": "For example",
    "比如": "Such as",
    "如": "Like",
    "即": "Namely",
    "其中": "Among",
    "关于": "About",
    "对于": "For",
    "根据": "Based on",
    "基于": "Based on",
    "通过": "Through",
    "使用": "Using",
    "利用": "Utilizing",
    "采用": "Adopting",
    "考虑": "Considering",
    "综合": "Comprehensive",
    "全面": "Comprehensive",
    "深入": "In-depth",
    "In-Depth": "In-depth",
    "详细": "Detailed",
    "简要": "Brief",
    "简单": "Simple",
    "复杂": "Complex",
    "complexity": "complexity",
}

def translate_text(text: str) -> str:
    """
    Translate Chinese characters in text to English.
    Uses both direct mapping and pattern matching.
    """
    if not text or not isinstance(text, str):
        return text

    result = text

    # Apply direct translations (sorted by length for better matching)
    for chinese, english in sorted(TRANSLATIONS.items(), key=lambda x: -len(x[0])):
        # Use regex to handle partial matches better
        result = result.replace(chinese, english)

    # Fix common mixed patterns
    patterns = [
        # Fix broken English-Chinese mixed phrases
        (r'(\w+)管理(\w+)', r'\1 Management \2'),
        (r'(\w+)控制(\w+)', r'\1 Control \2'),
        (r'(\w+)监控(\w+)', r'\1 Monitoring \2'),
        (r'(\w+)系统(\w+)', r'\1 System \2'),
        (r'(\w+)软件(\w+)', r'\1 Software \2'),
        (r'(\w+)平台(\w+)', r'\1 Platform \2'),
        (r'(\w+)方案(\w+)', r'\1 Solution \2'),
        (r'(\w+)工具(\w+)', r'\1 Tool \2'),

        # Fix mixed words
        (r'(\w+)最(\w+)', r'\1 Most \2'),
        (r'(\w+)领先(\w+)', r'\1 Leading \2'),
        (r'(\w+)完整(\w+)', r'\1 Complete \2'),
        (r'(\w+)全面(\w+)', r'\1 Comprehensive \2'),

        # Fix grammar issues
        (r'\s+', ' '),  # Normalize spaces
        (r'(\w)\s+(\w)', r'\1 \2'),  # Ensure single space between words
    ]

    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result)

    # Clean up
    result = result.strip()
    result = re.sub(r'\s+', ' ', result)  # Normalize multiple spaces

    return result

def translate_author(author: str) -> str:
    """Translate author name from Chinese to English format."""
    if not author:
        return author

    # Extract Chinese name and translate title
    parts = author.split(' - ')
    if len(parts) == 2:
        name = parts[0]
        title = translate_text(parts[1])

        # Translate common Chinese names
        name_translations = {
            "王军": "Wang Jun",
            "李志明": "Li Zhiming",
            "李明华": "Li Minghua",
            "刘伟": "Liu Wei",
            "王志华": "Wang Zhiming",
            "张伟": "Zhang Wei",
            "陈明": "Chen Ming",
            "赵强": "Zhao Qiang",
        }

        english_name = name_translations.get(name, translate_text(name))
        return f"{english_name} - {title}"

    return translate_text(author)

def translate_json_file(filepath: Path) -> Dict[str, Any]:
    """
    Load, translate, and return JSON file content.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Translate title
    if 'title' in data:
        data['title'] = translate_text(data['title'])

    # Translate description
    if 'description' in data:
        data['description'] = translate_text(data['description'])

    # Translate content
    if 'content' in data:
        data['content'] = translate_text(data['content'])

    # Translate author
    if 'author' in data:
        data['author'] = translate_author(data['author'])

    # Translate seo_keywords
    if 'seo_keywords' in data and isinstance(data['seo_keywords'], list):
        data['seo_keywords'] = [translate_text(keyword) for keyword in data['seo_keywords']]

    # Translate pros_and_cons
    if 'pros_and_cons' in data and isinstance(data['pros_and_cons'], list):
        for item in data['pros_and_cons']:
            if 'pros' in item and isinstance(item['pros'], list):
                item['pros'] = [translate_text(pro) for pro in item['pros']]
            if 'cons' in item and isinstance(item['cons'], list):
                item['cons'] = [translate_text(con) for con in item['cons']]

    # Translate FAQ
    if 'faq' in data and isinstance(data['faq'], list):
        for item in data['faq']:
            if 'question' in item:
                item['question'] = translate_text(item['question'])
            if 'answer' in item:
                item['answer'] = translate_text(item['answer'])

    # Ensure language is set to en-US
    data['language'] = 'en-US'

    # Keep slug unchanged
    # slug remains as-is

    return data

def process_directory(directory: Path):
    """Process all JSON files in directory."""
    json_files = list(directory.glob('*.json'))

    print(f"Found {len(json_files)} files to process")

    for filepath in json_files:
        print(f"Processing: {filepath.name}")

        # Translate
        translated_data = translate_json_file(filepath)

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(translated_data, f, ensure_ascii=False, indent=2)

        print(f"Completed: {filepath.name}")

    print(f"\nAll {len(json_files)} files translated successfully!")

if __name__ == '__main__':
    directory = Path('/Users/gejiayu/owner/seo/data/manufacturing-production-tools')
    process_directory(directory)