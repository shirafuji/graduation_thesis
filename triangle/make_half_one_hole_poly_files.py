for a in range(22):
    for b in range(22):

        poly_file = './poly/half_one_hole_' + str(a+1) + '_' + str(b+1) + '.poly'

        with open(poly_file, 'w') as f:
            # node
            text = '# node\n625 2 1 0\n'
            f.write(text)

            x = 0.0
            y = 0.0
            for i in range(625):
                text = str(i+1) + ' ' + str(x) + ' ' + str(y) + ' ' + '0\n'
                f.write(text)
                if (x == 24):
                    x = 0.0
                    y = y + 1.0
                else:
                    x = x + 1.0
            # segment
            text = '# segment\n1300 0\n'
            f.write(text)
            segment_number = 1
            for i in range(24):
                for j in range(24):
                    node_number = j * 25 + i + 1
                    text = str(segment_number) + ' ' + str(node_number) + ' ' + str(node_number+1) + '\n'
                    f.write(text)
                    segment_number = segment_number+1
                    text = str(segment_number) + ' ' + str(node_number) + ' ' + str(node_number+25) + '\n'
                    f.write(text)
                    segment_number = segment_number+1

            for i in range(24):
                node_number = 25 + i*25
                text = str(segment_number) + ' ' + str(node_number) + ' ' + str(node_number+25) + '\n'
                f.write(text)
                segment_number = segment_number + 1
            
            for i in range(24):
                node_number = 601 + i
                text = str(segment_number) + ' ' + str(node_number) + ' ' + str(node_number+1) + '\n'
                f.write(text)
                segment_number = segment_number + 1


            # hole
            text = '# hole\n1\n'
            f.write(text)
            text = '1 ' + str(a + 1.8) + ' ' + str(b + 1.1)
            f.write(text)

