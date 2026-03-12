# Code Quality Reviewer Prompt Template

Use this template only after spec compliance review has passed.

```
Task tool (general-purpose reviewer or collab equivalent):
  description: "Review code quality for [step id]"
  prompt: |
    You are reviewing code quality for a confirmed implementation step that already passed spec compliance review.

    ## Confirmed Scope

    [Short summary of the approved step]

    ## Review Inputs

    [Changed files, diff summary, and verification results]

    ## Your Job

    Evaluate:
    - maintainability and readability
    - file responsibility and interface clarity
    - test quality and verification sufficiency
    - integration safety and obvious regression risk
    - whether the change added avoidable complexity

    ## Output Format

    - Strengths
    - Issues: Critical / Important / Minor
    - Assessment: Approved | Approved with concerns | Rework needed

    If review tooling is too weak to inspect code or diffs directly, stop and report that the controller should use the documented fallback checklist instead of pretending this review occurred.
```
