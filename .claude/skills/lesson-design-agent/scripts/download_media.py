#!/usr/bin/env python3
"""批量下载视频/音频素材.

功能：根据素材清单批量下载媒体文件到指定目录.
职责边界：只做下载和基础验证，不做格式转换.

用法:
    python download_media.py --list "path/to/素材清单.md" --output "assets/media/"
    python download_media.py --urls "url1,url2,url3" --output "assets/media/"
"""

import argparse
import sys
import re
from pathlib import Path
from urllib.parse import urlparse


def parse_media_list(file_path: Path) -> list[dict[str, str]]:
    """从素材清单 markdown 中解析 URL 列表."""
    items: list[dict[str, str]] = []
    content = file_path.read_text(encoding="utf-8")

    # 匹配 markdown 表格中的 URL 行
    for line in content.splitlines():
        if "http" not in line:
            continue
        urls = re.findall(r"https?://[^\s|)\]]+", line)
        if urls:
            name_match = re.search(r"\|\s*([^|]+?)\s*\|.*http", line)
            name = name_match.group(1).strip() if name_match else "未命名"
            for url in urls:
                items.append({"name": name, "url": url})

    return items


def download_with_yt_dlp(url: str, output_dir: Path) -> bool:
    """使用 yt-dlp 下载."""
    try:
        import yt_dlp  # type: ignore[import-untyped]

        opts = {
            "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        return True
    except Exception as exc:
        print(f"  yt-dlp 失败: {exc}")
        return False


def download_with_you_get(url: str, output_dir: Path) -> bool:
    """使用 you-get 作为备选."""
    import subprocess

    try:
        subprocess.run(
            ["you-get", "-o", str(output_dir), url],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except Exception as exc:
        print(f"  you-get 失败: {exc}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="批量下载媒体素材")
    parser.add_argument("--list", "-l", help="素材清单 markdown 文件路径")
    parser.add_argument("--urls", "-u", help="逗号分隔的 URL 列表")
    parser.add_argument("--output", "-o", default="assets/media", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    items: list[dict[str, str]] = []
    if args.list:
        list_path = Path(args.list)
        if not list_path.exists():
            print(f"❌ 清单文件不存在: {args.list}")
            sys.exit(1)
        items = parse_media_list(list_path)
    elif args.urls:
        for url in args.urls.split(","):
            url = url.strip()
            if url:
                items.append({"name": urlparse(url).netloc or "未命名", "url": url})
    else:
        print("❌ 请提供 --list 或 --urls 参数")
        sys.exit(1)

    print(f"\n【批量下载】共 {len(items)} 个素材")
    print(f"输出目录: {output_dir.resolve()}")

    success = 0
    for item in items:
        print(f"\n⬇️  {item['name']}")
        print(f"   URL: {item['url']}")

        if download_with_yt_dlp(item["url"], output_dir):
            success += 1
            print("   ✅ yt-dlp 下载成功")
        elif download_with_you_get(item["url"], output_dir):
            success += 1
            print("   ✅ you-get 下载成功")
        else:
            print("   ❌ 所有下载方式均失败，请手动下载")

    print(f"\n【结果】成功 {success}/{len(items)} 个")
    if success < len(items):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
