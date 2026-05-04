#!/usr/bin/env python3
import json
import os
from pathlib import Path

# Directories to process
directories = [
    "airport-aviation-management-tools",
    "audio-video-equipment-rental-tools",
    "auto-dealer-management-tools",
    "automotive-dealer-dms-tools",
    "automotive-repair-tools",
    "banking-financial-services-tools",
    "beauty-salon-tools",
    "cybersecurity-it-security-tools",
    "dental-medical-practice-tools",
    "diving-water-sports-rental-tools",
    "education-lms-platform-tools",
    "event-planning-tools",
    "fitness-gym-management",
    "healthcare-medical-treatment-tools",
    "healthcare-wellness-tools",
    "manufacturing-quality-control-tools",
    "music-audio-production",
    "paintball-laser-tag-rental-tools",
    "party-event-supplies-rental-tools",
    "pet-services-tools",
    "pet-store-pet-supply-tools",
    "pet-vet-clinic-tools",
    "portable-sanitation-rental-tools",
    "retail-pos-inventory-tools",
    "retail-ecommerce-operations-tools",
    "scooter-moped-rental-tools",
    "ski-snowboard-rental-tools",
    "sports-equipment-rental-tools",
    "staging-rigging-rental-tools",
    "tennis-racket-rental-tools",
    "tent-canopy-rental-tools",
    "travel-agency-tour-operator-tools",
    "renewable-energy-management-tools"
]

base_path = Path("/Users/gejiayu/owner/seo/data")
zh_path = base_path / "zh"

processed_count = 0
skipped_count = 0

def process_file(file_path):
    """Process a single JSON file, truncating description to 155 chars."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if 'description' in data and isinstance(data['description'], str):
            original_desc = data['description']
            if len(original_desc) > 155:
                # Truncate to 155 characters
                data['description'] = original_desc[:155]

                # Write back
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                return True  # Modified
            else:
                return False  # Not modified
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

# Process each directory
for dir_name in directories:
    # Process main directory
    main_dir = base_path / dir_name
    if main_dir.exists():
        json_files = list(main_dir.glob("*.json"))
        for json_file in json_files:
            if process_file(json_file):
                processed_count += 1
            else:
                skipped_count += 1

    # Process zh directory
    zh_dir = zh_path / dir_name
    if zh_dir.exists():
        json_files = list(zh_dir.glob("*.json"))
        for json_file in json_files:
            if process_file(json_file):
                processed_count += 1
            else:
                skipped_count += 1

print(f"Total files processed (modified): {processed_count}")
print(f"Total files skipped (already <= 155 chars): {skipped_count}")
print(f"Total files checked: {processed_count + skipped_count}")