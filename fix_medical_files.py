#!/usr/bin/env python3
"""
Script to fix broken machine translations in medical-equipment-rental-tools JSON files.
"""

import json
import re
from pathlib import Path

def fix_concatenated_words(text):
    """
    Fix concatenated words by adding proper spacing.
    Uses intelligent spacing patterns based on common English word boundaries.
    """
    # Pattern to detect concatenated lowercase words (40+ chars without spaces)
    # We'll break them intelligently

    # Common medical/business terms that should stay together
    protected_terms = [
        'ICU', 'ERP', 'AI', 'IoT', 'FDA', 'CE', 'ISO', 'HIPAA',
        'APP', 'API', 'SaaS', 'AWS', 'RFID', 'BI', 'CT', 'MRI',
        'Web', 'iOS', 'Android'
    ]

    # Add space after known abbreviations
    for term in protected_terms:
        # Pattern: word + abbreviation (no space)
        text = re.sub(
            r'([a-z])(' + term + r')([a-z])',
            r'\1 \2 \3',
            text,
            flags=re.IGNORECASE
        )
        text = re.sub(
            r'([a-z])(' + term + r')',
            r'\1 \2',
            text,
            flags=re.IGNORECASE
        )
        text = re.sub(
            r'(' + term + r')([a-z])',
            r'\1 \2',
            text,
            flags=re.IGNORECASE
        )

    # Fix specific patterns we've seen
    replacements = [
        # Medical terms
        ('ICUcritical', 'ICU Critical'),
        ('CareEquipment', 'Care Equipment'),
        ('RentalManagement', 'Rental Management'),
        ('SystemReview', 'System Review'),

        # Equipment types
        ('InfusionPump', 'Infusion Pump'),
        ('medicalEquipment', 'Medical Equipment'),
        ('medicalDevice', 'Medical Device'),
        ('EquipmentRental', 'Equipment Rental'),
        ('EquipmentDepreciation', 'Equipment Depreciation'),
        ('ManagementSystem', 'Management System'),

        # Common concatenations
        ('equipmentrental', 'equipment rental'),
        ('managementplatform', 'management platform'),
        ('coretool', 'core tool'),
        ('reviewanalysis', 'review analysis'),

        # Specific broken patterns from files
        ('ICUequipmentrental', 'ICU equipment rental'),
        ('criticalcare', 'critical care'),
        ('equipmentrentalbackground', 'equipment rental background'),
        ('monitoringinstrument', 'monitoring instrument'),
        ('ventilatorrental', 'ventilator rental'),
        ('infusionpump', 'infusion pump'),

        # Title patterns
        ('Review|', 'Review | '),

        # Description patterns
        ('depthAnalysis', 'In-depth Analysis'),
        ('RelatedTool', 'Related Tool'),
        ('doMainSolution', 'domain solution'),
        ('Learn more about functionalityand', 'Learn more about functionality and'),
        ('price comparison', 'price comparison'),

        # Common word boundaries
        ('EquipmentRentalManagement', 'Equipment Rental Management'),
        ('RentalManagementSystem', 'Rental Management System'),
        ('ManagementSystemReview', 'Management System Review'),
        ('DepreciationManagementSystem', 'Depreciation Management System'),
        ('PredictionSystemReview', 'Prediction System Review'),
        ('CustomerchurnPrediction', 'Customer Churn Prediction'),
        ('Customerchurn', 'Customer Churn'),

        # Content patterns
        ('monitoringequipment', 'monitoring equipment'),
        ('respiratoryequipment', 'respiratory equipment'),
        ('infusionequipment', 'infusion equipment'),
        ('equipmenttracking', 'equipment tracking'),
        ('accuracymanagement', 'accuracy management'),
        ('safetymanagement', 'safety management'),
        ('maintenancemanagement', 'maintenance management'),
        ('batchmanagement', 'batch management'),
        ('equipmentaccuracy', 'equipment accuracy'),
        ('equipmentsafety', 'equipment safety'),
        ('equipmentmaintenance', 'equipment maintenance'),
        ('equipmentnumberamount', 'equipment number amount'),

        # ERP specific
        ('medical devicerentalERP', 'Medical Device Rental ERP'),
        ('ERPsystem', 'ERP system'),
        ('systemselectpurchase', 'system selection purchase'),
        ('selectpurchaseguide', 'selection purchase guide'),
        ('IndustrybackGround', 'Industry Background'),
        ('DigitaltransferType', 'Digital Transformation'),

        # Depreciation specific
        ('EquipmentDepreciationManagement', 'Equipment Depreciation Management'),
        ('DepreciationManagementSystem', 'Depreciation Management System'),
        ('DepreciationCalculate', 'Depreciation Calculation'),
        ('DepreciationTracking', 'Depreciation Tracking'),
        ('DepreciationOptimization', 'Depreciation Optimization'),
        ('DepreciationReport', 'Depreciation Report'),

        # Churn prediction specific
        ('RentalCustomerchurn', 'Rental Customer Churn'),
        ('CustomerchurnPrediction', 'Customer Churn Prediction'),
        ('churnPrediction', 'Churn Prediction'),
        ('PredictionbackGround', 'Prediction Background'),
        ('churnprediction', 'churn prediction'),
        ('customersavereturn', 'customer save return'),
        ('AIchurnprediction', 'AI churn prediction'),

        # General patterns
        ('background', 'background'),
        ('core functionality', 'core functionality'),
        ('comparisontable', 'comparison table'),
        ('trendprediction', 'trend prediction'),
        ('coretoolreview', 'core tool review'),

        # SEO keywords
        ('ICUequipmentrental', 'ICU equipment rental'),
        ('critical caremonitoringequipment', 'critical care monitoring equipment'),
        ('ICUventilatorrental', 'ICU ventilator rental'),
        ('ICUinfusionpump', 'ICU infusion pump'),
    ]

    for old, new in replacements:
        text = text.replace(old, new)

    # Add spaces after punctuation if missing
    text = re.sub(r'([.!?])([A-Za-z])', r'\1 \2', text)
    text = re.sub(r'([,])([a-z])', r'\1 \2', text)

    # Add space before punctuation if missing
    text = re.sub(r'([a-z])([.,!?])', r'\1 \2', text)

    # Fix "etc." pattern
    text = re.sub(r'etc\.([a-z])', r'etc. \1', text)
    text = re.sub(r'([a-z])etc\.', r'\1 etc.', text)

    return text

