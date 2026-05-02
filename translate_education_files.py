#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path

# Translation dictionary for common Chinese terms to natural English
TRANSLATION_MAP = {
    # Common Chinese phrases with natural English equivalents
    "背景介绍": "Background Introduction",
    "核心功能对比": "Core Feature Comparison",
    "功能维度": "Feature Dimension",
    "适用场景": "Applicable Scenario",
    "平台详解": "Platform Details",
    "核心能力": "Core Capabilities",
    "技术架构": "Technical Architecture",
    "功能亮点": "Feature Highlights",
    "定价模式": "Pricing Model",
    "优势劣势": "Pros and Cons",
    "对比总结表": "Comparison Summary Table",
    "评估维度": "Evaluation Dimension",
    "选择建议": "Selection Recommendations",
    "中小企业推荐": "Small Business Recommendation",
    "技术能力强的机构": "Technically Capable Organizations",
    "大型企业和认证机构": "Large Enterprises and Certification Bodies",
    "趋势预测": "Trend Predictions",
    "市场竞争格局": "Market Competition Landscape",
    
    # Common mixed Chinese/English patterns
    "评测": "Review",
    "对比": "Comparison",
    "对比｜": "vs",
    "｜": ":",
    "最佳": "Best",
    "深入": "In-depth",
    "全方位": "Comprehensive",
    "帮助": "Help",
    "了解更多": "Learn More",
    "找到最适合": "Find the Best",
    "方案": "Solution",
    "专业": "Professional",
    "决策": "Decision",
    
    # Specific domain terms
    "学习管理系统": "Learning Management System",
    "在线课程平台": "Online Course Platform",
    "课程管理": "Course Management",
    "用户体验": "User Experience",
    "技术集成": "Technical Integration",
    "价格体系": "Pricing Structure",
    "教育机构": "Educational Institutions",
    "中小企业": "Small to Medium Businesses",
    "企业培训": "Corporate Training",
    
    # Common descriptors
    "友好": "User-friendly",
    "直观": "Intuitive",
    "灵活": "Flexible",
    "强大": "Powerful",
    "完善": "Complete",
    "丰富": "Rich",
    "深度": "In-depth",
    "优秀": "Excellent",
    "便捷": "Convenient",
    
    # Numbers and metrics
    "分": "points",
    "评分": "Score",
    "权重": "Weight",
    "综合": "Overall",
    
    # Connectors and transitions
    "和": "and",
    "的": "",
    "是": "is",
    "在": "in",
    "从": "from",
    "到": "to",
    "方面": "aspect",
    "具有": "has",
    "提供": "provides",
    "支持": "supports",
    "包括": "includes",
    "适合": "suitable for",
    "优先": "prioritize",
    "需要": "need",
    "应该": "should",
    
    # Questions
    "应该选择": "Should Choose",
    "如何评估": "How to Evaluate",
    "是否支持": "Does it Support",
    "有什么": "What are",
    "是什么": "What is",
    "怎么样": "How is",
}

def translate_text(text):
    """Translate mixed Chinese/English text to natural English"""
    if not text or not isinstance(text, str):
        return text
    
    # Check if text contains Chinese characters
    if not re.search(r'[一-鿿]', text):
        return text
    
    # Apply translations
    result = text
    for chinese, english in TRANSLATION_MAP.items():
        result = result.replace(chinese, english)
    
    # Clean up extra spaces and formatting issues
    result = re.sub(r'\s+', ' ', result)  # Multiple spaces to single space
    result = result.strip()
    
    return result

def translate_content_field(content):
    """Translate the HTML content field"""
    if not content or not isinstance(content, str):
        return content
    
    # Check if contains Chinese
    if not re.search(r'[一-鿿]', content):
        return content
    
    # Apply translations
    result = content
    for chinese, english in TRANSLATION_MAP.items():
        result = result.replace(chinese, english)
    
    return result

def translate_author(author):
    """Translate author name to natural English equivalent"""
    if not author:
        return "Education Technology Research Team"
    
    # Common Chinese author patterns
    author_map = {
        "教育技术专家": "Education Technology Research Team",
        "LMS技术专家": "LMS Technology Research Team",
        "在线教育专家": "Online Education Research Team",
        "教育管理专家": "Education Management Research Team",
        "课程设计专家": "Course Design Research Team",
        "教学技术专家": "Instructional Technology Research Team",
    }
    
    return author_map.get(author, "Education Technology Research Team")

def translate_seo_keywords(keywords):
    """Translate SEO keywords array"""
    if not keywords or not isinstance(keywords, list):
        return keywords
    
    translated = []
    for keyword in keywords:
        translated_kw = translate_text(keyword)
        translated.append(translated_kw)
    
    return translated

def translate_pros_cons(pros_cons_list):
    """Translate pros and cons arrays"""
    if not pros_cons_list or not isinstance(pros_cons_list, list):
        return pros_cons_list
    
    translated = []
    for item in pros_cons_list:
        translated_item = {
            "tool": item.get("tool", ""),
            "pros": [translate_text(p) for p in item.get("pros", [])],
            "cons": [translate_text(c) for c in item.get("cons", [])]
        }
        translated.append(translated_item)
    
    return translated

def translate_faq(faq_list):
    """Translate FAQ array"""
    if not faq_list or not isinstance(faq_list, list):
        return faq_list
    
    translated = []
    for item in faq_list:
        translated_item = {
            "question": translate_text(item.get("question", "")),
            "answer": translate_text(item.get("answer", ""))
        }
        translated.append(translated_item)
    
    return translated

def process_file(filepath):
    """Process a single JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Translate each field
        data['title'] = translate_text(data.get('title', ''))
        data['description'] = translate_text(data.get('description', ''))
        data['author'] = translate_author(data.get('author', ''))
        data['seo_keywords'] = translate_seo_keywords(data.get('seo_keywords', []))
        data['content'] = translate_content_field(data.get('content', ''))
        data['pros_and_cons'] = translate_pros_cons(data.get('pros_and_cons', []))
        data['faq'] = translate_faq(data.get('faq', []))
        
        # Keep slug, category, published_at unchanged
        # Ensure language is set to en-US (if field exists)
        if 'language' in data:
            data['language'] = 'en-US'
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Process all education-tools JSON files"""
    base_dir = Path('/Users/gejiayu/owner/seo/data/education-tools')
    json_files = list(base_dir.glob('*.json'))
    
    print(f"Found {len(json_files)} JSON files to process")
    
    success_count = 0
    for filepath in json_files:
        if process_file(filepath):
            success_count += 1
            print(f"✓ Processed: {filepath.name}")
        else:
            print(f"✗ Failed: {filepath.name}")
    
    print(f"\nSuccessfully processed {success_count}/{len(json_files)} files")

if __name__ == '__main__':
    main()
