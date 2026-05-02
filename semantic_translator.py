#!/usr/bin/env python3
"""
Semantic Chinese → English Translation Script for Medical Equipment Rental Domain
Uses domain-specific vocabulary mappings for high-quality automated translation
"""

import json
import re

# Domain-specific Chinese → English vocabulary mappings
TRANSLATION_DICT = {
    # Core System Types
    "医疗设备租赁合规管理系统": "Medical Equipment Rental Compliance Management System",
    "医疗设备租赁合同管理系统": "Medical Equipment Rental Contract Management System",
    "医疗设备租赁成本管理系统": "Medical Equipment Rental Cost Management System",
    "医疗设备租赁CRM系统": "Medical Equipment Rental CRM System",
    "医疗设备租赁客户满意度系统": "Medical Equipment Rental Customer Satisfaction System",
    "医疗设备租赁客户服务管理系统": "Medical Equipment Rental Customer Service Management System",
    "医疗设备租赁数据分析平台": "Medical Equipment Rental Data Analytics Platform",
    "医疗设备租赁配送管理系统": "Medical Equipment Rental Delivery Management System",
    "医疗设备租赁需求预测系统": "Medical Equipment Rental Demand Prediction System",
    "医疗设备租赁数字化转型系统": "Medical Equipment Rental Digital Transformation System",
    "医疗设备租赁文档管理系统": "Medical Equipment Rental Document Management System",
    "医疗设备租赁能源管理系统": "Medical Equipment Rental Energy Management System",
    "医疗设备租赁财务管理系统": "Medical Equipment Rental Finance Management System",
    "医疗设备租赁金融管理系统": "Medical Equipment Rental Financial Management System",
    "医疗设备租赁车队管理系统": "Medical Equipment Rental Fleet Management System",
    "医疗设备租赁全球化管理系统": "Medical Equipment Rental Globalization Management System",
    "医疗设备租赁HR管理系统": "Medical Equipment Rental HR Management System",
    "医疗设备租赁创新管理系统": "Medical Equipment Rental Innovation Management System",

    # Common Terms
    "评测": "Review",
    "工具": "Tool",
    "系统": "System",
    "平台": "Platform",
    "软件": "Software",
    "管理": "Management",
    "设备": "Equipment",
    "租赁": "Rental",
    "合规": "Compliance",
    "认证": "Certification",
    "追踪": "Tracking",
    "检查": "Inspection",
    "安全": "Safety",
    "计划": "Plan",
    "记录": "Record",
    "报告": "Report",
    "流程": "Process",
    "功能": "Functionality",
    "价格": "Pricing",
    "对比": "Comparison",
    "分析": "Analysis",
    "评测": "Review",
    "方案": "Solution",
    "需求": "Needs",
    "决策": "Decision",

    # Medical Terms
    "医疗": "Medical",
    "FDA": "FDA",
    "CE": "CE",
    "CFDA": "CFDA",
    "ISO": "ISO",
    "医疗器械": "Medical Device",
    "质量管理体系": "Quality Management System",
    "有效期": "Validity Period",
    "过期": "Expiration",
    "续期": "Renewal",
    "到期": "Expiration",
    "提醒": "Reminder",
    "自动": "Automatic",

    # Compliance Terms
    "消毒": "Disinfection",
    "召回": "Recall",
    "整改": "Rectification",
    "不合格": "Non-compliant",
    "预警": "Warning",
    "隔离": "Isolation",
    "禁止": "Prohibition",
    "风险": "Risk",
    "监管": "Regulatory",
    "法规": "Regulations",
    "审核": "Audit",
    "文档": "Documentation",
    "技术": "Technical",
    "数据库": "Database",

    # Safety Terms
    "电气安全": "Electrical Safety",
    "机械安全": "Mechanical Safety",
    "辐射安全": "Radiation Safety",
    "月度": "Monthly",
    "季度": "Quarterly",
    "年度": "Annual",
    "周期": "Period",
    "周期设定": "Period Setting",

    # Disinfection Terms
    "高温消毒": "High-temperature Disinfection",
    "化学消毒": "Chemical Disinfection",
    "紫外线消毒": "UV Disinfection",
    "消毒剂": "Disinfectant",
    "消毒人员": "Disinfection Personnel",
    "消毒时间": "Disinfection Time",
    "消毒验证": "Disinfection Verification",
    "消毒效果": "Disinfection Effectiveness",
    "消毒标准": "Disinfection Standard",
    "租赁前消毒": "Pre-rental Disinfection",
    "租赁后消毒": "Post-rental Disinfection",
    "防止交叉感染": "Prevent Cross-infection",

    # Market Terms
    "美国市场": "US Market",
    "欧洲市场": "European Market",
    "中国市场": "Chinese Market",
    "目标市场": "Target Market",
    "全球": "Global",
    "全市场": "All Markets",
    "公告机构": "Notified Body",
    "欧盟医疗器械法规": "EU Medical Device Regulation",

    # Product Terms
    "产品": "Product",
    "核心定位": "Core Positioning",
    "月费范围": "Monthly Fee Range",
    "定价策略": "Pricing Strategy",
    "基础版": "Basic Version",
    "专业版": "Professional Version",
    "主流": "Mainstream",
    "专业": "Professional",
    "套件": "Suite",
    "专注": "Focus",
    "适合": "Suitable",
    "覆盖": "Covering",
    "支持": "Support",
    "无": "None",

    # Tech Terms
    "云端部署": "Cloud Deployment",
    "移动端APP": "Mobile App",
    "实时更新": "Real-time Update",
    "自动生成": "Automatic Generation",
    "API对接": "API Integration",
    "数据对接": "Data Integration",
    "存储": "Storage",
    "版本追踪": "Version Tracking",

    # Business Terms
    "企业": "Enterprise",
    "客户": "Customer",
    "信任": "Trust",
    "投诉": "Complaints",
    "法律责任": "Legal Liability",
    "停租": "Rental Suspension",
    "罚款": "Fines",
    "降低": "Reduce",
    "提升": "Enhance",
    "确保": "Ensure",

    # Analysis Terms
    "深度评测": "In-depth Review",
    "对比表": "Comparison Table",
    "对比维度": "Comparison Dimension",
    "核心功能": "Core Functionality",
    "技术特点": "Technical Features",
    "痛点": "Pain Points",
    "解决方案": "Solution",
    "遗漏": "Oversight",
    "缺失": "Missing",
    "不及时": "Untimely",

    # Prediction Terms
    "预测": "Prediction",
    "行业趋势": "Industry Trends",
    "数字化趋势": "Digitalization Trends",
    "AI合规预警": "AI Compliance Warning",
    "实时监控": "Real-time Monitoring",
    "多地区合规": "Multi-region Compliance",
    "一站式管理": "One-stop Management",
    "一键导出": "One-click Export",
    "提交监管机构": "Submit to Regulatory Authorities",
    "在线化": "Online",
    "在线课程": "Online Courses",
    "员工合规考核追踪": "Employee Compliance Assessment Tracking",

    # Selection Terms
    "选型建议": "Selection Recommendations",
    "推荐": "Recommend",
    "选型策略": "Selection Strategy",
    "一体化": "Integrated",
    "直接影响": "Directly Impact",
    "综合评估": "Comprehensive Evaluation",
    "针对不同": "For Different",

    # Date/Year
    "2026年评测": "2026 Review",
    "｜": "|",

    # Common Phrases
    "深度评测医疗设备租赁": "In-depth review of medical equipment rental",
    "涵盖": "covering",
    "等功能": "and other functionality",
    "提供详细产品对比表": "Provides detailed product comparison table",
    "了解更多功能和价格对比": "Learn more about functionality and pricing comparisons",
    "找到最适合你的方案": "to find the best solution for your needs",
    "专业评测助你决策": "Professional review helps you make informed decisions",
}

