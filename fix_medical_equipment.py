#!/usr/bin/env python3
"""
Script to fix broken machine translation in medical-equipment-rental-tools JSON files.
Uses intelligent word segmentation and proper spacing.
"""

import json
import re
import os
from pathlib import Path

DATA_DIR = "/Users/gejiayu/owner/seo/data/medical-equipment-rental-tools"

# Pattern to detect Chinese characters
CHINESE_PATTERN = re.compile(r'[一-鿿]')

# Common medical equipment rental terms for intelligent segmentation
MEDICAL_TERMS = [
    'medical', 'equipment', 'rental', 'management', 'system', 'review',
    'diagnostic', 'laboratory', 'tracking', 'control', 'quality',
    'maintenance', 'calibration', 'result', 'detect', 'test',
    'agent', 'inventory', 'report', 'plan', 'record', 'analysis',
    'prediction', 'fault', 'repair', 'warning', 'alert', 'audit',
    'depreciation', 'asset', 'financial', 'accounting', 'billing',
    'payment', 'invoice', 'contract', 'customer', 'vendor',
    'supplier', 'order', 'delivery', 'pickup', 'scheduling',
    'reservation', 'booking', 'availability', 'capacity',
    'performance', 'efficiency', 'optimization', 'automation',
    'ai', 'smart', 'intelligent', 'digital', 'platform',
    'suite', 'tool', 'application', 'software', 'solution',
    'aesthetic', 'cardiac', 'emergency', 'home', 'icu',
    'critical', 'care', 'infusion', 'pump', 'sterilization',
    'disinfection', 'imaging', 'xray', 'ultrasound', 'monitoring',
    'vital', 'sign', 'therapy', 'rehabilitation', 'surgical',
    'operation', 'procedure', 'clinical', 'hospital', 'clinic',
    'healthcare', 'health', 'patient', 'doctor', 'nurse',
    'staff', 'user', 'admin', 'manager', 'specialist',
    'professional', 'basic', 'standard', 'advanced', 'premium',
    'enterprise', 'cloud', 'mobile', 'web', 'api', 'integration',
    'comprehensive', 'full', 'process', 'workflow', 'dashboard',
    'visualization', 'data', 'storage', 'backup', 'security',
    'compliance', 'regulation', 'standard', 'certification',
    'birthization', 'biochemical', 'blood', 'cell', 'urine',
    'pcr', 'microscope', 'centrifuge', 'analyzer', 'scanner',
    'monitor', 'thermometer', 'scale', 'bed', 'wheelchair',
    'stretcher', 'ventilator', 'oxygen', 'concentrator',
    'nebulizer', 'dialysis', 'radiation', 'therapy',
    'comparison', 'table', 'dimension', 'functionality',
    'pricing', 'fee', 'cost', 'budget', 'roi', 'value',
    'benefit', 'advantage', 'feature', 'capability', 'option',
    'selection', 'recommendation', 'guide', 'strategy',
    'trend', 'future', 'industry', 'market', 'demand',
    'growth', 'development', 'innovation', 'technology',
    'digital', 'transformation', 'modernization', 'upgrade',
    'implementation', 'deployment', 'installation', 'setup',
    'training', 'support', 'service', 'maintenance',
    'indoor', 'inter', 'room', 'cross', 'external',
    'internal', 'local', 'remote', 'online', 'offline',
    'real', 'time', 'instant', 'automatic', 'manual',
    'preventive', 'corrective', 'scheduled', 'emergency',
    'urgent', 'priority', 'high', 'medium', 'low',
    'number', 'amount', 'quantity', 'volume', 'count',
    'type', 'category', 'class', 'group', 'batch',
    'individual', 'single', 'multiple', 'combined',
    'integrated', 'centralized', 'distributed',
    'accuracy', 'precision', 'reliability', 'validity',
    'traceability', 'audit', 'history', 'log', 'timeline',
    'trend', 'chart', 'graph', 'metric', 'indicator',
    'kpi', 'measure', 'assessment', 'evaluation',
    'verification', 'validation', 'confirmation',
    'approval', 'rejection', 'status', 'state',
    'active', 'inactive', 'pending', 'completed',
    'failed', 'success', 'error', 'warning',
    'compliant', 'non', 'standard', 'professional',
    'version', 'edition', 'package', 'bundle', 'module',
    'extension', 'plugin', 'addon', 'feature', 'option',
    'customize', 'configuration', 'setting', 'parameter',
    'property', 'attribute', 'field', 'value', 'data',
    'format', 'structure', 'schema', 'model', 'design',
    'architecture', 'framework', 'foundation', 'base',
    'core', 'main', 'primary', 'secondary', 'auxiliary',
    'supporting', 'additional', 'extra', 'optional',
    'required', 'mandatory', 'essential', 'critical',
    'important', 'significant', 'relevant', 'appropriate',
    'suitable', 'compatible', 'adaptable', 'flexible',
    'scalable', 'extensible', 'modular', 'unified',
    'consolidated', 'streamlined', 'simplified',
    'automated', 'manual', 'hybrid', 'mixed',
    'combined', 'separate', 'independent', 'isolated',
    'connected', 'linked', 'related', 'associated',
    'corresponding', 'matching', 'equivalent',
    'similar', 'identical', 'distinct', 'different',
    'unique', 'specific', 'general', 'common',
    'typical', 'standard', 'custom', 'specialized',
    'dedicated', 'exclusive', 'shared', 'public',
    'private', 'protected', 'secured', 'open',
    'closed', 'visible', 'hidden', 'accessible',
    'restricted', 'allowed', 'permitted', 'authorized',
    'authenticated', 'verified', 'validated',
    'trustworthy', 'credible', 'reliable', 'dependable',
    'stable', 'robust', 'resilient', 'fault',
    'tolerant', 'error', 'handling', 'exception',
    'failure', 'crash', 'breakdown', 'malfunction',
    'defect', 'bug', 'issue', 'problem', 'difficulty',
    'challenge', 'obstacle', 'barrier', 'limitation',
    'constraint', 'restriction', 'condition',
    'requirement', 'specification', 'expectation',
    'objective', 'goal', 'target', 'purpose',
    'intent', 'aim', 'ambition', 'vision', 'mission',
    'strategy', 'plan', 'roadmap', 'timeline',
    'schedule', 'milestone', 'phase', 'stage',
    'step', 'action', 'task', 'job', 'work',
    'operation', 'execution', 'implementation',
    'realization', 'achievement', 'completion',
    'finalization', 'conclusion', 'ending',
    'termination', 'stop', 'pause', 'resume',
    'restart', 'continue', 'proceed', 'advance',
    'progress', 'development', 'evolution',
    'improvement', 'enhancement', 'optimization',
    'refinement', 'adjustment', 'modification',
    'change', 'update', 'upgrade', 'revision',
    'correction', 'fix', 'repair', 'restoration',
    'recovery', 'return', 'revert', 'rollback',
    'backup', 'restore', 'archive', 'delete',
    'remove', 'clear', 'purge', 'clean', 'wipe',
    'erase', 'forget', 'remember', 'recall',
    'retrieve', 'fetch', 'load', 'save', 'store',
    'keep', 'hold', 'maintain', 'preserve',
    'protect', 'secure', 'guard', 'defend',
    'shield', 'cover', 'wrap', 'envelop',
    'enclose', 'contain', 'include', 'involve',
    'engage', 'participate', 'contribute',
    'collaborate', 'cooperate', 'work', 'team',
    'group', 'collective', 'joint', 'shared',
    'mutual', 'reciprocal', 'bilateral',
    'two', 'way', 'direction', 'channel',
    'path', 'route', 'way', 'method', 'approach',
    'technique', 'procedure', 'process',
    'algorithm', 'logic', 'rule', 'principle',
    'concept', 'idea', 'thought', 'notion',
    'theory', 'hypothesis', 'assumption',
    'postulate', 'premise', 'foundation',
    'ground', 'base', 'root', 'source',
    'origin', 'start', 'begin', 'initial',
    'first', 'primary', 'main', 'leading',
    'head', 'top', 'upper', 'higher',
    'maximum', 'peak', 'optimal', 'best',
    'superior', 'better', 'improved',
    'enhanced', 'advanced', 'modern',
    'current', 'latest', 'recent', 'new',
    'upcoming', 'future', 'next', 'following',
    'subsequent', 'later', 'after', 'post',
    'final', 'last', 'end', 'terminal',
    'concluding', 'closing', 'finishing',
    'completing', 'done', 'finished',
    'accomplished', 'achieved', 'realized',
    'fulfilled', 'satisfied', 'content',
    'happy', 'pleased', 'glad', 'delighted',
    'satisfied', 'fulfilled', 'content',
    'complete', 'total', 'whole', 'full',
    'entire', 'comprehensive', 'all',
    'every', 'each', 'any', 'some',
    'few', 'many', 'several', 'multiple',
    'various', 'diverse', 'different',
    'distinct', 'unique', 'individual',
    'personal', 'private', 'own',
    'self', 'auto', 'automatic', 'autonomous',
    'independent', 'standalone', 'separate',
    'isolated', 'detached', 'removed',
    'distant', 'remote', 'external',
    'outside', 'foreign', 'alien',
    'strange', 'unusual', 'uncommon',
    'rare', 'scarce', 'limited',
    'restricted', 'controlled', 'regulated',
    'governed', 'managed', 'directed',
    'guided', 'led', 'supervised',
    'monitored', 'observed', 'watched',
    'tracked', 'followed', 'chased',
    'pursued', 'seek', 'search', 'find',
    'discover', 'identify', 'recognize',
    'detect', 'sense', 'perceive',
    'observe', 'notice', 'realize',
    'understand', 'comprehend', 'grasp',
    'know', 'learn', 'study', 'examine',
    'investigate', 'research', 'explore',
    'analyze', 'assess', 'evaluate',
    'review', 'critique', 'judge',
    'rate', 'score', 'grade', 'mark',
    'measure', 'quantify', 'calculate',
    'compute', 'estimate', 'predict',
    'forecast', 'project', 'anticipate',
    'expect', 'hope', 'wish', 'desire',
    'want', 'need', 'require', 'demand',
    'request', 'ask', 'inquire', 'query',
    'question', 'interrogate', 'interview',
    'consult', 'advise', 'recommend',
    'suggest', 'propose', 'offer',
    'present', 'show', 'display',
    'exhibit', 'demonstrate', 'prove',
    'verify', 'confirm', 'validate',
    'authenticate', 'authorize',
    'certify', 'accredit', 'approve',
    'accept', 'agree', 'consent',
    'permit', 'allow', 'enable',
    'facilitate', 'support', 'assist',
    'help', 'aid', 'guide', 'direct',
    'instruct', 'teach', 'train',
    'educate', 'inform', 'notify',
    'announce', 'declare', 'state',
    'claim', 'assert', 'affirm',
    'confirm', 'verify', 'validate'
]

