#! /bin/bash
gcc make_half_four_holes_tmp_data.c
for i in `seq 0 20`
do
  for j in `seq 0 20`
  do
    ./a.out 1 "$i" "$j"
  done
done