# CLAUDE.md - 个人 Skill 仓库

这是我的个人 AI assistant skill 仓库，专注于想法记录和追踪功能，为 Claude Code 提供智能的想法管理能力。

## 项目概述

本仓库通过 Claude Code 的 skill 机制，提供 `idea-recorder` skill，帮助开发者在日常工作中记录和追踪想法。skill 会基于项目认知自动分析想法，提供技术关联分析、实现难度评估、疑问点和改进建议。

## Skill 列表

当前包含以下 1 个 skill:

### idea-recorder
**用途**: 想法记录和追踪
**触发关键词**: "记录我的想法"、"有个想法"、"记录想法"、"想法记录"、"保存我的想法"
**功能**:
- 自动记录用户想法为独立 Markdown 文件
- 基于项目认知提供智能分析
- 识别技术关联和架构影响
- 评估实现难度和风险等级
- 提供疑问点和改进建议
- 自动维护想法索引和状态追踪

## 目录结构

```
my-skills/
├── .claude/
│   └── skills/
│       └── idea-recorder/           # 想法记录 skill
│           ├── SKILL.md              # Skill 定义和工作流
│           └── ideas/                # 想法记录存储目录
│               ├── IDEA-*.md         # 各个想法文件
│               ├── IDEAS_INDEX.md    # 想法索引
│               └── README.md         # 想法目录说明
├── .claude-plugin/                   # Claude 插件市场配置
│   └── marketplace.json              # 插件定义
├── CLAUDE.md                         # 本文件
├── README.md                         # 项目说明
├── LICENSE                           # MIT License
└── .gitignore                        # Git 忽略文件
```

## 使用方式

### 在 Claude Code 中使用

1. **将仓库添加到 Claude Code 项目**
   ```bash
   # 方式1: 复制到项目目录
   cp -r my-skills/.claude /path/to/your/project/

   # 方式2: 符号链接 (推荐)
   ln -s /path/to/my-skills/.claude /path/to/your/project/.claude
   ```

2. **Skill 自动激活**
   - 当你说"记录我的想法"或类似语句时，skill 会自动激活
   - 查看 SKILL.md 中的 "When to Use This Skill" 部分

3. **验证安装**
   ```
   记录我的想法: 测试 idea-recorder skill
   ```

### Skill 开发和扩展

`idea-recorder` skill 是独立的，可以:
- 修改 SKILL.md 中的项目认知部分，适配具体项目
- 扩展想法分析维度和模板
- 添加新的想法分类和标签

## 想法记录格式

每个想法会保存为结构化的 Markdown 文件：

```markdown
# 想法标题

## 📝 用户原想法
> [用户输入的原话]

## 🧠 项目认知分析

### 技术关联
- 涉及模块: [列出相关的模块]
- 技术栈影响: [分析对技术栈的影响]
- 架构影响: [分析对整体架构的影响]

### 实现难度
- 前端工作量: [评估]
- 后端工作量: [评估]
- 数据库变更: [是否需要]
- 风险等级: [评估]

## ❓ 疑问点
[基于项目理解提出的疑问]

## 💡 改进建议
[基于最佳实践提出的建议]

## 📋 相关文档
[相关的技术文档]

## 🏷️ 标签
#标签1 #标签2 #标签3

---
**记录时间**: YYYY-MM-DD HH:MM:SS
**想法编号**: IDEA-YYYYMMDD-HHMMSS
```

## 维护和更新

### 版本管理
- 当前版本: 1.0.0
- 使用 Git 进行版本控制
- 记录重要变更

### 内容更新
- 定期更新项目认知部分
- 根据实际项目调整分析维度
- 补充实际使用经验
- 优化触发关键词

## 注意事项

1. **项目特定内容**: `idea-recorder` skill 包含项目认知部分，需要根据实际项目调整 `SKILL.md` 中的相关内容

2. **技能触发**: skill 的描述中已定义触发关键词，确保使用时使用这些关键词

3. **内容质量**: 定期审查和更新项目认知，保持分析的准确性

4. **想法管理**: 定期整理想法索引，更新实现状态

## 扩展阅读

- [Claude Code 官方文档](https://github.com/anthropics/claude-code)
- [参考项目: ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)

---

**仓库版本**: 1.0.0
**创建日期**: 2025-01-17
**维护者**: strainhzj
**适用 AI**: Claude Code
