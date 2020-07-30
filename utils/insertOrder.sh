#!/usr/bin/env bash
i=100
dir='/home/yhl2/workspace/xtp_test/utils/sz'
echo '--------------begin-----------------------'
while [ $i -gt 0 ]
do
for file in $(ls $dir);
do
	i=$(($i-1))
	if [ $i -le 0 ]
	python /home/yhl2/workspace/xtp_test/utils/sz/$file
	then
	    break
	fi
done
done
echo '---------------end------------------------'