# snapshot_export.py | Version: 5.2.0
import json
from pathlib import Path
from config import ALLOWED_EXTENSIONS, MODE_SKELETON, MODE_BLUEPRINT, IGNORED_FILES
from utils import should_ignore_dir, find_bundle

def skeletonize(content: str, ext: str, filename: str | None = None):
    """
    Returns: (processed_content, list_of_imports)
    """
    if filename and filename.lower() == '__init__.py':
        return content, []
    
    if ext not in {'.py', '.dart'}:
        return content, []
    
    lines = content.split('\n')
    skeleton_lines = []
    imports = []
    
    for line in lines:
        stripped = line.lstrip()
        
        # 🔗 Capture imports for the LLM's dependency map
        if stripped.startswith(('import ', 'from ')):
            imports.append(stripped)
            continue
        
        # ✅ Keep structural signatures
        signals = ['class ', 'def ', 'async def ', '@dataclass', '@property', 'void ', 'Future', 'Widget ']
        if any(stripped.startswith(kw) for kw in signals):
            skeleton_lines.append(line)
            continue
        
        # 📝 Keep Docstrings (Essential for LLM context!)
        if stripped.startswith(('#', '//')) or '"""' in line or "'''" in line:
            skeleton_lines.append(line)
            continue
        
        if not stripped:
            skeleton_lines.append(line)
            
    return '\n'.join(skeleton_lines), imports

def export_snapshot(project_path, output_file, mode):
    project_path = Path(project_path)
    files_data = []
    stats = {'total_files': 0, 'by_language': {}}
    
    def walk_directory(dir_path, relative_to):
        # Sort so the LLM sees files in a logical order
        for item in sorted(dir_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
            if item.is_dir():
                if not should_ignore_dir(item.name):
                    walk_directory(item, relative_to)
            elif item.is_file():
                # 🛡️ SECURITY: Stop .env processing
                if item.name in IGNORED_FILES:
                    continue 
                
                ext = item.suffix.lower()
                if ext not in ALLOWED_EXTENSIONS:
                    continue
                
                rel_path = item.relative_to(relative_to)
                try:
                    content = item.read_text(encoding='utf-8')
                    file_imports = []
                    
                    # If Blueprint mode, strip logic but save imports
                    if mode in [MODE_SKELETON, MODE_BLUEPRINT]:
                        content, file_imports = skeletonize(content, ext, item.name)
                    
                    entry = {
                        'path': rel_path.as_posix(), # Forward slashes for LLM compatibility
                        'bundle': find_bundle(item.name),
                        'language': ext[1:],
                        'content': content
                    }
                    
                    if file_imports:
                        entry['imports'] = file_imports

                    files_data.append(entry)
                    stats['total_files'] += 1
                except Exception as e:
                    print(f"⚠️ Error reading {rel_path}: {e}")

    walk_directory(project_path, project_path)
    
    output = {
        'metadata': {'project_name': project_path.name, 'mode': mode},
        'files': files_data,
        'stats': stats
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)