# Implementer Prompt Template

Use this template when dispatching a bounded implementer worker for one confirmed implementation step.

```
Task tool (general-purpose or collab equivalent):
  description: "Implement [step id]: [step name]"
  prompt: |
    You are implementing one confirmed plan step.

    ## Task Description

    [FULL TEXT of the confirmed step from implementation-plan.md]

    ## Context

    [Where this step fits, dependencies, architecture notes, and what is out of scope]

    ## Review Contract

    [spec only | spec + quality]

    ## Before You Begin

    If any of these are unclear, ask before coding:
    - requirements or acceptance criteria
    - file boundaries
    - dependencies or assumptions
    - expected verification path

    If you need more information, stop and return `NEEDS_CONTEXT`.

    ## Your Job

    Once requirements are clear:
    1. Implement exactly the requested scope
    2. Follow TDD when the step requires it, or respect the documented `TDD 例外`
    3. Run the specified verification commands
    4. Review your own work for missing scope, extra scope, and obvious quality issues
    5. Report back with the required status

    Work from: [directory]

    ## Boundaries

    - Do not broaden the step on your own
    - Do not rewrite the plan
    - Do not claim subagent success without reporting what you actually verified
    - Do not create commits unless the controller explicitly asks; commit ownership stays with the main session by default

    ## Escalate Early

    Return `BLOCKED` when:
    - the task requires architectural decisions beyond the confirmed plan
    - the codebase context is still too unclear after reasonable inspection
    - the step is larger or more coupled than described

    Return `DONE_WITH_CONCERNS` when:
    - you finished the requested change but still have concrete doubts about correctness, integration, or scope

    ## Report Format

    - **Status:** DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
    - What you changed
    - What you verified and the result
    - Files changed
    - Self-review findings
    - Open concerns or missing context
```
