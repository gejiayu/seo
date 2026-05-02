#!/usr/bin/env python3
"""Manual translation script with comprehensive mapping."""
import json
import re
from pathlib import Path

def contains_chinese(text):
    if not isinstance(text, str):
        return False
    return bool(re.search(r'[一-鿿]', text))

TRANSLATION_MAP = {
    "终极评测": "Ultimate Review",
    "深度评测": "In-depth Review",
    "十大": "Top 10",
    "助力学术出版": "for Academic Publishing",
    "全球": "Global",
    "市场规模": "market size",
    "预计达到": "expected to reach",
    "年增长率": "annual growth rate",
    "保持在": "maintained at",
    "行业面临": "industry faces",
    "核心挑战": "core challenges",
    "传统方法": "traditional methods",
    "难以满足": "struggle to meet",
    "现代需求": "modern demands",
    "成为核心竞争力": "becomes a core competitive advantage",
    "选择合适的工具": "Choosing the right tool",
    "直接影响": "directly impacts",
    "效率、成本与质量": "efficiency, cost, and quality",
    "一、行业特殊需求分析": "I. Industry Special Requirements Analysis",
    "二、十大平台深度评测": "II. Top 10 Platforms In-depth Review",
    "三、核心功能参数对比表": "III. Core Functionality Comparison Table",
    "四、发展趋势": "IV. Development Trends",
    "五、选型策略与实施路径": "V. Selection Strategy and Implementation Path",
    "效率提升需求": "Efficiency Improvement Requirements",
    "成本控制需求": "Cost Control Requirements",
    "质量控制需求": "Quality Control Requirements",
    "数据分析需求": "Data Analysis Requirements",
    "需高效率处理": "requires high-efficiency processing",
    "需成本控制优化": "requires cost control optimization",
    "需高质量输出": "requires high-quality output",
    "需数据分析支持": "requires data analysis support",
    "工具需支持": "tools need to support",
    "自动化流程": "automated workflows",
    "成本分析管理": "cost analysis management",
    "质量检验功能": "quality inspection functions",
    "数据深度分析": "in-depth data analysis",
    "专业级": "Professional-level",
    "工具": "tool",
    "核心功能": "Core features:",
    "自动化管理": "automated management",
    "成本优化分析支持": "cost optimization analysis support",
    "质量检验深度化": "in-depth quality inspection",
    "价格": "Price:",
    "订阅制": "Subscription-based",
    "月": "/month",
    "特色": "Special features:",
    "专业能力顶尖": "top-tier professional capabilities",
    "适合大型团队": "suitable for large teams",
    "适合中型团队": "suitable for medium-sized teams",
    "适合小型团队": "suitable for small teams",
    "性价比高": "high cost-effectiveness",
    "快速上手": "quick to start",
    "平台名称": "Platform Name",
    "核心定位": "Core Positioning",
    "价格区间": "Price Range",
    "效率能力": "Efficiency Capability",
    "成本控制": "Cost Control",
    "质量保障": "Quality Assurance",
    "数据分析": "Data Analysis",
    "高": "High",
    "中": "Medium",
    "低": "Low",
    "行业将呈现关键发展趋势": "The industry will present key development trends:",
    "AI驱动自动化": "AI-driven automation",
    "提升至": "increases to",
    "效率提升": "efficiency improves by",
    "成本控制智能化": "intelligent cost control",
    "成本降低": "cost reduction by",
    "质量检验实时化": "real-time quality inspection",
    "质量提升": "quality improvement by",
    "数据分析深度化": "in-depth data analysis",
    "决策准确性提升": "decision-making accuracy improves by",
    "团队应根据规模与需求选择工具": "Teams should choose tools based on size and requirements:",
    "选择企业级平台": "Choose enterprise-level platforms",
    "选择专业级平台": "Choose professional-level platforms",
    "选择轻量级平台": "Choose lightweight platforms",
    "月投入": "monthly investment of",
    "实施路径": "Implementation path:",
    "先完成需求评估": "First complete requirements assessment",
    "再试用核心工具": "then trial core tools",
    "最后规模化部署": "finally scale deployment",
    "个月": "months",
    "个": "",
    "学术排版工具": "academic typesetting tools",
    "LaTeX排版系统": "LaTeX typesetting system",
    "Overleaf学术排版": "Overleaf academic typesetting",
    "学术文献排版": "academic document typesetting",
    "公式处理平台": "formula processing platform",
    "引用管理工具": "reference management tools",
    "学术排版软件": "academic typesetting software",
    "文献排版平台": "document typesetting platform",
    "学术排版系统": "academic typesetting system",
    "排版工具软件": "typesetting tool software",
    "出版数字化研究院": "Publishing Digitalization Research Institute",
    "研究院": "Research Institute",
    "数字化": "Digitalization",
    "出版": "Publishing",
    "对比": "Comparison",
    "评测": "Review",
    "指南": "Guide",
    "助力": "Empowering",
    "管理": "Management",
    "系统": "System",
    "平台": "Platform",
    "软件": "Software",
    "方案": "Solution",
}

def translate_field(text):
    if not isinstance(text, str) or not contains_chinese(text):
        return text
    
    translated = text
    for chinese, english in sorted(TRANSLATION_MAP.items(), key=lambda x: len(x[0]), reverse=True):
        translated = translated.replace(chinese, english)
    
    translated = re.sub(r'2026年', '2026', translated)
    translated = re.sub(r'(\d+)美元', r'$\1M', translated)
    translated = re.sub(r'(\d+)%', r'\1%', translated)
    translated = re.sub(r'  +', ' ', translated)
    translated = translated.replace('：', ':').replace('，', ',').replace('。', '.').replace('！', '!')
    
    return translated.strip()

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        data['title'] = translate_field(data.get('title', ''))
        data['description'] = translate_field(data.get('description', ''))
        data['content'] = translate_field(data.get('content', ''))
        
        if 'seo_keywords' in data:
            data['seo_keywords'] = [translate_field(k) for k in data['seo_keywords']]
        
        if 'author' in data:
            data['author'] = translate_field(data['author'])
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    data_dir = Path('/Users/gejiayu/owner/seo/data/publishing-media-tools')
    json_files = list(data_dir.glob('*.json'))
    print(f"Processing {len(json_files)} files...")
    
    for i, filepath in enumerate(json_files, 1):
        if process_file(filepath):
            print(f"[{i}/{len(json_files)}] ✓ {filepath.name}")
    
    print("Done!")

if __name__ == '__main__':
    main()
