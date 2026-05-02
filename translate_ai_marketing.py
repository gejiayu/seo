#!/usr/bin/env python3
"""
Script to translate Chinese content to English in JSON files for data/ai-marketing/
This script processes files and outputs translated versions.
"""

import json
import os
import re

# Translation mappings for common terms
TRANSLATIONS = {
    # Common phrases
    "中小企业": "Small Business",
    "对比": "Comparison",
    "评测": "Review",
    "详解": "Detailed Analysis",
    "选择建议": "Selection Recommendations",
    "对比总结": "Comparison Summary",
    "帮你找到最适合中小企业的": "Help you find the best for small business",
    "了解更多功能和价格对比": "Learn more about features and pricing comparison",
    "找到最适合你的方案": "Find the best solution for you",
    "专业评测助你决策": "Professional review helps you decide",

    # Challenges
    "challenges": "Challenges",

    # Features
    "Corecapabilities": "Core Capabilities",
    "Core Features": "Core Features",
    "advantages": "Advantages",
    "disadvantages": "Disadvantages",
    "价格": "Price",
    "function": "Function",
    "最强": "Strongest",
    "强": "Strong",
    "中": "Medium",
    "弱": "Weak",
    "Limited": "Limited",
    "None": "None",
    "✅": "Yes",

    # Specific terms
    "关键词": "Keywords",
    "线索管理": "Lead Management",
    "销售automation": "Sales Automation",
    "营销automation": "Marketing Automation",
    "Free版": "Free Version",
    "强大": "Powerful",
    "性价比": "Cost-effective",
    "企业级": "Enterprise-level",
    "中小企业首选": "Small Business First Choice",
    "中小企业负担重": "Heavy burden for small business",
    "中小企业友好": "Small Business Friendly",
    "中小企业需要": "Small business needs",
    "中小企业建议": "Small business recommendation",

    # CRM specific
    "客户关系": "Customer Relationship",
    "线索追踪": "Lead Tracking",
    "销售流程": "Sales Process",
    "客户沟通": "Customer Communication",
    "智能管理": "Intelligent Management",
    "自动提醒": "Automatic Reminders",
    "data analysis": "Data Analysis",

    # Competitor analysis
    "竞品分析": "Competitor Analysis",
    "竞争对手": "Competitors",
    "关键词策略": "Keyword Strategy",
    "广告投放": "Ad Placement",
    "市场份额": "Market Share",
    "智能监测": "Intelligent Monitoring",
    "策略分析": "Strategy Analysis",
    "市场洞察": "Market Insights",
    "关键词分析": "Keyword Analysis",
    "广告分析": "Ad Analysis",
    "流量分析": "Traffic Analysis",
    "外链分析": "Backlink Analysis",
    "竞品关键词": "Competitor Keywords",
    "SEO分析": "SEO Analysis",
    "广告研究": "Ad Research",
    "流量洞察": "Traffic Insights",
    "广告竞品": "Ad Competitors",
    "价格亲民": "Affordable Price",
    "历史数据长": "Long Historical Data",
    "数据量不如": "Data volume less than",
    "市场份额洞察": "Market Share Insights",
    "用户行为": "User Behavior",
    "行业洞察": "Industry Insights",
    "竞品SEO": "Competitor SEO",
    "数据更新快": "Fast Data Updates",
    "关键词竞品选": "For keyword competitors choose",
    "广告竞品选": "For ad competitors choose",
    "流量分析选": "For traffic analysis choose",
    "外链竞品选": "For backlink competitors choose",
    "入门": "Entry-level",
    "深度": "Deep",
    "组合最优": "Best combination",

    # Content marketing
    "内容营销": "Content Marketing",
    "持续产出内容": "Continuously produce content",
    "内容规划": "Content Planning",
    "多channel发布": "Multi-channel Publishing",
    "effectiveness分析": "Effectiveness Analysis",
    "智能规划": "Intelligent Planning",
    "自动发布": "Automatic Publishing",
    "effectiveness追踪": "Effectiveness Tracking",
    "内容日历": "Content Calendar",
    "团队协作": "Team Collaboration",
    "内容发现": "Content Discovery",
    "AI recommendation": "AI Recommendation",
    "内容审批": "Content Approval",
    "审批体验好": "Good Approval Experience",
    "协作流畅": "Smooth Collaboration",
    "分析function": "Analysis Function",
    "内容发现None": "No Content Discovery",
    "营销automation选": "For marketing automation choose",
    "内容日历选": "For content calendar choose",
    "内容发现选": "For content discovery choose",
    "内容审批选": "For content approval choose",

    # Email marketing
    "邮件营销": "Email Marketing",
    "触达客户": "Reach Customers",
    "发送邮件": "Send Emails",
    "automation营销": "Automation Marketing",
    "追踪effectiveness": "Track Effectiveness",
    "智能发送": "Smart Sending",
    "personalization内容": "Personalized Content",
    "分析effectiveness": "Analyze Effectiveness",
    "邮件发送": "Email Sending",
    "短信营销": "SMS Marketing",
    "automation最强": "Strongest Automation",
    "模板库": "Template Library",
    "分析报告": "Analysis Reports",
    "模板最多": "Most Templates",
    "界面友好": "User-friendly Interface",
    "入门simple": "Simple Entry",
    "品牌知名": "Well-known Brand",
    "价格随联系人涨": "Price increases with contacts",
    "automation不如": "Automation less than",
    "邮件+CRM+营销automation一体": "Email + CRM + Marketing Automation Integrated",
    "行为追踪": "Behavior Tracking",
    "functioncomprehensive": "Comprehensive Function",
    "CRM一体": "CRM Integrated",
    "价格较高": "Higher Price",
    "学习曲线陡峭": "Steep Learning Curve",
    "模板不如": "Templates less than",
    "邮件+短信营销": "Email + SMS Marketing",
    "价格transparent": "Transparent Price",
    "短信营销独特": "Unique SMS Marketing",
    "functioncomprehensive": "Comprehensive Function",
    "模板不如": "Templates less than",
    "专注创作者": "Focus on Creators",
    "simple易用": "Simple and Easy to Use",
    "标签系统好": "Good Tag System",
    "function较Basic": "Basic Function",
    "分析较弱": "Weak Analysis",
    "模板少": "Few Templates",
    "创作者友好": "Creator Friendly",
    "模板需求": "Template Needs",
    "创作者": "Creators",
    "短信+邮件": "SMS + Email",
    "模板rich选": "For rich templates choose",
    "automation最强选": "For strongest automation choose",
    "短信营销选": "For SMS marketing choose",
    "创作者选": "For creators choose",

    # Customer support
    "客户支持": "Customer Support",
    "客户Yes": "Customer Support",
    "Yeschallenges": "Support Challenges",
    "提供客户Yes": "Provide Customer Support",
    "即时聊天": "Instant Chat",
    "问题追踪": "Issue Tracking",
    "知识库": "Knowledge Base",
    "AI客服工具": "AI Customer Service Tools",
    "自动回复": "Auto Reply",
    "智能路由": "Smart Routing",
    "知识库管理": "Knowledge Base Management",
    "AI聊天": "AI Chat",
    "客服工单": "Service Tickets",
    "聊天": "Chat",
    "分析": "Analysis",
    "客服工单最强": "Strongest Service Tickets",
    "企业级": "Enterprise-level",
    "集成多": "Many Integrations",
    "AIfunction需高级版": "AI Function Requires Premium",
    "AI机器人": "AI Robot",
    "Free版可用": "Free Version Available",
    "高级function需升级": "Premium Function Requires Upgrade",
    "集成少于": "Less Integrations than",
    "简洁客服平台": "Simple Customer Service Platform",
    "邮箱客服专业": "Professional Email Support",
    "体验流畅": "Smooth Experience",
    "邮箱客服": "Email Support",
    "简洁体验": "Simple Experience",
    "邮箱客服专业": "Professional Email Support",
    "体验简洁": "Simple Experience",
    "聊天function弱": "Weak Chat Function",
    "工单不如": "Tickets less than",
    "中小企业首选": "Small Business First Choice",
    "AI聊天选": "For AI chat choose",
    "工单管理选": "For ticket management choose",
    "邮箱客服选": "For email support choose",
    "客服": "Customer Service",

    # Advertising
    "广告优化": "Advertising Optimization",
    "广告投放": "Ad Placement",
    "efficient投放广告": "Efficient Ad Placement",
    "precise定位": "Precise Targeting",
    "预算控制": "Budget Control",
    "ROI追踪": "ROI Tracking",
    "AI广告工具": "AI Ad Tools",
    "智能投放": "Smart Placement",
    "自动optimization": "Automatic Optimization",
    "effectiveness分析": "Effectiveness Analysis",
    "AI optimization": "AI Optimization",
    "搜索广告": "Search Ads",
    "社交广告": "Social Ads",
    "视觉广告": "Visual Ads",
    "跨平台广告投放": "Cross-platform Ad Placement",
    "重定向广告": "Retargeting Ads",
    "重定向专业": "Professional Retargeting",
    "AIfunctionLimited": "Limited AI Function",
    "流量不如": "Traffic less than",
    "搜索流量最大": "Largest Search Traffic",
    "AI optimization好": "Good AI Optimization",
    "竞争激烈": "Intense Competition",
    "成本较高": "Higher Cost",
    "人群precise": "Precise Audience",
    "视觉广告好": "Good Visual Ads",
    "仅Meta平台": "Only Meta Platform",
    "隐私政策影响": "Privacy Policy Impact",
    "成本上涨": "Cost Increase",
    "跨平台覆盖": "Cross-platform Coverage",
    "价格transparent": "Transparent Price",
    "成本较低": "Lower Cost",
    "竞争较小": "Less Competition",
    "Office用户precise": "Precise Office Users",
    "流量较小": "Smaller Traffic",
    "市场份额低": "Low Market Share",
    "最佳scenarios": "Best Scenarios",
    "搜索广告选": "For search ads choose",
    "社交广告选": "For social ads choose",
    "跨平台选": "For cross-platform choose",
    "低成本选": "For low cost choose",
    "组合最优": "Best combination",

    # Common verbs/adjectives
    "需要": "Need",
    "能": "Can",
    "最": "Most/Best",
    "好": "Good",
    "如": "Like/As",
    "比": "Compare",
    "选": "Choose",
    "建议": "Recommend",
    "贵": "Expensive",
    "便宜": "Cheap/Affordable",
    "简单": "Simple",
    "复杂": "Complex",
    "快": "Fast",
    "慢": "Slow",
    "强": "Strong",
    "弱": "Weak",
    "多": "Many",
    "少": "Few",
    "大": "Large",
    "小": "Small",
    "高": "High",
    "低": "Low",
    "新": "New",
    "旧": "Old",
    "全": "Complete/Full",
    "不全": "Incomplete",
}

def translate_text(text):
    """Translate Chinese text to English using mapping dictionary."""
    result = text
    for chinese, english in TRANSLATIONS.items():
        result = result.replace(chinese, english)
    return result

def process_file(filepath):
    """Process a single JSON file and translate Chinese content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Translate title
    if data.get('title'):
        data['title'] = translate_text(data['title'])

    # Translate description
    if data.get('description'):
        data['description'] = translate_text(data['description'])

    # Translate content
    if data.get('content'):
        data['content'] = translate_text(data['content'])

    # Translate seo_keywords if needed
    if data.get('seo_keywords'):
        data['seo_keywords'] = [translate_text(kw) for kw in data['seo_keywords']]

    return data

def main():
    directory = '/Users/gejiayu/owner/seo/data/ai-marketing'

    files_processed = 0
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            data = process_file(filepath)

            # Write back to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            files_processed += 1
            print(f"Processed: {filename}")

    print(f"\nTotal files processed: {files_processed}")

if __name__ == '__main__':
    main()