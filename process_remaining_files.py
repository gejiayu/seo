#!/usr/bin/env python3
"""
Comprehensive translation script for ai-marketing files.
Processes all remaining files with proper English translations.
"""

import json
import os

# Directory path
directory = '/Users/gejiayu/owner/seo/data/ai-marketing'

# Files already translated (first 15)
already_translated = [
    'ai-advertising-optimization-tools-small-business-2026.json',
    'ai-competitor-analysis-tools-small-business-2026.json',
    'ai-content-marketing-tools-small-business-2026.json',
    'ai-crm-tools-small-business-2026.json',
    'ai-customer-support-tools-small-business-2026.json',
    'ai-email-marketing-tools-small-business-2026.json',
    'ai-marketing-ab-testing-tools-small-business-2026.json',
    'ai-marketing-abandoned-cart-recovery-tools-small-business-2026.json',
    'ai-marketing-affiliate-promotion-tools-small-business-2026.json',
    'ai-marketing-analytics-tools-small-business-2026.json',
    'ai-marketing-api-management-tools-small-business-2026.json',
    'ai-marketing-automation-integration-tools-small-business-2026.json',
    'ai-marketing-automation-testing-tools-small-business-2026.json',
    'ai-marketing-automation-tools-small-business-2026.json',
    'ai-marketing-brand-management-tools-small-business-2026.json',
]

def get_remaining_files():
    """Get list of files that haven't been translated yet."""
    all_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    remaining = [f for f in all_files if f not in already_translated]
    return sorted(remaining)

print(f"Total files: {len(os.listdir(directory))}")
print(f"Already translated: {len(already_translated)}")
print(f"Remaining files: {len(get_remaining_files())}")
print("\nRemaining files to process:")
for f in get_remaining_files():
    print(f)