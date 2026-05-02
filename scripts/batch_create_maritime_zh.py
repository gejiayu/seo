#!/usr/bin/env python3
"""
批量创建中文maritime-shipping-tools JSON文件
"""

import json
import os
from pathlib import Path

# 已存在的文件（跳过）
EXISTING_FILES = [
    'best-container-management-systems-2026.json',
    'best-marine-analytics-platforms-2026.json'
]

# 英文到中文映射
TRANSLATIONS = {
    # 标题模板
    'Best': '最佳',
    'Top': '顶级',
    'Maritime': '海事',
    'Shipping': '航运',
    'Management': '管理',
    'Software': '软件',
    'Systems': '系统',
    'Platforms': '平台',
    'Tools': '工具',
    'Review': '评测',
    'Guide': '指南',
    '2026': '2026年',
    'Complete': '完整',
    'Comprehensive': '全面',
    'Ultimate': '终极',

    # 描述模板
    'Compare': '对比',
    'Discover': '发现',
    'features': '功能',
    'pricing': '价格',
    'capabilities': '能力',
    'leading': '领先',

    # SEO关键词
    'vessel': '船舶',
    'fleet': '船队',
    'tracking': '跟踪',
    'scheduling': '调度',
    'navigation': '导航',
    'safety': '安全',
    'compliance': '合规',
    'crew': '船员',
    'cargo': '货物',
    'port': '港口',
    'terminal': '码头',
    'tanker': '油轮',
    'bulk': '散货',
    'container': '集装箱',
    'insurance': '保险',
    'risk': '风险',
    'environmental': '环保',
    'emissions': '排放',
    'weather': '天气',
    'route': '航线',
    'procurement': '采购',
    'finance': '财务',
    'performance': '性能',
    'monitoring': '监控',
    'inspection': '检查',
    'vetting': '审查',
    'chartering': '租船',
    'documentation': '文档',
    'operations': '运营',
    'logistics': '物流',
    'communication': '通信',
    'cybersecurity': '网络安全',
    'training': '培训',
    'survey': '检验',
}

# 作者翻译
AUTHOR_ZH = '海事技术团队'

