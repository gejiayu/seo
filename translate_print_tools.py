#!/usr/bin/env python3
"""
Comprehensive Chinese to English translation for print industry SEO content
Preserves HTML structure and handles full sentences
"""

import json
import re
from pathlib import Path

# Comprehensive translation dictionary - longest phrases first
TRANSLATIONS = {
    # Title/Description patterns
    '深度评测2026年': 'In-depth Review of 2026',
    '了解更多功能和价格对比，找到最适合你的方案！': 'Learn more about features and pricing comparisons to find the best solution for you!',
    '专业评测助你决策！': 'Professional reviews help you decide!',
    '为印刷企业': 'for print businesses',
    '提供方案': 'providing solutions',

    # Common section headers
    '用户评价': 'User Reviews',
    '核心功能': 'Core Features',
    '核心定位': 'Core Positioning',
    '价格': 'Pricing',
    '选型建议': 'Selection Recommendations',

    # Common content patterns
    '印刷厂认为': 'Print shops consider',
    '大型印刷厂认为': 'Large print shops consider',
    '中小印刷厂认为': 'Small and medium print shops consider',
    '需与': 'needs integration with',
    '系统集成': 'system integration',
    '但': 'but',
    '适合': 'suitable for',
    '适合已有': 'suitable for existing',
    '门槛': 'barrier',

    # Common phrases in descriptions
    '对比': 'comparison',
    '功能': 'features',
    '方案': 'solutions',

    # Industry terms - longest first
    '印刷数据分析专家': 'Print Data Analytics Expert',
    '印刷客户沟通专家': 'Print Customer Communication Expert',
    '印刷客户管理专家': 'Print Customer Management Expert',
    '印刷设计专家': 'Print Design Expert',
    '印刷生产专家': 'Print Production Expert',
    '印刷质量专家': 'Print Quality Expert',
    '印刷财务专家': 'Print Financial Expert',
    '印刷人力资源专家': 'Print HR Expert',
    '印刷设备专家': 'Print Equipment Expert',
    '印刷行业专家': 'Print Industry Expert',
    '印刷管理专家': 'Print Management Expert',
    '印刷数字化转型专家': 'Print Digital Transformation Expert',
    '印刷安全专家': 'Print Safety Expert',
    '印刷创新专家': 'Print Innovation Expert',

    '印刷数据分析与BI评测': 'Print Data Analytics and BI Review',
    '印刷客户沟通软件评测': 'Print Customer Communication Software Review',
    '印刷客户管理系统评测': 'Print Customer Management System Review',
    '印刷客户自助平台评测': 'Print Customer Self-Service Platform Review',
    '印刷客户服务平台评测': 'Print Customer Service Platform Review',

    '印刷MIS报表': 'Print MIS Reports',
    'Power BI印刷': 'Power BI for Print',
    'Tableau印刷分析': 'Tableau Print Analytics',

    '印刷经营分析': 'Print Business Analytics',
    '印刷生产分析': 'Print Production Analytics',
    '印刷客户分析': 'Print Customer Analytics',
    '印刷BI工具': 'Print BI Tools',
    '印刷数据仪表盘': 'Print Data Dashboard',

    '印刷客户沟通系统': 'Print Customer Communication System',
    '印刷在线客服': 'Print Online Customer Service',
    '印刷客户反馈': 'Print Customer Feedback',
    '印刷沟通渠道': 'Print Communication Channels',
    '印刷客服聊天': 'Print Customer Chat',
    '印刷客户反馈收集': 'Print Customer Feedback Collection',
    '印刷沟通记录': 'Print Communication Records',
    '印刷客服AI': 'Print Customer Service AI',

    '印刷客户管理系统': 'Print Customer Management System',
    '印刷客户档案': 'Print Customer Profiles',
    '印刷客户分类': 'Print Customer Segmentation',
    '印刷客户维护': 'Print Customer Maintenance',

    '印刷客户自助平台': 'Print Customer Self-Service Platform',
    '印刷自助下单': 'Print Self-Ordering',
    '印刷自助查询': 'Print Self-Inquiry',
    '印刷自助跟踪': 'Print Self-Tracking',

    '印刷客户服务平台': 'Print Customer Service Platform',
    '印刷客户支持': 'Print Customer Support',
    '印刷客户咨询': 'Print Customer Consultation',

    '印刷数据安全': 'Print Data Security',
    '印刷数据加密': 'Print Data Encryption',
    '印刷数据备份': 'Print Data Backup',
    '印刷数据权限': 'Print Data Permissions',

    '印刷设计协作': 'Print Design Collaboration',
    '印刷设计模板': 'Print Design Templates',
    '印刷设计验证': 'Print Design Validation',

    '印刷数字资产': 'Print Digital Assets',
    '印刷数字印刷': 'Print Digital Printing',
    '印刷数字方案': 'Print Digital Solutions',
    '印刷数字化转型': 'Print Digital Transformation',

    '印刷能源管理': 'Print Energy Management',
    '印刷企业管理': 'Print Enterprise Management',
    '印刷企业门户': 'Print Enterprise Portal',

    '印刷环保合规': 'Print Environmental Compliance',
    '印刷设备维护': 'Print Equipment Maintenance',
    '印刷设备监控': 'Print Equipment Monitoring',

    '印刷ERP系统': 'Print ERP System',
    '印刷文件管理': 'Print File Management',
    '印刷财务管理': 'Print Financial Management',

    '印刷印后加工': 'Print Finishing Processing',
    '印刷印后软件': 'Print Finishing Software',

    '印刷未来发展': 'Print Future Development',
    '印刷平面设计': 'Print Graphic Design',
    '印刷平面设计工具': 'Print Graphic Design Tools',

    '印刷人力资源': 'Print Human Resources',
    '印刷HR系统': 'Print HR System',

    '印刷行业认证': 'Print Industry Certification',
    '印刷行业标准': 'Print Industry Standards',
    '印刷行业培训': 'Print Industry Training',
    '印刷行业趋势': 'Print Industry Trends',

    '印刷创新管理': 'Print Innovation Management',

    '印刷印前处理': 'Print Prepress Processing',
    '印刷印前': 'Print Prepress',
    '印刷印前处理工具': 'Print Prepress Processing Tools',

    '印刷生产监控': 'Print Production Monitoring',
    '印刷生产报表': 'Print Production Reports',
    '印刷生产排程': 'Print Production Scheduling',

    '印刷质量检验': 'Print Quality Inspection',
    '印刷质量管理': 'Print Quality Management',

    '印刷报价优化': 'Print Quoting Optimization',
    '印刷报价软件': 'Print Quoting Software',

    '印刷报表分析': 'Print Report Analysis',
    '印刷安全管理': 'Print Safety Management',
    '印刷样品管理': 'Print Sample Management',

    '印刷CRM': 'Print CRM',
    '印刷客户门户': 'Print Customer Portal',
    '印刷交付管理': 'Print Delivery Management',
    '印刷电商集成': 'Print E-commerce Integration',
    '印刷员工管理': 'Print Employee Management',
    '印刷库存管理': 'Print Inventory Management',
    '印刷排程软件': 'Print Scheduling Software',
    '印刷排版软件': 'Print Typesetting Software',
    '印刷可变数据印刷': 'Print Variable Data Printing',
    '印刷可变数据': 'Print Variable Data',
    '印刷Web-to-Print': 'Print Web-to-Print',

    # Common business terms
    '印刷企业': 'Print Business',
    '印刷厂': 'Print Shop',
    '印刷行业': 'Print Industry',
    '印刷公司': 'Print Company',
    '印刷业务': 'Print Business',
    '印刷': 'Print',

    # Common descriptors
    '深度评测': 'In-depth Review',
    '全面评测': 'Comprehensive Review',
    '专业评测': 'Professional Review',

    '基础功能': 'Basic Features',
    '高级功能': 'Advanced Features',
    '完整功能': 'Complete Features',

    '性价比高': 'Cost-effective',
    '性价比': 'Cost-effectiveness',
    '便捷': 'Convenient',
    '高效': 'Efficient',
    '专业': 'Professional',
    '实时': 'Real-time',
    '完整': 'Complete',
    '全面': 'Comprehensive',
    '智能': 'Intelligent',
    '自动化': 'Automated',

    # Common verbs
    '提升': 'improve',
    '降低': 'reduce',
    '增加': 'increase',
    '优化': 'optimize',
    '整合': 'integrate',
    '提供': 'provide',
    '支持': 'support',
    '覆盖': 'cover',
    '包含': 'include',
    '生成': 'generate',
    '连接': 'connect',
    '分析': 'analyze',
    '管理': 'manage',
    '监控': 'monitor',
    '跟踪': 'track',
    '预测': 'predict',
    '响应': 'respond',

    # Common nouns
    '效率': 'efficiency',
    '成本': 'cost',
    '效果': 'effectiveness',
    '准确度': 'accuracy',
    '覆盖率': 'coverage',
    '满意度': 'satisfaction',

    '功能': 'features',
    '系统': 'system',
    '平台': 'platform',
    '工具': 'tools',
    '方案': 'solution',
    '服务': 'service',
    '应用': 'application',
    '模块': 'module',

    '报表': 'reports',
    '仪表盘': 'dashboard',
    '数据': 'data',
    '信息': 'information',

    # HTML content common patterns
    '涉及': 'involves',
    '通过': 'through',
    '导致': 'leads to',
    '痛点': 'pain points',
    '呈现': 'presents',
    '定位': 'positions',
    '认为': 'consider',

    '无': 'none',
    '有': 'yes',
    '含': 'includes',
    '含在': 'included in',

    # Numbers and time
    '2026年': '2026',
    '月度': 'monthly',
    '年度': 'annual',
    '未来两年': 'next two years',

    # Pricing patterns
    '许可': 'license',
    '月订阅': 'monthly subscription',
    '用户/月': 'user/month',
    '免费使用': 'free to use',
    '费用': 'cost',

    # Common sentence structures
    '是': 'is',
    '为': 'for',
    '在': 'in',
    '从': 'from',
    '到': 'to',
    '与': 'with',
    '对': 'for',
    '可': 'can',
    '能': 'can',
    '需': 'needs',

    # Misc common words
    '和': 'and',
    '或': 'or',
    '等': 'etc.',
    '已': 'already',
    '将': 'will',
    '应': 'should',
    '最': 'most',
    '更': 'more',
    '新': 'new',
    '旧': 'old',
    '主': 'main',
    '次': 'secondary',
}

