#!/usr/bin/env python3
"""
Translate Chinese content to English in tennis-racket-rental-tools JSON files.
Handles both isolated Chinese phrases and entirely Chinese files.
"""
import json
import re
from pathlib import Path

# Comprehensive translation dictionary for tennis rental domain
TRANSLATIONS = {
    # Titles - 2026 reviews
    "网球租赁客户忠诚度系统评测：会员积分与复租激励的关键工具｜2026年评测": "Tennis Rental Customer Loyalty System Review: Key Tools for Member Points and Repeat Rental Incentives | 2026 Review",
    "网球租赁数据导出工具评测：数据迁移与备份的关键解决方案｜2026年评测": "Tennis Rental Data Export Tools Review: Key Solutions for Data Migration and Backup | 2026 Review",
    "网球租赁决策支持系统评测：智能推荐与资源优化关键工具｜2026年评测": "Tennis Rental Decision Support System Review: Key Tools for Intelligent Recommendations and Resource Optimization | 2026 Review",
    "网球租赁企业解决方案评测：大型场馆与连锁品牌的数字化方案｜2026年评测": "Tennis Rental Enterprise Solutions Review: Digital Solutions for Large Venues and Chain Brands | 2026 Review",
    "网球租赁设备分析工具评测：设备利用率与损耗分析的关键解决方案｜2026年评测": "Tennis Rental Equipment Analytics Tools Review: Key Solutions for Equipment Utilization and Loss Analysis | 2026 Review",

    # Common system terms
    "系统": "System",
    "管理": "Management",
    "模块": "Module",
    "功能": "Features",
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

    # Tennis specific terms
    "网球": "Tennis",
    "网球租赁": "Tennis Rental",
    "球拍": "Racket",
    "拍线": "String",
    "握把": "Grip",
    "拍框": "Frame",
    "打球": "Playing",
    "时段": "Time slot",
    "场馆": "Venue",
    "赛事": "Event",
    "培训": "Training",
    "课程": "Course",
    "技能": "Skill",
    "教练": "Coach",
    "会员": "Member",
    "客户": "Customer",

    # Business terms
    "租赁": "Rental",
    "库存": "Inventory",
    "设备": "Equipment",
    "资产": "Asset",
    "价值": "Value",
    "成本": "Cost",
    "收入": "Revenue",
    "利润": "Profit",
    "财务": "Financial",
    "定价": "Pricing",
    "折扣": "Discount",
    "优惠": "Discount",
    "促销": "Promotion",
    "营销": "Marketing",
    "品牌": "Brand",
    "连锁": "Chain",
    "总部": "Headquarters",
    "扩张": "Expansion",
    "增长": "Growth",
    "效率": "Efficiency",
    "运营": "Operations",
    "业务": "Business",
    "企业": "Enterprise",

    # Personnel terms
    "员工": "Employee",
    "人员": "Personnel",
    "排班": "Scheduling",
    "调度": "Dispatch",
    "绩效": "Performance",
    "考核": "Assessment",
    "留存": "Retention",
    "流失": "Churn",
    "离职": "Resignation",

    # Customer/member terms
    "忠诚度": "Loyalty",
    "积分": "Points",
    "等级": "Level/Tier",
    "权益": "Rights/Benefits",
    "奖励": "Reward",
    "兑换": "Exchange",
    "粘性": "Stickiness",
    "复租": "Repeat rental",
    "转化": "Conversion",
    "推荐": "Recommendation/Referral",
    "邀请": "Invite",
    "好友": "Friend",
    "注册": "Register",
    "评价": "Review/Evaluation",
    "投诉": "Complaint",
    "反馈": "Feedback",
    "画像": "Profile",
    "生命周期": "Lifecycle",
    "行为": "Behavior",
    "偏好": "Preference",
    "信用": "Credit",

    # Operational terms
    "预约": "Appointment/Booking",
    "预订": "Booking",
    "提醒": "Reminder",
    "通知": "Notification",
    "警报": "Alert",
    "预警": "Warning",
    "风险": "Risk",
    "决策": "Decision",
    "模拟": "Simulation",
    "评估": "Assessment",
    "效果": "Effect",
    "趋势": "Trend",
    "预测": "Prediction",
    "智能": "Intelligent",
    "自动化": "Automation",
    "可视化": "Visualization",
    "实时": "Real-time",
    "云端": "Cloud",
    "整合": "Integration",
    "能力": "Capability",

    # Data terms
    "导出": "Export",
    "迁移": "Migration",
    "备份": "Backup",
    "格式": "Format",
    "验证": "Verification",
    "完整": "Complete",
    "覆盖": "Coverage",
    "定时": "Scheduled",
    "批量": "Batch",

    # Analysis terms
    "利用率": "Utilization rate",
    "损耗": "Loss/Wear",
    "残值": "Residual value",
    "折旧": "Depreciation",
    "周转率": "Turnover rate",
    "出租率": "Rental rate",
    "闲置率": "Idle rate",

    # Structural phrases
    "核心功能：": "<strong>Core Features:</strong>",
    "核心定位": "Core Focus",
    "定价模式": "Pricing Model",
    "整合范围": "Integration Scope",
    "价格方案：": "<strong>Pricing Plan:</strong>",
    "基础版每月": "Basic version monthly",
    "专业版每月": "Professional version monthly",
    "企业定制报价": "Enterprise custom pricing",
    "订阅模式": "Subscription model",
    "包含": "includes",
    "每年": "annually",
    "按": "By",
    "计费": "Charged",
    "免费": "free",
    "美元": "USD",

    # Section headers
    "功能对比表": "Feature Comparison Table",
    "系统名称": "System Name",
    "选择建议": "Selection Recommendations",
    "未来发展趋势": "Future Development Trends",
    "未来发展方向": "Future Development Directions",
    "核心价值在于": "Core value lies in",
    "数据显示": "Data shows that",
    "而采用": "After adopting",
    "后": "",
    "提升至": "increases to",
    "降低": "decreases",
    "达": "reaches",
    "仅": "only",
    "约": "approximately",

    # Common phrases in descriptions
    "专业评测网球租赁": "Professional review of tennis rental",
    "深度评测网球租赁": "In-depth analysis of tennis rental",
    "涵盖": "covering",
    "助租赁业务": "for rental businesses",
    "了解更多功能和价格对比": "Compare features and pricing",
    "找到最适合你的方案": "to find the best solution",
    "专业评测助你决策": "Professional reviews help you make decisions",

    # Paragraph starters
    "网球租赁业务": "Tennis rental businesses",
    "传统": "Traditional",
    "缺乏": "lacking",
    "依赖": "rely on",
    "难以": "difficult to",
    "导致": "leading to",

    # Product names (keep in English)
    "LoyaltyBoost Rental": "LoyaltyBoost Rental",
    "TennisLoyalty Pro": "TennisLoyalty Pro",
    "MemberEngage Suite": "MemberEngage Suite",
    "DataExport Rental": "DataExport Rental",
    "TennisData Pro": "TennisData Pro",
    "DataMigration Suite": "DataMigration Suite",
    "DecisionSupport Rental": "DecisionSupport Rental",
    "TennisDecision Pro": "TennisDecision Pro",
    "IntelligentDecision Suite": "IntelligentDecision Suite",
    "EnterpriseRental Suite": "EnterpriseRental Suite",
    "TennisEnterprise Pro": "TennisEnterprise Pro",
    "MultiLocation Manager": "MultiLocation Manager",
    "EquipmentAnalytics Rental": "EquipmentAnalytics Rental",
    "TennisEquipment Pro": "TennisEquipment Pro",
    "AssetAnalytics Suite": "AssetAnalytics Suite",

    # Company names
    "LoyaltyTech公司开发": "developed by LoyaltyTech",
    "TennisLoyalty公司开发": "developed by TennisLoyalty",
    "DataTech公司开发": "developed by DataTech",
    "TennisData公司开发": "developed by TennisData",
    "DecisionTech公司开发": "developed by DecisionTech",
    "TennisDecision公司开发": "developed by TennisDecision",
    "EnterpriseTech公司开发": "developed by EnterpriseTech",
    "TennisEnterprise公司开发": "developed by TennisEnterprise",
    "EquipmentTech公司开发": "developed by EquipmentTech",
    "TennisEquipment公司开发": "developed by TennisEquipment",

    # Company name variations
    "由LoyaltyTech公司开发": "developed by LoyaltyTech",
    "由TennisLoyalty公司开发": "developed by TennisLoyalty",
    "由DataTech公司开发": "developed by DataTech",
    "由TennisData公司开发": "developed by TennisData",
    "由DecisionTech公司开发": "developed by DecisionTech",
    "由TennisDecision公司开发": "developed by TennisDecision",
    "由EnterpriseTech公司开发": "developed by EnterpriseTech",
    "由TennisEnterprise公司开发": "developed by TennisEnterprise",
    "由EquipmentTech公司开发": "developed by EquipmentTech",
    "由TennisEquipment公司开发": "developed by TennisEquipment",

    # Descriptive phrases
    "是专业的租赁": "is a professional rental",
    "是网球专项": "is a tennis-specific",
    "是综合性": "is a comprehensive",
    "系统将": "The system integrates",
    "与": "with",
    "深度整合": "deeply integrated",
    "深度理解": "deeply understands",
    "租赁业务深度整合": "deeply integrated with rental business",
    "网球特点": "tennis characteristics",

    # List items markers
    "<li>": "<li>",
    "</li>": "</li>",
    "<ul>": "<ul>",
    "</ul>": "</ul>",

    # Table elements
    "<thead>": "<thead>",
    "</thead>": "</thead>",
    "<tbody>": "<tbody>",
    "</tbody>": "</tbody>",
    "<tr>": "<tr>",
    "</tr>": "</tr>",
    "<th>": "<th>",
    "</th>": "</th>",
    "<td>": "<td>",
    "</td>": "</td>",

    # Other common words
    "大型": "large-scale",
    "中型": "medium-sized",
    "小型": "small",
    "每个": "each",
    "每次": "each time",
    "每次租赁": "each rental",
    "每次打球": "each playing session",
    "累计": "accumulated",
    "享受": "enjoy",
    "获得": "obtain/get",
    "支持": "supports",
    "适用于": "suitable for",
    "提供": "provides",
    "实现": "achieve",
    "保障": "guarantee",
    "降低风险": "reduce risks",
    "提升效率": "improve efficiency",
    "优化配置": "optimize configuration",
    "精准分析": "precise analysis",
    "科学评估": "scientific assessment",
    "自动生成": "automatically generated",
    "实时追踪": "real-time tracking",
    "统一管理": "unified management",
    "标准化": "standardization",
    "定制开发": "custom development",
    "规模化运营": "scaled operations",
    "品牌一致性": "brand consistency",

    # Action verbs
    "推荐": "recommend",
    "适合": "suitable for",
    "建议": "suggest",
    "注重": "emphasizing",
    "已成为": "has become",
    "必备工具": "essential tool",

    # Connector words
    "和": "and",
    "与": "and",
    "或": "or",
    "的": "",
    "等": "etc.",
    "以及": "as well as",

    # Numbers and quantities
    "万": "10,000",
    "每月万": "monthly 10,000",
    "以下": "under",
    "以上": "over",
    "每月": "monthly",
    "每年": "annually",
    "起": "starting from",

    # Percentages and comparisons
    "%": "%",
    "提升": "increase",
    "降低": "decrease",
    "增加": "increase",
    "减少": "decrease",

    # Qualifiers
    "仅": "only",
    "高达": "up to",
    "约为": "approximately",
    "左右": "around",

    # Negations
    "不足": "insufficient",
    "不及时": "untimely",
    "不清晰": "unclear",
    "不准确": "inaccurate",
    "不合理": "unreasonable",
    "无法": "unable to",
    "缺乏": "lacking",

    # Pain points and challenges
    "痛点": "pain points",
    "挑战": "challenges",
    "困难": "difficulties",
    "复杂": "complex",
    "繁琐": "tedious",
    "众多": "numerous",
    "多样": "diverse",
    "深远": "far-reaching",
    "高": "high",
    "低": "low",

    # Specific feature descriptions
    "积分体系": "Points system",
    "会员等级体系": "Member tier system",
    "奖励兑换商城": "Reward exchange marketplace",
    "社交裂变传播": "Social viral spread",
    "数据自动导出": "Automatic data export",
    "数据格式迁移": "Data format migration",
    "数据安全备份": "Secure data backup",
    "数据完整验证": "Complete data verification",
    "决策系统分析": "Decision system analysis",
    "资源优化配置": "Resource optimization configuration",
    "智能决策推荐": "Intelligent decision recommendation",
    "决策模拟验证": "Decision simulation verification",
    "多场馆统一管理": "Multi-venue unified management",
    "连锁运营标准化": "Chain operation standardization",
    "企业架构定制化": "Enterprise architecture customization",
    "总部管控功能": "Headquarters control functions",
    "利用率精准分析": "Utilization precise analysis",
    "损耗实时追踪": "Loss real-time tracking",
    "价值科学评估": "Value scientific assessment",
    "配置优化建议": "Configuration optimization suggestions",

    # Time-related
    "定期": "periodic",
    "增量": "incremental",
    "完整备份": "complete backup",
    "实时": "real-time",
    "即时": "instant",

    # Format types
    "Excel": "Excel",
    "CSV": "CSV",
    "JSON": "JSON",
    "XML": "XML",
    "数据库": "database",

    # Status indicators
    "成功": "success",
    "失败": "failure",
    "异常": "anomaly",
    "正常": "normal",
}

