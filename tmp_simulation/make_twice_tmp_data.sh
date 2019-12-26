#! /bin/bash
gcc make_twice_one_hole_tmp_data.c
for i in `seq 0 94`
do
  for j in `seq 0 94`
  do
    ./a.out 1 "$i" "$j"
  done
done

gcc make_twice_four_holes_tmp_data.c
for i in `seq 0 92`
do
  for j in `seq 0 92`
  do
    ./a.out 1 "$i" "$j"
  done
done