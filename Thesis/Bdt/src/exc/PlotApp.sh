#!/usr/bin/bash
check_exit(){
    local exit_stat=$1
    if [ $exit_stat -ne 0 ]; then
	exit
    fi
}

# Set up the testing
num=12
dataset="WPhi_2mu_M50MixedDeltas_Application"
modelname="WPhi_2mu_M50MixedDeltas"
model="myModel"$modelname"_conf"$num

# Setup plotting
plot="/home/kpapad/UG_thesis/Thesis/Bdt/src/plotResultsSmeared.py"
prediction=$dataset"Pred"$num
output_plot=$dataset$num"BDTplot.pdf"

# Test and plot
output_test=$dataset"Pred"$num
python $plot $prediction $output_plot
ret=$?
check_exit $ret
