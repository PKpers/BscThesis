#!/usr/bin/bash
check_exit(){
    local exit_stat=$1
    if [ $exit_stat -ne 0 ]; then
	exit
    fi
}

train="/home/kpapad/UG_thesis/tutorial_scripts/MachineLearning/src/Training.py"
test="/home/kpapad/UG_thesis/tutorial_scripts/MachineLearning/src/Testing.py" 
dataset="69s2"
#configs=("training_conf1.dict" "training_conf2.dict" "training_conf3.dict" "training_conf5.dict")
configs=("training_conf10.dict")
#"training_conf10.dict" "training_conf11.dict" "training_conf12.dict" "training_conf13.dict" "training_conf14.dict" "training_conf15.dict")
k=10
for config in "${configs[@]}"; do
    model="myModel"$dataset"_conf"$k
    output=$dataset"Conf"$k"Pred"
    python $train $dataset $config
    ret=$?
    check_exit $ret
    python $test $dataset $model $output 
    ret=$?
    check_exit $ret
    k=$(($k+1))
done
