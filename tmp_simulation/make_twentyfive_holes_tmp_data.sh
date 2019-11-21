#! /bin/bash
gcc make_twentyfive_holes_tmp_data.c
for i in `seq 0 42`
do
  for j in `seq 0 42`
  do
    ./a.out 1 "$i" "$j"
  done
done