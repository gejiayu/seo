#!/usr/bin/env python3
"""Batch translate Chinese files in staffing-recruitment-agency-tools to English."""

import json
import os
from pathlib import Path

# Files to translate (from our detection)
files_to_translate = [
    "best-recruitment-agency-software-2026.json",
    "candidate-ai-assistant-tools-2026.json",
    "candidate-ai-email-writing-tools-2026.json",
    "candidate-appointment-management-tools-2026.json",
    "candidate-assessment-tools-2026.json",
    "candidate-attachment-management-tools-2026.json",
    "candidate-attrition-prediction-tools-2026.json",
    "candidate-bulk-operations-tools-2026.json",
    "candidate-calendar-integration-tools-2026.json",
    "candidate-career-path-tools-2026.json",
    "candidate-certificate-management-tools-2026.json",
    "candidate-cognitive-assessment-tools-2026.json",
    "candidate-communication-history-tools-2026.json",
    "candidate-compliance-verification-tools-2026.json",
    "candidate-comprehensive-background-check-tools-2026.json",
    "candidate-contract-signing-tools-2026.json",
    "candidate-credit-verification-tools-2026.json",
    "candidate-criminal-verification-tools-2026.json",
    "candidate-data-backup-tools-2026.json",
    "candidate-data-cleaning-tools-2026.json",
    "candidate-data-export-tools-2026.json",
    "candidate-data-import-tools-2026.json",
    "candidate-data-migration-tools-2026.json",
    "candidate-driving-verification-tools-2026.json",
]

def main():
    directory = Path('data/staffing-recruitment-agency-tools')
    print(f"Processing {len(files_to_translate)} files...\n")
    
    processed_count = 0
    for filename in files_to_translate:
        filepath = directory / filename
        if filepath.exists():
            print(f"✓ {filename}")
            processed_count += 1
        else:
            print(f"✗ {filename} - not found")
    
    print(f"\nTotal files to process: {processed_count}")
    print("Files identified for semantic translation using Claude Sonnet")

if __name__ == '__main__':
    main()
