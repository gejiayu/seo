#!/usr/bin/env python3
"""
Translate Chinese content to English in massage-spa-wellness-tools JSON files.
"""

import json
import os
import re
from pathlib import Path

# Comprehensive translation dictionary for massage/spa/wellness domain
TRANSLATIONS = {
    # Common system terms
    "系统": "System",
    "管理": "Management",
    "模块": "Module",
    "功能": "Function",
    "平台": "Platform",
    "软件": "Software",
    "工具": "Tool",
    "方案": "Solution",
    "评测": "Review",
    "指南": "Guide",
    "分析": "Analysis",
    "优化": "Optimization",
    "策略": "Strategy",
    "配置": "Configuration",
    "监控": "Monitoring",
    "追踪": "Tracking",
    "报表": "Report",
    "记录": "Record",
    "数据": "Data",
    "信息": "Information",
    "服务": "Service",
    "流程": "Process",
    "标准": "Standard",
    "规范": "Specification",
    "合规": "Compliance",
    "安全": "Safety",
    "保护": "Protection",
    "隐私": "Privacy",

    # Industry specific terms - Massage & Wellness
    "按摩": "Massage",
    "按摩店": "Massage Shop",
    "按摩师": "Massage Therapist",
    "技师": "Technician",
    "技师管理": "Technician Management",
    "技师排班": "Technician Scheduling",
    "技师绩效": "Technician Performance",
    "技师考核": "Technician Assessment",
    "技师培训": "Technician Training",
    "技师技能": "Technician Skill",
    "技师晋升": "Technician Promotion",
    "技师合同": "Technician Contract",
    "技师离职": "Technician Resignation",
    "技师关怀": "Technician Care",
    "技师满意度": "Technician Satisfaction",
    "技师留存": "Technician Retention",
    "技师流失预警": "Technician Churn Warning",
    "技师佣金": "Technician Commission",
    "技师奖金": "Technician Bonus",
    "技师心理健康": "Technician Mental Health",
    "技师服务标准化": "Technician Service Standardization",
    "技师认证": "Technician Certification",
    "技师招聘": "Technician Recruitment",
    "技师职业发展": "Technician Career Development",
    "技师工时": "Technician Hours",

    "SPA": "SPA",
    "养生": "Wellness",
    "养生店": "Wellness Center",
    "养生行业": "Wellness Industry",
    "健康": "Health",
    "健康档案": "Health Record",

    # Member/Customer terms
    "会员": "Member",
    "会员管理": "Member Management",
    "会员储值": "Member Stored Value",
    "会员关怀": "Member Care",
    "会员权益": "Member Benefits",
    "会员积分": "Member Points",
    "会员等级": "Member Tier",
    "会员忠诚度": "Member Loyalty",
    "会员留存": "Member Retention",
    "会员激活": "Member Activation",
    "会员营销": "Member Marketing",
    "会员满意度": "Member Satisfaction",
    "会员画像": "Member Profile",
    "会员生命周期": "Member Lifecycle",
    "会员流失": "Member Churn",
    "会员复购": "Member Repurchase",
    "会员分层": "Member Segmentation",
    "会员推荐": "Member Referral",
    "会员投诉": "Member Complaint",
    "会员隐私": "Member Privacy",
    "会员反馈": "Member Feedback",
    "会员评价": "Member Review",
    "会员行为": "Member Behavior",

    "客户": "Customer",
    "客户管理": "Customer Management",
    "客户档案": "Customer Profile",
    "客户满意度": "Customer Satisfaction",
    "客户忠诚度": "Customer Loyalty",
    "客户留存": "Customer Retention",
    "客户投诉": "Customer Complaint",
    "客户反馈": "Customer Feedback",
    "客户评价": "Customer Review",
    "客户推荐": "Customer Referral",
    "客户画像": "Customer Profile",
    "客户生命周期": "Customer Lifecycle",
    "客户流失": "Customer Churn",
    "客户复购预测": "Customer Repurchase Prediction",
    "客户分层": "Customer Segmentation",
    "客户行为": "Customer Behavior",
    "客户偏好": "Customer Preference",
    "客户健康档案": "Customer Health Record",
    "客户信用": "Customer Credit",

    # Appointment terms
    "预约": "Appointment",
    "预约优化": "Appointment Optimization",
    "预约调度": "Appointment Scheduling",
    "预约管理": "Appointment Management",
    "预约提醒": "Appointment Reminder",
    "预约冲突": "Appointment Conflict",
    "预约数据分析": "Appointment Data Analysis",
    "预约渠道": "Appointment Channel",
    "预约需求预测": "Appointment Demand Prediction",
    "预约等候": "Appointment Waitlist",

    # Room terms
    "房间": "Room",
    "房间调度": "Room Scheduling",
    "房间管理": "Room Management",
    "房间状态": "Room Status",
    "房间清洁": "Room Cleaning",
    "房间设备": "Room Equipment",

    # Service terms
    "服务项目": "Service Project",
    "服务组合": "Service Combination",
    "服务套餐": "Service Package",
    "服务附加": "Service Add-on",
    "服务标准化": "Service Standardization",
    "服务流程": "Service Process",
    "服务安全": "Service Safety",
    "服务合规": "Service Compliance",
    "服务质量": "Service Quality",
    "服务质量监控": "Service Quality Monitoring",
    "服务风险": "Service Risk",
    "服务创新": "Service Innovation",
    "服务治疗": "Service Treatment",

    # Promotion/Marketing terms
    "促销": "Promotion",
    "促销活动": "Promotional Campaign",
    "促销管理": "Promotion Management",
    "促销内容": "Promotion Content",
    "促销渠道": "Promotion Channel",
    "促销效果": "Promotion Effect",
    "促销成本": "Promotion Cost",

    "营销": "Marketing",
    "营销自动化": "Marketing Automation",
    "营销ROI": "Marketing ROI",
    "社交媒体营销": "Social Media Marketing",
    "品牌推广": "Brand Promotion",
    "口碑管理": "Reputation Management",

    # Financial terms
    "财务": "Financial",
    "财务管理": "Financial Management",
    "财务报表": "Financial Report",
    "成本分析": "Cost Analysis",
    "利润分析": "Profit Analysis",
    "预收款": "Pre-collection",
    "储值": "Stored Value",
    "储值卡": "Stored Value Card",
    "储值管理": "Stored Value Management",
    "储值充值": "Stored Value Recharge",
    "储值消费": "Stored Value Consumption",
    "储值退款": "Stored Value Refund",
    "储值过期": "Stored Value Expiration",
    "储值会计": "Stored Value Accounting",
    "储值余额": "Stored Value Balance",

    # Inventory/Equipment terms
    "库存": "Inventory",
    "库存管理": "Inventory Management",
    "供应商": "Supplier",
    "供应商管理": "Supplier Management",
    "设备": "Equipment",
    "设备维护": "Equipment Maintenance",
    "能源": "Energy",
    "能源管理": "Energy Management",

    # Employee/Staff terms
    "员工": "Employee",
    "员工管理": "Employee Management",
    "排班": "Scheduling",
    "排班管理": "Scheduling Management",
    "排班轮班": "Scheduling Shift",
    "考勤": "Attendance",
    "考勤管理": "Attendance Management",
    "请假": "Leave",
    "请假管理": "Leave Management",
    "绩效": "Performance",
    "绩效管理": "Performance Management",
    "绩效考核": "Performance Assessment",

    # Store/Location terms
    "连锁": "Chain",
    "跨店": "Cross-store",
    "选址": "Location",
    "选址分析": "Location Analysis",
    "店面": "Store",
    "店面选址": "Store Location",
    "内部设计": "Interior Design",

    # Payment terms
    "POS": "POS",
    "POS支付": "POS Payment",
    "支付": "Payment",
    "支付系统": "Payment System",

    "礼品卡": "Gift Card",
    "礼品卡管理": "Gift Card Management",

    # Analytics terms
    "数据可视化": "Data Visualization",
    "数据分析": "Data Analysis",
    "数据分析平台": "Data Analytics Platform",
    "运营效率": "Operation Efficiency",
    "高峰时段": "Peak Hour",
    "定价策略": "Pricing Strategy",
    "竞争分析": "Competitor Analysis",

    # Platform names
    "美业帮": "MeiYeBang",
    "店务通": "DianWuTong",
    "客如云": "KeRuYun",

    # Status/Quality terms
    "完善": "Comprehensive",
    "强大": "Powerful",
    "基础": "Basic",
    "年费": "Annual fee",
    "月费": "Monthly fee",
    "内置免费": "Built-in Free",
    "需定制": "Customization needed",
    "不支持": "Not supported",
    "深度集成": "Deep integration",
    "性价比突出": "Exceptional value",
    "本土化": "Localized",
    "本土": "Local",
    "全球": "Global",
    "云端": "Cloud",
    "新一代": "Next-generation",
    "领先": "Leading",
    "主流": "Mainstream",

    # Time terms
    "2026年": "2026",
    "专业": "Professional",
    "完整": "Complete",
    "全面": "Comprehensive",
    "深入": "In-depth",
    "核心": "Core",
    "关键": "Key",
    "重要": "Important",
    "战略价值": "Strategic Value",
    "发展趋势": "Development Trends",
    "决策要点": "Decision Points",
    "综合建议": "Comprehensive recommendation",

    # Action terms
    "识别": "Identify",
    "创作": "Create",
    "推送": "Push",
    "生成": "Generate",
    "保存": "Save",
    "查询": "Query",
    "分配": "Allocate",
    "执行": "Execute",
    "审批": "Approve",
    "应用": "Apply",
    "开具": "Issue",
    "检查": "Check",
    "维护": "Maintain",
    "预测": "Predict",
    "推荐": "Recommend",
    "预警": "Warning",
    "提醒": "Reminder",
    "通知": "Notification",
    "自动": "Automatic",
    "手动": "Manual",
    "灵活": "Flexible",
    "实时": "Real-time",
    "定时": "Scheduled",
    "精准": "Precise",
    "智能": "Intelligent",
    "AI": "AI",
    "自动化": "Automation",

    # Relationship terms
    "关联": "Association",
    "对比": "Comparison",
    "对比表": "Comparison Table",

    # Common phrases
    "数据显示": "Data shows",
    "提升": "Increase",
    "降低": "Decrease",
    "缩短": "Shorten",
    "增长": "Grow",
    "面临独特挑战": "Faces unique challenges",
    "面临特殊挑战": "Faces special challenges",
    "多样化": "Diversified",
    "复杂": "Complex",
    "精细化": "Fine-grained",
    "精细化管理": "Fine-grained management",
    "智能化": "Intelligent",
    "系统化": "Systematic",
    "移动化": "Mobile",
    "无缝化": "Seamless",
    "实时化": "Real-time",
    "精准化": "Precise",
    "个性化": "Personalized",
    "吸引力": "Attractiveness",
    "多触达": "Multi-touch",
    "多渠道": "Multi-channel",
    "多样": "Diverse",
    "动态": "Dynamic",
    "无缝": "Seamless",
    "统一": "Unified",
    "合规": "Compliant",
    "符合": "Comply with",
    "消费者权益保护法规": "Consumer rights protection regulations",

    # Ending phrases
    "了解更多功能和价格对比，找到最适合你的方案！专业评测助你决策！": "Compare features and pricing to find your ideal solution!",
    "了解更多功能和价格对比，找到最适合你的方案！": "Compare features and pricing to find your ideal solution!",
}

