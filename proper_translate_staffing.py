#!/usr/bin/env python3
"""Proper semantic translation of staffing-recruitment-agency-tools Chinese files."""

import json
import os
from pathlib import Path
import re

# Proper translations for all 24 files
translations = {
    "best-recruitment-agency-software-2026.json": {
        "title": "Best Recruitment Agency Software Review 2026: 10 Major Platforms Deep Comparison",
        "description": "Comprehensive review of 2026 best recruitment agency software, including Bullhorn, Job Adder, Recruiterflow, Vincere, Firefish feature comparisons, helping staffing agencies select the right platform. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Recruitment Technology Research Institute",
        "seo_keywords": ["recruitment agency software", "recruitment CRM", "Bullhorn", "Job Adder", "Recruiterflow", "recruitment management system", "staffing software", "headhunting system"]
    },
    "candidate-ai-assistant-tools-2026.json": {
        "title": "Candidate AI Assistant Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate AI assistant tools, including AI automation, candidate communication features, helping staffing agencies enhance recruitment efficiency. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "AI Assistant Research Institute",
        "seo_keywords": ["candidate AI assistant", "AI recruitment", "automation tools", "candidate communication", "Recruiterflow", "HireVue", "ChatGPT", "AI assistant"]
    },
    "candidate-ai-email-writing-tools-2026.json": {
        "title": "Candidate AI Email Writing Tools: 2026 Intelligent Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate AI email writing tools for staffing agencies, including AI content generation, personalized emails, and feature comparisons, helping staffing agencies optimize communication workflows. Learn more about features and pricing comparisons to find the most suitable solution! Professional reviews!",
        "author": "AI Email Writing Research Institute",
        "seo_keywords": ["candidate AI email", "AI content generation", "personalized emails", "email templates", "Recruiterflow", "Jasper", "Copy.ai", "AI recruitment email"]
    },
    "candidate-appointment-management-tools-2026.json": {
        "title": "Candidate Appointment Management Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate appointment management tools, including scheduling automation, calendar integration, and feature comparisons, helping staffing agencies optimize interview scheduling workflows. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Appointment Management Research Institute",
        "seo_keywords": ["candidate appointment", "scheduling tools", "calendar integration", "interview scheduling", "Calendly", "Acuity", "YouCanBook.me", "appointment platform"]
    },
    "candidate-assessment-tools-2026.json": {
        "title": "Candidate Assessment Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate assessment tools, including cognitive tests, skill evaluations, behavioral assessments, and feature comparisons, helping staffing agencies improve candidate quality evaluation. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Candidate Assessment Research Institute",
        "seo_keywords": ["candidate assessment", "skill evaluation", "cognitive tests", "behavioral assessment", "Pymetrics", "Hogan", "Codility", "assessment platform"]
    },
    "candidate-attachment-management-tools-2026.json": {
        "title": "Candidate Attachment Management Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate attachment management tools, including document storage, file tracking, and feature comparisons, helping staffing agencies efficiently manage candidate documents and portfolios. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Attachment Management Research Institute",
        "seo_keywords": ["candidate attachments", "document management", "file storage", "portfolio tracking", "Bullhorn", "JobAdder", "document platform", "candidate files"]
    },
    "candidate-attrition-prediction-tools-2026.json": {
        "title": "Candidate Attrition Prediction Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate attrition prediction tools, including predictive analytics, retention analytics, and feature comparisons, helping staffing agencies improve candidate retention rates. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Attrition Prediction Research Institute",
        "seo_keywords": ["attrition prediction", "retention analytics", "predictive tools", "candidate retention", "Visier", "Workday", "retention platform", "analytics tools"]
    },
    "candidate-bulk-operations-tools-2026.json": {
        "title": "Candidate Bulk Operations Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate bulk operations tools, including mass updates, batch processing, and feature comparisons, helping staffing agencies efficiently handle large-scale candidate data operations. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Bulk Operations Research Institute",
        "seo_keywords": ["bulk operations", "batch processing", "mass updates", "candidate data", "Bullhorn", "JobAdder", "bulk tools", "mass processing"]
    },
    "candidate-calendar-integration-tools-2026.json": {
        "title": "Candidate Calendar Integration Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate calendar integration tools, including calendar sync, scheduling automation, and feature comparisons, helping staffing agencies streamline interview scheduling and coordination. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Calendar Integration Research Institute",
        "seo_keywords": ["calendar integration", "scheduling sync", "calendar tools", "interview coordination", "Google Calendar", "Outlook", "calendar platform", "scheduling automation"]
    },
    "candidate-career-path-tools-2026.json": {
        "title": "Candidate Career Path Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate career path planning tools, including career development, progression tracking, and feature comparisons, helping staffing agencies support candidate long-term career growth. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Career Path Research Institute",
        "seo_keywords": ["career path", "career development", "progression tracking", "candidate growth", "LinkedIn", "career platform", "development tools", "career planning"]
    },
    "candidate-certificate-management-tools-2026.json": {
        "title": "Candidate Certificate Management Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate certificate management tools, including credential tracking, certification verification, and feature comparisons, helping staffing agencies manage and verify candidate certifications and credentials. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Certificate Management Research Institute",
        "seo_keywords": ["certificate management", "credential tracking", "certification verification", "candidate credentials", "Bullhorn", "credential platform", "certification tools", "verification system"]
    },
    "candidate-cognitive-assessment-tools-2026.json": {
        "title": "Candidate Cognitive Assessment Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate cognitive assessment tools, including cognitive ability tests, reasoning assessments, and feature comparisons, helping staffing agencies evaluate candidate problem-solving and analytical skills. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Cognitive Assessment Research Institute",
        "seo_keywords": ["cognitive assessment", "reasoning tests", "ability evaluation", "problem-solving tests", "Wonderlic", "Criteria", "cognitive platform", "assessment tools"]
    },
    "candidate-communication-history-tools-2026.json": {
        "title": "Candidate Communication History Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate communication history tools, including interaction tracking, conversation archives, and feature comparisons, helping staffing agencies maintain comprehensive communication records with candidates. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Communication History Research Institute",
        "seo_keywords": ["communication history", "interaction tracking", "conversation archives", "candidate communication", "Bullhorn", "JobAdder", "communication platform", "history tools"]
    },
    "candidate-compliance-verification-tools-2026.json": {
        "title": "Candidate Compliance Verification Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate compliance verification tools, including regulatory checks, compliance tracking, and feature comparisons, helping staffing agencies ensure candidate regulatory and legal compliance. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Compliance Verification Research Institute",
        "seo_keywords": ["compliance verification", "regulatory checks", "compliance tracking", "candidate compliance", "Checkr", "GoodHire", "compliance platform", "verification tools"]
    },
    "candidate-comprehensive-background-check-tools-2026.json": {
        "title": "Candidate Comprehensive Background Check Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate comprehensive background check tools, including criminal records, education verification, work history, and feature comparisons, helping staffing agencies conduct thorough candidate screening. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Background Check Research Institute",
        "seo_keywords": ["background check", "criminal records", "education verification", "work history", "Checkr", "Sterling", "HireRight", "screening platform"]
    },
    "candidate-contract-signing-tools-2026.json": {
        "title": "Candidate Contract Signing Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate contract signing tools, including digital signatures, contract management, and feature comparisons, helping staffing agencies streamline contract workflows with candidates. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Contract Signing Research Institute",
        "seo_keywords": ["contract signing", "digital signatures", "contract management", "e-signature tools", "DocuSign", "Adobe Sign", "contract platform", "signature tools"]
    },
    "candidate-credit-verification-tools-2026.json": {
        "title": "Candidate Credit Verification Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate credit verification tools, including credit checks, financial history, and feature comparisons, helping staffing agencies verify candidate financial background for relevant positions. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Credit Verification Research Institute",
        "seo_keywords": ["credit verification", "credit checks", "financial history", "candidate background", "Checkr", "GoodHire", "credit platform", "verification tools"]
    },
    "candidate-criminal-verification-tools-2026.json": {
        "title": "Candidate Criminal Verification Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate criminal verification tools, including criminal record checks, background screening, and feature comparisons, helping staffing agencies verify candidate criminal background for safety-sensitive positions. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Criminal Verification Research Institute",
        "seo_keywords": ["criminal verification", "criminal checks", "background screening", "candidate safety", "Checkr", "Sterling", "criminal platform", "verification tools"]
    },
    "candidate-data-backup-tools-2026.json": {
        "title": "Candidate Data Backup Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate data backup tools, including data protection, backup automation, and feature comparisons, helping staffing agencies ensure candidate data security and disaster recovery. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Data Backup Research Institute",
        "seo_keywords": ["data backup", "data protection", "backup automation", "disaster recovery", "AWS", "Azure", "backup platform", "data security"]
    },
    "candidate-data-cleaning-tools-2026.json": {
        "title": "Candidate Data Cleaning Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate data cleaning tools, including data quality, deduplication, and feature comparisons, helping staffing agencies maintain accurate and clean candidate databases. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Data Cleaning Research Institute",
        "seo_keywords": ["data cleaning", "data quality", "deduplication", "database maintenance", "Bullhorn", "data platform", "cleaning tools", "data hygiene"]
    },
    "candidate-data-export-tools-2026.json": {
        "title": "Candidate Data Export Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate data export tools, including data migration, export automation, and feature comparisons, helping staffing agencies efficiently export and transfer candidate data. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Data Export Research Institute",
        "seo_keywords": ["data export", "data migration", "export automation", "data transfer", "Bullhorn", "JobAdder", "export platform", "migration tools"]
    },
    "candidate-data-import-tools-2026.json": {
        "title": "Candidate Data Import Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate data import tools, including bulk import, data integration, and feature comparisons, helping staffing agencies efficiently import and integrate candidate data into systems. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Data Import Research Institute",
        "seo_keywords": ["data import", "bulk import", "data integration", "candidate data", "Bullhorn", "JobAdder", "import platform", "integration tools"]
    },
    "candidate-data-migration-tools-2026.json": {
        "title": "Candidate Data Migration Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate data migration tools, including system transfer, data mapping, and feature comparisons, helping staffing agencies seamlessly migrate candidate data between platforms. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Data Migration Research Institute",
        "seo_keywords": ["data migration", "system transfer", "data mapping", "platform migration", "Bullhorn", "migration platform", "transfer tools", "data conversion"]
    },
    "candidate-driving-verification-tools-2026.json": {
        "title": "Candidate Driving Verification Tools: 2026 Platform Deep Comparison",
        "description": "Comprehensive review of 2026 candidate driving verification tools, including driving record checks, license verification, and feature comparisons, helping staffing agencies verify candidate driving background for transportation-related positions. Learn more about features and price comparisons to find the best solution for you! Professional reviews to help you decide!",
        "author": "Driving Verification Research Institute",
        "seo_keywords": ["driving verification", "driving records", "license checks", "candidate background", "Checkr", "GoodHire", "driving platform", "verification tools"]
    }
}

def translate_file(filepath, translation_data):
    """Apply proper translation to a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Apply translations
        if 'title' in translation_data:
            data['title'] = translation_data['title']
        if 'description' in translation_data:
            data['description'] = translation_data['description']
        if 'author' in translation_data:
            data['author'] = translation_data['author']
        if 'seo_keywords' in translation_data:
            data['seo_keywords'] = translation_data['seo_keywords']
        
        # Ensure language field
        data['language'] = 'en-US'
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    directory = Path('data/staffing-recruitment-agency-tools')
    
    print("Applying proper semantic translations to 24 files...\n")
    
    success_count = 0
    for filename, trans_data in translations.items():
        filepath = directory / filename
        if filepath.exists():
            if translate_file(filepath, trans_data):
                print(f"✓ {filename}")
                success_count += 1
            else:
                print(f"✗ {filename} - error")
        else:
            print(f"✗ {filename} - not found")
    
    print(f"\nSuccessfully translated: {success_count} files")
    print(f"Total files processed: {len(translations)}")

if __name__ == '__main__':
    main()
