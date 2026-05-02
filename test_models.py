#!/usr/bin/env python3
from anthropic import Anthropic

client = Anthropic()

models_to_try = [
    'claude-3-5-haiku-20241022',
    'claude-3-5-sonnet-20240620',
    'claude-3-haiku-20240307',
    'claude-3-sonnet-20240229',
    'claude-2.1',
    'claude-2',
    'claude-instant-1.2'
]

print("Testing models...")
for model in models_to_try:
    try:
        message = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{'role': 'user', 'content': 'test'}]
        )
        print(f'✓ {model} works!')
        print(f'  Response: {message.content[0].text}')
        break
    except Exception as e:
        print(f'✗ {model} failed: {str(e)[:150]}')