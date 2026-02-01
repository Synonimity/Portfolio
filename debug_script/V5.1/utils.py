# utils.py | Version: 5.1.0
# Utility helpers for the debug / export pipeline.

from pathlib import Path
from config import IGNORED_DIRS, OUTPUT_PATH, FILENAME_TO_BUNDLE

# ─────────────────────────────────────────────────
# 📂 PROJECT DISCOVERY
# ─────────────────────────────────────────────────

def list_projects(root):
    """List all project folders in root directory, excluding Debug output"""
    root_path = Path(root)
    # Keep natural filesystem order, skip our 'Debug' output folder
    projects = [
        d for d in root_path.iterdir() 
        if d.is_dir() and d.name != 'Debug' and not d.name.startswith('.')
    ]
    return sorted(projects, key=lambda p: p.name.lower())

def ensure_dir(path):
    """Ensure a directory exists, creating it if necessary"""
    Path(path).mkdir(parents=True, exist_ok=True)

def should_ignore_dir(dirname):
    """Check if a directory should be ignored"""
    return dirname in IGNORED_DIRS or dirname.startswith('.')

# ─────────────────────────────────────────────────
# 📦 BUNDLE RESOLUTION
# ─────────────────────────────────────────────────

def find_bundle(filename):
    """Find which bundle a file belongs to, defaulting to unsorted"""
    return FILENAME_TO_BUNDLE.get(filename.lower(), '99_unsorted.json')

# ─────────────────────────────────────────────────
# 📝 FILENAME GENERATOR
# ─────────────────────────────────────────────────

def generate_output_path(base_path, folder_name, mode):
    """Generate output path with mode suffix"""
    output_dir = Path(base_path) / folder_name
    ensure_dir(output_dir)
    
    if mode == 'skeleton' or mode == 'blueprint':
        return output_dir / f'{folder_name}_blueprint.json'
    else:
        return output_dir / f'{folder_name}_snapshot.json'

# The cake is a lie.
# 42
