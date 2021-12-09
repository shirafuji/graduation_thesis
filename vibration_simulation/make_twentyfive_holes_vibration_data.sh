#! /bin/bash
for i in `seq 0 43`
do
  if [ $(($i % 2)) = 0 ]; then
    for j in `seq 0 43`
    do
      if [ $(($j % 2)) = 0 ]; then
        python make_twentyfive_holes_vibration_data.py "$i" "$j"
      fi
    done
  fi
done