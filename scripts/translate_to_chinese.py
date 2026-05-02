#!/usr/bin/env python3
"""
批量翻译SEO内容为中文
使用DashScope/Claude API进行高质量翻译
"""

import json
import os
import sys
import time
import requests
from pathlib import Path
from typing import Dict, Any, Optional

# 配置
BASE_DIR = Path("/Users/gejiayu/owner/seo/data")
ZH_DIR = BASE_DIR / "zh"

API_KEY = os.environ.get("ANTHROPIC_AUTH_TOKEN")
BASE_URL = os.environ.get("ANTHROPIC_BASE_URL", "https://dashscope.aliyuncs.com/apps/anthropic")

# 不翻译的专业术语
KEEP_ENGLISH = [
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
]


def call_api(prompt: str) -> str:
    """调用Claude API"""
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01"
    }

    data = {
        "model": "claude-sonnet-4-6-20250514",
        "max_tokens": 16000,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    url = f"{BASE_URL}/v1/messages"

    response = requests.post(url, headers=headers, json=data, timeout=120)

    if response.status_code == 200:
        result = response.json()
        return result["content"][0]["text"]
    else:
        raise Exception(f"API调用失败: {response.status_code} - {response.text}")


def load_json(filepath: Path) -> Dict[str, Any]:
    """加载JSON文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(filepath: Path, data: Dict[str, Any]) -> None:
    """保存JSON文件"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def needs_translation(filepath: Path) -> bool:
    """检查文件是否需要翻译"""
    try:
        data = load_json(filepath)
        title = data.get("title", "")
        return title.startswith("[待翻译]") or title.startswith("[需要翻译]")
    except:
        return True


def translate_file(en_filepath: Path, zh_filepath: Path) -> bool:
    """翻译单个文件"""
    # 加载EN文件
    en_data = load_json(en_filepath)

    # 构建翻译提示词
    keep_terms_str = ", ".join(KEEP_ENGLISH[:30])

    extra_content = ""
    if "pros_and_cons" in en_data:
        pros = en_data["pros_and_cons"].get("pros", [])
        cons = en_data["pros_and_cons"].get("cons", [])
        extra_content += f"\n优点：{json.dumps(pros, ensure_ascii=False)}"
        extra_content += f"\n缺点：{json.dumps(cons, ensure_ascii=False)}"

    if "faq" in en_data:
        extra_content += f"\nFAQ：{json.dumps(en_data['faq'], ensure_ascii=False)}"

    prompt = f"""你是一个专业的SEO内容翻译专家。请将以下英文内容翻译为中文。

**翻译规则：**
1. 保持HTML标签结构不变（<h2>, <p>, <table>, <li>, <thead>, <tbody>, <tr>, <td>, <th>等）
2. 专业术语保持英文：{keep_terms_str}
3. 保持原文的专业性和准确性
4. 使用自然的中文表达
5. 产品名和品牌名保持英文

**翻译内容：**

标题：{en_data['title']}

描述：{en_data['description']}

正文（HTML格式）：{en_data['content'][:8000]}
{extra_content}

**输出格式（JSON）：**
```json
{
  "title": "翻译后的中文标题",
  "description": "翻译后的中文描述（150-160字符）",
  "content": "翻译后的HTML正文内容",
  "pros_and_cons": {"pros": ["优点列表"], "cons": ["缺点列表"]},
  "faq": [{"question": "问题", "answer": "答案"}]
}
```

只输出JSON，不要其他内容。"""

    try:
        # 调用API
        response = call_api(prompt)

        # 解析JSON
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            response = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            response = response[start:end].strip()

        translated = json.loads(response)

        # 更新ZH文件
        zh_data = {
            "title": translated.get("title", en_data["title"]),
            "description": translated.get("description", en_data["description"]),
            "content": translated.get("content", en_data["content"]),
            "seo_keywords": en_data.get("seo_keywords", []),
            "slug": en_data.get("slug", ""),
            "published_at": en_data.get("published_at", ""),
            "author": en_data.get("author", ""),
            "language": "zh-CN",
            "canonical_link": f"https://www.housecar.life/zh/posts/{en_data.get('slug', '')}",
            "alternate_links": en_data.get("alternate_links", {}),
            "category": en_data.get("category", "")
        }

        if "pros_and_cons" in translated:
            zh_data["pros_and_cons"] = translated["pros_and_cons"]

        if "faq" in translated:
            zh_data["faq"] = translated["faq"]

        save_json(zh_filepath, zh_data)
        return True

    except Exception as e:
        print(f"翻译失败: {e}")
        return False


def process_category(category: str, limit: int = 0) -> tuple:
    """处理一个类别"""
    en_dir = BASE_DIR / category
    zh_dir = ZH_DIR / category

    if not zh_dir.exists():
        print(f"ZH目录不存在: {zh_dir}")
        return 0, 0

    zh_files = list(zh_dir.glob("*.json"))
    to_translate = [f for f in zh_files if needs_translation(f)]

    if limit > 0:
        to_translate = to_translate[:limit]

    print(f"\n类别 {category}: 共{len(zh_files)}个文件，待翻译{len(to_translate)}个")

    success = 0
    failed = 0

    for zh_filepath in to_translate:
        slug = zh_filepath.stem
        en_filepath = en_dir / zh_filepath.name

        if not en_filepath.exists():
            print(f"EN文件不存在: {en_filepath}")
            failed += 1
            continue

        print(f"翻译: {slug}")

        if translate_file(en_filepath, zh_filepath):
            success += 1
        else:
            failed += 1

        # 报告进度
        if success % 20 == 0:
            print(f"进度: {success}/{len(to_translate)} 已翻译")

        # API限速
        time.sleep(0.5)

    print(f"完成 {category}: 成功{success}, 失败{failed}")
    return success, failed


def main():
    """主函数"""
    if not API_KEY:
        print("请设置ANTHROPIC_AUTH_TOKEN环境变量")
        sys.exit(1)

    # 需要处理的类别
    categories = [
        "hr-recruitment-tools",
        "insurance-agency-tools",
        "insurance-claims-processing-tools",
        "jewelry-watch-retail-tools",
        "kitchen-cooking-rental-tools",
        "landscaping-grounds-maintenance",
    ]

    total_success = 0
    total_failed = 0

    # 每个类别限制处理数量（用于测试，设为0处理全部）
    LIMIT_PER_CATEGORY = int(os.environ.get("TRANSLATE_LIMIT", "0"))

    for category in categories:
        s, f = process_category(category, limit=LIMIT_PER_CATEGORY)
        total_success += s
        total_failed += f

    print(f"\n总计: 成功翻译 {total_success} 个文件, 失败 {total_failed} 个")


if __name__ == "__main__":
    main()