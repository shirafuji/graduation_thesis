#! /bin/bash
gcc make_half_one_hole_tmp_data.c
for i in `seq 0 21`
do
  for j in `seq 0 21`
  do
    ./a.out 1 "$i" "$j"
  done
done