#!/bin/bash
# SmolVLA 微调（基于 lerobot/smolvla_base 预训练模型，v3 合并数据集 55 集）
# 显存 11.5GB 可用 batch=8；140W 满血下 20000 步约 1.5~2 小时
set -e

cd ~/lerobot
unset HF_ENDPOINT
export HTTPS_PROXY=http://127.0.0.1:7897 HTTP_PROXY=http://127.0.0.1:7897
export HF_HUB_DISABLE_XET=1
export PYTHONPATH=""

lerobot-train \
  --policy.path=lerobot/smolvla_base \
  --dataset.repo_id=oye-Li-bc/oye \
  --dataset.root=/home/lbc/.cache/huggingface/lerobot/oye-Li-bc/oye_tissue_v3_20260825_161500 \
  --rename_map='{"observation.images.front": "observation.images.camera1"}' \
  --policy.empty_cameras=2 \
  --output_dir=/home/lbc/output_lerobot_train/tissue/smolvla_v2 \
  --job_name=tissue_smolvla_v2 \
  --policy.device=cuda \
  --wandb.enable=false \
  --policy.push_to_hub=false \
  --steps=20000 \
  --batch_size=8
