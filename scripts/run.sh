#!/bin/bash
# File              : run.sh
# Author            : Yanqing Wu <meet.yanqing.wu@gmail.com>
# Date              : 21.11.2019
# Last Modified Date: 27.11.2019
# Last Modified By  : Yanqing Wu <meet.yanqing.wu@gmail.com>

# `$ sudo crontab -e` to auto schedule
cd /home/pwyq/github/WarshipGirls/scripts

file=auto.log
date > $file
minimum_size=10000
actual_size=$(wc -c <"$file")

while [ $actualsize -le $minimumsize ]; do
    #echo "running scripts..." | tee -a $file
    echo "running scripts..." > $file
    #python3 kitchen_popularity.py | tee -a $file
    python3 kitchen_popularity.py >> $file
    #python3 kitchen_popularity_new.py | tee -a $file
    python3 kitchen_popularity_new.py >> $file
done

notify-send "WGR auto scripting is done!"
