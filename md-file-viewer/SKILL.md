---
name: md-file-viewer
description: Popup viewer for browsing Markdown (with Mermaid), images, and text files in a GUI window. Use when Codex needs to open a window to browse the current working directory, preview a generated Markdown file (including Mermaid diagrams), inspect images with metadata, or view plain-text files. Includes hidden-files toggle and optional root-folder switching.
---

# Md File Viewer

## Overview
Launch a lightweight PySide6 popup that previews Markdown (with Mermaid), images, and text files, plus a file tree rooted at the current working directory.

## Dependencies
- `PySide6` for the UI (includes QtWebEngine via Addons).
- `markdown` for Markdown-to-HTML rendering (optional; fallback is raw text).

## Quick Start
- Preferred launcher (uses `.venv` if present):
  - `scripts/run_viewer.sh --file <path-to-md>`
- Direct run:
  - `python3 scripts/md_file_viewer.py --file <path-to-md>`
- Browse files only:
  - `scripts/run_viewer.sh` (uses current working directory as root)
- Switch root directory with the **Choose Folder** button.
- Toggle hidden files with the **Show hidden** checkbox.

## Setup (Recommended venv)
```
/usr/bin/python3 -m venv .venv
.venv/bin/python -m pip install PySide6 markdown
```

## Behavior
- Markdown renders with `markdown` if available, and Mermaid diagrams render via the bundled `assets/vendor/mermaid.min.js` when QtWebEngine is available.
- Images show the image on top with file metadata below (path, dimensions, size, modified time).
- Text shows as plain text, up to 2MB.
- Binary files show a "not supported" message.

## CLI
- `--root <path>` sets the root directory for the file tree (default: cwd).
- `--file <path>` opens a file immediately.
- `--show-hidden` shows hidden files by default.

## Resources
- `scripts/md_file_viewer.py`
- `scripts/run_viewer.sh`
- `assets/vendor/mermaid.min.js`
