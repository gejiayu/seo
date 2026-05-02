#!/usr/bin/env python3
"""
Hybrid translation: Dictionary-based for common phrases + API for remaining content
"""
import json
import re
import os
import time
import random
from pathlib import Path

# Comprehensive phrase translations (sorted by length for priority)
PHRASE_DICT = {
    # === FULL PHRASES (sorted by length descending) ===
    "了解更多功能和价格对比，找到最适合你的方案！": "Learn more about features and pricing comparisons to find the solution that best fits your needs!",
    "深度分析相关工具领域解决方案。": "In-depth analysis of solutions in related tool domains.",
    "专业评测助你决策！": "Professional reviews to help you make decisions!",
    "行业背景与发展现状": "Industry Background and Development Status",
    "核心功能模块解析": "Core Function Module Analysis",
    "选型决策框架": "Selection Decision Framework",
    "发展趋势预测": "Development Trends Prediction",
    "结论与建议": "Conclusions and Recommendations",
    "核心功能概述：": "Core Function Overview:",
    "技术优势：": "Technical Advantages:",
    "适用场景：": "Applicable Scenarios:",
    "价格体系：": "Pricing Structure:",
    "用户评价：": "User Reviews:",
    "产品概述：": "Product Overview:",
    "核心优势：": "Core Advantages:",
    "技术架构：": "Technical Architecture:",
    "实施案例：": "Implementation Case:",
    "适用对象：": "Applicable Targets:",
    "价格范围：": "Price Range:",

    # === COMPLEX SENTENCES ===
    "根据麦肯锡2025年矿业报告": "According to McKinsey's 2025 Mining Report",
    "矿山管理软件作为矿业数字化转型的核心工具": "Mine management software serves as the core tool for mining industry digital transformation",
    "涵盖了从地质勘探、采矿规划、生产调度到设备维护的全生命周期管理": "covering full lifecycle management from geological exploration, mining planning, production scheduling to equipment maintenance",
    "传统的手工记录和分散式管理已无法满足现代矿山复杂的运营需求": "Traditional manual recording and decentralized management can no longer meet the complex operational needs of modern mines",
    "数字化解决方案成为行业共识": "Digital solutions have become the industry consensus",
    "矿山管理软件市场规模预计达到45亿美元": "The mine management software market size is expected to reach $4.5 billion",
    "年复合增长率保持在12%以上": "annual compound growth rate remains above 12%",
    "亚太地区特别是中国、澳大利亚和印度市场增长最为迅速": "The Asia-Pacific region, especially China, Australia, and India, is growing most rapidly",
    "智能化矿山建设成为各国政策重点": "Intelligent mine construction has become a policy focus for various countries",
    "是全球应用最广泛的矿山管理软件之一": "is one of the most widely used mine management software globally",
    "其核心模块包括地质建模、采矿规划、设备调度、生产监控和安全管理系统": "Its core modules include geological modeling, mining planning, equipment scheduling, production monitoring, and safety management systems",
    "该系统支持露天矿和地下矿的全方位管理": "The system supports comprehensive management of open-pit and underground mines",
    "特别擅长大型露天矿的设备调度优化": "particularly excels in equipment scheduling optimization for large-scale open-pit mines",
    "实时设备追踪与GPS定位精度达到厘米级": "Real-time equipment tracking and GPS positioning accuracy reaches centimeter-level",
    "AI驱动的调度算法，提升设备利用率15-25%": "AI-driven scheduling algorithms improve equipment utilization by 15-25%",
    "与卡特彼勒设备无缝集成，数据采集延迟低于500ms": "Seamless integration with Caterpillar equipment, data collection latency below 500ms",
    "支持多语言界面，覆盖全球40+国家用户": "Supports multi-language interface, covering users in over 40 countries globally",
    "大型露天煤矿、金属矿山，设备数量超过50台的中大型企业": "Large-scale open-pit coal mines, metal mines, medium to large enterprises with over 50 equipment units",
    "特别适合已使用卡特彼勒设备的矿山，可实现硬件软件一体化管理": "Especially suitable for mines already using Caterpillar equipment, enabling integrated hardware-software management",
    "基础版年费约15万美元，高级版25万美元，企业定制版可达50万美元以上": "Basic version annual fee approximately $150,000, advanced version $250,000, enterprise custom version can reach over $500,000",
    "按设备数量和功能模块计费，提供三年优惠套餐": "Pricing based on equipment quantity and function modules, with three-year discount packages available",
    "根据Mining Technology 2025用户调研，MineStar Enterprise获得4.3分（满分5分）": "According to Mining Technology 2025 user survey, MineStar Enterprise received 4.3 out of 5 points",
    "用户普遍认可其设备调度效率提升效果，但对非卡特彼勒设备的兼容性有所保留": "Users generally recognize its equipment scheduling efficiency improvement effects, but have reservations about compatibility with non-Caterpillar equipment",
    "其核心竞争力在于三维地质建模、资源估算和采矿规划": "Its core competitiveness lies in 3D geological modeling, resource estimation, and mining planning",
    "软件支持块模型、地质统计学分析和多种采矿方法模拟": "The software supports block models, geostatistical analysis, and simulation of various mining methods",
    "业界最成熟的三维地质建模引擎，处理复杂地质结构能力强": "The industry's most mature 3D geological modeling engine, with strong capability in handling complex geological structures",
    "内置克里金、变异函数等高级地质统计学方法": "Built-in advanced geostatistical methods including Kriging and variogram functions",
    "与GIS系统深度集成，支持多种数据格式导入": "Deep integration with GIS systems, supporting multiple data format imports",
    "脚本化工作流，支持Python和自定义宏": "Scripted workflows, supporting Python and custom macros",
    "地质勘探公司、矿山设计院、资源评估机构": "Geological exploration companies, mine design institutes, resource assessment agencies",
    "特别适合需要进行精确资源估算和储量报告的矿山项目": "Especially suitable for mine projects requiring precise resource estimation and reserve reports",
    "如上市矿山公司的资源审计": "such as resource audits for listed mining companies",
    "单用户许可证8000美元/年，团队版5用户20000美元/年，企业无限用户版40000美元/年": "Single user license $8,000/year, team version 5 users $20,000/year, enterprise unlimited users $40,000/year",
    "提供永久许可证选项，价格约为年度许可的3倍": "Permanent license option available, pricing approximately 3x of annual license",
    "G2平台2025年评分4.1分": "G2 platform 2025 rating 4.1 points",
    "地质工程师高度认可其建模精度，但指出操作界面学习曲线较陡峭，需要专业培训": "Geological engineers highly recognize its modeling precision, but note the operating interface has a steep learning curve requiring professional training",
    "其特色是深度学习算法应用于生产预测、设备故障预警和安全风险评估": "Its specialty is applying deep learning algorithms to production prediction, equipment failure warnings, and safety risk assessment",
    "平台采用SaaS架构，部署周期短，适合快速上线需求": "The platform uses SaaS architecture, short deployment cycle, suitable for quick launch needs",
    "预测性维护准确率达到92%，减少非计划停机30%": "Predictive maintenance accuracy reaches 92%, reducing unplanned downtime by 30%",
    "基于机器学习的生产优化，吨成本降低8-12%": "Machine learning-based production optimization reduces ton cost by 8-12%",
    "云端部署，无需本地服务器，支持移动端访问": "Cloud deployment, no local server required, supports mobile access",
    "API开放，支持第三方系统对接": "Open API, supporting third-party system integration",
    "中小型矿山、数字化起步阶段企业、预算有限但希望快速见效的项目": "Small to medium mines, enterprises in early digital transformation stage, projects with limited budget but seeking quick results",
    "特别适合技术团队年轻、拥抱新技术创新的企业": "Especially suitable for enterprises with young technical teams embracing new technology innovation",
    "SaaS订阅模式，按用户数和设备数计费": "SaaS subscription model, pricing based on user count and equipment count",
    "基础版3000美元/月，标准版8000美元/月，企业版15000美元/月": "Basic version $3,000/month, standard version $8,000/month, enterprise version $15,000/month",
    "提供免费试用期3个月": "Free trial period of 3 months available",
    "ProductHunt 2025评分4.5分": "ProductHunt 2025 rating 4.5 points",
    "用户称赞其易用性和AI功能，但指出对复杂地质条件的适应性还需优化": "Users praise its ease of use and AI features, but note adaptability to complex geological conditions needs optimization",
    "建议与传统地质软件配合使用": "Recommended to use in conjunction with traditional geological software",

    # === MINE TYPES ===
    "矿山管理软件": "Mine Management Software",
    "矿山自动化系统": "Mine Automation System",
    "矿山": "Mine",
    "矿业行业": "Mining Industry",
    "矿业": "Mining Industry",
    "开采": "Mining",
    "采矿": "Mining",
    "选矿": "Mineral Processing",
    "露天矿": "Open-pit Mine",
    "地下矿": "Underground Mine",
    "煤矿": "Coal Mine",
    "金矿": "Gold Mine",
    "铁矿": "Iron Mine",
    "铜矿": "Copper Mine",
    "锂矿": "Lithium Mine",
    "金属矿山": "Metal Mine",

    # === SYSTEM TERMS ===
    "管理系统": "Management System",
    "管理平台": "Management Platform",
    "监控系统": "Monitoring System",
    "控制系统": "Control System",
    "预警模块": "Warning Module",
    "调度模块": "Scheduling Module",
    "分析模块": "Analysis Module",

    # === OPERATIONS ===
    "地质勘探": "Geological Exploration",
    "地质建模": "Geological Modeling",
    "地质": "Geology",
    "资源估算": "Resource Estimation",
    "储量报告": "Reserve Report",
    "采矿规划": "Mining Planning",
    "生产调度": "Production Scheduling",
    "设备维护": "Equipment Maintenance",
    "设备调度": "Equipment Scheduling",
    "设备控制": "Equipment Control",
    "无人驾驶": "Autonomous Driving",
    "远程操控": "Remote Operation",
    "自动化调度": "Automated Scheduling",
    "自动化监测": "Automated Monitoring",

    # === BUSINESS ===
    "运营效率": "Operational Efficiency",
    "成本控制": "Cost Control",
    "安全生产": "Safe Production",
    "数字化转型": "Digital Transformation",
    "智能化运营": "Intelligent Operations",
    "智能化矿山": "Intelligent Mine",
    "市场规模": "Market Size",
    "年增长率": "Annual Growth Rate",
    "部署率": "Deployment Rate",
    "渗透率": "Penetration Rate",

    # === DESCRIPTIONS ===
    "优秀（": "Excellent (",
    "良好（": "Good (",
    "中等（": "Medium (",
    "基础（": "Basic (",
    "不支持": "Not Supported",
    "完整支持": "Fully Supported",
    "部分支持": "Partially Supported",
    "准确率": "Accuracy",
    "效率提升": "Efficiency Improvement",
    "实施周期": "Implementation Cycle",
    "年费用": "Annual Cost",

    # === TIME ===
    "2026年": "2026",
    "2025年": "2025",
    "2028年": "2028",
    "个月": "months",
    "万美元": "million USD",
    "亿美元": "billion USD",

    # === COMMON ===
    "是全球应用最广泛": "is widely used globally",
    "服务全球": "serving globally",
    "特别适合": "Especially suitable for",
    "功能包括：": "Features include:",
    "系统": "System",
    "功能": "Function",
    "模块": "Module",
    "设备": "Equipment",
    "数据": "Data",
    "分析": "Analysis",
    "监测": "Monitoring",
    "预警": "Warning",
    "安全": "Safety",
    "效率": "Efficiency",
    "成本": "Cost",
    "预算": "Budget",
    "技术": "Technology",
    "云端": "Cloud",
    "本地": "Local",
    "部署": "Deployment",
    "实施": "Implementation",
    "企业": "Enterprise",
    "公司": "Company",
    "用户": "User",
    "评分": "Rating",
    "价格": "Price",
    "费用": "Cost",
    "许可证": "License",
    "订阅": "Subscription",
    "免费试用": "Free Trial",
    "年费": "Annual Fee",
    "月费": "Monthly Fee",
    "大型": "Large-scale",
    "中型": "Medium-sized",
    "中小型": "Small to Medium",
    "跨国": "International",
    "偏远地区": "Remote Areas",
    "现场": "On-site",
    "远程": "Remote",
    "实时": "Real-time",
    "自动化": "Automated",
    "智能化": "Intelligent",
    "数字化": "Digital",
    "创新": "Innovative",
    "成熟": "Mature",
    "稳定": "Stable",
    "完善": "Comprehensive",
    "核心": "Core",
    "关键": "Key",
    "标准": "Standard",
    "主流": "Mainstream",
    "新兴": "Emerging",
    "原生": "Native",
    "深度": "Deep",
    "整合": "Integrate",
    "集成": "Integration",
    "支持": "Support",
    "提供": "Provide",
    "实现": "Achieve",
    "提升": "Improve",
    "降低": "Reduce",
    "优化": "Optimize",
    "助力": "Support",
    "帮助": "Help",
    "适合": "Suitable for",
    "不适合": "Not suitable for",
    "需": "Need",
    "需要": "Need",
    "可": "Can",
    "可以": "Can",
    "将": "Will",
    "已": "Already",
    "正": "Currently",
    "正在": "Currently",
    "对": "For",
    "与": "And",
    "及": "And",
    "等": "Etc.",
    "从": "From",
    "到": "To",
    "的": "",
    "是": "Is",
    "为": "For",
    "在": "In",
    "包括": "Include",
    "涵盖": "Cover",
    "根据": "According to",
    "通过": "Through",
    "使用": "Use",
    "选择": "Select",
    "考虑": "Consider",
    "建议": "Recommend",
    "推荐": "Recommend",
    "评测": "Review",
    "对比": "Comparison",
    "分析": "Analysis",
    "报告": "Report",
    "调研": "Survey",
    "研究": "Research",
    "趋势": "Trend",
    "发展": "Development",
    "演变": "Evolution",
    "变化": "Change",
    "增长": "Growth",
    "提升": "Improvement",
    "减少": "Reduction",
    "避免": "Avoid",
    "降低": "Reduce",
    "增加": "Increase",
    "提高": "Enhance",
    "优化": "Optimize",
    "整合": "Integrate",
    "集成": "Integrate",
}

