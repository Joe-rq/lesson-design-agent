#!/usr/bin/env python3
"""Markdown 教案结构验证 - Skill 辅助脚本.

功能：验证教案 Markdown 文件的结构完整性.
职责边界：只做结构检查，不做内容质量判断.

用法:
    python validate_md.py --file "path/to/教案.md"
"""

import argparse
import re
import sys
import io

# Windows 终端 UTF-8 兼容
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
from pathlib import Path


# 教案必备结构（与 SKILL.md 中的标准结构一致）
REQUIRED_SECTIONS = [
    ("基本信息", r"##?\s*基本信息"),
    ("教学主线", r"##?\s*教学主线"),
    ("教学目标", r"##?\s*教学目标"),
    ("教学过程", r"##?\s*教学过程"),
    ("课后作业", r"##?\s*课后作业"),
    ("板书设计", r"##?\s*板书设计"),
    ("教学资源", r"##?\s*教学资源"),
]

# 每环节必备三要素
REQUIRED_ELEMENTS = [
    ("教师活动", r"教师活动"),
    ("学生活动", r"学生活动"),
    ("设计意图", r"设计意图"),
]


def validate_structure(content: str) -> tuple[list[str], list[str]]:
    """验证教案结构."""
    errors: list[str] = []
    warnings: list[str] = []

    # 检查必备章节
    for name, pattern in REQUIRED_SECTIONS:
        if not re.search(pattern, content, re.IGNORECASE):
            errors.append(f"缺少必备章节: {name}")

    # 检查三要素
    # 找到所有教学过程子环节
    process_match = re.search(r"##?\s*教学过程(.*)$", content, re.DOTALL | re.IGNORECASE)
    if process_match:
        process_content = process_match.group(1)
        # 统计环节数量（精确匹配 ### 而非 ####）
        sections = re.findall(r"^###\s+(?!#).+?$", process_content, re.MULTILINE)
        if len(sections) > 5:
            errors.append(f"教学环节数量 {len(sections)} 超过上限 5，建议进行结构重组（合并为 3-4 个大环节，内含子活动）")

        # 检查子活动数量（#### 层级视为子活动）
        for section in sections:
            section_name = section.strip("# \n")
            section_start = content.find(section)
            if section_start == -1:
                continue
            next_match = re.search(r"^###\s+(?!#)", content[section_start + 1:], re.MULTILINE)
            if next_match:
                next_section = section_start + 1 + next_match.start()
            else:
                next_section = len(content)
            section_content = content[section_start:next_section]
            sub_activities = re.findall(r"####\s+.+?\n", section_content)
            if len(sub_activities) > 4:
                errors.append(f"环节 '{section_name}' 的子活动数量 {len(sub_activities)} 超过上限 4")

        # 检查每个环节的三要素
        for section in sections:
            section_name = section.strip("# \n")
            for elem_name, elem_pattern in REQUIRED_ELEMENTS:
                section_start = content.find(section)
                if section_start == -1:
                    continue
                next_match = re.search(r"###\s+(?!#)", content[section_start + 1:])
                if next_match:
                    next_section = section_start + 1 + next_match.start()
                else:
                    next_section = len(content)
                section_content = content[section_start:next_section]
                if not re.search(elem_pattern, section_content):
                    errors.append(f"环节 '{section_name}' 缺少: {elem_name}")

    # 提取课时时长
    lesson_duration = 45  # 默认 45 分钟
    duration_match = re.search(r"课时[：:]*\s*(\d+)\s*分钟", content)
    if duration_match:
        lesson_duration = int(duration_match.group(1))
    else:
        # 尝试从基本信息中提取
        duration_match2 = re.search(r"(\d+)\s*分钟", content[:500])
        if duration_match2:
            lesson_duration = int(duration_match2.group(1))

    # 检查时间分配
    time_mentions = re.findall(r"(\d+)\s*分钟", content)
    total_time = sum(int(t) for t in time_mentions)
    time_threshold = int(lesson_duration * 1.1)
    if total_time > time_threshold:
        warnings.append(f"时间总和 {total_time} 分钟，可能超过 {lesson_duration} 分钟课时（阈值 {time_threshold} 分钟）")

    # 检查素材引用与资源清单一致性
    resource_match = re.search(r"##?\s*教学资源.*?(?=##|\Z)", content, re.DOTALL | re.IGNORECASE)
    if resource_match:
        resource_content = resource_match.group(0)
        # 统计教案中提到的素材（音频/视频/图片）
        media_refs = re.findall(r"[音频视频图片]\s*[：:]\s*(.+?)(?:\n|$)", content)
        media_in_list = re.findall(r"[音频视频图片]\s*[：:]\s*(.+?)(?:\n|$)", resource_content)
        for media in media_refs:
            media_name = media.strip()
            if media_name and not any(media_name in m for m in media_in_list):
                warnings.append(f"素材 '{media_name}' 可能在资源清单中未列出")

    # 检查专业关联
    if not re.search(r"专业关联|专业结合|专业融入|专业实践", content):
        warnings.append("未检测到专业关联关键词，建议检查专业结合是否充分")

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Markdown 教案结构验证")
    parser.add_argument("--file", "-f", required=True, help="教案文件路径")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"❌ 文件不存在: {args.file}")
        sys.exit(1)

    content = path.read_text(encoding="utf-8")

    print(f"\n【{path.name}】结构验证")
    print(f"文件大小: {len(content)} 字符")
    print(f"总行数: {content.count(chr(10))}")

    errors, warnings = validate_structure(content)

    if warnings:
        print(f"\n⚠️ 警告 ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print(f"\n❌ 错误 ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("\n✅ 结构验证通过")
    sys.exit(0)


if __name__ == "__main__":
    main()