def fix_file(filepath):
    """Fix a single JSON file."""
    print(f"Fixing: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Fix title
    if 'title' in data:
        data['title'] = fix_concatenated_words(data['title'])

    # Fix description
    if 'description' in data:
        data['description'] = fix_concatenated_words(data['description'])

    # Fix content
    if 'content' in data:
        # For content, we need to be more careful with HTML tags
        # First, let's add proper spacing to concatenated words
        content = data['content']
        content = fix_concatenated_words(content)
        data['content'] = content

    # Fix SEO keywords (they're an array, need to fix each item)
    if 'seo_keywords' in data and isinstance(data['seo_keywords'], list):
        data['seo_keywords'] = [fix_concatenated_words(kw) for kw in data['seo_keywords']]

    # Ensure language field exists
    if 'language' not in data:
        data['language'] = 'en-US'

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✓ Fixed: {filepath}")

def main():
    # Files to fix (identified earlier)
    files_to_fix = [
        'icu-critical-care-equipment-rental-management-system-review.json',
        'infusion-pump-equipment-rental-management-system-review.json',
        'medical-device-rental-erp-selection-guide.json',
        'medical-equipment-depreciation-management-system-review.json',
        'medical-equipment-rental-churn-prediction-system-review.json'
    ]

    base_dir = '/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools'

    print("=" * 80)
    print("FIXING BROKEN MACHINE TRANSLATIONS")
    print("=" * 80)

    for filename in files_to_fix:
        filepath = Path(base_dir) / filename
        if filepath.exists():
            fix_file(filepath)
        else:
            print(f"❌ File not found: {filepath}")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total files fixed: {len(files_to_fix)}")

if __name__ == '__main__':
    main()