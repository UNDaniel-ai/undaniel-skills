---
description: Test skill missing the required 'name' field
homepage: https://example.com/test
---

# Test - Missing Name Field

This SKILL.md intentionally omits the `name` field in YAML frontmatter.

The validation tool should report:
- ❌ ERROR: Missing required field 'name'

## Content

```bash
echo "This is valid content, but YAML is invalid"
```
