#!/usr/bin/env python3
import json
import re

# Comprehensive medical equipment rental vocabulary
# Including compound terms that should NOT be split
MEDICAL_VOCAB_EXTENDED = {
    # Single words
    'medical', 'equipment', 'rental', 'compliance', 'management', 'system', 'review', 'tool',
    'certification', 'tracking', 'safety', 'inspection', 'plan', 'disinfection', 'quality',
    'device', 'standard', 'market', 'validity', 'period', 'expired', 'renewal', 'scope',
    'cover', 'model', 'functionality', 'use', 'update', 'reminder', 'expiration',
    'automatic', 'class', 'level', 'technology', 'documentation', 'storage', 'public',
    'report', 'structure', 'information', 'audit', 'design', 'maintenance', 'process',
    'project', 'list', 'electric', 'gas', 'machine', 'instrument', 'radiation', 'result',
    'record', 'rectification', 'completed', 'recovery', 'prevent', 'infection', 'high',
    'temperature', 'agent', 'personnel', 'time', 'verification', 'effectiveness',
    'prohibit', 'mainstream', 'product', 'suite', 'professional', 'core', 'database',
    'cloud', 'deployment', 'generate', 'pricing', 'strategy', 'basic', 'version',
    'include', 'depth', 'manager', 'focuses', 'connect', 'api', 'real', 'status',
    'query', 'european', 'union', 'method', 'platform', 'allocation', 'execution',
    'task', 'mobile', 'terminal', 'app', 'support', 'sterilize', 'log', 'prediction',
    'demand', 'crm', 'customer', 'service', 'satisfaction', 'analytics', 'data', 'bi',
    'visualization', 'delivery', 'digital', 'transformation', 'document', 'energy',
    'finance', 'financial', 'flow', 'roi', 'calculate', 'fleet', 'globalization',
    'hr', 'human', 'resource', 'innovation', 'churn', 'ai', 'big', 'blockchain',
    'cashflow', 'change', 'analysis', 'related', 'domain', 'solution', 'marketing',
    'automation', 'type', 'calculate', 'fda', 'ce', 'iso', 'cfda',

    # Compound terms (keep together)
    'equipmentrental', 'rentalcompliance', 'compliancemanagement', 'managementsystem',
    'systemreview', 'certificationtracking', 'safetyinspection', 'inspectiontool',
    'certificationmanagement', 'disinfectioncompliance', 'qualitymanagement',
    'medicaldevice', 'validityperiod', 'expirationreminder', 'automaticreminder',
    'inspectionplan', 'inspectionrecord', 'rectificationtracking', 'disinfectionrecord',
    'disinfectionagent', 'publicreport', 'machinestructure', 'technologydocumentation',
    'clouddeployment', 'databaseupdate', 'pricingstrategy', 'basicversion',
    'professionalversion', 'corefunctionality', 'targetmarket', 'compliancereport',
    'recallmanagement', 'customerservice', 'satisfactionsystem', 'dataanalytics',
    'analyticsplatform', 'visualizationreport', 'demandprediction', 'digitaltransformation',
    'documentmanagement', 'energymanagement', 'financemanagement', 'financialmanagement',
    'cashflowprediction', 'flowanalysis', 'roicalculate', 'fleetmanagement',
    'globalizationmanagement', 'humanresource', 'resourcemanagement', 'innovationmanagement',
    'customermanagement', 'marketingautomation', 'churnprediction', 'changemanagement',
    'aimanagement', 'bigdata', 'blockchainmanagement', 'trackingandsafety',
    'and', 'for', 'the', 'with', 'of', 'in', 'to', 'a', 'is', 'are',

    # Even longer compounds
    'equipmentrentalcompliance', 'equipmentrentalcontract', 'equipmentrentalcost',
    'equipmentrentalcrm', 'equipmentrentalcustomer', 'equipmentrentaldata',
    'equipmentrentaldelivery', 'equipmentrentaldemand', 'equipmentrentaldigital',
    'equipmentrentaldocument', 'equipmentrentalenergy', 'equipmentrentalfinance',
    'equipmentrentalfinancial', 'equipmentrentalfleet', 'equipmentrentalglobalization',
    'equipmentrentalhr', 'equipmentrentalinnovation', 'compliancemanagementsystem',
    'contractmanagementsystem', 'costmanagementsystem', 'crmsystemreview',
    'customersatisfactionsystem', 'customerservice management', 'dataanalyticsplatform',
    'deliverymanagementsystem', 'demandpredictionsystem', 'digitaltransformationsystem',
    'documentmanagementsystem', 'energymanagementsystem', 'financemanagementsystem',
    'financialmanagementsystem', 'fleetmanagementsystem', 'globalizationmanagementsystem',
    'hrmanagementsystem', 'innovationmanagementsystem', 'certificationtrackingandsafety',
    'trackingandsafetyinspection'
}

def greedy_word_split(word):
    """
    Greedy algorithm: match longest possible words from vocabulary
    """
    word_lower = word.lower()
    result = []
    remaining = word_lower

    max_len = max(len(w) for w in MEDICAL_VOCAB_EXTENDED)

    while remaining:
        matched = False
        # Try longest matches first
        for length in range(min(max_len, len(remaining)), 2, -1):
            candidate = remaining[:length]
            if candidate in MEDICAL_VOCAB_EXTENDED:
                result.append(candidate)
                remaining = remaining[length:]
                matched = True
                break

        if not matched:
            # If no match found, keep 4-8 chars together (avoid tiny fragments)
            chunk_size = min(8, max(4, len(remaining)))
            result.append(remaining[:chunk_size])
            remaining = remaining[chunk_size:]

    return ' '.join(result)

def semantic_split(text):
    """
    Split using camelCase + greedy vocabulary matching
    """
    # Step 1: CamelCase splitting (preserves capital letters)
    result = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    result = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', result)

    # Step 2: Find very long lowercase words (>15 chars)
    long_words = re.findall(r'[a-z]{15,}', result)

    for word in long_words:
        split_version = greedy_word_split(word)
        result = result.replace(word, split_version)

    return result

def fix_file(filepath):
    """Fix file with semantic splitting"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Fix all text fields
        for key in ['title', 'description', 'content']:
            if key in data and isinstance(data[key], str):
                data[key] = semantic_split(data[key])

        # Fix keywords
        if 'seo_keywords' in data:
            data['seo_keywords'] = [semantic_split(kw) for kw in data['seo_keywords']]

        # Add language field
        data['language'] = 'en-US'

        # Save
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# Test on first file
test_file = "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools/medical-equipment-rental-compliance-management-system-review.json"

print("=" * 80)
print("TESTING SEMANTIC WORD SPLITTING")
print("=" * 80)

if fix_file(test_file):
    with open(test_file, 'r') as f:
        data = json.load(f)

    print("\n✅ Test successful!")
    print(f"\nFixed title:\n{data['title']}")
    print(f"\nLanguage field: {data.get('language')}")
else:
    print("\n❌ Test failed")

# Show sample from content
print("\n" + "=" * 80)
print("CONTENT SAMPLE (first 500 chars)")
print("=" * 80)
print(data['content'][:500])