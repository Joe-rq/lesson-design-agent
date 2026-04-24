# 教案设计智能 Agent

基于四层元架构的 7 阶段工作流，用于主题班会课/思政课教案设计。

## 核心能力

```
需求澄清 → 学情调研 → 教案初稿 → 迭代优化 → 配套资源 → 试讲打磨 → 定稿输出
```

## 适用场景

- 45 分钟主题班会课
- 需要声音/视频素材的沉浸式教学设计
- 中职/高职专业融合课程
- 思政课教案设计与迭代优化

## 快速开始

本项目的核心是一个 [Claude Code Skill](https://docs.anthropic.com/en/docs/claude-code/skills)，在项目目录下使用 Claude Code 即可自动加载。

触发关键词：教案设计、主题班会、教学方案、PPT设计、学情分析、课前问卷、教案迭代、试讲打磨

## 项目结构

```
.claude/skills/lesson-design-agent/
├── SKILL.md                 # Skill 入口：工作流、约束、防护机制
├── references/              # 参考文档
│   ├── workflow-guide.md    # 7 阶段工作流详细指南
│   ├── checkpoint-guide.md  # 元反思检查点指南
│   ├── 学情分析解读指南.md  # 学情数据→教学调整映射
│   ├── templates/           # 教案模板、问卷模板
│   ├── patterns/            # 导入环节模板、创新教学形式库
│   └── anti-patterns/       # 常见问题清单（6类典型问题）
├── scripts/                 # Python 辅助脚本
│   ├── entity_check.py      # 实体约束自动拆分
│   ├── stage_timeout.py     # 阶段超时监控
│   ├── validate_md.py       # Markdown 结构验证
│   ├── version_track.py     # 版本迭代记录
│   ├── download_media.py    # 批量下载媒体素材
│   ├── clip_audio.py        # 按时间戳剪辑音频
│   └── media_inventory.py   # 扫描素材目录生成清单
└── memory/                  # 积累飞轮（运行时积累经验）
    ├── patterns/
    ├── templates/
    └── anti-patterns/
```

## 四层元架构

| 层级 | 名称 | 职责 |
|------|------|------|
| Layer 4 | 持续优化层 | 倍速测试 + 同类扫描 + 积累飞轮 |
| Layer 3 | 执行可靠层 | 看门狗脚本 + 完整性 + 对齐验证 |
| Layer 2 | 意图防护层 | 兜底策略 + 三重防护 + 自我校验 |
| Layer 1 | 认知边界层 | 元反思检查点(6问) + 实体约束 + 问题重构 |

## 实体约束

| 阶段 | 实体类型 | 上限 |
|------|---------|------|
| 需求澄清 | 核心问题 | 4 个 |
| 学情调研 | 问卷问题 | 15 题（5板块） |
| 教案初稿 | 教学环节 | 5 个 |
| 教案初稿 | 子活动 | 每环节 ≤ 4 个 |
| 迭代优化 | 修改要求 | 6 项 |
| 配套资源 | 素材文件 | 20 个 |

## 辅助脚本使用

```bash
# 实体约束检查
python .claude/skills/lesson-design-agent/scripts/entity_check.py --items "环节1,环节2" --stage "教案初稿"

# 教案结构验证
python .claude/skills/lesson-design-agent/scripts/validate_md.py --file "教案.md"

# 版本迭代记录
python .claude/skills/lesson-design-agent/scripts/version_track.py --from v1 --to v2 --requirements "要求1,要求2" --changes "修改1,修改2"

# 阶段超时检查
python .claude/skills/lesson-design-agent/scripts/stage_timeout.py --stage "教案初稿" --elapsed 180
```

## 技术要求

- Python >= 3.10
- 媒体下载（可选）：`yt-dlp`
- 音频剪辑（可选）：`ffmpeg`
