#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文字幕提取工具
从双语字幕文件中提取中文字幕,支持单文件和批量处理
输出统一到项目根目录的 output 文件夹
"""

import re
import os
import sys
import glob
from typing import List, Set, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SubtitleEvent:
    """字幕事件数据类"""
    layer: int
    start: str
    end: str
    style: str
    name: str
    margin_l: int
    margin_r: int
    margin_v: int
    effect: str
    text: str

    def to_ass_line(self) -> str:
        """转换为ASS格式的Dialogue行"""
        return (f"Dialogue: {self.layer},{self.start},{self.end},"
                f"{self.style},{self.name},{self.margin_l},{self.margin_r},"
                f"{self.margin_v},{self.effect},{self.text}")


class ChineseExtractor:
    """中文字幕提取器"""

    # 中文样式关键词
    CN_KEYWORDS = {'CN', 'CHINESE', 'ZH', 'ZH-CN'}

    def __init__(self, input_file: str, output_dir: str):
        """
        初始化提取器

        Args:
            input_file: 输入的双语字幕文件
            output_dir: 输出目录(项目根目录的output文件夹)
        """
        self.input_file = input_file
        self.output_dir = output_dir

        # 生成输出文件名
        base_name = Path(input_file).stem
        # 移除已有的语言后缀
        for ext in ['.zh-cn', '.jp', '.chi', '.japanese', '_cn', '_jp']:
            base_name = base_name.replace(ext, '')

        self.output_cn = os.path.join(output_dir, f"{base_name}_cn.ass")

        self.header_lines: List[str] = []
        self.all_events: List[SubtitleEvent] = []
        self.cn_styles: Set[str] = set()

        self._parse_file()

    def _parse_file(self):
        """解析字幕文件"""
        try:
            with open(self.input_file, 'r', encoding='utf-8-sig') as f:
                lines = f.readlines()
        except Exception as e:
            raise Exception(f"无法读取文件 {self.input_file}: {e}")

        in_events = False

        for line in lines:
            line_stripped = line.strip()

            # 检测并分类样式
            if line_stripped.startswith('Style:'):
                style_name = self._extract_style_name(line_stripped)
                if style_name and self._is_chinese_style(style_name):
                    self.cn_styles.add(style_name)

            # 保存头部信息
            if not in_events:
                self.header_lines.append(line.rstrip('\n'))
                if line_stripped == '[Events]':
                    in_events = True
                continue

            # 解析字幕事件
            if line_stripped.startswith('Dialogue:'):
                event = self._parse_dialogue(line_stripped)
                if event:
                    self.all_events.append(event)

    def _extract_style_name(self, style_line: str) -> Optional[str]:
        """从样式行中提取样式名称"""
        match = re.match(r'Style:\s*([^,]+)', style_line)
        return match.group(1).strip() if match else None

    def _is_chinese_style(self, style_name: str) -> bool:
        """判断是否为中文字幕样式"""
        style_upper = style_name.upper()
        return any(keyword in style_upper for keyword in self.CN_KEYWORDS)

    def _parse_dialogue(self, line: str) -> Optional[SubtitleEvent]:
        """解析Dialogue行"""
        pattern = r'Dialogue:\s*(\d+),([^,]+),([^,]+),([^,]+),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),(.*)'
        match = re.match(pattern, line)

        if match:
            return SubtitleEvent(
                layer=int(match.group(1)),
                start=match.group(2),
                end=match.group(3),
                style=match.group(4),
                name=match.group(5),
                margin_l=int(match.group(6)) if match.group(6) else 0,
                margin_r=int(match.group(7)) if match.group(7) else 0,
                margin_v=int(match.group(8)) if match.group(8) else 0,
                effect=match.group(9),
                text=match.group(10)
            )
        return None

    def extract(self) -> dict:
        """执行提取操作,返回统计信息"""
        # 提取中文字幕
        cn_events = [e for e in self.all_events if e.style in self.cn_styles]

        # 写入文件
        self._write_subtitle(self.output_cn, cn_events)

        return {
            'total': len(self.all_events),
            'cn': len(cn_events)
        }

    def _write_subtitle(self, output_file: str, events: List[SubtitleEvent]):
        """写入字幕文件"""
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)

        # 过滤头部中的样式定义,只保留中文样式
        filtered_header = self._filter_chinese_header()

        with open(output_file, 'w', encoding='utf-8-sig') as f:
            # 写入头部
            for line in filtered_header:
                f.write(line + '\n')

            # 写入字幕事件
            for event in events:
                f.write(event.to_ass_line() + '\n')

    def _filter_chinese_header(self) -> List[str]:
        """过滤头部,只保留中文样式定义"""
        filtered = []

        for line in self.header_lines:
            # 保留所有非样式定义行
            if not line.startswith('Style:'):
                filtered.append(line)
                continue

            # 只保留中文样式
            style_name = self._extract_style_name(line)
            if style_name and style_name in self.cn_styles:
                filtered.append(line)

        return filtered


def extract_from_file(input_file: str, output_dir: str) -> dict:
    """
    从单个文件提取中文字幕

    Args:
        input_file: 输入字幕文件路径
        output_dir: 输出目录

    Returns:
        统计信息字典
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"文件不存在: {input_file}")

    extractor = ChineseExtractor(input_file, output_dir)
    stats = extractor.extract()

    print(f"[OK] 已处理: {os.path.basename(input_file)}")
    print(f"     总计: {stats['total']} 条字幕")
    print(f"     中文: {stats['cn']} 条")
    print(f"     输出: {os.path.basename(extractor.output_cn)}")

    return stats


