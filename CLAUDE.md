# 教案设计智能 Agent

## 项目概述

本项目是一个 Claude Code Skill，提供主题班会课/思政课教案设计的 7 阶段工作流。

## Skill 位置

核心 Skill 文件位于 `.claude/skills/lesson-design-agent/`，包括：

- `SKILL.md` — Skill 主文件，定义工作流、约束、防护机制
- `references/` — 参考文档（工作流指南、模板、模式库、反模式）
- `scripts/` — Python 辅助脚本（实体检查、格式验证、版本追踪等）
- `memory/` — 积累飞轮（运行时积累的设计模式和经验）

## 使用方式

在当前项目中直接使用，Skill 会被自动加载。触发关键词：教案设计、主题班会、教学方案、PPT设计、学情分析、课前问卷、教案迭代、试讲打磨。

## 脚本运行

所有脚本位于 `.claude/skills/lesson-design-agent/scripts/`，运行时需使用该路径：

```bash
python .claude/skills/lesson-design-agent/scripts/entity_check.py --items "环节1,环节2" --stage "教案初稿"
python .claude/skills/lesson-design-agent/scripts/validate_md.py --file "教案.md"
python .claude/skills/lesson-design-agent/scripts/version_track.py --from v1 --to v2 --requirements "要求1" --changes "修改1"
```

## Git 规范

- 所有 commit message 必须使用中文
