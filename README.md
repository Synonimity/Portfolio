\# Debug Script — JSON Snapshots \& Blueprints



A Python-based utility for capturing structured JSON snapshots and project blueprints, designed with modularity, filtering rules, and bundle mapping. Ideal for debugging and project introspection.



\## Features

\- Modular bundle mapping for backend, Flutter/Dart, and documentation files.

\- Filtering rules for sensitive files and ignored directories.

\- Snapshot modes: full, skeleton, blueprint.

\- Clear path management using Python's `pathlib`.



\## Example Use

```python

from config import ROOT\_PATH, OUTPUT\_PATH, MODE\_FULL

\# Initialize and run snapshot process



