#!/usr/bin/env python3
"""
Batch translate English JSON files to Chinese for pSEO project
Processes customer-support-tools and construction-contractor-tools directories
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

# Translation mappings for common terms
TERM_MAPPINGS = {
    # Customer Support Terms
    "customer service": "客服",
    "support": "支持",
    "agent": "客服",
    "platform": "平台",
    "software": "软件",
    "tools": "工具",
    "analytics": "分析",
    "management": "管理",
    "monitoring": "监控",
    "automation": "自动化",
    "integration": "整合",
    "tracking": "跟踪",
    "performance": "绩效",
    "metrics": "指标",
    "dashboard": "仪表板",
    "reporting": "报告",
    "chat": "聊天",
    "chatbot": "聊天机器人",
    "ticket": "工单",
    "call center": "呼叫中心",
    "live chat": "在线聊天",
    "help desk": "帮助台",
    "CRM": "客户关系管理",
    "email": "邮件",
    "social media": "社交媒体",
    "feedback": "反馈",
    "survey": "调查",
    "customer satisfaction": "客户满意度",
    "response time": "响应时间",
    "resolution": "解决",
    "workflow": "工作流",
    "knowledge base": "知识库",
    "self-service": "自助服务",
    "remote": "远程",
    "cobrowsing": "协作浏览",
    "screen sharing": "屏幕共享",
    "video support": "视频支持",

    # Construction Terms
    "construction": "建筑",
    "contractor": "承包商",
    "project": "项目",
    "building": "建筑",
    "site": "现场",
    "safety": "安全",
    "quality": "质量",
    "budget": "预算",
    "cost": "成本",
    "estimate": "估算",
    "bid": "投标",
    "scheduling": "调度",
    "document": "文档",
    "blueprint": "蓝图",
    "BIM": "建筑信息模型",
    "3D": "三维",
    "equipment": "设备",
    "material": "材料",
    "inventory": "库存",
    "subcontractor": "分包商",
    "vendor": "供应商",
    "compliance": "合规",
    "inspection": "检查",
    "punch list": "缺陷清单",
    "RFI": "信息请求",
    "change order": "变更单",
    "daily log": "日志",
    "field": "现场",
    "drone": "无人机",
    "mobile": "移动",
    "warehouse": "仓库",
    "waste": "废弃物",
    "training": "培训",
    "certification": "认证",
    "hoisting": "起重",
    "crane": "起重机",
    "excavation": "挖掘",
    "foundation": "基础",
    "concrete": "混凝土",
    "steel": "钢材",
    "roofing": "屋顶",
    "plumbing": "管道",
    "electrical": "电气",
    "HVAC": "暖通空调",
    "energy": "能源",
    "environmental": "环境",
    "permits": "许可证",
    "regulatory": "监管",
    "OSHA": "职业安全与健康管理局",
    "insurance": "保险",
    "bond": "担保",
    "financial": "财务",
    "accounting": "会计",
    "invoicing": "开票",
    "labor": "劳动力",
    "crew": "团队",
    "manpower": "人力",
    "drug testing": "药物检测",
    "background check": "背景调查",

    # General Terms
    "best": "最佳",
    "top": "顶级",
    "review": "评测",
    "comparison": "对比",
    "guide": "指南",
    "features": "功能",
    "benefits": "优势",
    "advantages": "优点",
    "disadvantages": "缺点",
    "implementation": "实施",
    "deployment": "部署",
    "ROI": "投资回报",
    "efficiency": "效率",
    "productivity": "生产力",
    "collaboration": "协作",
    "communication": "沟通",
    "workflow": "工作流程",
    "2026": "2026年",
}

def translate_title(title: str) -> str:
    """Translate title with key term replacements"""
    zh_title = title
    # Apply term mappings
    for en_term, zh_term in TERM_MAPPINGS.items():
        zh_title = zh_title.replace(en_term, zh_term)
    return zh_title

def translate_description(description: str) -> str:
    """Translate description maintaining CTA structure"""
    zh_desc = description
    for en_term, zh_term in TERM_MAPPINGS.items():
        zh_desc = zh_desc.replace(en_term, zh_term)
    return zh_desc

def translate_content(content: str) -> str:
    """Translate HTML content preserving structure"""
    zh_content = content
    # Translate key terms while preserving HTML structure
    for en_term, zh_term in TERM_MAPPINGS.items():
        zh_content = zh_content.replace(en_term, zh_term)
    return zh_content

def translate_keywords(keywords: List[str]) -> List[str]:
    """Translate SEO keywords array"""
    zh_keywords = []
    for keyword in keywords:
        zh_keyword = keyword
        for en_term, zh_term in TERM_MAPPINGS.items():
            zh_keyword = zh_keyword.replace(en_term, zh_term)
        zh_keywords.append(zh_keyword)
    return zh_keywords

def translate_pros_cons(pros_cons: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Translate pros and cons arrays"""
    zh_pros_cons = {"pros": [], "cons": []}
    for pro in pros_cons.get("pros", []):
        zh_pro = pro
        for en_term, zh_term in TERM_MAPPINGS.items():
            zh_pro = zh_pro.replace(en_term, zh_term)
        zh_pros_cons["pros"].append(zh_pro)
    for con in pros_cons.get("cons", []):
        zh_con = con
        for en_term, zh_term in TERM_MAPPINGS.items():
            zh_con = zh_con.replace(en_term, zh_term)
        zh_pros_cons["cons"].append(zh_con)
    return zh_pros_cons

