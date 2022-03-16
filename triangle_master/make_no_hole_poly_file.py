poly_file = './poly/no_hole.poly'

with open(poly_file, 'w') as f:
    # node
    text = '# node\n2601 2 1 0\n'
    f.write(text)

    x = 0.0
    y = 0.0
    for i in range(2601):
        text = str(i+1) + ' ' + str(x) + ' ' + str(y) + ' ' + '0\n'
        f.write(text)
        if (x == 50):
            x = 0.0
            y = y + 1.0
        else:
            x = x + 1.0
    # segment
    text = '# segment\n5100 0\n'
    f.write(text)
    segment_number = 1
    for i in range(50):
        for j in range(50):
            node_number = j * 51 + i + 1
            text = str(segment_number) + ' ' + str(node_number) + ' ' + str(node_number+1) + '\n'
            f.write(text)
            segment_number = segment_number+1
            text = str(segment_number) + ' ' + str(node_number) + ' ' + str(node_number+51) + '\n'
            f.write(text)
            segment_number = segment_number+1

    for i in range(50):
        node_number = 51 + i*51
        text = str(segment_number) + ' ' + str(node_number) + ' ' + str(node_number+51) + '\n'
        f.write(text)
        segment_number = segment_number + 1

    for i in range(50):
        node_number = 2551 + i
        text = str(segment_number) + ' ' + str(node_number) + ' ' + str(node_number+1) + '\n'
        f.write(text)
        segment_number = segment_number + 1


    # hole
    text = '# hole\n0\n'
    f.write(text)


