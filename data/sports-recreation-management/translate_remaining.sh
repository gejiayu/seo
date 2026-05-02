#!/bin/bash

# List of files still needing translation based on earlier checks
files=(
  "tennis-club-management-software-comprehensive-review.json"
  "trail-running-event-management-system-comprehensive-review.json"
  "volleyball-court-management-software-deep-analysis.json"
  "water-park-management-software-deep-analysis.json"
  "wrestling-club-management-software-comprehensive-review.json"
  "yoga-studio-management-software-comprehensive-review.json"
  "youth-athlete-development-tracking-system-comprehensive-review.json"
  "youth-sports-league-management-system-deep-review.json"
  "youth-sports-registration-platform-comprehensive-review.json"
)

for file in "${files[@]}"; do
  if [ -f "$file" ]; then
    # Check if file has Chinese title
    if grep -qP '[\p{Han}]' "$file"; then
      echo "Needs translation: $file"
    else
      echo "Already English: $file"
    fi
  fi
done
