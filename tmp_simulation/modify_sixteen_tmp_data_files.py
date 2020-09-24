import time
with open('./tmp_data/sixteen_holes_size_data.csv', 'r') as f4:
    x = 3
    y = 3

    lines = f4.readlines()
    new_lines = []
    for line in lines:
        new_lines.append(str(x) + ',' + str(y) + ',' + line)
        x = x + 1
        if (x > 46):
            x = 3
            y = y + 1
    
    with open('./tmp_data/sixteen_holes_data.csv', 'w') as f4new:
        f4new.writelines(new_lines)
        f4new.close()
f4.close()
