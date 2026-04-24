#!/usr/bin/env python3
"""扫描素材目录，生成素材清单.

功能：递归扫描素材目录，统计各类素材并生成 markdown 格式的素材清单表.
职责边界：只做扫描和清单生成，不做格式转换.

用法:
    python media_inventory.py --dir "assets/media/" --output "assets/素材清单.md"
"""

import argparse
import mimetypes
import sys
import io

# Windows 终端 UTF-8 兼容
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
from pathlib import Path

# 素材类型分类
MEDIA_TYPES = {
    "视频": [".mp4", ".mov", ".avi", ".mkv", ".webm"],
    "音频": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
    "文档": [".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"],
}


def categorize_file(path: Path) -> str:
    """根据扩展名分类文件."""
    ext = path.suffix.lower()
    for category, exts in MEDIA_TYPES.items():
        if ext in exts:
            return category
    return "其他"


def format_size(size_bytes: int) -> str:
    """格式化文件大小."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def scan_directory(dir_path: Path) -> dict[str, list[dict[str, str]]]:
    """递归扫描目录，按类型归类素材."""
    inventory: dict[str, list[dict[str, str]]] = {cat: [] for cat in MEDIA_TYPES}
    inventory["其他"] = []

    for path in dir_path.rglob("*"):
        if not path.is_file():
            continue

        category = categorize_file(path)
        inventory[category].append({
            "name": path.name,
            "path": str(path.relative_to(dir_path)),
            "size": format_size(path.stat().st_size),
        })

    return inventory


def generate_markdown(inventory: dict[str, list[dict[str, str]]], dir_path: Path) -> str:
    """生成 markdown 格式的素材清单."""
    lines = [
        "# 素材清单",
        "",
        f"> 扫描目录: `{dir_path}`",
        f"> 生成时间: 自动更新",
        "",
    ]

    total = 0
    for category, items in inventory.items():
        if not items:
            continue
        total += len(items)
        lines.append(f"## {category} ({len(items)} 个)")
        lines.append("")
        lines.append("| 序号 | 文件名 | 路径 | 大小 |")
        lines.append("|------|--------|------|------|")
        for idx, item in enumerate(items, 1):
            lines.append(
                f"| {idx} | {item['name']} | `{item['path']}` | {item['size']} |"
            )
        lines.append("")

    lines.insert(3, f"> 总计: {total} 个文件")
    lines.append("---")
    lines.append("")
    lines.append("*本清单由 `scripts/media_inventory.py` 自动生成*")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="扫描素材目录并生成清单")
    parser.add_argument("--dir", "-d", default="assets/media", help="素材目录路径")
    parser.add_argument("--output", "-o", help="输出 markdown 文件路径（默认 stdout）")
    args = parser.parse_args()

    dir_path = Path(args.dir)
    if not dir_path.exists():
        print(f"❌ 目录不存在: {args.dir}")
        sys.exit(1)

    print(f"\n【扫描素材】{dir_path}")
    inventory = scan_directory(dir_path)

    total = sum(len(items) for items in inventory.values())
    for category, items in inventory.items():
        if items:
            print(f"  {category}: {len(items)} 个")

    print(f"  总计: {total} 个")

    markdown = generate_markdown(inventory, dir_path)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
        print(f"\n✅ 清单已保存: {output_path}")
    else:
        print("\n" + markdown)

    sys.exit(0)


if __name__ == "__main__":
    main()
