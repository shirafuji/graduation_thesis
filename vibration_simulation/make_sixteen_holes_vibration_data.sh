#! /bin/bash
for i in `seq 0 44`
do
  for j in `seq 0 44`
  do
    python make_sixteen_holes_vibration_data.py "$i" "$j"
  done
done