def smart_word_segmentation(text):
    """
    Intelligently segment concatenated words into proper English text.
    Uses dictionary-based longest match approach.
    """
    if not text:
        return text

    # Sort terms by length (longest first) for greedy matching
    sorted_terms = sorted(MEDICAL_TERMS, key=len, reverse=True)

    # Create pattern for all terms
    result = []
    i = 0
    while i < len(text):
        matched = False
        # Try to match longest possible term
        for term in sorted_terms:
            if text[i:i+len(term)].lower() == term.lower():
                # Match found
                result.append(term.capitalize())
                i += len(term)
                matched = True
                break

        if not matched:
            # No match, keep character
            result.append(text[i])
            i += 1

    # Join with proper spacing
    segmented = ''.join(result)

    # Clean up spacing issues
    # Remove multiple spaces
    segmented = re.sub(r'\s+', ' ', segmented)
    # Add space after colons
    segmented = re.sub(r':', ': ', segmented)
    segmented = re.sub(r'::+', ': ', segmented)
    # Add space before colons if needed
    segmented = re.sub(r'(\w):', r'\1: ', segmented)
    # Fix double spaces
    segmented = re.sub(r'\s+', ' ', segmented)

    return segmented

def fix_broken_translation(text):
    """
    Fix broken machine translation by segmenting concatenated words.
    """
    if not text:
        return text

    # Pattern to find long concatenated lowercase words (30+ chars)
    # Split them into proper words

    # For HTML content, we need to be careful
    if '<h' in text or '<p' in text or '<li' in text or '<table' in text:
        # Process HTML content - extract and fix text parts
        # Split by HTML tags
        parts = re.split(r'(<[^>]+>)', text)
        fixed_parts = []

        for part in parts:
            if part.startswith('<') and part.endswith('>'):
                # HTML tag - keep as is
                fixed_parts.append(part)
            else:
                # Text content - fix it
                # Find concatenated words
                words = part.split()
                fixed_words = []
                for word in words:
                    if len(word) > 30 and word.islower():
                        # This is a broken word - segment it
                        segmented = smart_word_segmentation(word)
                        fixed_words.append(segmented)
                    else:
                        fixed_words.append(word)

                fixed_parts.append(' '.join(fixed_words))

        return ''.join(fixed_parts)
    else:
        # Plain text - fix concatenated words
        words = text.split()
        fixed_words = []
        for word in words:
            # Check if this word is a broken concatenation
            # Look for patterns like long lowercase strings
            if re.match(r'[a-z]{30,}', word):
                # Segment it
                segmented = smart_word_segmentation(word)
                fixed_words.append(segmented)
            elif len(word) > 30:
                # Might be broken
                # Check for mixed case issues
                segmented = smart_word_segmentation(word.lower())
                fixed_words.append(segmented)
            else:
                fixed_words.append(word)

        return ' '.join(fixed_words)

