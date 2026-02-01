# snapshot_export.py | Version: 5.1.0
# Builds a semantic snapshot of a project as JSON
# Preserves actual filesystem hierarchy and order.

import json
from pathlib import Path
from config import ALLOWED_EXTENSIONS, MODE_SKELETON, MODE_BLUEPRINT
from utils import should_ignore_dir, find_bundle

# ─────────────────────────────────────────────────
# 🦴 SKELETON LOGIC
# ─────────────────────────────────────────────────

def skeletonize(content: str, ext: str, filename: str | None = None):
    """
    Convert file content to skeleton (structure only, no implementation)
    Keeps: comments, class/function signatures, structural keywords
    Drops: imports, implementation logic
    """
    
    # ─────────────────────────────────────────────────
    # 🧠 RULE 0: __init__.py is sacred
    # ─────────────────────────────────────────────────
    if filename and filename.lower() == '__init__.py':
        return content
    
    # Only skeletonize code files
    if ext not in {'.py', '.dart'}:
        return content
    
    lines = content.split('\n')
    skeleton_lines = []
    
    for line in lines:
        stripped = line.lstrip()
        
        # ─────────────────────────────────────────────────
        # 🚫 DROP ALL IMPORTS (blueprint rule)
        # ─────────────────────────────────────────────────
        if stripped.startswith(('import ', 'from ')):
            continue
        
        # ─────────────────────────────────────────────────
        # ✅ KEEP STRUCTURAL SIGNAL
        # ─────────────────────────────────────────────────
        # Python structural keywords
        if any(stripped.startswith(kw) for kw in [
            'class ', 'def ', 'async def ', '@dataclass', '@property',
            'if __name__', 'try:', 'except:', 'finally:', 'with '
        ]):
            skeleton_lines.append(line)
            continue
        
        # Dart-specific structural keywords
        if ext == '.dart' and any(stripped.startswith(kw) for kw in [
            'class ', 'abstract class ', 'enum ', 'extension ',
            'void ', 'Future', 'Widget ', 'State<'
        ]):
            skeleton_lines.append(line)
            continue
        
        # ─────────────────────────────────────────────────
        # 📝 KEEP FILE-LEVEL & DOC COMMENTS
        # ─────────────────────────────────────────────────
        if stripped.startswith('#') or stripped.startswith('//') or '"""' in line or "'''" in line:
            skeleton_lines.append(line)
            continue
        
        # ─────────────────────────────────────────────────
        # ⬜ KEEP EMPTY LINES (readability)
        # ─────────────────────────────────────────────────
        if not stripped:
            skeleton_lines.append(line)
            continue
        
        # ─────────────────────────────────────────────────
        # ❌ EVERYTHING ELSE IS LOGIC → DROP
        # ─────────────────────────────────────────────────
    
    return '\n'.join(skeleton_lines)


# ─────────────────────────────────────────────────
# 📤 EXPORT ENGINE
# ─────────────────────────────────────────────────

def export_snapshot(project_path, output_file, mode):
    """
    Export project as structured JSON snapshot
    
    Args:
        project_path: Path to project folder
        output_file: Output JSON file path
        mode: 'full' or 'skeleton'/'blueprint'
    """
    project_path = Path(project_path)
    files_data = []
    stats = {'total_files': 0, 'by_language': {}}
    
    def walk_directory(dir_path, relative_to):
        """Recursively walk directory and collect files"""
        for item in sorted(dir_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
            if item.is_dir():
                if should_ignore_dir(item.name):
                    continue
                walk_directory(item, relative_to)
            elif item.is_file():
                ext = item.suffix.lower()
                if ext not in ALLOWED_EXTENSIONS:
                    continue
                
                rel_path = item.relative_to(relative_to)
                bundle = find_bundle(item.name)
                
                try:
                    content = item.read_text(encoding='utf-8')
                    
                    # Apply skeleton logic if requested
                    if mode in [MODE_SKELETON, MODE_BLUEPRINT]:
                        content = skeletonize(content, ext, item.name)
                    
                    files_data.append({
                        'path': str(rel_path).replace('\\', '\\\\'),
                        'bundle': bundle,
                        'language': ext[1:],  # Remove the dot
                        'content': content
                    })
                    
                    stats['total_files'] += 1
                    lang = ext[1:]
                    stats['by_language'][lang] = stats['by_language'].get(lang, 0) + 1
                    
                except Exception as e:
                    print(f"⚠️  Could not read {rel_path}: {e}")
    
    # Walk the project
    walk_directory(project_path, project_path)
    
    # Build output structure
    output = {
        'metadata': {
            'project_name': project_path.name,
            'export_mode': mode
        },
        'root': project_path.name,
        'files': files_data,
        'stats': stats
    }
    
    # Write JSON
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported {stats['total_files']} files to {output_file}")
    return output_file