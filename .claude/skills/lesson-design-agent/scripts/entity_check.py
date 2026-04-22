#!/usr/bin/env python3
"""实体约束检查 - Skill 辅助脚本.

功能：自动检查实体数量，超限时自动拆分并给出建议.
职责边界：只做数量检查和拆分，不做内容判断.

用法:
    python entity_check.py --items "环节1,环节2,环节3,环节4,环节5,环节6" --stage "教案初稿"
"""

import argparse
import sys

# 实体约束配置（与 SKILL.md 保持一致）
CONSTRAINTS = {
    "需求澄清": {"max": 4, "type": "核心问题"},
    "学情调研": {"max": 15, "type": "问卷问题"},
    "教案初稿": {"max": 5, "type": "教学环节"},
    "子活动": {"max": 4, "type": "每环节子活动"},
    "迭代优化": {"max": 6, "type": "修改要求"},
    "配套资源": {"max": 20, "type": "素材文件"},
}


def main() -> None:
    parser = argparse.ArgumentParser(description="实体约束检查")
    parser.add_argument("--items", "-i", required=True, help="逗号分隔的实体列表")
    parser.add_argument("--stage", "-s", default="教案初稿", help="阶段名称")
    args = parser.parse_args()

    items = [s.strip() for s in args.items.split(",") if s.strip()]
    constraint = CONSTRAINTS.get(args.stage)

    if not constraint:
        print(f"⚠️ 未知阶段 '{args.stage}'，使用默认约束 max=4")
        constraint = {"max": 4, "type": "实体"}

    print(f"\n【{args.stage}】实体约束检查")
    print(f"实体类型: {constraint['type']}")
    print(f"实体数量: {len(items)}")
    print(f"约束上限: {constraint['max']}")

    if len(items) <= constraint["max"]:
        print(f"\n✅ 通过 - 实体数量 {len(items)} ≤ {constraint['max']}")
        sys.exit(0)

    max_size = constraint["max"]
    batches = [items[i : i + max_size] for i in range(0, len(items), max_size)]

    print(f"\n❌ 超限 - 实体数量 {len(items)} > {constraint['max']}")
    print(f"建议拆分为 {len(batches)} 批:\n")

    for idx, batch in enumerate(batches, 1):
        print(f"  批次 {idx}: {', '.join(batch)}")

    sys.exit(1)


if __name__ == "__main__":
    main()
