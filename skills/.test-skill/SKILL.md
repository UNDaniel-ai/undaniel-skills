---
name: test-skill
description: Comprehensive test skill for validating quick_validate.py tool
homepage: https://example.com/test-skill
metadata: {"version": "1.0.0", "author": "test"}
---

# Test Skill - Error Examples Collection

This skill contains intentional errors to validate the quick_validate.py tool.

## Section 1: Valid Examples (Baseline)

### Valid Code Block - JSON

```json
{
  "key": "value",
  "number": 123,
  "array": [1, 2, 3]
}
```

### Valid Code Block - Bash

```bash
#!/bin/bash
echo "Hello World"
ls -la
```

### Valid Links

- [Internal Link](../AIWay/SKILL.md)
- [External Link](https://github.com)

---

## Section 2: YAML Frontmatter Errors

**Note**: The YAML above is valid. To test YAML errors, create separate files:
- Missing `name` field
- Missing `description` field
- Invalid `homepage` URL format
- Invalid `metadata` JSON syntax

---

## Section 3: Markdown Structure Errors

### Error 3.1: Unclosed Code Block

This should trigger an error - code block not closed:

```bash
echo "This code block is not closed
ls -la
# Missing closing ```

### Error 3.2: Heading Level Jump

# H1 Heading

### H3 Heading (Skipped H2)

This should trigger a warning about heading level jump.

### Error 3.3: Odd Backticks

This line has an `odd number of backticks which should trigger a warning.

And another one here: `unclosed inline code

---

## Section 4: Code Block Content Errors

### Error 4.1: Invalid JSON

```json
{
  "key": "value"
  "missing": "comma",
  invalid_key: "no quotes"
}
```

### Error 4.2: Bash Unclosed Quotes

```bash
echo "Unclosed double quote
echo 'Unclosed single quote
```

### Error 4.3: Curl Missing URL

```bash
curl -X POST
# Missing URL parameter
```

### Error 4.4: Invalid Bash Syntax

```bash
if [ -f file.txt ]
# Missing 'then' keyword
  echo "exists"
fi
```

---

## Section 5: Link Validation Errors

### Error 5.1: Broken Internal Link

[This link points to non-existent file](../NonExistent/SKILL.md)

### Error 5.2: Invalid URL Format

[Link with spaces in URL](https://example .com/broken url)

### Error 5.3: Malformed Markdown Link

[Missing closing paren](https://example.com

---

## Section 6: Mixed Errors

This section combines multiple error types:

### Complex Error Example

```json
{
  "unclosed": {
    "nested": "object"
  // Missing closing braces
```

The code block above has:
- Invalid JSON syntax (unclosed object)
- Unclosed code block (no closing ```)

And this paragraph has `unclosed inline code that should warn.

### Another Heading Jump Issue

# Main Title

#### H4 Without H2 or H3

---

## Section 7: Edge Cases

### Empty Code Blocks

```bash
```

```json
```

### Code Block with No Language

```
This is a code block without language specification
```

### Multiple Consecutive Backticks

```bash
echo "test"
```
```json
{"key": "value"}
```
```python
print("hello")
```

---

## Section 8: Real-World Scenarios

### Scenario 1: Documentation Typo

```bash
# User forgot to close the code fence
cd /path/to/project
npm install
npm start

### Scenario 2: Copy-Paste Error

```json
{
  "config": {
    "api_key": "xxx"
}
# User pasted incomplete JSON
```

---

## Summary

This test skill contains approximately **14+ intentional errors**:

**YAML Errors** (separate files needed):
1. Missing `name` field
2. Missing `description` field
3. Invalid `homepage` URL
4. Invalid `metadata` JSON

**Markdown Structure Errors**:
5. Unclosed code block (Line ~45)
6. Heading level jump h1→h3 (Line ~52)
7. Odd number of backticks (Line ~58)

**Code Block Content Errors**:
8. Invalid JSON syntax (Line ~68)
9. Bash unclosed quotes (Line ~75)
10. Curl missing URL (Line ~81)
11. Invalid bash syntax (Line ~87)

**Link Errors**:
12. Broken internal link (Line ~100)
13. URL with spaces (Line ~104)
14. Malformed link syntax (Line ~108)

**Edge Cases**:
15. Multiple unclosed code blocks
16. Mixed error combinations

Use this skill to verify quick_validate.py detects all these issues correctly.
