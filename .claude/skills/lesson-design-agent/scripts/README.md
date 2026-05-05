# 辅助脚本索引

## 脚本一览

| 脚本 | 功能 | 使用阶段 | 依赖 |
|------|------|---------|------|
| `entity_check.py` | 实体约束自动检查与拆分建议 | 每阶段开始前 | 无 |
| `stage_timeout.py` | 阶段超时监控 | 长阶段定时检查 | 无 |
| `validate_md.py` | Markdown 教案结构验证 | 教案输出后 | 无 |
| `version_track.py` | 版本迭代记录 | 每次迭代后 | 无 |
| `download_media.py` | 批量下载媒体素材 | 配套资源阶段 | yt-dlp 或 you-get |
| `clip_audio.py` | 按时间戳剪辑音频 | 配套资源阶段 | ffmpeg |
| `media_inventory.py` | 扫描素材目录生成清单 | 配套资源阶段 | 无 |

## 快速使用

```bash
# 实体约束检查
python scripts/entity_check.py --items "环节1,环节2,环节3" --stage "教案初稿"

# 结构验证
python scripts/validate_md.py --file "教案.md"

# 版本记录
python scripts/version_track.py --from v1 --to v2 --requirements "要求1" --changes "修改1"

# 超时检查
python scripts/stage_timeout.py --stage "教案初稿" --elapsed 180

# 批量下载
python scripts/download_media.py --list "素材清单.md" --output "assets/media/"

# 音频剪辑
python scripts/clip_audio.py --input "video.mp4" --start 00:02:33 --end 00:02:55 --output "clip.mp3"

# 素材扫描
python scripts/media_inventory.py --dir "assets/media/" --output "assets/素材清单.md"
```

## 注意事项

- 所有脚本均兼容 Windows 终端（UTF-8 编码处理）
- 脚本只做 Skill 做不到的事（文件操作、状态追踪、格式验证）
- 脚本不做内容判断和工作流决策
