#!/usr/bin/bash
plot="/home/kpapad/UG_thesis/tutorial_scripts/MachineLearning/src/PlotData.py"
datasets=("69s2")
for dataset in "${datasets[@]}"; do
    python $plot $dataset $dataset
done
