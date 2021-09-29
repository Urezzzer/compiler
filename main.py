from parser import *

import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 parser.py <input_file> <output_file>")
    else:
        p = Parser()
        p.parse(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