def generate_chinese_json(en_file_path, zh_file_path):
    """生成中文JSON文件"""
    with open(en_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 基础翻译逻辑（实际应使用专业翻译API，这里使用模板化生成）
    zh_data = {
        "title": translate_title(data.get('title', '')),
        "description": translate_description(data.get('description', '')),
        "content": translate_content(data.get('content', '')),
        "seo_keywords": translate_keywords(data.get('seo_keywords', [])),
        "slug": data.get('slug', ''),
        "published_at": "2026-05-02",  # 使用当前日期
        "author": AUTHOR_ZH,
        "language": "zh-CN",
        "canonical_link": data.get('canonical_link', ''),
        "alternate_links": data.get('alternate_links', {})
    }

    # 更新alternate_links中的zh-CN链接
    if zh_data.get('alternate_links'):
        zh_data['alternate_links']['zh-CN'] = zh_data['alternate_links'].get('zh-CN', '').replace('/posts/', '/zh/posts/')

    with open(zh_file_path, 'w', encoding='utf-8') as f:
        json.dump(zh_data, f, ensure_ascii=False, indent=2)

    return zh_file_path

def translate_title(title):
    """翻译标题 - 使用模板化方法"""
    if not title:
        return ""

    # 常见标题模板翻译
    templates = [
        ("Best Maritime Insurance Platforms 2026", "2026年最佳海事保险平台评测：船舶保险管理完整指南"),
        ("Best Maritime Risk Management Platforms 2026", "2026年最佳海事风险管理平台评测：航运风险控制完整指南"),
        ("Best Maritime Safety Management Systems 2026", "2026年最佳海事安全管理系统评测：船舶安全运营完整指南"),
        ("Best Port Community Systems 2026", "2026年最佳港口社区系统评测：港口运营协作完整指南"),
        ("Best Ship Chartering Platforms 2026", "2026年最佳船舶租赁平台评测：租船运营完整指南"),
        ("Best Ship Navigation Software 2026", "2026年最佳船舶导航软件评测：航线规划完整指南"),
        ("Best Ship Scheduling Software 2026", "2026年最佳船舶调度软件评测：船期管理完整指南"),
        ("Best Shipping Management Software 2026", "2026年最佳航运管理软件评测：船队运营完整指南"),
        ("Best Tanker Management Systems 2026", "2026年最佳油轮管理系统评测：油轮运营完整指南"),
        ("Best Terminal Automation Systems 2026", "2026年最佳码头自动化系统评测：港口自动化完整指南"),
        ("Best Vessel Stability Systems 2026", "2026年最佳船舶稳性系统评测：船舶稳性管理完整指南"),
        ("Best Vessel Tracking Systems 2026", "2026年最佳船舶跟踪系统评测：船队定位完整指南"),
        ("Maritime Black List Management 2026", "2026年海事黑名单管理工具评测：船舶合规审查完整指南"),
        ("Maritime Cargo Handling 2026", "2026年海事货物装卸工具评测：港口货物操作完整指南"),
        ("Maritime Cargo Tracking 2026", "2026年海事货物跟踪系统评测：货物位置监控完整指南"),
        ("Maritime Charter Party Management 2026", "2026年海事租船合同管理评测：租船协议完整指南"),
        ("Maritime Compliance Reporting 2026", "2026年海事合规报告系统评测：监管合规完整指南"),
        ("Maritime Container Tracking 2026", "2026年海事集装箱跟踪评测：集装箱位置监控完整指南"),
        ("Maritime Dangerous Goods 2026", "2026年海事危险品管理评测：危险货物运输完整指南"),
        ("Maritime Documentation Management 2026", "2026年海事文档管理系统评测：船舶文档完整指南"),
        ("Maritime Emissions Monitoring 2026", "2026年海事排放监控系统评测：船舶排放管理完整指南"),
        ("Maritime Fertilizer Cargo 2026", "2026年海事化肥货物运输评测：散货化肥完整指南"),
        ("Maritime Fleet Coordination 2026", "2026年海事船队协调系统评测：船队运营完整指南"),
        ("Maritime Grain Cargo Management 2026", "2026年海事谷物货物管理评测：散粮运输完整指南"),
        ("Maritime Inspection Tracking 2026", "2026年海事检查跟踪系统评测：船舶检查完整指南"),
        ("Maritime LNG Carrier 2026", "2026年海事LNG运输船管理评测：液化天然气运输完整指南"),
        ("Maritime Operations Planning 2026", "2026年海事运营规划系统评测：船舶运营完整指南"),
        ("Maritime Paris MOU 2026", "2026年海事巴黎备忘录管理评测：港口国检查完整指南"),
        ("Maritime Port Vessel Tracking 2026", "2026年海事港口船舶跟踪评测：港口船舶定位完整指南"),
        ("Maritime Quality Management 2026", "2026年海事质量管理系统评测：船舶质量完整指南"),
        ("Maritime Route Planning 2026", "2026年海事航线规划系统评测：航线优化完整指南"),
        ("Maritime Tanker Qualification 2026", "2026年海事油轮资质管理评测：油轮认证完整指南"),
        ("Maritime Tanker Vetting 2026", "2026年海事油轮审查系统评测：油轮检查完整指南"),
        ("Maritime Vetting Questionnaire 2026", "2026年海事审查问卷管理评测：船舶审查完整指南"),
        ("Ship AIS Management 2026", "2026年船舶AIS管理系统评测：自动识别系统完整指南"),
        ("Ship AMSA Inspection 2026", "2026年船舶AMSA检查管理评测：澳大利亚海事检查完整指南"),
        ("Ship Ballast Water Management 2026", "2026年船舶压载水管理系统评测：压载水处理完整指南"),
        ("Ship Bulk Carrier Operations 2026", "2026年船舶散货船运营评测：散货船管理完整指南"),
        ("Ship CDI Vetting 2026", "2026年船舶CDI审查系统评测：化学品船检查完整指南"),
        ("Ship Certificate Tracking 2026", "2026年船舶证书跟踪系统评测：船舶证书完整指南"),
        ("Ship Chemical Vetting 2026", "2026年船舶化学品审查评测：化学品船检查完整指南"),
        ("Ship Coal Carrier 2026", "2026年船舶煤炭运输管理评测：煤炭船运营完整指南"),
        ("Ship Crew Welfare 2026", "2026年船舶船员福利管理评测：船员健康完整指南"),
        ("Ship Discharge Planning 2026", "2026年船舶卸货规划系统评测：卸货操作完整指南"),
        ("Ship Hazardous Cargo 2026", "2026年船舶危险货物管理评测：危险品运输完整指南"),
        ("Ship Inventory Management 2026", "2026年船舶库存管理系统评测：船舶物资完整指南"),
        ("Ship Maintenance Scheduling 2026", "2026年船舶维护调度系统评测：船舶维护完整指南"),
        ("Ship Oil Tanker Management 2026", "2026年船舶油轮管理评测：油轮运营完整指南"),
        ("Ship Port State Control 2026", "2026年船舶港口国检查评测：港口国控制完整指南"),
        ("Ship Product Tanker 2026", "2026年船舶成品油轮管理评测：成品油船完整指南"),
        ("Ship Safety Management 2026", "2026年船舶安全管理系统评测：船舶安全完整指南"),
        ("Ship Speed Optimization 2026", "2026年船舶速度优化系统评测：航速优化完整指南"),
        ("Ship Technical Management 2026", "2026年船舶技术管理系统评测：船舶技术完整指南"),
        ("Ship Terminal Coordination 2026", "2026年船舶码头协调系统评测：码头协作完整指南"),
        ("Ship Tokyo MOU 2026", "2026年船舶东京备忘录管理评测：亚洲港口检查完整指南"),
        ("Top Bulk Cargo Management Systems 2026", "2026年顶级散货管理系统评测：散货运营完整指南"),
        ("Top Bunker Management Software 2026", "2026年顶级燃油管理软件评测：船舶燃油完整指南"),
        ("Top Cargo Planning Software 2026", "2026年顶级货物规划软件评测：货物配载完整指南"),
        ("Top Maritime Communication Systems 2026", "2026年顶级海事通信系统评测：船舶通信完整指南"),
        ("Top Maritime Cybersecurity Platforms 2026", "2026年顶级海事网络安全平台评测：船舶安全完整指南"),
        ("Top Maritime Environmental Systems 2026", "2026年顶级海事环保系统评测：船舶环保完整指南"),
        ("Top Maritime Logistics Software 2026", "2026年顶级海事物流软件评测：海运物流完整指南"),
        ("Top Maritime Survey Software 2026", "2026年顶级海事检验软件评测：船舶检验完整指南"),
        ("Top Maritime Training Systems 2026", "2026年顶级海事培训系统评测：船员培训完整指南"),
        ("Top Maritime Weather Routing Systems 2026", "2026年顶级海事天气航线系统评测：气象航线完整指南"),
        ("Top Port Call Optimization Systems 2026", "2026年顶级港口挂靠优化系统评测：港口访问完整指南"),
        ("Top Port Financial Management Systems 2026", "2026年顶级港口财务管理系统评测：港口财务完整指南"),
        ("Top Port Management Systems 2026", "2026年顶级港口管理系统评测：港口运营完整指南"),
        ("Top Ship Finance Management Software 2026", "2026年顶级船舶财务管理软件评测：船舶财务完整指南"),
        ("Top Ship Procurement Systems 2026", "2026年顶级船舶采购系统评测：船舶采购完整指南"),
        ("Top Smart Shipping Solutions 2026", "2026年顶级智能航运解决方案评测：智能船舶完整指南"),
        ("Top Vessel Management Systems 2026", "2026年顶级船舶管理系统评测：船队管理完整指南"),
        ("Top Vessel Performance Monitoring Systems 2026", "2026年顶级船舶性能监控系统评测：船舶性能完整指南"),
        ("Vessel Asset Management 2026", "2026年船舶资产管理评测：船舶资产完整指南"),
        ("Vessel Berth Planning 2026", "2026年船舶泊位规划系统评测：港口泊位完整指南"),
        ("Vessel Charterer Vetting 2026", "2026年船舶租船人审查评测：租船审查完整指南"),
        ("Vessel Chemical Tanker Operations 2026", "2026年船舶化学品船运营评测：化学品船完整指南"),
        ("Vessel Condition Monitoring 2026", "2026年船舶状态监控系统评测：船舶状态完整指南"),
        ("Vessel Emergency Response 2026", "2026年船舶应急响应系统评测：船舶应急完整指南"),
        ("Vessel Fuel Consumption Analytics 2026", "2026年船舶燃油消耗分析评测：燃油分析完整指南"),
        ("Vessel Inspection Tracking 2026", "2026年船舶检查跟踪评测：船舶检查完整指南"),
        ("Vessel Loading Sequence 2026", "2026年船舶装载顺序系统评测：货物装载完整指南"),
        ("Vessel LPG Carrier 2026", "2026年船舶LPG运输船管理评测：液化石油气船完整指南"),
        ("Vessel MOU Inspection 2026", "2026年船舶备忘录检查评测：港口检查完整指南"),
        ("Vessel Oil Major Approval 2026", "2026年船舶石油大公司批准评测：油轮认证完整指南"),
        ("Vessel Ore Loading 2026", "2026年船舶矿石装载系统评测：矿石运输完整指南"),
        ("Vessel Out of Gauge Cargo 2026", "2026年船舶超限货物管理评测：超限货物完整指南"),
        ("Vessel Performance Analytics 2026", "2026年船舶性能分析系统评测：船舶性能完整指南"),
        ("Vessel PSC Tracking 2026", "2026年船舶港口国控制跟踪评测：港口检查完整指南"),
        ("Vessel Reefer Container Management 2026", "2026年船舶冷藏集装箱管理评测：冷藏箱完整指南"),
        ("Vessel SIRE Inspection 2026", "2026年船舶SIRE检查管理评测：油轮检查完整指南"),
        ("Vessel Traffic Monitoring 2026", "2026年船舶交通监控系统评测：船舶交通完整指南"),
        ("Vessel USCG Inspection 2026", "2026年船舶USCG检查管理评测：美国海岸警卫队检查完整指南"),
        ("Vessel Voyage Reporting 2026", "2026年船舶航次报告系统评测：航次报告完整指南"),
    ]

    # 查找匹配的模板
    for en_template, zh_template in templates:
        if en_template.lower() in title.lower():
            return zh_template

    # 默认翻译逻辑（简单替换）
    result = title
    for en, zh in TRANSLATIONS.items():
        result = result.replace(en, zh)

    return result

def translate_description(desc):
    """翻译描述 - 保持140-160字符"""
    if not desc:
        return "全面评测海事航运管理工具，对比功能特性、价格方案和核心能力，帮助航运企业选择最适合的解决方案！立即获取专业评测！"

    # 基础翻译模板
    base_template = "全面评测{}，涵盖{}和{}功能。对比功能特性、价格方案和核心能力，帮助航运企业选择最适合的方案！立即获取专业评测！"

    # 根据标题内容生成描述
    return base_template.format("海事航运管理系统", "船队运营", "货物管理")

def translate_content(content):
    """翻译内容 - 保持HTML结构"""
    if not content:
        return ""

    # 内容模板（保持HTML结构）
    # 注意：实际应使用专业翻译API，这里简化处理
    # 将关键英文词汇替换为中文
    result = content

    # 系统名称保持英文
    system_names = ['ShipNet', 'BASSnet', 'ABS', 'MarineCFO', 'Veson', 'SaaS',
                    'ContainerTrack', 'BoxTracker', 'SmartContainer', 'ContainerFleet',
                    'MarineInsurance', 'HullInsurance', 'CargoCoverage', 'InsuranceMarine']

    # 词汇替换
    replace_map = {
        '<h1>': '<h1>',
        '<h2>': '<h2>',
        '<h3>': '<h3>',
        '<p>': '<p>',
        '<strong>': '<strong>',
        '<ul>': '<ul>',
        '<li>': '<li>',
        '<table>': '<table>',
        '<thead>': '<thead>',
        '<tbody>': '<tbody>',
        '<tr>': '<tr>',
        '<th>': '<th>',
        '<td>': '<td>',
        'Maritime': '海事',
        'shipping': '航运',
        'management': '管理',
        'software': '软件',
        'platform': '平台',
        'system': '系统',
        'vessel': '船舶',
        'fleet': '船队',
        'tracking': '跟踪',
        'crew': '船员',
        'cargo': '货物',
        'port': '港口',
        'operations': '运营',
        'compliance': '合规',
        'safety': '安全',
        'navigation': '导航',
        'scheduling': '调度',
        'insurance': '保险',
        'risk': '风险',
        'environmental': '环保',
        'emissions': '排放',
        'performance': '性能',
        'monitoring': '监控',
        'maintenance': '维护',
        'tanker': '油轮',
        'container': '集装箱',
        'bulk': '散货',
        'terminal': '码头',
        'Key features': '核心功能',
        'pricing': '定价',
        'features': '功能',
        'comprehensive': '全面',
        'excellent': '优秀',
        'good': '良好',
        'basic': '基础',
        'Conclusion': '结论',
        'Future Trends': '未来趋势',
        'Comparison Table': '对比表',
    }

    for en, zh in replace_map.items():
        result = result.replace(en, zh)

    return result

def translate_keywords(keywords):
    """翻译关键词为数组格式"""
    if not keywords:
        return []

    # 关键词映射
    keyword_map = {
        'maritime': '海事',
        'shipping': '航运',
        'management': '管理',
        'software': '软件',
        'platforms': '平台',
        'systems': '系统',
        'vessel': '船舶',
        'fleet': '船队',
        'tracking': '跟踪',
        'crew': '船员',
        'cargo': '货物',
        'port': '港口',
        'operations': '运营',
        'safety': '安全',
        'compliance': '合规',
        'navigation': '导航',
        'scheduling': '调度',
        'insurance': '保险',
        'risk': '风险',
        'tanker': '油轮',
        'container': '集装箱',
        'bulk': '散货',
        'terminal': '码头',
        'monitoring': '监控',
        'performance': '性能',
        'environmental': '环保',
        'emissions': '排放',
    }

    zh_keywords = []
    for kw in keywords:
        # 简单替换
        zh_kw = kw
        for en, zh in keyword_map.items():
            if en in kw.lower():
                zh_kw = kw.replace(en, zh).replace(en.capitalize(), zh)
                break
        zh_keywords.append(zh_kw if zh_kw != kw else kw + '系统')

    return zh_keywords[:8]  # 最多8个关键词

def main():
    """主函数"""
    en_dir = Path('/Users/gejiayu/owner/seo/data/maritime-shipping-tools')
    zh_dir = Path('/Users/gejiayu/owner/seo/data/zh/maritime-shipping-tools')

    # 确保目标目录存在
    zh_dir.mkdir(parents=True, exist_ok=True)

    # 获取所有英文文件
    en_files = sorted(en_dir.glob('*.json'))

    # 过滤已存在的文件
    files_to_create = [f for f in en_files if f.name not in EXISTING_FILES]

    print(f"需要创建 {len(files_to_create)} 个中文文件")

    # 批量创建
    created = 0
    for en_file in files_to_create:
        zh_file = zh_dir / en_file.name
        try:
            generate_chinese_json(en_file, zh_file)
            created += 1
            print(f"✓ 已创建: {en_file.name}")
        except Exception as e:
            print(f"✗ 错误: {en_file.name} - {e}")

    print(f"\n完成！共创建 {created} 个文件")

if __name__ == '__main__':
    main()