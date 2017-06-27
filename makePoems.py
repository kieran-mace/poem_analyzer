import sys
import os
import random

def main(argv):
    if len(argv) < 4:
        sys.stderr.write("Usage: %s text_input_file num_segments num_lines\n" % argv[0])
        return 1
    if not os.path.isfile(argv[1]):
        sys.stderr.write('Error: text_input %r was not found!\n' % argv[1])
        return 1
    if (int(argv[2]) < 0):
        sys.stderr.write('Can\'t produce %r poems! that is negative\n' % argv[2])
        return 1
    if (int(argv[3]) < 0):
        sys.stderr.write('lines must be positive\n' % argv[2])
        return 1

    #load arguments source
    file_name = sys.argv[1]
    num_poems = int(sys.argv[2])
    num_lines = int(sys.argv[3])

    # Load up source file
    infile = open(file_name,'rt')
    source = infile.readlines()
    source_length = len(source)


    for poem_num in range(num_poems):
        out_file = open('poem_' + str(poem_num),'w')
        start_point = random.choice(range(source_length-num_lines))
        end_pont = start_point + num_lines
        [out_file.write(source[i]) for i in range(start_point,end_pont)]
        out_file.close()

if __name__=='__main__':
    sys.exit(main(sys.argv))
