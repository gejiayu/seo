#!/usr/bin/env python3
"""
批量翻译英文SEO内容为中文版本
使用标准库 urllib.request（无需安装额外依赖）
处理 customer-support-tools 和 construction-contractor-tools 目录
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any

# 配置
BASE_DIR = Path("/Users/gejiayu/owner/seo/data")

# API配置 - 使用环境变量
API_KEY = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")
BASE_URL = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com")

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
    "SaaS", "B2B", "B2C", "CRM", "ERP", "HRIS", "ATS",
    "GDPR", "CCPA", "HIPAA", "SOC2", "ISO", "PCI", "DSS",
    "UI", "UX", "GUI", "CLI", "IDE", "SDK", "PDF", "CSV",
    "URL", "URI", "HTTP", "TCP", "IP", "DNS", "VPN", "FTP",
    "HTML", "CSS", "JSON", "XML", "YAML", "SQL", "NoSQL",
    "IoT", "5G", "4G", "LTE", "WiFi", "Bluetooth", "USB",
    "Figma", "Sketch", "Adobe", "Photoshop", "Illustrator",
    "Zoom", "Teams", "Notion", "Trello", "Asana", "Monday",
    "Salesforce", "HubSpot", "Zendesk", "Intercom", "Stripe", "PayPal",
    "Shopify", "WooCommerce", "Magento", "BigCommerce",
    "WordPress", "Drupal", "Joomla", "Ghost", "Medium",
    "Procore", "Buildertrend", "CoConstruct", "PlanGrid", "Bluebeam",
    "ServiceNow", "Freshdesk", "Help Scout", "Kustomer", "Gladly",
]


def call_api(prompt: str) -> str:
    """调用Claude API进行翻译（使用urllib）"""
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01"
    }

    data = {
        "model": os.environ.get("ANTHROPIC_DEFAULT_SONNET_MODEL", "glm-5"),
        "max_tokens": 16000,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    url = f"{BASE_URL}/v1/messages"

    try:
        # 创建请求
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        # 发送请求
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result["content"][0]["text"]

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"API调用失败: {e.code} - {error_body[:200]}")
        return ""
    except urllib.error.URLError as e:
        print(f"网络错误: {e.reason}")
        return ""
    except Exception as e:
        print(f"API请求异常: {e}")
        return ""


def translate_file(en_filepath: Path, zh_filepath: Path) -> bool:
    """翻译单个文件"""
    print(f"正在翻译: {en_filepath.name}", flush=True)

    # 加载英文文件
    with open(en_filepath, 'r', encoding='utf-8') as f:
        en_data = json.load(f)

    # 构建翻译提示词
    keep_terms_str = ", ".join(KEEP_ENGLISH[:40])

    # 准备额外内容
    extra_content = ""
    if "pros_and_cons" in en_data:
        pros = en_data["pros_and_cons"].get("pros", [])
        cons = en_data["pros_and_cons"].get("cons", [])
        extra_content += f"\n优点列表：{json.dumps(pros, ensure_ascii=False)}"
        extra_content += f"\n缺点列表：{json.dumps(cons, ensure_ascii=False)}"

    if "faq" in en_data:
        extra_content += f"\nFAQ问答：{json.dumps(en_data['faq'], ensure_ascii=False)}"

    # 分段处理长内容
    content_to_translate = en_data['content']
    if len(content_to_translate) > 8000:
        content_to_translate = content_to_translate[:8000]
        print(f"  注意: 内容过长，截取前8000字符", flush=True)

    prompt = """你是一个专业的SEO内容翻译专家。请将以下英文内容翻译为高质量中文。

**翻译规则（CRITICAL）：**
1. **HTML结构保持完整** - 所有HTML标签必须保留且格式正确（<h2>, <p>, <ul>, <ol>, <li>, <table>, <thead>, <tbody>, <tr>, <th>, <td>, <strong>等）
2. **专业术语保持英文** - 以下术语不翻译：""" + keep_terms_str + """
3. **保持专业性** - 使用专业、自然的中文表达
4. **SEO关键词翻译** - 关键词需要翻译为中文，但要考虑搜索习惯
5. **零Markdown政策** - 翻译后的content字段中禁止出现任何Markdown符号（#, -, *, >, |, []），必须100%使用HTML标签
6. **产品品牌名保持英文** - 如Procore, Buildertrend, Zendesk等品牌名不翻译

**需要翻译的内容：**

标题：""" + en_data['title'] + """

描述：""" + en_data['description'] + """

正文内容（HTML格式）：
""" + content_to_translate + """