def extract_from_directory(input_dir: str, output_dir: str, pattern: str = "*.ass") -> dict:
    """
    从目录批量提取中文字幕

    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        pattern: 文件匹配模式

    Returns:
        统计信息字典
    """
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"目录不存在: {input_dir}")

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 查找所有字幕文件
    search_pattern = os.path.join(input_dir, pattern)
    subtitle_files = glob.glob(search_pattern)

    if not subtitle_files:
        print(f"[INFO] 未找到匹配的字幕文件: {search_pattern}")
        return {'total_files': 0, 'success': 0, 'failed': 0}

    total_files = len(subtitle_files)
    success_count = 0
    failed_count = 0
    failed_files = []

    print(f"\n找到 {total_files} 个字幕文件\n")
    print("=" * 60)

    # 处理每个文件
    for i, subtitle_file in enumerate(subtitle_files, 1):
        filename = os.path.basename(subtitle_file)
        print(f"[{i}/{total_files}] {filename}")

        try:
            extract_from_file(subtitle_file, output_dir)
            print()
            success_count += 1
        except Exception as e:
            print(f"  [ERROR] 处理失败: {e}\n")
            failed_count += 1
            failed_files.append(filename)

    # 显示统计结果
    print("=" * 60)
    print(f"处理完成: 成功 {success_count}/{total_files}")
    if failed_files:
        print(f"失败的文件:")
        for filename in failed_files:
            print(f"  - {filename}")
    print(f"输出目录: {output_dir}")
    print("=" * 60)

    return {
        'total_files': total_files,
        'success': success_count,
        'failed': failed_count,
        'failed_files': failed_files
    }


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("=" * 60)
        print("  中文字幕提取工具")
        print("=" * 60)
        print("\n用法:")
        print("  单文件模式: python chinese_extractor.py <字幕文件>")
        print("  批量模式:   python chinese_extractor.py <目录> [选项]")
        print("\n参数:")
        print("  <字幕文件/目录>  必填,字幕文件路径或包含字幕的目录")
        print("\n选项:")
        print("  --output=<目录>   指定输出目录(默认: ./output)")
        print("  --pattern=<模式>  文件匹配模式(默认: *.ass)")
        print("\n示例:")
        print("  python chinese_extractor.py video.ass")
        print("  python chinese_extractor.py ./subtitles")
        print("  python chinese_extractor.py ./videos --output=./extracted --pattern=\"*.zh-cn.ass\"")
        print("\n说明:")
        print("  - 自动检测输入是文件还是目录")
        print("  - 只提取中文字幕,忽略外文字幕")
        print("  - 输出文件名添加 _cn 后缀")
        print("  - 输出统一到指定目录(默认: ./output)")
        print("=" * 60)
        return

    input_path = sys.argv[1]
    output_dir = "./output"
    pattern = "*.ass"

    # 解析可选参数
    for arg in sys.argv[2:]:
        if arg.startswith('--output='):
            output_dir = arg.split('=', 1)[1]
        elif arg.startswith('--pattern='):
            pattern = arg.split('=', 1)[1]

    # 判断是文件还是目录
    if os.path.isfile(input_path):
        # 单文件模式
        print("=" * 60)
        print("  中文字幕提取工具 - 单文件模式")
        print("=" * 60)
        try:
            extract_from_file(input_path, output_dir)
            print(f"\n输出文件: {os.path.abspath(output_dir)}")
        except Exception as e:
            print(f"\n[ERROR] {e}")
            import traceback
            traceback.print_exc()

    elif os.path.isdir(input_path):
        # 批量模式
        extract_from_directory(input_path, output_dir, pattern)

    else:
        print(f"[ERROR] 路径不存在: {input_path}")


if __name__ == '__main__':
    main()
