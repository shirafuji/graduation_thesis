#! /bin/bash
for i in `seq 0 46`
do
  for j in `seq 0 46`
  do
    python make_four_holes_vibration_data.py "$i" "$j"
  done
done