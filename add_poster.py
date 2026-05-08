#!/usr/bin/env python3
"""
Add a poster PDF to the gallery.

Usage:
    python add_poster.py /path/to/poster.pdf

This script will:
  1. Ask for the poster title and author(s)
  2. Copy the PDF into assets/posters/ with a standardized filename
  3. Generate a PNG thumbnail (1200px tall) in assets/posters/thumbnails/
  4. Extract text from the PDF via pdftotext
  5. Append the entry to _data/posters.yml
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

# Paths relative to this script's location (project root)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
POSTERS_DIR = os.path.join(SCRIPT_DIR, "assets", "posters")
THUMBS_DIR = os.path.join(POSTERS_DIR, "thumbnails")
YAML_FILE = os.path.join(SCRIPT_DIR, "_data", "posters.yml")
THUMB_HEIGHT = 1200  # pixels — matches existing thumbnails


def sanitize(text):
    """Convert text to a clean filename component (matches rename_posters.py)."""
    text = text.replace(":", "").replace(",", "").replace(".", "")
    text = text.replace("'", "").replace('"', "").replace("(", "").replace(")", "")
    text = text.replace("/", "-").replace("&", "and")
    text = re.sub(r'[\s]+', '-', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text


def generate_thumbnail(pdf_path, thumb_path):
    """Render the first page of a PDF as a PNG thumbnail at THUMB_HEIGHT px tall."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_prefix = os.path.join(tmp, "page")

        # pdftoppm renders PDF page -> PPM/PNG; -f 1 -l 1 = first page only
        subprocess.run(
            ["pdftoppm", "-png", "-f", "1", "-l", "1", "-scale-to", str(THUMB_HEIGHT),
             pdf_path, tmp_prefix],
            check=True, capture_output=True
        )

        # pdftoppm names the output <prefix>-1.png (or -01.png depending on page count)
        candidates = [f for f in os.listdir(tmp) if f.endswith(".png")]
        if not candidates:
            raise RuntimeError("pdftoppm produced no PNG output")

        rendered = os.path.join(tmp, candidates[0])
        shutil.move(rendered, thumb_path)

    print(f"  Thumbnail saved: {thumb_path}")


def extract_text(pdf_path):
    """Extract text from a PDF using pdftotext (matches extract_pdf_text.py)."""
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", pdf_path, "-"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            text = result.stdout.strip()
            text = re.sub(r'\s+', ' ', text)
            text = text.replace('\\', '\\\\').replace('"', '\\"')
            return text
        else:
            print(f"  WARNING: pdftotext failed: {result.stderr}")
            return ""
    except Exception as e:
        print(f"  ERROR extracting text: {e}")
        return ""


def append_to_yaml(title, author, filename, pdf_text):
    """Append a new poster entry to posters.yml."""
    with open(YAML_FILE, 'a') as f:
        f.write(f'- title: "{title}"\n')
        f.write(f'  author: "{author}"\n')
        f.write(f'  filename: "{filename}"\n')
        f.write(f'  pdfText: "{pdf_text}"\n')
        f.write('\n')
    print(f"  Added entry to {YAML_FILE}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python add_poster.py /path/to/poster.pdf")
        sys.exit(1)

    pdf_path = os.path.abspath(sys.argv[1])
    if not os.path.isfile(pdf_path):
        print(f"Error: file not found: {pdf_path}")
        sys.exit(1)
    if not pdf_path.lower().endswith(".pdf"):
        print("Error: file must be a PDF")
        sys.exit(1)

    # --- Prompt for metadata ---
    title = input("Enter poster title: ").strip()
    if not title:
        print("Error: title cannot be empty")
        sys.exit(1)

    author = input("Enter author(s): ").strip()
    if not author:
        print("Error: author cannot be empty")
        sys.exit(1)

    # --- Build standardized filename ---
    title_part = sanitize(title)
    author_part = sanitize(author)
    new_filename = f"{title_part}-{author_part}.pdf"
    if len(new_filename) > 200:
        new_filename = new_filename[:196] + ".pdf"

    dest_pdf = os.path.join(POSTERS_DIR, new_filename)
    dest_thumb = os.path.join(THUMBS_DIR, new_filename.replace(".pdf", ".png"))

    # --- Check for duplicates ---
    if os.path.exists(dest_pdf):
        print(f"Warning: {new_filename} already exists in {POSTERS_DIR}")
        overwrite = input("Overwrite? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("Aborted.")
            sys.exit(0)

    # --- Copy PDF ---
    shutil.copy2(pdf_path, dest_pdf)
    print(f"  Copied PDF to {dest_pdf}")

    # --- Generate thumbnail ---
    print("  Generating thumbnail...")
    try:
        generate_thumbnail(dest_pdf, dest_thumb)
    except Exception as e:
        print(f"  ERROR generating thumbnail: {e}")
        print("  (Continuing without thumbnail)")

    # --- Extract text ---
    print("  Extracting PDF text...")
    pdf_text = extract_text(dest_pdf)
    print(f"  Extracted {len(pdf_text)} characters")

    # --- Append to YAML ---
    # Escape title/author for YAML (double quotes inside the value)
    yaml_title = title.replace('\\', '\\\\').replace('"', '\\"')
    yaml_author = author.replace('\\', '\\\\').replace('"', '\\"')
    append_to_yaml(yaml_title, yaml_author, new_filename, pdf_text)

    print(f"\nDone! Poster \"{title}\" has been added.")


if __name__ == "__main__":
    main()
