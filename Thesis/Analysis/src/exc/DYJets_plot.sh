#!/bin/bash
check_exit(){
    local exit_stat=$1
    if [ $exit_stat -ne 0 ]; then
	exit
    fi
}

DIR='/home/kpapad/UG_thesis/Thesis/Analysis/MC_Samples/'
plot='/home/kpapad/UG_thesis/Thesis/Analysis/src/WPhi_2mu_plot.py'
inFile="DYJets_M50Hist.root"
outFile="DYJetsM50_MassHist.pdf"
python $plot $inFile $outFile 
ret=$?
check_exit $ret

