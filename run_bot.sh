#!/bin/bash

while :
do 
	echo "Start bot:$(date --iso-8601=minutes)" | tee -a bot.log
	python3 twitter_bot.py 2>&1 | tee -a bot.log
	RES=$?

	echo "Crashed bot:${RES}" | tee -a bot.log
	python3 twitter_bot.py --oneshot "Sorry crushed bot(${RES}). Please wait restart(10min)." 2>&1 \
			| tee -a bot.log

	sleep 10s

done


