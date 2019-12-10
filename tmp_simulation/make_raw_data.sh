#! /bin/bash
for filename in ./tmp_data/one_hole_position_data.csv ./tmp_data/four_holes_position_data.csv ./tmp_data/nine_holes_position_data.csv ./tmp_data/sixteen_holes_position_data.csv ./tmp_data/twentyfive_holes_position_data.csv
do
python make_raw_data.py "$filename"
done
