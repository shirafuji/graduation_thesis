for a in range(45):
    for b in range(45):

        poly_file = './poly/nine_holes_' + str(a+1) + '_' + str(b+1) + '.poly'

        with open(poly_file, 'w') as f:
            # node
            text = '# node\n2500 2 1 0\n'
            f.write(text)

            x = 0.0
            y = 0.0
            for i in range(2500):
                text = str(i+1) + ' ' + str(x) + ' ' + str(y) + ' ' + '0\n'
                f.write(text)
                if (x == 49):
                    x = 0.0
                    y = y + 1.0
                else:
                    x = x + 1.0
            # segment
            text = '# segment\n4900 0\n'
            f.write(text)
            segment_number = 1
            for i in range(49):
                for j in range(49):
                    node_number = j * 50 + i + 1
                    text = str(segment_number) + ' ' + str(node_number) + ' ' + str(node_number+1) + '\n'
                    f.write(text)
                    segment_number = segment_number+1
                    text = str(segment_number) + ' ' + str(node_number) + ' ' + str(node_number+50) + '\n'
                    f.write(text)
                    segment_number = segment_number+1

            for i in range(49):
                node_number = 50 + i*50
                text = str(segment_number) + ' ' + str(node_number) + ' ' + str(node_number+50) + '\n'
                f.write(text)
                segment_number = segment_number + 1
            
            for i in range(49):
                node_number = 2451 + i
                text = str(segment_number) + ' ' + str(node_number) + ' ' + str(node_number+1) + '\n'
                f.write(text)
                segment_number = segment_number + 1


            # hole
            text = '# hole\n9\n'
            f.write(text)
            hole_count = 1
            for c in range(3):
                for d in range(3):
                    text = str(hole_count) + ' ' + str(a + 1.8 + c) + ' ' + str(b + 1.1 + d) + '\n'
                    f.write(text)
                    hole_count = hole_count + 1