def fix_file(filepath):
    """Fix a single JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Fix title
    if 'title' in data:
        data['title'] = fix_broken_translation(data['title'])

    # Fix description
    if 'description' in data:
        data['description'] = fix_broken_translation(data['description'])

    # Fix content
    if 'content' in data:
        data['content'] = fix_broken_translation(data['content'])

    # Fix seo_keywords
    if 'seo_keywords' in data:
        if isinstance(data['seo_keywords'], str):
            # Convert string to array
            keywords = data['seo_keywords'].split(',')
            data['seo_keywords'] = [kw.strip() for kw in keywords]

        # Fix broken keywords
        fixed_keywords = []
        for kw in data['seo_keywords']:
            if re.match(r'[a-z]{30,}', kw):
                # Broken keyword - segment it
                segmented = smart_word_segmentation(kw)
                # Keywords should be lowercase with spaces
                fixed_keywords.append(segmented.lower())
            else:
                fixed_keywords.append(kw)

        data['seo_keywords'] = fixed_keywords

    # Add language field
    data['language'] = 'en-US'

    # Save fixed file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return True

def main():
    """Main processing function."""
    files = sorted(Path(DATA_DIR).glob('*.json'))

    print(f"Total files to process: {len(files)}\n")

    fixed_count = 0
    error_count = 0

    for i, filepath in enumerate(files):
        try:
            if fix_file(filepath):
                fixed_count += 1
                print(f"[{i+1}/{len(files)}] Fixed: {filepath.name}")
        except Exception as e:
            error_count += 1
            print(f"[{i+1}/{len(files)}] Error fixing {filepath.name}: {e}")

    print(f"\nFixed: {fixed_count} files")
    print(f"Errors: {error_count} files")

if __name__ == "__main__":
    main()