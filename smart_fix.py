#!/usr/bin/env python3
import json
import re

def smart_word_splitting(text):
    """
    Intelligently split concatenated words based on context and common patterns
    """
    # Medical equipment domain patterns
    patterns = [
        # Common medical equipment rental terms
        (r'medical[equipment]', 'medical equipment'),
        (r'equipment[rental]', 'equipment rental'),
        (r'rental[compliance]', 'rental compliance'),
        (r'compliance[management]', 'compliance management'),
        (r'management[system]', 'management system'),
        (r'system[review]', 'system review'),
        (r'fda[certification]', 'FDA certification'),
        (r'certification[tracking]', 'certification tracking'),
        (r'safety[inspection]', 'safety inspection'),
        (r'inspection[tool]', 'inspection tool'),
        (r'ce[certification]', 'CE certification'),
        (r'disinfection[compliance]', 'disinfection compliance'),
        (r'iso[quality]', 'ISO quality'),
        (r'quality[management]', 'quality management'),
        (r'medical[device]', 'medical device'),
        (r'validity[period]', 'validity period'),
        (r'expiration[reminder]', 'expiration reminder'),
        (r'automatic[reminder]', 'automatic reminder'),
        (r'inspection[plan]', 'inspection plan'),
        (r'inspection[record]', 'inspection record'),
        (r'rectification[tracking]', 'rectification tracking'),
        (r'disinfection[record]', 'disinfection record'),
        (r'disinfection[agent]', 'disinfection agent'),
        (r'public[report]', 'public report'),
        (r'machine[structure]', 'machine structure'),
        (r'technology[documentation]', 'technology documentation'),
        (r'cloud[deployment]', 'cloud deployment'),
        (r'database[update]', 'database update'),
        (r'pricing[strategy]', 'pricing strategy'),
        (r'basic[version]', 'basic version'),
        (r'professional[version]', 'professional version'),
        (r'core[functionality]', 'core functionality'),
        (r'target[market]', 'target market'),
        (r'compliance[report]', 'compliance report'),
        (r'recall[management]', 'recall management'),
        (r'customer[service]', 'customer service'),
        (r'satisfaction[system]', 'satisfaction system'),
        (r'data[analytics]', 'data analytics'),
        (r'bi[tool]', 'BI tool'),
        (r'visualization[report]', 'visualization report'),
        (r'demand[prediction]', 'demand prediction'),
        (r'digital[transformation]', 'digital transformation'),
        (r'energy[management]', 'energy management'),
        (r'finance[management]', 'finance management'),
        (r'financial[management]', 'financial management'),
        (r'cashflow[prediction]', 'cashflow prediction'),
        (r'flow[analysis]', 'flow analysis'),
        (r'roi[calculate]', 'ROI calculate'),
        (r'fleet[management]', 'fleet management'),
        (r'globalization[management]', 'globalization management'),
        (r'hr[management]', 'HR management'),
        (r'human[resource]', 'human resource'),
        (r'innovation[management]', 'innovation management'),
        (r'crm[system]', 'CRM system'),
        (r'customer[management]', 'customer management'),
        (r'marketing[automation]', 'marketing automation'),
        (r'churn[prediction]', 'churn prediction'),
        (r'change[management]', 'change management'),
        (r'ai[management]', 'AI management'),
        (r'big[data]', 'big data'),
        (r'blockchain[management]', 'blockchain management'),
        # Specific long patterns
        (r'medical[equipmentrental]', 'medical equipment rental'),
        (r'equipmentrental[compliance]', 'equipment rental compliance'),
        (r'equipmentrental[contract]', 'equipment rental contract'),
        (r'equipmentrental[cost]', 'equipment rental cost'),
        (r'equipmentrental[crm]', 'equipment rental CRM'),
        (r'equipmentrental[customer]', 'equipment rental customer'),
        (r'equipmentrental[data]', 'equipment rental data'),
        (r'equipmentrental[delivery]', 'equipment rental delivery'),
        (r'equipmentrental[demand]', 'equipment rental demand'),
        (r'equipmentrental[digital]', 'equipment rental digital'),
        (r'equipmentrental[document]', 'equipment rental document'),
        (r'equipmentrental[energy]', 'equipment rental energy'),
        (r'equipmentrental[finance]', 'equipment rental finance'),
        (r'equipmentrental[financial]', 'equipment rental financial'),
        (r'equipmentrental[fleet]', 'equipment rental fleet'),
        (r'equipmentrental[globalization]', 'equipment rental globalization'),
        (r'equipmentrental[hr]', 'equipment rental HR'),
        (r'equipmentrental[innovation]', 'equipment rental innovation'),
        # More specific patterns
        (r'compliancemanagement[system]', 'compliance management system'),
        (r'contractmanagement[system]', 'contract management system'),
        (r'costmanagement[system]', 'cost management system'),
        (r'crmsystem[review]', 'CRM system review'),
        (r'customersatisfaction[system]', 'customer satisfaction system'),
        (r'customerservice[management]', 'customer service management'),
        (r'dataanalytics[platform]', 'data analytics platform'),
        (r'deliverymanagement[system]', 'delivery management system'),
        (r'demandprediction[system]', 'demand prediction system'),
        (r'digitaltransformation[system]', 'digital transformation system'),
        (r'documentmanagement[system]', 'document management system'),
        (r'energymanagement[system]', 'energy management system'),
        (r'financemanagement[system]', 'finance management system'),
        (r'financialmanagement[system]', 'financial management system'),
        (r'fleetmanagement[system]', 'fleet management system'),
        (r'globalizationmanagement[system]', 'globalization management system'),
        (r'hrmanagement[system]', 'HR management system'),
        (r'innovationmanagement[system]', 'innovation management system'),
    ]

    # Apply patterns
    result = text.lower()
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

    # Additional smart splitting for remaining long words
    # Split on common word boundaries (capital letters in original camelCase)
    def camel_case_split(match):
        word = match.group(0)
        # Insert space before capital letters (but not at start)
        result = re.sub(r'([a-z])([A-Z])', r'\1 \2', word)
        # Handle multiple capitals together (like "FDA")
        result = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', result)
        return result

    # Find remaining long words and apply camelCase splitting
    long_words = re.findall(r'[a-zA-Z]{20,}', result)
    for word in long_words:
        split = camel_case_split(lambda m: m.group(0))
        # Apply camelCase splitting
        split = re.sub(r'([a-z])([A-Z])', r'\1 \2', word)
        split = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', split)
        result = result.replace(word, split)

    return result

def fix_file(filepath):
    """Fix broken translations in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Fix all string fields
        for key in ['title', 'description', 'content']:
            if key in data:
                data[key] = smart_word_splitting(data[key])

        # Fix keywords array
        if 'seo_keywords' in data:
            data['seo_keywords'] = [smart_word_splitting(kw) for kw in data['seo_keywords']]

        # Ensure language field
        if 'language' not in data:
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
print(f"Testing fix on: {test_file}")
if fix_file(test_file):
    print("✅ Test successful")
    # Read and show sample of fixed content
    with open(test_file, 'r') as f:
        data = json.load(f)
    print("\nSample fixed title:")
    print(data['title'][:200])
else:
    print("❌ Test failed")