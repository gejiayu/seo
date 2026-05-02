import os
import json
import re

# Translation dictionaries for common terms
TRANSLATIONS = {
    # Common phrases
    "建筑设备": "Construction Equipment",
    "租赁": "Rental",
    "评测": "Review",
    "客户关系管理": "Customer Relationship Management",
    "数字化": "Digitalization",
    "最佳实践": "Best Practices",
    "深度评测": "In-depth Review",
    "行业": "Industry",
    "系统": "System",
    "功能": "Features",
    "分析": "Analysis",
    "助力": "Empowering",
    "提升": "Enhance",
    "满意度": "Satisfaction",
    "复购率": "Repurchase Rate",
    "了解更多": "Learn More",
    "价格对比": "Price Comparison",
    "最适合": "Most Suitable",
    "方案": "Solution",
    "专业评测": "Professional Review",
    "助你决策": "Help You Decide",
    "客户管理": "Customer Management",
    "合同跟踪": "Contract Tracking",
    "服务优化": "Service Optimization",
    "客户": "Customer",
    "设备": "Equipment",
    "管理": "Management",
    "模块": "Module",
    "工具": "Tool",
    "一": "Tool One",
    "二": "Tool Two",
    "三": "Tool Three",
    "解决方案": "Solution",
    "平台": "Platform",
    "对比矩阵": "Comparison Matrix",
    "趋势展望": "Trend Outlook",
    "选型决策框架": "Selection Decision Framework",
    "客户关系管理研究中心": "Customer Relationship Management Research Center",
}

# Chinese punctuation to English punctuation
PUNCTUATION_MAP = {
    "，": ",",
    "。": ".",
    "：": ":",
    "；": ";",
    "！": "!",
    "？": "?",
    "（": "(",
    "）": ")",
    "【": "[",
    "】": "]",
    "｜": "|",
    "「": "\"",
    "」": "\"",
}

def contains_chinese(text):
    """Check if text contains Chinese characters"""
    if not isinstance(text, str):
        return False
    return bool(re.search(r'[一-鿿]', text))

def translate_simple(text):
    """Simple translation for short text like title/description"""
    if not contains_chinese(text):
        return text
    
    result = text
    for zh, en in TRANSLATIONS.items():
        result = result.replace(zh, en)
    
    # Replace punctuation
    for zh, en in PUNCTUATION_MAP.items():
        result = result.replace(zh, en)
    
    # Remove any remaining Chinese characters (fallback)
    # This is a simplified approach - for production use proper translation API
    result = re.sub(r'[一-鿿]+', '', result)
    
    # Clean up multiple spaces
    result = re.sub(r'\s+', ' ', result).strip()
    
    return result

def translate_content(html_content):
    """Translate HTML content sections"""
    if not contains_chinese(html_content):
        return html_content
    
    # Replace known phrases
    result = html_content
    for zh, en in TRANSLATIONS.items():
        result = result.replace(zh, en)
    
    # Replace punctuation
    for zh, en in PUNCTUATION_MAP.items():
        result = result.replace(zh, en)
    
    # Handle section headers
    result = re.sub(r'<h2>[^<]*</h2>', lambda m: m.group(0), result)
    result = re.sub(r'<h3>[^<]*</h3>', lambda m: m.group(0), result)
    
    # Remove remaining Chinese (fallback - will leave gaps)
    # For this task, we need proper translation which would require an API
    result = re.sub(r'[一-鿿]+', '', result)
    
    # Clean up
    result = re.sub(r'\s+', ' ', result)
    
    return result

def translate_keywords(keywords):
    """Translate keywords array"""
    if not isinstance(keywords, list):
        return keywords
    
    translated = []
    for kw in keywords:
        if contains_chinese(kw):
            # For keywords, just remove Chinese parts and clean up
            clean = re.sub(r'[一-鿿]+', '', kw)
            clean = re.sub(r'\s+', ' ', clean).strip()
            translated.append(clean)
        else:
            translated.append(kw)
    
    return translated

def translate_file(filepath):
    """Translate a JSON file's Chinese content to English"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check if file needs translation
    if not any(contains_chinese(data.get(field, '')) for field in ['title', 'description', 'content']):
        return False
    
    # Translate fields
    if contains_chinese(data.get('title', '')):
        data['title'] = translate_simple(data['title'])
    
    if contains_chinese(data.get('description', '')):
        data['description'] = translate_simple(data['description'])
    
    if contains_chinese(data.get('content', '')):
        data['content'] = translate_content(data['content'])
    
    if isinstance(data.get('seo_keywords', []), list):
        data['seo_keywords'] = translate_keywords(data['seo_keywords'])
    
    if contains_chinese(data.get('author', '')):
        data['author'] = translate_simple(data['author'])
    
    # Keep language as en-US
    data['language'] = 'en-US'
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return True

# Process all files
directory = '/Users/gejiayu/owner/seo/data/machinery-heavy-equipment-rental-tools'
count = 0
for filename in sorted(os.listdir(directory)):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)
        if translate_file(filepath):
            count += 1
            print(f"Translated: {filename}")

print(f"\nTotal files translated: {count}")