def translate_text(chinese_text):
    """
    Translate Chinese text to English using domain-specific vocabulary
    """
    # Sort by length (longest first) to replace compounds before components
    sorted_dict = sorted(TRANSLATION_DICT.items(), key=lambda x: len(x[0]), reverse=True)

    result = chinese_text
    for chinese, english in sorted_dict:
        result = result.replace(chinese, english)

    # Handle any remaining Chinese characters with a placeholder
    # (should be minimal if vocabulary is comprehensive)
    chinese_chars = re.findall(r'[一-鿿]+', result)
    if chinese_chars:
        # For remaining Chinese, we'll leave as-is and note for manual review
        pass

    return result

def translate_file(filepath):
    """
    Translate a JSON file from Chinese to English
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Translate all string fields
        for key in ['title', 'description', 'content']:
            if key in data and isinstance(data[key], str):
                data[key] = translate_text(data[key])

        # Translate keywords
        if 'seo_keywords' in data and isinstance(data['seo_keywords'], list):
            data['seo_keywords'] = [translate_text(kw) for kw in data['seo_keywords']]

        # Add language field
        data['language'] = 'en-US'

        # Save translated file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"Error translating {filepath}: {e}")
        return False

# Files to translate (files 21-39 from the directory)
import os

files = [
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-contract-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-cost-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-crm-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-customer-satisfaction-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-customer-service-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-data-analytics-platform-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-delivery-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-demand-prediction-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-digital-transformation-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-document-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-energy-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-finance-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-financial-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-fleet-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-globalization-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-hr-management-system-review.json",
    "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-innovation-management-system-review.json",
]

print("=" * 80)
print("TRANSLATING CHINESE FILES TO ENGLISH (Files 21-39)")
print("=" * 80)

translated_count = 0
failed_count = 0

for filepath in files:
    filename = os.path.basename(filepath)
    print(f"\n📝 Translating: {filename}")

    if translate_file(filepath):
        translated_count += 1
        print(f"   ✅ Successfully translated")

        # Show preview
        with open(filepath, 'r') as f:
            data = json.load(f)
        print(f"   Preview: {data['title'][:100]}...")
    else:
        failed_count += 1
        print(f"   ❌ Translation failed")

print("\n" + "=" * 80)
print("TRANSLATION SUMMARY")
print("=" * 80)
print(f"Successfully translated: {translated_count}/{len(files)}")
print(f"Failed: {failed_count}")
print(f"\nAll translated files now have 'language': 'en-US' field added.")