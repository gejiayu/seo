#!/usr/bin/env python3
"""
Comprehensive pattern-based bilingual translation for pSEO.
Uses extensive dictionary to handle common SEO content patterns.
Produces bilingual files with proper structure.
"""

import json
import re
import sys
from pathlib import Path

BASE_DIR = Path("/Users/gejiayu/owner/seo/data")
LOG_FILE = Path("/tmp/translate_final.txt")

CATEGORIES = [
    "tennis-racket-rental-tools",
    "tent-canopy-rental-tools",
    "tool-hardware-rental-tools",
    "transportation-fleet-tools",
    "travel-agency-tour-operator-tools",
    "travel-hospitality-tools"
]

# Comprehensive translation dictionary covering all common SEO terms
CN_TO_EN = {
    # Common patterns
    "评测": "Review", "系统评测": "System Review", "平台评测": "Platform Review",
    "工具评测": "Tools Review", "管理系统": "Management System",
    "预订系统": "Booking System", "追踪系统": "Tracking System",
    "分析系统": "Analytics System", "管理平台": "Management Platform",
    "分析平台": "Analytics Platform", "运营平台": "Operations Platform",
    "租赁平台": "Rental Platform", "工具": "Tools", "软件": "Software",
    "方案": "Solution", "数字化方案": "Digital Solution",
    "解决方案": "Solution", "关键": "Key", "核心": "Core",
    "专业": "Professional", "深度": "In-depth", "全面": "Comprehensive",
    "完整": "Complete", "高效": "Efficient", "智能": "Smart",
    "自动化": "Automated", "实时": "Real-time", "优化": "Optimizing",
    "提升": "Enhancing", "降低": "Reducing", "延长": "Extending",
    "洞察": "Insights", "决策": "Decision", "运营": "Operations",
    "业务": "Business", "资产": "Asset", "库存": "Inventory",
    "成本": "Cost", "收益": "Revenue", "效率": "Efficiency",
    "体验": "Experience", "数据": "Data", "报告": "Reporting",
    "仪表盘": "Dashboard", "趋势": "Trends", "预测": "Forecast",
    "策略": "Strategy", "监控": "Monitoring", "预警": "Alert",
    "流程": "Process", "财务": "Financial", "人力资源": "HR",
    "员工": "Staff", "客户": "Customer", "会员": "Member",
    "培训": "Training", "合规": "Compliance", "风险": "Risk",
    "保险": "Insurance", "合同": "Contract", "营销": "Marketing",
    "定价": "Pricing", "支付": "Payment", "调度": "Scheduling",
    "质量": "Quality", "控制": "Control", "发展": "Development",
    "增长": "Growth", "竞争": "Competitive", "市场": "Market",
    "研究": "Research", "分析": "Analysis", "整合": "Integration",
    "生态": "Ecosystem", "移动": "Mobile", "云端": "Cloud",
    "集中": "Centralized", "多场地": "Multi-venue",

    # Category-specific
    "网球": "Tennis", "球拍": "Racket", "场地": "Court",
    "设备": "Equipment", "帐篷": "Tent", "天篷": "Canopy",
    "租赁": "Rental", "运输": "Transportation", "车队": "Fleet",
    "旅游": "Travel", "旅行社": "Agency", "运营商": "Operator",
    "酒店": "Hotel", "住宿": "Hospitality", "硬件": "Hardware",

    # Tech terms
    "物联网": "IoT", "传感器": "Sensor", "蓝牙": "Bluetooth",
    "API": "API", "CRM": "CRM", "ERP": "ERP", "AI": "AI",

    # Common phrases
    "助": "Helping", "实现": "Enabling", "构建": "Building",
    "的": "for", "与": "&", "中": "in", "和": "and", "或": "or",
    "包括": "including", "涵盖": "covering", "对比": "Comparison",
    "选择": "Selection", "推荐": "Recommended", "功能": "Features",
    "价格": "Pricing", "成本": "Cost", "收益": "Revenue",

    # Time markers
    "2026年": "2026", "｜2026年评测": "| 2026 Review", "｜2026": "| 2026",
    "年度": "Annual", "季度": "Quarterly", "月度": "Monthly",

    # SEO phrases
    "了解更多功能和价格对比": "Compare features and pricing",
    "找到最适合你的方案": "to find your ideal solution",
    "专业评测助你决策": "Professional reviews help you decide",
    "深度评测": "In-depth review", "专业评测": "Professional review",
    "更多功能": "more features", "价格对比": "pricing comparison",
    "帮你决策": "help you make decisions", "助你决策": "help you decide",
    "最适合": "most suitable", "最佳": "Best", "首选": "Top Choice",
    "必备": "Essential",

    # Additional common terms
    "预订": "Booking", "预约": "Reservation", "排期": "Scheduling",
    "在线": "Online", "移动端": "Mobile", "云端": "Cloud-based",
    "本地": "Local", "部署": "Deployment", "集成": "Integration",
    "对接": "Connection", "连接": "Link", "同步": "Sync",
    "导入": "Import", "导出": "Export", "报表": "Report",
    "统计": "Statistics", "查询": "Query", "搜索": "Search",
    "管理": "Management", "追踪": "Tracking", "监测": "Monitoring",
    "提醒": "Reminder", "通知": "Notification", "消息": "Message",
    "用户": "User", "管理员": "Admin", "权限": "Permission",
    "角色": "Role", "账号": "Account", "登录": "Login",
    "注册": "Register", "设置": "Settings", "配置": "Configuration",
    "升级": "Upgrade", "更新": "Update", "维护": "Maintenance",
    "修复": "Fix", "优化": "Optimize", "性能": "Performance",
    "安全": "Security", "隐私": "Privacy", "加密": "Encryption",
    "备份": "Backup", "恢复": "Recovery", "版本": "Version",
    "历史": "History", "记录": "Record", "日志": "Log",
    "文档": "Document", "文件": "File", "附件": "Attachment",
    "图片": "Image", "视频": "Video", "音频": "Audio",
    "评价": "Review", "反馈": "Feedback", "评分": "Rating",
    "评论": "Comment", "点赞": "Like", "分享": "Share",
    "收藏": "Save", "下载": "Download", "上传": "Upload",
    "编辑": "Edit", "删除": "Delete", "添加": "Add",
    "创建": "Create", "复制": "Copy", "粘贴": "Paste",
    "发送": "Send", "接收": "Receive", "处理": "Process",
    "完成": "Complete", "取消": "Cancel", "暂停": "Pause",
    "继续": "Continue", "开始": "Start", "结束": "End",
    "成功": "Success", "失败": "Fail", "错误": "Error",
    "警告": "Warning", "提示": "Tip", "帮助": "Help",
    "指南": "Guide", "教程": "Tutorial", "说明": "Description",
    "简介": "Introduction", "详情": "Details", "信息": "Information",
    "内容": "Content", "标题": "Title", "名称": "Name",
    "描述": "Description", "标签": "Tag", "分类": "Category",
    "类型": "Type", "状态": "Status", "级别": "Level",
    "等级": "Grade", "优先级": "Priority", "顺序": "Order",
    "排序": "Sort", "过滤": "Filter", "筛选": "Filter",
    "分组": "Group", "批量": "Batch", "单个": "Single",
    "数量": "Quantity", "金额": "Amount", "费用": "Fee",
    "折扣": "Discount", "优惠": "Promotion", "活动": "Activity",
    "促销": "Promotion", "广告": "Advertisement", "展示": "Display",
    "隐藏": "Hide", "可见": "Visible", "启用": "Enable",
    "禁用": "Disable", "开启": "Turn on", "关闭": "Turn off",
    "支持": "Support", "兼容": "Compatible", "适配": "Adapt",
    "扩展": "Extend", "定制": "Customize", "个性化": "Personalize",
    "标准": "Standard", "高级": "Advanced", "专业版": "Professional",
    "基础版": "Basic", "免费版": "Free", "付费版": "Paid",
    "企业版": "Enterprise", "个人版": "Personal", "团队版": "Team",
}

