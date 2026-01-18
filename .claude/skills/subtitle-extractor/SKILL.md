---
name: subtitle-extractor
description: 中文字幕提取技能,用于从ASS格式双语字幕文件中提取中文字幕并输出到output文件夹。使用场景: (1) 用户明确要求提取中文字幕,如"提取中文字幕"、"处理字幕文件"、"extract Chinese subtitles" (2) 用户提供字幕文件路径,要求处理该文件 (3) 用户提供目录路径,要求批量处理目录下的字幕文件。支持单个文件和批量目录处理,自动输出到项目根目录的output文件夹。
---

# 中文字幕提取技能

从ASS格式双语字幕文件中提取中文字幕,支持单文件和批量处理。

## 快速开始

### 单文件处理

处理单个字幕文件:

```bash
python chinese_extractor.py <字幕文件>
```

示例:
```bash
python chinese_extractor.py video.ass
python chinese_extractor.py "卡罗尔与星期二 - S01E01 - 第1集.chi.zh-cn.jp.ass"
```

### 批量处理

处理整个目录下的字幕文件:

```bash
python chinese_extractor.py <目录>
```

示例:
```bash
python chinese_extractor.py ./subtitles
python chinese_extractor.py ./videos --pattern="*.zh-cn.ass"
```

## 工作流程

### 1. 确定处理模式

根据用户输入自动判断:
- **文件路径**: 单文件模式
- **目录路径**: 批量模式

### 2. 执行提取

调用 `chinese_extractor.py` 脚本:

```bash
# 单文件模式
python chinese_extractor.py <文件路径> --output="./output"

# 批量模式
python chinese_extractor.py <目录路径> --output="./output" --pattern="*.ass"
```

### 3. 验证输出

检查 `./output` 目录下生成的文件:
- 文件名格式: `<原文件名>_cn.ass`
- 确认只包含中文字幕内容

## 命令行选项

- `--output=<目录>`: 指定输出目录(默认: `./output`)
- `--pattern=<模式>`: 文件匹配模式,仅批量模式有效(默认: `*.ass`)

## 中文样式识别

脚本自动识别以下中文样式关键词:
- `CN`
- `CHINESE`
- `ZH`
- `ZH-CN`

## 输出规则

- 所有提取的中文字幕统一输出到指定目录(默认: `./output`)
- 输出文件名在原文件名基础上添加 `_cn` 后缀
- 自动过滤掉外文字幕样式,只保留中文样式定义
- 自动创建输出目录(如果不存在)

## 错误处理

常见错误及解决方案:

1. **文件不存在**: 检查输入路径是否正确
2. **找不到中文字幕样式**: 确认字幕文件包含中文样式(样式名包含CN/CHINESE/ZH/ZH-CN关键词)
3. **编码错误**: 确保字幕文件使用UTF-8或UTF-8-SIG编码

## 使用示例

### 示例1: 处理单个文件

用户请求: "提取这个文件的中文字幕"

```bash
python chinese_extractor.py "卡罗尔与星期二 - S01E01 - 第1集.chi.zh-cn.jp.ass"
```

输出:
```
[OK] 已处理: 卡罗尔与星期二 - S01E01 - 第1集.chi.zh-cn.jp.ass
     总计: 779 条字幕
     中文: 471 条
     输出: 卡罗尔与星期二 - S01E01 - 第1集_cn.ass
```

### 示例2: 批量处理目录

用户请求: "批量处理这个文件夹下的字幕"

```bash
python chinese_extractor.py ./subtitles
```

输出:
```
找到 3 个字幕文件

[1/3] video1.ass
[OK] 已处理: video1.ass
     总计: 500 条字幕
     中文: 300 条

[2/3] video2.ass
[OK] 已处理: video2.ass
     总计: 600 条字幕
     中文: 350 条

============================================================
处理完成: 成功 3/3
输出目录: ./output
============================================================
```

## 注意事项

- 脚本仅处理ASS格式字幕文件
- 只提取中文字幕,不保留外文字幕
- 确保有足够的磁盘空间存储输出文件
- 大批量处理时注意监控进程状态
