import time
with open('./tmp_data/one_hole_size_data.csv', 'r') as f1:
    x = 1.5
    y = 1.5

    lines = f1.readlines()
    new_lines = []
    for line in lines:
        new_lines.append(str(x) + ',' + str(y) + ',' + line)
        x = x + 1
        if (x > 48):
            x = 1.5
            y = y + 1
    
    with open('./tmp_data/one_hole_data.csv', 'w') as f1new:
        f1new.writelines(new_lines)
        f1new.close()
f1.close()
