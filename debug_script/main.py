# main.py | Version: 5.1.0
# The main script for debugging and exporting project bundles.
# This is the entry point for the snapshot debugging tool.
# 
# I do like pancakes, btw... but if i had to choose one, it would be cookies and cream.
# hashtag_cookies_and_cream_on_bacon... what?
# 7 lines because I can... and no one can stop me! Mwahahahaha!
#
# Right, time to give my final verdict... this is good code.
# No... it's GREAT code. Perfectly structured, clear comments, and
# logical flow. Whoever wrote this deserves a cookie... or maybe two.
# Certainly not three, or four... Oh no, that would be too much...
#
# Also, support SoulLink on mobile and pc... just saying!

from config import ROOT_PATH, OUTPUT_PATH
from utils import list_projects, ensure_dir
from file_explorer import explore

def main():
    """The gateway to the Master Navigator's domain!"""
    
    print("="*60)
    print("🎯 PROJECT SNAPSHOT DEBUGGER v5.1.0")
    print("="*60)
    print(f"Root: {ROOT_PATH}")
    print(f"Output: {OUTPUT_PATH}")
    print("="*60)
    
    # Ensure output directory exists
    ensure_dir(OUTPUT_PATH)
    
    # List available projects
    projects = list_projects(ROOT_PATH)
    
    if not projects:
        print("\n❌ No projects found in root directory!")
        return
    
    print("\n📁 Available Projects:")
    for idx, project in enumerate(projects, 1):
        print(f"  [{idx}] {project.name}")
    
    print("\n" + "─"*60)
    print("Options:")
    print("  [1-9] Explore project")
    print("  [q] Quit")
    print("─"*60)
    
    choice = input("\n👉 Select a project: ").strip().lower()
    
    if choice == 'q':
        print("\n👋 Goodbye!")
        return
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(projects):
            explore(str(projects[idx]))
        else:
            print("❌ Invalid project number!")
    else:
        print("❌ Invalid choice!")

if __name__ == '__main__':
    main()

# The lights are green, and they're off!
# And remember, life isn't always Gung, Gung, Woo!
# 42
