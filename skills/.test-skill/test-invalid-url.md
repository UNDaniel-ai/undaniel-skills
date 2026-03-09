---
name: test-invalid-url
description: Test skill with invalid homepage URL format
homepage: not-a-valid-url
---

# Test - Invalid Homepage URL

This SKILL.md has an invalid `homepage` value that is not a proper URL.

The validation tool should report:
- ⚠️ WARN: Invalid homepage URL format

## Content

```bash
echo "This is valid content, but YAML homepage is invalid"
```
