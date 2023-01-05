#!/usr/bin/bash
plot="/home/kpapad/UG_thesis/tutorial_scripts/MachineLearning/src/plotResults.py"
predictions=()
outputs=()
datasets=("49s2")
for dataset in "${datasets[@]}"; do
    prediction=$dataset"Conf9Pred"
    output=$dataset"Conf9BDTplot.pdf"
    python $plot $prediction $output
done

