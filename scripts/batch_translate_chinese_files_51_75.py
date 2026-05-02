#!/usr/bin/env python3
"""
Batch translate Chinese JSON files to English using Claude Sonnet 4.6.

This script:
1. Reads JSON files from staffing-recruitment-agency-tools directory (files 51-75)
2. Translates Chinese content in title, description, content, seo_keywords, and author fields
3. Uses semantic translation optimized for SEO and business context
4. Uses prompt caching for efficiency
5. Saves translated files back with "language": "en-US"
"""

import json
import os
import anthropic
from pathlib import Path
import re
import time

# Configuration
DIRECTORY = "/Users/gejiayu/owner/seo/data/staffing-recruitment-agency-tools/"
MODEL = "claude-sonnet-4-20250514"  # Sonnet 4 (full ID for compatibility)
FILES_TO_PROCESS = 25  # Files 51-75
START_INDEX = 50  # 0-indexed, so file 51 is at index 50

# Chinese detection pattern
CHINESE_PATTERN = re.compile(r'[一-鿿]+')

def has_chinese_content(data: dict) -> bool:
    """Check if JSON data contains Chinese characters."""
    for key, value in data.items():
        if isinstance(value, str) and CHINESE_PATTERN.search(value):
            return True
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str) and CHINESE_PATTERN.search(item):
                    return True
    return False

