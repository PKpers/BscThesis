#!/bin/bash
check_exit(){
    local exit_stat=$1
    if [ $exit_stat -ne 0 ]; then
	exit
    fi
}

names=('M-25' 'M-30' 'M-40' 'M-50')
DIR='/home/kpapad/UG_thesis/Thesis/Analysis/MC_Samples/'
plot='/home/kpapad/UG_thesis/Thesis/Analysis/src/WPhi_2mu_plot.py'
for name in "${names[@]}"; do
    dataset=WPhi_2mu_M"${name#*-}"
    echo 'Now working with '$dataset
    inFile=$dataset'Hist.root'
    outFile=$dataset'_MassHist.pdf'
    #echo input $inFile
    #echo $outFile
    python $plot $inFile $outFile 
    ret=$?
    check_exit $ret
done

