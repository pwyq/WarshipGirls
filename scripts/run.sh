#!/bin/bash
# File              : run.sh
# Author            : Yanqing Wu <meet.yanqing.wu@gmail.com>
# Date              : 21.11.2019
# Last Modified Date: 05.01.2020
# Last Modified By  : Yanqing Wu <meet.yanqing.wu@gmail.com>

# `$ sudo crontab -e` to auto schedule
cd /home/pwyq/github/WarshipGirls/scripts

file=auto.log
file2=kiss.log
#minimum_size=10000
#actual_size=$(wc -c <"$file")

#while [ $actualsize -le $minimumsize ]; do
    #echo "running scripts..." | tee -a $file
echo "running scripts..." >> $file

date > $file2
python3 auto_favorability.py >> $file2

    #python3 kitchen_popularity.py | tee -a $file
date > $file
python3 kitchen_popularity.py >> $file
    #python3 kitchen_popularity.py

    #python3 kitchen_popularity_new.py | tee -a $file
python3 kitchen_popularity_new.py >> $file
    #python3 kitchen_popularity_new.py


#    actual_size=$(wc -c <"$file")
#done

notify-send "WGR auto scripting is done!"
