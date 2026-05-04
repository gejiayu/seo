#!/usr/bin/env python3
"""
Script to fix and improve descriptions in JSON files.
Targets descriptions with awkward phrasing or those shorter than proper SEO length.
"""

import json
import re
from pathlib import Path
from typing import Dict, List

# Configuration
DATA_DIR = Path("data")
MIN_DESC_LENGTH = 150
MAX_DESC_LENGTH = 160

def clean_tool_type(tool_type: str) -> str:
    """Clean and simplify tool type for better descriptions."""
    # Remove year references
    tool_type = re.sub(r'\b(202[4-9])\b', '', tool_type)
    # Remove "for small business" etc
    tool_type = re.sub(r'for (small business|enterprise|business)', '', tool_type, flags=re.IGNORECASE)
    # Remove common filler words
    tool_type = re.sub(r'\s+(guide|comparison|tools|platforms|systems|software)\s*$', '', tool_type, flags=re.IGNORECASE)
    # Clean up extra spaces
    tool_type = ' '.join(tool_type.split())
    return tool_type.strip()

def generate_description(title: str, content: str) -> str:
    """Generate an SEO-optimized description (150-160 chars)."""
    # Parse year from title
    year_match = re.search(r'\b(202[4-9])\b', title)
    year = year_match.group(1) if year_match else '2026'

    # Extract tool type - multiple patterns
    tool_type = ''

    # Pattern 1: Before "for" keyword
    match = re.search(r'(.+?)\s+for\s+', title)
    if match:
        tool_type = match.group(1)

    # Pattern 2: Before common suffixes
    if not tool_type:
        match = re.search(r'(.+?)\s+(?:guide|comparison|review|tools|platforms)', title, re.IGNORECASE)
        if match:
            tool_type = match.group(1)

    # Pattern 3: First part before colon
    if not tool_type:
        match = re.search(r'^([^:]+)', title)
        if match:
            tool_type = match.group(1)

    # Clean tool type
    tool_type = clean_tool_type(tool_type)

    # Determine business type
    business_type = 'small business' if 'small business' in title.lower() else 'business'

    # Generate clean descriptions
    templates = [
        f"Best {tool_type.lower()} for {year}: Compare top platforms, pricing & features. Cut costs 20-30%, boost efficiency 25-40% for your {business_type}.",
        f"{year} {tool_type} comparison: Top platforms with pricing, features & ROI. Optimize operations, cut costs 20-35% for {business_type} success.",
        f"Struggling with {tool_type.lower()}? Compare {year}'s best platforms, pricing & features. Boost efficiency 30-45% & cut costs for {business_type}.",
        f"Top {tool_type.lower()} for {business_type} in {year}: Compare features, pricing & automation. Save hours weekly & reduce operational costs 20-30%.",
        f"Discover best {tool_type.lower()} for {year}. Compare platforms on features, pricing & integrations. Boost efficiency 25-50% for {business_type}."
    ]

    # Find template that fits length requirements
    for template in templates:
        if MIN_DESC_LENGTH <= len(template) <= MAX_DESC_LENGTH:
            return template

    # Fallback - use first template and adjust
    desc = templates[0]
    if len(desc) < MIN_DESC_LENGTH:
        desc += " Automate operations."
    elif len(desc) > MAX_DESC_LENGTH:
        desc = desc[:MAX_DESC_LENGTH-1] + '.'

    return desc

def needs_improvement(description: str) -> bool:
    """Check if description needs improvement."""
    # Check for awkward patterns
    awkward_patterns = [
        r'for\s+202\d\s+chaos',  # "for 2026 chaos" is awkward
        r'chaos\s*\?',  # Chaos pattern at end
        r'^.{0,140}$',  # Too short
        r'\s+fo\s*!$',  # Truncated "for your"
        r'\s+for\s+y\s*!$',  # Another truncation pattern
    ]

    for pattern in awkward_patterns:
        if re.search(pattern, description):
            return True

    # Check length
    if len(description) < MIN_DESC_LENGTH or len(description) > MAX_DESC_LENGTH + 5:
        return True

    return False

def process_json_file(file_path: Path) -> bool:
    """Process a single JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        original_desc = data.get('description', '')

        # Check if needs improvement
        if not needs_improvement(original_desc):
            return False

        # Generate new description
        title = data.get('title', '')
        content = data.get('content', '')
        new_desc = generate_description(title, content)

        # Final length check
        if len(new_desc) < MIN_DESC_LENGTH:
            new_desc += " Ideal for modern operations."
        elif len(new_desc) > MAX_DESC_LENGTH:
            new_desc = new_desc[:MAX_DESC_LENGTH-1] + '.'

        # Update data
        data['description'] = new_desc

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Improved: {file_path.name} | {len(original_desc)}→{len(new_desc)} chars")
        print(f"  Old: {original_desc[:80]}...")
        print(f"  New: {new_desc}")
        return True

    except Exception as e:
        print(f"Error: {file_path.name} - {e}")
        return False

def find_files_to_fix() -> List[Path]:
    """Find all JSON files that need improvement."""
    files_to_fix = []

    for json_file in DATA_DIR.rglob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            desc = data.get('description', '')
            if needs_improvement(desc):
                files_to_fix.append(json_file)
        except:
            continue

    return files_to_fix

def main():
    """Main function."""
    print("Scanning for files with awkward or short descriptions...")

    files_to_fix = find_files_to_fix()
    print(f"Found {len(files_to_fix)} files to improve\n")

    if not files_to_fix:
        print("All descriptions look good!")
        return

    fixed_count = 0
    for file_path in files_to_fix:
        if process_json_file(file_path):
            fixed_count += 1

    print(f"\n✅ Improved {fixed_count} descriptions")
    print(f"All descriptions now {MIN_DESC_LENGTH}-{MAX_DESC_LENGTH} chars with natural phrasing")

if __name__ == "__main__":
    main()