SEO关键词：""" + json.dumps(en_data['seo_keywords'], ensure_ascii=False) + """
""" + extra_content + """

**输出格式（仅输出JSON，不要其他内容）：**
```json
{
  "title": "翻译后的中文标题",
  "description": "翻译后的中文描述",
  "content": "翻译后的HTML正文（保持所有HTML标签）",
  "seo_keywords": ["关键词1", "关键词2", "关键词3"],
  "pros_and_cons": {"pros": ["优点翻译"], "cons": ["缺点翻译"]},
  "faq": [{"question": "问题翻译", "answer": "答案翻译"}]
}
```

请确保：
- content字段中所有HTML标签完整且正确
- 表格结构完整（thead/tbody/tr/th/td）
- 无Markdown符号残留
- 专业术语保持英文"""

    # 调用API
    response = call_api(prompt)

    if not response:
        print(f"翻译失败: API无响应", flush=True)
        return False

    # 解析JSON响应
    try:
        # 提取JSON内容
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            response = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            response = response[start:end].strip()

        translated = json.loads(response)

        # 构建中文JSON结构
        zh_data = {
            "title": translated.get("title", en_data["title"]),
            "description": translated.get("description", en_data["description"]),
            "content": translated.get("content", en_data["content"]),
            "seo_keywords": translated.get("seo_keywords", en_data.get("seo_keywords", [])),
            "slug": en_data.get("slug", ""),
            "published_at": en_data.get("published_at", ""),
            "author": en_data.get("author", ""),
            "language": "zh-CN",
            "canonical_link": f"https://www.housecar.life/zh/posts/{en_data.get('slug', '')}",
            "alternate_links": en_data.get("alternate_links", {})
        }

        # 添加可选字段
        if "pros_and_cons" in translated:
            zh_data["pros_and_cons"] = translated["pros_and_cons"]

        if "faq" in translated:
            zh_data["faq"] = translated["faq"]

        # 保存中文文件
        zh_filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(zh_filepath, 'w', encoding='utf-8') as f:
            json.dump(zh_data, f, ensure_ascii=False, indent=2)

        print(f"✓ 翻译成功: {zh_filepath.name}", flush=True)
        return True

    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}", flush=True)
        print(f"响应内容: {response[:200]}", flush=True)
        return False
    except Exception as e:
        print(f"处理失败: {e}", flush=True)
        return False


def process_category(category: str) -> tuple:
    """处理单个类别"""
    category_dir = BASE_DIR / category

    if not category_dir.exists():
        print(f"目录不存在: {category_dir}")
        return 0, 0

    # 获取所有英文JSON文件（排除已有中文版本）
    en_files = [
        f for f in category_dir.glob("*.json")
        if not f.name.endswith(".zh.json")
    ]

    print(f"\n类别: {category}")
    print(f"总文件数: {len(en_files)}")

    success = 0
    failed = 0

    for en_filepath in sorted(en_files):
        # 创建对应的中文文件路径
        zh_filepath = en_filepath.parent / f"{en_filepath.stem}.zh.json"

        # 如果中文文件已存在，跳过
        if zh_filepath.exists():
            print(f"⊗ 已存在: {zh_filepath.name}")
            continue

        # 翻译文件
        if translate_file(en_filepath, zh_filepath):
            success += 1
        else:
            failed += 1

        # 进度报告
        if (success + failed) % 10 == 0:
            print(f"进度: {success + failed}/{len(en_files)} 已处理")

        # API限速（避免超速）
        time.sleep(0.3)

    print(f"类别 {category} 完成: 成功 {success}, 失败 {failed}")
    return success, failed


def main():
    """主函数"""
    # 检查API密钥
    if not API_KEY:
        print("错误: 请设置 ANTHROPIC_API_KEY 或 ANTHROPIC_AUTH_TOKEN 环境变量")
        print("提示: 可以运行 'export ANTHROPIC_API_KEY=your_key' 设置环境变量")
        sys.exit(1)

    # 要处理的类别
    categories = [
        "customer-support-tools",
        "construction-contractor-tools"
    ]

    print("=" * 60)
    print("开始批量翻译英文SEO内容为中文")
    print(f"目标类别: {', '.join(categories)}")
    print("=" * 60)

    total_success = 0
    total_failed = 0

    for category in categories:
        s, f = process_category(category)
        total_success += s
        total_failed += f

    print("\n" + "=" * 60)
    print(f"翻译完成")
    print(f"成功: {total_success} 个文件")
    print(f"失败: {total_failed} 个文件")
    print(f"总计: {total_success + total_failed} 个文件处理")
    print("=" * 60)


if __name__ == "__main__":
    main()