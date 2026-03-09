# .test-skill - Validation Test Suite

## Purpose

This is a **test skill** designed to validate the functionality of the `quick_validate.py` tool. It intentionally contains various types of errors and edge cases that the validation tool should detect.

## ⚠️ Important Notes

1. **DO NOT use this skill in production** - it contains intentional errors
2. **DO NOT sync this skill to agents** - it will fail validation
3. **This skill is excluded from Git** - see `.gitignore`

## Usage

### Running Validation

Test the validation tool against this skill:

```bash
# Should report multiple errors and warnings
tools/quick_validate.py skills/.test-skill

# Or using skillctl
tools/skillctl validate --skill .test-skill
```

### Expected Output

The validation should detect approximately **14+ errors/warnings**:

#### YAML Frontmatter (Baseline Valid)
The main SKILL.md has valid YAML. To test YAML errors, create additional test files:
- `test-missing-name.md` - Missing required `name` field
- `test-missing-description.md` - Missing required `description` field
- `test-invalid-url.md` - Invalid `homepage` URL format
- `test-invalid-json.md` - Invalid `metadata` JSON

#### Markdown Structure Errors
- ❌ **Line ~45**: Unclosed code block (missing closing ```)
- ⚠️ **Line ~52**: Heading level jump (h1 → h3, skipped h2)
- ⚠️ **Line ~58**: Odd number of backticks (unclosed inline code)

#### Code Block Content Errors
- ❌ **Line ~68**: Invalid JSON syntax (missing commas, unquoted keys)
- ⚠️ **Line ~75**: Bash unclosed quotes
- ⚠️ **Line ~81**: Curl command missing URL parameter
- ⚠️ **Line ~87**: Invalid bash syntax (missing `then`)

#### Link Validation Errors
- ⚠️ **Line ~100**: Broken internal link (file doesn't exist)
- ❌ **Line ~104**: Invalid URL format (spaces in URL)
- ❌ **Line ~108**: Malformed markdown link (missing closing paren)

#### Complex/Mixed Errors
- Multiple unclosed code blocks
- Combined JSON + fence errors
- Edge cases (empty blocks, no language spec)

## Test Categories

### 1. Baseline Valid Examples
Section 1 contains properly formatted examples as control cases.

### 2. YAML Validation
Instructions for creating separate test files with YAML errors.

### 3. Structure Validation
Tests markdown structure issues like:
- Unclosed code fences
- Heading hierarchy violations
- Backtick matching

### 4. Content Validation
Tests code block content issues:
- JSON parsing errors
- Bash syntax problems
- Command parameter validation

### 5. Link Validation
Tests link integrity:
- Broken internal references
- Invalid URL formats
- Malformed link syntax

### 6. Real-World Scenarios
Common mistakes developers make:
- Forgetting to close code fences
- Pasting incomplete code
- Copy-paste formatting errors

## Maintenance

When updating `quick_validate.py` to detect new error types:

1. Add corresponding error examples to `SKILL.md`
2. Document the expected behavior in this README
3. Update the error count summary
4. Run validation to verify detection

## Testing Workflow

```bash
# 1. Run validation (should fail with multiple errors)
tools/quick_validate.py skills/.test-skill

# 2. Review the output - should match expected errors listed above

# 3. Use as test data for unit tests
# See: tests/test_quick_validate.py

# 4. Create additional test files for YAML validation
cd skills/.test-skill
# Create test-missing-name.md, test-invalid-url.md, etc.
```

## Integration with Unit Tests

This skill serves as **real-world test data** for the pytest test suite:

- `tests/test_quick_validate.py` can reference these files
- Validates the tool against actual markdown content
- Provides comprehensive error coverage
- Reduces need for synthetic test fixtures

## See Also

- [quick_validate.py](../../tools/quick_validate.py) - The validation tool
- [governance.md](../skills-manager/references/governance.md) - Validation requirements
- [tests/](../../tests/) - Unit test suite (P2 Phase 2)
