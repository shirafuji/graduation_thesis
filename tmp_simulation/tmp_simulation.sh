#! /bin/bash
gcc fem.c
for filename in `ls ./../triangle/poly/*.ele`
do
./a.out "$filename" 1
done
