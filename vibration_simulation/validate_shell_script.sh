#! /bin/bash
for i in `seq 0 47`
do
  if [ $(($i % 2)) = 0 ]; then
    for j in `seq 0 47`
    do
      if [ $(($j % 2)) = 0 ]; then
        # python make_one_hole_vibration_data.py "$i" "$j"
        echo "$i $j"
      fi
    done
  fi
done