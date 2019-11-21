#! /bin/bash
gcc make_four_holes_tmp_data.c
for i in `seq 0 43`
do
  for j in `seq 0 43`
  do
    ./a.out 1 "$i" "$j"
  done
done