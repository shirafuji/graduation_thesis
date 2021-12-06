#! /bin/bash
for i in `seq 0 45`
do
  for j in `seq 0 45`
  do
    python make_nine_holes_vibration_data.py "$i" "$j"
  done
done