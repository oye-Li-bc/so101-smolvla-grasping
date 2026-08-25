# 数据集说明

数据集为 **LeRobot v3.0 格式**（`~/.cache/huggingface/lerobot/oye-Li-bc/`），完整数据（视频+parquet）托管在 HuggingFace，本仓库不存放二进制。

## 版本演进

| 版本 | 集数 | 帧数 | 目录 | 说明 |
|---|---|---|---|---|
| v1 | 40 | 10,000 | `oye_tissue_20260815_133841` | 初次录制 |
| v2 | 15 | 5,625 | `oye_tissue_v2_20260825_143500` | 补录：贴着夹 + 位置变体 |
| v3 | 55 | 15,625 | `oye_tissue_v3_20260825_161500` | v1+v2 合并（训练用） |

## 特征

- `observation.images.front`：1080×1920 @ 25 FPS（H.264/AV1 视频编码）
- `observation.state`：6 维关节位置（shoulder_pan/lift, elbow_flex, wrist_flex/roll, gripper）
- `action`：6 维关节位置指令
- `task`：语言指令（单任务，task_index=0）

## 语言指令（关键）

```
Pick up the tissue roll wrapped with orange-yellow tape on the wooden table and place it on the blue-purple area
```

录制时 LeRobot **不会自动写入任务描述**，需用 `scripts/fix_tasks_parquet.py` 修复 `meta/tasks.parquet`。
