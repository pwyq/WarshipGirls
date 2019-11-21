#!/bin/bash
# File              : run.sh
# Author            : Yanqing Wu <meet.yanqing.wu@gmail.com>
# Date              : 21.11.2019
# Last Modified Date: 22.11.2019
# Last Modified By  : Yanqing Wu <meet.yanqing.wu@gmail.com>

# `$ sudo crontab -e` to auto schedule
cd /home/pwyq/github/WarshipGirls/scripts
python3 kitchen_popularity.py >> nov.log
python3 kitchen_popularity_new.py >> nov.log
