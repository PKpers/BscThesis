#!/sbin/bash
destination="/home/kpapad/UG_thesis/Thesis/share/SimuData/"
path="/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
for file in *; do
    if [[ $file == ${0#*/} ]]; then # do not create symlink for the symlinks script
	continue
    fi
    ln -sf $path$file $destination  
done
exit

