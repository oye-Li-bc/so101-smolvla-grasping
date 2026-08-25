#!/bin/bash
# SmolVLA 真机部署（rollout）
# 注意: --task 口令必须与训练数据集的 tasks.parquet 一字不差
#       --rename_map 必须与训练时一致
set -e

cd ~/lerobot
unset HF_ENDPOINT
export HTTPS_PROXY=http://127.0.0.1:7897 HTTP_PROXY=http://127.0.0.1:7897
export HF_HUB_DISABLE_XET=1
export PYTHONPATH=""

lerobot-rollout \
  --strategy.type=base \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM0 \
  --robot.id=oye_follower_arm \
  --robot.cameras="{front: {type: opencv, index_or_path: 2, width: 1920, height: 1080, fps: 30, fourcc: MJPG}}" \
  --rename_map='{"observation.images.front": "observation.images.camera1"}' \
  --display_data=true \
  --duration=300 \
  --task="Pick up the tissue roll wrapped with orange-yellow tape on the wooden table and place it on the blue-purple area" \
  --policy.path=/home/lbc/output_lerobot_train/tissue/smolvla_v2/checkpoints/last/pretrained_model
