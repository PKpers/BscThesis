#!/usr/bin/bash
check_exit(){
    local exit_stat=$1
    if [ $exit_stat -ne 0 ]; then
	exit
    fi
}


# Set up smearing
smear="/home/kpapad/UG_thesis/Thesis/Analysis/src/WPhi_2mu_Smear.py"
dataset="WPhi_2mu_M25M30_Trimmed"
out="WPhi_2mu_M25M30_SmearBoth30"

# Run the smear module
python $smear $dataset $out 
ret=$?
check_exit $ret