def translate_text(text: str) -> str:
    """Translate Chinese text to English, preserving structure"""
    if not text or not re.search(r'[一-鿿]', text):
        return text

    result = text

    # Apply translations - longest matches first (already sorted by length in dict)
    for chinese, english in TRANSLATIONS.items():
        result = result.replace(chinese, english)

    # Clean up any remaining common patterns
    result = result.replace('  ', ' ')  # Remove double spaces
    result = result.strip()

    return result

def translate_file(filepath: Path) -> bool:
    """Translate a single JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if needs translation
        if not re.search(r'[一-鿿]', data.get('title', '')):
            return False

        # Translate all fields
        data['title'] = translate_text(data.get('title', ''))
        data['description'] = translate_text(data.get('description', ''))
        data['content'] = translate_text(data.get('content', ''))

        # Translate keywords array (maintains array format per memory rules)
        if 'seo_keywords' in data and isinstance(data['seo_keywords'], list):
            data['seo_keywords'] = [translate_text(kw) for kw in data['seo_keywords']]

        data['author'] = translate_text(data.get('author', ''))

        # Add language marker
        data['language'] = 'en-US'

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True

    except Exception as e:
        print(f"ERROR: Failed to translate {filepath.name}: {e}")
        return False

def main():
    """Process all files in print-graphic-design-tools directory"""
    base_dir = Path('/Users/gejiayu/owner/seo/data/print-graphic-design-tools')

    # Find all JSON files with Chinese content
    chinese_files = []
    for filepath in base_dir.glob('*.json'):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if re.search(r'[一-鿿]', content):
                chinese_files.append(filepath)

    print(f"Found {len(chinese_files)} files with Chinese content to translate")
    print("="*60)

    success = 0
    failed = 0

    for filepath in sorted(chinese_files):
        if translate_file(filepath):
            success += 1
            print(f" [{success}/{len(chinese_files)}] Translated: {filepath.name}")
        else:
            failed += 1

    print("="*60)
    print(f"Translation complete: {success} success, {failed} skipped")
    return success

if __name__ == '__main__':
    import sys
    sys.exit(main())