# Prompt Policy Skill — I/O Contract

Version: 1.0.0

---

## Overview

This document defines the machine-readable input/output contract for the `prompt-policy` skill.

The contract is designed to be compatible with an agent loop where a **Task Router** or **Central Manager** produces a structured prompt object, passes it through `prompt-policy` for constraint governance, and then hands the result to an **Execution Agent**.

All field names use `snake_case`. All payloads are JSON-compatible.

---

## Input Contract

```json
{
  "task_type": "code_development | code_review | research | service_management | deployment | document_generation | general",
  "task_body": "The original task description, objective, and execution intent. Treated as immutable.",
  "existing_constraints": [
    "Optional array of constraint strings already present in the prompt.",
    "May be empty if no constraints were detected."
  ],
  "router_instructions": "Optional free-text instructions from the Task Router, such as routing context, agent assignment, or execution hints. These are also treated as immutable.",
  "risk_level": "low | medium | high",
  "router_confidence": 0.0
}
```

### Field Specifications

| Field | Type | Required | Description |
|---|---|---|---|
| `task_type` | `string` (enum) | Yes | Determines which task-specific constraints to load from the static JSON. Use `general` when no specific type matches. |
| `task_body` | `string` | Yes | The core task intent. This field is **frozen** — the skill must never alter it. |
| `existing_constraints` | `string[]` | No | Constraint strings extracted from the original prompt. May be empty. The skill will deduplicate and normalize these against the static policy. |
| `router_instructions` | `string` | No | Router-level directives. Frozen — do not rewrite. |
| `risk_level` | `string` (enum) | Yes | Influences bypass decision and constraint injection aggressiveness. `low` favors bypass. `high` favors full injection. |
| `router_confidence` | `float` [0.0, 1.0] | No | Router's confidence in its task classification. Below a threshold (default 0.5), the skill may bypass task-specific constraints to avoid injecting irrelevant rules. Default: `1.0` if not provided. |

### Risk Level Semantics

| Level | Behavior |
|---|---|
| `low` | Prefer bypass. Only inject if critical constraints are clearly missing. |
| `medium` | Apply standard governance. Deduplicate and append missing task-specific rules. |
| `high` | Apply full governance. All missing global and task-specific constraints are appended. |

---

## Output Contract

```json
{
  "should_apply": true,
  "preserved_task_body": "Exact copy of input.task_body, unchanged.",
  "preserved_router_instructions": "Exact copy of input.router_instructions, unchanged. Null if not provided.",
  "normalized_constraints": [
    {
      "id": "global.no_fabrication",
      "priority": 1,
      "text": "Do not fabricate facts, results, observations, or completion status.",
      "source": "global"
    },
    {
      "id": "code_development.risky_change_transparency",
      "priority": 2,
      "text": "Call out assumptions, risky changes, and possible side effects when modifying code or configuration.",
      "source": "task_specific"
    }
  ],
  "final_prompt": "The reassembled prompt string with preserved task body and merged constraint block.",
  "bypass_reason": "Null when should_apply is true. Contains a short reason string when should_apply is false."
}
```

### Field Specifications

| Field | Type | Always Present | Description |
|---|---|---|---|
| `should_apply` | `boolean` | Yes | `true` if the skill made changes or confirmed constraints are adequate. `false` if the skill decided to bypass. |
| `preserved_task_body` | `string` | Yes | Exact copy of `input.task_body`. Must be bitwise identical. If it differs, the skill violated its core contract. |
| `preserved_router_instructions` | `string \| null` | Yes | Exact copy of `input.router_instructions`. Null if the input did not provide it. |
| `normalized_constraints` | `object[]` | When `should_apply` is `true` | The final constraint set after deduplication and merge. Each entry includes `id`, `priority`, `text`, and `source`. |
| `final_prompt` | `string` | When `should_apply` is `true` | The reassembled prompt ready for the Execution Agent. Structured as `[Task]` + `[Constraints]` sections. |
| `bypass_reason` | `string \| null` | Yes | Non-null when `should_apply` is `false`. Explains why governance was skipped. Null otherwise. |