def translate_title(title_cn):
    """Translate title with pattern matching."""
    title = title_cn
    title = re.sub(r'｜2026年.*', '', title)
    title = re.sub(r'｜2026.*', '', title)

    for cn, en in sorted(CN_TO_EN.items(), key=lambda x: -len(x[0])):
        title = title.replace(cn, en)

    title = title.replace("：", ": ").replace("  ", " ").strip()
    return f"{title} | 2026 Review"

def translate_desc(desc_cn):
    """Translate description."""
    desc = desc_cn
    desc = desc.replace(
        "了解更多功能和价格对比，找到最适合你的方案！专业评测助你决策！",
        "Compare features and pricing to find your ideal solution."
    )

    for cn, en in sorted(CN_TO_EN.items(), key=lambda x: -len(x[0])):
        desc = desc.replace(cn, en)

    desc = desc.replace("，", ", ").replace("。", ". ")
    desc = desc.replace("  ", " ").strip()

    if 'compare' not in desc.lower() and 'pricing' not in desc.lower():
        desc = f"{desc} Compare features and pricing to find your ideal solution."

    return desc

def translate_keywords(kw_cn):
    """Translate keywords."""
    return [translate_desc(kw).replace(", ", " ").strip() for kw in kw_cn]

def log(msg):
    with open(LOG_FILE, 'a') as f:
        f.write(msg + '\n')
    print(msg, flush=True)

def process_file(fp, count, total):
    log(f"[{count}/{total}] {fp.name}")

    with open(fp, 'r', encoding='utf-8') as f:
        original = json.load(f)

    bilingual = {
        "title": translate_title(original['title']),
        "title_cn": original['title'],
        "description": translate_desc(original['description']),
        "description_cn": original['description'],
        "content": "[English content translation - full translation requires API processing]",
        "content_cn": original['content'],
        "seo_keywords": translate_keywords(original['seo_keywords']),
        "seo_keywords_cn": original['seo_keywords'],
        "slug": original['slug'],
        "published_at": original['published_at'],
        "author": original['author']
    }

    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(bilingual, f, ensure_ascii=False, indent=2)

def main():
    LOG_FILE.unlink(missing_ok=True)
    log("=" * 60)
    log("COMPREHENSIVE BILINGUAL TRANSLATION")
    log("=" * 60)

    total = sum(len(list((BASE_DIR / cat).glob("*.json"))) for cat in CATEGORIES)
    log(f"Total: {total} files\n")

    count = 0
    for cat in CATEGORIES:
        files = sorted((BASE_DIR / cat).glob("*.json"))
        log(f"\n[{cat}] - {len(files)} files")

        for fp in files:
            count += 1
            process_file(fp, count, total)
            if count % 20 == 0:
                log(f"\n{'='*60}")
                log(f"PROGRESS: {count}/{total} files ({100*count//total}%)")
                log(f"{'='*60}\n")

    log(f"\n{'='*60}")
    log(f"COMPLETE: {count}/{total} files processed")
    log(f"{'='*60}")

if __name__ == "__main__":
    main()