def translate_text(text):
    """Translate Chinese text to English using the translation dictionary"""
    if not isinstance(text, str):
        return text

    # Apply all translations
    for chinese, english in TRANSLATIONS.items():
        text = text.replace(chinese, english)

    return text

def process_entirely_chinese_file(filepath):
    """Process a file that is entirely in Chinese"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Translate all content fields
    if 'title' in data:
        data['title'] = translate_text(data['title'])
    if 'description' in data:
        data['description'] = translate_text(data['description'])
    if 'content' in data:
        data['content'] = translate_text(data['content'])
    if 'author' in data:
        data['author'] = translate_text(data['author'])

    # Ensure language is en-US
    data['language'] = 'en-US'

    # Save updated file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return f"TRANSLATED: {filepath.name}"

def main():
    # List of entirely Chinese files
    entirely_chinese_files = [
        "tennis-rental-customer-loyalty-system.json",
        "tennis-rental-data-export-tools.json",
        "tennis-rental-decision-support-system.json",
        "tennis-rental-enterprise-solutions.json",
        "tennis-rental-equipment-analytics-tools.json",
        "tennis-rental-financial-management-system.json",
        "tennis-rental-franchise-management-system.json",
        "tennis-rental-growth-analysis-platform.json",
        "tennis-rental-insurance-integration-platform.json",
        "tennis-rental-inventory-management-software.json",
        "tennis-rental-kpi-tracking-tools.json",
        "tennis-rental-market-research-tools.json",
        "tennis-rental-marketing-automation-system.json",
        "tennis-rental-membership-management-system.json",
        "tennis-rental-mobile-app-review.json",
        "tennis-rental-multi-venue-management-system.json",
        "tennis-rental-notification-reminder-system.json",
        "tennis-rental-operation-efficiency-tools.json",
        "tennis-rental-payment-system-review.json",
        "tennis-rental-performance-management-system.json",
        "tennis-rental-pricing-strategy-system.json",
        "tennis-rental-quality-control-system.json",
        "tennis-rental-referral-program-platform.json",
        "tennis-rental-reporting-dashboard.json",
        "tennis-rental-revenue-optimization-platform.json",
        "tennis-rental-risk-management-platform.json",
        "tennis-rental-scheduling-dispatch-system.json",
        "tennis-rental-staff-management-system.json",
        "tennis-rental-staff-training-platform.json",
        "tennis-rental-strategic-planning-tools.json",
        "tennis-rental-subscription-model-platform.json",
        "tennis-rental-system-integration-platform.json",
        "tennis-rental-trend-analysis-platform.json",
        "tennis-rental-user-experience-platform.json",
        "tennis-rental-venue-analytics-system.json",
    ]

    directory = Path('/Users/gejiayu/owner/seo/data/tennis-racket-rental-tools')

    results = []
    for filename in entirely_chinese_files:
        filepath = directory / filename
        if filepath.exists():
            result = process_entirely_chinese_file(filepath)
            results.append(result)

    for result in results:
        print(result)

    print(f"\nTotal entirely Chinese files translated: {len(results)}")

if __name__ == '__main__':
    main()