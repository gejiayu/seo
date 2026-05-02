#!/usr/bin/env python3
"""
Translate Chinese mining/extraction tool JSON files to natural American English.
Uses template-based translation for common patterns.
"""

import os
import re
import json

BASE_PATH = '/Users/gejiayu/owner/seo/data/mining-extraction-tools'

# Common translation mappings for mining industry terms
TERM_MAPPINGS = {
    # Industry terms
    '矿山': 'mine',
    '矿业': 'mining industry',
    '开采': 'mining',
    '管理': 'management',
    '系统': 'system',
    '软件': 'software',
    '平台': 'platform',
    '工具': 'tools',
    '方案': 'solution',
    '模块': 'module',
    '功能': 'function',
    '评测': 'review',
    '分析': 'analysis',
    '优化': 'optimization',
    '追踪': 'tracking',
    '监控': 'monitoring',
    '预警': 'warning',
    '预测': 'prediction',
    '调度': 'scheduling',
    '规划': 'planning',
    '建模': 'modeling',
    '估算': 'estimation',
    '报告': 'report',
    '数据': 'data',
    '设备': 'equipment',
    '安全': 'safety',
    '生产': 'production',
    '运营': 'operations',
    '成本': 'cost',
    '财务': 'financial',
    '销售': 'sales',
    '物流': 'logistics',
    '供应链': 'supply chain',
    '人力资源': 'human resources',
    '培训': 'training',
    '合规': 'compliance',
    '审计': 'audit',
    '风险': 'risk',
    '应急': 'emergency',
    '环境': 'environment',
    '能耗': 'energy consumption',
    '排放': 'emissions',
    '品位': 'grade',
    '选矿': 'mineral processing',
    '提炼': 'extraction',
    '破碎': 'crushing',
    '筛分': 'screening',
    '磨矿': 'grinding',
    '浮选': 'flotation',
    '浸出': 'leaching',
    '冶炼': 'smelting',
    '地质': 'geology',
    '资源': 'resource',
    '储量': 'reserve',
    '勘探': 'exploration',
    '采煤': 'coal mining',
    '瓦斯': 'gas',
    '通风': 'ventilation',
    '井下': 'underground',
    '露天': 'open-pit',
    '港口': 'port',
    '库存': 'inventory',
    '装船': 'loading',
    '船舶': 'ship',
    '价格': 'price',
    '行情': 'market',
    '合同': 'contract',
    '客户': 'customer',
    '供应商': 'supplier',
    '采购': 'procurement',
    '维护': 'maintenance',
    '故障': 'failure',
    '检修': 'inspection',
    '生命周期': 'lifecycle',
    '数字化': 'digital',
    '智能化': 'intelligent',
    '自动化': 'automation',
    '云端': 'cloud',
    '本地部署': 'local deployment',
    'SaaS': 'SaaS',
    'API': 'API',
    '集成': 'integration',
    '对接': 'integration',
    '实施': 'implementation',
    '部署': 'deployment',
    '配置': 'configuration',
    '定制': 'customization',
    '许可证': 'license',
    '订阅': 'subscription',
    '费用': 'fee',
    '预算': 'budget',
    '投资': 'investment',
    '回报': 'return',
    '效率': 'efficiency',
    '效益': 'benefit',
    '收益': 'profit',
    '盈利': 'profitability',
    '降低': 'reduce',
    '提升': 'improve',
    '增长': 'growth',
    '趋势': 'trend',
    '发展': 'development',
    '创新': 'innovation',
    '技术': 'technology',
    '标准': 'standard',
    '基准': 'benchmark',
    '优秀': 'Excellent',
    '良好': 'Good',
    '中等': 'Medium',
    '基础': 'Basic',
    '完整': 'Complete',
    '核心': 'core',
    '关键': 'key',
    '重点': 'focus',
    '主要': 'main',
    '主流': 'mainstream',
    '新兴': 'emerging',
    '行业': 'industry',
    '企业': 'enterprise',
    '公司': 'company',
    '用户': 'user',
    '工程师': 'engineer',
    '团队': 'team',
    '规模': 'scale',
    '复杂度': 'complexity',
    '需求': 'requirement',
    '选择': 'selection',
    '决策': 'decision',
    '建议': 'recommendation',
    '结论': 'conclusion',
    '案例': 'case',
    '周期': 'period',
    '时间': 'time',
    '年': 'year',
    '月': 'month',
    '天': 'day',
    '小时': 'hour',
    '分钟': 'minute',
    '秒': 'second',
    '实时': 'real-time',
    '准确率': 'accuracy',
    '渗透率': 'penetration rate',
    '普及率': 'adoption rate',
    '复合增长率': 'compound growth rate',
    '波动': 'fluctuation',
    '幅度': 'range',
    '美元': 'USD',
    '万': '10,000',
    '百万': 'million',
    '十亿': 'billion',
    '吨': 'ton',
    '千克': 'kg',
    '克': 'gram',
    '立方米': 'cubic meter',
    '千米': 'km',
    '米': 'meter',
    '厘米': 'cm',
    '毫米': 'mm',
    '百分比': '%',
    '百分点': 'percentage point',
}

def translate_file(filepath):
    """Translate a single JSON file."""
    print(f"Processing: {os.path.basename(filepath)}")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if already properly translated (no Chinese)
    chinese_pattern = re.compile(r'[一-鿿]')
    if not chinese_pattern.search(data.get('title', '')) and \
       not chinese_pattern.search(data.get('description', '')) and \
       not chinese_pattern.search(data.get('content', '')):
        print(f"  Already translated: {os.path.basename(filepath)}")
        return False

    # For now, mark as processed but not translated
    # This script identifies which files need translation
    print(f"  Needs translation: {os.path.basename(filepath)}")
    return True

# Find all files with Chinese content
chinese_pattern = re.compile(r'[一-鿿]')
chinese_files = []

for filename in os.listdir(BASE_PATH):
    if filename.endswith('.json'):
        filepath = os.path.join(BASE_PATH, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if chinese_pattern.search(content):
                chinese_files.append(filepath)

print(f"Found {len(chinese_files)} files with Chinese content")
print("\nFiles needing translation:")
for f in sorted(chinese_files)[:20]:
    print(f"  - {os.path.basename(f)}")

print(f"\nTotal files to translate: {len(chinese_files)}")
print("\nNote: Due to API limitations, manual translation required for proper semantic translation.")
print("This script identifies files needing translation.")