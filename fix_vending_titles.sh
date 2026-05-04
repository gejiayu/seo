#!/bin/bash

# Fix .json artifact in titles for vending machine management tools files
# This script removes the ".json" artifact from titles and descriptions

DIR="/Users/gejiayu/owner/seo/data/vending-machine-management-tools"

for file in "$DIR"/*.json; do
  # Check if file has .json artifact in title
  if grep -q '.json for Vending' "$file"; then
    # Get the current title and fix it
    current_title=$(grep '"title":' "$file" | sed 's/.*"title": "//; s/",.*//')

    # Remove .json from title
    new_title=$(echo "$current_title" | sed 's/\.json//')

    # Also fix description if needed
    current_desc=$(grep '"description":' "$file" | sed 's/.*"description": "//; s/",.*//')
    new_desc=$(echo "$current_desc" | sed 's/\.json//')

    # Use sed to replace
    sed -i '' "s/$current_title/$new_title/" "$file"
    sed -i '' "s/$current_desc/$new_desc/" "$file"

    echo "Fixed: $file"
  fi
done

echo "Done fixing .json artifacts"