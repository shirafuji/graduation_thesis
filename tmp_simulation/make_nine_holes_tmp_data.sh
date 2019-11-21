#! /bin/bash
gcc make_nine_holes_tmp_data.c
for i in `seq 0 44`
do
  for j in `seq 0 44`
  do
    ./a.out 1 "$i" "$j"
  done
done