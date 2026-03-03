#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
VENV_PY="${SKILL_DIR}/.venv/bin/python"
VIEWER="${SCRIPT_DIR}/md_file_viewer.py"

if [[ -x "${VENV_PY}" ]]; then
  exec "${VENV_PY}" "${VIEWER}" "$@"
fi

if command -v python3 >/dev/null 2>&1; then
  exec python3 "${VIEWER}" "$@"
fi

printf 'Python not found. Install Python 3 or create a venv at %s\n' "${SKILL_DIR}/.venv" >&2
exit 1
