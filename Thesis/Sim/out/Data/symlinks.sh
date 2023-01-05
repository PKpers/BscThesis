#!/sbin/bash
destination="/home/kpapad/UG_thesis/Thesis/share/SimuData/"
path="/home/kpapad/UG_thesis/Thesis/Sim/out/Data/"
for file in *; do
    ln -sf $path$file $destination  
done
exit

