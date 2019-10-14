#! /bin/bash
for filename in `ls ./../triangle/poly/*.csv`
do
python csvToVtk.py "$filename"
done
