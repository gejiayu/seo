#!/usr/bin/env python3
"""
Convert Markdown content in JSON files to HTML format.
Handles: ## headers, **bold**, - lists, | tables, numbered lists, code blocks
"""

import json
import re
import os
from pathlib import Path

def convert_markdown_to_html(content):
    """Convert Markdown syntax to HTML tags."""

    # Convert code blocks (```text``` -> <pre><code>text</code></pre>)
    content = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', content, flags=re.DOTALL)

    # Convert headers: ## -> <h2>, ### -> <h3>
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)

    # Convert bold: **text** -> <strong>text</strong>
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)

    # Convert unordered lists: - item -> <li>item</li>
    # Need to group consecutive list items into <ul>
    lines = content.split('\n')
    in_list = False
    new_lines = []
    list_items = []

    for line in lines:
        # Check if line is a list item (- or bullet)
        if re.match(r'^- (.+)$', line) or re.match(r'^• (.+)$', line):
            if not in_list:
                in_list = True
                list_items = []
            item_text = re.sub(r'^- (.+)$', r'\1', line)
            item_text = re.sub(r'^• (.+)$', r'\1', item_text)
            list_items.append(f'<li>{item_text}</li>')
        else:
            if in_list:
                # End the list
                new_lines.append('<ul>')
                new_lines.extend(list_items)
                new_lines.append('</ul>')
                list_items = []
                in_list = False
            new_lines.append(line)

    # Handle remaining list items
    if in_list:
        new_lines.append('<ul>')
        new_lines.extend(list_items)
        new_lines.append('</ul>')

    content = '\n'.join(new_lines)

    # Convert numbered lists: 1. item -> <li>item</li> wrapped in <ol>
    lines = content.split('\n')
    in_ol = False
    new_lines = []
    ol_items = []

    for line in lines:
        if re.match(r'^\d+\. (.+)$', line):
            if not in_ol:
                in_ol = True
                ol_items = []
            item_text = re.sub(r'^\d+\. (.+)$', r'\1', line)
            ol_items.append(f'<li>{item_text}</li>')
        else:
            if in_ol:
                new_lines.append('<ol>')
                new_lines.extend(ol_items)
                new_lines.append('</ol>')
                ol_items = []
                in_ol = False
            new_lines.append(line)

    if in_ol:
        new_lines.append('<ol>')
        new_lines.extend(ol_items)
        new_lines.append('</ol>')

    content = '\n'.join(new_lines)

    # Convert tables: Markdown tables -> HTML tables
    # Pattern: | header | header | followed by |---|---| and rows
    content = convert_tables(content)

    # Convert paragraphs: double newlines -> <p> tags (for non-tagged content)
    paragraphs = []
    parts = content.split('\n\n')
    for part in parts:
        part = part.strip()
        if part:
            # Don't wrap if it's already a HTML tag
            if not part.startswith('<') and not re.match(r'^<h[23]|^<ul|^<ol|^<pre|^<table', part):
                paragraphs.append(f'<p>{part}</p>')
            else:
                paragraphs.append(part)

    content = '\n\n'.join(paragraphs)

    # Clean up extra whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content

def convert_tables(content):
    """Convert Markdown tables to HTML tables."""
    lines = content.split('\n')
    result_lines = []
    table_lines = []
    in_table = False

    for line in lines:
        # Check if line is part of a table
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
        else:
            if in_table:
                # Process the table
                html_table = process_table(table_lines)
                result_lines.append(html_table)
                table_lines = []
                in_table = False
            result_lines.append(line)

    if in_table:
        html_table = process_table(table_lines)
        result_lines.append(html_table)

    return '\n'.join(result_lines)

def process_table(table_lines):
    """Process collected table lines into HTML table."""
    if len(table_lines) < 2:
        return '\n'.join(table_lines)

    # First line is header
    header_line = table_lines[0]
    headers = [cell.strip() for cell in header_line.split('|')[1:-1]]

    # Second line is separator (|---|---|), skip it
    # Remaining lines are data rows
    rows = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        if cells:
            rows.append(cells)

    # Build HTML table
    html = '<table>\n<thead>\n<tr>\n'
    for header in headers:
        html += f'<th>{header}</th>\n'
    html += '</tr>\n</thead>\n<tbody>\n'

    for row in rows:
        html += '<tr>\n'
        for cell in row:
            # Convert any remaining markdown in cells
            cell = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', cell)
            # Convert checkmarks
            cell = re.sub(r'✓', '✓', cell)
            html += f'<td>{cell}</td>\n'
        html += '</tr>\n'

    html += '</tbody>\n</table>'
    return html

def process_json_file(filepath):
    """Process a single JSON file."""
    print(f"Processing: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Convert content field
    if 'content' in data:
        data['content'] = convert_markdown_to_html(data['content'])

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✓ Converted: {filepath}")

def main():
    """Process all JSON files in data directories."""
    data_dir = Path('/Users/gejiayu/owner/seo/data')

    # Process all categories
    for category_dir in data_dir.iterdir():
        if category_dir.is_dir():
            for json_file in category_dir.glob('*.json'):
                try:
                    process_json_file(json_file)
                except Exception as e:
                    print(f"Error processing {json_file}: {e}")

    print("\n✓ All files converted!")

if __name__ == '__main__':
    main()