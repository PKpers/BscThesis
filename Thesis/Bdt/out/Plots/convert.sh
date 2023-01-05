#!/sbin/bash
for file in *.jpg; do
    len=${#file}
    last_string=$(($len-4))
    fname=${file:0:$last_string}
    convert $file $fname".jpeg"
done