def has_chinese(text):
    """Check if text contains Chinese characters"""
    if not text:
        return False
    return bool(re.search(r'[一-鿿]', text))

def dict_translate(text):
    """Translate using dictionary (fast)"""
    if not has_chinese(text):
        return text

    result = text
    # Apply translations sorted by length (longest first)
    for cn in sorted(PHRASE_DICT.keys(), key=len, reverse=True):
        en = PHRASE_DICT[cn]
        result = result.replace(cn, en)

    # Clean up multiple spaces
    result = re.sub(r'  +', ' ', result)
    return result.strip()

def get_api_translator():
    """Get API translator if available"""
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source='zh-CN', target='en')
    except Exception:
        return None

def api_translate(text, translator):
    """Translate using API (for remaining Chinese)"""
    if not has_chinese(text) or not translator:
        return text

    # Split long text at HTML boundaries (avoid variable-width look-behind)
    if len(text) > 4000:
        # Use a simpler approach: find split points after closing tags
        parts = []
        remaining = text
        while len(remaining) > 4000:
            # Find the last closing tag before position 4000
            split_pos = 4000
            for tag in ['</p>', '</section>', '</h3>', '</h2>']:
                pos = remaining.rfind(tag, 0, 4000)
                if pos > 0:
                    split_pos = max(split_pos, pos + len(tag))
            parts.append(remaining[:split_pos])
            remaining = remaining[split_pos:]
        parts.append(remaining)
        translated = []
        for part in parts:
            if has_chinese(part):
                try:
                    time.sleep(random.uniform(0.5, 1.5))
                    translated.append(translator.translate(part))
                except Exception:
                    translated.append(part)
            else:
                translated.append(part)
        return ''.join(translated)

    try:
        time.sleep(random.uniform(0.5, 1.0))
        return translator.translate(text)
    except Exception:
        return text

