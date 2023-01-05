#!/usr/bin/bash
test="/home/kpapad/UG_thesis/tutorial_scripts/MachineLearning/src/Testing.py" 
datasets=("29s2" "39s2" "49s2" "59s2" "69s2")
bestModel="myModel49s2_conf9"
bestLessOVT="myModel49s2_conf10"
for dataset in "${datasets[@]}"; do
    python $test $dataset $bestModel $dataset"Pred"
    python $test $dataset $bestLessOVT $dataset"Pred"
done
