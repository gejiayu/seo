#!/bin/bash

# Process all JSON files in religious-nonprofit-organization-tools directory
# Generate Chinese translations for each file

EN_DIR="/Users/gejiayu/owner/seo/data/religious-nonprofit-organization-tools"
ZH_DIR="/Users/gejiayu/owner/seo/data-zh/religious-nonprofit-organization-tools"

# Create target directory if it doesn't exist
mkdir -p "$ZH_DIR"

# Get list of all JSON files
FILES=$(ls "$EN_DIR"/*.json)

for FILE in $FILES; do
  FILENAME=$(basename "$FILE")
  echo "Processing: $FILENAME"

  # Use claude to generate Chinese version
  claude --print "Read the JSON file at $FILE and create a Chinese translation. Output ONLY the complete JSON content (no explanations). The JSON should have:
- title translated to Chinese
- description translated to Chinese (keep it concise, 150-160 chars)
- content HTML translated to Chinese (all headings, paragraphs, lists, tables - keep HTML structure intact)
- seo_keywords translated to Chinese keywords (array format, NOT string)
- language changed to 'zh-CN'
- canonical_link changed to Chinese version (replace /posts/ with /zh/posts/)
- alternate_links updated with zh-CN as canonical and en-US as alternate
- Keep same slug, published_at, author, and category
Output valid JSON only." > "$ZH_DIR/$FILENAME"

  sleep 1
done

echo "Done! Processed $(ls "$ZH_DIR"/*.json | wc -l) files"