#!/bin/bash
check_exit(){
    local exit_stat=$1
    if [ $exit_stat -ne 0 ]; then
	exit
    fi
}
get_dir(){
    local path=$1 #where to look for the dirs
    local name=$2 #the name of the dir to look for
    for dir in $path*; do
	if [[ $dir == *'_'$name'_'* ]]; then
	    dir_name=$dir #the value of this global variable is the wanted dir name 
	    return
	fi
    done
}


#names=('M-50')
DIR='/home/kpapad/UG_thesis/Thesis/Analysis/MC_Samples/'
indir=$DIR"/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8"
analysis='/home/kpapad/UG_thesis/Thesis/Analysis/src/DYJets_mkdata.py'
outName="DYJets_M50"

python $analysis $indir $outName 
ret=$?
check_exit $ret

