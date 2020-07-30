#!/bin/bash

dir=./

res="RESTART"
restart_files=()
i=0

for file in $dir/*.py; do
    file1=${file#*//}
    if [[ $file1 == *$res* ]]
    then
        restart_files[$i]=$file1
        let i++
    else
        python $file1
    fi
done

for restart_file in ${restart_files[@]}; do
    python $restart_file
done

