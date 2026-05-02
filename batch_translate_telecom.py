#!/usr/bin/env python3
"""
Batch translation script for telecom JSON files.
Translates Chinese content to English.
"""
import json
import re
from pathlib import Path

# Directory containing JSON files
DATA_DIR = Path("/Users/gejiayu/owner/seo/data/telecommunications-network-tools")

# Translation mappings for common terms
TRANSLATION_MAP = {
    # Common phrases
    "深度分析相关工具领域解决方案。了解更多功能和价格对比，找到最适合你的方案！": "In-depth analysis of telecom solutions. Compare features and pricing to find the best solution for your needs!",
    "了解更多功能和价格对比，找到最适合你的方案！": "Compare features and pricing to find the best solution for your needs!",
    "了解更多功能和价格对比，找到最适合你的方案！专业评测助你决策！": "Compare features and pricing to find the best solution for your needs! Professional evaluation helps you decide!",

    # Title patterns
    "深度评测｜2026年评测": "In-depth Review | 2026 Evaluation",
    "对比评测｜2026年评测": "Comparison Review | 2026 Evaluation",
    "对比评测2026版": "Comparison Review 2026 Edition",
    "深度评测与对比｜2026年评测": "In-depth Review and Comparison | 2026 Evaluation",
    "深度评测与选购指南｜2026年评测": "In-depth Review and Selection Guide | 2026 Evaluation",

    # Content sections
    "背景介绍": "Background Introduction",
    "深度评测": "In-depth Review",
    "参数对比表": "Parameter Comparison Table",
    "趋势预测": "Trend Prediction",
    "趋势预测": "Trend Forecast",

    # Common terms
    "电信网络": "Telecom Network",
    "电信运营商": "Telecom Operator",
    "运营商": "Operator",
    "优势在于": "advantage lies in",
    "本地化支持": "localized support",
    "本地化适配": "localized adaptation",
    "云端管理": "cloud management",
    "自动化": "automation",
    "AI驱动": "AI-driven",
    "实时监控": "real-time monitoring",
    "全面覆盖": "full coverage",
    "精准预测": "precise prediction",
    "智能": "intelligent",
    "深度": "depth",
    "高级别": "high-level",
    "全面": "comprehensive",
    "灵活": "flexible",
    "强大的": "powerful",
    "确保": "ensure",
    "支持": "support",
    "提供": "provide",
    "集成": "integration",
    "功能": "function",
    "能力": "capability",
    "平台": "platform",
    "系统": "system",
    "管理": "management",
    "监控": "monitoring",
    "分析": "analysis",
    "预测": "prediction",
    "优化": "optimization",
    "配置": "configuration",
    "部署": "deployment",
    "执行": "execution",
    "处理": "processing",
    "追踪": "tracking",
    "诊断": "diagnosis",
    "修复": "repair",
    "测试": "testing",
    "验证": "verification",
    "调整": "adjustment",
    "规划": "planning",
    "设计": "design",
    "实施": "implementation",
    "运行": "operation",
    "维护": "maintenance",
    "保护": "protection",
    "安全": "security",
    "性能": "performance",
    "效率": "efficiency",
    "成本": "cost",
    "价值": "value",
    "资源": "resource",
    "数据": "data",
    "信息": "information",
    "流程": "process",
    "任务": "task",
    "服务": "service",
    "用户": "user",
    "客户": "customer",
    "业务": "business",
    "应用": "application",
    "工具": "tool",
    "设备": "device/equipment",
    "网络": "network",
    "技术": "technology",
    "方案": "solution",
    "建议": "recommendation",
    "报告": "report",
    "结果": "result",
    "效果": "effect",
    "状态": "status",
    "参数": "parameter",
    "指标": "indicator/metric",
    "场景": "scenario",
    "需求": "requirement",
    "挑战": "challenge",
    "趋势": "trend",
    "发展": "development",
    "演进": "evolution",
    "转型": "transformation",
    "准备": "preparation",
    "未来": "future",
    "核心": "core",
    "关键": "key",
    "重要": "important",
    "特殊": "special",
    "优秀": "excellent",
    "主流": "mainstream",
    "新型": "new type",
    "智能": "intelligent",
    "自动化": "automated",
    "数字化": "digital",
    "云端": "cloud",
    "边缘": "edge",
    "分布式": "distributed",
    "统一": "unified",
    "灵活": "flexible",
    "强大": "powerful",
    "高效": "efficient",
    "精准": "precise",
    "实时": "real-time",
    "动态": "dynamic",
    "持续": "continuous",
    "完整": "complete",
    "全面": "comprehensive",
    "严格": "strict",
    "高级别": "high-level",
    "低延迟": "low-latency",
    "高吞吐量": "high throughput",
    "大规模": "large-scale",
    "海量": "massive",
    "复杂": "complex",
    "精细": "fine/precise",
    "敏捷": "agile",
    "快速": "fast/rapid",
    "弹性": "elastic",
    "可靠": "reliable",
    "稳定": "stable",
    "安全": "secure",
    "可信": "trustworthy",
    "透明": "transparent",
    "开放": "open",
    "集成": "integrated",
    "无缝": "seamless",
    "端到端": "end-to-end",
    "零接触": "zero-touch",
    "闭环": "closed-loop",
    "智能化": "intelligent",
    "自动化": "automated",
    "数字化": "digitalized",
    "云化": "cloudified",
    "现代化": "modernized",
    "企业化": "enterprise",
    "专业化": "specialized",
    "本地化": "localized",
    "定制化": "customized",
    "标准化": "standardized",
    "规范化": "regulated",
    "合规化": "compliant",
}

def contains_chinese(text):
    """Check if text contains Chinese characters."""
    return bool(re.search('[一-鿿]', text))

def translate_field(text):
    """Translate text field from Chinese to English."""
    if not contains_chinese(text):
        return text

    # Apply direct translations
    translated = text
    for cn, en in TRANSLATION_MAP.items():
        translated = translated.replace(cn, en)

    return translated

def process_file(file_path):
    """Process a single JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if file needs translation
        needs_translation = False
        for key in ['title', 'description', 'content']:
            if key in data and contains_chinese(data[key]):
                needs_translation = True
                break

        if not needs_translation:
            return False

        # Translate fields
        if 'title' in data:
            data['title'] = translate_field(data['title'])
        if 'description' in data:
            data['description'] = translate_field(data['description'])
        if 'content' in data:
            data['content'] = translate_field(data['content'])
        if 'seo_keywords' in data and isinstance(data['seo_keywords'], list):
            data['seo_keywords'] = [translate_field(kw) for kw in data['seo_keywords']]

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Process all JSON files in the directory."""
    json_files = list(DATA_DIR.glob('*.json'))
    translated_count = 0

    for file_path in json_files:
        if process_file(file_path):
            translated_count += 1
            print(f"Translated: {file_path.name}")

    print(f"\nTotal files translated: {translated_count}")
    print(f"Total files processed: {len(json_files)}")

if __name__ == '__main__':
    main()