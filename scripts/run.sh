#!/bin/bash
# File              : run.sh
# Author            : Yanqing Wu <meet.yanqing.wu@gmail.com>
# Date              : 21.11.2019
# Last Modified Date: 24.11.2019
# Last Modified By  : Yanqing Wu <meet.yanqing.wu@gmail.com>

# `$ sudo crontab -e` to auto schedule
cd /home/pwyq/github/WarshipGirls/scripts
date > nov.log
python3 kitchen_popularity.py 2>&1 | tee -a nov.log
python3 kitchen_popularity_new.py 2>&1 | tee -a nov.log
