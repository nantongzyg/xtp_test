dir=./
 
for file in $dir/*.py; do
        python ${file#*//}
   
    done
