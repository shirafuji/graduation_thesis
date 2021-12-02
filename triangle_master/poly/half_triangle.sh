#! /bin/bash
for file_name in `ls half*.poly`
do
triangle -pqe "$file_name"
done
