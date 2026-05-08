#!/usr/bin/env python3
"""
Extract text from poster PDFs using pdftotext and add pdfText to posters.yml.
No external dependencies required.
"""

import subprocess
import os
import re

POSTERS_YML = "_data/posters.yml"
POSTERS_DIR = "assets/posters"

def extract_text(pdf_path):
    """Run pdftotext on a PDF and return the extracted text as a single line."""
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", pdf_path, "-"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            text = result.stdout.strip()
            # Collapse all whitespace into single spaces
            text = re.sub(r'\s+', ' ', text)
            # Escape any double quotes and backslashes for YAML
            text = text.replace('\\', '\\\\').replace('"', '\\"')
            return text
        else:
            print(f"  WARNING: pdftotext failed for {pdf_path}: {result.stderr}")
            return ""
    except Exception as e:
        print(f"  ERROR: {e} for {pdf_path}")
        return ""

def parse_posters(yml_path):
    """Parse the simple posters.yml format (list of items with title, author, filename)."""
    posters = []
    current = {}
    with open(yml_path, 'r') as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith('#') or stripped == '':
                continue
            if stripped.startswith('- '):
                if current:
                    posters.append(current)
                current = {}
                # Parse the first key on the '- ' line
                rest = stripped[2:]  # Remove '- '
                key, val = parse_kv(rest)
                if key:
                    current[key] = val
            elif ':' in stripped and current is not None:
                key, val = parse_kv(stripped)
                if key:
                    current[key] = val
        if current:
            posters.append(current)
    return posters

def parse_kv(s):
    """Parse 'key: "value"' or 'key: value'."""
    m = re.match(r'(\w+):\s*"(.*)"', s)
    if m:
        return m.group(1), m.group(2)
    m = re.match(r'(\w+):\s*(.*)', s)
    if m:
        return m.group(1), m.group(2).strip()
    return None, None

def write_posters(posters, yml_path):
    """Write posters back to YAML."""
    with open(yml_path, 'w') as f:
        f.write("# Poster Gallery Data\n")
        f.write("# Each entry should have: title, author, and filename\n")
        f.write("# filename must match the PDF in assets/posters/\n")
        f.write("\n")
        for poster in posters:
            f.write(f'- title: "{poster.get("title", "")}"\n')
            f.write(f'  author: "{poster.get("author", "")}"\n')
            f.write(f'  filename: "{poster.get("filename", "")}"\n')
            pdf_text = poster.get("pdfText", "")
            f.write(f'  pdfText: "{pdf_text}"\n')
            f.write('\n')

def main():
    posters = parse_posters(POSTERS_YML)
    print(f"Found {len(posters)} posters in {POSTERS_YML}")

    for poster in posters:
        filename = poster.get("filename", "")
        pdf_path = os.path.join(POSTERS_DIR, filename)
        if os.path.exists(pdf_path):
            print(f"Extracting: {filename}")
            text = extract_text(pdf_path)
            poster["pdfText"] = text
            print(f"  -> {len(text)} chars")
        else:
            print(f"  MISSING: {pdf_path}")
            poster["pdfText"] = ""

    write_posters(posters, POSTERS_YML)
    print(f"\nDone! Updated {POSTERS_YML} with pdfText for {len(posters)} posters.")

if __name__ == "__main__":
    main()
