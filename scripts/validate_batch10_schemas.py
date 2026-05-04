#!/usr/bin/env python3
"""
Validate generated schemas for batch 10 categories.
"""

import json
from pathlib import Path

DATA_DIR = Path("/Users/gejiayu/owner/seo/data")

CATEGORIES = [
    "boat-marine-rental-tools",
    "costume-fashion-rental-tools",
    "camera-photography-rental-tools",
    "audio-video-equipment-rental-tools",
    "party-event-supplies-rental-tools",
]

def validate_schema(file_path):
    """Validate schema_markup in a JSON file."""

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        schema_markup = data.get('schema_markup', '')

        if not schema_markup:
            return False, "No schema_markup found"

        # Parse schema
        schema = json.loads(schema_markup)

        # Check for @graph structure
        if '@graph' not in schema:
            return False, "Missing @graph structure"

        # Check for FAQPage
        has_faq = False
        has_howto = False
        has_software = False

        for item in schema['@graph']:
            item_type = item.get('@type', '')

            if item_type == 'FAQPage':
                has_faq = True
                # Validate FAQ structure
                if 'mainEntity' not in item:
                    return False, "FAQPage missing mainEntity"

                # Check question count (should be 5-7)
                question_count = len(item['mainEntity'])
                if question_count < 5 or question_count > 7:
                    return False, f"Invalid FAQ count: {question_count} (expected 5-7)"

            elif item_type == 'HowTo':
                has_howto = True
                # Validate HowTo structure
                if 'step' not in item:
                    return False, "HowTo missing step"

                # Check step count (should be 3-5)
                step_count = len(item['step'])
                if step_count < 3 or step_count > 5:
                    return False, f"Invalid HowTo step count: {step_count} (expected 3-5)"

            elif item_type == 'SoftwareApplication':
                has_software = True

        # Check all schemas are present
        if not has_faq:
            return False, "Missing FAQPage schema"
        if not has_howto:
            return False, "Missing HowTo schema"

        return True, f"Valid (FAQs: {question_count}, Steps: {step_count}, Software: {has_software})"

    except json.JSONDecodeError as e:
        return False, f"JSON decode error: {str(e)}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def main():
    """Main validation function."""

    print("=" * 80)
    print("Schema Validation Report for Batch 10")
    print("=" * 80)
    print()

    total_valid = 0
    total_invalid = 0
    stats = []

    for category in CATEGORIES:
        category_dir = DATA_DIR / category
        json_files = list(category_dir.glob('*.json'))

        valid_count = 0
        invalid_count = 0

        for json_file in json_files:
            is_valid, message = validate_schema(json_file)

            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
                print(f"❌ {json_file.name}: {message}")

        stats.append({
            'category': category,
            'total': len(json_files),
            'valid': valid_count,
            'invalid': invalid_count,
        })

        total_valid += valid_count
        total_invalid += invalid_count

        print(f"✅ {category}: {valid_count}/{len(json_files)} files valid")

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    for stat in stats:
        pct = (stat['valid'] / stat['total'] * 100) if stat['total'] > 0 else 0
        print(f"{stat['category']:40s} - {stat['valid']}/{stat['total']} ({pct:.1f}%)")

    print()
    print(f"Total valid schemas: {total_valid}")
    print(f"Total invalid schemas: {total_invalid}")
    print(f"Success rate: {(total_valid / (total_valid + total_invalid) * 100):.1f}%")
    print()

if __name__ == "__main__":
    main()