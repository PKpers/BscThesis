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
names=('M-250')
DIR='/home/kpapad/UG_thesis/Thesis/Analysis/MC_Samples/'
analysis='/home/kpapad/UG_thesis/Thesis/Analysis/src/WPhi_2mu_mkdata.py'
for name in "${names[@]}"; do
    get_dir $DIR $name #every time this function runs the $dir_name var gets updated
    echo 'Now working in '$dir_name
    prefix=WPhi_2mu_M"${name#*-}"
    indir=$dir_name
    outName=$prefix
   # echo input $indir
   # echo $outName
    python $analysis $indir $outName 
    ret=$?
    check_exit $ret
done

