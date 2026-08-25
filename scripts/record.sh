#!/bin/bash
# 录制示教数据（v2 补录：夹取动作"贴住再夹，夹住停 1 秒"，位置挪 3~5 个点）
# 注意：task 口令必须在录制提示时一字不差输入（与训练/部署一致）
set -e

cd ~/lerobot
unset HF_ENDPOINT
export HTTPS_PROXY=http://127.0.0.1:7897 HTTP_PROXY=http://127.0.0.1:7897
export HF_HUB_DISABLE_XET=1
export PYTHONPATH=""

TASK="Pick up the tissue roll wrapped with orange-yellow tape on the wooden table and place it on the blue-purple area"

lerobot-record \
  --dataset.repo_id=oye-Li-bc/oye_tissue_v2 \
  --dataset.root=/home/lbc/.cache/huggingface/lerobot/oye-Li-bc/oye_tissue_v2_20260825_143500 \
  --dataset.fps=25 \
  --dataset.num_episodes=15 \
  --dataset.episode_time_s=15 \
  --dataset.reset_time_s=5 \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM0 \
  --robot.id=oye_follower_arm \
  --teleop.type=so100_leader \
  --teleop.port=/dev/ttyACM1 \
  --teleop.id=oye_leader_arm \
  --robot.cameras="{front: {type: opencv, index_or_path: 2, width: 1920, height: 1080, fps: 30, fourcc: MJPG}}"

echo "任务口令（训练/部署用）: $TASK"
