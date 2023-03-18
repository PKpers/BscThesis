#!/usr/bin/bash
check_exit(){
    local exit_stat=$1
    if [ $exit_stat -ne 0 ]; then
	exit
    fi
}

# Set up the testing
test="/home/kpapad/UG_thesis/Thesis/Bdt/src/TestSmeared.py"
dataset="WPhi_2mu_M50MixedDeltas_Application"
modelname="WPhi_2mu_M50MixedDeltas"
model="myModel"$modelname"_conf"11

# Setup plotting
plot="/home/kpapad/UG_thesis/Thesis/Bdt/src/plotResultsSmeared.py"
prediction=$dataset"Pred"
output_plot=$dataset"BDTplot.pdf"

# Test and plot
output_test=$dataset"Pred"
python $test $dataset $model $output_test 
ret=$?
check_exit $ret
python $plot $prediction $output_plot
ret=$?
check_exit $ret