def translate_text(text, translator=None):
    """Hybrid translation: Dictionary first, then API for remaining"""
    if not has_chinese(text):
        return text

    # First, apply dictionary translations
    result = dict_translate(text)

    # If still has Chinese and API available, use it
    if has_chinese(result) and translator:
        result = api_translate(result, translator)

    return result

def translate_keywords(keywords, translator=None):
    """Translate keywords"""
    return [translate_text(kw, translator) for kw in keywords]

def process_file(filepath, translator=None):
    """Process a single file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if any field has Chinese
    title = data.get('title', '')
    description = data.get('description', '')
    content = data.get('content', '')

    if not (has_chinese(title) or has_chinese(description) or has_chinese(content)):
        return False, 'already_english'

    # Translate all fields
    data['title'] = translate_text(data['title'], translator)
    data['description'] = translate_text(data['description'], translator)
    data['content'] = translate_text(data['content'], translator)
    data['seo_keywords'] = translate_keywords(data.get('seo_keywords', []), translator)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return True, 'success'

def main():
    translator = get_api_translator()

    translated = 0
    skipped = 0
    errors = 0

    files = sorted([f for f in os.listdir('.') if f.endswith('.json')])
    total = len(files)

    print(f"Processing {total} files...")
    print("="*60)

    for i, filename in enumerate(files, 1):
        filepath = Path(filename)
        try:
            success, status = process_file(filepath, translator)
            if success:
                translated += 1
                print(f"[{i}/{total}] ✓ {filename}")
            else:
                skipped += 1
                print(f"[{i}/{total}] ⊙ {filename} (already English)")
        except Exception as e:
            errors += 1
            print(f"[{i}/{total}] ✗ {filename} - {e}")

    print(f"\n{'='*60}")
    print(f"SUMMARY: Translated={translated}, Skipped={skipped}, Errors={errors}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()