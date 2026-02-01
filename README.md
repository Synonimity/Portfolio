# DebugScript — JSON Snapshots & Blueprints

A modular Python utility for capturing structured project snapshots and blueprints. Designed to help developers and project managers **analyze, archive, and debug complex projects** with a clean, automated workflow.

## Overview

DebugScript is composed of 5 main files:

| File | Purpose |
|------|---------|
| `config.py` | Core configuration: paths, filtering rules, bundle mapping, and snapshot modes. |
| `file_explorer.py` | Simple UI for navigating projects and selecting target directories. |
| `main.py` | Entry point to run the entire script. Orchestrates project discovery, file filtering, and snapshot generation. |
| `snapshot_export.py` | Handles JSON output and bundle resolution according to the rules defined in `config.py`. |
| `utils.py` | Helper functions for directory handling, project listing, and output path generation. |

---

## Features

- **Multi-mode snapshotting**:  
  - `full` — complete project snapshot  
  - `skeleton` / `blueprint` — lightweight blueprint output  

- **Bundle mapping** for structured JSON output.  
- **Project discovery** with automatic filtering of `.git`, `.idea`, `node_modules`, and other irrelevant directories.  
- **Safe file handling**: ignores sensitive files such as `.env` and credentials.  
- **Cross-platform path management** with Python’s `pathlib`.  

---

## Quick Start

1. **Clone the repo**
```bash
git clone https://github.com/Synonimity/Portfolio.git
cd Portfolio/DebugScript
