#! /bin/bash
for i in `seq 0 43`
do
  for j in `seq 0 43`
  do
    python make_twentyfive_holes_vibration_data.py "$i" "$j"
  done
done