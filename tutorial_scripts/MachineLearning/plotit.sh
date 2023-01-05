#!/usr/bin/bash
plot="/home/kpapad/UG_thesis/tutorial_scripts/MachineLearning/src/plotResults.py"
predictions=()
outputs=()
for (( i=10 ; i<=10 ; i++));
do
    prediction="69s2Conf"$i"Pred"
    output="69s2Conf"$i"BDTplot.pdf"
    python $plot $prediction $output
done

