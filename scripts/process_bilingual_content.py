#!/usr/bin/env python3
"""
双语SEO内容处理脚本
正确规范：
- 每个原始文件 → 生成两个独立JSON文件
- 英文版：data/[category]/[slug].json（language: "en-US"）
- 中文版：data/zh/[category]/[slug].json（language: "zh-CN"）
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any

BASE_DIR = Path("/Users/gejiayu/owner/seo/data")
ZH_DIR = BASE_DIR / "zh"
SITE_URL = "https://www.housecar.life"

# 不翻译的专业术语列表
KEEP_ENGLISH_TERMS = [
    "Slack", "JIRA", "API", "SDK", "AWS", "Azure", "GCP", "Google Cloud",
    "Microsoft", "Apple", "iOS", "Android", "Linux", "Windows", "Mac",
    "Python", "JavaScript", "TypeScript", "Java", "Go", "Rust", "Ruby",
    "React", "Vue", "Angular", "Next.js", "Node.js", "Django", "Spring",
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "Kafka",
    "Docker", "Kubernetes", "CI/CD", "Git", "GitHub", "GitLab",
    "REST", "GraphQL", "OAuth", "JWT", "SSL", "TLS", "HTTPS",
    "AI", "ML", "NLP", "LLM", "GPT", "ChatGPT", "Claude", "OpenAI",
    "SaaS", "B2B", "B2C", "CRM", "ERP", "HRIS", "ATS", "API",
    "GDPR", "CCPA", "HIPAA", "SOC2", "ISO", "PCI", "DSS",
    "UI", "UX", "GUI", "CLI", "IDE", "SDK", "PDF", "CSV",
    "URL", "URI", "HTTP", "TCP", "IP", "DNS", "VPN", "FTP",
    "PDF", "HTML", "CSS", "JSON", "XML", "YAML", "SQL", "NoSQL",
    "IoT", "5G", "4G", "LTE", "WiFi", "Bluetooth", "USB",
    "Figma", "Sketch", "Adobe", "Photoshop", "Illustrator",
    "Zoom", "Teams", "Slack", "Notion", "Trello", "Asana", "Monday",
    "Salesforce", "HubSpot", "Zendesk", "Intercom", "Stripe", "PayPal",
    "Shopify", "WooCommerce", "Magento", "BigCommerce",
    "WordPress", "Drupal", "Joomla", "Ghost", "Medium",
    "Terraform", "Ansible", "Puppet", "Chef", "Vagrant",
    "Paradox Olivia", "HireVue", "Pymetrics", "MyInterview", "Clovers",
    "LogicGate", "SailPoint", "ServiceNow", "Archer", "Convercent",
    "Diligent", "AuditBoard", "OneTrust", "Resolver",
    # 添加更多常见品牌和术语
]


def load_json(filepath: Path) -> Dict[str, Any]:
    """加载JSON文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(filepath: Path, data: Dict[str, Any]) -> None:
    """保存JSON文件"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def update_en_file(data: Dict[str, Any], category: str, slug: str) -> Dict[str, Any]:
    """更新英文文件，添加语言和链接字段"""
    en_url = f"{SITE_URL}/posts/{slug}"
    zh_url = f"{SITE_URL}/zh/posts/{slug}"

    # 添加必要字段
    if "language" not in data:
        data["language"] = "en-US"

    if "canonical_link" not in data:
        data["canonical_link"] = en_url

    if "alternate_links" not in data:
        data["alternate_links"] = {
            "en-US": en_url,
            "zh-CN": zh_url
        }

    if "category" not in data:
        data["category"] = category

    return data


def translate_content(content: str) -> str:
    """
    翻译内容为中文（简单占位，实际需要调用翻译API）
    这里返回标记内容，实际处理时需要使用翻译服务
    """
    # 这里只返回占位符，实际翻译需要在外部处理
    return f"[需要翻译]\n{content}"


def translate_title(title: str) -> str:
    """翻译标题"""
    return f"[待翻译] {title}"


def translate_description(desc: str) -> str:
    """翻译描述"""
    return f"[需要翻译] {desc}"


def create_zh_version(en_data: Dict[str, Any], category: str, slug: str) -> Dict[str, Any]:
    """创建中文版本"""
    en_url = f"{SITE_URL}/posts/{slug}"
    zh_url = f"{SITE_URL}/zh/posts/{slug}"

    zh_data = {
        "title": translate_title(en_data.get("title", "")),
        "description": translate_description(en_data.get("description", "")),
        "content": translate_content(en_data.get("content", "")),
        "seo_keywords": en_data.get("seo_keywords", []),
        "slug": slug,
        "published_at": en_data.get("published_at", ""),
        "author": en_data.get("author", ""),
        "language": "zh-CN",
        "canonical_link": zh_url,
        "alternate_links": {
            "en-US": en_url,
            "zh-CN": zh_url
        },
        "category": category
    }

    # 保留可选字段
    if "pros_and_cons" in en_data:
        zh_data["pros_and_cons"] = {
            "pros": [f"[待翻译] {p}" for p in en_data["pros_and_cons"]["pros"]],
            "cons": [f"[待翻译] {c}" for c in en_data["pros_and_cons"]["cons"]]
        }

    if "faq" in en_data:
        zh_data["faq"] = [
            {
                "question": f"[待翻译] {q['question']}",
                "answer": f"[待翻译] {q['answer']}"
            }
            for q in en_data["faq"]
        ]

    return zh_data


def process_category(category: str) -> tuple:
    """处理单个类别"""
    en_dir = BASE_DIR / category
    zh_dir = ZH_DIR / category

    if not en_dir.exists():
        print(f"EN目录不存在: {en_dir}")
        return 0, 0

    # 创建ZH目录
    zh_dir.mkdir(parents=True, exist_ok=True)

    files = list(en_dir.glob("*.json"))
    processed_en = 0
    processed_zh = 0

    for filepath in files:
        slug = filepath.stem

        try:
            # 加载EN文件
            en_data = load_json(filepath)

            # 更新EN文件
            en_data = update_en_file(en_data, category, slug)
            save_json(filepath, en_data)
            processed_en += 1

            # 创建ZH版本（如果不存在）
            zh_filepath = zh_dir / filepath.name
            if not zh_filepath.exists():
                zh_data = create_zh_version(en_data, category, slug)
                save_json(zh_filepath, zh_data)
                processed_zh += 1

            if processed_en % 20 == 0:
                print(f"进度: {processed_en}/{len(files)} 文件已处理")

        except Exception as e:
            print(f"处理失败: {filepath}, 错误: {e}")

    return processed_en, processed_zh


def main():
    """主函数"""
    # 需要处理的类别
    categories = [
        "hr-recruitment-tools",
        "insurance-agency-tools",
        "insurance-claims-processing-tools",
        "jewelry-watch-retail-tools",
        "kitchen-cooking-rental-tools",
        "landscaping-grounds-maintenance",
    ]

    total_en = 0
    total_zh = 0

    for category in categories:
        print(f"\n处理类别: {category}")
        en_count, zh_count = process_category(category)
        total_en += en_count
        total_zh += zh_count
        print(f"完成: {category} - EN更新: {en_count}, ZH创建: {zh_count}")

    print(f"\n总计: EN更新: {total_en}, ZH创建: {total_zh}")

    # 输出下一步翻译指令
    print("\n下一步: 需要运行翻译脚本处理ZH目录中的[待翻译]内容")


if __name__ == "__main__":
    main()