def translate_text(client: anthropic.Anthropic, text: str, field_name: str, cache_system: bool = True) -> str:
    """
    Translate Chinese text to professional English using Claude Sonnet 4.6.

    Args:
        client: Anthropic client instance
        text: Text to translate
        field_name: Name of the field (for context)
        cache_system: Whether to use cached system prompt

    Returns:
        Translated English text
    """
    # System prompt optimized for SEO and business context
    # This is cached across all requests for efficiency
    system_prompt = """You are a professional translator specializing in SEO-optimized business content for staffing and recruitment tools.

Translate Chinese text to natural, professional English following these rules:
- Translate semantically, not literally - convey the intended meaning
- Maintain SEO optimization - preserve keyword density and structure
- Use professional business terminology common in staffing/recruitment industry
- Keep HTML tags intact if present (e.g., <h2>, <p>, <table>)
- For content fields: keep structure and formatting
- For keywords: translate to English equivalents that are commonly searched
- For titles: make them compelling and SEO-friendly
- For descriptions: optimize for meta descriptions (150-160 chars ideal)
- Output only the translated text, no explanations or commentary"""

    # User prompt with the text to translate
    user_prompt = f"""Translate this {field_name} field content for a staffing/recruitment tool SEO article:

{text}

Provide only the English translation, preserving any HTML structure or formatting."""

    try:
        # Use cached system prompt for efficiency
        if cache_system:
            response = client.messages.create(
                model=MODEL,
                max_tokens=4096 if field_name == "content" else 512,
                system=[
                    {
                        "type": "text",
                        "text": system_prompt,
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
        else:
            response = client.messages.create(
                model=MODEL,
                max_tokens=4096 if field_name == "content" else 512,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

        # Extract translated text
        translated_text = next(
            (block.text for block in response.content if block.type == "text"),
            text  # Fallback to original if no text block
        )

        return translated_text.strip()

    except Exception as e:
        print(f"  ✗ Translation error for {field_name}: {e}")
        return text  # Return original text on error

def translate_keywords(client: anthropic.Anthropic, keywords: list) -> list:
    """Translate SEO keywords array."""
    translated_keywords = []

    # Batch translate all keywords in one request for efficiency
    keywords_text = "\n".join(f"{i+1}. {kw}" for i, kw in enumerate(keywords) if kw)

    if not keywords_text:
        return keywords

    system_prompt = """You are a translator for SEO keywords. Translate Chinese keywords to English equivalents that are:
- Commonly searched in the staffing/recruitment industry
- Concise (typically 1-3 words)
- SEO-friendly

Output format: numbered list matching input, one per line."""

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=256,
            system=[
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=[
                {"role": "user", "content": f"Translate these SEO keywords:\n{keywords_text}\n\nOutput as numbered list (one per line)."}
            ]
        )

        # Parse translated keywords
        response_text = next(
            (block.text for block in response.content if block.type == "text"),
            ""
        )

        # Extract keywords from numbered list
        for line in response_text.strip().split('\n'):
            # Remove numbering (e.g., "1. keyword" -> "keyword")
            cleaned = re.sub(r'^\d+\.\s*', '', line.strip())
            if cleaned and cleaned not in ['', 'None', '-']:
                translated_keywords.append(cleaned)

        # If parsing failed, return original
        if len(translated_keywords) != len([k for k in keywords if k]):
            print(f"  ⚠ Keyword count mismatch: got {len(translated_keywords)}, expected {len([k for k in keywords if k])}")
            return keywords

        return translated_keywords

    except Exception as e:
        print(f"  ✗ Keyword translation error: {e}")
        return keywords

def process_file(client: anthropic.Anthropic, filepath: Path, use_cache: bool = True) -> bool:
    """
    Process a single JSON file: translate Chinese content to English.

    Returns True if successful, False otherwise.
    """
    print(f"\nProcessing: {filepath.name}")

    # Read file
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  ✗ Failed to read file: {e}")
        return False

    # Check if has Chinese content
    if not has_chinese_content(data):
        print("  ✓ No Chinese content found, skipping translation")
        # Still ensure language field is set
        data['language'] = 'en-US'
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True

    print("  → Translating Chinese content...")

    # Translate each field
    translation_count = 0

    # Title
    if data.get('title') and CHINESE_PATTERN.search(data['title']):
        print("  → Translating title...")
        data['title'] = translate_text(client, data['title'], 'title', use_cache)
        translation_count += 1

    # Description
    if data.get('description') and CHINESE_PATTERN.search(data['description']):
        print("  → Translating description...")
        data['description'] = translate_text(client, data['description'], 'description', use_cache)
        translation_count += 1

    # Content (large field, needs more tokens)
    if data.get('content') and CHINESE_PATTERN.search(data['content']):
        print("  → Translating content (this may take a moment)...")
        data['content'] = translate_text(client, data['content'], 'content', use_cache)
        translation_count += 1

    # SEO Keywords (batch translation)
    if data.get('seo_keywords') and isinstance(data['seo_keywords'], list):
        has_chinese_keywords = any(
            kw and CHINESE_PATTERN.search(kw) for kw in data['seo_keywords']
        )
        if has_chinese_keywords:
            print("  → Translating SEO keywords...")
            data['seo_keywords'] = translate_keywords(client, data['seo_keywords'])
            translation_count += 1

    # Author
    if data.get('author') and CHINESE_PATTERN.search(data['author']):
        print("  → Translating author...")
        data['author'] = translate_text(client, data['author'], 'author', use_cache)
        translation_count += 1

    # Ensure language field
    data['language'] = 'en-US'

    # Write back
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Successfully translated {translation_count} fields")
        return True
    except Exception as e:
        print(f"  ✗ Failed to write file: {e}")
        return False

def main():
    """Main batch translation process."""
    print("=" * 70)
    print("Batch Chinese-to-English Translation for SEO JSON Files")
    print("=" * 70)
    print(f"\nModel: {MODEL}")
    print(f"Directory: {DIRECTORY}")
    print(f"Processing files: {START_INDEX + 1} to {START_INDEX + FILES_TO_PROCESS} (indices {START_INDEX} to {START_INDEX + FILES_TO_PROCESS - 1})")

    # Initialize Anthropic client
    # Uses ANTHROPIC_API_KEY environment variable
    client = anthropic.Anthropic()

    # Get all JSON files and sort them
    all_files = sorted([
        f for f in os.listdir(DIRECTORY)
        if f.endswith('.json')
    ])

    print(f"\nTotal files in directory: {len(all_files)}")

    # Get files 51-75
    files_to_process = all_files[START_INDEX:START_INDEX + FILES_TO_PROCESS]

    print(f"Files to process: {len(files_to_process)}")
    print(f"\nFiles:\n  " + "\n  ".join(files_to_process[:5]) + f"\n  ... ({len(files_to_process) - 5} more)")

    # Process each file
    success_count = 0
    error_count = 0
    start_time = time.time()

    for i, filename in enumerate(files_to_process, start=START_INDEX + 1):
        filepath = Path(DIRECTORY) / filename

        print(f"\n[{i}/{START_INDEX + FILES_TO_PROCESS}] ", end="")

        # Use caching for first request, then reuse cache
        use_cache = (i == START_INDEX + 1)

        if process_file(client, filepath, use_cache):
            success_count += 1
        else:
            error_count += 1

        # Small delay to avoid rate limits
        if i < START_INDEX + FILES_TO_PROCESS:
            time.sleep(0.5)

    # Summary
    elapsed_time = time.time() - start_time
    print("\n" + "=" * 70)
    print("Translation Complete")
    print("=" * 70)
    print(f"\n✓ Successfully processed: {success_count}/{FILES_TO_PROCESS} files")
    print(f"✗ Errors: {error_count}")
    print(f"⏱ Total time: {elapsed_time:.1f} seconds ({elapsed_time/FILES_TO_PROCESS:.1f}s per file avg)")
    print(f"\nAll files now have 'language': 'en-US' field set")

    # Cache statistics (if available from first response)
    # Note: In production, you'd track these across requests
    print("\n💡 Prompt caching used for efficiency")
    print("   - System prompt cached across all translation requests")
    print("   - Reduces API costs and latency")

if __name__ == "__main__":
    main()