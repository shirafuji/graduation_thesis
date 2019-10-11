# csvToVtk
# http://www.geocities.jp/penguinitis2002/study/ParaView/contour/contour.html

import sys
import os

def main():
	if len(sys.argv) < 2:
		print("csvToVtk <csv file>")
		sys.exit()
	
	# input
	filename = sys.argv[1]
	
	file = open(filename, "r")
	
	file.readline()
	
	x = []
	y = []
	value = []
	
	for line0 in file:
		line = line0[0:len(line0)-1]
		item = line.split(",")
		x.append(item[0])
		y.append(item[1])
		value.append(item[2])
	
	file.close()
	
	
	# output
	basename = os.path.splitext(filename)[0]
	
	file = open(basename + ".vtk", "w")
	
	file.write("# vtk DataFile Version 2.0\n")
	file.write(basename + "\n")
	file.write("ASCII\n")
	file.write("DATASET UNSTRUCTURED_GRID\n")
	
	file.write("POINTS %d float\n" % len(x))
	
	num = len(x)
	
	for i in range(0, num):
		file.write(x[i] + " " + y[i] + " 0\n")
	
	file.write("CELLS %d %d\n" % (num, 2*num))
	
	for i in range(0, num):
		file.write("1 %d\n" % i)
	
	file.write("CELL_TYPES %d\n" % num)
	
	for i in range(0, num):
		file.write("1\n")
	
	file.write("POINT_DATA %d\n" % num)
	file.write("SCALARS point_scalars float\n")
	file.write("LOOKUP_TABLE default\n")
	
	for i in range(0, num):
		file.write(value[i] + "\n")
	
	file.close()


if __name__ == "__main__":
	main()
