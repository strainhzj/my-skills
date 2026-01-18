# Marketplace.json Schema Reference

This document describes the structure of `.claude-plugin/marketplace.json` for the my-skills project.

## Complete Structure

```json
{
  "name": "my-skills",
  "id": "my-skills",
  "owner": {
    "name": "strainhzj"
  },
  "metadata": {
    "description": "Personal AI Assistant Skill for idea recording and tracking...",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "skill-name",
      "source": "./.claude/skills/skill-name",
      "description": "Full skill description...",
      "version": "1.0.0",
      "author": {
        "name": "strainhzj"
      },
      "keywords": [
        "keyword1",
        "keyword2",
        "keyword3"
      ],
      "category": "productivity",
      "strict": false
    }
  ]
}
```

## Root Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Project name (e.g., "my-skills") |
| `id` | string | Yes | Project identifier (usually same as name) |
| `owner` | object | Yes | Owner information |
| `metadata` | object | Yes | Project metadata |
| `plugins` | array | Yes | List of plugin configurations |

## Owner Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Owner username (e.g., "strainhzj") |

## Metadata Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | string | Yes | Project description |
| `version` | string | Yes | Project version (e.g., "1.0.0") |

## Plugin Object (Array Items)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Skill name (must match directory name) |
| `source` | string | Yes | Relative path to skill directory (format: `./.claude/skills/{skill-name}`) |
| `description` | string | Yes | Skill description (from SKILL.md) |
| `version` | string | Yes | Skill version (default: "1.0.0") |
| `author` | object | Yes | Author information (inherited from root owner) |
| `keywords` | array | Yes | 5-8 relevant keywords |
| `category` | string | Yes | Category: `productivity`, `design`, `development`, or `utilities` |
| `strict` | boolean | Yes | Strict mode flag (default: `false`) |

## Author Object (within Plugin)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Author name (inherited from root owner.name) |

## Category Guidelines

### productivity
Skills for productivity, organization, and workflow management:
- Notes, tracking, recording
- Task management, organization
- Brainstorming, ideation
- Project management

### design
Skills for visual design and user experience:
- UI/UX design guidance
- Styling, theming
- Graphics, icons
- Layout design

### development
Skills for software development:
- Code generation, analysis
- Testing, debugging
- API design, documentation
- Refactoring, code review

### utilities
Skills for utility functions and helper tools:
- File conversion, formatting
- Text processing
- System utilities
- Developer tools

## Keyword Extraction Guidelines

Extract 5-8 meaningful keywords from skill description:

**Good keywords:**
- Technical terms: "api", "ui", "ux", "cli", "git"
- Action verbs: "tracking", "recording", "parsing", "generating"
- Domain-specific: "database", "frontend", "backend", "testing"

**Avoid:**
- Common words: "the", "a", "an", "is", "are"
- Generic terms: "tool", "help", "provide", "user"
- Stop words: "this", "that", "with", "from"

## Examples

### Example 1: Productivity Skill

```json
{
  "name": "idea-recorder",
  "source": "./.claude/skills/idea-recorder",
  "description": "Idea recording and tracking system with intelligent analysis...",
  "version": "1.0.0",
  "author": {
    "name": "strainhzj"
  },
  "keywords": [
    "idea",
    "recording",
    "tracking",
    "notes",
    "brainstorming",
    "project-analysis"
  ],
  "category": "productivity",
  "strict": false
}
```

### Example 2: Development Skill

```json
{
  "name": "code-reviewer",
  "source": "./.claude/skills/code-reviewer",
  "description": "Automated code review with quality analysis...",
  "version": "1.0.0",
  "author": {
    "name": "strainhzj"
  },
  "keywords": [
    "code",
    "review",
    "quality",
    "analysis",
    "debugging",
    "best-practices"
  ],
  "category": "development",
  "strict": false
}
```

## Updating marketplace.json

When adding a new skill:

1. **Parse** SKILL.md to extract `name` and `description`
2. **Extract keywords** from description (5-8 terms)
3. **Infer category** based on description content
4. **Generate plugin config** with all required fields
5. **Update plugins array**:
   - If skill name exists: **replace** the entry
   - If skill name doesn't exist: **append** to array
6. **Maintain formatting**: 2-space indentation, ensure_ascii=false

## Validation Checklist

Before committing marketplace.json:

- ✅ All required fields present
- ✅ `source` path follows format `./.claude/skills/{skill-name}`
- ✅ `author.name` matches root `owner.name`
- ✅ 5-8 keywords provided
- ✅ Category is one of: productivity, design, development, utilities
- ✅ `strict` field is set to `false`
- ✅ JSON is valid (no syntax errors)
- ✅ Formatting is consistent (2-space indentation)
