---
name: test-missing-description
homepage: https://example.com/test
---

# Test - Missing Description Field

This SKILL.md intentionally omits the `description` field in YAML frontmatter.

The validation tool should report:
- ❌ ERROR: Missing required field 'description'

## Content

```bash
echo "This is valid content, but YAML is invalid"
```
