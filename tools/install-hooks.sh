#!/usr/bin/env bash
#
# Install Git hooks for lulu-skills-common repository
#
# Usage:
#   bash tools/install-hooks.sh

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Get repository root
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo ".")"
cd "${REPO_ROOT}"

# Paths
HOOKS_DIR="${REPO_ROOT}/.git/hooks"
PRE_COMMIT_SOURCE="${REPO_ROOT}/tools/pre-commit-hook"
PRE_COMMIT_TARGET="${HOOKS_DIR}/pre-commit"

# Check if we're in a git repository
if [[ ! -d "${REPO_ROOT}/.git" ]]; then
  echo -e "${RED}❌ Error: Not in a git repository${NC}"
  echo "Please run this script from within the lulu-skills-common repository"
  exit 1
fi

# Check for global core.hooksPath that might override local hooks
GLOBAL_HOOKS_PATH=$(git config --get core.hooksPath || true)
if [[ -n "${GLOBAL_HOOKS_PATH}" ]]; then
  echo -e "${YELLOW}⚠️  Warning: Global core.hooksPath is set to: ${GLOBAL_HOOKS_PATH}${NC}"
  echo "This will override local repository hooks."
  echo ""
  echo "Options:"
  echo "  1. Unset global hooksPath: git config --global --unset core.hooksPath"
  echo "  2. Copy hook to global location: cp tools/pre-commit-hook ${GLOBAL_HOOKS_PATH}/"
  echo "  3. Continue anyway (hook won't run)"
  echo ""
  read -p "Continue anyway? (y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

# Check if source hook exists
if [[ ! -f "${PRE_COMMIT_SOURCE}" ]]; then
  echo -e "${RED}❌ Error: pre-commit hook not found at ${PRE_COMMIT_SOURCE}${NC}"
  exit 1
fi

echo -e "${BLUE}Installing Git hooks...${NC}"
echo ""

# Backup existing hook if present
if [[ -f "${PRE_COMMIT_TARGET}" ]] && [[ ! -L "${PRE_COMMIT_TARGET}" ]]; then
  BACKUP="${PRE_COMMIT_TARGET}.backup.$(date +%Y%m%d-%H%M%S)"
  echo -e "${YELLOW}⚠️  Existing pre-commit hook found${NC}"
  echo "Backing up to: ${BACKUP}"
  mv "${PRE_COMMIT_TARGET}" "${BACKUP}"
  echo ""
fi

# Remove existing symlink if present
if [[ -L "${PRE_COMMIT_TARGET}" ]]; then
  echo "Removing existing symlink..."
  rm "${PRE_COMMIT_TARGET}"
fi

# Create symlink
echo "Creating symlink: .git/hooks/pre-commit -> ../../tools/pre-commit-hook"
ln -sf "../../tools/pre-commit-hook" "${PRE_COMMIT_TARGET}"

# Ensure source is executable
chmod +x "${PRE_COMMIT_SOURCE}"

echo ""
echo -e "${GREEN}✅ Git hooks installed successfully${NC}"
echo ""
echo "The pre-commit hook will now:"
echo "  • Validate SKILL.md files before each commit"
echo "  • Only check files you're committing (fast!)"
echo "  • Provide clear error messages if validation fails"
echo ""
echo -e "${YELLOW}Note:${NC} You can bypass the hook with: ${BLUE}git commit --no-verify${NC}"
echo ""

# Test the hook
echo "Testing hook installation..."
if bash "${PRE_COMMIT_TARGET}" <<< "" 2>/dev/null; then
  echo -e "${GREEN}✅ Hook is working correctly${NC}"
else
  echo -e "${YELLOW}⚠️  Hook test returned non-zero (this may be expected)${NC}"
fi

echo ""
echo "Installation complete!"
