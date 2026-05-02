#!/usr/bin/env python3
"""
Ultimate comprehensive translation for publishing-media-tools SEO content.
Uses massive phrase-level translation dictionary to produce proper English.
"""
import json
import re
from pathlib import Path

def translate_comprehensive(text):
    """Translate using comprehensive phrase-level mapping."""
    if not isinstance(text, str):
        return text

    if not re.search(r'[一-鿿]', text):
        return text

    # Massive phrase-level translation dictionary
    phrases = {
        # Complete titles patterns (priority)
        "学术排版工具终极评测：2026年十大学术文献排版平台助力学术出版": "Academic Typesetting Tools Ultimate Review: Top 10 Academic Document Formatting Platforms for 2026",
        "有声书制作工具终极指南：2026十大平台助力音频内容创作与分发": "Audiobook Production Tools Ultimate Guide: Top 10 Platforms Empowering Audio Content Creation and Distribution for 2026",

        # Common sentence patterns
        "市场规模预计达到": "market size is projected to reach",
        "年增长率保持在": "annual growth rate maintained at",
        "以上": "above",
        "行业面临": "industry faces",
        "核心挑战": "core challenges",
        "传统方法难以满足": "traditional methods struggle to meet",
        "现代需求": "modern requirements",
        "成为核心竞争力": "becomes a core competitive advantage",
        "选择合适的工具直接影响": "choosing the right tools directly impacts",
        "效率、成本与质量": "efficiency, cost, and quality",

        # Full section headers
        "一、行业特殊需求分析": "1. Industry-Specific Requirements Analysis",
        "二、十大平台深度评测": "2. Top 10 Platforms In-depth Review",
        "三、核心功能参数对比表": "3. Core Feature Comparison Table",
        "四、发展趋势": "4. Development Trends",
        "五、选型策略与实施路径": "5. Selection Strategy and Implementation Roadmap",

        # Requirements with proper phrasing
        "效率提升需求": "efficiency improvement requirements",
        "成本控制需求": "cost control requirements",
        "质量控制需求": "quality control requirements",
        "数据分析需求": "data analysis requirements",
        "需高效率处理": "requires high-efficiency processing",
        "需成本控制优化": "requires cost control optimization",
        "需高质量输出": "requires high-quality output",
        "需数据分析支持": "requires data analysis support",
        "工具需支持": "tools need to support",
        "自动化流程": "automated workflows",
        "成本分析管理": "cost analysis management",
        "质量检验功能": "quality inspection functions",
        "数据深度分析": "in-depth data analysis",

        # Platform descriptions - complete
        "专业级": "professional-grade",
        "核心功能": "core features",
        "自动化管理": "automated management",
        "成本优化分析支持": "cost optimization and analysis support",
        "质量检验深度化": "in-depth quality inspection",
        "价格：订阅制": "pricing: subscription-based",
        "特色：专业能力顶尖": "specialty: top-tier professional capabilities",
        "适合大型团队": "suitable for large teams",
        "适合中型团队": "suitable for medium-sized teams",
        "适合小型团队": "suitable for small teams",
        "性价比高": "high cost-effectiveness",
        "快速上手": "quick to start",

        # Complete table headers
        "平台名称": "Platform Name",
        "核心定位": "Core Positioning",
        "价格区间": "Price Range",
        "效率能力": "Efficiency Capability",
        "成本控制": "Cost Control",
        "质量保障": "Quality Assurance",
        "数据分析": "Data Analysis",

        # Complete trend statements
        "行业将呈现关键发展趋势": "The industry will exhibit key development trends",
        "AI驱动自动化": "AI-driven automation",
        "AI自动化覆盖率从": "AI automation coverage from",
        "提升至": "increases to",
        "效率提升": "efficiency improves by",
        "成本控制智能化": "intelligent cost control",
        "智能化成本控制覆盖率从": "intelligent cost control coverage from",
        "成本降低": "cost reduction by",
        "质量检验实时化": "real-time quality inspection",
        "实时质量检验覆盖率从": "real-time quality inspection coverage from",
        "质量提升": "quality improvement by",
        "数据分析深度化": "deep data analysis",
        "深度数据分析覆盖率从": "deep data analysis coverage from",
        "决策准确性提升": "decision accuracy improves by",

        # Complete selection strategy
        "团队应根据规模与需求选择工具": "Teams should select tools based on scale and requirements",
        "选择企业级平台": "choose enterprise-grade platforms",
        "选择专业级平台": "choose professional-grade platforms",
        "选择轻量级平台": "choose lightweight platforms",
        "月投入": "monthly investment of",
        "实施路径：先完成需求评估": "Implementation roadmap: first complete requirements assessment",
        "再试用核心工具": "then trial core tools",
        "最后规模化部署": "finally scale deployment",
        "预计效率提升": "expected efficiency improvement",
        "成本降低": "cost reduction",

        # Word-level translations for remaining content
        "全球": "global",
        "美元": "USD",
        "年": "year",
        "月": "month",
        "高": "high",
        "中": "medium",
        "低": "low",
        "工具": "tools",
        "平台": "platforms",
        "系统": "systems",
        "软件": "software",
        "方案": "solutions",
        "功能": "features",
        "服务": "services",
        "管理": "management",
        "编辑": "editing",
        "制作": "production",
        "分发": "distribution",
        "营销": "marketing",
        "推广": "promotion",
        "收益": "revenue",
        "成本": "cost",
        "效率": "efficiency",
        "质量": "quality",
        "数据": "data",
        "分析": "analysis",
        "智能": "intelligent",
        "自动化": "automated",
        "数字": "digital",
        "出版": "publishing",
        "学术": "academic",
        "文献": "documents",
        "排版": "typesetting",
        "录音": "recording",
        "音频": "audio",
        "有声书": "audiobook",
        "配音": "voiceover",
        "语音": "voice",
        "自然度": "naturalness",
        "渠道": "channels",
        "内容": "content",
        "创作": "creation",
        "作者": "author",
        "读者": "reader",
        "听众": "listener",
        "用户": "user",
        "团队": "team",
        "企业": "enterprise",
        "专业": "professional",
        "独立": "independent",
        "大型": "large",
        "中型": "medium-sized",
        "小型": "small",
        "基础": "basic",
        "高级": "advanced",
        "完整": "complete",
        "深度": "in-depth",
        "终极": "ultimate",
        "最佳": "best",
        "最优": "optimal",
        "核心": "core",
        "关键": "key",
        "主要": "main",
        "重要": "important",
        "特殊": "special",
        "需求": "requirements",
        "挑战": "challenges",
        "趋势": "trends",
        "发展": "development",
        "策略": "strategies",
        "方法": "methods",
        "技术": "technologies",
        "创新": "innovation",
        "突破": "breakthrough",
        "变革": "transformation",
        "行业": "industry",
        "市场": "market",
        "领域": "field",
        "细分": "segment",
        "规模": "scale",
        "范围": "scope",
        "程度": "extent",
        "阶段": "stage",
        "步骤": "steps",
        "流程": "processes",
        "环节": "phases",
        "节点": "nodes",
        "顺序": "sequence",
        "并行": "parallel",
        "同步": "synchronous",
        "异步": "asynchronous",
        "批量": "batch",
        "单个": "individual",
        "整体": "overall",
        "局部": "partial",
        "全部": "all",
        "部分": "part",
        "必要": "necessary",
        "可选": "optional",
        "必需": "required",
        "推荐": "recommended",
        "建议": "suggested",
        "提示": "tips",
        "说明": "descriptions",
        "解释": "explanations",
        "定义": "definitions",
        "概念": "concepts",
        "原理": "principles",
        "机制": "mechanisms",
        "算法": "algorithms",
        "模型": "models",
        "框架": "frameworks",
        "架构": "architectures",
        "结构": "structures",
        "组件": "components",
        "模块": "modules",
        "单元": "units",
        "元素": "elements",
        "对象": "objects",
        "属性": "attributes",
        "参数": "parameters",
        "变量": "variables",
        "常量": "constants",
        "因子": "factors",
        "指标": "indicators",
        "标准": "standards",
        "基准": "benchmarks",
        "参考": "references",
        "比较": "comparisons",
        "对比": "contrasts",
        "对照": "controls",
        "评价": "evaluations",
        "评估": "assessments",
        "测试": "tests",
        "验证": "validations",
        "确认": "confirmations",
        "检查": "inspections",
        "审核": "reviews",
        "审批": "approvals",
        "授权": "authorizations",
        "认证": "certifications",
        "许可": "licenses",
        "权利": "rights",
        "版权": "copyright",
        "知识产权": "intellectual property",
        "专利": "patents",
        "商标": "trademarks",
        "品牌": "brands",
        "声誉": "reputation",
        "影响力": "influence",
        "竞争力": "competitiveness",
        "驱动力": "driving force",
        "推动力": "propulsion",
        "阻力": "resistance",
        "障碍": "obstacles",
        "瓶颈": "bottlenecks",
        "限制": "limitations",
        "约束": "constraints",
        "边界": "boundaries",
        "空间": "spaces",
        "环境": "environments",
        "背景": "backgrounds",
        "场景": "scenarios",
        "案例": "cases",
        "示例": "examples",
        "样本": "samples",
        "模板": "templates",
        "原型": "prototypes",
        "实例": "instances",
        "实体": "entities",
        "主体": "subjects",
        "属性": "properties",
        "特征": "characteristics",
        "特点": "features",
        "性质": "nature",
        "本质": "essence",
        "表象": "appearance",
        "现象": "phenomena",
        "事实": "facts",
        "真相": "truth",
        "假设": "hypotheses",
        "理论": "theories",
        "观点": "viewpoints",
        "意见": "opinions",
        "看法": "perspectives",
        "态度": "attitudes",
        "立场": "stances",
        "角度": "angles",
        "维度": "dimensions",
        "层面": "levels",
        "层次": "hierarchies",
        "级别": "grades",
        "等级": "ranks",
        "排序": "ranking",
        "名次": "positions",
        "排名": "rankings",
        "首位": "first",
        "领先": "leading",
        "落后": "lagging",
        "追赶": "catching up",
        "超越": "surpassing",
        "保持": "maintaining",
        "稳定": "stable",
        "波动": "fluctuating",
        "变化": "changing",
        "增长": "growing",
        "下降": "declining",
        "上升": "rising",
        "提高": "improving",
        "降低": "reducing",
        "增强": "enhancing",
        "减弱": "weakening",
        "扩大": "expanding",
        "缩小": "shrinking",
        "延伸": "extending",
        "收缩": "contracting",
        "加速": "accelerating",
        "减速": "decelerating",
        "加快": "speeding up",
        "放慢": "slowing down",
        "提前": "advancing",
        "推迟": "delaying",
        "延期": "postponing",
        "取消": "canceling",
        "终止": "terminating",
        "完成": "completing",
        "结束": "ending",
        "开始": "starting",
        "启动": "launching",
        "初始化": "initializing",
        "配置": "configuring",
        "设置": "setting",
        "调整": "adjusting",
        "修改": "modifying",
        "更新": "updating",
        "删除": "deleting",
        "添加": "adding",
        "插入": "inserting",
        "替换": "replacing",
        "转换": "converting",
        "变换": "transforming",
        "处理": "processing",
        "计算": "calculating",
        "综合": "synthesizing",
        "归纳": "inducing",
        "演绎": "deducing",
        "推理": "reasoning",
        "预测": "predicting",
        "预报": "forecasting",
        "估计": "estimating",
        "测算": "measuring",
        "记录": "recording",
        "存储": "storing",
        "保存": "saving",
        "读取": "reading",
        "加载": "loading",
        "导出": "exporting",
        "导入": "importing",
        "上传": "uploading",
        "下载": "downloading",
        "传输": "transmitting",
        "发送": "sending",
        "接收": "receiving",
        "推送": "pushing",
        "拉取": "pulling",
        "并发": "concurrent",
        "循环": "cyclic",
        "迭代": "iterative",
        "递归": "recursive",
        "分步": "step-by-step",
        "逐步": "gradual",
        "分段": "segmented",
        "分层": "layered",
        "分模块": "modular",
        "分组件": "component-based",
        "分服务": "service-based",
        "分功能": "function-based",
        "研究院": "Research Institute",
        "数字化": "Digitalization",
    }

    translated = text

    # Apply phrase-level translations first (sorted by length, longest first)
    for chinese, english in sorted(phrases.items(), key=lambda x: len(x[0]), reverse=True):
        translated = translated.replace(chinese, english)

    # Handle specific patterns
    translated = re.sub(r'2026年', '2026', translated)
    translated = re.sub(r'(\d+)年', r'\1', translated)
    translated = re.sub(r'(\d+)美元', r'$\1', translated)
    translated = re.sub(r'(\d+)个月', r'\1 months', translated)
    translated = re.sub(r'(\d+)小时', r'\1 hours', translated)

    # Fix punctuation
    translated = translated.replace('：', ':').replace('，', ',').replace('。', '.').replace('！', '!').replace('？', '?')
    translated = translated.replace('（', '(').replace('）', ')')

    # Clean up spacing
    translated = re.sub(r'  +', ' ', translated)

    return translated.strip()

def process_file(filepath):
    """Process JSON file with comprehensive translation."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Translate all fields
        for field in ['title', 'description', 'content', 'author']:
            if field in data:
                data[field] = translate_comprehensive(data[field])

        if 'seo_keywords' in data:
            data['seo_keywords'] = [translate_comprehensive(k) for k in data['seo_keywords']]

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    data_dir = Path('/Users/gejiayu/owner/seo/data/publishing-media-tools')
    files = list(data_dir.glob('*.json'))

    print(f"Comprehensive translation for {len(files)} files...")

    success = 0
    for i, f in enumerate(files, 1):
        if process_file(f):
            print(f"[{i}/{len(files)}] ✓ {f.name}")
            success += 1

    print(f"\nComplete: {success}/{len(files)} files")

if __name__ == '__main__':
    main()