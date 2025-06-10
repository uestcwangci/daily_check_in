#!/bin/zsh
export PYTHONPATH="/home/ecs-user/dev/py/daily_check_in:$PYTHONPATH"
source /home/ecs-user/miniconda3/etc/profile.d/conda.sh
conda activate py310
python /home/ecs-user/dev/py/daily_check_in/android/dingtalk.py