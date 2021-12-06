#! /bin/bash
for i in `seq 0 47`
do
  for j in `seq 0 47`
  do
    python make_one_hole_vibration_data.py "$i" "$j"
  done
done