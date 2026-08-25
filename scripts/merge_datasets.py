"""
合并 oye_tissue 数据集: v1(40集) + v2(15集) → v3(55集), 统一补语言指令。

用法:
    export PYTHONPATH=""
    ~/miniconda3/envs/lerobot/bin/python ~/Projects/AI-Study/scripts/merge_oye_tissue.py

纯本地操作, 不需要网络。预计 10~20 分钟 (逐帧解码 + 重新编码视频)。
"""
import json
from pathlib import Path

from lerobot.datasets import LeRobotDataset

# ========== 配置 ==========

TASK_TEXT = (
    "Pick up the tissue roll wrapped with orange-yellow tape on the "
    "wooden table and place it on the blue-purple area"
)

V1 = Path.home() / ".cache/huggingface/lerobot/oye-Li-bc/oye_tissue_20260815_133841"
V2 = Path.home() / ".cache/huggingface/lerobot/oye-Li-bc/oye_tissue_v2_20260825_143500"
V3 = Path.home() / ".cache/huggingface/lerobot/oye-Li-bc/oye_tissue_v3_20260825_161500"

# ========== 以下不用动 ==========

def get_item_value(item, key):
    """统一处理 tensor/scalar/numpy 取值"""
    v = item[key]
    if hasattr(v, "item") and v.ndim == 0:
        return v.item()
    return v

def main():
    if V3.exists():
        raise FileExistsError(f"目标目录已存在: {V3}\n换一个新的 v3 时间戳目录")

    info = json.load(open(V1 / "meta" / "info.json"))
    features = info["features"]
    fps = info["fps"]

    # 帧里要写入的特征键 (排除 timestamp/frame_index/index/episode_index/task_index)
    frame_keys = [k for k in features if not k.startswith(("timestamp", "frame_index", "index", "episode_index", "task_index"))]
    # 视频特征 (__getitem__ 返回 float32 [0,1] CHW, 写入需转回 uint8 HWC)
    video_keys = {k for k in features if features[k].get("dtype") == "video"}
    print("写入特征:", frame_keys)
    print("视频特征:", video_keys)

    ds3 = LeRobotDataset.create(
        # repo_id 用 HF 上已存在的 repo 占位 (create 会联网查 repo 存在性),
        # 实际数据全在本地 root, 训练时 --dataset.repo_id 也用这个占位即可
        repo_id="oye-Li-bc/oye",
        root=V3,
        fps=fps,
        features=features,
        use_videos=True,
    )

    total_eps = 0
    for label, src_root in [("v1", V1), ("v2", V2)]:
        src = LeRobotDataset(repo_id="oye-Li-bc/oye", root=src_root)
        print(f"[{label}] 共 {src.num_episodes} 集, {src.num_frames} 帧")

        # 注意: __getitem__ 返回的 dict 是 reader 复用的对象,
        # 不能跨调用缓存引用, 必须逐帧立即转换并 add_frame
        cur_ep = None
        n_saved = 0
        n_frames_ep = 0

        for idx in range(src.num_frames):
            item = src[idx]
            ep = get_item_value(item, "episode_index")
            if cur_ep is None:
                cur_ep = ep
            if ep != cur_ep:
                # 上一集结束
                ds3.save_episode()
                n_saved += 1
                print(f"  episode {cur_ep} 完成 ({n_frames_ep} 帧)")
                cur_ep = ep
                n_frames_ep = 0

            frame = {}
            for k in frame_keys:
                v = item[k]
                if k in video_keys:
                    # float32 [0,1] CHW -> uint8 HWC (writer 期望 0-255)
                    v = (v.permute(1, 2, 0) * 255).round().byte().numpy()
                frame[k] = v
            frame["task"] = TASK_TEXT
            ds3.add_frame(frame)
            n_frames_ep += 1

        if n_frames_ep > 0:  # 最后一集
            ds3.save_episode()
            n_saved += 1
            print(f"  episode {cur_ep} 完成 ({n_frames_ep} 帧)")

        total_eps += n_saved
        print(f"[{label}] 保存 {n_saved} 集")

    print()
    print(f"合并完成! v3 共 {total_eps} 集")

    # 关键: 落盘 meta/episodes 元数据, 否则数据集无法被读取
    ds3.finalize()

    print("验证:", ds3.num_episodes, "集,", ds3.num_frames, "帧")

if __name__ == "__main__":
    main()