def translate_faq(faq: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Translate FAQ question and answer pairs"""
    zh_faq = []
    for item in faq:
        zh_question = item["question"]
        zh_answer = item["answer"]
        for en_term, zh_term in TERM_MAPPINGS.items():
            zh_question = zh_question.replace(en_term, zh_term)
            zh_answer = zh_answer.replace(en_term, zh_term)
        zh_faq.append({"question": zh_question, "answer": zh_answer})
    return zh_faq

def process_file(input_path: Path, output_path: Path) -> bool:
    """Process single JSON file translation"""
    try:
        # Read English file
        with open(input_path, 'r', encoding='utf-8') as f:
            en_data = json.load(f)

        # Create Chinese translation
        zh_data = {
            "title": translate_title(en_data["title"]),
            "description": translate_description(en_data["description"]),
            "content": translate_content(en_data["content"]),
            "seo_keywords": translate_keywords(en_data["seo_keywords"]),
            "slug": en_data["slug"],
            "published_at": en_data["published_at"],
            "author": en_data["author"],
            "language": "zh-CN",
            "canonical_link": f"https://www.housecar.life/zh/posts/{en_data['slug']}",
            "alternate_links": en_data.get("alternate_links", {
                "en-US": f"https://www.housecar.life/posts/{en_data['slug']}",
                "zh-CN": f"https://www.housecar.life/zh/posts/{en_data['slug']}"
            })
        }

        # Translate optional fields
        if "pros_and_cons" in en_data:
            zh_data["pros_and_cons"] = translate_pros_cons(en_data["pros_and_cons"])
        if "faq" in en_data:
            zh_data["faq"] = translate_faq(en_data["faq"])

        # Write Chinese file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(zh_data, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def main():
    """Process all English JSON files in both directories"""
    base_dir = Path("/Users/gejiayu/owner/seo/data")

    # Process customer-support-tools
    cs_dir = base_dir / "customer-support-tools"
    cs_files = [f for f in cs_dir.glob("*.json") if not f.name.endswith(".zh.json")]

    # Process construction-contractor-tools
    cc_dir = base_dir / "construction-contractor-tools"
    cc_files = [f for f in cc_dir.glob("*.json") if not f.name.endswith(".zh.json")]

    total_files = len(cs_files) + len(cc_files)
    print(f"Total files to process: {total_files}")
    print(f"customer-support-tools: {len(cs_files)}")
    print(f"construction-contractor-tools: {len(cc_files)}")

    success_count = 0
    error_count = 0

    # Process customer-support-tools files
    for input_file in cs_files:
        output_file = input_file.parent / f"{input_file.stem}.zh.json"
        if process_file(input_file, output_file):
            success_count += 1
            print(f"✓ {input_file.name}")
        else:
            error_count += 1

    # Process construction-contractor-tools files
    for input_file in cc_files:
        output_file = input_file.parent / f"{input_file.stem}.zh.json"
        if process_file(input_file, output_file):
            success_count += 1
            print(f"✓ {input_file.name}")
        else:
            error_count += 1

    print(f"\n✅ Successfully processed: {success_count}/{total_files}")
    print(f"❌ Errors: {error_count}")

if __name__ == "__main__":
    main()