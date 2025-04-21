#!/bin/zsh
export PYTHONPATH="/home/ecs-user/dev/py/daily_check_in:$PYTHONPATH"
source /home/ecs-user/miniconda3/etc/profile.d/conda.sh
conda activate py310
python /home/ecs-user/dev/py/daily_check_in/android/longhu.py >> /home/ecs-user/dev/py/daily_check_in/logs/longhu.log 2>&1
python /home/ecs-user/dev/py/daily_check_in/android/main_qiandao.py >> /home/ecs-user/dev/py/daily_check_in/logs/qiandao.log 2>&1