### Constraint Object Structure

```json
{
  "id": "string — matches the id field in global_constraints.json or task_constraints.json",
  "priority": 1,
  "text": "string — the normalized constraint text",
  "source": "global | task_specific | existing_merged"
}
```

| Source Value | Meaning |
|---|---|
| `global` | Loaded from `global_constraints.json` |
| `task_specific` | Loaded from `task_constraints.json` for the matched `task_type` |
| `existing_merged` | Originated from the caller's `existing_constraints` array, normalized and kept |

---

## Bypass Logic

The skill sets `should_apply: false` when **any** of these conditions are met:

| Condition | Rule |
|---|---|
| Low risk + clean prompt | `risk_level == "low"` AND `existing_constraints` is empty or already sufficient AND no critical global constraint is missing |
| Router confidence too low | `router_confidence < 0.5` — cannot safely select task-specific policy |
| Task type unresolvable | `task_type` is not in the supported enum and no `general` fallback applies |
| Prompt already complete | All applicable global and task-specific constraints are already present in `existing_constraints` with semantic equivalence |

When bypassed, the output is:

```json
{
  "should_apply": false,
  "preserved_task_body": "<unchanged>",
  "preserved_router_instructions": "<unchanged or null>",
  "normalized_constraints": [],
  "final_prompt": "<not included or equal to task_body>",
  "bypass_reason": "low_risk_clean_prompt | router_confidence_below_threshold | task_type_unresolvable | constraints_already_complete"
}
```

---

## Merge Algorithm Summary

```
1. Freeze task_body and router_instructions
2. Load global constraints from global_constraints.json
3. Load task-specific constraints from task_constraints.json for task_type
4. Collect existing_constraints from input
5. Deduplicate:
   - Exact string match → keep one
   - Semantic equivalence → keep the version from static policy (stricter canonical form)
6. Conflict resolution:
   - Two rules with same scope but different strictness → keep stricter
   - Two rules that genuinely conflict → keep higher priority from static policy
7. Append missing:
   - Add global constraints not already covered
   - Add task-specific constraints not already covered (if risk_level permits)
8. Sort by priority (1 → 2 → 3)
9. Reassemble final_prompt:
   - [Task] section = task_body
   - [Constraints] section = priority-ordered constraint texts
   - [Router Instructions] section = router_instructions (if provided)
```

---

## Final Prompt Template

When `should_apply` is `true`, the `final_prompt` field uses this structure:

```
[Task]
{preserved_task_body}

[Constraints]
Priority 1 — Critical
- {constraint text}
- {constraint text}

Priority 2 — Task-Specific
- {constraint text}

Priority 3 — Output / Style
- {constraint text} (if any)

[Router Instructions]
{preserved_router_instructions} (if provided)
```

When `should_apply` is `false`, the caller should use `preserved_task_body` directly (optionally appending `router_instructions` if present).

---

## Version Compatibility

This contract is versioned alongside the static JSON rule files.

- `policy_meta.json` defines the canonical `version` field
- Breaking changes to this I/O contract require a major version bump
- New constraint entries in JSON files are backward-compatible and require only a minor bump

---

## Integration Notes

For the upstream caller (Task Router or Central Manager):

1. Construct the input object with `task_type`, `task_body`, and `risk_level` at minimum
2. Pass `existing_constraints` if the original prompt contains constraint-like sections
3. Pass `router_confidence` if the router produces a confidence score
4. Consume the output: if `should_apply` is `true`, use `final_prompt`; if `false`, use `preserved_task_body`
5. Do not post-process `final_prompt` in a way that rewrites the task body — that would defeat the governance guarantee

For downstream consumers (Execution Agent):

- Treat the `[Task]` section as the authoritative task definition
- Treat the `[Constraints]` section as operational guardrails
- Treat the `[Router Instructions]` section as routing context, not task intent
