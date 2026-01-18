---
name: skill-registrar
description: Automatically register new skills in the my-skills project. Detects new skill directories in .claude/skills/, extracts metadata from SKILL.md, updates marketplace.json with complete plugin configuration, and performs git operations (add, commit, push). Triggered by keywords: "注册技能", "添加技能", "注册新技能", "skill register", "register skill". Use when user adds a new skill to the project and wants to register it in marketplace.json and push to GitHub.
---

# Skill Registrar

Automatically register new skills in the my-skills project with Git integration.

## When to Use

Activate this skill when:
- User says "注册技能 [skill-name]" or "register skill [skill-name]"
- User says "添加技能 [skill-name1] [skill-name2]" (multiple skills)
- Any new skill needs to be added to marketplace.json and pushed to GitHub

## Workflow

### 1. Parse User Request

Extract skill names from user input. Examples:
- "注册技能 my-new-skill" → `["my-new-skill"]`
- "register skill skill-a skill-b" → `["skill-a", "skill-b"]`
- "注册新技能" (no names) → Ask user to specify

### 2. Validate Skills Exist

For each skill name:
1. Check if `.claude/skills/{skill-name}/` directory exists
2. Check if `.claude/skills/{skill-name}/SKILL.md` file exists

If any validation fails:
- Show error: "❌ 技能 '{skill-name}' 不存在或缺少 SKILL.md 文件"
- "请检查输入的技能名称是否正确"
- "可用的技能目录: [list available directories from .claude/skills/]"
- **STOP** and ask for corrected names

### 3. Extract Metadata from SKILL.md

For each valid skill, read the SKILL.md YAML frontmatter:

**Required fields:**
- `name`: Skill name
- `description`: Skill description

**Optional fields:**
- Extract any other metadata if present (e.g., custom fields)

**If SKILL.md is missing or invalid:**
- Show error and stop (see step 2)

### 4. Generate Complete Plugin Configuration

For each skill, generate a plugin entry following this schema:

```json
{
  "name": "{skill-name}",
  "source": "./.claude/skills/{skill-name}",
  "description": "{description from SKILL.md}",
  "version": "1.0.0",
  "author": {
    "name": "{owner.name from marketplace.json root}"
  },
  "keywords": [
    "{extract 5-8 relevant keywords from description}"
  ],
  "category": "{infer from description: productivity|design|development|utilities}",
  "strict": false
}
```

**Keyword extraction guidelines:**
- Extract 5-8 meaningful keywords from description
- Prefer technical terms, action verbs, domain-specific terms
- Examples: "idea", "recording", "tracking", "notes", "brainstorming"

**Category inference:**
- `productivity`: Notes, tracking, organization, workflow
- `design`: UI, UX, styling, graphics
- `development`: Code, testing, debugging, APIs
- `utilities`: Helpers, tools, utilities

### 5. Update marketplace.json

1. Read `.claude-plugin/marketplace.json`
2. For each skill:
   - **If skill name already exists in plugins array**: Replace the existing entry
   - **If skill name doesn't exist**: Append to plugins array
3. Maintain JSON formatting (2-space indentation)
4. Write back to `.claude-plugin/marketplace.json`

### 6. Perform Git Operations

Execute in sequence:

```bash
# Stage changes
git add .claude-plugin/marketplace.json

# Commit with conventional format
git commit -m "feat: add new skill {skill-names}"

# Push to remote
git push
```

**Commit message format:**
- Single skill: `feat: add new skill my-skill`
- Multiple skills: `feat: add new skills skill-a, skill-b`

### 7. Report Success

Show success message:

```
✅ 技能注册成功！

已注册技能:
- {skill-name-1}
- {skill-name-2}

✅ marketplace.json 已更新
✅ Git 提交已完成
✅ 已推送到 GitHub
```

## Error Handling

### Skill Directory Not Found
```
❌ 错误: 找不到技能目录 '.claude/skills/{skill-name}/'

可用的技能目录:
- idea-recorder
- skill-creator
- skill-registrar

请检查技能名称是否正确。
```

### SKILL.md Not Found
```
❌ 错误: 技能 '{skill-name}' 缺少 SKILL.md 文件

请确保技能目录包含 SKILL.md 文件，且格式正确。
```

### SKILL.md Invalid Format
```
❌ 错误: 无法解析 SKILL.md 文件

请检查 SKILL.md 的 YAML frontmatter 格式：
---
name: skill-name
description: Skill description
---
```

### Git Push Fails
```
⚠️  警告: marketplace.json 已更新并提交，但推送到 GitHub 失败

请检查网络连接或 Git 配置，然后手动执行：
git push
```

## Examples

### Example 1: Register Single Skill

**User:** "注册技能 my-new-skill"

**Action:**
1. Validate `.claude/skills/my-new-skill/` exists
2. Read SKILL.md, extract name and description
3. Generate plugin configuration
4. Update marketplace.json
5. Git add → commit → push

**Output:**
```
✅ 技能注册成功！

已注册技能:
- my-new-skill

✅ marketplace.json 已更新
✅ Git 提交已完成: feat: add new skill my-new-skill
✅ 已推送到 GitHub
```

### Example 2: Register Multiple Skills

**User:** "添加技能 skill-a skill-b"

**Action:**
1. Validate both skills exist
2. Process both skills in order
3. Add both to marketplace.json
4. Git add → commit → push

**Output:**
```
✅ 技能注册成功！

已注册技能:
- skill-a
- skill-b

✅ marketplace.json 已更新
✅ Git 提交已完成: feat: add new skills skill-a, skill-b
✅ 已推送到 GitHub
```

### Example 3: Skill Not Found

**User:** "注册技能 non-existent"

**Output:**
```
❌ 错误: 找不到技能目录 '.claude/skills/non-existent/'

可用的技能目录:
- idea-recorder
- skill-creator
- skill-registrar

请检查技能名称是否正确。
```

## Notes

- **Overwrite behavior**: If a skill already exists in marketplace.json, it will be replaced with new metadata
- **Multiple skills**: Process in the order provided, fail-fast if any skill is invalid
- **Git integration**: Automatically uses project's owner name from marketplace.json root
- **Keyword extraction**: Use simple keyword extraction based on description content
- **Category inference**: Use simple rules based on description keywords
