#! /bin/bash
for file_name in `ls twice*.poly`
do
triangle -pqe "$file_name"
done
