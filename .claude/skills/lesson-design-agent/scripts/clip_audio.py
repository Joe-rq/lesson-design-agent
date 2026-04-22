#!/usr/bin/env python3
"""按时间戳剪辑音频/视频.

功能：从媒体文件中提取指定时间范围的片段，输出为音频文件.
职责边界：只做时间范围裁剪，不做格式转换以外的处理.

依赖：ffmpeg（系统需已安装）

用法:
    python clip_audio.py --input "xxx.mp4" --start 00:02:33 --end 00:02:55 --output "clip.mp3"
    python clip_audio.py --input "audio.mp3" --start 120 --end 145 --output "segment.mp3"
"""

import argparse
import subprocess
import sys
from pathlib import Path


def time_to_seconds(time_str: str) -> int:
    """将时间字符串转换为秒数，支持 HH:MM:SS 或纯秒数."""
    if ":" in time_str:
        parts = time_str.split(":")
        if len(parts) == 2:
            m, s = map(int, parts)
            return m * 60 + s
        elif len(parts) == 3:
            h, m, s = map(int, parts)
            return h * 3600 + m * 60 + s
    return int(time_str)


def clip_media(input_path: Path, start: int, end: int, output_path: Path) -> bool:
    """使用 ffmpeg 裁剪媒体片段."""
    duration = end - start
    if duration <= 0:
        print(f"❌ 结束时间({end}s)必须大于开始时间({start}s)")
        return False

    cmd = [
        "ffmpeg",
        "-y",  # 覆盖输出文件
        "-i", str(input_path),
        "-ss", str(start),
        "-t", str(duration),
        "-vn",  # 不输出视频
        "-ar", "44100",  # 音频采样率
        "-ac", "2",  # 双声道
        "-b:a", "192k",  # 音频比特率
        str(output_path),
    ]

    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except subprocess.CalledProcessError as exc:
        print(f"❌ ffmpeg 执行失败:\n{exc.stderr}")
        return False
    except FileNotFoundError:
        print("❌ 未找到 ffmpeg，请先安装 ffmpeg 并添加到系统 PATH")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="剪辑音频片段")
    parser.add_argument("--input", "-i", required=True, help="输入媒体文件路径")
    parser.add_argument("--start", "-s", required=True, help="开始时间 (HH:MM:SS 或秒数)")
    parser.add_argument("--end", "-e", required=True, help="结束时间 (HH:MM:SS 或秒数)")
    parser.add_argument("--output", "-o", required=True, help="输出音频文件路径")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"❌ 输入文件不存在: {args.input}")
        sys.exit(1)

    start_sec = time_to_seconds(args.start)
    end_sec = time_to_seconds(args.end)

    print(f"\n【音频剪辑】")
    print(f"输入: {input_path}")
    print(f"输出: {output_path}")
    print(f"时间: {start_sec}s ~ {end_sec}s (时长: {end_sec - start_sec}s)")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if clip_media(input_path, start_sec, end_sec, output_path):
        print("✅ 剪辑完成")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
