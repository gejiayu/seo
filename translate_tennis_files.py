#!/usr/bin/env python3
import json
import re
from pathlib import Path

# Comprehensive translation dictionary for Chinese to English
# For isolated Chinese phrases in English text
PHRASE_TRANSLATIONS = {
    "及时发现": "timely detection",
    "隐患": "risks",
    "难以": "difficult to",
    "繁琐": "tedious",
    "不足": "insufficient",
    "不系统": "unsystematic",
    "不及时": "untimely",
    "缺乏": "lacking",
    "导致": "leading to",
    "仅有": "only",
    "达到": "reach",
}

# Full translations for entirely Chinese files
# These will be used to translate entire articles
FULL_TRANSLATIONS = {
    # Common terms
    "网球租赁": "Tennis Rental",
    "评测": "Review",
    "系统": "System",
    "工具": "Tool",
    "平台": "Platform",
    "软件": "Software",
    "方案": "Solution",
    "功能": "Features",
    "价格": "Pricing",
    "核心": "Core",
    "专业": "Professional",
    "深度": "In-depth",
    "主流": "Leading",
    "关键": "Key",
    "必备": "Essential",
    "挑战": "Challenges",
    "痛点": "Pain Points",
    "数据显示": "Data shows that",
    "核心价值在于": "Core value lies in",
    "未来发展趋势": "Future Development Trends",
    "选择建议": "Selection Recommendations",
    "功能对比表": "Feature Comparison Table",
    "系统名称": "System Name",
    "核心定位": "Core Focus",
    "定价模式": "Pricing Model",
    "整合范围": "Integration Scope",
    "价格方案": "Pricing Plan",
    "基础版": "Basic version",
    "专业版": "Professional version",
    "企业版": "Enterprise version",
    "每月": "monthly",
    "订阅模式": "Subscription model",
    "按": "By",
    "计费": "Charged",
    "免费": "free",
    "美元": "USD",
    "包含": "includes",
    "整合": "Integrate",
    "能力": "Capability",
    "自动化": "Automation",
    "智能": "Intelligent",
    "分析": "Analysis",
    "管理": "Management",
    "监控": "Monitoring",
    "控制": "Control",
    "优化": "Optimization",
    "预测": "Prediction",
    "推荐": "Recommendation",
    "报表": "Report",
    "提醒": "Reminder",
    "警报": "Alert",
    "决策": "Decision",
    "资源": "Resource",
    "配置": "Configuration",
    "调度": "Scheduling",
    "激励": "Incentive",
    "积分": "Points",
    "会员": "Member",
    "等级": "Level",
    "奖励": "Reward",
    "兑换": "Exchange",
    "忠诚度": "Loyalty",
    "粘性": "Stickiness",
    "复租": "Repeat rental",
    "流失": "Churn",
    "转化": "Conversion",
    "社交": "Social",
    "裂变": "Viral spread",
    "邀请": "Invite",
    "好友": "Friend",
    "注册": "Register",
    "评价": "Review/Evaluation",
    "折扣": "Discount",
    "优先": "Priority",
    "专属": "Exclusive",
    "服务": "Service",
    "权益": "Rights",
    "客户": "Customer",
    "用户": "User",
    "业务": "Business",
    "运营": "Operations",
    "效率": "Efficiency",
    "成本": "Cost",
    "收入": "Revenue",
    "利润": "Profit",
    "财务": "Financial",
    "合规": "Compliance",
    "法规": "Regulations",
    "标准": "Standards",
    "审计": "Audit",
    "检查": "Inspection",
    "风险": "Risk",
    "警报": "Alert",
    "提醒": "Reminder",
    "培训": "Training",
    "教育": "Education",
    "知识": "Knowledge",
    "导出": "Export",
    "迁移": "Migration",
    "备份": "Backup",
    "格式": "Format",
    "验证": "Verification",
    "完整": "Complete",
    "安全": "Secure",
    "效率": "Efficiency",
    "成功": "Success",
    "覆盖": "Coverage",
    "定时": "Scheduled",
    "批量": "Batch",
    "实时": "Real-time",
    "可视化": "Visualization",
    "云端": "Cloud",
    "数据": "Data",
    "设备": "Equipment",
    "时段": "Time slot",
    "场馆": "Venue",
    "赛事": "Event",
    "课程": "Course",
    "打球": "Playing",
    "采购": "Procurement",
    "定价": "Pricing",
    "营销": "Marketing",
    "扩张": "Expansion",
    "品牌": "Brand",
    "连锁": "Chain",
    "总部": "Headquarters",
    "决策": "Decision",
    "模拟": "Simulation",
    "评估": "Assessment",
    "效果": "Effect",
    "策略": "Strategy",
    "方案": "Plan",
    "智能推荐": "Intelligent Recommendation",
    "资源优化": "Resource Optimization",
    "决策支持": "Decision Support",
    "数据导出": "Data Export",
    "数据迁移": "Data Migration",
    "忠诚度系统": "Loyalty System",
    "会员积分": "Member Points",
    "复租激励": "Repeat Rental Incentive",
    "客户粘性": "Customer Stickiness",
    # Title translations
    "网球租赁客户忠诚度系统评测：会员积分与复租激励的关键工具｜2026年评测": "Tennis Rental Customer Loyalty System Review: Key Tools for Member Points and Repeat Rental Incentives | 2026 Review",
    "网球租赁数据导出工具评测：数据迁移与备份的关键解决方案｜2026年评测": "Tennis Rental Data Export Tools Review: Key Solutions for Data Migration and Backup | 2026 Review",
    "网球租赁决策支持系统评测：智能推荐与资源优化关键工具｜2026年评测": "Tennis Rental Decision Support System Review: Key Tools for Intelligent Recommendations and Resource Optimization | 2026 Review",
}

def translate_chinese_phrase(text):
    """Translate Chinese phrases embedded in English text"""
    if not isinstance(text, str):
        return text

    for chinese, english in PHRASE_TRANSLATIONS.items():
        text = text.replace(chinese, english)

    return text

def is_entirely_chinese(text):
    """Check if text is entirely in Chinese"""
    if not isinstance(text, str):
        return False
    # Remove HTML tags and check if remaining text is mostly Chinese
    clean_text = re.sub(r'<[^>]+>', '', text)
    chinese_chars = len(re.findall(r'[一-鿿]', clean_text))
    total_chars = len(re.sub(r'\s', '', clean_text))
    return chinese_chars > total_chars * 0.5

def process_file(filepath):
    """Process a single JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if title is entirely Chinese
    if is_entirely_chinese(data.get('title', '')):
        # File is entirely in Chinese - needs full translation
        # For now, just flag it for manual review
        return f"FULL_CHINESE: {filepath.name}"

    # File has isolated Chinese phrases - translate them
    modified = False
    for key in ['title', 'description', 'content', 'author']:
        if key in data:
            original = data[key]
            translated = translate_chinese_phrase(data[key])
            if original != translated:
                data[key] = translated
                modified = True

    if modified:
        # Ensure language stays en-US
        data['language'] = 'en-US'

        # Save updated file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return f"UPDATED: {filepath.name}"

    return None

def main():
    directory = Path('/Users/gejiayu/owner/seo/data/tennis-racket-rental-tools')

    results = []
    for json_file in directory.glob('*.json'):
        result = process_file(json_file)
        if result:
            results.append(result)

    for result in results:
        print(result)

    print(f"\nTotal files processed: {len(results)}")

if __name__ == '__main__':
    main()