def translate_text(text):
    """
    Translate Chinese text to English using the dictionary.
    """
    if not isinstance(text, str):
        return text

    # Apply translations from dictionary
    for chinese, english in TRANSLATIONS.items():
        text = text.replace(chinese, english)

    # Clean up extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text

def translate_content(content):
    """
    Translate HTML content with Chinese text to English.
    """
    if not isinstance(content, str):
        return content

    # Apply dictionary translations
    for chinese, english in TRANSLATIONS.items():
        content = content.replace(chinese, english)

    return content

def fix_seo_keywords(keywords):
    """
    Fix SEO keywords by removing extra spaces.
    """
    if not keywords:
        return keywords

    fixed_keywords = []
    for keyword in keywords:
        # Remove extra spaces
        keyword = re.sub(r'\s+', ' ', keyword).strip()
        fixed_keywords.append(keyword)

    return fixed_keywords

def process_file(filepath):
    """
    Process a single JSON file: translate Chinese content and fix SEO keywords.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if file contains Chinese in key fields
    has_chinese = False
    for key in ['title', 'description', 'content', 'author']:
        if key in data and isinstance(data[key], str):
            if re.search(r'[一-鿿]', data[key]):
                has_chinese = True
                break

    if not has_chinese:
        return False

    # Translate Chinese content
    if 'title' in data:
        data['title'] = translate_text(data['title'])
    if 'description' in data:
        data['description'] = translate_text(data['description'])
    if 'content' in data:
        data['content'] = translate_content(data['content'])
    if 'author' in data:
        data['author'] = translate_text(data['author'])

    # Fix SEO keywords
    if 'seo_keywords' in data:
        data['seo_keywords'] = fix_seo_keywords(data['seo_keywords'])

    # Ensure language stays en-US
    data['language'] = 'en-US'

    # Save updated file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return True

def main():
    """
    Main function to process all files with Chinese content.
    """
    directory = Path('/Users/gejiayu/owner/seo/data/massage-spa-wellness-tools')

    processed_count = 0
    for json_file in sorted(directory.glob('*.json')):
        if process_file(json_file):
            processed_count += 1
            print(f"Processed: {json_file.name}")

    print(f"\nTotal files processed: {processed_count}")

if __name__ == '__main__':
    main()