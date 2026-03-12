# Spec Reviewer Prompt Template

Use this template when dispatching the first review pass after an implementer returns.

```
Task tool (general-purpose or collab equivalent):
  description: "Review spec compliance for [step id]"
  prompt: |
    You are reviewing whether an implementation matches a confirmed plan step.

    ## What Was Requested

    [FULL TEXT of the confirmed step]

    ## What Changed

    [Changed files, diff summary, and any verification evidence]

    ## Do Not Trust Summaries

    The implementer report is only a lead. Verify by reading actual code or diffs.

    ## Your Job

    Check for:
    - missing requirements
    - extra scope that was not requested
    - requirement misunderstandings
    - mismatches between claimed verification and actual changes

    ## Output Format

    - `PASS` if the implementation matches the confirmed step
    - `ISSUES` if not, with concrete items and file:line references when possible

    Do not start code quality review here. Spec compliance review is the first gate.
```
