#!/usr/bin/env python3
"""
Refinement script to convert mechanical translations to natural American English
following SEO best practices for education technology websites
"""
import json
import os
import re
from pathlib import Path

def refine_title(title):
    """Convert title to natural SEO-optimized English"""
    if not title:
        return title
    
    # Common title pattern fixes
    title = title.replace("Review:", "Review:")
    title = title.replace("Comparison｜", "vs")
    title = title.replace("｜", ":")
    title = title.replace("Small Business", "Small Business")
    title = re.sub(r'([A-Z][a-z]+)([A-Z][a-z]+)', r'\1 \2', title)  # Add spaces between joined words
    
    # Specific fixes
    title = title.replace("Learning Management SystemReview", "Learning Management System Review")
    title = title.replace("Online CoursePlatform", "Online Course Platform")
    
    return title.strip()

def refine_description(desc):
    """Convert description to natural fluent English"""
    if not desc:
        return desc
    
    # Fix common patterns
    desc = desc.replace("In-depth Review2026", "In-depth 2026 Review")
    desc = desc.replace("From", "From")
    desc = desc.replace("To", "to")
    desc = desc.replace("Help", "Help")
    desc = desc.replace("Learn More", "Learn more about")
    desc = desc.replace("Find Your Best Solution", "Find the best solution")
    
    # Remove awkward punctuation
    desc = re.sub(r'、', ', ', desc)
    desc = re.sub(r'；', '; ', desc)
    
    # Fix spacing
    desc = re.sub(r'\s+', ' ', desc)
    
    return desc.strip()

def refine_keywords(keywords):
    """Refine SEO keywords to proper English"""
    if not keywords or not isinstance(keywords, list):
        return keywords
    
    refined = []
    for kw in keywords:
        # Fix common patterns
        kw = kw.replace("Platform", " platform")
        kw = kw.replace("System", " system")
        kw = kw.replace("工具", "tool")
        kw = kw.replace("软件", "software")
        
        # Remove Chinese characters if any remain
        kw = re.sub(r'[一-鿿]', '', kw)
        
        # Fix spacing
        kw = re.sub(r'\s+', ' ', kw).strip()
        
        if kw:
            refined.append(kw)
    
    return refined

def refine_author(author):
    """Standardize author names"""
    if not author:
        return "Education Technology Research Team"
    
    # Standard patterns
    author = author.replace("LMS Technology Research Team", "Education Technology Research Team")
    author = author.replace("Technology Research Team", "Education Technology Research Team")
    
    return author

def refine_content_field(content):
    """Refine HTML content to natural professional English"""
    if not content or not isinstance(content, str):
        return content
    
    # Fix punctuation
    content = content.replace('、', ', ')
    content = content.replace('；', '; ')
    content = content.replace('。', '. ')
    content = content.replace('：', ': ')
    
    # Fix common mechanical translations
    content = content.replace("is数字化教育", "is the digital education")
    content = content.replace("Provide", "provide")
    content = content.replace("provide了", "provide")
    content = content.replace("Has", "has")
    content = content.replace("Include", "include")
    content = content.replace("Suitable for", "Suitable for")
    content = content.replace("need", "need")
    content = content.replace("Should", "should")
    content = content.replace("in线", "online")
    content = content.replace("in", "in")
    content = content.replace("From", "from")
    content = content.replace("To", "to")
    
    # Fix word spacing
    content = re.sub(r'([a-z])([A-Z])', r'\1 \2', content)
    
    # Remove remaining Chinese
    content = re.sub(r'[一-鿿]', '', content)
    
    # Clean spacing
    content = re.sub(r'\s+', ' ', content)
    
    return content

def refine_pros_cons_item(item):
    """Refine a single pros or cons string"""
    if not item:
        return item
    
    # Fix punctuation
    item = item.replace('、', ', ')
    item = item.replace('；', '; ')
    
    # Fix spacing
    item = re.sub(r'([a-z])([A-Z])', r'\1 \2', item)
    item = re.sub(r'\s+', ' ', item)
    
    # Remove Chinese
    item = re.sub(r'[一-鿿]', '', item)
    
    return item.strip()

def process_file(filepath):
    """Process and refine a single JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Refine each field
        data['title'] = refine_title(data.get('title', ''))
        data['description'] = refine_description(data.get('description', ''))
        data['author'] = refine_author(data.get('author', ''))
        data['seo_keywords'] = refine_keywords(data.get('seo_keywords', []))
        data['content'] = refine_content_field(data.get('content', ''))
        
        # Refine pros and cons
        if data.get('pros_and_cons'):
            for tool_item in data['pros_and_cons']:
                tool_item['pros'] = [refine_pros_cons_item(p) for p in tool_item.get('pros', [])]
                tool_item['cons'] = [refine_pros_cons_item(c) for c in tool_item.get('cons', [])]
        
        # Refine FAQ
        if data.get('faq'):
            for faq_item in data['faq']:
                faq_item['question'] = refine_pros_cons_item(faq_item.get('question', ''))
                faq_item['answer'] = refine_pros_cons_item(faq_item.get('answer', ''))
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error refining {filepath}: {e}")
        return False

def main():
    """Refine all education-tools JSON files"""
    base_dir = Path('/Users/gejiayu/owner/seo/data/education-tools')
    json_files = list(base_dir.glob('*.json'))
    
    print(f"Refining {len(json_files)} JSON files")
    
    success_count = 0
    for filepath in json_files:
        if process_file(filepath):
            success_count += 1
            print(f"✓ Refined: {filepath.name}")
        else:
            print(f"✗ Failed: {filepath.name}")
    
    print(f"\nSuccessfully refined {success_count}/{len(json_files)} files")

if __name__ == '__main__':
    main()
