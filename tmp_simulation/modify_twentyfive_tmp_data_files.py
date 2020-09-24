import time
with open('./tmp_data/twentyfive_holes_size_data.csv', 'r') as f5:
    x = 3.5
    y = 3.5

    lines = f5.readlines()
    new_lines = []
    for line in lines:
        new_lines.append(str(x) + ',' + str(y) + ',' + line)
        x = x + 1
        if (x > 46):
            x = 3.5
            y = y + 1
    
    with open('./tmp_data/twentyfive_holes_data.csv', 'w') as f5new:
        f5new.writelines(new_lines)
        f5new.close()
f5.close()
