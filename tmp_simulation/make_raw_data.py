import sys

args = sys.argv
read_file_path = args[1]
read_file_path_array = read_file_path.split("_")
write_file_path = ""
write_file_path_array = []
for i in range(len(read_file_path_array)):
    write_file_path_array.append(read_file_path_array[i])
    if i == 3:
        write_file_path_array.append("raw")
write_file_path = "_".join(write_file_path_array)

with open(read_file_path, mode='r') as fr:
    line = fr.readlines()
    with open(write_file_path, mode='a') as fw:
        for i in range(len(line)):
            line_array = line[i].split(',')
            line_array[0] = str(i)
            i += 1
            write_line = (',').join(line_array)
            print(write_line)
            fw.write(write_line)
