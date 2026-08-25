"""
修复 oye_tissue 数据集的 tasks.parquet：补上 SmolVLA 必需的语言指令。

用法:
    cd ~/Projects/AI-Study
    export PYTHONPATH=""
    ~/miniconda3/envs/lerobot/bin/python scripts/fix_tasks_parquet.py

注意:
    - 只改本地缓存的数据集文件, 不会动视频/动作数据
    - 如果数据集已上传到 HuggingFace, 改完后需要重新上传,
      否则训练时从远端拉到的还是旧版
    - 这句 task 描述要记牢, 部署时 --task= 必须一字不差
"""
import pandas as pd
from pathlib import Path

# ========== 需要修改的地方 ==========

# 1. 数据集路径 (如果是另一个时间戳目录, 改这里)
DATASET_DIR = Path.home() / ".cache/huggingface/lerobot/oye-Li-bc/oye_tissue_20260815_133841"

# 2. 语言指令 (SmolVLA 训练和部署共用这一句, 定稿后别改)
TASK_TEXT = (
    "Pick up the tissue roll wrapped with orange-yellow tape on the "
    "wooden table and place it on the blue-purple area"
)

# 3. 任务名 (index, 随便起, 不能重复)
TASK_NAME = "move_tissue_to_area"

# ========== 以下不用动 ==========

def main():
    parquet_path = DATASET_DIR / "meta" / "tasks.parquet"
    if not parquet_path.exists():
        raise FileNotFoundError(f"找不到 tasks.parquet: {parquet_path}\n"
                                f"请检查 DATASET_DIR 路径是否正确")

    df = pd.DataFrame(
        {"task": [TASK_TEXT], "task_index": [0]},
        index=[TASK_NAME],
    )
    df.to_parquet(parquet_path, index=True)

    print(f"已写入: {parquet_path}")
    print()
    print("写入内容:")
    print(pd.read_parquet(parquet_path))
    print()
    print("记住这句, 部署时 --task= 要一字不差:")
    print(f"  {TASK_TEXT}")

if __name__ == "__main__":
    main()
