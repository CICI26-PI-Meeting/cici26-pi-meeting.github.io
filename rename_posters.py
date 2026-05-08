#!/usr/bin/env python3
"""Rename poster PDFs and thumbnails to TITLE-AUTHORS format, update YAML."""
import os
import re
import yaml

POSTERS_DIR = "assets/posters"
THUMBS_DIR = "assets/posters/thumbnails"
YAML_FILE = "_data/posters.yml"

def sanitize(text):
    """Convert text to a clean filename component."""
    # Replace colons, commas, and other punctuation with nothing or hyphens
    text = text.replace(":", "").replace(",", "").replace(".", "")
    text = text.replace("'", "").replace('"', "").replace("(", "").replace(")", "")
    text = text.replace("/", "-").replace("&", "and")
    # Replace spaces and multiple hyphens
    text = re.sub(r'[\s]+', '-', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text

with open(YAML_FILE, 'r') as f:
    posters = yaml.safe_load(f)

renames = []
for poster in posters:
    old_filename = poster['filename']
    title_part = sanitize(poster['title'])
    # Use only first author's last name + first name for brevity if many authors
    authors_raw = poster['author']
    author_part = sanitize(authors_raw)
    
    new_filename = f"{title_part}-{author_part}.pdf"
    
    # Truncate if too long (max 200 chars for safety)
    if len(new_filename) > 200:
        new_filename = new_filename[:196] + ".pdf"
    
    renames.append((old_filename, new_filename, poster))

# Check for duplicates
new_names = [r[1] for r in renames]
if len(new_names) != len(set(new_names)):
    dupes = [n for n in new_names if new_names.count(n) > 1]
    print(f"WARNING: Duplicate filenames detected: {set(dupes)}")
    # Add index suffix to duplicates
    seen = {}
    for i, (old, new, poster) in enumerate(renames):
        if new in seen:
            seen[new] += 1
            base = new.rsplit('.pdf', 1)[0]
            renames[i] = (old, f"{base}-{seen[new]}.pdf", poster)
        else:
            seen[new] = 1

# Perform renames
for old_filename, new_filename, poster in renames:
    old_pdf = os.path.join(POSTERS_DIR, old_filename)
    new_pdf = os.path.join(POSTERS_DIR, new_filename)
    
    old_thumb = os.path.join(THUMBS_DIR, old_filename.replace('.pdf', '.png'))
    new_thumb = os.path.join(THUMBS_DIR, new_filename.replace('.pdf', '.png'))
    
    if os.path.exists(old_pdf):
        os.rename(old_pdf, new_pdf)
        print(f"PDF: {old_filename} -> {new_filename}")
    else:
        print(f"MISSING PDF: {old_pdf}")
    
    if os.path.exists(old_thumb):
        os.rename(old_thumb, new_thumb)
    
    poster['filename'] = new_filename

# Remove summary field and write updated YAML
for poster in posters:
    if 'summary' in poster:
        del poster['summary']

with open(YAML_FILE, 'w') as f:
    f.write("# Poster Gallery Data\n")
    f.write("# Each entry should have: title, author, and filename\n")
    f.write("# filename must match the PDF in assets/posters/\n\n")
    for poster in posters:
        f.write(f'- title: "{poster["title"]}"\n')
        f.write(f'  author: "{poster["author"]}"\n')
        f.write(f'  filename: "{poster["filename"]}"\n\n')

print("\nYAML updated successfully!")
