#!/bin/bash
# Script to check which files still need translation

echo "Files with Chinese characters:"
grep -l "[一-龥]" /Users/gejiayu/owner/seo/data/agricultural-farming-rental-tools/*.json | wc -l

echo "\nRemaining files to translate:"
grep -l "[一-龥]" /Users/gejiayu/owner/seo/data/agricultural-farming-rental-tools/*.json