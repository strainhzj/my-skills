# My Skills - 个人 AI Assistant Skill 仓库

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/skills-1-purple?style=for-the-badge" alt="Skills Count">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/platform-Claude%20Code-informational?style=for-the-badge" alt="Platform">
</p>

个人 AI Assistant Skill，专注于想法记录和追踪，基于项目认知提供智能分析。

## 📖 简介

本仓库提供 `idea-recorder` skill，帮助开发者在日常工作中记录和追踪想法。当你说"记录我的想法"时，skill 会自动创建独立的 Markdown 文件，包含：
- 你的原始想法
- 基于项目认知的智能分析
- 潜在问题和疑问点
- 改进建议

## ✨ 特性

- **💭 智能记录**: 自动将想法保存为结构化的 Markdown 文件
- **🧠 项目认知**: 基于项目的技术栈和架构提供上下文分析
- **🔍 问题识别**: 自动识别潜在的技术难点和风险点
- **💡 改进建议**: 基于最佳实践提供优化建议
- **🏷️ 标签管理**: 自动为想法打标签，便于后续检索
- **📋 索引管理**: 自动维护想法索引，追踪实现状态

## 🎯 适用场景

- **功能构思**: 记录新功能的想法和实现思路
- **问题追踪**: 记录遇到的问题和解决方案
- **优化建议**: 记录性能优化和代码改进的想法
- **技术探索**: 记录新技术尝试和实验性想法
- **架构调整**: 记录架构演进和重构计划

## 📦 Skill 列表

| Skill | 说明 | 触发方式 |
|-------|------|----------|
| **idea-recorder** | 想法记录和追踪，基于项目认知提供智能分析 | "记录我的想法"、"有个想法"、"记录想法" |

## 🚀 快速开始

### 方式 1: 直接复制（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/strainhzj/my-skills.git
cd my-skills

# 2. 复制到你的项目
cp -r .claude /path/to/your/project/

# 3. 在 Claude Code 中使用
# 打开 Claude Code，开始对话，skill 会根据上下文自动激活
```

### 方式 2: 符号链接

```bash
# 创建符号链接到项目目录
ln -s /path/to/my-skills/.claude /path/to/your/project/.claude
```

### 验证安装

在 Claude Code 中测试：

```
记录我的想法: 测试 idea-recorder skill
```

## 📚 使用方式

### 触发 Skill

当你说以下任何一句话时，skill 会自动激活：

- "记录我的想法"
- "有个想法"
- "记录想法"
- "想法记录"
- "保存我的想法"

### 想法记录格式

每个想法会保存为独立的 Markdown 文件，包含以下部分：

```markdown
# 想法标题

## 📝 用户原想法
> [你输入的原话]

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

### 文件命名规则

```
IDEA-YYYYMMDD-HHMMSS-[关键词].md
```

示例：
- `IDEA-20250117-143000-用户认证优化.md`
- `IDEA-20250117-150500-下载器状态同步.md`

## 🏗️ 项目结构

```
my-skills/
├── .claude/                      # Claude Code skills
│   └── skills/
│       └── idea-recorder/        # 想法记录 skill
│           ├── SKILL.md          # Skill 定义
│           └── ideas/            # 想法存储目录
│               ├── IDEA-*.md     # 各个想法文件
│               └── IDEAS_INDEX.md # 想法索引
├── .claude-plugin/               # Claude 插件市场配置
│   └── marketplace.json          # 插件定义
├── .cursor/                      # Cursor 支持
├── .windsurf/                    # Windsurf 支持
├── .agent/                       # Antigravity 支持
├── .github/                      # GitHub 配置
│   ├── ISSUE_TEMPLATE/           # Issue 模板
│   └── PULL_REQUEST_TEMPLATE.md  # PR 模板
├── CLAUDE.md                     # Claude Code 项目说明
├── README.md                     # 本文件
├── LICENSE                       # MIT License
└── .gitignore                    # Git 忽略文件
```

## 🎨 自定义和扩展

### 修改 Skill 配置

1. 找到 skill 目录：`.claude/skills/idea-recorder/`
2. 编辑 `SKILL.md` 文件
3. 修改项目认知部分，适配你的项目

### 添加新的想法分类

在 `SKILL.md` 中扩展分析维度：

```markdown
### 新的分析维度
- 维度1: 说明
- 维度2: 说明
```

## 📝 使用示例

### 示例 1: 功能想法

**用户输入**:
```
记录我的想法: 我希望为用户添加批量重命名功能
```

**Skill 处理**:
1. 识别关键词: 用户、批量重命名
2. 生成文件名: `IDEA-20250117-143000-用户批量重命名.md`
3. 基于项目认知分析:
   - 涉及模块: 用户管理 API、前端用户列表页面
   - 技术难点: 批量操作的事务处理
   - 风险评估: 低风险，UI 交互为主
4. 保存到 ideas 目录
5. 更新想法索引

### 示例 2: 优化想法

**用户输入**:
```
记录我的想法: 下载器的状态同步可以改为 WebSocket 推送
```

**Skill 处理**:
1. 识别关键词: 下载器、状态同步、WebSocket
2. 生成文件名: `IDEA-20250117-150500-WebSocket状态同步.md`
3. 基于项目认知分析:
   - 涉及模块: WebSocket 服务、下载器管理
   - 技术优势: 实时性提升，减少轮询开销
   - 风险评估: 中等风险，需要处理连接断开
4. 保存到 ideas 目录
5. 更新想法索引

## 🔧 技术栈

- **AI Assistant**: Claude Code
- **语言**: Markdown
- **版本管理**: Git
- **适用项目**: 任何需要记录想法的项目

## 🤝 贡献

这是个人 skill 仓库，主要用于个人使用和知识积累。欢迎：
- 🐛 报告问题
- 💡 提出建议
- 📖 分享使用经验
- 🔄 Fork 并自定义

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

## 🔗 相关资源

- [Claude Code 官方文档](https://github.com/anthropics/claude-code)
- [参考项目: ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)

## 📮 联系方式

- GitHub: [@strainhzj](https://github.com/strainhzj)

---

<p align="center">
  <b>如果这个项目对你有帮助，请考虑给个 ⭐️</b>
</p>

<p align="center">
  **维护者**: strainhzj | **创建日期**: 2025-01-17 | **版本**: 1.0.0
</p>
