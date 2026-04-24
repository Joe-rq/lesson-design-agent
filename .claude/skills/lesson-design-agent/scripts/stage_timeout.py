#!/usr/bin/env python3
"""阶段超时监控 - Skill 辅助脚本.

功能：检查当前阶段是否超时或即将超时.
职责边界：只做时间检查，不做工作流决策.

用法:
    python stage_timeout.py --stage "教案初稿" --elapsed 180
"""

import argparse
import sys
import io

# Windows 终端 UTF-8 兼容
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 阶段建议时长（分钟），与 SKILL.md 保持一致
TIME_LIMITS = {
    "需求澄清": 120,
    "学情调研": 1440,
    "教案初稿": 240,
    "迭代优化": 30,
    "配套资源": 240,
    "试讲打磨": 30,
    "定稿输出": 120,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="阶段超时检查")
    parser.add_argument("--stage", "-s", required=True, help="当前阶段名称")
    parser.add_argument("--elapsed", "-e", type=int, required=True, help="已耗时（分钟）")
    args = parser.parse_args()

    limit = TIME_LIMITS.get(args.stage, 120)
    warning_threshold = int(limit * 0.8)

    print(f"\n【{args.stage}】阶段超时检查")
    print(f"建议时长: {limit} 分钟")
    print(f"已耗时: {args.elapsed} 分钟")
    print(f"预警阈值: {warning_threshold} 分钟")

    if args.elapsed > limit:
        print(f"\n❌ 已超时 - 超出 {args.elapsed - limit} 分钟")
        print("建议:")
        print("  1. 砍掉次要环节")
        print("  2. 压缩讨论时间")
        print("  3. 将部分内容转为课前预习")
        sys.exit(1)
    elif args.elapsed > warning_threshold:
        print(f"\n⚠️ 即将超时 - 剩余 {limit - args.elapsed} 分钟")
        print("建议: 关注进度，准备精简方案")
        sys.exit(0)
    else:
        print(f"\n✅ 时间充裕 - 剩余 {limit - args.elapsed} 分钟")
        sys.exit(0)


if __name__ == "__main__":
    main()
