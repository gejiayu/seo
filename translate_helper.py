#!/usr/bin/env python3
"""
Script to translate Chinese content in JSON files to English.
This is a helper script for tracking progress, actual translation done manually.
"""

import json
import os
from pathlib import Path

def count_files_to_translate(directory):
    """Count total files in directory."""
    json_files = list(Path(directory).glob "*.json")
    return len(json_files)

def list_all_files(directory):
    """List all JSON files in directory."""
    json_files = list(Path(directory).glob "*.json")
    return [f.name for f in json_files]

if __name__ == "__main__":
    directory = "/Users/gejiayu/owner/seo/data/tennis-racket-rental-tools"
    total = count_files_to_translate(directory)
    files = list_all_files(directory)

    print(f"Total files: {total}")
    print(f"Files list:")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")