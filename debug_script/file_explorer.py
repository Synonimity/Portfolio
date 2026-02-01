# file_explorer.py | Version: 5.1.0
# Interactive filesystem explorer for snapshot debugging
#
# This module is intentionally isolated to keep main.py clean.
# It provides a full navigation loop with unlimited depth.
#
# It was on this day that Syn discovered something unique
# Something that changed his perspective about coding
# And so it came to pass that he leveld up and became
# A master navigator!

from pathlib import Path
from config import ROOT_PATH, MODE_FULL, MODE_SKELETON, MODE_BLUEPRINT
from utils import should_ignore_dir, generate_output_path
from snapshot_export import export_snapshot

# ─────────────────────────────────────────────────
# 📂 DIRECTORY EXPLORER LOOP
# ─────────────────────────────────────────────────

def explore(start_path: str):
    """Interactive directory explorer with export capabilities"""
    current_path = Path(start_path)
    
    while True:
        print(f"\n{'='*60}")
        print(f"📂 Current: {current_path}")
        print(f"{'='*60}")
        
        # Collect directories and files
        try:
            items = sorted(current_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        except PermissionError:
            print("❌ Permission denied!")
            return
        
        dirs = [d for d in items if d.is_dir() and not should_ignore_dir(d.name)]
        files = [f for f in items if f.is_file()]
        
        # Display folders
        print("\n📁 Directories:")
        for idx, d in enumerate(dirs, 1):
            print(f"  [{idx}] {d.name}/")
        
        if not dirs:
            print("  (none)")
        
        # Display files (read-only info)
        print("\n📄 Files:")
        for f in files[:10]:  # Show first 10 files
            print(f"  • {f.name}")
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more")
        
        # Options
        print("\n" + "─"*60)
        print("Options:")
        print("  [f] Export FULL snapshot")
        print("  [s] Export SKELETON/blueprint")
        print("  [b] Go BACK")
        print("  [q] QUIT")
        if dirs:
            print("  [1-9] Enter directory")
        print("─"*60)
        
        choice = input("\n👉 Your choice: ").strip().lower()
        
        # ────────────────────────
        # EXPORT (Full or Skeleton)
        # ────────────────────────
        if choice in ['f', 's']:
            mode = MODE_FULL if choice == 'f' else MODE_SKELETON
            
            # Determine mode and generate the unique filename
            output_file = generate_output_path(
                Path(ROOT_PATH) / 'Debug',
                current_path.name,
                mode
            )
            
            print(f"\n🚀 Exporting {mode.upper()} snapshot...")
            export_snapshot(current_path, output_file, mode)
            print(f"✅ Saved to: {output_file}")
            input("\nPress Enter to continue...")
        
        # ────────────────────────
        # BACK
        # ────────────────────────
        elif choice == 'b':
            # Prevent escaping ROOT_PATH
            if current_path == Path(ROOT_PATH) or not current_path.is_relative_to(ROOT_PATH):
                print("⚠️  Cannot go back further!")
                continue
            current_path = current_path.parent
        
        # ────────────────────────
        # QUIT
        # ────────────────────────
        elif choice == 'q':
            print("\n👋 Goodbye!")
            break
        
        # ────────────────────────
        # ENTER DIRECTORY
        # ────────────────────────
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(dirs):
                current_path = dirs[idx]
            else:
                print("❌ Invalid directory number!")
                input("Press Enter to continue...")
        
        else:
            print("❌ Invalid choice!")
            input("Press Enter to continue...")
