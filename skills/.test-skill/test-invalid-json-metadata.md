---
name: test-invalid-json
description: Test skill with invalid JSON in metadata field
homepage: https://example.com/test
metadata: {invalid json syntax, missing quotes}
---

# Test - Invalid Metadata JSON

This SKILL.md has invalid JSON in the `metadata` field.

The validation tool should report:
- ⚠️ WARN: Invalid JSON in metadata field

## Content

```bash
echo "This is valid content, but YAML metadata is invalid"
```
