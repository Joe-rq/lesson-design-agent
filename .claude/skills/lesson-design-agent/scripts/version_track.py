#!/usr/bin/env python3
"""版本迭代记录 - Skill 辅助脚本.

功能：记录每次迭代的修改要求和修改内容.
职责边界：只做记录和格式检查，不做内容判断.

用法:
    python version_track.py --from v10 --to v11 --requirements "要求1,要求2" --changes "修改1,修改2"
"""

import argparse
import json
import sys
import io

# Windows 终端 UTF-8 兼容
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("version-log.json")


def load_log() -> list[dict]:
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text(encoding="utf-8"))
    return []


def save_log(log: list[dict]) -> None:
    LOG_FILE.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="版本迭代记录")
    parser.add_argument("--from", "-f", dest="from_ver", required=True, help="起始版本")
    parser.add_argument("--to", "-t", dest="to_ver", required=True, help="目标版本")
    parser.add_argument("--requirements", "-r", required=True, help="修改要求（逗号分隔）")
    parser.add_argument("--changes", "-c", required=True, help="修改内容（逗号分隔）")
    parser.add_argument("--status", "-s", default="completed", help="状态: completed/pending")
    args = parser.parse_args()

    log = load_log()

    entry = {
        "time": datetime.now().isoformat(),
        "from": args.from_ver,
        "to": args.to_ver,
        "requirements": [r.strip() for r in args.requirements.split(",") if r.strip()],
        "changes": [c.strip() for c in args.changes.split(",") if c.strip()],
        "status": args.status,
    }

    log.append(entry)
    save_log(log)

    print(f"\n版本迭代记录: {args.from_ver} → {args.to_ver}")
    print(f"修改要求 ({len(entry['requirements'])}):")
    for r in entry["requirements"]:
        print(f"  - {r}")
    print(f"修改内容 ({len(entry['changes'])}):")
    for c in entry["changes"]:
        print(f"  - {c}")
    print(f"状态: {args.status}")
    print(f"\n✅ 已记录到 {LOG_FILE}")

    # 检查修改要求数量是否超限
    if len(entry["requirements"]) > 6:
        print(f"\n⚠️ 警告: 修改要求 {len(entry['requirements'])} 项超过上限 6")
        print("建议: 分批次迭代")
        sys.exit(1)


if __name__ == "__main__":
    main()
