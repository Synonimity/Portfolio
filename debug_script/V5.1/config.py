# config.py | Version: 5.1.0
# Essential configuration for the debug script.
# Defines paths, filtering rules, and project structure.
# ==============================================================
# "My ideals have no stains. I must correct you.
# People here bear no sins in the eyes of the gods...
# Only laws and the Tribunal can judge someone.
# They can judge even me. So praise my magnificence and purity."
# 
# Furina de Fontaine
# ==============================================================
# "In the past, we sat in our high chairs in the court,
# giving our opinions on isolated cases,
# all the while knowing very little about the human stories
# behind each and every one."
# 
# Furina de Fontaine
# ==============================================================

from pathlib import Path

# ─────────────────────────────────────────────────
# 🧭 PATHS
# ─────────────────────────────────────────────────
# No, not the kind you walk down, silly!

ROOT_PATH = Path(r'D:\Coding')
OUTPUT_PATH = ROOT_PATH / 'Debug'

# ─────────────────────────────────────────────────
# 🚫 FILTERING RULES
# ─────────────────────────────────────────────────
# Like my coffee, strong and rubbish-free!

IGNORED_DIRS = {
    # Version control & tooling
    '.git', '.github', '.vscode', '.idea', '__pycache__', '.pytest_cache',
    'node_modules', '.dart_tool', '.pub', 'venv', 'env', '.venv',
    
    # Build artifacts
    'build', 'dist', 'Debug', '.flutter-plugins', '.flutter-plugins-dependencies',
    
    # Flutter / platform noise (ignored everywhere by design)
    'android', 'ios', 'linux', 'macos', 'windows', 'web',
}

# The allowed extensions for files to be included in the debug process.
ALLOWED_EXTENSIONS = {'.py', '.json', '.yaml', '.yml', '.txt', '.md', '.dart', '.sql'}

# ─────────────────────────────────────────────────
# 📦 BUNDLES
# ─────────────────────────────────────────────────
# "Ugh, it's pouring outside. Good thing I have my umbrella!"
# - Furina de Fontaine

BUNDLE_MAP = {
    # Backend Python files
    'main.py': '01_main.json',
    'entities.py': '02_entities.json',
    'services.py': '03_services.json',
    'routes.py': '04_routes.json',
    'run_backend.py': '05_bootstrap.json',
    
    # Soul definitions
    'core.json': '10_souls_core.json',
    'context.json': '11_souls_context.json',
    'metadata.json': '12_souls_metadata.json',
    
    # Flutter/Dart files
    'main.dart': '20_flutter_main.json',
    'app.dart': '21_flutter_app.json',
    
    # Docs
    'readme.md': '30_docs.json',
    'full_concept.txt': '31_design_docs.json',
}

# ⚖️ BUNDLE LOOKUP (I AM THE LAW)
# Gemma Comment: We use .lower() here to ensure your filenames match regardless of typos!
FILENAME_TO_BUNDLE = {k.lower(): v for k, v in BUNDLE_MAP.items()}

# ─────────────────────────────────────────────────
# ✨ SNAPSHOT MODES
# ─────────────────────────────────────────────────
# New constants to help us toggle between "Full" and "Skeleton"

MODE_FULL = 'full'
MODE_SKELETON = 'skeleton'
MODE_BLUEPRINT = 'blueprint'  # Alias for skeleton

# If this doesn't work, remember: Just keep swimming, just keep swimming...
# 
# It's pouring out here! Wait, the water levels aren't rising, are they?
# - Furina de Fontaine
#
# Is my obsession with a certain character coming through? I hope so :)
